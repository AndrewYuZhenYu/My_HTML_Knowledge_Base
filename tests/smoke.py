"""Static smoke test: python tests/smoke.py (after build)."""
from pathlib import Path
from bs4 import BeautifulSoup
import json

root = Path(__file__).resolve().parents[1]
report = json.loads((root / 'docs/conversion-report.json').read_text(encoding='utf8'))
assert report['total_documents'] == 13
assert not report['warnings'] and not report['math_errors']

articles = []
for page in (root / 'subjects').rglob('*.html'):
    doc = BeautifulSoup(page.read_text(encoding='utf8'), 'html.parser')
    article = doc.select_one('article.reading-content')
    if not article:
        continue
    articles.append(page)
    diagrams = article.select('figure.concept-visual')
    images = article.select('img[src]')
    assert len(diagrams) + len(images) >= 15, page
    assert all(fig.find('svg') and fig.find('figcaption') and fig.parent.name != 'p' for fig in diagrams), page
    for image in images:
        assert (page.parent / image['src']).is_file(), (page, image['src'])
    link = article.select_one('.chapter-links a[href$="-mindmap.html"]')
    assert link, page
    map_page = page.parent / link['href']
    mindmap = BeautifulSoup(map_page.read_text(encoding='utf8'), 'html.parser')
    assert len(mindmap.select('details.map-branch')) >= 4, map_page
    ids = {node['id'] for node in article.select('[id]')}
    for leaf in mindmap.select('a.map-leaf[href]'):
        file, anchor = leaf['href'].split('#', 1)
        assert (map_page.parent / file).resolve() == page.resolve()
        assert anchor in ids, (map_page, anchor)

assert len(articles) == 13
assert all(item['visual_count'] >= 15 for item in report['files'].values())
expected = {'12-gas-theory.html': 40, '13-thermodynamics.html': 28,
            '14-oscillations.html': 42, '15-waves.html': 35}
for filename, image_count in expected.items():
    page = root / 'subjects' / 'physics' / filename
    assert page in articles
    doc = BeautifulSoup(page.read_text(encoding='utf8'), 'html.parser')
    assert len(doc.select('article.reading-content img[src]')) == image_count, page
    assert len(doc.select('article.reading-content .math-inline, article.reading-content .math-display')) > 100, page
    assert len(doc.select('article.reading-content .callout')) >= 15, page

physics_pages = [BeautifulSoup((root / 'subjects' / 'physics' / filename).read_text(encoding='utf8'), 'html.parser')
                 for filename in expected]
widgets = [widget for page in physics_pages for widget in page.select('article figure.physics-widget')]
assert len(widgets) == 10
assert all(widget.select_one('svg[role="img"]') and widget.select_one('.physics-controls input[type="range"]')
           for widget in widgets)
assert physics_pages[0].select_one('article .inline-viz #maxwellPlot')
assert sum(bool(page.select_one('script[src$="physics-widgets.js"]')) for page in physics_pages) == 3

learning = []
scientific = []
traces = []
for page in articles:
    doc = BeautifulSoup(page.read_text(encoding='utf8'), 'html.parser')
    learning.extend(doc.select('article figure.learning-widget'))
    scientific.extend(doc.select('article figure.scientific-widget'))
    traces.extend(doc.select('article figure.trace-widget'))
assert len(learning) == 9
assert len(scientific) == 6
assert len(traces) == 18
assert all(node.select_one('.scientific-controls input[type="range"]') for node in scientific)
assert all(node.select_one('.trace-controls button[data-step="next"]') for node in traces)
assert {node['data-kind'] for node in learning} == {'stepper', 'truth'}
for node in learning:
    assert node.select_one('svg[role="img"]') and node.select_one('.learning-controls')
    if node['data-kind'] == 'stepper':
        assert len(json.loads(node['data-states'])) >= 3
    else:
        assert len(json.loads(node['data-rows'])) in (4, 8)
print('PASS: 13 articles, linked mind maps, 145 ZIP images, 10 physics widgets, learning interactions')
