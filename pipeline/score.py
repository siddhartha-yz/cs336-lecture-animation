#!/usr/bin/env python3
"""Validate score prompts; render with the private Stable Audio 3 Medium runtime."""
import argparse
import json
from pathlib import Path
import re
import sys
import time

MODEL = "stabilityai/stable-audio-3-medium"
SAMPLE_RATE = 44100
MAX_SECONDS = 380
CUE = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}\Z")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(plan):
    if plan.get("model") != MODEL or not str(plan.get("global_musical_key", "")).strip():
        raise ValueError("指定 Stable Audio 3 Medium 与全片关系调")
    tracks, sfx = plan.get("tracks"), plan.get("sfx", [])
    if not isinstance(tracks, list) or not tracks or not isinstance(sfx, list):
        raise ValueError("music.json 至少要有一条乐段")
    cues = tracks + sfx
    seen = set()
    for cue in cues:
        key, seconds, seeds, prompt = (cue[k] for k in ("id", "duration_seconds", "preview_seeds", "prompt"))
        if not CUE.fullmatch(key) or key in seen:
            raise ValueError(f"{key}: 乐段号重复或不合法")
        seen.add(key)
        if type(seconds) is not int or not 1 <= seconds <= MAX_SECONDS:
            raise ValueError(f"{key}: 长轨需在 1–{MAX_SECONDS}s；长乐章拆乐段，不截断或循环")
        if (not isinstance(seeds, list) or len(seeds) != 3 or
            not all(type(s) is int and 0 <= s < 2**31 for s in seeds) or len(set(seeds)) != 3):
            raise ValueError(f"{key}: 每段恰好三个不同整数试听种子")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError(f"{key}: 缺配乐提示词")
        if cue in tracks and not prompt.startswith("TrackType: Music, VocalType: Instrumental"):
            raise ValueError(f"{key}: 乐章保留明确的纯器乐前缀")
    return cues


def choose(cues, only):
    by_id = {c["id"]: c for c in cues}
    if only:
        unknown = set(only) - by_id.keys()
        if unknown:
            raise ValueError(f"未知提示：{sorted(unknown)}")
        return [c for c in cues if c["id"] in only]
    return cues


def remember(out, cues):
    content = {c["id"]: {"seeds": c["preview_seeds"], "prompt": c["prompt"]} for c in cues}
    out.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock = out / "preview-lock.json"
    if not lock.exists():
        with lock.open("x", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
            f.write("\n")
    elif read(lock) != content:
        raise ValueError("已有试听对应别的提示词或种子；请用新的私有输出目录")


def render(a, cues, shortlist):
    import numpy as np
    import soundfile as sf

    def valid(path, seconds):
        if not path.is_file():
            return False
        i = sf.info(path)
        return (i.format, i.subtype, i.samplerate, i.channels, i.frames) == (
            "WAV", "PCM_24", SAMPLE_RATE, 2, SAMPLE_RATE * seconds)

    remember(a.out, cues)
    jobs = []
    choices = read(a.choices) if a.mode == "masters" else None
    for cue in shortlist:
        key, seeds = cue["id"], cue["preview_seeds"]
        if a.mode == "masters":
            selected = choices.get(key)
            if not isinstance(selected, list) or not 1 <= len(selected) <= 2 or len(set(selected)) != len(selected) or not set(selected) <= set(seeds):
                raise ValueError(f"{key}: 从三个试听种子中选 1–2 个")
            for seed in selected:
                if not valid(a.out / "previews" / key / f"{seed}.wav", 30):
                    raise ValueError(f"{key}: 找不到同方案的 30 秒试听 {seed}")
            folder, seconds = "long_candidates", cue["duration_seconds"]
        else:
            folder, seconds, selected = "previews", 30, seeds
        jobs.extend((cue, seed, seconds, a.out / folder / key / f"{seed}.wav") for seed in selected)
    pending = [j for j in jobs if not valid(j[3], j[2])]
    if not pending:
        print("本轮 WAV 已齐，无需重跑")
        return

    import os
    import torch
    from flash_attn import flash_attn_func
    from stable_audio_3 import StableAudioModel

    if os.environ.get("HF_HUB_OFFLINE") != "1" or torch.cuda.device_count() != 1:
        raise ValueError("请在已授权服务器上明确选择一个 CUDA 设备并使用离线模型缓存")
    probe = torch.ones(1, 8, 2, 64, device="cuda", dtype=torch.float16)
    if not torch.allclose(flash_attn_func(probe, probe, probe), probe):
        raise ValueError("现用 FlashAttention 自检未通过")
    model = StableAudioModel.from_pretrained("medium", device="cuda")
    config = model.model_config
    if (config["sample_rate"], config["audio_channels"]) != (SAMPLE_RATE, 2):
        raise ValueError("当前不是验证过的 44.1 kHz 立体声 Medium 模型")
    cap = config["sample_size"]
    for cue, seed, seconds, path in pending:
        if seconds * SAMPLE_RATE > cap:
            raise ValueError(f"{cue['id']}: 超过当前模型的实际采样上限")
        started = time.monotonic()
        print(f"{a.mode} {cue['id']} {seed} {seconds}s", flush=True)
        audio = model.generate(prompt=cue["prompt"], duration=seconds, seed=seed, sample_size=cap)
        samples = audio[0].transpose(0, 1).contiguous().cpu().numpy()
        if samples.shape != (seconds * SAMPLE_RATE, 2) or not np.isfinite(samples).all():
            raise ValueError(f"{cue['id']}: 生成音频时钟或采样异常")
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".part")
        sf.write(tmp, samples, SAMPLE_RATE, format="WAV", subtype="PCM_24")
        if not valid(tmp, seconds):
            raise ValueError(f"{cue['id']}: 写出的 WAV 无法回读")
        tmp.replace(path)
        with (a.out / "render-log.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps({"id": cue["id"],"seed": seed,"seconds": seconds,
                "path": str(path.relative_to(a.out)), "elapsed_s": round(time.monotonic()-started, 2)})+"\n")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode", choices=("check", "previews", "masters"))
    p.add_argument("--project", required=True, type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--choices", type=Path)
    p.add_argument("--only", nargs="+")
    a = p.parse_args()
    try:
        cues = validate(read(a.project))
        shortlist = choose(cues, a.only)
        if a.mode == "check":
            print(f"{len(shortlist)} 个乐段 · 每段 3 个不同试听种子")
            return
        if not a.out or (a.mode == "masters" and not a.choices):
            p.error("渲染需 --out；长轨还需 --choices")
        import os
        os.umask(0o077)
        render(a, cues, shortlist)
    except (ValueError, TypeError, KeyError, OSError) as e:
        p.exit(1, f"{e}\n")


if __name__ == "__main__":
    main()
