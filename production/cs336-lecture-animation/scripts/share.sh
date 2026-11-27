#!/usr/bin/env bash
# v6.2 sharing recipe: keep pixels, frame rate and chapter clock.
set -euo pipefail
usage() { printf '%s\n' '用法：share.sh audible|silent 字幕压印版.mp4 新分享版.mp4 [CQ=25]' >&2; exit 2; }
[[ $# -ge 3 && $# -le 4 ]] || usage
mode=$1;in=$2;out=$3;cq=${4:-25}
[[ -f "$in" && ! -e "$out" && "$out" == *.mp4 && "$cq" =~ ^[0-9]+$ ]] || usage
ff=${CS336_FFMPEG:-/usr/bin/ffmpeg}
[[ -x "$ff" ]] || { echo 'CS336_FFMPEG 要指向可工作的 FFmpeg 可执行文件' >&2; exit 2; }
if [[ -n "$(ffprobe -v error -select_streams s -show_entries stream=index -of csv=p=0 "$in")" ]]; then
    echo '先压印字幕，再用这个入口生成单文件分享版' >&2; exit 2
fi
case "$mode" in
    audible) audio=(-map 0:a:0 -c:a copy);;
    silent) audio=(-an);;
    *) usage;;
esac
mkdir -p -- "$(dirname -- "$out")"
tmp=$(mktemp -d "$(dirname -- "$out")/share.XXXXXX")
trap 'rm -f -- "$tmp/share.mp4"; rmdir -- "$tmp"' EXIT
nice -n 14 "$ff" -v error -nostdin -n \
  -hwaccel cuda -hwaccel_output_format cuda -i "$in" \
  -map 0:v:0 "${audio[@]}" -map_chapters 0 \
  -c:v h264_nvenc -preset p6 -tune hq -rc vbr -cq "$cq" -b:v 0 -multipass qres -rc-lookahead 32 \
  -spatial-aq 1 -aq-strength 6 -temporal-aq 1 -g 240 -bf 3 -b_ref_mode middle -profile:v high \
  -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -fps_mode passthrough -movflags +faststart "$tmp/share.mp4"
mv -n -- "$tmp/share.mp4" "$out"
printf '%s\n' "$out"
