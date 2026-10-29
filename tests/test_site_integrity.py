"""Targeted regression checks for local URLs, case, CSS, SVG, and Pages paths."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from check_site_integrity import Checker


with TemporaryDirectory(prefix='hkb-links-') as folder:
    root = Path(folder)
    (root / 'assets').mkdir()
    (root / 'subjects').mkdir()
    (root / 'assets' / 'plot.png').write_bytes(b'png fixture')
    (root / 'assets' / 'style.css').write_text('body{background:url("./plot.png")}', encoding='utf-8')
    (root / 'assets' / 'icon.svg').write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><image href="plot.png"/></svg>', encoding='utf-8')
    (root / 'subjects' / '中文 note.html').write_text('<h1 id="section">OK</h1>', encoding='utf-8')
    (root / 'index.html').write_text(
        '<link href="assets/style.css" rel="stylesheet">'
        '<img src="assets/plot.png">'
        '<picture><source srcset="data:image/png;base64,AAAA 1x, assets/plot.png 2x, assets/missing.png 3x"></picture>'
        '<a href="subjects/%E4%B8%AD%E6%96%87%20note.html#section">中文页</a>'
        '<a href="https://example.com/elsewhere.html">外部</a>'
        '<img src="//example.com/remote.png">'
        '<img src="Assets/plot.png"><a href="/assets/plot.png">根路径</a>'
        '<a href="subjects/no-page.html">缺失页</a>', encoding='utf-8')
    result = Checker(root).run()
    types = {item['type'] for item in result.issues}
    assert types == {'missing_file', 'case_mismatch', 'root_absolute_url'}, result.issues
    assert sum(item['kind'] == 'image' for item in result.issues) == 3
    assert sum(item['kind'] == 'page' for item in result.issues) == 1
    assert result.counts['html_files'] == 2
    assert result.counts['references'] == 10
print('PASS: encoded Chinese URLs, srcset, CSS/SVG, case, root paths, missing pages')
