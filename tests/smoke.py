"""Static smoke test: python tests/smoke.py (after build)."""
from pathlib import Path
from bs4 import BeautifulSoup
import json
root=Path(__file__).resolve().parents[1]
note=BeautifulSoup((root/'subjects/physics/12-gas-theory.html').read_text(encoding='utf8'),'html.parser')
mp=BeautifulSoup((root/'subjects/physics/12-mindmap.html').read_text(encoding='utf8'),'html.parser')
report=json.loads((root/'docs/conversion-report.json').read_text(encoding='utf8'))
assert len(note.select('article h1,article h2,article h3,article h4'))==48
assert len(note.select('article .math-inline,article .math-display'))==341
assert len(note.select('article .callout'))==47
assert {'note','important','warning','tip','example','summary'}.issubset({n['data-callout'] for n in note.select('.callout')})
assert len(mp.select('details.map-branch'))==8
assert len(mp.select('.map-leaf[href]'))==32
assert report['total_documents']==12
articles=[]
for page in (root/'subjects').rglob('*.html'):
 doc=BeautifulSoup(page.read_text(encoding='utf8'),'html.parser')
 if not doc.select_one('article.reading-content'):continue
 articles.append(page)
 figures=doc.select('article figure.concept-visual')
 assert len(figures)>=20,page
 assert all(fig.find('svg') and fig.find('figcaption') and fig.parent.name!='p' for fig in figures)
 link=doc.select_one('article .chapter-links a[href$="-mindmap.html"]')
 assert link,page
 map_page=page.parent/link['href']
 mindmap=BeautifulSoup(map_page.read_text(encoding='utf8'),'html.parser')
 assert len(mindmap.select('details.map-branch'))>=4,map_page
 ids={node['id'] for node in doc.select('article [id]')}
 for leaf in mindmap.select('a.map-leaf[href]'):
  file,anchor=leaf['href'].split('#',1)
  assert (map_page.parent/file).resolve()==page.resolve()
  assert anchor in ids,(map_page,anchor)
assert len(articles)==12
assert all(file['visual_count']>=20 for file in report['files'].values())
assert sum(file['visual_count'] for file in report['files'].values())>=240
assert sum(file['visual_count'] for name,file in report['files'].items() if name.startswith('physics/'))>=60
physics_pages=[BeautifulSoup((root/'subjects/physics'/name).read_text(encoding='utf8'),'html.parser') for name in ('12-gas-theory.html','13-thermodynamics.html','14-oscillations.html')]
widgets=[widget for page in physics_pages for widget in page.select('article figure.physics-widget')]
assert len(widgets)==10
assert all(widget.select_one('svg[role="img"]') and widget.select_one('.physics-controls input[type="range"]') for widget in widgets)
assert physics_pages[0].select_one('article .inline-viz #maxwellPlot')
assert sum(bool(page.select_one('script[src$="physics-widgets.js"]')) for page in physics_pages)==3
assert len(physics_pages[2].select('article figure.concept-visual'))>=20
learning=[]
scientific=[]
traces=[]
for page in articles:
 doc=BeautifulSoup(page.read_text(encoding='utf8'),'html.parser')
 learning.extend(doc.select('article figure.learning-widget'))
 scientific.extend(doc.select('article figure.scientific-widget'))
 traces.extend(doc.select('article figure.trace-widget'))
assert len(learning)==9
assert len(scientific)==8
assert len(traces)==18
assert all(node.select_one('.scientific-controls input[type="range"]') for node in scientific)
assert all(node.select_one('.trace-controls button[data-step="next"]') for node in traces)
assert {node['data-kind'] for node in learning}=={'stepper','truth'}
for node in learning:
 assert node.select_one('svg[role="img"]') and node.select_one('.learning-controls')
 if node['data-kind']=='stepper':assert len(json.loads(node['data-states']))>=3
 else:assert len(json.loads(node['data-rows'])) in (4,8)
print('PASS: 12 articles / 12 linked maps / 20 figures each / 240 counted figures / 46 inline interactive components including Maxwell')
