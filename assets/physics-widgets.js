/* Inline, offline physics figures. Source equations live beside each figure. */
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const colors = ['var(--viz-blue)', 'var(--viz-orange)', 'var(--viz-green)'];
  const fmt = (n, digits = 2) => Number(n).toFixed(digits).replace(/(\.\d*?)0+$/, '$1').replace(/\.$/, '');
  const el = (tag, attrs = {}) => {
    const node = document.createElementNS(NS, tag);
    for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
    return node;
  };
  const label = (svg, x, y, value, attrs = {}) => {
    const node = el('text', { x, y, fill: 'var(--soft)', 'font-size': 13, ...attrs });
    node.textContent = value;
    svg.append(node);
  };
  const line = (svg, x1, y1, x2, y2, stroke = 'var(--border)', width = 1) =>
    svg.append(el('line', { x1, y1, x2, y2, stroke, 'stroke-width': width }));
  const chart = (svg, bounds, curves, xLabel, yLabel, info) => {
    const [xmin, xmax, ymin, ymax] = bounds;
    const L = 68, R = 710, T = 28, B = 240;
    const X = x => L + (x - xmin) * (R - L) / (xmax - xmin);
    const Y = y => B - (y - ymin) * (B - T) / (ymax - ymin);
    svg.setAttribute('viewBox', '0 0 760 310');
    svg.replaceChildren();
    for (let i = 0; i <= 4; i++) {
      const y = T + i * (B - T) / 4;
      line(svg, L, y, R, y);
      label(svg, L - 8, y + 4, fmt(ymax - i * (ymax - ymin) / 4, 1), { 'text-anchor': 'end', 'font-size': 11 });
    }
    line(svg, L, T, L, B, 'var(--soft)', 1.5);
    line(svg, L, B, R, B, 'var(--soft)', 1.5);
    for (let i = 0; i <= 4; i++) {
      const x = xmin + i * (xmax - xmin) / 4;
      label(svg, X(x), B + 18, fmt(x, 1), { 'text-anchor': 'middle', 'font-size': 11 });
    }
    label(svg, L, 18, yLabel, { 'font-size': 12 });
    label(svg, R, 290, xLabel, { 'text-anchor': 'end', 'font-size': 12 });
    curves.forEach((curve, i) => {
      const points = [];
      for (let k = 0; k <= 640; k++) {
        const x = xmin + (xmax - xmin) * k / 640;
        const y = curve.fn(x);
        if (Number.isFinite(y)) points.push(`${X(x).toFixed(1)},${Y(Math.max(ymin, Math.min(ymax, y))).toFixed(1)}`);
      }
      svg.append(el('polyline', { points: points.join(' '), fill: 'none', stroke: colors[i], 'stroke-width': 2.8, 'stroke-linejoin': 'round' }));
      const lx = L + i * 215;
      line(svg, lx, 269, lx + 26, 269, colors[i], 3);
      label(svg, lx + 32, 273, curve.name, { 'font-size': 12 });
    });
    info.textContent = curves.map(c => c.summary).filter(Boolean).join('　·　');
  };
  const cycle = (svg, p, info) => {
    svg.setAttribute('viewBox', '0 0 760 310');
    svg.replaceChildren();
    const dp = p.dp, dv = p.dv;
    const x1 = 130, x2 = x1 + 95 + dv * 72;
    const y2 = 215, y1 = y2 - 45 - dp * 1.25;
    for (let i = 0; i < 5; i++) line(svg, 85, 35 + i * 45, 700, 35 + i * 45);
    line(svg, 85, 25, 85, 245, 'var(--soft)', 1.5);
    line(svg, 85, 245, 700, 245, 'var(--soft)', 1.5);
    svg.append(el('rect', { x: x1, y: y1, width: x2 - x1, height: y2 - y1, fill: 'var(--viz-blue-bg)', stroke: colors[0], 'stroke-width': 3 }));
    label(svg, (x1 + x2) / 2, y1 - 11, '→ 膨胀', { 'text-anchor': 'middle' });
    label(svg, (x1 + x2) / 2, y2 + 25, '← 压缩', { 'text-anchor': 'middle' });
    label(svg, x1 - 12, (y1 + y2) / 2, `Δp = ${fmt(dp, 0)} kPa`, { 'text-anchor': 'end' });
    label(svg, (x1 + x2) / 2, 285, `ΔV = ${fmt(dv)} L`, { 'text-anchor': 'middle' });
    label(svg, 90, 20, '压强 p');
    label(svg, 700, 265, '体积 V', { 'text-anchor': 'end' });
    info.textContent = `顺时针循环净功 W = ${fmt(dp * dv)} J；矩形仅用于展示 p–V 面积与净功的关系。`;
  };
  const phasePlane = (svg, p, info) => {
    svg.setAttribute('viewBox', '0 0 760 310');
    svg.replaceChildren();
    const cx = 380, cy = 145, rx = 205, ry = 105;
    line(svg, 100, cy, 665, cy, 'var(--soft)', 1.3);
    line(svg, cx, 25, cx, 265, 'var(--soft)', 1.3);
    const points = [];
    for (let k = 0; k <= 320; k++) {
      const t = 2 * Math.PI * k / 320;
      points.push(`${(cx + rx * Math.sin(t)).toFixed(1)},${(cy - ry * Math.sin(t + p.phase)).toFixed(1)}`);
    }
    svg.append(el('polyline', { points: points.join(' '), fill: 'none', stroke: colors[0], 'stroke-width': 3 }));
    label(svg, 665, 138, 'x', { 'text-anchor': 'end' });
    label(svg, cx + 8, 30, 'y');
    info.textContent = `相位差 δ = ${fmt(p.phase)} rad；0 或 π 时成为直线，π/2 时成为圆。`;
  };
  const render = (widget, p) => {
    const svg = widget.querySelector('svg');
    const info = widget.querySelector('.physics-live');
    const kind = widget.dataset.widget;
    if (kind === 'gas_isotherm') {
      chart(svg, [0.6, 3, 0, 3.5], [
        { name: `T/T₀=${fmt(p.temperature, 1)}`, fn: v => p.temperature / v, summary: `V/V₀=1 时 p/p₀=${fmt(p.temperature)}` },
        { name: 'T/T₀=1（对照）', fn: v => 1 / v }
      ], '体积比 V/V₀', '压强比 p/p₀', info);
    } else if (kind === 'gas_barometric') {
      const n = (z, t) => Math.exp(-0.029 * 9.81 * z * 1000 / (8.314 * t));
      chart(svg, [0, 20, 0, 1.05], [
        { name: `${fmt(p.temperature, 0)} K`, fn: z => n(z, p.temperature), summary: `10 km 处 n/n₀=${fmt(n(10, p.temperature), 3)}` },
        { name: '300 K（对照）', fn: z => n(z, 300) }
      ], '高度 z（km）', '相对数密度 n/n₀', info);
    } else if (kind === 'gas_mfp') {
      const lambda = (press, t) => 1.380649e-23 * t / (Math.SQRT2 * Math.PI * (0.37e-9) ** 2 * press * 1000) * 1e9;
      chart(svg, [20, 200, 0, 850], [
        { name: `${fmt(p.temperature, 0)} K`, fn: press => lambda(press, p.temperature), summary: `100 kPa 时 λ=${fmt(lambda(100, p.temperature), 1)} nm` },
        { name: '300 K（对照）', fn: press => lambda(press, 300) }
      ], '压强 p（kPa）', '自由程 λ（nm）', info);
    } else if (kind === 'thermo_adiabat') {
      chart(svg, [0.7, 2.5, 0, 1.9], [
        { name: `绝热 γ=${fmt(p.gamma)}`, fn: v => v ** (-p.gamma), summary: `V/V₀=2 时 p/p₀=${fmt(2 ** (-p.gamma))}` },
        { name: '等温（对照）', fn: v => 1 / v }
      ], '体积比 V/V₀', '压强比 p/p₀', info);
    } else if (kind === 'thermo_cycle') {
      cycle(svg, p, info);
    } else if (kind === 'thermo_carnot') {
      const ratio = p.cold / p.hot;
      chart(svg, [0, 1, 0, 1.05], [
        { name: 'η = 1 − T꜀/Tₕ', fn: r => 1 - r, summary: `当前效率上限 η=${fmt((1 - ratio) * 100, 1)}%` }
      ], '温度比 T꜀/Tₕ', '效率 η', info);
      line(svg, 68 + ratio * 642, 240, 68 + ratio * 642, 240 - (1 - ratio) * 212, colors[1], 2);
      svg.append(el('circle', { cx: 68 + ratio * 642, cy: 240 - (1 - ratio) * 212, r: 6, fill: colors[1] }));
    } else if (kind === 'vib_sho') {
      chart(svg, [0, 4 * Math.PI, -1.6, 1.6], [
        { name: '位移 x(t)', fn: t => p.amplitude * Math.cos(p.omega * t + p.phase), summary: `周期 T=${fmt(2 * Math.PI / p.omega)}（时间单位）` },
        { name: 'A=1, ω=1, φ=0', fn: t => Math.cos(t) }
      ], '时间 t', '位移 x', info);
    } else if (kind === 'vib_resonance') {
      const amp = (r, z) => 1 / Math.sqrt((1 - r * r) ** 2 + (2 * z * r) ** 2);
      chart(svg, [0, 2.5, 0, 11], [
        { name: `ζ=${fmt(p.zeta, 3)}`, fn: r => amp(r, p.zeta), summary: `r=1 时相对振幅=${fmt(amp(1, p.zeta))}` },
        { name: 'ζ=0.3（对照）', fn: r => amp(r, 0.3) }
      ], '频率比 r=ω/ω₀', '相对振幅', info);
    } else if (kind === 'vib_beats') {
      chart(svg, [0, 20, -2.2, 2.2], [
        { name: '合成位移', fn: t => 2 * Math.cos(Math.PI * p.delta * t) * Math.cos(2 * Math.PI * 2 * t), summary: `拍周期 1/Δf=${fmt(1 / p.delta)} s` },
        { name: '上包络', fn: t => 2 * Math.abs(Math.cos(Math.PI * p.delta * t)) }
      ], '时间 t（s）', '相对位移', info);
    } else if (kind === 'vib_lissajous') {
      phasePlane(svg, p, info);
    }
  };
  document.querySelectorAll('.physics-widget').forEach(widget => {
    const inputs = [...widget.querySelectorAll('input[data-param]')];
    const update = () => {
      const params = {};
      inputs.forEach(input => {
        params[input.dataset.param] = Number(input.value);
        input.nextElementSibling.textContent = fmt(input.value, 2);
      });
      render(widget, params);
    };
    inputs.forEach(input => input.addEventListener('input', update));
    update();
    widget.classList.add('widget-ready');
  });
})();
