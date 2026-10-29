#!/usr/bin/env python3
"""Import the four authoritative physics ZIP chapters into local Markdown sources."""
from __future__ import annotations

from pathlib import Path
import argparse
import re
import zipfile


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'sources' / 'physics'
CHAPTERS = {
    12: ('GPT12 气体动理论.zip', '12 气体动理论.md'),
    13: ('GPT13 热力学基础.zip', '13 热力学基础｜知识体系重构版.md'),
    14: ('GPT14振动.zip', '14 振动 扩充版.md'),
    15: ('GPT15 波动.zip', '15 波动.md'),
}
WIKI_IMAGE = re.compile(r'!\[\[([^\]]+)\]\]')
MARKDOWN_IMAGE = re.compile(r'(!\[[^\]]*\]\()([^\)]+)(\))')


def import_chapter(chapter: int, archive: Path) -> None:
    with zipfile.ZipFile(archive) as bundle:
        files = [info for info in bundle.infolist() if not info.is_dir()]
        if any(Path(info.filename).is_absolute() or '..' in Path(info.filename).parts or
               (info.external_attr >> 16) & 0o170000 == 0o120000 for info in files):
            raise ValueError(f'Unsafe ZIP entry in {archive}')
        if sum(info.file_size for info in files) > 100_000_000:
            raise ValueError(f'ZIP exceeds expected size: {archive}')
        markdown = [info for info in files if info.filename.lower().endswith('.md')]
        if len(markdown) != 1:
            raise ValueError(f'Expected one Markdown file in {archive}')
        images = {Path(info.filename).name: info for info in files if info.filename.lower().endswith('.png')}
        if len(images) != len([info for info in files if info.filename.lower().endswith('.png')]):
            raise ValueError(f'Duplicate image filename in {archive}')
        content = bundle.read(markdown[0]).decode('utf-8-sig')
        referenced: set[str] = set()

        def image_path(raw: str) -> str:
            name = Path(raw.split('|', 1)[0]).name
            if name not in images:
                raise ValueError(f'Image {raw!r} not found in {archive}')
            referenced.add(name)
            return f'./_assets/zip{chapter}/images/{name}'

        def wiki_image(match: re.Match[str]) -> str:
            following = content[match.end():]
            caption = re.match(r'\s*\n\s*\*([^*\n]+)\*', following)
            if caption and caption.group(1).strip().startswith('图'):
                alt = caption.group(1).strip()
            else:
                headings = re.findall(r'^#{1,6}\s+(.+)$', content[:match.start()], re.M)
                alt = (headings[-1] if headings else f'第 {chapter} 章') + '配图'
            return f'![{alt.replace("$", "")}]({image_path(match.group(1))})'

        content = WIKI_IMAGE.sub(wiki_image, content)
        content = MARKDOWN_IMAGE.sub(lambda match: match.group(1) + image_path(match.group(2)) + match.group(3), content)
        if referenced != set(images):
            raise ValueError(f'Unreferenced image(s) in {archive}: {set(images) - referenced}')

        image_dir = DEST / '_assets' / f'zip{chapter}' / 'images'
        image_dir.mkdir(parents=True, exist_ok=True)
        for name, info in images.items():
            (image_dir / name).write_bytes(bundle.read(info))
        (DEST / CHAPTERS[chapter][1]).write_text(content, encoding='utf-8')
        print(f'Imported chapter {chapter}: {len(images)} images, {len(content)} characters')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('archive_dir', type=Path)
    args = parser.parse_args()
    for chapter, (filename, _) in CHAPTERS.items():
        import_chapter(chapter, args.archive_dir / filename)


if __name__ == '__main__':
    main()
