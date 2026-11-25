"""The composer's tracks and the seven musical hand-offs in the continuous v3 mix."""
from timeline3 import starts,clock,TOTAL
# slug, credit, album, public attribution number, source in (seconds), body RMS (dBFS)
TRACKS=(
 ('the-gran-dias','The Gran Dias','Butterstone',408386,.34,-28.1),
 ('a-certain-lightness','A Certain Lightness','Migration',408158,6.17,-28.7),
 ('the-silver-hatch','The Silver Hatch','Rayling',408387,2.80,-28.8),
 ('tuck-and-point','Tuck and Point','Onesuch Village',408156,5.38,-28.4),
 ('vulcan-street','Vulcan Street','Castro',408388,15.70,-28.6),
 ('balti','Balti','K2',408395,5.30,-28.1),
 ('denzel-sprak','Denzel Sprak','CloudCover',408396,.31,-28.7),
 ('one-little-triumph','One Little Triumph','Piano Mover',408157,1.35,-28.0),
)
MUSIC_CREDIT=' / '.join(q[1] for q in TRACKS)+' — Blue Dot Sessions'
PURPOSE=('分数与投影','预测词元、比较语料','考试与区分度','投票与偏好','真实补丁与网格','推理预算与行为','真实交付、原题追踪','许可证、新题与六把尺')
def layout():
 # Centres live on the existing speech clock. Widths depend on the two recordings' pulses.
 handoffs=[(starts['2-1']-.34,4.),(starts['3-1']+7.05,3.6),(starts['4-2']-.64,3.2),
           (starts['4-4']+clock('4-4').at('可写得再漂亮')-1.20,4.8),(starts['6-2']+.05,3.3),
           (starts['7-1']+4.9,3.6),(starts['7-4']-.85,4.4)]
 boundaries=[0.]+[t-w/2 for t,w in handoffs]
 ends=[t+w/2 for t,w in handoffs]+[TOTAL]
 rows=[]
 for i,(slug,title,album,credit,offset,target) in enumerate(TRACKS):
  rows.append(dict(i=i,slug=slug,title=title,album=album,credit=credit,movement=1+i//2,start=boundaries[i],end=ends[i],source=offset,
                   target_db=target,fade_in=handoffs[i-1][1] if i else .65,fade_out=handoffs[i][1] if i<len(handoffs) else 1.05,purpose=PURPOSE[i]))
 return rows
