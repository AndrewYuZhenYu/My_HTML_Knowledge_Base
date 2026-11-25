"""Reconstruct imported social-science SVGs in the site's visual language.

The original vector coordinates and labels are retained as source evidence;
the published figure is rebuilt from supported primitives with new styling.
This does not change plotted data or diagram topology.
"""
from __future__ import annotations

import colorsys
import re
import xml.etree.ElementTree as ET
from pathlib import Path

SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
ALLOWED = {'svg', 'defs', 'g', 'path', 'rect', 'circle', 'ellipse', 'line',
           'polyline', 'polygon', 'text', 'tspan', 'use', 'marker', 'clipPath',
           'linearGradient', 'radialGradient', 'stop', 'pattern', 'image', 'title'}
INK = '#20343a'
MUTED = '#5f737b'
GRID = '#d5e1e4'
PAPER = '#ffffff'
TINT = '#f3f8f8'
PALETTE = {
    'blue': '#26729f', 'teal': '#15877b', 'amber': '#a76d21',
    'red': '#bd565e', 'purple': '#7755a5',
}
HEX = re.compile(r'#[0-9a-fA-F]{6}\b')


def color(value: str) -> str:
    low = value.lower()
    if low in {'none', 'transparent', 'currentcolor'} or low.startswith('url('):
        return value
    if low in {'white', '#fff'}:
        return PAPER
    if low in {'black', '#000'}:
        return INK
    if not HEX.fullmatch(value):
        return value
    r, g, b = (int(value[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    if s < .12:
        if v > .97:
            return PAPER
        if v > .88:
            return GRID
        return INK if v < .55 else MUTED
    if v > .94 and s < .20:
        return TINT
    if s < .26 and v > .80:
        return GRID if v < .89 else TINT
    if v < .38:
        return INK
    if s < .30 and v < .58:
        return MUTED
    family = None
    if h < .045 or h > .96:
        family = 'red'
    elif h < .14:
        family = 'amber'
    elif h < .49:
        family = 'teal'
    elif h < .70:
        family = 'blue'
    else:
        family = 'purple'
    base = PALETTE[family]
    base_rgb = [int(base[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    base_h = colorsys.rgb_to_hls(*base_rgb)[0]
    # Keep source light/dark relationships between series; changing every blue
    # to a single blue would erase information from multi-series plots.
    new_l = min(.65, max(.31, .38 + (v - .55) * .38))
    new_s = min(.76, max(.40, s * .83))
    out = colorsys.hls_to_rgb(base_h, new_l, new_s)
    return '#' + ''.join(f'{round(channel * 255):02x}' for channel in out)


def recreate(source: Path, dest: Path) -> None:
    original = ET.parse(source).getroot()

    def element(node: ET.Element) -> ET.Element | None:
        local = node.tag.rsplit('}', 1)[-1]
        if local not in ALLOWED:
            return None
        attrs = {}
        for name, value in node.attrib.items():
            key = name.rsplit('}', 1)[-1]
            if key.startswith('on') or key == 'href' and value.startswith(('http:', 'https:', 'file:')):
                continue
            if key in {'fill', 'stroke', 'stop-color'}:
                value = color(value)
            elif key == 'font-family':
                value = 'Inter, PingFang SC, Noto Sans CJK SC, sans-serif'
            elif key == 'style':
                value = HEX.sub(lambda m: color(m.group()), value)
            attrs[name] = value
        result = ET.Element(node.tag, attrs)
        result.text = node.text
        result.tail = node.tail
        for child in node:
            updated = element(child)
            if updated is not None:
                result.append(updated)
        return result

    rebuilt = element(original)
    if rebuilt is None:
        raise ValueError(f'Unsupported SVG root: {source}')
    rebuilt.set('data-redraw', 'source-geometry/site-style')
    dest.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(rebuilt).write(dest, encoding='utf-8', xml_declaration=True)
