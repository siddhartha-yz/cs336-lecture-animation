"""Typeset each complete expression in one TeX box and keep the resulting vector outlines."""
from pathlib import Path
import argparse,subprocess
W=Path(__file__).resolve().parent
expr={
 'ppl':(r'\operatorname{PPL}=\exp\!\left(-\dfrac1T\sum_{i=1}^{T}\log p_i\right)','FFFFFF'),
 'geometric':(r'\sqrt{5\,\times\,20}=10','5CD0B3'),
 'elo':(r'P(A>B)=\dfrac{1}{1+10^{(E_B-E_A)/400}}','FFFFFF'),
 'elo_diff':(r'P(A>B)=\dfrac{1}{1+10^{\color[HTML]{FFFF00}(E_B-E_A)/400}}','FFFFFF'),
 'elo_add':(r'P(A>B)=\dfrac{1}{{\color[HTML]{FFFF00}1+}10^{(E_B-E_A)/400}}','FFFFFF'),
 'elo_den':(r'P(A>B)=\dfrac{1}{\color[HTML]{FFFF00}1+10^{(E_B-E_A)/400}}','FFFFFF'),
 'elo_inv':(r'P(A>B)={\color[HTML]{FFFF00}\dfrac{\color[HTML]{FFFF00}1}{\color[HTML]{FFFFFF}1+10^{(E_B-E_A)/400}}}','FFFFFF'),
 'surprise':(r's=-\log p(u\,|\,x)','FFFFFF'),
 'transfer':(r'\widehat{P}(B\mid A)=\dfrac{n_{AB}}{n_A}','FFFFFF'),
 'both':(r'\widehat{P}(A\cap B)=\dfrac{n_{AB}}{N}','FFFFFF'),
 'domain_mean':(r'\exp\!\left(\frac16\sum_{d=1}^{6}\ln\mathrm{PPL}_d\right)','CDD2D7'),
}
args=argparse.ArgumentParser(description=__doc__);args.add_argument('formula',nargs='*')
selected=args.parse_args().formula
for id in selected or expr:
 if id not in expr:args.error('unknown formula: '+id)
 eq,col=expr[id]
 tex=(r'\documentclass[border=1pt]{standalone}\usepackage{amsmath,xcolor}\begin{document}'
      +r'\color[HTML]{'+col+r'}$\displaystyle '+eq+r'$\end{document}')
 (W/(id+'.tex')).write_text(tex)
 subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',id+'.tex'],cwd=W,stdout=subprocess.DEVNULL,check=True)
 subprocess.run(['pdftocairo','-svg',id+'.pdf',id+'.svg'],cwd=W,check=True)
