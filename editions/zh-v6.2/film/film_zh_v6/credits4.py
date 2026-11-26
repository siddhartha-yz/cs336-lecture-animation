from edition4 import *
def run():
 x=json.loads((W/'assets/four-axes.json').read_text());cuebook=json.loads((W/'audio/cuebook.json').read_text());r=cuebook['passages']
 models='\n'.join(f"| {z['name']} | {z['index']:.2f} | {z['cost']:.3f} | {z['arena']:.1f} | {z['traffic_T']:g} |" for z in x)
 music='\n'.join(f"| {z['movement']} | {mm(z['start'],1)} | [{z['title']}](https://app.sessions.blue/browse?trackId={z['credit']}) · {z['album']} | {z['purpose']} |" for z in r)
 a=(DEST/'sources-base.md').read_text().replace('{COHORT}',models).replace('{MUSIC}',music)
 ss=book();a=a.replace('{RUNTIME}',mm(ss[-1]['t0']+ss[-1]['duration'],1))
 for z in ss:a=a.replace('{START:'+z['id']+'}',mm(int(z['t0'])))
 assert '{START:' not in a
 m=cuebook['picture_locked_layback']
 bridge=f"**26:25 附近的转场**：*{m['title_from']}* 向 *{m['title_to']}* 的交叠从 {mm(m['start'],1)} 到 {mm(m['end'],1)}，低音先接，上部音色随后进入。曲目、录音位置及其他切点沿用原剪。上表为原剪曲目入点。"
 a=a.replace('片头两束影子在',bridge+'\n\n片头两束影子在')
 (DEST/(STEM+'-数据与配乐.md')).write_text(a)
if __name__=='__main__':run()
