/* Quantitative interactions for source-linked scientific and algorithm figures. */
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const make = (tag, attrs = {}) => {
    const n = document.createElementNS(NS, tag);
    for (const [key, value] of Object.entries(attrs)) n.setAttribute(key, value);
    return n;
  };
  const append = (svg, tag, attrs = {}) => svg.append(make(tag, attrs));
  const label = (svg, x, y, value, size = 13, anchor = 'middle', color = 'var(--text)') => {
    const n = make('text', {x, y, 'text-anchor': anchor, 'font-size': size, fill: color});
    n.textContent = value;
    svg.append(n);
  };
  const line = (svg, x1, y1, x2, y2, color = 'var(--border)', width = 1.3) => append(svg, 'line', {x1, y1, x2, y2, stroke: color, 'stroke-width': width});
  const poly = (svg, points, color = 'var(--viz-blue)', width = 2.6) => append(svg, 'polyline', {points: points.map(p => p.map(x => x.toFixed(1)).join(',')).join(' '), fill: 'none', stroke: color, 'stroke-width': width});
  const axes = (svg, xLabel, yLabel, xticks = [], yticks = []) => {
    const L = 75, R = 705, T = 34, B = 234;
    yticks.forEach(([y, name]) => {line(svg, L, y, R, y); label(svg, L - 8, y + 4, name, 11, 'end', 'var(--soft)');});
    xticks.forEach(([x, name]) => label(svg, x, B + 21, name, 11, 'middle', 'var(--soft)'));
    line(svg, L, T, L, B, 'var(--soft)'); line(svg, L, B, R, B, 'var(--soft)');
    label(svg, L, 23, yLabel, 12, 'start', 'var(--soft)');
    label(svg, R, B + 49, xLabel, 12, 'end', 'var(--soft)');
  };
  const choose = (n, k) => {
    let result = 1;
    for (let i = 1; i <= k; i++) result = result * (n - i + 1) / i;
    return result;
  };
  const draw = (widget, p) => {
    const kind = widget.dataset.science, svg = widget.querySelector('svg');
    const readout = widget.querySelector('.scientific-readout');
    svg.replaceChildren();
    svg.setAttribute('viewBox', '0 0 760 310');
    if (kind === 'galton') {
      axes(svg, '向右偏转次数 k', '理论概率 P(k)', Array.from({length: 11}, (_, i) => [90 + i * 60, String(i)]), [[234, '0'], [148, '0.15'], [34, '0.35']]);
      for (let k = 0; k <= 10; k++) {
        const probability = choose(10, k) * p.p ** k * (1 - p.p) ** (10 - k);
        const height = probability / .35 * 200;
        append(svg, 'rect', {x: 82 + k * 60, y: 234 - height, width: 25, height, rx: 2, fill: 'var(--viz-blue-bg)', stroke: 'var(--viz-blue)'});
      }
      readout.textContent = `每次向右偏转概率 p=${p.p.toFixed(2)}；10 次偏转后向右 5 次的理论概率为 ${(choose(10, 5) * p.p ** 5 * (1 - p.p) ** 5 * 100).toFixed(1)}%。`;
    } else if (kind === 'maxwell_area') {
      const M = .032, R = 8.314;
      const f = v => 4 * Math.PI * (M / (2 * Math.PI * R * p.T)) ** 1.5 * v * v * Math.exp(-M * v * v / (2 * R * p.T));
      const maxY = Math.max(...Array.from({length: 141}, (_, i) => f(i * 10))) * 1.08;
      const X = v => 75 + v / 1400 * 630, Y = v => 234 - f(v) / maxY * 200;
      axes(svg, '速率 v（m/s）', '概率密度 f(v)', [0, 350, 700, 1050, 1400].map(v => [X(v), String(v)]), [[234, '0'], [134, (maxY / 2).toExponential(1)], [34, maxY.toExponential(1)]]);
      const shaded = [[X(p.lo), 234]];
      for (let v = p.lo; v <= p.hi; v += 5) shaded.push([X(v), Y(v)]);
      shaded.push([X(p.hi), Y(p.hi)], [X(p.hi), 234]);
      append(svg, 'polygon', {points: shaded.map(x => x.map(y => y.toFixed(1)).join(',')).join(' '), fill: 'var(--viz-green-bg)', stroke: 'var(--viz-green)', 'stroke-width': 1.3});
      poly(svg, Array.from({length: 281}, (_, i) => [X(i * 5), Y(i * 5)]));
      let area = 0;
      for (let v = p.lo; v < p.hi; v += 1) area += (f(v) + f(v + 1)) / 2;
      readout.textContent = `氧气 ${p.T} K：P(${p.lo} ≤ v ≤ ${p.hi} m/s) ≈ ${(area * 100).toFixed(1)}%；绿色面积是概率，不是曲线高度。`;
    } else if (kind === 'complexity') {
      const X = n => 75 + n / 20 * 630, Y = v => 234 - Math.log10(1 + v) / Math.log10(401) * 200;
      axes(svg, '输入规模 n', '示意次数（对数轴）', [0, 5, 10, 15, 20].map(n => [X(n), String(n)]), [[234, '0'], [157, '9'], [80, '99'], [34, '400']]);
      const curves = [['O(1)', n => 1, 'var(--viz-green)'], ['O(log n)', n => Math.log2(1 + n), 'var(--viz-orange)'], ['O(n)', n => n, 'var(--viz-blue)'], ['O(n²)', n => n * n, '#b25c67']];
      curves.forEach(([name, fn, color]) => {poly(svg, Array.from({length: 101}, (_, i) => [X(i / 5), Y(fn(i / 5))]), color); label(svg, X(17), Y(fn(17)) - 8, name, 13, 'middle', color);});
      line(svg, X(p.n), 34, X(p.n), 234, 'var(--viz-orange)', 1.5);
      readout.textContent = `n=${p.n}：示意值 O(1)=1，O(log n)≈${Math.log2(1 + p.n).toFixed(1)}，O(n)=${p.n}，O(n²)=${p.n ** 2}。`;
    } else if (kind === 'prefix_bars') {
      const word = 'ABABAC', lengths = [0, 0, 1, 2, 3, 0];
      axes(svg, '前缀长度 i', 'LPS[i]', Array.from({length: 6}, (_, i) => [117 + i * 103, String(i + 1)]), [[234, '0'], [170, '1'], [106, '2'], [42, '3']]);
      lengths.forEach((value, i) => {
        const x = 98 + i * 103, active = i === p.i - 1;
        append(svg, 'rect', {x, y: 234 - value * 64, width: 39, height: value * 64 || 2, fill: active ? 'var(--viz-orange-bg)' : 'var(--viz-green-bg)', stroke: active ? 'var(--viz-orange)' : 'var(--viz-green)', 'stroke-width': active ? 2.5 : 1.5});
        label(svg, x + 20, 219 - value * 64, word[i], 15);
      });
      const prefix = word.slice(0, p.i), border = lengths[p.i - 1] ? prefix.slice(0, lengths[p.i - 1]) : '无';
      readout.textContent = `前缀 ${prefix}：最长相等真前后缀为 ${border}，长度 ${lengths[p.i - 1]}。这是 LPS 长度，不等同于教材 next 数组的具体下标。`;
    } else if (kind === 'strides') {
      const values = [['a₀₀', 'a₀₁', 'a₀₂'], ['a₁₀', 'a₁₁', 'a₁₂']];
      values.forEach((row, i) => row.forEach((value, j) => {
        const active = i === p.i && j === p.j;
        append(svg, 'rect', {x: 75 + j * 76, y: 45 + i * 58, width: 68, height: 50, rx: 2, fill: active ? 'var(--viz-orange-bg)' : 'var(--viz-blue-bg)', stroke: active ? 'var(--viz-orange)' : 'var(--viz-blue)', 'stroke-width': active ? 2.5 : 1.5});
        label(svg, 109 + j * 76, 77 + i * 58, value, 16);
      }));
      label(svg, 185, 198, '逻辑矩阵 2×3', 16);
      const orders = [['行优先', ['00', '01', '02', '10', '11', '12'], p.i * 3 + p.j, 45], ['列优先', ['00', '10', '01', '11', '02', '12'], p.j * 2 + p.i, 145]];
      orders.forEach(([name, cells, selected, y]) => {
        label(svg, 416, y - 9, name, 13, 'start', 'var(--soft)');
        cells.forEach((value, k) => {
          const active = k === selected;
          append(svg, 'rect', {x: 417 + k * 49, y, width: 44, height: 41, rx: 2, fill: active ? 'var(--viz-orange-bg)' : 'var(--viz-green-bg)', stroke: active ? 'var(--viz-orange)' : 'var(--viz-green)', 'stroke-width': active ? 2.5 : 1.5});
          label(svg, 439 + k * 49, y + 27, value, 12);
        });
      });
      readout.textContent = `a[${p.i}][${p.j}]：行优先偏移 ${p.i}×3+${p.j}=${p.i * 3 + p.j}；列优先偏移 ${p.j}×2+${p.i}=${p.j * 2 + p.i}。`;
    } else if (kind === 'kmap_true' || kind === 'kmap_false') {
      label(svg, 237, 42, 'Q=0', 14); label(svg, 391, 42, 'Q=1', 14);
      for (let i = 0; i < 2; i++) {
        label(svg, 90, 110 + i * 92, `P=${i}`, 14);
        for (let j = 0; j < 2; j++) {
          const active = i === p.p && j === p.q, selected = kind === 'kmap_true' ? i !== j : i === j;
          const x = 160 + j * 154, y = 60 + i * 92;
          append(svg, 'rect', {x, y, width: 145, height: 82, rx: 3, fill: selected ? 'var(--viz-green-bg)' : 'var(--paper)', stroke: active ? 'var(--viz-orange)' : selected ? 'var(--viz-green)' : 'var(--border)', 'stroke-width': active ? 3 : 1.5});
          label(svg, x + 72, y + 33, `${i}${j}`, 15);
          label(svg, x + 72, y + 62, `${kind === 'kmap_true' ? 'm' : 'M'}${2 * i + j}`, 17, 'middle', selected ? 'var(--viz-green)' : 'var(--soft)');
        }
      }
      const f = p.p !== p.q ? 1 : 0, include = kind === 'kmap_true' ? f === 1 : f === 0;
      readout.textContent = `赋值 P=${p.p}、Q=${p.q} 时，P⊕Q=${f}；格 ${p.p}${p.q} ${include ? '进入' : '不进入'}${kind === 'kmap_true' ? '主析取范式的极小项集合' : '主合取范式的极大项集合'}。`;
    }
  };
  document.querySelectorAll('.scientific-widget').forEach(widget => {
    try {
      const inputs = [...widget.querySelectorAll('input[data-parameter]')];
      const update = () => {
        const params = {};
        inputs.forEach(input => {params[input.dataset.parameter] = Number(input.value); input.nextElementSibling.textContent = input.value;});
        draw(widget, params);
      };
      inputs.forEach(input => input.addEventListener('input', update));
      update();
      widget.classList.add('scientific-ready');
    } catch (error) {
      console.error('scientific widget:', error);
    }
  });
})();
