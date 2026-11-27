#!/usr/bin/env python3
"""Render a clean shot on an integer frame clock, then assemble the approved cut."""
import argparse
from fractions import Fraction
from functools import lru_cache
import json
import re
from pathlib import Path
import os
import subprocess as sp
import sys
import tempfile

from export_codec import encoder, ffmpeg_paths, h264, worker_options

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
RATE = 48000
C_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")

def probe(path):
    return json.loads(sp.check_output(["ffprobe", "-v", "error", "-show_streams",
                                      "-show_chapters", "-of", "json", str(path)]))

def plan():
    data = json.loads((ROOT / "cut.json").read_text(encoding="utf-8"))
    fps = data["fps"]
    if type(fps) is not int or fps not in (24, 25, 30, 50, 60):
        raise ValueError("fps 取 24 / 25 / 30 / 50 / 60")
    if not data.get("title") or not data["scenes"]:
        raise ValueError("cut.json 要有片名和至少一镜")
    seen = set()
    for s in data["scenes"]:
        k, n = s["id"], s["frames"]
        if k in seen or not C_ID.fullmatch(k) or type(n) is not int or n < 1:
            raise ValueError(f"无效或重复镜号 / 帧数：{k}")
        seen.add(k)
        captions = s.get("captions", [])
        old = 0
        for a,b,text in captions:
            if (type(a) is not int or type(b) is not int or not old <= a < b <= n
                or not text.strip() or "\n\n" in text):
                raise ValueError(f"{k}: 字幕必须按本镜帧编号排序，且不能叠压")
            old = b
        if any(type(v) is not int or not 0 <= v < n for v in s.get("cues", {}).values()):
            raise ValueError(f"{k}: cues 必须落在镜内")
    return data

