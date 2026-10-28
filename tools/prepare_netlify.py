#!/usr/bin/env python3
"""Create a small, self-contained folder for Netlify's manual drag-and-drop deploy."""
from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote, urlsplit
from html.parser import HTMLParser
import shutil


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'netlify-upload'
PUBLISH_ITEMS = ('index.html', 'assets', 'subjects', 'sources', 'docs')


class References(HTMLParser):
 def __init__(self):
  super().__init__(); self.references=[]
 def handle_starttag(self, tag, attrs):
  values=dict(attrs)
  for key in ('href','src'):
   value=values.get(key)
   if value:self.references.append(value)


def verify_links():
 broken=[]
 for page in OUTPUT.rglob('*.html'):
  parser=References();parser.feed(page.read_text(encoding='utf-8'))
  for raw in parser.references:
   parts=urlsplit(raw)
   if parts.scheme or parts.netloc or not parts.path:continue
   relative=unquote(parts.path)
   target=(OUTPUT/relative.lstrip('/')) if relative.startswith('/') else (page.parent/relative)
   resolved=target.resolve()
   if not resolved.is_relative_to(OUTPUT.resolve()) or not resolved.is_file():
    broken.append(f'{page.relative_to(OUTPUT)} → {raw}')
 if broken:raise SystemExit('Broken local links in upload folder:\n'+'\n'.join(broken[:30]))


def main():
 for item in PUBLISH_ITEMS:
  if not (ROOT/item).exists():raise SystemExit(f'Missing build output: {item}')
 if OUTPUT.exists():shutil.rmtree(OUTPUT)
 OUTPUT.mkdir()
 for item in PUBLISH_ITEMS:
  source=ROOT/item;dest=OUTPUT/item
  if source.is_dir():shutil.copytree(source,dest)
  else:shutil.copy2(source,dest)
 verify_links()
 files=[p for p in OUTPUT.rglob('*') if p.is_file()]
 size=sum(p.stat().st_size for p in files)
 largest=max(files,key=lambda p:p.stat().st_size)
 print(f'Prepared {OUTPUT}')
 print(f'{len(files)} files, {size/1024/1024:.1f} MiB; largest: {largest.relative_to(OUTPUT)} ({largest.stat().st_size/1024/1024:.1f} MiB)')
 print('All local HTML href/src links resolve within the upload folder.')


if __name__=='__main__':main()
