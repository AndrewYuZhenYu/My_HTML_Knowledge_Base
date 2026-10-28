/* Exercise scientific controls and trace stepping without browser access. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

class Node {
  constructor() { this.children = []; this.attributes = {}; this.textContent = ''; }
  setAttribute(k, v) { this.attributes[k] = String(v); }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { this.children = nodes; }
  addEventListener(_, fn) { this.listener = fn; }
}
const ready = new Set();
const configs = [
  ['galton', {p: .5}], ['maxwell_area', {T: 300, lo: 300, hi: 600}],
  ['complexity', {n: 10}], ['prefix_bars', {i: 3}],
  ['strides', {i: 0, j: 1}], ['kmap_true', {p: 0, q: 1}], ['kmap_false', {p: 0, q: 0}],
];
const widgets = configs.map(([kind, values]) => {
  const svg = new Node(), info = new Node();
  const inputs = Object.entries(values).map(([name, value]) => Object.assign(new Node(), {dataset: {parameter: name}, value: String(value), nextElementSibling: new Node()}));
  return {dataset: {science: kind}, svg, info, inputs,
    querySelector(s) { return s === 'svg' ? svg : info; }, querySelectorAll() { return inputs; },
    classList: {add(c) {ready.add(`${kind}:${c}`);}}};
});
const errors = [];
const document = {querySelectorAll() {return widgets;}, createElementNS(ns) {assert.equal(ns, 'http://www.w3.org/2000/svg'); return new Node();}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../assets/concept-interactions.js'), 'utf8'), {document, console: {error: (...args) => errors.push(args)}, Math, Number, Object});
assert.equal(errors.length, 0, 'scientific initialization');
for (const widget of widgets) {
  assert(ready.has(`${widget.dataset.science}:scientific-ready`));
  assert(widget.svg.children.length > 5);
  assert(widget.info.textContent.length > 5);
  const before = widget.info.textContent;
  widget.inputs[0].value = String(Number(widget.inputs[0].value) + (widget.dataset.science === 'maxwell_area' ? 25 : widget.dataset.science === 'galton' ? .05 : 1));
  widget.inputs[0].listener();
  assert.notEqual(widget.info.textContent, before, widget.dataset.science);
}
const traceSvg = new Node(), traceInfo = new Node(), progress = new Node(), prev = new Node(), next = new Node();
const trace = {dataset: {rows: JSON.stringify([['初始', ['A','B','·']], ['插入', ['A','X','B']]])},
  querySelector(s) {return ({svg: traceSvg, '.trace-explanation': traceInfo, '.trace-progress': progress, '[data-step="prev"]': prev, '[data-step="next"]': next})[s];},
  classList: {add(c) {ready.add(c);}}};
const traceDocument = {querySelectorAll() {return [trace];}, createElementNS() {return new Node();}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../assets/trace-widgets.js'), 'utf8'), {document: traceDocument, console: {error: (...args) => errors.push(args)}, JSON, Object});
assert.equal(errors.length, 0, 'trace initialization');
assert(ready.has('trace-ready'));
const before = traceInfo.textContent;
next.listener();
assert.notEqual(traceInfo.textContent, before);
assert.equal(next.disabled, true);
console.log('PASS: 7 scientific modes and trace stepping initialize and react to input');
