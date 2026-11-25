#!/usr/bin/env python3
"""Import selected Obsidian ZIP notes and their referenced images.

The archive is untrusted input: only Markdown and referenced image bytes are
copied, never arbitrary ZIP members or code. Re-running is deterministic.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARCHIVES = Path('/Users/andrewyu/Documents/Obsidian 知识库 zip 文件存档')
SELECTION = [
    ('数据结构', 'GPT02 数据结构线性表.zip', 'data-structures', 'GPT02 数据结构第二章：线性表.md'),
    ('数据结构', 'GPT03 数据结构栈和队列.zip', 'data-structures', 'GPT03数据结构第三章：栈和队列.md'),
    ('数据结构', 'GPT04数据结构串.zip', 'data-structures', 'GPT04 数据结构第四章：串.md'),
    ('数据结构', 'GPT05 数据结构数组和广义表.zip', 'data-structures', 'GPT05 数据结构第五章：数组和广义表.md'),
    ('数据结构', 'GPT06数据结构树和二叉树.zip', 'data-structures', '06 树和二叉树.md'),
    ('数据结构', 'GPT07数据结构图.zip', 'data-structures', '07 图.md'),
    ('数据结构', 'GPT08数据结构扣.zip', 'data-structures', '09 查找.md'),
    ('离散数学', 'GPT01离散数学.zip', 'discrete-math', 'GPT01命题逻辑基础：命题、联结词、命题公式与真值表.md'),
    ('离散数学', 'GPT02 离散数学.zip', 'discrete-math', 'GPT02命题逻辑命题公式、逻辑等值式与联结词完备集.md'),
    ('离散数学', 'GPT03 离散数学.zip', 'discrete-math', 'GPT03命题逻辑-范式：析取范式、合取范式与主范式.md'),
    ('离散数学', 'GPT4.5离散数学.zip', 'discrete-math', '04-05 推理与自然推理综合.md'),
    ('离散数学', 'GPT06离散数学.zip', 'discrete-math', '06 一阶逻辑基础.md'),
    ('离散数学', 'GPT07离散数学.zip', 'discrete-math', '07 一阶逻辑等值式.md'),
    ('离散数学', 'GPT08离散数学.zip', 'discrete-math', '08 谓词逻辑推理.md'),
    ('离散数学', 'GPT09离散数学.zip', 'discrete-math', '09 集合的基本概念.md'),
    ('离散数学', 'GPT10离散数学.zip', 'discrete-math', '10 集合运算与计数.md'),
    ('离散数学', 'GPT11离散数学.zip', 'discrete-math', '11 集合恒等式.md'),
    ('面向对象 CPP', 'C++第五讲_友元与程序组织_65幅原创插图_第五版终修防截断.zip', 'cpp-oop', '05 友元与程序组织.md'),
    ('面向对象 CPP', 'GPT06CPP.zip', 'cpp-oop', '06 重载与类型转换.md'),
    ('面向对象 CPP', 'GPT07CPP.zip', 'cpp-oop', '07 继承与派生类.md'),
    ('面向对象 CPP', 'GPT08CPP.zip', 'cpp-oop', '08 多态性与虚函数.md'),
]

WIKI = re.compile(r'!\[\[([^\]]+)\]\]')
STANDARD = re.compile(r'(!\[[^\]]*\]\()([^\)]+)(\))')
IMAGE_SUFFIXES = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg'}


def selected_source_keys() -> set[str]:
    return {f'{course}/{filename}' for _, _, course, filename in SELECTION}


def prepare(archives: Path, selection=None, *, prefer_svg=False, caption_from_context=False):
    """Validate every ZIP before writing any file; return prepared changes."""
    prepared = []
    for category, archive_name, course, filename in selection or SELECTION:
        archive = archives / category / archive_name
        with zipfile.ZipFile(archive) as bundle:
            entries = [i for i in bundle.infolist() if not i.is_dir()]
            if any(PurePosixPath(i.filename).is_absolute() or '..' in PurePosixPath(i.filename).parts
                   or ((i.external_attr >> 16) & 0o170000) == 0o120000 for i in entries):
                raise ValueError(f'Unsafe ZIP member: {archive}')
            if sum(i.file_size for i in entries) > 120_000_000:
                raise ValueError(f'Oversized archive: {archive}')
            markdown = [i for i in entries if i.filename.lower().endswith('.md')
                        and '/code/' not in i.filename.lower() and '图片质量说明' not in i.filename]
            if len(markdown) != 1:
                raise ValueError(f'Expected one primary note in {archive}: {[i.filename for i in markdown]}')
            images: dict[str, list[zipfile.ZipInfo]] = {}
            for info in entries:
                if PurePosixPath(info.filename).suffix.lower() in IMAGE_SUFFIXES:
                    images.setdefault(PurePosixPath(info.filename).name, []).append(info)
            vectors_by_topic: dict[str, list[str]] = {}
            for image_name in images:
                if image_name.lower().endswith('.svg'):
                    vectors_by_topic.setdefault(image_name.rsplit('_', 1)[0], []).append(image_name)
            content = bundle.read(markdown[0]).decode('utf-8-sig')
            used: dict[str, bytes] = {}
            media_id = hashlib.sha1(f'{course}/{filename}'.encode('utf-8')).hexdigest()[:10]
            target_dir = ROOT / 'sources' / course / '_assets' / media_id

            def image_ref(raw: str) -> str:
                name = PurePosixPath(unquote(raw.split('|', 1)[0])).name
                if prefer_svg and name.lower().endswith('.png'):
                    vector = name[:-4] + '.svg'
                    if vector in images:
                        name = vector
                    elif len(vectors_by_topic.get(name.rsplit('_', 1)[0], [])) == 1:
                        # Some exports give the PNG and SVG of the same diagram
                        # different UUIDs while retaining a unique topic stem.
                        name = vectors_by_topic[name.rsplit('_', 1)[0]][0]
                if name not in images:
                    raise ValueError(f'{archive.name}: missing referenced image {raw}')
                candidates = images[name]
                payloads = [bundle.read(info) for info in candidates]
                if len(set(payloads)) != 1:
                    raise ValueError(f'{archive.name}: ambiguous image basename {name}')
                data = payloads[0]
                if name.lower().endswith('.svg') and re.search(rb'<script\b|\bon\w+\s*=|(?:href|src)\s*=\s*["\'](?:https?:|//|javascript:)', data, re.I):
                    raise ValueError(f'{archive.name}: active or external SVG content in {name}')
                used[name] = data
                return f'./_assets/{media_id}/{quote(name, safe="-_.~")}'

            def wiki_replace(match: re.Match[str]) -> str:
                raw = match.group(1)
                if '|' in raw:
                    label = raw.split('|', 1)[1]
                elif caption_from_context:
                    following = content[match.end():]
                    caption = re.match(r'\s*\n\s*\*([^*\n]+)\*', following)
                    if caption and caption.group(1).strip().startswith('图'):
                        label = caption.group(1).strip()
                    else:
                        headings = re.findall(r'^#{1,6}\s+(.+)$', content[:match.start()], re.M)
                        label = headings[-1].strip() if headings else PurePosixPath(raw).stem
                else:
                    label = PurePosixPath(raw).stem
                label = label.replace('[', '').replace(']', '')
                return f'![{label}]({image_ref(raw)})'

            content = WIKI.sub(wiki_replace, content)
            content = STANDARD.sub(lambda m: m.group(1) + image_ref(m.group(2)) + m.group(3), content)
            content = content.rstrip('\n') + '\n'
            if '![[`' in content or WIKI.search(content):
                raise ValueError(f'{archive.name}: unresolved Obsidian image')
            prepared.append((archive, course, filename, content, target_dir, used,
                             hashlib.sha256(bundle.read(markdown[0])).hexdigest()))
    return prepared


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('archive_dir', nargs='?', type=Path, default=DEFAULT_ARCHIVES)
    args = parser.parse_args()
    prepared = prepare(args.archive_dir)
    report = []
    for archive, course, filename, content, target_dir, used, digest in prepared:
        target_dir.mkdir(parents=True, exist_ok=True)
        for name, data in used.items():
            (target_dir / name).write_bytes(data)
        dest = ROOT / 'sources' / course / filename
        dest.write_text(content, encoding='utf-8')
        report.append({'archive': str(archive.relative_to(args.archive_dir)),
                       'source': str(dest.relative_to(ROOT)), 'sha256': digest,
                       'referenced_images': len(used)})
        print(f'{dest.relative_to(ROOT)}: {len(used)} images')
    (ROOT / 'docs' / 'archive-import-report.json').write_text(
        json.dumps({'selected': report}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Imported {len(report)} selected notes.')


if __name__ == '__main__':
    main()
