#!/usr/bin/env python3
"""查看、重画或用已有镜头装配《能力的影子》；从任意目录运行。"""
from pathlib import Path
import argparse,sys,math
ROOT=Path(__file__).resolve().parent
WORK=ROOT/'film/film_zh_v6'; BUILD=ROOT/'build'
sys.path.insert(0,str(WORK))
from edition4 import book,mm
def fresh(value,ext):
 p=Path(value).expanduser().resolve()
 if p.suffix.lower()!=ext:raise SystemExit('输出扩展名应为 '+ext)
 if p.exists():raise SystemExit('输出已存在，请换一个文件名：'+str(p))
 p.parent.mkdir(parents=True,exist_ok=True);return p
def main():
 p=argparse.ArgumentParser(description=__doc__);a=p.add_mutually_exclusive_group(required=True)
 a.add_argument('--list',action='store_true',help='列出 35 镜及起始时间')
 a.add_argument('--still',nargs=2,metavar=('镜号','镜内秒数'),help='直接从矢量画面生成单帧')
 a.add_argument('--draw',metavar='镜号',help='在 build 中重画一镜，不更改锁定切片')
 a.add_argument('--assemble-silent',action='store_true',help='无损重组无声全片，附章节与可选字幕')
 a.add_argument('--assemble',metavar='本版成片',type=Path,help='从配套 MP4 取两条音轨，与工程画面重新装配')
 p.add_argument('--with-next',action='store_true',help='同时显影下一镜的转场入口')
 p.add_argument('--width',type=int,default=1280,help='单帧预览宽，16 的倍数')
 p.add_argument('--out',type=Path,help='单帧 PNG 或整片 MP4 的另存位置')
 o=p.parse_args();rows=book();ids=[r['id']for r in rows]
 if o.with_next and not o.draw:p.error('--with-next 配合 --draw')
 if o.width!=1280 and not o.still:p.error('--width 只控制单帧预览')
 if o.out and (o.list or o.draw):p.error('重画总是写入 build；用 --out 指定单帧或整片')
 if o.list:
  for z in rows:print(f"{z['id']:7s} {mm(z['t0'],1)}   {z['duration']:5.1f}s   {z['title']}")
  return
 if o.assemble_silent or o.assemble is not None:
  from mux4 import assemble
  name='无声长剪.mp4' if o.assemble_silent else '重新装配.mp4';dest=fresh(o.out or BUILD/name,'.mp4')
  if o.assemble and not o.assemble.is_file():p.error('请提供本版带双音轨的 MP4')
  assemble(dest,audio_from=None if o.assemble_silent else o.assemble,override=BUILD);return
 k=o.still[0] if o.still else o.draw
 if k not in ids:p.error('镜号不存在；--list 查看可用镜号')
 try:from shoot4 import cue,prev,draw,clipshot
 except (ModuleNotFoundError,ImportError,ValueError) as e:
  raise SystemExit('生成新画面需要系统 Python、Cairo、Pango、GI 以及 Rsvg，见 README。错误：'+str(e))
 if o.still:
  try:t=float(o.still[1])
  except ValueError:p.error('秒数必须为数字')
  if not(math.isfinite(t) and 0<=t<cue(k).d):p.error(f'镜内范围：0 至 {cue(k).d:g} 秒（不含终点）')
  if o.width%16 or not 320<=o.width<=3840:p.error('单帧宽需为 320–3840 间 16 的倍数')
  dest=fresh(o.out or BUILD/f'{k}-{t:g}s.png','.png');sf,g=prev.surface(o.width);draw(g,k,t);sf.write_to_png(str(dest));print(dest);return
 ix=ids.index(k);targets=ids[ix:ix+(2 if o.with_next else 1)]
 for tag in targets:clipshot(tag,2560,BUILD)
if __name__=='__main__':main()
