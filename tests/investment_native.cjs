const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

class Element {
  constructor(tag) { this.tag = tag; this.children = []; this.attributes = {}; this.textContent = ''; }
  setAttribute(key, value) { this.attributes[key] = String(value); }
  appendChild(child) { this.children.push(child); return child; }
  replaceChildren() { this.children = []; }
}
function figure(panel, copyKind) {
  const svg = panel ? new Element('svg') : null;
  const input = panel === 'quote' ? { value: '18', nextElementSibling: { textContent: '' },
    addEventListener(_, fn) { this.update = fn; } } : null;
  const button = { dataset: { investCopy: copyKind }, textContent: '复制',
    addEventListener(_, fn) { this.click = fn; } };
  const row = { querySelectorAll: () => [{ textContent: '买1' }, { textContent: '38.56' }, { textContent: '5.30万' }] };
  const stat = { querySelector: key => ({ textContent: key === 'dt' ? '最新价' : '38.56 元' }) };
  return {
    dataset: { investPanel: panel }, svg, input, button,
    querySelector(key) {
      if (key === '.invest-panel-chart') return svg;
      if (key === '[data-invest-time]') return input;
      if (key === '[data-invest-copy]') return button;
    },
    querySelectorAll(key) {
      if (key === '.invest-stat') return [stat];
      if (key === 'table tr') return [row];
      if (key === 'svg text') return [{ textContent: '可复制的矢量图文字' }];
      return [];
    }
  };
}

(async () => {
  const figures = [figure('quote', 'stats'), figure('time', 'stats'), figure('daily', 'stats'),
    figure('', 'table'), figure('', 'svg')];
  let copied = '';
  let fallbackValue = '';
  const document = { createElementNS: (_, tag) => new Element(tag),
    createElement: () => ({ value: '', style: {}, select() { fallbackValue = this.value; }, remove() {} }),
    body: { appendChild() {} }, execCommand: () => true,
    querySelectorAll: key => key === '.invest-native' ? figures : [] };
  const navigator = { clipboard: { async writeText(value) { copied = value; } } };
  const source = fs.readFileSync(path.join(__dirname, '../assets/investment-native.js'), 'utf8');
  vm.runInNewContext(source, { document, navigator, setTimeout: () => {}, console });
  for (const item of figures.slice(0, 3)) assert.ok(item.svg.children.length > 10, item.dataset.investPanel);
  for (const point of ['0', '18']) {
    figures[0].input.value = point;
    figures[0].input.update();
    assert.ok(figures[0].svg.children.length > 10);
    assert.equal(figures[0].input.nextElementSibling.textContent, `${Number(point) + 1} / 19`);
  }
  figures[3].button.click(); await Promise.resolve();
  assert.equal(copied, '买1\t38.56\t5.30万');
  figures[4].button.click(); await Promise.resolve();
  assert.equal(copied, '可复制的矢量图文字');
  figures[1].button.click(); await Promise.resolve();
  assert.equal(copied, '最新价\t38.56 元');
  navigator.clipboard.writeText = async () => { throw new Error('file protocol denied'); };
  figures[3].button.click(); await new Promise(setImmediate);
  assert.equal(fallbackValue, '买1\t38.56\t5.30万');
  console.log('PASS: quote slider, screenshot charts, table and text copying');
})().catch(error => { console.error(error); process.exitCode = 1; });
