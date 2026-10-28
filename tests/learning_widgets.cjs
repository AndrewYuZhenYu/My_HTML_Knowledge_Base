/* Runtime interaction smoke test: node tests/learning_widgets.cjs */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

class Node {
  constructor() { this.children = []; this.attributes = {}; this.textContent = ''; }
  setAttribute(key, value) { this.attributes[key] = String(value); }
  append(...items) { this.children.push(...items); }
  replaceChildren(...items) { this.children = items; }
  addEventListener(name, listener) { this.listener = listener; }
}

function stepper(mode, states) {
  const svg = new Node(), status = new Node(), progress = new Node();
  const prev = new Node(), next = new Node(), classes = new Set();
  const nodes = {'svg': svg, '.learning-status': status, '.learning-progress': progress, '[data-action="prev"]': prev, '[data-action="next"]': next};
  return {dataset: {kind: 'stepper', mode, states: JSON.stringify(states)}, svg, status, prev, next, classes,
    querySelector(key) { return nodes[key]; }, querySelectorAll() { return []; }, classList: {add(c) { classes.add(c); }}};
}

function truth(vars) {
  const svg = new Node(), status = new Node(), classes = new Set();
  const inputs = vars.map(name => Object.assign(new Node(), {dataset: {var: name}, checked: false, nextElementSibling: new Node()}));
  const rows = Array.from({length: 2 ** vars.length}, (_, i) => [...i.toString(2).padStart(vars.length, '0'), String(i % 2)]);
  return {dataset: {kind: 'truth', rows: JSON.stringify(rows), columns: JSON.stringify([...vars, 'F'])}, svg, status, inputs, classes,
    querySelector(key) { return key === 'svg' ? svg : status; }, querySelectorAll() { return inputs; }, classList: {add(c) { classes.add(c); }}};
}

const widgets = [
  stepper('slots', [{label: '前', cells: ['A','B','·'], detail: '前态'}, {label: '后', cells: ['A','X','B'], detail: '后态'}]),
  stepper('queue', [{label: '前', cells: ['A','·','·'], front: 0, rear: 1, detail: '前态'}, {label: '后', cells: ['A','B','·'], front: 0, rear: 2, detail: '后态'}]),
  stepper('match', [{label: '前', shift: 0, detail: '失配'}, {label: '后', shift: 2, detail: '匹配'}]),
  stepper('triples', [{label: '前', cells: ['(0,1,5)','(1,2,3)','(2,0,7)'], detail: '原矩阵'}, {label: '后', cells: ['(0,2,7)','(1,0,5)','(2,1,3)'], detail: '转置'}]),
  truth(['P','Q']), truth(['P','Q','R'])
];
const errors = [];
const document = {querySelectorAll() { return widgets; }, createElementNS(ns) { assert.equal(ns, 'http://www.w3.org/2000/svg'); return new Node(); }};
const source = fs.readFileSync(path.join(__dirname, '../assets/learning-widgets.js'), 'utf8');
vm.runInNewContext(source, {document, JSON, Object, console: {error: (...args) => errors.push(args)}});
assert.equal(errors.length, 0, 'widget initialization error');
for (const widget of widgets) {
  assert(widget.classes.has('widget-ready'));
  assert(widget.svg.children.length > 0);
  assert(widget.status.textContent.length > 0);
  const before = widget.status.textContent;
  if (widget.dataset.kind === 'stepper') widget.next.listener();
  else { widget.inputs[0].checked = true; widget.inputs[0].listener(); }
  assert.notEqual(widget.status.textContent, before);
}
console.log('PASS: 4 algorithm modes and 2/3-variable truth tables respond to controls');
