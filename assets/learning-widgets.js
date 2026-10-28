/* Offline step-by-step data-structure and logic explorers. */
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const make = (tag, attrs = {}) => {
    const node = document.createElementNS(NS, tag);
    for (const [name, value] of Object.entries(attrs)) node.setAttribute(name, value);
    return node;
  };
  const addText = (svg, x, y, content, size = 15, anchor = 'middle', color = 'var(--text)') => {
    const node = make('text', {x, y, 'text-anchor': anchor, 'font-size': size, fill: color});
    node.textContent = content;
    svg.append(node);
  };
  const cell = (svg, x, y, width, height, content, tone = 'plain', font = 16) => {
    const fill = tone === 'active' ? 'var(--viz-green-bg)' : tone === 'error' ? 'var(--accent-bg)' : 'var(--viz-blue-bg)';
    const stroke = tone === 'active' ? 'var(--viz-green)' : tone === 'error' ? 'var(--viz-orange)' : 'var(--viz-blue)';
    svg.append(make('rect', {x, y, width, height, rx: 7, fill, stroke, 'stroke-width': 1.5}));
    addText(svg, x + width / 2, y + height / 2 + 6, content, font);
  };
  const drawStep = (widget, states, index) => {
    const step = states[index], svg = widget.querySelector('svg');
    const status = widget.querySelector('.learning-status');
    const mode = widget.dataset.mode;
    svg.setAttribute('viewBox', '0 0 760 225');
    svg.replaceChildren();
    addText(svg, 380, 39, step.label, 20);
    if (mode === 'match') {
      const main = 'ABABC', pattern = 'ABC', shift = step.shift;
      addText(svg, 120, 99, '主串', 14, 'end', 'var(--soft)');
      addText(svg, 120, 167, '模式', 14, 'end', 'var(--soft)');
      let failing = false;
      for (let j = 0; j < main.length; j++) cell(svg, 145 + j * 101, 67, 86, 45, main[j]);
      for (let j = 0; j < pattern.length; j++) {
        const equal = main[shift + j] === pattern[j];
        const tone = failing ? 'plain' : equal ? 'active' : 'error';
        cell(svg, 145 + (shift + j) * 101, 135, 86, 45, pattern[j], tone);
        if (!equal) failing = true;
      }
    } else {
      const values = step.cells;
      const width = mode === 'triples' ? 174 : 96;
      const gap = mode === 'triples' ? 18 : 21;
      const start = (760 - values.length * width - (values.length - 1) * gap) / 2;
      values.forEach((value, j) => cell(svg, start + j * (width + gap), 88, width, 59, value, value === '·' ? 'plain' : 'active', mode === 'triples' ? 15 : 19));
      if (mode === 'queue') {
        addText(svg, start + step.front * (width + gap) + width / 2, 178, 'front', 13, 'middle', 'var(--viz-blue)');
        addText(svg, start + step.rear * (width + gap) + width / 2, 199, 'rear', 13, 'middle', 'var(--viz-orange)');
      }
    }
    widget.querySelector('.learning-progress').textContent = `${index + 1} / ${states.length}`;
    widget.querySelector('[data-action="prev"]').disabled = index === 0;
    widget.querySelector('[data-action="next"]').disabled = index === states.length - 1;
    status.textContent = step.detail;
  };
  const drawTruth = (widget, rows, columns) => {
    const inputs = [...widget.querySelectorAll('input[data-var]')];
    const bits = inputs.map(input => input.checked ? '1' : '0');
    const selected = rows.findIndex(row => bits.every((bit, i) => row[i] === bit));
    const svg = widget.querySelector('svg');
    const cw = Math.min(132, 692 / columns.length), total = columns.length * cw;
    const start = (760 - total) / 2, height = 45 + (rows.length + 1) * 35;
    svg.setAttribute('viewBox', `0 0 760 ${height}`);
    svg.replaceChildren();
    columns.forEach((title, j) => {
      svg.append(make('rect', {x: start + j * cw, y: 24, width: cw, height: 35, fill: 'var(--viz-blue-bg)', stroke: 'var(--border)'}));
      addText(svg, start + (j + .5) * cw, 47, title, title.length > 12 ? 10 : 13);
    });
    rows.forEach((row, i) => row.forEach((value, j) => {
      const y = 59 + i * 35;
      svg.append(make('rect', {x: start + j * cw, y, width: cw, height: 35, fill: i === selected ? 'var(--viz-green-bg)' : 'var(--paper)', stroke: 'var(--border)'}));
      addText(svg, start + (j + .5) * cw, y + 24, value, 14);
    }));
    inputs.forEach((input, i) => { input.nextElementSibling.textContent = bits[i]; });
    widget.querySelector('.learning-status').textContent = `当前赋值 ${bits.map((b, i) => `${inputs[i].dataset.var}=${b}`).join('，')}；结果：${columns.slice(bits.length).map((name, j) => `${name}=${rows[selected][bits.length + j]}`).join('，')}`;
  };
  document.querySelectorAll('.learning-widget').forEach(widget => {
    try {
      if (widget.dataset.kind === 'stepper') {
        const states = JSON.parse(widget.dataset.states);
        let index = 0;
        widget.querySelector('[data-action="prev"]').addEventListener('click', () => drawStep(widget, states, --index));
        widget.querySelector('[data-action="next"]').addEventListener('click', () => drawStep(widget, states, ++index));
        drawStep(widget, states, index);
      } else {
        const rows = JSON.parse(widget.dataset.rows), columns = JSON.parse(widget.dataset.columns);
        widget.querySelectorAll('input[data-var]').forEach(input => input.addEventListener('change', () => drawTruth(widget, rows, columns)));
        drawTruth(widget, rows, columns);
      }
      widget.classList.add('widget-ready');
    } catch (error) {
      /* Keep the source-aligned static SVG if an individual widget cannot initialize. */
      console.error('learning widget:', error);
    }
  });
})();
