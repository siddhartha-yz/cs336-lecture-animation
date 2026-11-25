"""Burn reader-sized Chinese type onto the final native frames, retaining both original audio tracks."""
from edition3 import W,O,BASE,S,starts,captions,TOTAL
from press3 import ass
from export_codec import encoder,h264
from pathlib import Path
import subprocess as sp,sys,json
def burn(src,dst):
 src=Path(src);dst=Path(dst);rows=[(starts[k]+a,starts[k]+b,s) for k,r in S.items()for a,b,s in captions(r)]
 full=W/'ass/full.ass';ass(rows,full);exe,enc=encoder('nvenc');tmp=dst.with_name(dst.stem+'.part.mp4')
 f="hwdownload,format=nv12,ass=filename=ass/full.ass,hwupload_cuda"
 cmd=[exe,'-y','-v','warning','-nostdin','-hwaccel','cuda','-hwaccel_output_format','cuda','-threads','1','-i',str(src.resolve()),'-map','0:v:0','-map','0:a','-map_metadata','0','-map_chapters','0','-filter_threads','1','-vf',f,*h264(enc,15),'-g','120','-profile:v','high','-video_track_timescale','15360','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','copy','-movflags','+faststart',str(tmp.resolve())]
 sp.run(cmd,check=True,cwd=W);tmp.replace(dst)
if __name__=='__main__':burn(*(sys.argv[1:3] or [O/(BASE+'.mp4'),O/(BASE+'-字幕版.mp4')]))
