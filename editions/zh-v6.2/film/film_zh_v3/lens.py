"""Camera blocking. Each move answers 'what changed', rather than animating an empty room."""
from ink import *
def seat(g,k,c):
 t=c.t
 def a(x):return c.at(x)
 def w(p,q):return phase(t,p-.18,p+.6)*(1-phase(t,q-.55,q+.12))
 # Anchor, image position, magnification. All the lettering is glued to the set in this transform.
 # Callers which carry the physical last pose return to the handoff mark before the cut.
 z=1.;ax=800.;ay=427.;px=800.;py=427.
 if k=='3-2':
  u=w(1.,a('第二刀'));v=w(a('第三刀'),a('换一张卷子'));z=1.07+.13*u+.10*v;ay=470;py=393
 elif k=='3-4':
  f=w(.18,a('第一道对抗筛网'));s=w(a('第一道对抗筛网'),a('两千五百'));v=w(a('必须看图'),a('第一道对抗筛网'));e=1-phase(t,a('可把这封')-.6,a('可把这封')+.3)
  z=1+.13*f+.08*s+.12*v;ax=795-80*f+150*v;ay=420;py=420-44*e
 elif k=='4-1':
  v=w(.8,a('把这一票留下'));b=w(a('A 赢过 B'),a('更可能赢'));z=1+.075*v+.19*b;ax=800;ay=447;py=447-42*(v+b)
 elif k=='4-2':
  q=w(a('极大似然'),a('真实投票记录'));z=1+.075*q;ax=556;ay=445;px=550;py=437
 elif k=='4-3':
  v=w(a('换一种措辞'),a('长度偏见'));z=1.04+.115*v;ax=800+208*v;px=800+164*v;ay=465;py=386
 elif k=='4-4':
  v=w(a('长度差设成零'),a('论文比较'));z=1+.075*v;ax=1100;ay=429;px=1100;py=413
 elif k=='5-1':
  v=w(a('完整的代码库'),a('复核') if '复核' in c.s['chars'] else a('Verified'));settle=phase(t,0,.93)
  z=1+.04*settle+.077*v;ax=786-171*v;ay=450;px=ax;py=434-39*settle
 elif k=='5-2':
  v=w(a('删掉'),a('两排一起看'));z=1.045+.08*v;ax=800+205*v;px=800+174*v;ay=453;py=376
 elif k=='5-3':
  v=w(a('允许交两份'),a('先把中间'));z=1.035+.035*v;ax=800;ay=480;py=414
 elif k=='5-4':
  v=w(.4,a('拿走它熟悉'));z=1+.105*v;ay=459;py=459-69*v
 elif k=='6-3':
  v=w(a('先把第一句'),a('一道无害'));z=1.075+.15*v;ay=438;py=381
 elif k=='6-4':
  v=w(a('HarmBench'),a('二十道题'));z=1.035+.065*v;ay=467;py=402
 elif k=='7-1':
  v=w(a('卷筒参数'),a('夹具的设计图'));z=1.07+.055*v;ay=461;py=388
 elif k=='7-2':
  v=w(a('原始顺序'),a('随机打乱'));z=1.015+.055*v;ay=449;py=423
 elif k in ('7-3','7-4'):
  # Text wall occupies the lens; 7-3 and 7-4 are identical at their joint.
  z=1.045;ax=773;px=773;ay=441;py=370
 elif k=='7-5':
  v=w(a('机构内部'),a('专家二次审计'));z=1.025+.09*v;ay=430;py=375
 ctx=g.c;ctx.translate(px,py);ctx.scale(z,z);ctx.translate(-ax,-ay)

def historical(g,k,c):
 # A real dolly into the common dataset; it withdraws only when both systems need comparison.
 t=c.t;z=1.;a=c.at;ax=px=800.;ay=py=427.
 if k=='1-3':
  d=phase(t,a('先看左边')-.37,a('ImageNet')+1.11)*(1-phase(t,a('可换成两个')-.45,a('训练集里有什么')+.15))
  pull=phase(t,a('右边这家')-.28,a('拿了第一')+.55)*(1-phase(t,c.d-2.65,c.d-.16))
  z=1+.50*d+.10*pull;ax=540*d+800*(1-d)+210*pull;ay=437;px=800-92*d+70*pull;py=421
 elif k=='2-1':
  f=phase(t,a('十万个词')-.26,a('均匀乱猜')+.61)*(1-phase(t,a('第一步五选一')-.76,a('第一步五选一')-.13))
  z=1+.045*f;ay=446;py=446-17*f
 else:return
 g.c.translate(px,py);g.c.scale(z,z);g.c.translate(-ax,-ay)
