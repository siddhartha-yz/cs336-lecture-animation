"""Mix the five approved OST recordings against cut.json, touching only the music bus."""
import argparse
import json
import math
import re
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import lfilter

SR = 48000


def ffmpeg(*args, measure=False):
    cmd = ["ffmpeg", "-hide_banner", "-nostdin", "-nostats", "-v", "info" if measure else "error", *map(str, args)]
    result = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stderr


def db(gain):
    return 10.0 ** (gain / 20.0)


def sample(t):
    return round(t * SR)


def lengths(file, frames, channels):
    info = sf.info(file)
    if (info.samplerate, info.frames, info.channels) != (SR, frames, channels):
        raise ValueError(f"Unexpected sample clock: {info}")


def extract_dialogue(master, output, frames, fps, samples):
    # No arbitrary resampling of a mismatched master. Strip only the AAC
    # encoder's decoded padding from the matching 48 kHz mono track.
    data=subprocess.check_output(["ffprobe","-v","error","-show_streams","-of","json",str(master)],text=True)
    streams=json.loads(data)["streams"]
    v=next((row for row in streams if row["codec_type"]=="video"),None)
    aud=[row for row in streams if row["codec_type"]=="audio"]
    if (not v or v.get("nb_frames")!=str(frames) or v.get("avg_frame_rate")!=f"{fps}/1"
        or len(aud)<2 or aud[1].get("channels")!=1 or aud[1].get("sample_rate")!=str(SR)):
        raise ValueError("Use this cut's 60 fps master with the 48 kHz mono narration as its second audio track.")
    ffmpeg("-n","-i",master,"-map","0:a:1","-af",f"atrim=end_sample={samples}",
           "-c:a","pcm_s16le",output)
    lengths(output,samples,1)
    return output


def loudness(file):
    log = ffmpeg("-i", file, "-af", "ebur128=peak=true:framelog=verbose", "-f", "null", "-", measure=True)
    summary = log.rsplit("Summary:", 1)[1]
    i = float(re.search(r"\bI:\s+(-?[\d.]+)\s+LUFS", summary)[1])
    p = float(re.search(r"\bPeak:\s+(-?[\d.]+)\s+dBFS", summary)[1])
    return {"lufs": i, "dbtp": p}


def phase(t):
    return 0.5 - 0.5 * np.cos(np.pi * np.clip(t, 0, 1))


def biquad(eq):
    a = 10 ** (eq["db"] / 40)
    w = 2 * np.pi * eq["frequency"] / SR
    c, s = np.cos(w), np.sin(w)
    if eq["type"] == "bell":
        alpha = s / (2 * eq["q"]) if "q" in eq else s*np.sinh(np.log(2)/2*eq["widthOctaves"]*w/s)
        b0, b1, b2 = 1 + alpha*a, -2*c, 1 - alpha*a
        a0, a1, a2 = 1 + alpha/a, -2*c, 1 - alpha/a
    elif eq["type"] == "lowShelf":
        v = np.sqrt(2*a)*s
        b0, b1, b2 = a*((a+1)-(a-1)*c+v), 2*a*((a-1)-(a+1)*c), a*((a+1)-(a-1)*c-v)
        a0, a1, a2 = (a+1)+(a-1)*c+v, -2*((a-1)+(a+1)*c), (a+1)+(a-1)*c-v
    else:
        raise ValueError(eq["type"])
    return np.array([b0,b1,b2])/a0, np.array([a0,a1,a2])/a0


def duck_envelope(voice, spec):
    # A bounded gain controller keyed only by the dry voice. At rest the score
    # returns to its previous level; music-only holds are not normalized down.
    k = sample(0.01)
    z = np.pad(voice, (0, (-len(voice)) % k)).reshape(-1, k)
    rms = np.sqrt(np.mean(z*z, axis=1))
    target = spec["maxDb"] * phase((20*np.log10(np.maximum(rms,1e-9))+45)/15)
    attack = -math.expm1(-0.01 / spec["attackSeconds"])
    release = -math.expm1(-0.01 / spec["releaseSeconds"])
    d = np.empty_like(target)
    state = 0.
    for i, want in enumerate(target):
        state += (attack if want > state else release) * (want - state)
        d[i] = state
    return np.arange(len(d))*k+k//2, d


def stereo_samples(file):
    info=sf.info(file)
    if info.channels != 2:
        raise ValueError(f"Expected approved stereo source: {file}")
    data=subprocess.check_output(["ffmpeg","-hide_banner","-nostdin","-v","error","-i",str(file),
                                  "-ar",str(SR),"-f","f32le","-"])
    track=np.frombuffer(data,dtype="<f4").reshape(-1,2)
    if len(track)!=round(info.frames*SR/info.samplerate):
        raise ValueError(f"Resampled source clock mismatch: {file}, {len(track)}")
    return track


