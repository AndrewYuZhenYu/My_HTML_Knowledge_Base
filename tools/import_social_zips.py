#!/usr/bin/env python3
"""Import eight social-science knowledge systems with vector-first figures."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from import_archive_zips import DEFAULT_ARCHIVES, prepare

ROOT = Path(__file__).resolve().parents[1]
SELECTION = [
    ('社会科学_认知拓展', '世界法学知识体系.zip', 'social-sciences', '01 世界法学知识体系.md'),
    ('社会科学_认知拓展', '政治学知识体系.zip', 'social-sciences', '02 政治学知识体系.md'),
    ('社会科学_认知拓展', '经济学知识体系_V2.5_Obsidian.zip', 'social-sciences', '03 经济学知识体系.md'),
    ('社会科学_认知拓展', '金融学知识体系.zip', 'social-sciences', '04 金融学知识体系.md'),
    ('社会科学_认知拓展', '投资学特别专栏_股票投资与证券交易实战_Obsidian.zip', 'social-sciences', '05 股票投资与证券交易.md'),
    ('社会科学_认知拓展', '会计学知识体系.zip', 'social-sciences', '06 会计学知识体系.md'),
    ('社会科学_认知拓展', '管理学知识体系.zip', 'social-sciences', '07 管理学知识体系.md'),
    ('社会科学_认知拓展', '心理学知识体系_Obsidian.zip', 'social-sciences', '08 心理学知识体系.md'),
]

DEMO_ANCHORS = {
    'law_dilution_demo': 'law_dilution',
    'politics_dhondt': 'politics_dhondt', 'politics_poll': 'politics_poll',
    'politics_effective': 'politics_effective',
    'invest_offline_calculators': 'invest_compound',
    'accounting_balance': 'accounting_balance',
    'accounting_depreciation': 'accounting_line_5cbcb66a',
    'accounting_breakeven': 'accounting_breakeven',
    'accounting_ccc': 'accounting_ccc', 'accounting_dupont': 'accounting_tree_f334',
    'accounting_npv': 'accounting_npv', 'accounting_leverage': 'accounting_leverage',
    'management_weighted': 'management_weighted', 'management_ltv': 'management_ltv',
    'management_eoq': 'management_eoq', 'management_evm': 'management_evm',
    'management_bep': 'management_bep', 'psych_bigfive': 'psych_radar',
}


def localize_demo_links(content: str) -> str:
    """Point obsolete Obsidian HTML embeds at their in-article recreations."""
    def replace(match: re.Match[str]) -> str:
        filename = match.group(1).rsplit('/', 1)[-1]
        label = match.group(2)
        anchor = next((target for prefix, target in DEMO_ANCHORS.items()
                       if filename.startswith(prefix + '_')), None)
        if not anchor:
            raise ValueError(f'No recreated widget for {filename}')
        return f'[{label}](#social-{anchor})'
    content = re.sub(r'\[\[(Assets/[^\]|]+\.html)\|([^\]]+)\]\]', replace, content)
    content = content.replace('（如 Obsidian 不直接打开 HTML，可在资源目录中使用浏览器打开。）', '')
    if re.search(r'\[\[[^\]]+\.html', content):
        raise ValueError('Unconverted Obsidian HTML widget link')
    return content


def selected_source_keys() -> set[str]:
    return {f'{course}/{filename}' for _, _, course, filename in SELECTION}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('archive_dir', nargs='?', type=Path, default=DEFAULT_ARCHIVES)
    args = parser.parse_args()
    staged = prepare(args.archive_dir, SELECTION, prefer_svg=True, caption_from_context=True)
    report = []
    for archive, course, filename, content, target_dir, used, digest in staged:
        target_dir.mkdir(parents=True, exist_ok=True)
        for name, data in used.items():
            (target_dir / name).write_bytes(data)
        source = ROOT / 'sources' / course / filename
        source.write_text(localize_demo_links(content), encoding='utf-8')
        report.append({'archive': str(archive.relative_to(args.archive_dir)),
                       'source': str(source.relative_to(ROOT)), 'archive_sha256': digest,
                       'figures': len(used),
                       'vectors': sum(name.lower().endswith('.svg') for name in used),
                       'raster_fallbacks': sum(not name.lower().endswith('.svg') for name in used)})
        print(f'{source.relative_to(ROOT)}: {len(used)} figures')
    (ROOT / 'docs' / 'social-archive-import-report.json').write_text(
        json.dumps({'selected': report}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Imported {len(report)} knowledge systems.')


if __name__ == '__main__':
    main()
