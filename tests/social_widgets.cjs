const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { spawnSync } = require('node:child_process');
const m = require('../assets/social-widgets.js');
const close = (actual, expected, tolerance = 1e-8) => assert.ok(Math.abs(actual - expected) < tolerance, `${actual} != ${expected}`);

close(m.compound(1000, 0.05, 2), 1102.5);
close(m.bondPrice(0.05, 3, 0.05), 100);
assert.ok(m.bondPrice(0.05, 3, 0.07) < 100);
assert.deepEqual(m.dhondt([300, 210, 120], 7).seats, [4, 2, 1]);
close(m.bayes(0.01, 0.9, 0.95).ppv, 0.009 / (0.009 + 0.0495));
close(m.eoq(1000, 40, 2), 200);
close(m.npv(100, 60, 0, 2), 20);
close(m.breakEven(100, 60, 4000), 100);
close(m.portfolioRisk(1, 0), 0.25);
close(m.winrate(1, 0), 0.5);

const root = path.resolve(__dirname, '..');
const config = spawnSync('python3', ['-c',
  'import sys,json;sys.path.insert(0,"tools");from social_widgets import WIDGETS;print(json.dumps([x for group in WIDGETS.values() for x in group],ensure_ascii=False))'],
  { cwd: root, encoding: 'utf8' });
assert.equal(config.status, 0, config.stderr);
const specs = JSON.parse(config.stdout);
assert.equal(specs.length, 43);

class Shape {
  constructor(tag) { this.tag = tag; this.children = []; this.attributes = {}; this.textContent = ''; }
  setAttribute(key, value) { this.attributes[key] = String(value); }
  append(child) { this.children.push(child); }
  replaceChildren() { this.children = []; }
}
const widgets = specs.map(spec => {
  const svg = new Shape('svg'), readout = { textContent: '' }, original = { open: true };
  const inputs = spec.controls.map(([, key, min, max, , value]) => ({
    dataset: { param: key }, min, max, value, nextElementSibling: { textContent: '' },
    addEventListener(event, fn) { this[event] = fn; }
  }));
  const buttons = ['prev', 'next'].map(step => ({
    dataset: { step }, addEventListener(event, fn) { this[event] = fn; }
  }));
  const nodes = { svg, '.social-readout': readout, '.social-original': original,
    '[data-step="prev"]': buttons[0], '[data-step="next"]': buttons[1] };
  const widget = {
    dataset: { widget: spec.kind, steps: JSON.stringify(spec.steps) },
    classList: { ready: false, add(value) { if (value === 'widget-ready') this.ready = true; } },
    querySelector: key => nodes[key],
    querySelectorAll: key => key === 'input[data-param]' ? inputs : key === '[data-step]' ? (spec.steps.length ? buttons : []) : []
  };
  return { widget, svg, readout, original, inputs, buttons, spec };
});
const document = { createElementNS: (_, tag) => new Shape(tag),
  querySelectorAll: key => key === '.social-widget' ? widgets.map(x => x.widget) : [] };
const code = fs.readFileSync(path.join(root, 'assets/social-widgets.js'), 'utf8');
vm.runInNewContext(code, { document, module: { exports: {} }, Intl, console });
for (const entry of widgets) {
  assert.equal(entry.widget.classList.ready, true, entry.spec.kind);
  assert.equal(entry.original.open, false, entry.spec.kind);
  assert.ok(entry.svg.children.length > 0, entry.spec.kind);
  assert.ok(entry.readout.textContent && !/NaN|Infinity/.test(entry.readout.textContent), entry.spec.kind);
  for (const input of entry.inputs) {
    for (const value of [input.min, input.max]) {
      input.value = value;
      input.input();
      assert.ok(entry.svg.children.length > 0, `${entry.spec.kind} at ${value}`);
      assert.ok(!/NaN|Infinity/.test(entry.readout.textContent), `${entry.spec.kind} at ${value}`);
    }
  }
  if (entry.spec.steps.length > 1) {
    entry.buttons[1].click();
    assert.ok(entry.widget.dataset.stepIndex === 1, entry.spec.kind);
  }
}
console.log('PASS: 43 social widgets render at default and slider limits; model formulas');