def canvas(width):
    # The stock distribution build may already provide the bridge; in a
    # mismatched local build use the known ABI-compatible edition explicitly.
    if bridge := os.environ.get("CS336_GI_BRIDGE"):
        import gi
        if not Path(bridge).is_dir():
            raise ValueError("CS336_GI_BRIDGE 要指向含 _gi_cairo 的目录")
        gi.__path__.append(bridge)
    try:
        from visual import Canvas, Pango, PangoCairo, cairo, desc, background
        from scenes import draw
    except ImportError as e:
        raise RuntimeError(f"绘图需系统 Python / PyCairo / PangoCairo。若缺 gi._gi_cairo，请见工程说明：{e}") from e

    class Board(Canvas):
        # Fixed-em paths: labels keep their advances and baseline through zoom.
        @staticmethod
        @lru_cache(maxsize=512)
        def label_path(s, font, weight):
            c = cairo.Context(cairo.ImageSurface(cairo.FORMAT_A8, 1, 1))
            opts = cairo.FontOptions(hint_style=cairo.HINT_STYLE_NONE,
                                     hint_metrics=cairo.HINT_METRICS_OFF)
            c.set_font_options(opts)
            layout = PangoCairo.create_layout(c)
            context = layout.get_context()
            PangoCairo.context_set_font_options(context, opts)
            context.set_round_glyph_positions(False)
            context.set_language(Pango.Language.from_string("zh-cn"))
            f = "Latin Modern Roman, Noto Serif CJK SC" if font == "sans" else font
            layout.set_font_description(desc(128, f, weight))
            layout.set_text(s, -1)
            if layout.get_unknown_glyphs_count():
                raise ValueError(f"字体缺字：{s}")
            c.move_to(0,0)
            PangoCairo.layout_path(c, layout)
            ink, _ = layout.get_extents()
            return c.copy_path(), tuple(x/Pango.SCALE for x in (ink.x, ink.y, ink.width, ink.height))

        def text(self, s, x, y, size=36, color="#FFFFFF", alpha=1, align="center",
                 font="sans", weight="normal"):
            if not s or alpha <= 0 or size <= 0:
                return
            path, (left,top,w,h) = self.label_path(str(s),font,weight)
            c = self.c
            c.save()
            c.translate(x,y)
            c.scale(size/128, size/128)
            c.translate(-left-{"center":w/2,"right":w}.get(align,0),-top-h/2)
            c.new_path()
            c.append_path(path)
            self.source(color,alpha)
            c.fill()
            c.restore()

        def measure(self, s, size=36, font="sans", weight="normal"):
            return self.label_path(str(s), font, weight)[1][2] * size / 128

    s = cairo.ImageSurface(cairo.FORMAT_RGB24, width, width*9//16)
    g = Board(cairo.Context(s), s.get_width(), s.get_height())
    def paint(row, frame, fps):
        g.c.save()
        try:
            background(g)
            draw(g,row,frame,fps)
        finally:
            g.c.restore()
        s.flush()
        return s
    return paint

def shots_dir(width):
    return BUILD / "shots" / str(width)

def render_shot(row, fps, width, codec, paint):
    dest = shots_dir(width) / (row["id"] + ".mp4")
    dest.parent.mkdir(parents=True,exist_ok=True)
    exe, actual = encoder(codec)
    pix = "bgr0" if sys.byteorder == "little" else "0rgb"
    with tempfile.TemporaryDirectory(dir=dest.parent, prefix="expose-") as d:
        temp=Path(d)/"shot.mp4"
        cmd = [exe,"-v","error","-nostdin","-f","rawvideo","-pix_fmt",pix,"-s",f"{width}x{width*9//16}",
               "-r",str(fps),"-threads","1","-i","pipe:0","-filter_threads","1",
               "-vf","scale=out_color_matrix=bt709:out_range=tv,format=yuv420p","-an",
               *h264(actual,15),"-g",str(2*fps),"-profile:v","high","-video_track_timescale",str(256*fps),
               "-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709",
               "-color_range","tv",str(temp)]
        with sp.Popen(cmd,stdin=sp.PIPE, **worker_options()) as p:
            try:
                for i in range(row["frames"]):
                    p.stdin.write(paint(row,i,fps).get_data())
            finally:
                p.stdin.close()
            if p.wait():
                raise sp.CalledProcessError(p.returncode,cmd)
        verify_shot(temp,row,width,fps)
        temp.replace(dest)
    print(dest)

def verify_shot(path,row,width,fps):
    streams = probe(path)["streams"]
    if len(streams)!=1:
        raise ValueError(f"镜头应为无声画面：{path}")
    v = streams[0]
    found = (v["codec_name"],v.get("width"),v.get("height"),v.get("avg_frame_rate"),
             v.get("nb_frames"),v.get("time_base"),v.get("pix_fmt"),v.get("color_space"))
    expect = ("h264",width,width*9//16,f"{fps}/1",str(row["frames"]),f"1/{256*fps}","yuv420p","bt709")
    if found != expect:
        raise ValueError(f"{path.name} 的画面和 cut.json 不同；重画本镜。{found}")

def clock(num,fps,base):
    if base==100:
        # ASS stores centiseconds. Put each boundary between the last
        # preceding frame and the intended first frame, including end marks.
        t=round(Fraction(max(0,2*num-1)*base,2*fps))
    else:
        t=num*base//fps
    h,t=divmod(t,3600*base)
    m,t=divmod(t,60*base)
    s,f=divmod(t,base)
    return f"{h:02}:{m:02}:{s:02},{f:03}" if base==1000 else f"{h}:{m:02}:{s:02}.{f:02}"

def ffescape(s):
    return re.sub(r"([;#=\\])",r"\\\1",s.replace("\n"," "))

def sidecars(book,temp):
    fps=book["fps"]
    chapters=[";FFMETADATA1",f"title={ffescape(book['title'])}"]
    caps=[]; t=0; ch=[]
    for row in book["scenes"]:
        if row.get("chapter"):
            ch.append((t,row["chapter"]))
        caps.extend((t+a,t+b,s) for a,b,s in row.get("captions",[]))
        t+=row["frames"]
    for i,(a,title) in enumerate(ch):
        end=ch[i+1][0] if i+1<len(ch) else t
        chapters.extend(("[CHAPTER]",f"TIMEBASE=1/{fps}",f"START={a}",f"END={end}",
                        f"title={ffescape(title)}"))
    (temp/"chapters.ffmeta").write_text("\n".join(chapters)+"\n",encoding="utf-8")
    (temp/"captions.srt").write_text("\n\n".join(
        f"{j}\n{clock(a,fps,1000)} --> {clock(b,fps,1000)}\n{s}" for j,(a,b,s) in enumerate(caps,1))+"\n",
        encoding="utf-8")
    return t,caps,len(ch)

def write_ass(caps,fps,path):
    head="""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Chinese,Noto Serif CJK SC,58,&H00F4F4F4,&H00F4F4F4,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,1.6,0,2,96,96,58,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with path.open("w",encoding="utf-8") as f:
        f.write(head)
        for a,b,text in caps:
            text=text.replace("{","｛").replace("}","｝").replace("\\","＼").replace("\n",r"\N")
            f.write(f"Dialogue: 0,{clock(a,fps,100)},{clock(b,fps,100)},Chinese,,0,0,0,,{text}\n")

def fresh(path,suffix):
    p=path.expanduser().resolve()
    if p.exists() or p.suffix.lower()!=suffix:
        raise ValueError(f"选一个不存在的 {suffix} 文件：{p}")
    p.parent.mkdir(parents=True,exist_ok=True)
    return p

def audio_input(path,frames,fps,channels):
    s=probe(path)["streams"]
    if len(s)!=1 or s[0]["codec_type"]!="audio":
        raise ValueError("音轨输入使用单条 48 kHz WAV")
    a=s[0]
    duration=Fraction(a["duration_ts"])*Fraction(a["time_base"])
    if (a["sample_rate"]!=str(RATE) or a["channels"]!=channels or
        not a["codec_name"].startswith("pcm_") or duration!=Fraction(frames,fps)):
        raise ValueError(f"{path.name} 必须为 {channels} 声道、48 kHz PCM、整片同长（{frames/fps:g}秒）")

def ffpath(p):
    s=str(p)
    if "\n" in s or "\r" in s:
        raise ValueError("工程路径不能含换行")
    return s.replace("'","'\\''")

def concat_file(rows,paths,fps):
    text=["ffconcat version 1.0"]
    frames=offset=0
    for row,path in zip(rows,paths):
        frames+=row["frames"]
        end=round(Fraction(frames*1_000_000,fps))
        text.extend((f"file '{ffpath(path)}'",f"duration {(end-offset)/1e6:.6f}"))
        offset=end
    return "\n".join(text)+"\n"

def verify_clock(mp4,frames):
    dat=json.loads(sp.check_output(["ffprobe","-v","error","-select_streams","v:0","-show_packets",
        "-show_entries","packet=pts,duration","-of","json",str(mp4)]))
    ticks=sorted(p["pts"] for p in dat["packets"])
    if ticks!=list(range(0,frames*256,256)) or any(p.get("duration")!=256 for p in dat["packets"]):
        raise ValueError("装配时出现漏帧、重复帧或时码跳变")

def assemble(book,a):
    fps=book["fps"]
    out=fresh(a.out,".mp4")
    rows=book["scenes"]
    paths=[shots_dir(a.width)/(r["id"]+".mp4") for r in rows]
    for p,row in zip(paths,rows):
        if not p.is_file():
            raise ValueError(f"缺 {p.name}；先用相同宽度渲染本镜")
        verify_shot(p,row,a.width,fps)
    audio=[p.resolve(strict=True) for p in (a.mix,a.dialogue) if p]
    with tempfile.TemporaryDirectory(prefix="edit-",dir=BUILD) as d:
        p=Path(d)
        frames,caps,chapters=sidecars(book,p)
        if a.burn and not caps:
            raise ValueError("没有可压印的字幕")
        for i,n in enumerate(audio):
            audio_input(n,frames,fps,2-i)
        (p/"shots.ffconcat").write_text(concat_file(rows,paths,fps),encoding="utf-8")
        if a.burn:
            exe, chosen=encoder(a.codec)
        else:
            exe=ffmpeg_paths()[0]
        opts=[exe,"-v","error","-nostdin","-f","concat","-safe","0","-i","shots.ffconcat"]
        maps=["-map","0:v:0"]
        if a.burn:
            write_ass(caps,fps,p/"captions.ass")
            video=["-filter_threads","2","-vf","ass=filename=captions.ass",*h264(chosen,15),
                   "-colorspace","bt709","-color_range","tv"]
        else:
            video=["-c:v","copy"]
        for i,n in enumerate(audio):
            opts+=["-i",str(n)]
            maps+=["-map",f"{i+1}:a:0"]
        i=len(audio)+1
        if caps and not a.burn:
            opts+=["-i","captions.srt"]
            maps+=["-map",f"{i}:s:0","-c:s","mov_text","-metadata:s:s:0","language=zho"]
            i+=1
        opts+=["-f","ffmetadata","-i","chapters.ffmeta"]
        extra=[]
        if audio:
            extra=["-c:a","aac","-b:a:0","224k","-metadata:s:a:0","handler_name=旁白与配乐"]
            if len(audio)==2:
                extra+=["-b:a:1","144k","-metadata:s:a:1","handler_name=纯旁白","-disposition:a:1","0"]
        dest=p/"assembled.mp4"
        sp.run([*opts,*maps,*video,*extra,"-map_metadata",str(i),"-map_chapters",str(i),
                "-video_track_timescale",str(256*fps),"-movflags","+faststart",str(dest)],
               cwd=p,check=True,**worker_options())
        info=probe(dest)
        vs,=[x for x in info["streams"] if x["codec_type"]=="video"]
        assert int(vs["nb_frames"])==frames and vs["avg_frame_rate"]==f"{fps}/1"
        assert len(info["chapters"])==chapters
        assert sum(x["codec_type"]=="audio" for x in info["streams"])==len(audio)
        assert sum(x["codec_type"]=="subtitle" for x in info["streams"])==int(bool(caps) and not a.burn)
        verify_clock(dest,frames)
        meta=BUILD/"previews"/a.scene if a.scene else BUILD
        meta.mkdir(parents=True,exist_ok=True)
        (meta/"captions.srt").write_bytes((p/"captions.srt").read_bytes())
        (meta/"chapters.ffmeta").write_bytes((p/"chapters.ffmeta").read_bytes())
        # The output may be on another volume.
        import shutil
        shutil.move(dest,out)
    print(out)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    subs=p.add_subparsers(dest="action",required=True)
    subs.add_parser("list")
    still=subs.add_parser("still");still.add_argument("scene");still.add_argument("frame",type=int)
    still.add_argument("--out",required=True,type=Path)
    shot=subs.add_parser("shot");shot.add_argument("scene",nargs="+")
    edit=subs.add_parser("assemble");edit.add_argument("--out",required=True,type=Path)
    edit.add_argument("--scene",help="只导出一镜样片；字幕和音轨从本镜 0 起")
    audio=edit.add_mutually_exclusive_group(required=True)
    audio.add_argument("--silent",action="store_true");audio.add_argument("--mix",type=Path)
    edit.add_argument("--dialogue",type=Path)
    edit.add_argument("--burn",action="store_true")
    for s in (still,shot,edit):
        s.add_argument("--width",type=int,default=1920)
    for s in (shot,edit):
        s.add_argument("--codec",choices=("nvenc","cpu"),default="nvenc")
    a=p.parse_args()
    data=plan();fps=data["fps"];rows={s["id"]:s for s in data["scenes"]}
    if a.action=="list":
        if data.get("demo"):print("示范工程 · 等量平移 logits")
        offset=0
        for k,s in rows.items():
            print(k,offset,s["frames"],s.get("chapter",""),sep="\t")
            offset+=s["frames"]
        return
    if a.width%32 or not 320<=a.width<=3840:
        p.error("宽度用 320–3840 间的 32 倍数（YUV 4:2:0 要求偶数高度）")
    if a.action=="assemble":
        if a.dialogue and not a.mix:p.error("--dialogue 需要 --mix")
        if a.scene:
            if a.scene not in rows:p.error("样片镜号不在 cut.json")
            data={**data,"scenes":[rows[a.scene]]}
        assemble(data,a)
    elif a.action=="still":
        if a.scene not in rows or not 0<=a.frame<rows[a.scene]["frames"]:
            p.error("镜号 / 帧号不在 cut.json")
        dest=fresh(a.out,".png")
        canvas(a.width)(rows[a.scene],a.frame,fps).write_to_png(str(dest));print(dest)
    else:
        ids=list(rows) if a.scene==["all"] else a.scene
        if any(x not in rows for x in ids):p.error("镜号不在 cut.json")
        paint=canvas(a.width)
        for k in ids:render_shot(rows[k],fps,a.width,a.codec,paint)

if __name__=="__main__":
    main()
