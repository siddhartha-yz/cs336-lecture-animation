from pathlib import Path
import sys,math
from functools import lru_cache
from timeline3 import W,OLD,S,B,IDS,remap,clock
sys.path.insert(0,str(OLD))
import direct as v2
from ink import *
from cut_common import cairo,stage
from motion import out3
# Bound at the glyph run, so visual labels and their measured widths always agree.
NAMES={'原来的题序，有多特别？':'原序与置换','讲义图 205 · Sphinx #5560 → #8713 · 文档解析修复节选':'sphinx-doc/sphinx · #5560 → #8713','讲义图 208 的题序 · 四符号示例的全部 24 种排列':'四道题 · 全部 24 种排列','HLE 制题流程 · 讲义图 201':'','Text Arena · 讲义快照':'Text Arena','讲义图 203 · 历史榜单 · 同分可并列':'',
'一个答案，还是一份作品？':'交付一份作品','还要等多少张选票？':'等一轮真人投票','长一点，就更好吗？':'长度红利','五份补丁，交哪几份？':'五份补丁，十种配对','修过旧仓库，就会解新题吗？':'从旧代码到新网格','拒绝全部请求，会发生什么？':'拒答与误拒','只看开头，能判整份回答吗？':'同一句开头，两种结果','同样三张，除以几张？':'同一批题，两个分母','命中的是原题，还是许可证？':'重合位置决定处理方式','把题留到最后，还是把旧题审一遍？':'让新题晚于训练','只听第一句，能判吗？':'先读第一句','换个模型，发生率变了多少？':'相同协议下的差异','到了这把尺，谁先跑完？':'先过线的用时更短'}
import mounting
from pigments import chalk,visibility
from lab_ink import engage
engage()
class Board(v2.Ink):
 chroma_master=True
 def source(self,color,alpha=1):
  if not self.chroma_master:return super().source(color,alpha)
  pigment,ch=chalk(color);self.c.set_source_rgba(*pigment,max(0.,min(1.,visibility(alpha,ch))))
 def line(self,x1,y1,x2,y2,color='#FFFFFF',width=2,alpha=1,dash=None):
  if self.chroma_master and 0<width<2.3:
   _,ch=chalk(color);width+=.33*ch*(1-min(1,max(0,(width-1.6)/.7)))
  return super().line(x1,y1,x2,y2,color,width,alpha,dash)
 def rect(self,x,y,w,h,fill=None,stroke=None,width=2,r=0,alpha=1):
  if self.chroma_master and getattr(self,'editor_id','')=='2-2' and fill and stroke in (C,Y) and 12<h<45:
   fill=inkcol(stroke,.28 if h>33 else .23)
  if self.chroma_master and getattr(self,'editor_id','')=='2-4' and abs(h-77)<.01 and fill and w>5:
   from visual import rgb
   rr,gg,bb=rgb(fill)
   if stroke==E:fill='#268C74' if gg>rr else '#793F3B'
   elif stroke in (C,V):fill=inkcol(stroke,.38)
  return super().rect(x,y,w,h,fill,stroke,width,r,alpha)
 def outside(self,s,x,y,fs):
  if getattr(self,'_attached',False):return False
  s=NAMES.get(str(s),str(s));s=v2.tr(s) if self.loc else s
  return mounting.omit(getattr(self,'editor_id',''),s,x,y,fs)
 def text(self,s,x,y,size=36,color='#FFFFFF',alpha=1,align='center',font='sans',weight='normal'):
  s=NAMES.get(str(s),str(s))
  if not getattr(self,'_attached',False):
   lab=v2.tr(s) if self.loc else s
   if getattr(self,'legacy',False) and not self.no_text and mounting.raw_legacy(self,self.editor_id,lab,x,y,size,color,alpha,align,font,weight):return
   if mounting.omit(getattr(self,'editor_id',''),lab,x,y,size):return
  return super().text(s,x,y,size,color,alpha,align,font,weight)
 def measure(self,s,*args,**kw):return super().measure(NAMES.get(str(s),s),*args,**kw)
def surface(w):
 sf=cairo.ImageSurface(cairo.FORMAT_RGB24,w,w*9//16);return sf,Board(cairo.Context(sf),w,w*9//16)
def olddraw(g,k,t):
 g.editor_id=k
 # Early continuous projection scenes already share their last and first pose exactly.
 v2.paint(g,k,remap(k,t))
# Selected sequences own the whole canvas, including the type and their physical hand-off.
CUSTOM={'3-1':('studio_saturation','saturation'),'6-2':('studio_compute','compute'),'8-1':('studio_finale','orbit'),'3-2':('studio_exam','pro'),'3-3':('studio_science','gpqa'),'3-4':('studio_examples','sieve'),'4-1':('studio_ballot','arena'),'4-2':('studio_votes','rating'),'4-3':('studio_preference','judgement'),'4-4':('studio_votes','length'),'5-1':('studio_engineering','repos'),'5-2':('studio_engineering','tests'),'5-3':('studio_tests','combinations'),'5-4':('studio_tests','repo_to_arc'),'6-1':('studio_tests','arc'),'6-3':('studio_behaviors','refusal'),'6-4':('studio_behaviors','replication'),'7-1':('studio_industry','industry'),'7-2':('studio_evidence','shuffle'),'7-3':('studio_corpus','scan'),'7-4':('studio_corpus','unmask'),'7-5':('studio_dates','newtests')}
def raw(g,k,t):
 g.editor_id=k;g.loc=False;g.no_text=False;g.legacy=k not in CUSTOM
 c=clock(k).clk(t)
 if g.legacy:
  from lens import historical
  stage(g);g.c.save()
  try:
   historical(g,k,c);v2.raw(g,k,remap(k,t))
   if k=='2-2':
    from studio_units import compare
    g.loc=False;compare(g,c)
  finally:g.c.restore();g.loc=False
  return
 import importlib
 from lens import seat
 mod,method=CUSTOM[k];stage(g);g.c.save()
 try:
  seat(g,k,c)
  getattr(importlib.import_module(mod),method)(g,c)
  if k!='6-2':mounting.place(g,k,c)
 finally:g.c.restore()
def paint(g,k,t):
 raw(g,k,t)
 if k[0]>='3' and t<.82:
  import v3joins
  v3joins.link(g,k,t,raw,surface)
