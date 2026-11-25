"""Native HTML/SVG replacements for the investment chapter's source figures."""
from __future__ import annotations

from html import escape
import hashlib
import re
from pathlib import Path
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup

ET.register_namespace('', 'http://www.w3.org/2000/svg')


def table(title: str, headings: tuple[str, ...], rows: list[tuple[str, ...]], *, note: str = '') -> str:
    head = ''.join(f'<th scope="col">{escape(x)}</th>' for x in headings)
    body = ''.join('<tr>' + ''.join(f'<td>{escape(x)}</td>' for x in row) + '</tr>' for row in rows)
    foot = f'<p class="concept-visual-note">{escape(note)}</p>' if note else ''
    return (f'<figure class="concept-visual invest-native invest-table"><figcaption><span>网页数据表</span>'
            f'<strong>{escape(title)}</strong></figcaption><div class="invest-toolbar">'
            '<button type="button" data-invest-copy="table">复制表格数据</button></div>'
            f'<div class="invest-table-scroll"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>{foot}</figure>')


def dashboard(kind: str) -> str:
    if kind == 'invest_screen_time_':
        facts = [
            ('最新价', '38.56 元'), ('较昨收', '+3.51 元 / +10.01%'), ('昨收', '35.05 元'),
            ('开盘', '37.43 元'), ('最高 / 最低', '38.56 / 36.80 元'), ('分时均价', '38.02 元'),
            ('成交额', '23.87 亿元'), ('换手率', '8.24%'), ('量比', '1.02'),
            ('总 / 流通市值', '294.22 / 293.74 亿元'), ('PE TTM', '445.45 倍'),
            ('涨停状态', '7 天 5 板'), ('最高封单额', '2.11 亿元'), ('涨停成交额', '3.04 亿元'),
        ]
        title = '九阳股份 002242 · 分时行情快照'
        note = '根据所附午间截图重写；只有截图可辨认的读数。走势图不提供逐笔价格，避免虚构时间序列。'
        panel = 'time'
    else:
        facts = [
            ('最新价', '38.56 元'), ('较昨收', '+3.51 元 / +10.01%'), ('开 / 高 / 低', '37.43 / 38.56 / 36.80 元'),
            ('MA5', '33.13 元'), ('MA10', '30.76 元'), ('MA20', '27.56 元'), ('MA30', '25.22 元'),
            ('图示低点', '19.32 元'), ('午间量', '62.79 万（软件单位待核）'),
            ('量均线 M5 / M10', '100.8 / 110.9 万'),
            ('MACD / DIF / DEA', '+1.29 / +4.14 / +3.49'),
        ]
        title = '九阳股份 002242 · 日线截图读数'
        note = '根据截图可辨认数值重写；历史每日 OHLC 未从截图反推。图中为价格与均线的截面比较，不是历史 K 线。'
        panel = 'daily'
    data = ''.join(f'<div class="invest-stat"><dt>{escape(a)}</dt><dd>{escape(b)}</dd></div>' for a,b in facts)
    title_escaped = escape(title)
    return (f'<figure class="concept-visual invest-native invest-dashboard" data-invest-panel="{panel}">'
            f'<figcaption><span>截图内容重构</span><strong>{title_escaped}</strong></figcaption>'
            '<div class="invest-toolbar"><button type="button" data-invest-copy="stats">复制截图数据</button></div>'
            f'<dl class="invest-stats">{data}</dl>'
            '<svg class="invest-panel-chart" viewBox="0 0 760 310" role="img" aria-label="截图可辨认价格数据的示意图"></svg>'
            f'<p class="concept-visual-note">{escape(note)}</p></figure>')


def quote_demo() -> str:
    facts = [('最新价', '12.60 元'), ('涨跌', '+0.60 元 / +5.00%'), ('今开', '12.10 元'),
             ('昨收', '12.00 元'), ('最高 / 最低', '12.85 / 11.90 元'),
             ('成交量', '800 万股'), ('成交额', '约 0.98 亿元'), ('换手率', '2.40%')]
    stats = ''.join(f'<div class="invest-stat"><dt>{escape(a)}</dt><dd>{escape(b)}</dd></div>' for a,b in facts)
    return ('<figure class="concept-visual invest-native invest-dashboard" data-invest-panel="quote">'
            '<figcaption><span>可交互行情模型</span><strong>示例科技 · 股票行情界面</strong></figcaption>'
            '<div class="invest-toolbar"><label>观察时点 <input type="range" min="0" max="18" value="18" data-invest-time>'
            '<output>收盘附近</output></label><button type="button" data-invest-copy="stats">复制示例数据</button></div>'
            f'<dl class="invest-stats">{stats}</dl><svg class="invest-panel-chart" viewBox="0 0 760 310" role="img" '
            'aria-label="虚构的分时价格、均价与成交量"></svg>'
            '<p class="concept-visual-note">虚构行情，仅用于识别价格、均价和成交量；拖动滑块查看相应时点。</p></figure>')


