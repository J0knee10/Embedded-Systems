"""Build a blue handwriting-font copy (Patrick Hand) of a cheat-sheet HTML and print it to PDF.

Usage:
  python make_handwritten.py                      # Part2_Cheat_Sheet.html -> Part2_Cheat_Sheet_Handwritten.html/.pdf
  python make_handwritten.py [font] [size] [line-height]          # same, with a different font / size / line height
  python make_handwritten.py --src=Final_Cheat_Sheet.html [--out=X.html] [--ink-digits] [font] [size] [line-height]
Paths are relative to this folder (or absolute). --out defaults to <src>_Handwritten.html; the PDF sits next to it.
--ink-digits draws superscript/subscript digits (² ³ …) and vulgar fractions (½ ⅓ …) in Ink Free, because
Patrick Hand's versions are unreadable dots at small sizes. An empty font argument ("") keeps the default font.
Final sheet: python make_handwritten.py --src=Final_Cheat_Sheet.html --ink-digits "" 6.3 1.0
Prints the page count, the fonts used and each column's bottom (from the PDF text, and from the page layout,
which also catches text clipped by the fixed-height .side boxes)."""
import sys, os, re, json, subprocess, time, tempfile, shutil, fitz
HERE = os.path.dirname(os.path.abspath(__file__))
opts = {k[2:]: v for k, v in (a.split('=', 1) for a in sys.argv[1:] if a.startswith('--') and '=' in a)}
flags = {a[2:] for a in sys.argv[1:] if a.startswith('--') and '=' not in a}
pos = [a for a in sys.argv[1:] if not a.startswith('--')]
SRC = os.path.join(HERE, opts.get('src', 'Part2_Cheat_Sheet.html'))
OUT = os.path.join(HERE, opts['out']) if 'out' in opts else os.path.splitext(SRC)[0] + '_Handwritten.html'
PDF = os.path.splitext(OUT)[0] + '.pdf'
a = pos + [None] * 3
font = a[0] or "'Patrick Hand', 'Ink Free', 'Comic Sans MS', cursive"; size = float(a[1] or 8.9); lh = float(a[2] or 1.06)
s = open(SRC, encoding='utf-8').read()
link = '<style>\n' + open(os.path.join(HERE, 'fonts', 'fonts.css'), encoding='utf-8').read() + '</style>\n'
if 'ink-digits' in flags:
    link += ("<style>@font-face { font-family: 'HW Digits'; src: local('Ink Free'), local('InkFree'); "
             "unicode-range: U+00B2-00B3, U+00B9, U+00BC-00BE, U+2070-209F, U+2150-215F; }</style>\n")
    font = "'HW Digits', " + font
css = f'''
  /* ---- handwritten blue override ---- */
  body, .f, .f .lab, .head h1, .head span, .panel h2, .panel.qa h2, h3, th, td, table.m td, table.m td.t {{ font-family: {font}; }}
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
  .opt, p.r i, .ref {{ color: #3b5bb5; }}
  b {{ font-weight: 700; }}
'''
s = s.replace('</style>', css + '</style>', 1).replace('<style>', link + '<style>', 1)
s = re.sub(r'<title>(.*?)</title>', lambda m: f'<title>{m.group(1)} (handwritten)</title>', s, count=1)
open(OUT, 'w', encoding='utf-8', newline='\n').write(s)
edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

def print_pdf(html, pdf):
    if os.path.exists(pdf): os.remove(pdf)
    prof = tempfile.mkdtemp(prefix='edge_cheatsheet_')        # fresh profile: a reused one can silently write nothing
    subprocess.run([edge, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=8000',
                    '--user-data-dir=' + prof, '--print-to-pdf=' + pdf, 'file:///' + html.replace(os.sep, '/')], capture_output=True)
    for _ in range(60):
        if os.path.exists(pdf) and os.path.getsize(pdf) > 0: break
        time.sleep(0.5)
    time.sleep(1)
    shutil.rmtree(prof, ignore_errors=True)

print_pdf(OUT, PDF)
d = fitz.open(PDF); print('pages', len(d))
print('fonts', sorted({f[3] for p in d for f in p.get_fonts()}))
for pi, p in enumerate(d):
    for c, (x0, x1) in enumerate([(0, 285), (285, 565), (565, 842)]):
        bl = [b for b in p.get_text('blocks') if x0 <= b[0] < x1]
        bottom = max((b[3] for b in bl), default=0)
        print(f'side {pi+1} col {c+1} bottom {bottom:.0f}pt', '(OVERFLOW?)' if bottom > 572 else '')
d.close()

# Layout check: the .side boxes clip silently, so also measure every column's content. The script runs in screen
# media, so the body is pinned to the printed content width first (A4 landscape 297 mm minus two 6 mm margins).
JS = r'''<style>@media screen { body { width: 285mm; } }</style>
<script>window.addEventListener('load',function(){document.fonts.ready.then(function(){var o=[];
document.querySelectorAll('.side').forEach(function(sd){var t=sd.getBoundingClientRect(),c=[];sd.querySelectorAll('.col').forEach(function(col){var b=0;
col.querySelectorAll('*').forEach(function(e){var r=e.getBoundingClientRect();if(r.height>0&&r.bottom>b)b=r.bottom;});c.push(Math.round((b-t.top)*0.75));});
o.push({h:Math.round(t.height*0.75),c:c});});document.title='MEASURE'+JSON.stringify(o)+'END';});});</script>'''
tmp_html = os.path.splitext(OUT)[0] + '_measure_tmp.html'
tmp_pdf = os.path.join(tempfile.gettempdir(), 'cheatsheet_measure_tmp.pdf')
open(tmp_html, 'w', encoding='utf-8').write(s.replace('</head>', JS + '</head>', 1))
print_pdf(tmp_html, tmp_pdf)
os.remove(tmp_html)
m = re.search(r'MEASURE(.*?)END', fitz.open(tmp_pdf).metadata.get('title', '') if os.path.exists(tmp_pdf) else '')
if m:
    for i, sd in enumerate(json.loads(m.group(1))):
        print(f'layout side {i+1}: column bottoms ' + ', '.join(f'{c + 17}pt' + (' (CLIPPED)' if c > sd['h'] else '') for c in sd['c'])
              + f"  (page limit {sd['h'] + 17}pt)")
else:
    print('layout check unavailable')
