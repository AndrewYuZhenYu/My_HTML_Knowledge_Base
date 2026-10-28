"""Run after build: PYTHONPATH=.build-deps python3 tests/code_blocks.py."""
from pathlib import Path
from html import unescape
import re
import sys

from bs4 import BeautifulSoup

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'tools'))
from build import docs_list, md  # noqa: E402
from code_blocks import highlight  # noqa: E402

sample = '    #include <vector>\n    int n = 42; // 说明\n    std::string s = "if // literal";\n'
markup = BeautifulSoup(highlight(sample, 'cpp'), 'html.parser')
assert unescape(re.sub(r'</?span[^>]*>', '', highlight(sample, 'cpp'))) == sample
assert markup.select_one('.tok-directive').get_text() == '#include'
assert markup.select_one('.tok-comment').get_text() == '// 说明'
assert markup.select_one('.tok-string').get_text() == '<vector>'
assert markup.select_one('.tok-number').get_text() == '42'

total = 0
for doc in docs_list():
    original = BeautifulSoup(md(doc['source'].read_text(encoding='utf8')), 'html.parser').select('pre code')
    rendered = BeautifulSoup(doc['output'].read_text(encoding='utf8'), 'html.parser')
    blocks = rendered.select('article .code-panel pre code')
    assert len(original) == len(blocks), doc['source_rel']
    assert [n.get_text() for n in original] == [n.get_text() for n in blocks], doc['source_rel']
    assert len(rendered.select('article .code-copy')) == len(blocks), doc['source_rel']
    if blocks:
        assert rendered.select_one('script[src$="code-copy.js"]'), doc['source_rel']
    total += len(blocks)

assert total == 116, total
print(f'PASS: {total} highlighted code blocks preserve exact source and have copy controls')