def overlap(left,right,frames):
    if len(left)<frames or len(right)<frames:
        raise ValueError("Not enough source for a musical crossfade.")
    phi=np.linspace(0,np.pi/2,frames,dtype=np.float32)[:,None]
    return left[-frames:]*np.cos(phi)+right[:frames]*np.sin(phi)


def build_bed(tracks, cfg, index, n, spp, voice_end, bed_file):
    # Explicit sample-count edits and overlaps, independent of decoder packets.
    starts=[index[t["scene"]][0]*spp for t in cfg["tracks"]]
    cross=sample(cfg["crossfadeSeconds"])
    ends=[t+cross for t in starts[1:]]+[n]
    bed=np.zeros((n,2),dtype=np.float32)
    for i,(t,start,end) in enumerate(zip(cfg["tracks"],starts,ends,strict=True)):
        z=stereo_samples(tracks/t["file"])
        keep=end-start
        if i==0:
            op=cfg["opening"]
            cut_at=index[op["scene"]][0]*spp
            omitted=op["removedFrames"]*spp
            f=sample(op["seamSeconds"])
            if not 0<f<cut_at<cut_at+omitted<keep+omitted<=len(z):
                raise ValueError("Opening score jump falls outside the M1 selection.")
            left=z[:cut_at]
            right=z[cut_at+omitted-f:keep+omitted]
            take=np.concatenate((left[:-f],overlap(left,right,f),right[f:]))
        elif i==4:
            c=cfg["coda"]
            last=voice_end+sample(c["afterVoiceSeconds"])
            from_src=sample(c["sourceInSeconds"])
            chord=sample(c["sourceChordSeconds"])
            switch=last-(chord-from_src)
            xf=sample(c["crossfadeSeconds"])
            b=sample(t["sourceInSeconds"])
            first_end=b+switch-start+xf
            last_end=from_src+n-switch
            if not(start<switch<voice_end<last<n and max(first_end,last_end)<=len(z)):
                raise ValueError("The M5 coda does not fit the current narration and frame clock.")
            left=z[b:first_end]
            right=z[from_src:last_end]
            take=np.concatenate((left[:-xf],overlap(left,right,xf),right[xf:]))
        else:
            b=sample(t.get("sourceInSeconds",0))
            take=z[b:b+keep]
        if len(take)!=keep:
            raise ValueError(f"Length mismatch inside {t['file']}: expected {keep}, got {len(take)}")
        if i==0:bed[start:end]=take
        else:
            bed[start:start+cross]=overlap(bed[:start+cross],take,cross)
            bed[start+cross:end]=take[cross:]
        del take,z
    eq=dict(cfg["baseEq"],type="bell")
    b,aa=biquad(eq)
    zi=np.zeros((2,2))
    with sf.SoundFile(bed_file,"x",SR,2,"FLOAT") as w:
        for l in range(0,n,SR*5):
            q,zi=lfilter(b,aa,bed[l:l+SR*5],axis=0,zi=zi)
            w.write(q.astype("float32"))
    lengths(bed_file,n,2)
    return {"start_samples":starts,"chord_sample":last,"coda_stage_sample":switch,
            "source_chord_sample":chord,"score_end_sample":last_end}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tracks",type=Path,required=True,help="Directory with the five approved scores and chime.")
    input_group=ap.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--dialogue",type=Path,help="Mono WAV on the current cut clock, including silent outro.")
    input_group.add_argument("--master",type=Path,help="Matching video master; the second audio track is isolated narration.")
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--cut",type=Path,default=Path("src/data/cut.json"))
    ap.add_argument("--config",type=Path,default=Path("src/data/ost.json"))
    a=ap.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    cuts=json.loads(a.cut.read_text())
    cfg=json.loads(a.config.read_text())
    index={};f=0
    fps=cuts["fps"]
    if SR%fps:
        raise ValueError("48 kHz must divide evenly into video frames.")
    spp=SR//fps
    for scene in cuts["scenes"]:
        index[scene["id"]]=(f,scene);f+=scene["frames"]
    n=f*spp
    source=a.dialogue if a.dialogue else extract_dialogue(a.master,a.out/"dialogue.wav",f,fps,n)
    lengths(source,n,1)
    voice,_=sf.read(source,dtype="float32")
    active=np.flatnonzero(np.abs(voice[-sample(10):])>db(-55))
    if not active.size:
        raise ValueError("No closing voice above -55 dBFS in the last ten seconds.")
    ve=n-sample(10)+int(active[-1])
    if not 3.5<=(n-ve)/SR<=4:
        raise ValueError(f"Closing pause must be 3.5–4.0 s, found {(n-ve)/SR:.3f} s.")
    bed_file=a.out/"score-aligned.wav"
    bed_report=build_bed(a.tracks,cfg,index,n,spp,ve,bed_file)
    bed,_=sf.read(bed_file,dtype="float32")
    modifications=[]
    for q in cfg["scoreEdits"]:
        def at(pair):
            return (index[pair[0]][0]+pair[1])*spp
        l,r=at(q["start"]),at(q["end"])
        ramp=sample(q["rampSeconds"])
        if not 0<=l<l+2*ramp<r<=n:
            raise ValueError(f"Bad music edit: {q['movement']}")
        pos=np.arange(r-l,dtype=np.float32)
        wet=(phase(pos/ramp)*phase((len(pos)-1-pos)/ramp))[:,None]
        b,aa=biquad(q["eq"])
        pad=max(0,l-sample(0.18))
        filtered=lfilter(b,aa,bed[pad:r],axis=0)[l-pad:].astype("float32")
        patch=bed[l:r]
        dry_rms=float(np.sqrt(np.mean(patch[ramp:-ramp]**2)))
        patch+=(filtered-patch)*wet
        patch*=db(q["db"]*wet)
        changed_rms=float(np.sqrt(np.mean(patch[ramp:-ramp]**2)))
        modifications.append(dict(movement=q["movement"],seconds=[l/SR,r/SR],
             full_gain_db=q["db"],eq=q["eq"],measured_music_rms_delta_db=round(20*np.log10(changed_rms/dry_rms),3)))
    for q in (a.out/"pre-peak.wav",a.out/"mix.wav",a.out/"music-only.wav"):
        if q.exists():
            raise FileExistsError(str(q))
    sfx_path=a.tracks/cfg["chime"]["file"]
    sfx_raw=subprocess.check_output(["ffmpeg","-hide_banner","-nostdin","-v","error","-i",str(sfx_path),"-ar",str(SR),"-ac","2","-f","f32le","-"])
    chime=np.frombuffer(sfx_raw,dtype="<f4").reshape(-1,2)*db(cfg["mixDb"]["chime"])
    cues=[]
    for k in cfg["chime"]["scenes"]:
        start,row=index[k]
        hit=(start+row["cues"]["chime"])*spp
        if hit-(start+row["speech_end"])*spp!=sample(.15):
            raise ValueError(f"Chime no longer follows the question: {k}")
        cues.append((k,hit))
    kp,duck=duck_envelope(voice,cfg["ducking"])
    tail=sample(cfg["coda"]["fadeToBlackSeconds"])
    g=float(db(cfg["mixDb"]["score"]))
    gv=float(db(cfg["mixDb"]["dialogue"]))
    pre=a.out/"pre-peak.wav"
    with sf.SoundFile(pre,"x",SR,2,"FLOAT") as w, sf.SoundFile(a.out/"music-only.wav","x",SR,2,"PCM_24") as music:
        for l in range(0,n,SR*5):
            r=min(n,l+SR*5)
            pos=np.arange(l,r)
            shaped=bed[l:r]*(g*db(-np.interp(pos,kp,duck))*phase((n-1-pos)/tail))[:,None]
            music.write(shaped)
            summed=voice[l:r,None]*gv+shaped
            for _,hit in cues:
                lo,hi=max(hit,l),min(hit+len(chime),r)
                if lo<hi:
                    summed[lo-l:hi-l]+=chime[lo-hit:hi-hit]
            w.write(summed)
    measured=loudness(pre)
    processing=[]
    if measured["dbtp"]>-1.0:
        processing=["-af",f"aresample=192000,alimiter=limit=.875:attack=5:release=80:level=false:latency=true,aresample=48000,apad=whole_len={n},atrim=end_sample={n}"]
    out=a.out/"mix.wav"
    ffmpeg("-n","-i",pre,*processing,"-c:a","pcm_s24le",out)
    lengths(out,n,2)
    actual=loudness(out)
    if actual["dbtp"]>-1:
        raise ValueError(f"True-peak ceiling missed: {actual}")
    result=dict(frames=f, samples=n, audio=dict(base=measured,final=actual,limited=bool(processing)),
      voice_end=ve/SR, tail_after_voice=(n-ve)/SR,
      bed=bed_report, music_edits=modifications, duck_ceiling_measured=float(max(duck)),
      chimes=[dict(scene=k,second=i/SR) for k,i in cues])
    print(json.dumps(result,indent=2),flush=True)
    (a.out/"mix-report.json").write_text(json.dumps(result,indent=2)+"\n")


if __name__=="__main__":
    main()
