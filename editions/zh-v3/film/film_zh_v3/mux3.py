"""Combine native picture edits, both Mandarin soundtracks and chapter marks without touching the pixels."""
from edition3 import W,O,BASE,S,make,TOTAL,picture_credits
from pathlib import Path
import argparse,subprocess,json
def probe(p,props):
 return json.loads(subprocess.check_output(['/usr/bin/ffprobe','-v','error','-of','json','-select_streams','v:0','-show_entries','stream='+props,str(p)]))['streams'][0]
def esc(f):return str(f.resolve()).replace("'","'\\''")
def assemble(folder,out,width,fps,burned=False,audio_from=None,*,picture_only=False):
 if picture_only and audio_from is not None:raise ValueError('无声装配不接收音轨')
 make();folder=Path(folder);out=Path(out);out.parent.mkdir(exist_ok=True,parents=True)
 if audio_from is not None and Path(audio_from).resolve()==out.resolve():raise ValueError('audio input cannot be the output')
 ff=W/(folder.name+'-video.ffconcat');rows=['ffconcat version 1.0']
 for k,d in S.items():
  src=folder/(k+'.mp4');props=probe(src,'width,height,nb_frames,avg_frame_rate')
  assert (int(props['nb_frames']),props['width'],props['height'])==(d['frames']*fps//30,width,width*9//16),(k,props)
  assert props['avg_frame_rate']==f'{fps}/1',(k,props)
  rows += [f"file '{esc(src)}'",f"duration {d['duration']:.9f}"]
 ff.write_text('\n'.join(rows)+'\n')
 cmd=['/usr/bin/ffmpeg','-nostdin','-hide_banner','-loglevel','warning','-y','-f','concat','-safe','0','-i',str(ff)]
 if picture_only:
  audio_map=[];audio_codec=['-an'];i=1
 elif audio_from is None:
  for fn in ('master-mix.wav','master-dry.wav'):
   path=W/fn;dur=float(subprocess.check_output(['/usr/bin/ffprobe','-v','error','-of','csv=p=0','-show_entries','format=duration',str(path)]))
   assert abs(dur-TOTAL)<.00008,(fn,dur,TOTAL)
   cmd+=['-i',str(path)]
  audio_map=['-map','1:a:0','-map','2:a:0'];audio_codec=['-c:a','aac','-threads:a','1','-b:a:0','224k','-b:a:1','144k'];i=3
 else:
  aud=json.loads(subprocess.check_output(['/usr/bin/ffprobe','-v','error','-select_streams','a','-show_entries','stream=codec_name,duration,channels','-of','json',str(audio_from)]))['streams']
  assert [a['channels'] for a in aud]==[2,1] and all(a['codec_name']=='aac' and abs(float(a['duration'])-TOTAL)<.03 for a in aud)
  cmd+=['-i',str(audio_from)];audio_map=['-map','1:a:0','-map','1:a:1'];audio_codec=['-c:a','copy'];i=2
 maps=['-map','0:v:0',*audio_map];subs=[]
 if not burned:
  cmd+=['-i',str(O/(BASE+'.srt'))];maps+=['-map',f'{i}:s:0'];i+=1
  subs=['-c:s','mov_text','-metadata:s:s:0','language=zho','-metadata:s:s:0','handler_name=简体中文','-disposition:s:0','default']
 temp=out.with_name(out.stem+'.part.mp4')
 tags=(['-metadata','title=模型评测与基准测试 · 无声字幕版','-metadata','comment='+picture_credits] if picture_only else
       ['-metadata:s:a:0','language=zho','-metadata:s:a:0','handler_name=科普音色 · Drama 3 旁白与配乐','-metadata:s:a:1','language=zho','-metadata:s:a:1','handler_name=科普音色 · Drama 3 纯旁白',
        '-disposition:a:0','default','-disposition:a:1','0'])
 cmd+=['-f','ffmetadata','-i',str(W/'master.ffmeta'),*maps,'-map_metadata',str(i),'-map_chapters',str(i),
       '-c:v','copy','-video_track_timescale','15360',*audio_codec,*subs,*tags,'-movflags','+faststart',str(temp)]
 subprocess.run(cmd,check=True);temp.replace(out);print(out,flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();u=p.add_mutually_exclusive_group();u.add_argument('--edit',action='store_true');u.add_argument('--lettered',action='store_true');p.add_argument('--audio-from',type=Path);p.add_argument('--out',type=Path);a=p.parse_args()
 dr='shots-edit' if a.edit else 'shots-sub' if a.lettered else 'shots'
 dest=W/'notes/editorial.mp4' if a.edit else O/(BASE+('-字幕版' if a.lettered else '')+'.mp4')
 assemble(W/dr,a.out or dest,1152 if a.edit else 1920,30 if a.edit else 60,a.lettered,a.audio_from)
