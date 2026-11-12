"""Build Part2_Cheat_Sheet_Handwritten.html/.pdf (blue, Patrick Hand) from Part2_Cheat_Sheet.html.
Usage: python make_handwritten.py   (optional args: font-family size line-height)"""
import sys, os, subprocess, time, tempfile, fitz
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(HERE,'Part2_Cheat_Sheet.html')
OUT=os.path.join(HERE,'Part2_Cheat_Sheet_Handwritten.html')
PDF=os.path.join(HERE,'Part2_Cheat_Sheet_Handwritten.pdf')
a=sys.argv[1:]+[None]*3
font=a[0] or "'Patrick Hand', 'Ink Free', 'Comic Sans MS', cursive"; size=float(a[1] or 8.9); lh=float(a[2] or 1.06)
s=open(SRC,encoding='utf-8').read()
link='<style>\n'+open(os.path.join(HERE,'fonts','fonts.css'),encoding='utf-8').read()+'</style>\n'
css=f'''
  /* ---- handwritten blue override ---- */
  body, .f, .f .lab, .head h1, .head span, .panel h2, .panel.qa h2, h3, th, td {{ font-family: {font}; }}
  body {{ font-size: {size}pt; line-height: {lh}; color: #1b3fa0; }}
  .f {{ font-size: {size}pt; line-height: {lh+0.1}; }}
  .f .lab {{ font-size: {size*0.85}pt; color: #1b3fa0; }}
  .head h1 {{ font-size: {size*1.35}pt; }}
  .head span {{ font-size: {size}pt; }}
  .panel h2 {{ font-size: {size*1.12}pt; font-style: normal; text-decoration: underline; color: #1b3fa0; }}
  .panel.qa h2 {{ color: #1b3fa0; }}
  h3 {{ font-size: {size}pt; }}
  .head {{ border-bottom-color: #1b3fa0; }}
  .panel, .panel.qa {{ border-color: #1b3fa0; }}
  th {{ border-top-color: #1b3fa0; border-bottom-color: #1b3fa0; }}
  td {{ border-bottom-color: #9fb0dd; }}
  tr:last-child td {{ border-bottom-color: #1b3fa0; }}
  .frac > span:first-child {{ border-bottom-color: #1b3fa0; }}
  .ex {{ border-left-color: #1b3fa0; }}
  .opt, p.r i {{ color: #3b5bb5; }}
  b {{ font-weight: 700; }}
'''
s=s.replace('</style>',css+'</style>',1).replace('<style>',link+'<style>',1)
s=s.replace('<title>SC3102 Part 2 Cheat Sheet</title>','<title>SC3102 Part 2 Cheat Sheet (handwritten)</title>')
open(OUT,'w',encoding='utf-8',newline='\n').write(s)
edge=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
subprocess.run([edge,'--headless=new','--disable-gpu','--no-pdf-header-footer','--virtual-time-budget=8000',
 '--user-data-dir='+os.path.join(tempfile.gettempdir(),'edge_cheatsheet'),
 '--print-to-pdf='+PDF,'file:///'+OUT.replace(os.sep,'/')],capture_output=True)
time.sleep(1)
d=fitz.open(PDF); print('pages',len(d))
print('fonts',sorted({f[3] for p in d for f in p.get_fonts()}))
for pi,p in enumerate(d):
    for c,(x0,x1) in enumerate([(0,285),(285,565),(565,842)]):
        bl=[b for b in p.get_text('blocks') if x0<=b[0]<x1]
        bottom=max(b[3] for b in bl)
        print(f'side {pi+1} col {c+1} bottom {bottom:.0f}pt', '(OVERFLOW?)' if bottom>572 else '')
