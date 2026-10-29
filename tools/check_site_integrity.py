#!/usr/bin/env python3
"""Check generated pages, static assets, anchors, and optional Git publish trees."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from functools import lru_cache
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
CSS_URL = re.compile(r'url\(\s*["\']?([^"\')]+)', re.I)
CSS_IMPORT = re.compile(r'@import\s+["\']([^"\']+)["\']', re.I)
JS_LITERAL = re.compile(
    r'(?:\.src\s*=|\.href\s*=|fetch\s*\(|new\s+URL\s*\()\s*["\']([^"\']+\.(?:html?|css|js|png|jpe?g|gif|webp|svg)(?:[?#][^"\']*)?)["\']',
    re.I,
)
SRCSET = {'img', 'source'}
LINK_ATTRS = {
    'a': ('href',), 'link': ('href',), 'script': ('src',),
    'img': ('src',), 'source': ('src',), 'iframe': ('src',),
    'video': ('src', 'poster'), 'audio': ('src',), 'track': ('src',),
    'embed': ('src',), 'object': ('data',), 'input': ('src',),
    'image': ('href', 'xlink:href'), 'use': ('href', 'xlink:href'),
}
IMAGE_EXT = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.avif'}


def srcset_urls(value: str):
    """Keep commas inside data: URLs while splitting image candidates."""
    pos = 0
    while pos < len(value):
        while pos < len(value) and value[pos] in ' \t\r\n,':
            pos += 1
        start = pos
        is_data = value[pos:pos + 5].lower() == 'data:'
        while pos < len(value) and not value[pos].isspace() and (is_data or value[pos] != ','):
            pos += 1
        if pos > start:
            yield value[start:pos]
        while pos < len(value) and value[pos] != ',':
            pos += 1
        pos += 1


def generated_html(root: Path) -> list[Path]:
    pages = [root / 'index.html']
    pages += list((root / 'subjects').rglob('*.html'))
    pages += list((root / 'docs').rglob('*.html'))
    return sorted(p for p in pages if p.is_file())


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs: list[tuple[str, str]] = []
        self.ids: set[str] = set()
        self.in_style = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get('id'):
            self.ids.add(values['id'])
        for attr in LINK_ATTRS.get(tag, ()):
            if values.get(attr):
                self.refs.append((f'{tag}[{attr}]', values[attr]))
        if tag in SRCSET and values.get('srcset'):
            self.refs.extend((f'{tag}[srcset]', url) for url in srcset_urls(values['srcset']))
        if values.get('style'):
            self.refs.extend(('style[url]', url.strip()) for url in CSS_URL.findall(values['style']))
        if tag == 'style':
            self.in_style = True

    def handle_endtag(self, tag):
        if tag == 'style':
            self.in_style = False

    def handle_data(self, data):
        if self.in_style:
            self.refs.extend(('style[url]', url.strip()) for url in CSS_URL.findall(data))


@lru_cache(maxsize=None)
def directory_names(path: Path) -> tuple[str, ...]:
    try:
        return tuple(item.name for item in path.iterdir())
    except (FileNotFoundError, NotADirectoryError):
        return ()


def case_match(path: Path) -> Path | None:
    """Find a same-name path with different case on case-insensitive development disks."""
    parts = path.parts
    current = Path(parts[0])
    changed = False
    for part in parts[1:]:
        names = directory_names(current)
        if part in names:
            current /= part
            continue
        match = next((name for name in names if name.casefold() == part.casefold()), None)
        if match is None:
            return None
        current /= match
        changed = True
    return current if changed else None


def git_paths(root: Path, ref: str | None) -> set[str]:
    command = ['git', 'ls-tree', '-r', '--name-only', '-z', ref] if ref else ['git', 'ls-files', '-z']
    result = subprocess.run(command, cwd=root, capture_output=True, check=True)
    return {name.decode('utf-8') for name in result.stdout.split(b'\0') if name}


class Checker:
    def __init__(self, root: Path, ref: str | None = None, require_tracked: bool = False):
        self.root = root.resolve()
        self.ref = ref
        self.tracked = git_paths(self.root, ref) if ref or require_tracked else None
        self.pages = generated_html(self.root)
        self.parsed: dict[Path, PageParser] = {}
        self.issues: list[dict[str, str]] = []
        self.counts = Counter()

    def relative(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def issue(self, code: str, source: Path, raw: str, kind: str, advice: str, target: Path | None = None):
        self.issues.append({
            'type': code, 'kind': kind, 'source': self.relative(source),
            'reference': raw, 'target': self.relative(target) if target and target.is_relative_to(self.root) else '',
            'suggestion': advice,
        })

    def kind(self, context: str, path: str) -> str:
        suffix = Path(path).suffix.lower()
        if suffix in IMAGE_EXT or context.startswith(('img[', 'image[', 'source[', 'video[poster]')):
            return 'image'
        if suffix in {'.html', '.htm'} or context == 'a[href]' and (not suffix or path.endswith('/')):
            return 'page'
        return 'resource'

    def parse_page(self, path: Path) -> PageParser:
        if path not in self.parsed:
            parser = PageParser()
            parser.feed(path.read_text(encoding='utf-8'))
            self.parsed[path] = parser
        return self.parsed[path]

    def check_ref(self, source: Path, context: str, raw: str, *, site_root: bool = False):
        raw = raw.strip()
        if not raw:
            return
        split = urlsplit(raw)
        scheme = split.scheme.lower()
        if (scheme in {'http', 'https'} or split.netloc) and split.hostname not in {'localhost', '127.0.0.1', '::1'}:
            return
        if scheme in {'data', 'blob', 'mailto', 'tel'}:
            return
        if scheme and scheme not in {'file', 'javascript', 'http', 'https'}:
            return
        self.counts['references'] += 1
        kind = self.kind(context, split.path)
        self.counts[kind + '_references'] += 1
        if scheme or split.netloc:
            self.issue('local_only_or_unsafe_url', source, raw, kind, 'Use a relative repository path; remove file:// and localhost URLs.')
            return
        if split.path.startswith('/'):
            self.issue('root_absolute_url', source, raw, kind, 'Use a path relative to this page so GitHub Pages project prefixes and file:// both work.')
            return
        decoded = unquote(split.path)
        if '\\' in decoded:
            self.issue('backslash_url', source, raw, kind, 'Use forward slashes in web URLs.')
            return
        target = (self.root / decoded if site_root else source.parent / decoded).resolve() if decoded else source.resolve()
        if not target.is_relative_to(self.root):
            self.issue('outside_site', source, raw, kind, 'Keep referenced files inside the publish root.')
            return
        if target.is_dir():
            target /= 'index.html'
        matched = case_match(target)
        if matched and matched.is_file():
            self.issue('case_mismatch', source, raw, kind, f'Use exact case: {self.relative(matched)}', target)
            return
        if not target.is_file():
            self.issue('missing_file', source, raw, kind, 'Check the relative path and ensure the target is generated and included in Git.', target)
            return
        if self.tracked is not None and self.relative(target) not in self.tracked:
            label = self.ref or 'the Git index'
            self.issue('not_in_publish_tree', source, raw, kind, f'Add this file to {label} before publishing.', target)
        if split.fragment and target.suffix.lower() in {'.html', '.htm'}:
            anchor = unquote(split.fragment)
            if anchor not in self.parse_page(target).ids:
                self.issue('missing_anchor', source, raw, 'page', 'Regenerate the mind map or correct the target heading ID.', target)

    def run(self):
        self.counts['html_files'] = len(self.pages)
        for page in self.pages:
            if self.tracked is not None and self.relative(page) not in self.tracked:
                self.issue('page_not_in_publish_tree', page, self.relative(page), 'page',
                           f'Add the generated page to {self.ref or "the Git index"} before publishing.', page)
            parsed = self.parse_page(page)
            for context, raw in parsed.refs:
                self.check_ref(page, context, raw)
        for css in (self.root / 'assets').rglob('*.css'):
            content = css.read_text(encoding='utf-8')
            for url in CSS_URL.findall(content) + CSS_IMPORT.findall(content):
                self.check_ref(css, 'css[url]', url)
        for svg in self.root.rglob('*.svg'):
            if any(part in {'.git', 'netlify-upload', 'node_modules', '.venv', '.build-deps'} for part in svg.relative_to(self.root).parts):
                continue
            try:
                tree = ElementTree.parse(svg)
            except ElementTree.ParseError:
                self.issue('invalid_svg', svg, '', 'image', 'Repair malformed SVG markup.')
                continue
            for element in tree.iter():
                for attr, value in element.attrib.items():
                    if attr.endswith('}href') or attr in {'href', 'xlink:href'}:
                        self.check_ref(svg, 'svg[href]', value)
        for js in (self.root / 'assets').rglob('*.js'):
            if js.name == 'search-data.js':
                prefix = 'window.HKB_SEARCH_INDEX='
                content = js.read_text(encoding='utf-8').strip().rstrip(';')
                if not content.startswith(prefix):
                    self.issue('invalid_search_index', js, '', 'page', 'Rebuild assets/search-data.js.')
                    continue
                try:
                    entries = json.loads(content[len(prefix):])
                except json.JSONDecodeError:
                    self.issue('invalid_search_index', js, '', 'page', 'Rebuild assets/search-data.js.')
                    continue
                for entry in entries:
                    self.check_ref(js, 'search[url]', entry['url'], site_root=True)
            else:
                for url in JS_LITERAL.findall(js.read_text(encoding='utf-8')):
                    self.check_ref(js, 'js[literal]', url)
        return self


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--git-ref', help='Compare referenced files with a Git tree, e.g. origin/main.')
    parser.add_argument('--require-tracked', action='store_true', help='Require every referenced file in the Git index.')
    parser.add_argument('--json-out', type=Path, help='Write the full report as JSON.')
    parser.add_argument('--limit', type=int, default=25, help='Maximum issues printed.')
    args = parser.parse_args()
    report = Checker(args.root, args.git_ref, args.require_tracked).run()
    counts = Counter(item['type'] for item in report.issues)
    summary = {'root': str(report.root), 'git_ref': args.git_ref, 'counts': dict(report.counts),
               'issue_count': len(report.issues), 'issue_types': dict(counts), 'issues': report.issues}
    if args.json_out:
        args.json_out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Scanned {report.counts['html_files']} HTML files and {report.counts['references']} local references "
          f"({report.counts['image_references']} images, {report.counts['page_references']} pages).")
    for item in report.issues[:args.limit]:
        print(f"{item['type']}: {item['source']} → {item['reference']} "
              f"[{item['kind']}] {item['suggestion']}")
    if len(report.issues) > args.limit:
        print(f'... {len(report.issues) - args.limit} more; use --json-out for all details.')
    print('Issue types:', dict(counts) if counts else 'none')
    return 1 if report.issues else 0


if __name__ == '__main__':
    sys.exit(main())
