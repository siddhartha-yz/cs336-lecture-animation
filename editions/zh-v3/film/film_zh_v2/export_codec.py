"""Select a working encoder for this edit, without changing the desktop GPU."""
import os
import shutil
import subprocess
import sys
from functools import lru_cache
from pathlib import Path


def quiet_encoder():
    """Child-side only: leave the workstation responsive during long exports."""
    if hasattr(os, 'nice'):
        os.nice(max(0, 15 - os.nice(0)))
    if hasattr(os, 'sched_getaffinity'):
        allowed = os.sched_getaffinity(0)
        cpu = max(allowed)
        core = {cpu}
        topology = Path(f'/sys/devices/system/cpu/cpu{cpu}/topology/thread_siblings_list')
        if topology.is_file():
            for group in topology.read_text().strip().split(','):
                first, _, last = group.partition('-')
                core.update(range(int(first), int(last or first) + 1))
        os.sched_setaffinity(0, allowed & core)


def worker_options():
    return {'preexec_fn': quiet_encoder} if os.name == 'posix' else {}


@lru_cache(maxsize=None)
def encoder(mode='auto'):
    if mode not in ('auto', 'nvenc', 'cpu'):
        raise ValueError(mode)
    # A bundled ffmpeg can precede the distribution build and omit NVENC.
    override = os.environ.get('CS336_FFMPEG')
    paths = [shutil.which(override)] if override else ['/usr/bin/ffmpeg', shutil.which('ffmpeg')]
    paths = list(dict.fromkeys(p for p in paths if p and os.access(p, os.X_OK)))
    if not paths:
        raise SystemExit('未找到可执行的 FFmpeg。')
    if mode != 'cpu':
        for exe in paths:
            # Exercise the actual driver, not just the compiled-in encoder list.
            probe = [exe, '-v', 'error', '-nostdin', '-f', 'lavfi', '-i',
                     'color=size=256x144:rate=30', '-filter_threads', '1', '-frames:v', '1',
                     '-c:v', 'h264_nvenc', '-gpu', '0', '-preset', 'p5', '-f', 'null', '-']
            check = subprocess.run(probe, capture_output=True, text=True, **worker_options())
            if check.returncode == 0:
                print(f'视频编码：NVIDIA NVENC · {exe}', file=sys.stderr, flush=True)
                return exe, 'nvenc'
        if mode == 'nvenc':
            raise SystemExit('NVIDIA NVENC 初始化失败：' + check.stderr.strip())
    print(f'视频编码：CPU x264（低优先级）· {paths[0]}', file=sys.stderr, flush=True)
    return paths[0], 'cpu'


def h264(codec, quality):
    if codec == 'nvenc':
        return ['-c:v', 'h264_nvenc', '-gpu', '0', '-preset', 'p5', '-tune', 'hq',
                '-rc:v', 'vbr', '-cq:v', str(quality), '-b:v', '0', '-bf', '3']
    return ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-threads:v', '2',
            '-preset', 'veryfast', '-crf', str(quality)]
