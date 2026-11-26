"""Lossless-picture conform of the clean or lettered release. Reopening a locked edit requires only FFmpeg."""
from pathlib import Path
import json,subprocess,argparse,shutil,tempfile,math
from edition4 import W,DEST,STEM,book
def probe(path):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-print_format','json','-show_entries','stream=codec_type,codec_name,channels,sample_rate,duration,width,height,nb_frames,avg_frame_rate,pix_fmt,time_base,color_space','-show_format',str(path)]))
def gg(path):return str(Path(path).resolve()).replace("'","'\\''")
def prepare_audio(output=None):
 root=W/'audio';out=Path(output) if output else root/'mix-and-dialogue.m4a';dest=out.with_name(out.stem+'.part.m4a');dest.parent.mkdir(parents=True,exist_ok=True)
 for f,c in [('screening.wav',2),('dialogue.wav',1)]:
  props=probe(root/f)['streams'][0];assert int(props['sample_rate'])==48000 and props['channels']==c and abs(float(props['duration'])-sum(r['duration']for r in book()))<1/48000,(f,props)
 subprocess.run(['ffmpeg','-v','error','-y','-nostdin','-i',str(root/'screening.wav'),'-i',str(root/'dialogue.wav'),'-map','0:a:0','-map','1:a:0','-threads:a','1','-c:a','aac','-b:a:0','224k','-b:a:1','144k','-metadata:s:a:0','language=zho','-metadata:s:a:1','language=zho',str(dest)],check=True)
 dest.replace(out);return out
def assemble(out,*,audio_from=None,burned=False,override=None,rows=None):
 rows=book() if rows is None else rows;end=rows[-1]['t0']+rows[-1]['duration'];out=Path(out).expanduser().resolve();out.parent.mkdir(parents=True,exist_ok=True);layer='shots-sub'if burned else'shots';folder=W/layer
 if audio_from and Path(audio_from).resolve()==out:raise ValueError('输出必须区别于输入音轨')
 sampled=[]
 for r in rows:
  k=r['id'];filename=k+'.mp4';part=Path(override)/layer/filename if override else folder/filename
  if override and not part.is_file():part=folder/filename
  if not part.is_file():raise FileNotFoundError(part)
  st=probe(part)['streams']
  if len(st)!=1:raise ValueError(f'{k} 应为一条无声画面')
  s=st[0];marker=(s['codec_name'],s['width'],s['height'],s['avg_frame_rate'],s['time_base'],int(s['nb_frames']))
  if marker!=('h264',1920,1080,'60/1','1/15360',round(r['duration']*60)):raise ValueError((part,marker))
  sampled.append((part,r['duration']))
 with tempfile.TemporaryDirectory(prefix='cut-v4-',dir=out.parent) as temp:
  d=Path(temp);lst=d/'cuts.ffconcat';lst.write_text('ffconcat version 1.0\n'+''.join("file '"+gg(p)+f"'\nduration {dur:.9f}\n"for p,dur in sampled))
  cmd=['ffmpeg','-v','error','-nostdin','-y','-f','concat','-safe','0','-i',str(lst)];i=1;maps=['-map','0:v:0'];opts=['-c:v','copy','-video_track_timescale','15360']
  if audio_from:
   aa=[s for s in probe(audio_from)['streams'] if s['codec_type']=='audio']
   if len(aa)!=2 or any(s['codec_name']!='aac' or abs(float(s['duration'])-end)>.025 for s in aa) or [s['channels']for s in aa]!=[2,1]:raise ValueError('需要本版同长的成片（立体声混音＋单声道人声）')
   cmd+=['-i',str(audio_from)];maps+=['-map',f'{i}:a:0','-map',f'{i}:a:1'];i+=1
   opts+=['-c:a','copy','-metadata:s:a:0','language=zho','-metadata:s:a:0','handler_name=中文旁白与配乐','-metadata:s:a:1','language=zho','-metadata:s:a:1','handler_name=中文纯旁白','-disposition:a:0','default','-disposition:a:1','0']
  else:opts+=['-an']
  if not burned:
   cmd+=['-i',str(DEST/(STEM+'.srt'))];maps+=['-map',f'{i}:s:0'];i+=1
   opts+=['-c:s','mov_text','-metadata:s:s:0','language=zho','-metadata:s:s:0','handler_name=简体中文','-disposition:s:0','default']
  cmd+=['-f','ffmetadata','-i',str(DEST/'chapters.ffmeta'),*maps,'-map_metadata',str(i),'-map_chapters',str(i),*opts]
  if not audio_from:cmd+=['-metadata','title=能力的影子 · 无声画面','-metadata','comment=CS336 第十二讲：模型评估指标与基准测试评测。']
  tmp=d/'assembly.mp4';subprocess.run([*cmd,'-movflags','+faststart',str(tmp)],check=True);tmp.replace(out)
 print(out,flush=True);return out
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--encode-audio',action='store_true');p.add_argument('--audio-from',type=Path);p.add_argument('--burned',action='store_true');p.add_argument('--silent',action='store_true');p.add_argument('--out',type=Path);p.add_argument('--override',type=Path);o=p.parse_args()
 if o.encode_audio:prepare_audio(o.out)
 else:
  if o.silent and o.audio_from:p.error('--silent 不能加入音轨')
  if not o.out:p.error('请指定 --out')
  src=None if o.silent else o.audio_from or W/'audio/mix-and-dialogue.m4a'
  assemble(o.out,audio_from=src,burned=o.burned,override=o.override)
