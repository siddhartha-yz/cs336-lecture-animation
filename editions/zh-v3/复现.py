#!/usr/bin/env python3
"""预览或重画镜头，装配无声画面；也可在本地沿用已有母版音轨。"""
import argparse,json,os,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
F=ROOT/'film'/'film_zh_v3';B=ROOT/'build'
sys.path.insert(0,str(F))
from timeline3 import IDS,S,starts,mm
def safeout(p,ext):
 p=Path(p).expanduser().resolve()
 if p.suffix.lower()!=ext:raise SystemExit('输出应为 '+ext+' 文件。')
 if p.exists():raise SystemExit('已有同名结果。用 --out 换个文件名。')
 p.parent.mkdir(parents=True,exist_ok=True);return p
def main():
 p=argparse.ArgumentParser(description=__doc__);c=p.add_mutually_exclusive_group(required=True)
 c.add_argument('--list',action='store_true',help='列出镜头编号与开始时刻')
 c.add_argument('--still',nargs=2,metavar=('镜头','镜头内秒数'))
 c.add_argument('--draw',metavar='镜头',help='重画一个镜头，原始切片保留')
 c.add_argument('--assemble-silent',action='store_true',help='用现有画面拼出无声全片，保留章节和可切换中文字幕')
 c.add_argument('--assemble',type=Path,metavar='v3全片',help='使用配套全片的两条原声，仅重组画面')
 c.add_argument('--burn',type=Path,metavar='可切换字幕版',help='为改过画面的全片烙上中文字幕')
 p.add_argument('--out',type=Path,help='PNG 或 MP4 输出路径（不覆盖已有文件）')
 p.add_argument('--with-next',action='store_true',help='重画下一镜入口，用于修改过镜尾的情况')
 p.add_argument('--width',type=int,default=1280,help='单帧预览宽度，16 的倍数')
 a=p.parse_args()
 if a.with_next and not a.draw:p.error('--with-next 配合 --draw 使用')
 if a.out and not (a.burn or a.assemble or a.assemble_silent or a.still):p.error('改镜头自动存在 build/shots，--out 用于单帧或全片')
 if a.list:
  tl=json.loads((F/'timeline.json').read_text())
  for s in tl['scenes']:print(f"{s['id']:3}  {mm(s['time'],1)}   {s['duration']:5.1f}s   {s['title']}")
  return
 if a.assemble or a.assemble_silent:
  src=a.assemble.expanduser().resolve() if a.assemble else None
  if src is not None and not src.is_file():raise SystemExit('请提供 v3 全片 MP4 作为双音轨来源。')
  dst=safeout(a.out or B/('无声修订版.mp4' if a.assemble_silent else '重新装配.mp4'),'.mp4')
  B.mkdir(parents=True,exist_ok=True)
  from mux3 import assemble
  with tempfile.TemporaryDirectory(dir=B,prefix='splice-')as temp:
   cuts=Path(temp)/'有效画面';cuts.mkdir()
   for k in IDS:
    new=B/'shots'/(k+'.mp4');f=new if new.is_file()else F/'shots'/(k+'.mp4')
    if not f.is_file():raise SystemExit(k+' 缺少画面。')
    (cuts/(k+'.mp4')).symlink_to(f.resolve())
   assemble(cuts,dst,1920,60,False,src,picture_only=a.assemble_silent)
  return
 if a.burn:
  from letter3_master import burn
  src=a.burn.expanduser().resolve()
  if not src.is_file():raise SystemExit('请先用 --assemble 装配带可选字幕的全片。')
  dst=safeout(a.out or B/'重新装配-字幕版.mp4','.mp4')
  import subprocess
  cmd=['/usr/bin/ffprobe','-v','error','-show_entries','stream=codec_type,codec_name,channels,duration','-of','json',str(src)]
  tracks=json.loads(subprocess.check_output(cmd))['streams']
  if not any(x['codec_type']=='subtitle'for x in tracks) or [x['channels']for x in tracks if x['codec_type']=='audio']!=[2,1]:
   raise SystemExit('输入应是 v3 带两条音轨和可切换字幕的母版。')
  (F/'ass').mkdir(exist_ok=True);burn(src,dst);print(dst);return
 k=a.still[0] if a.still else a.draw
 if k not in S:p.error('未知镜头，可用 --list 查看')
 try:from stage3 import surface,paint
 except ImportError as ex:raise SystemExit('画面引擎缺少系统绘图组件；见 README 的依赖与字体。\n'+str(ex))
 if a.still:
  try:t=float(a.still[1])
  except ValueError:p.error('镜头内秒数应是数值')
  if not 0<=t<S[k]['duration'] or a.width<192 or a.width%16:p.error('镜头内秒数须在片段内，宽度取 16 的倍数且不小于 192')
  dst=safeout(a.out or B/f'{k}-{t:.2f}.png','.png');sf,g=surface(a.width);paint(g,k,t);sf.write_to_png(str(dst));print(dst);return
 from render3 import render
 ids=[k]
 if a.with_next and k!=IDS[-1]:ids.append(IDS[IDS.index(k)+1])
 for sid in ids:render(sid,2560,60,outroot=B)
 print('新切片在 build/shots；重新装配时会优先选用它们。')
if __name__=='__main__':main()
