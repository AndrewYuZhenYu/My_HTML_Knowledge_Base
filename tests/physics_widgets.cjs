/* Runtime smoke test without browser or network: node tests/physics_widgets.cjs */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

class Node {
  constructor(tag) { this.tag = tag; this.attributes = {}; this.children = []; this.textContent = ''; }
  setAttribute(key, value) { this.attributes[key] = String(value); }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { this.children = nodes; }
}

const cases = [
  ['gas_isotherm', {temperature: 1}],
  ['gas_barometric', {temperature: 300}],
  ['gas_mfp', {temperature: 300}],
  ['thermo_adiabat', {gamma: 1.4}],
  ['thermo_cycle', {dp: 50, dv: 2}],
  ['thermo_carnot', {hot: 600, cold: 300}],
  ['vib_sho', {amplitude: 1, omega: 1, phase: 0}],
  ['vib_resonance', {zeta: 0.15}],
  ['vib_beats', {delta: 0.3}],
  ['vib_lissajous', {phase: 1.57}],
];

const widgets = cases.map(([kind, values]) => {
  const svg = new Node('svg');
  const info = new Node('div');
  const inputs = Object.entries(values).map(([param, value]) => ({
    dataset: {param}, value: String(value), nextElementSibling: new Node('output'),
    addEventListener(event, listener) { this.listener = listener; },
  }));
  const classes = new Set();
  return {
    dataset: {widget: kind}, inputs, svg, info, classes,
    querySelector(selector) { return selector === 'svg' ? svg : info; },
    querySelectorAll() { return inputs; },
    classList: {add(value) { classes.add(value); }},
  };
});

const document = {
  createElementNS(ns, tag) { assert.equal(ns, 'http://www.w3.org/2000/svg'); return new Node(tag); },
  querySelectorAll() { return widgets; },
};
const source = fs.readFileSync(path.join(__dirname, '../assets/physics-widgets.js'), 'utf8');
vm.runInNewContext(source, {document, Math, Number, Object});
for (const widget of widgets) {
  assert(widget.classes.has('widget-ready'), widget.dataset.widget);
  assert(widget.svg.children.length >= 5, widget.dataset.widget);
  assert(widget.info.textContent.length > 4, widget.dataset.widget);
  const before = JSON.stringify([widget.svg.children, widget.info.textContent]);
  const input = widget.inputs[0];
  input.value = String(Number(input.value) + 0.1);
  input.listener();
  const after = JSON.stringify([widget.svg.children, widget.info.textContent]);
  assert.notEqual(after, before, `${widget.dataset.widget} did not respond to input`);
}
console.log('PASS: 10 physics widgets initialize and respond to input');