def inline_svg(path: Path, title: str) -> str:
    """Inline generated vector primitives so labels are selectable DOM text."""
    # Strip the XML declaration before parsing as an HTML fragment.
    soup = BeautifulSoup(ET.tostring(ET.parse(path).getroot(), encoding='unicode'), 'html.parser')
    svg = soup.find('svg')
    if svg is None:
        raise ValueError(f'No SVG in {path}')
    for style in svg.find_all('style'):
        style.decompose()  # An SVG-wide '*' rule must not leak into article CSS.
    prefix = 'inv-' + hashlib.sha1(path.name.encode()).hexdigest()[:9] + '-'
    ids = {tag['id']: prefix + tag['id'] for tag in svg.find_all(id=True)}
    for tag in svg.find_all(True):
        for attr, value in list(tag.attrs.items()):
            if not isinstance(value, str):
                continue
            if attr == 'id' and value in ids:
                tag[attr] = ids[value]
            elif value.startswith('#') and value[1:] in ids:
                tag[attr] = '#' + ids[value[1:]]
            else:
                tag[attr] = re.sub(r'url\(#([^)]*)\)',
                                   lambda m: f'url(#{ids.get(m.group(1), m.group(1))})', value)
    svg['role'] = 'img'
    svg['aria-label'] = title
    svg['class'] = 'invest-inline-svg'
    svg.attrs.pop('width', None)
    svg.attrs.pop('height', None)
    return (f'<figure class="concept-visual invest-native invest-inline"><figcaption><span>网页内绘图</span>'
            f'<strong>{escape(title)}</strong></figcaption><div class="invest-toolbar">'
            '<button type="button" data-invest-copy="svg">复制图中文字</button></div>'
            f'{svg}</figure>')


def render(path: Path, title: str) -> str:
    name = path.name
    if name.startswith('invest_quote_'):
        return quote_demo()
    if name.startswith('invest_screen_time_'):
        return dashboard('invest_screen_time_')
    if name.startswith('invest_screen_daily_'):
        return dashboard('invest_screen_daily_')
    if name.startswith('invest_realquote_'):
        return table('午间行情字段', ('字段', '截图读数'), [
            ('最新价', '38.56 元'), ('较昨收', '+3.51 元 / +10.01%'), ('昨收', '35.05 元'),
            ('开盘', '37.43 元'), ('最高 / 最低', '38.56 / 36.80 元'), ('分时均价', '38.02 元'),
            ('总市值', '294.22 亿元'), ('流通市值', '293.74 亿元'), ('PE TTM', '445.45 倍'),
            ('量比', '1.02'), ('换手率', '8.24%'), ('成交额', '23.87 亿元'),
            ('涨停状态', '7 天 5 板'), ('人气排名', '1 / 4284')],
            note='数据来自用户提供的午间截图，并非实时行情。')
    if name.startswith('invest_limitbook_'):
        return table('涨停盘口 · 买单排队与实际成交', ('档位 / 字段', '价格 / 金额', '挂单数量 / 说明'), [
            ('买1', '38.56 元', '5.30 万（截图原显示）'), ('买2', '38.55 元', '170'),
            ('买3', '38.54 元', '254'), ('买4', '38.53 元', '83'), ('买5', '38.52 元', '273'),
            ('最高封单额', '2.11 亿元', '封单可撤销'),
            ('涨停成交额', '3.04 亿元', '已成交，不是挂单')],
            note='截图字段重写；买单数量的单位以行情软件设置为准，不自行换算为股数。')
    if path.suffix.lower() == '.svg':
        return inline_svg(path, title)
    raise ValueError(f'Unhandled investment media: {path}')
