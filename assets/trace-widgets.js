/* Step through source-linked memory states. Static multi-row SVG remains as fallback. */
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const node = (tag, attrs = {}) => {
    const el = document.createElementNS(NS, tag);
    for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, value);
    return el;
  };
  const text = (svg, x, y, value, size = 14, color = 'var(--text)') => {
    const el = node('text', {x, y, 'text-anchor': 'middle', 'font-size': size, fill: color});
    el.textContent = value;
    svg.append(el);
  };
  document.querySelectorAll('.trace-widget').forEach(widget => {
    try {
      const rows = JSON.parse(widget.dataset.rows);
      let position = 0;
      const svg = widget.querySelector('svg');
      const previous = widget.querySelector('[data-step="prev"]');
      const next = widget.querySelector('[data-step="next"]');
      const render = () => {
        const [caption, cells] = rows[position];
        const old = position > 0 ? rows[position - 1][1] : [];
        const width = Math.min(96, (650 - 12 * (cells.length - 1)) / cells.length);
        const gap = 12, start = (760 - cells.length * width - (cells.length - 1) * gap) / 2;
        svg.setAttribute('viewBox', '0 0 760 207');
        svg.replaceChildren();
        text(svg, 380, 37, caption, 19);
        cells.forEach((raw, index) => {
          const value = String(raw).replace(/^\*/, '');
          const changed = String(old[index] ?? '').replace(/^\*/, '') !== value;
          const active = changed || String(raw).startsWith('*');
          const x = start + index * (width + gap);
          svg.append(node('rect', {x, y: 78, width, height: 62, rx: 5,
            fill: active ? 'var(--viz-green-bg)' : 'var(--viz-blue-bg)',
            stroke: active ? 'var(--viz-green)' : 'var(--viz-blue)', 'stroke-width': 1.8}));
          text(svg, x + width / 2, 116, value, cells.length > 6 ? 13 : 16);
          text(svg, x + width / 2, 166, String(index), 11, 'var(--soft)');
        });
        text(svg, 380, 191, '下标从 0 开始；绿色表示本步变化或所关注的单元', 12, 'var(--soft)');
        widget.querySelector('.trace-progress').textContent = `${position + 1} / ${rows.length}`;
        widget.querySelector('.trace-explanation').textContent = `${caption}：${cells.map(x => String(x).replace(/^\*/, '')).join(' · ')}`;
        previous.disabled = position === 0;
        next.disabled = position === rows.length - 1;
      };
      previous.addEventListener('click', () => {if (position > 0) {position--; render();}});
      next.addEventListener('click', () => {if (position < rows.length - 1) {position++; render();}});
      render();
      widget.classList.add('trace-ready');
    } catch (error) {
      console.error('trace widget:', error);
    }
  });
})();
