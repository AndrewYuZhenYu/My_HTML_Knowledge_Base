"""Offline syntax highlighting and controls for fenced Markdown code blocks."""
from __future__ import annotations

from html import escape
import re

from bs4 import BeautifulSoup, NavigableString


CPP_TOKENS = re.compile(
    r'(?P<comment>//[^\n]*|/\*[\s\S]*?(?:\*/|$))'
    r'|(?P<string>"(?:\\[\s\S]|[^"\\])*"|\'(?:\\[\s\S]|[^\'\\])*\')'
    r'|(?P<directive>\#[A-Za-z_]\w*)'
    r'|(?P<angle><[A-Za-z_][\w./-]*>)'
    r'|(?P<number>\b(?:0[xX][\da-fA-F\']+|0[bB][01\']+|\d[\d\']*(?:\.\d[\d\']*)?(?:[eE][+-]?\d+)?)[uUlLfF]*\b)'
    r'|(?P<identifier>[A-Za-z_]\w*)'
    r'|(?P<operator>::|->|&&|\|\||==|!=|<=|>=|<<|>>|[+*/%=!&|^~?:<>-])'
    r'|(?P<plain>[\s\S])'
)

CPP_KEYWORDS = set('''alignas alignof asm break case catch class concept consteval constexpr constinit continue
default delete do else enum explicit export extern false for friend goto if inline namespace new
noexcept nullptr operator private protected public requires return static_assert static_cast struct
switch template this throw true try typedef typeid typename union using virtual while'''.split())
CPP_TYPES = set('''auto bool char char8_t char16_t char32_t const decltype double float int long short signed
unsigned void volatile wchar_t size_t ptrdiff_t string vector array deque list map unordered_map set
unordered_set pair tuple optional unique_ptr shared_ptr ostream istream'''.split())
SHELL_TOKENS = re.compile(
    r'(?P<comment>\#[^\n]*)'
    r'|(?P<string>"(?:\\[\s\S]|[^"\\])*"|\'(?:\\[\s\S]|[^\'\\])*\')'
    r'|(?P<variable>\$\{?[A-Za-z_][A-Za-z_0-9]*\}?)'
    r'|(?P<number>\b\d+(?:\.\d+)?\b)'
    r'|(?P<identifier>[A-Za-z_][\w-]*)'
    r'|(?P<operator>&&|\|\||[|><=])'
    r'|(?P<plain>[\s\S])'
)
SHELL_KEYWORDS = set('if then else elif fi for in do done case esac while function export local'.split())
LANGUAGES = {'cpp': 'C++', 'c++': 'C++', 'bash': 'Shell', 'sh': 'Shell', 'shell': 'Shell', 'text': '文本'}
COPY_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="8" y="8" width="11" height="12" rx="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h2"/></svg>'


def _span(kind: str, value: str) -> str:
    safe = escape(value)
    return f'<span class="tok-{kind}">{safe}</span>' if kind else safe


def tokens(source: str, language: str):
    """Yield colour classes and untouched source fragments."""
    if language not in ('cpp', 'c++', 'bash', 'sh', 'shell'):
        yield '', source
        return
    if language in ('cpp', 'c++'):
        include_header = False
        for token in CPP_TOKENS.finditer(source):
            kind, value = token.lastgroup, token.group()
            style = ''
            if kind == 'comment': style = 'comment'
            elif kind == 'string': style = 'string'
            elif kind == 'directive':
                style = 'directive'
                include_header = value == '#include'
            elif kind == 'angle' and include_header: style = 'string'
            elif kind == 'number': style = 'number'
            elif kind == 'identifier':
                if value in CPP_KEYWORDS: style = 'keyword'
                elif value in CPP_TYPES: style = 'type'
                elif value == 'std': style = 'namespace'
                elif re.match(r'\s*\(', source[token.end():]): style = 'function'
            elif kind == 'operator': style = 'operator'
            yield style, value
            if '\n' in value: include_header = False
    else:
        for token in SHELL_TOKENS.finditer(source):
            kind, value = token.lastgroup, token.group()
            style = {'comment': 'comment', 'string': 'string', 'variable': 'variable',
                     'number': 'number', 'operator': 'operator'}.get(kind, '')
            if kind == 'identifier':
                style = 'keyword' if value in SHELL_KEYWORDS else 'function' if value in ('python', 'python3', 'g++', 'cmake', 'make', 'git', 'node', 'npm') else ''
            yield style, value


def highlight(source: str, language: str) -> str:
    """Return escaped markup for syntax-coloured source."""
    return ''.join(_span(style, value) for style, value in tokens(source, language))


def enhance(soup: BeautifulSoup) -> int:
    """Add a compact editor toolbar and pre-rendered highlighting to article code."""
    count = 0
    for pre in list(soup.select('pre')):
        code = pre.find('code', recursive=False)
        if code is None:
            continue
        lang_class = next((name for name in code.get('class', []) if name.startswith('language-')), '')
        language = lang_class.removeprefix('language-') or 'text'
        source = code.get_text()
        code.clear()
        for style, value in tokens(source, language):
            if style:
                span = soup.new_tag('span')
                span['class'] = 'tok-' + style
                span.string = value
                code.append(span)
            else:
                code.append(NavigableString(value))
        panel = soup.new_tag('div')
        panel['class'] = 'code-panel'
        panel['data-language'] = language
        pre.wrap(panel)
        toolbar = soup.new_tag('div')
        toolbar['class'] = 'code-panel-toolbar'
        badge = soup.new_tag('span')
        badge['class'] = 'code-panel-language'
        badge.string = LANGUAGES.get(language, language.upper())
        button = soup.new_tag('button')
        button['class'] = 'code-copy'
        button['type'] = 'button'
        button['aria-label'] = '复制代码'
        button['title'] = '复制代码'
        button['data-copy-code'] = ''
        button.append(BeautifulSoup(COPY_ICON, 'html.parser'))
        caption = soup.new_tag('span')
        caption['class'] = 'code-copy-label'
        caption.string = '复制代码'
        button.append(caption)
        toolbar.append(badge)
        toolbar.append(button)
        panel.insert(0, toolbar)
        count += 1
    return count
