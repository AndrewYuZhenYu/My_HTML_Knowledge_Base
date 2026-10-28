/* Check both clipboard paths without requiring a browser or network. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

const source = fs.readFileSync(path.join(__dirname, '..', 'assets', 'code-copy.js'), 'utf8');
const codeText = '    int value = 42;\n    return value;\n';

async function check(useModern) {
  let handler, copied, legacyCalls = 0;
  const label = {textContent: '复制代码'};
  const classes = {toggle() {}, remove() {}};
  const code = {textContent: codeText};
  const panel = {querySelector(selector) {assert.equal(selector, 'pre code'); return code;}};
  const button = {
    closest(selector) {assert.equal(selector, '.code-panel'); return panel;},
    querySelector(selector) {assert.equal(selector, '.code-copy-label'); return label;},
    setAttribute(name, value) {if (name === 'aria-label') this.ariaLabel = value;},
    classList: classes,
  };
  const field = {
    style: {},
    setAttribute() {},
    select() {},
    remove() {},
  };
  const document = {
    addEventListener(type, fn) {assert.equal(type, 'click'); handler = fn;},
    createElement(type) {assert.equal(type, 'textarea'); return field;},
    body: {append(node) {assert.equal(node, field);}},
    execCommand(command) {assert.equal(command, 'copy'); legacyCalls++; copied = field.value; return true;},
  };
  const navigator = {clipboard: useModern ? {async writeText(value) {copied = value;}} : undefined};
  vm.runInNewContext(source, {document, navigator, setTimeout() {return 1;}, clearTimeout() {}, window: {}});
  await handler({target: {closest(selector) {assert.equal(selector, '[data-copy-code]'); return button;}}});
  assert.equal(copied, codeText);
  assert.equal(label.textContent, '已复制');
  assert.equal(button.ariaLabel, '已复制');
  assert.equal(legacyCalls, useModern ? 0 : 1);
}

Promise.all([check(true), check(false)]).then(() => {
  console.log('PASS: code copy preserves indentation with Clipboard API and local-file fallback');
}).catch(error => {console.error(error); process.exitCode = 1;});
