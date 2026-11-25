/* Selectable, copyable investment figures. All values are local teaching data. */
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const prices = [12.10,12.04,11.90,12.16,12.27,12.19,12.45,12.53,12.37,12.66,12.58,12.75,12.85,12.62,12.49,12.64,12.50,12.61,12.60];
  const average = [12.10,12.07,12.00,12.02,12.08,12.09,12.16,12.22,12.23,12.28,12.33,12.40,12.43,12.44,12.44,12.45,12.45,12.46,12.47];
  const volume = [19,14,26,12,20,18,29,24,12,23,34,48,21,17,13,20,10,15,16];
  const node = (tag, attrs = {}, label) => {
    const element = document.createElementNS(NS, tag);
    for (const [key, value] of Object.entries(attrs)) element.setAttribute(key, String(value));
    if (label !== undefined) element.textContent = String(label);
    return element;
  };
  const append = (svg, tag, attrs, label) => svg.appendChild(node(tag, attrs, label));
  const text = (svg, x, y, label, options = {}) => append(svg, 'text', { x, y, fill: 'var(--text)', 'font-size': 13, ...options }, label);
  const line = (svg, x1, y1, x2, y2, color = 'var(--border)', width = 1) =>
    append(svg, 'line', { x1, y1, x2, y2, stroke: color, 'stroke-width': width });
  const clear = svg => { svg.replaceChildren(); svg.setAttribute('viewBox', '0 0 760 310'); };

  function quote(svg, index) {
    clear(svg);
    const x = i => 65 + i * 35.2, y = p => 212 - (p - 11.8) * 190;
    [12.0,12.2,12.4,12.6,12.8].forEach(value => {
      line(svg, 65, y(value), 715, y(value), value === 12 ? '#a7773a' : 'var(--border)', value === 12 ? 1.8 : 1);
      text(svg, 58, y(value) + 4, value.toFixed(1), { 'text-anchor': 'end', fill: 'var(--soft)', 'font-size': 11 });
    });
    const series = (values, color) => append(svg, 'polyline', {
      points: values.slice(0,index + 1).map((value,i) => `${x(i).toFixed(1)},${y(value).toFixed(1)}`).join(' '),
      fill: 'none', stroke: color, 'stroke-width': 3, 'stroke-linecap': 'round', 'stroke-linejoin': 'round'
    });
    series(prices, 'var(--viz-blue)'); series(average, 'var(--viz-orange)');
    volume.forEach((value,i) => append(svg, 'rect', { x: x(i) - 8, y: 284 - value, width: 16, height: value,
      fill: i <= index ? (prices[i] >= (prices[i - 1] ?? prices[i]) ? '#bd4e57' : '#218f83') : 'var(--border)' }));
    line(svg, x(index), 28, x(index), 215, 'var(--accent)', 1.5);
    append(svg, 'circle', { cx: x(index), cy: y(prices[index]), r: 5, fill: 'var(--viz-blue)' });
    text(svg, 66, 22, `第 ${index + 1} / ${prices.length} 个示意时点 · 价格 ${prices[index].toFixed(2)} · 均价 ${average[index].toFixed(2)}`,
      { fill: 'var(--accent)', 'font-size': 14, 'font-weight': 700 });
    text(svg, 712, 306, '虚构分时序列 · 量柱为相对量', { fill: 'var(--soft)', 'text-anchor': 'end', 'font-size': 11 });
  }

  function snapshot(svg) {
    clear(svg);
    const min = 35, max = 39, x = p => 90 + (p - min) / (max - min) * 600;
    [35,36,37,38,39].forEach(value => {
      line(svg, x(value), 75, x(value), 235);
      text(svg, x(value), 252, value.toFixed(0), { 'text-anchor': 'middle', fill: 'var(--soft)', 'font-size': 12 });
    });
    text(svg, 90, 44, '截图读数的价格区间（无逐笔轨迹）', { 'font-size': 15, 'font-weight': 700 });
    const points = [['昨收',35.05,95],['最低',36.80,135],['开盘',37.43,175],['均价',38.02,215],['最新 / 最高',38.56,95]];
    points.forEach(([label,value,y],i) => {
      append(svg,'circle',{cx:x(value),cy:y,r:6,fill:i===4?'#bd4e57':'var(--viz-blue)'});
      text(svg,x(value)+8,y-7,`${label} ${value.toFixed(2)}`,{'font-size':12});
    });
    line(svg,x(36.8),275,x(38.56),275,'var(--viz-orange)',4);
    text(svg,390,302,'当日可见最低价至最高价',{'text-anchor':'middle','font-size':12,fill:'var(--soft)'});
  }

  function daily(svg) {
    clear(svg);
    const min = 19, max = 40, x = p => 95 + (p - min) / (max - min) * 585;
    [20,25,30,35,40].forEach(value => {
      line(svg,x(value),52,x(value),256);
      text(svg,x(value),278,value,{'text-anchor':'middle','font-size':11,fill:'var(--soft)'});
    });
    text(svg,95,30,'截面价格与均线比较；不推测历史逐日 K 线',{'font-size':14,'font-weight':700});
    [['图示低点',19.32],['MA30',25.22],['MA20',27.56],['MA10',30.76],['MA5',33.13],['截图最新',38.56]]
      .forEach(([label,value],i) => {
        const y=67+i*34;
        line(svg,95,y,x(value),y,i===5?'#bd4e57':'var(--viz-blue)',4);
        append(svg,'circle',{cx:x(value),cy:y,r:5,fill:i===5?'#bd4e57':'var(--viz-blue)'});
        text(svg,8,y+4,label,{'font-size':12});
        text(svg,Math.min(690,x(value)+8),y+4,value.toFixed(2),{'font-size':12});
      });
  }

  async function copy(value, button) {
    try {
      let copied = false;
      if (navigator.clipboard?.writeText) {
        try { await navigator.clipboard.writeText(value); copied = true; }
        catch (_) { /* Local file permissions may deny Clipboard API. */ }
      }
      if (!copied) {
        const field = document.createElement('textarea');
        field.value = value; field.style.position = 'fixed'; field.style.opacity = '0';
        document.body.appendChild(field); field.select();
        copied = document.execCommand('copy');
        field.remove();
        if (!copied) throw new Error('copy failed');
      }
      const old = button.textContent; button.textContent = '已复制';
      setTimeout(() => { button.textContent = old; }, 1800);
    } catch (_) { button.textContent = '请选中文字复制'; }
  }

  document.querySelectorAll('.invest-native').forEach(figure => {
    const svg = figure.querySelector('.invest-panel-chart');
    if (svg) {
      const type = figure.dataset.investPanel;
      if (type === 'quote') {
        const input = figure.querySelector('[data-invest-time]');
        const update = () => {
          const index = Number(input.value);
          quote(svg,index);
          input.nextElementSibling.textContent = `${index + 1} / ${prices.length}`;
        };
        input.addEventListener('input',update); update();
      } else if (type === 'time') snapshot(svg);
      else if (type === 'daily') daily(svg);
    }
    const button = figure.querySelector('[data-invest-copy]');
    if (!button) return;
    button.addEventListener('click', () => {
      const kind = button.dataset.investCopy;
      let value;
      if (kind === 'table') value = [...figure.querySelectorAll('table tr')]
        .map(row => [...row.querySelectorAll('th,td')].map(cell => cell.textContent.trim()).join('\t')).join('\n');
      else if (kind === 'stats') value = [...figure.querySelectorAll('.invest-stat')]
        .map(item => `${item.querySelector('dt').textContent}\t${item.querySelector('dd').textContent}`).join('\n');
      else value = [...figure.querySelectorAll('svg text')].map(item => item.textContent.trim()).filter(Boolean).join('\n');
      copy(value,button);
    });
  });
})();
