"""Light the three physical projection faces before they enter the z-buffer. Keep the far
edges legible through either solid; no postprocessing, bloom or background exposure."""
import opening
_outer=opening.outer
class Material:
 def __init__(self,w):self.w=w
 def face(self,pts,c,al,fill,edge):
  return self.w.face(pts,c,al,fill={.105:.32,.185:.48,.224:.64}.get(fill,fill),edge=edge)
 def segment(self,p,q,col,width,op):return self.w.segment(p,q,col,width*1.16,op)
def chalk_box(w,n,primary,t,replace=0,al=1):
 if getattr(w.g,'editor_id','')=='8-2'and t<2.66:al=1.
 return _outer(Material(w),n,primary,t,replace,al)
def engage():opening.outer=chalk_box
