/* Offline, source-aligned scientific and structural redraws. No external data. */
(() => {
  const math = {
    compound: (principal, rate, years) => principal * (1 + rate) ** years,
    bondPrice: (couponRate, years, yieldRate, face = 100) => {
      let value = face / (1 + yieldRate) ** years;
      for (let year = 1; year <= years; year++) value += face * couponRate / (1 + yieldRate) ** year;
      return value;
    },
    dhondt: (votes, seats) => {
      const result = votes.map(() => 0), order = [];
      for (let n = 0; n < seats; n++) {
        let winner = 0;
        for (let i = 1; i < votes.length; i++)
          if (votes[i] / (result[i] + 1) > votes[winner] / (result[winner] + 1)) winner = i;
        order.push({ party: winner, quotient: votes[winner] / (result[winner] + 1) });
        result[winner]++;
      }
      return { seats: result, order };
    },
    bayes: (prevalence, sensitivity, specificity) => {
      const tp = prevalence * sensitivity, fp = (1 - prevalence) * (1 - specificity);
      return { tp, fp, ppv: tp + fp ? tp / (tp + fp) : 0 };
    },
    eoq: (demand, order, holding) => Math.sqrt(2 * demand * order / holding),
    npv: (initial, cashflow, rate, years) => {
      let value = -initial;
      for (let year = 1; year <= years; year++) value += cashflow / (1 + rate) ** year;
      return value;
    },
    breakEven: (price, variable, fixed) => price > variable ? fixed / (price - variable) : Infinity,
    portfolioRisk: (weight, rho, a = 0.25, b = 0.12) =>
      Math.sqrt((weight * a) ** 2 + ((1 - weight) * b) ** 2 + 2 * weight * (1 - weight) * rho * a * b),
    winrate: (ratio, cost) => (1 + cost) / (1 + ratio)
  };
  if (typeof module !== 'undefined') module.exports = math;
  if (typeof document === 'undefined') return;

  const NS = 'http://www.w3.org/2000/svg';
  const ink = 'var(--text)', muted = 'var(--soft)', grid = 'var(--border)';
  const blue = 'var(--viz-blue)', orange = 'var(--viz-orange)', green = 'var(--viz-green)';
  const purple = '#8a6ec2', red = '#cf6970';
  const colors = [blue, orange, green, purple, red];
  const fmt = (x, digits = 2) => new Intl.NumberFormat('zh-CN', { maximumFractionDigits: digits }).format(x);
  const betweenPoints = (values, x) => {
    const left = Math.min(values.length - 1, Math.max(0, Math.floor(x)));
    const right = Math.min(values.length - 1, left + 1);
    return values[left] + (values[right] - values[left]) * Math.max(0, Math.min(1, x - left));
  };
  const el = (tag, attrs = {}, value = null) => {
    const n = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([k, v]) => n.setAttribute(k, String(v)));
    if (value !== null) n.textContent = value;
    return n;
  };
  const add = (svg, tag, attrs, value = null) => svg.append(el(tag, attrs, value));
  const line = (svg, x1, y1, x2, y2, stroke = grid, width = 1, dash = '') =>
    add(svg, 'line', { x1, y1, x2, y2, stroke, 'stroke-width': width, ...(dash ? { 'stroke-dasharray': dash } : {}) });
  const label = (svg, x, y, value, options = {}) =>
    add(svg, 'text', { x, y, fill: ink, 'font-size': 13, ...options }, String(value));
  const reset = svg => { svg.setAttribute('viewBox', '0 0 760 330'); svg.replaceChildren(); };
  const display = (widget, value) => { widget.querySelector('.social-readout').textContent = value; };

  function plot(svg, bounds, series, xName, yName, markers = []) {
    reset(svg);
    const [xmin, xmax, ymin, ymax] = bounds, L = 68, R = 715, T = 28, B = 268;
    const X = x => L + (x - xmin) * (R - L) / (xmax - xmin);
    const Y = y => B - (y - ymin) * (B - T) / (ymax - ymin);
    for (let i = 0; i <= 4; i++) {
      const y = T + (B - T) * i / 4;
      line(svg, L, y, R, y);
      label(svg, L - 8, y + 4, fmt(ymax - (ymax - ymin) * i / 4, 1), { 'text-anchor': 'end', 'font-size': 11, fill: muted });
      const x = xmin + (xmax - xmin) * i / 4;
      label(svg, X(x), B + 19, fmt(x, 1), { 'text-anchor': 'middle', 'font-size': 11, fill: muted });
    }
    line(svg, L, T, L, B, muted, 1.4); line(svg, L, B, R, B, muted, 1.4);
    label(svg, L, 17, yName, { 'font-size': 12 });
    label(svg, R, 316, xName, { 'text-anchor': 'end', 'font-size': 12 });
    series.forEach((s, index) => {
      const points = [];
      const count = s.samples || 160;
      for (let i = 0; i <= count; i++) {
        const x = xmin + (xmax - xmin) * i / count, y = s.fn(x);
        if (Number.isFinite(y)) points.push(`${X(x).toFixed(1)},${Y(Math.max(ymin, Math.min(ymax, y))).toFixed(1)}`);
      }
      add(svg, 'polyline', { points: points.join(' '), fill: 'none', stroke: s.color || colors[index % colors.length],
        'stroke-width': 3, 'stroke-linecap': 'round', 'stroke-linejoin': 'round',
        ...(s.dash ? { 'stroke-dasharray': '7 5' } : {}) });
      const lx = L + index * 180;
      line(svg, lx, 302, lx + 23, 302, s.color || colors[index % colors.length], 3);
      label(svg, lx + 29, 306, s.name, { 'font-size': 11 });
    });
    markers.forEach(m => {
      if (m.x < xmin || m.x > xmax || m.y < ymin || m.y > ymax) return;
      add(svg, 'circle', { cx: X(m.x), cy: Y(m.y), r: 6, fill: m.color || red, stroke: 'white', 'stroke-width': 2 });
      label(svg, X(m.x) + 9, Y(m.y) - 8, m.name || '', { 'font-size': 11, fill: m.color || red });
    });
  }

  function bars(svg, entries, maximum = null, suffix = '') {
    reset(svg);
    const L = 88, B = 265, top = 35, max = maximum || Math.max(1, ...entries.map(e => e.value)) * 1.18;
    for (let i = 0; i <= 4; i++) {
      const y = B - (B - top) * i / 4;
      line(svg, L, y, 710, y);
      label(svg, L - 9, y + 4, `${fmt(max * i / 4, 1)}${suffix}`, { 'text-anchor': 'end', fill: muted, 'font-size': 11 });
    }
    const width = 590 / entries.length;
    entries.forEach((e, i) => {
      const height = Math.max(0, Math.min(B - top, e.value / max * (B - top)));
      const x = L + width * i + width * 0.17;
      add(svg, 'rect', { x, y: B - height, width: width * 0.66, height, rx: 5, fill: e.color || colors[i % colors.length] });
      label(svg, x + width * 0.33, B - height - 9, `${fmt(e.value, 1)}${suffix}`, { 'text-anchor': 'middle', 'font-size': 12 });
      label(svg, x + width * 0.33, B + 25, e.name, { 'text-anchor': 'middle', 'font-size': 12 });
    });
  }

  function steps(widget, svg) {
    const items = JSON.parse(widget.dataset.steps);
    const index = Number(widget.dataset.stepIndex || 0);
    reset(svg);
    const width = 670 / items.length;
    items.forEach(([name], i) => {
      const x = 44 + width * i;
      add(svg, 'rect', { x, y: 88, width: width - 11, height: 110, rx: 10,
        fill: i === index ? blue : 'var(--accent-bg)', stroke: i === index ? blue : grid, 'stroke-width': 2 });
      label(svg, x + (width - 11) / 2, 145, name, { 'text-anchor': 'middle', fill: i === index ? 'white' : ink,
        'font-size': items.length > 5 ? 13 : 15, 'font-weight': 650 });
      if (i < items.length - 1) label(svg, x + width - 7, 147, '→', { fill: muted, 'font-size': 17 });
    });
    label(svg, 50, 49, `第 ${index + 1} / ${items.length} 步`, { fill: blue, 'font-size': 14 });
    display(widget, `${items[index][0]}：${items[index][1]}`);
    const prev = widget.querySelector('[data-step="prev"]'), next = widget.querySelector('[data-step="next"]');
    prev.disabled = index === 0; next.disabled = index === items.length - 1;
  }

  function draw(widget, p) {
    const svg = widget.querySelector('svg'), kind = widget.dataset.widget;
    if (kind === 'steps') return steps(widget, svg);
    if (kind === 'dilution') {
      reset(svg);
      const total = p.old + p.new, share = p.old / total;
      label(svg, 78, 58, '发行前：原股东 100%', { 'font-size': 17 });
      add(svg, 'rect', { x: 78, y: 83, width: 610, height: 57, rx: 8, fill: blue });
      label(svg, 78, 196, `发行后：原股东 ${fmt(share * 100, 1)}%`, { 'font-size': 17 });
      add(svg, 'rect', { x: 78, y: 219, width: 610 * share, height: 57, rx: 8, fill: blue });
      add(svg, 'rect', { x: 78 + 610 * share, y: 219, width: 610 * (1 - share), height: 57, rx: 8, fill: orange });
      display(widget, `原有 ${fmt(p.old)} 万股 + 新增 ${fmt(p.new)} 万股 = ${fmt(total)} 万股；新股东 ${fmt((1 - share) * 100, 1)}%。`);
    } else if (kind === 'dhondt') {
      const votes = [p.a, p.b, p.c], result = math.dhondt(votes, p.seats);
      bars(svg, result.seats.map((value, i) => ({ name: 'ABC'[i], value })), Math.max(3, p.seats), '席');
      display(widget, `分席顺序：${result.order.map(o => 'ABC'[o.party]).join(' → ')}。当前 A/B/C 席数：${result.seats.join(' / ')}。`);
    } else if (kind === 'prisoner') {
      reset(svg);
      const payoffs = [[[3, 3], [0, 5]], [[5, 0], [1, 1]]];
      label(svg, 280, 48, 'B 合作', { 'text-anchor': 'middle' });
      label(svg, 545, 48, 'B 不合作', { 'text-anchor': 'middle' });
      for (let row = 0; row < 2; row++) for (let col = 0; col < 2; col++) {
        const x = 155 + col * 265, y = 68 + row * 112;
        add(svg, 'rect', { x, y, width: 245, height: 95, rx: 10,
          fill: row === p.a && col === p.b ? blue : 'var(--accent-bg)', stroke: grid });
        label(svg, x + 122, y + 55, `(${payoffs[row][col].join(', ')})`, { 'text-anchor': 'middle',
          fill: row === p.a && col === p.b ? 'white' : ink, 'font-size': 24 });
      }
      label(svg, 35, 120, 'A 合作'); label(svg, 35, 232, 'A 不合作');
      display(widget, `当前选择：A${p.a ? '不合作' : '合作'}、B${p.b ? '不合作' : '合作'}；收益为 (${payoffs[p.a][p.b].join(', ')})。`);
    } else if (kind === 'did') {
      const treated = p.treated, control = p.control, effect = (treated - 70) - (control - 68);
      plot(svg, [0, 1, 60, 95], [
        { name: '实施组', fn: x => 70 + (treated - 70) * x },
        { name: '对照组', fn: x => 68 + (control - 68) * x },
        { name: '平行趋势反事实', fn: x => 70 + (control - 68) * x, dash: true }
      ], '0=政策前，1=政策后', '就业率（%）');
      display(widget, `DID=(${fmt(treated)}−70)−(${fmt(control)}−68)=${fmt(effect)} 个百分点；平行趋势等条件须另行检验。`);
    } else if (kind === 'poll') {
      const rate = p.p / 100, se = Math.sqrt(rate * (1 - rate) / p.n), moe = 1.96 * se * 100;
      const lo = Math.max(0, p.p - 4 * moe), hi = Math.min(100, p.p + 4 * moe);
      plot(svg, [lo, hi, 0, 1.1], [
        { name: '近似抽样分布', fn: x => Math.exp(-0.5 * ((x - p.p) / (se * 100)) ** 2) }
      ], '估计比例（%）', '相对密度', [{ x: p.p, y: 1, name: `${fmt(p.p)}%` }]);
      display(widget, `95% 正态近似误差约 ±${fmt(moe, 1)} 个百分点；区间约 ${fmt(p.p - moe, 1)}%～${fmt(p.p + moe, 1)}%。`);
    } else if (kind === 'effective') {
      const raw = [p.a, p.b, p.c], total = raw.reduce((a, b) => a + b, 0), shares = raw.map(v => v / total);
      bars(svg, shares.map((value, i) => ({ name: 'ABC'[i], value: value * 100 })), 100, '%');
      display(widget, `份额 ${shares.map(x => `${fmt(x * 100, 1)}%`).join(' / ')}；有效政党数量 ${fmt(1 / shares.reduce((sum, x) => sum + x * x, 0))}。`);
    } else if (kind === 'supply_demand') {
      const demand = q => p.demand - 0.5 * q, supply = q => 10 + p.slope * q;
      const qStar = (p.demand - 10) / (0.5 + p.slope), price = demand(qStar);
      plot(svg, [0, 130, 0, 100], [
        { name: '需求 Pᵈ(Q)', fn: demand }, { name: '供给 Pˢ(Q)', fn: supply }
      ], '数量 Q', '价格 P', [{ x: qStar, y: price, name: '均衡' }]);
      display(widget, `线性示例的均衡：Q≈${fmt(qStar, 1)}，P≈${fmt(price, 1)}。改变需求强度会移动整条需求曲线。`);
    } else if (kind === 'breakeven') {
      const be = math.breakEven(p.price, p.variable, p.fixed), xmax = Number.isFinite(be) ? Math.max(100, be * 1.7) : 100;
      const ymax = Math.max(p.price * xmax, p.fixed + p.variable * xmax) * 1.08;
      plot(svg, [0, xmax, 0, ymax], [
        { name: '收入 pQ', fn: q => p.price * q },
        { name: '总成本 F+vQ', fn: q => p.fixed + p.variable * q }
      ], '销量 Q', '金额', Number.isFinite(be) ? [{ x: be, y: p.price * be, name: '盈亏平衡' }] : []);
      display(widget, Number.isFinite(be) ? `单位贡献 ${fmt(p.price - p.variable)}；盈亏平衡销量约 ${fmt(be, 0)}。` :
        '单价不高于单位变动成本，当前模型不存在有限的盈亏平衡销量。');
    } else if (kind === 'lorenz') {
      plot(svg, [0, 1, 0, 1], [
        { name: '完全平等线', fn: x => x, dash: true },
        { name: '合成洛伦兹曲线', fn: x => x ** p.k }
      ], '累计人口份额', '累计收入份额');
      display(widget, `L(p)=p^${fmt(p.k, 1)}；该合成曲线的基尼系数 G=${fmt((p.k - 1) / (p.k + 1), 3)}。`);
    } else if (kind === 'compound') {
      const rate = p.rate / 100, end = math.compound(1000, rate, p.years), max = Math.max(1000, end, 1000 * (1 + rate * p.years)) * 1.1;
      plot(svg, [0, p.years, Math.min(0, end), max], [
        { name: '复利', fn: t => math.compound(1000, rate, t) },
        { name: '单利对照', fn: t => 1000 * (1 + rate * t), dash: true }
      ], '年数', '金额');
      display(widget, `本金 1000，${fmt(p.years, 0)} 年后复利结果 ${fmt(end)}；这是给定利率的数学情景。`);
    } else if (kind === 'bond') {
      const price = math.bondPrice(p.coupon / 100, p.years, p.yield / 100);
      plot(svg, [1, 15, 50, 150], [{ name: '债券价格', fn: y => math.bondPrice(p.coupon / 100, p.years, y / 100) }],
        '要求收益率（%）', '价格（面值=100）', [{ x: p.yield, y: price, name: '当前' }]);
      display(widget, `票息 ${fmt(p.coupon, 1)}%，期限 ${p.years} 年，要求收益率 ${fmt(p.yield, 1)}% 时价格约 ${fmt(price)}。`);
    } else if (kind === 'portfolio') {
      const weight = p.weight / 100, risk = math.portfolioRisk(weight, p.rho);
      plot(svg, [0, 100, 0, 30], [{ name: '组合标准差', fn: w => 100 * math.portfolioRisk(w / 100, p.rho) }],
        '资产 A 权重（%）', '风险 σ（%）', [{ x: p.weight, y: risk * 100, name: '当前' }]);
      display(widget, `假设 σA=25%、σB=12%、相关系数 ${fmt(p.rho, 1)}；当前组合标准差 ${fmt(risk * 100, 1)}%。`);
    } else if (kind === 'drawdown') {
      const values = [100, 108, 114, 111, 114 * (1 - p.shock / 100), 108, 112, 117];
      const peaks = values.map((v, i) => Math.max(...values.slice(0, i + 1)));
      const worst = Math.min(...values.map((v, i) => v / peaks[i] - 1));
      plot(svg, [0, 7, 60, 130], [
        { name: '合成价格', fn: x => betweenPoints(values, x) },
        { name: '历史高点', fn: x => betweenPoints(peaks, x), dash: true }
      ], '时间点', '相对价格');
      display(widget, `最大回撤 ${fmt(-worst * 100, 1)}%，按历史高点到后续低点计算；路径为合成示例。`);
    } else if (kind === 'candle') {
      reset(svg);
      const o = p.open, c = o + p.change, h = Math.max(o, c) + p.upper, l = Math.min(o, c) - p.lower;
      const Y = value => 258 - (value - (l - 5)) / (h - l + 10) * 200;
      line(svg, 375, Y(h), 375, Y(l), muted, 5);
      add(svg, 'rect', { x: 320, y: Y(Math.max(o, c)), width: 110,
        height: Math.max(3, Math.abs(Y(o) - Y(c))), fill: c >= o ? red : green, rx: 3 });
      [['高 H', h], ['开 O', o], ['收 C', c], ['低 L', l]].forEach(([name, value], i) =>
        label(svg, i % 2 ? 495 : 190, 70 + i * 63, `${name} = ${fmt(value)}`, { 'font-size': 17 }));
      display(widget, `H=${fmt(h)} ≥ max(O,C)；L=${fmt(l)} ≤ min(O,C)。单根 K 线不能单独证明未来方向。`);
    } else if (kind === 'vwap') {
      const prices = [100, 102, 99, 104, 101], volumes = [10, 15, 20 * p.volume, 8, 12];
      let money = 0, count = 0;
      const vwap = prices.map((price, i) => { money += price * volumes[i]; count += volumes[i]; return money / count; });
      plot(svg, [1, 5, 96, 106], [
        { name: '成交价格', fn: x => betweenPoints(prices, x - 1) },
        { name: '累计 VWAP', fn: x => betweenPoints(vwap, x - 1) }
      ], '第几笔成交', '价格');
      display(widget, `第五笔后的 VWAP=${fmt(vwap[4])}；第三笔成交量为 ${fmt(volumes[2])} 单位。`);
    } else if (kind === 'position') {
      const budget = p.capital * 10000 * p.risk / 100, quantity = budget / p.gap;
      reset(svg);
      [[65, '资金 × 风险比例', `${fmt(p.capital)} 万元 × ${fmt(p.risk, 1)}%`],
        [300, '计划风险预算', `${fmt(budget)} 元`],
        [535, '理论持股数', `${fmt(quantity, 0)} 股`]].forEach(([x, title, value]) => {
        add(svg, 'rect', { x, y: 84, width: 170, height: 136, rx: 12, fill: 'var(--accent-bg)', stroke: grid, 'stroke-width': 2 });
        label(svg, x + 85, 133, title, { 'text-anchor': 'middle', 'font-size': 14 });
        label(svg, x + 85, 179, value, { 'text-anchor': 'middle', 'font-size': 20, fill: blue, 'font-weight': 700 });
      });
      label(svg, 262, 164, '→', { 'font-size': 29, fill: muted });
      label(svg, 497, 164, '÷', { 'font-size': 29, fill: muted });
      label(svg, 605, 251, `每股价差 ${fmt(p.gap)} 元`, { 'text-anchor': 'middle', 'font-size': 13 });
      display(widget, `Q=(${fmt(p.capital)} 万元×${fmt(p.risk, 1)}%)/${fmt(p.gap)} 元≈${fmt(quantity, 0)} 股；不是实际亏损上限。`);
    } else if (kind === 'winrate') {
      const now = math.winrate(p.ratio, p.cost);
      plot(svg, [0.5, 5, 0, 100], [{ name: '盈亏平衡胜率', fn: b => 100 * math.winrate(b, p.cost) }],
        '盈亏比 b', '最低胜率（%）', [{ x: p.ratio, y: now * 100, name: '当前' }]);
      display(widget, `忽略其他因素时，pₘᵢₙ=(1+c)/(1+b)=${fmt(now * 100, 1)}%。`);
    } else if (kind === 'leveragepath') {
      const index = [100, 100 * (1 + p.up / 100), 100 * (1 + p.up / 100) * (1 - p.down / 100)];
      const leveraged = [100, 100 * (1 + p.factor * p.up / 100),
        100 * (1 + p.factor * p.up / 100) * (1 - p.factor * p.down / 100)];
      plot(svg, [0, 2, 50, 160], [
        { name: '指数', fn: x => betweenPoints(index, x) },
        { name: `${fmt(p.factor, 1)} 倍每日重置`, fn: x => betweenPoints(leveraged, x) }
      ], '交易日', '初始净值=100');
      display(widget, `两日后指数 ${fmt(index[2])}，每日重置产品 ${fmt(leveraged[2])}；路径和复利共同影响结果。`);
    } else if (kind === 'balance') {
      const assets = p.liability + p.equity;
      bars(svg, [{ name: '资产', value: assets }, { name: '负债', value: p.liability }, { name: '权益', value: p.equity }]);
      display(widget, `资产 ${fmt(assets)} = 负债 ${fmt(p.liability)} + 所有者权益 ${fmt(p.equity)}（万元）。`);
    } else if (kind === 'depreciation') {
      const salvage = Math.min(p.cost, p.salvage), annual = (p.cost - salvage) / p.years;
      plot(svg, [0, p.years, 0, p.cost * 1.1], [
        { name: '账面价值', fn: t => Math.max(salvage, p.cost - annual * t) },
        { name: '残值', fn: () => salvage, dash: true }
      ], '年数', '金额（万元）');
      display(widget, `每年折旧 ${fmt(annual)} 万元；第 ${p.years} 年末账面价值 ${fmt(salvage)} 万元。`);
    } else if (kind === 'ccc') {
      const ccc = p.dio + p.dso - p.dpo;
      bars(svg, [
        { name: '存货 DIO', value: p.dio }, { name: '应收 DSO', value: p.dso },
        { name: '应付 DPO', value: p.dpo }, { name: '现金周期', value: Math.max(0, ccc) }
      ], null, '天');
      display(widget, `CCC=${fmt(p.dio)}+${fmt(p.dso)}−${fmt(p.dpo)}=${fmt(ccc)} 天。`);
    } else if (kind === 'dupont') {
      const roe = p.margin / 100 * p.turnover * p.multiplier * 100;
      reset(svg);
      [[45, '销售净利率', `${fmt(p.margin, 1)}%`],
        [240, '资产周转率', `${fmt(p.turnover, 1)} 次`],
        [435, '权益乘数', `${fmt(p.multiplier, 1)} 倍`]].forEach(([x, title, value]) => {
        add(svg, 'rect', { x, y: 72, width: 170, height: 115, rx: 12, fill: 'var(--accent-bg)', stroke: grid, 'stroke-width': 2 });
        label(svg, x + 85, 116, title, { 'text-anchor': 'middle', 'font-size': 14 });
        label(svg, x + 85, 158, value, { 'text-anchor': 'middle', 'font-size': 21, fill: blue, 'font-weight': 700 });
      });
      label(svg, 221, 142, '×', { 'font-size': 24 }); label(svg, 416, 142, '×', { 'font-size': 24 });
      label(svg, 622, 142, `= ROE ${fmt(roe, 1)}%`, { 'font-size': 18, fill: orange, 'font-weight': 700 });
      display(widget, `ROE=${fmt(p.margin, 1)}%×${fmt(p.turnover, 1)}×${fmt(p.multiplier, 1)}=${fmt(roe, 1)}%。`);
    } else if (kind === 'npv') {
      const rate = p.rate / 100, npv = math.npv(p.initial, p.cashflow, rate, p.years);
      const cumulative = t => {
        let value = -p.initial;
        for (let year = 1; year <= Math.floor(t); year++) value += p.cashflow / (1 + rate) ** year;
        return value;
      };
      const limit = Math.max(p.initial, Math.abs(npv), p.cashflow * p.years) * 1.2;
      plot(svg, [0, p.years, -limit, limit], [
        { name: '累计折现净现金流', fn: cumulative }, { name: '零基线', fn: () => 0, dash: true }
      ], '年末', '金额（万元）');
      display(widget, `NPV=${fmt(npv)} 万元；未来各期现金流按 ${fmt(p.rate, 1)}% 折现。`);
    } else if (kind === 'finleverage') {
      const roe = debt => (p.ebit - debt * p.rate / 100) * 0.75 / (1000 - debt) * 100;
      plot(svg, [0, 800, -20, 80], [{ name: '简化 ROE', fn: roe }],
        '债务金额（万元）', '股东回报率（%）', [{ x: p.debt, y: roe(p.debt), name: '当前' }]);
      display(widget, `假设资产 1000 万、税率 25%；债务 ${fmt(p.debt)} 万时 ROE≈${fmt(roe(p.debt), 1)}%。`);
    } else if (kind === 'weighted') {
      const sum = p.cost + p.quality + p.delivery;
      const weights = [p.cost / sum, p.quality / sum, p.delivery / sum];
      const scores = [[90, 65, 70], [70, 90, 85], [80, 80, 75]]
        .map(row => row.reduce((a, value, i) => a + value * weights[i], 0));
      bars(svg, scores.map((value, i) => ({ name: 'ABC'[i], value })), 100, '分');
      display(widget, `归一化权重 ${weights.map(v => `${fmt(v * 100, 0)}%`).join(' / ')}；当前最高为 ${'ABC'[scores.indexOf(Math.max(...scores))]}。`);
    } else if (kind === 'ltv') {
      const value = p.margin / (p.churn / 100);
      bars(svg, [{ name: '简化 LTV', value }, { name: '获客成本 CAC', value: p.cac }]);
      display(widget, `简化 LTV=${fmt(p.margin)}/(${fmt(p.churn)}%)=${fmt(value)} 元；LTV/CAC=${fmt(value / p.cac)}。`);
    } else if (kind === 'eoq') {
      const optimum = math.eoq(p.demand, p.order, p.holding), xmax = Math.max(200, optimum * 2.5);
      const ordering = q => p.demand / Math.max(1, q) * p.order, holding = q => q / 2 * p.holding;
      const ymax = (ordering(optimum / 3) + holding(optimum / 3)) * 1.1;
      plot(svg, [Math.max(1, optimum / 3), xmax, 0, ymax], [
        { name: '年订货成本', fn: ordering }, { name: '年持有成本', fn: holding },
        { name: '两项合计', fn: q => ordering(q) + holding(q) }
      ], '每次订货量 Q', '年度成本', [{ x: optimum, y: ordering(optimum) + holding(optimum), name: 'EOQ' }]);
      display(widget, `EOQ=√(2DS/H)≈${fmt(optimum, 0)} 件；该点两类成本相等。`);
    } else if (kind === 'evm') {
      bars(svg, [
        { name: '计划价值 PV', value: p.pv }, { name: '挣得价值 EV', value: p.ev },
        { name: '实际成本 AC', value: p.ac }
      ]);
      display(widget, `CV=${fmt(p.ev - p.ac)}，SV=${fmt(p.ev - p.pv)}；CPI=${fmt(p.ev / p.ac)}，SPI=${fmt(p.ev / p.pv)}。`);
    } else if (kind === 'pareto') {
      const counts = [40, 30, 15, 10, 5], names = ['接口', '配置', '性能', '界面', '其他'];
      bars(svg, counts.map((value, i) => ({ name: names[i], value,
        color: i < p.top ? blue : 'var(--border)' })), 50, '项');
      display(widget, `前 ${p.top} 类缺陷占 ${counts.slice(0, p.top).reduce((a, b) => a + b, 0)}%；先排查高频类别，仍需验证具体原因。`);
    } else if (kind === 'sigmoid') {
      plot(svg, [0, 10, 0, 1], [{ name: 'Logistic 示意', fn: t => 1 / (1 + Math.exp(-p.rate * (t - p.mid))) }],
        '时间', '相对采纳比例', [{ x: p.mid, y: 0.5, name: '拐点' }]);
      display(widget, `拐点在 t=${fmt(p.mid, 1)}；增长速率参数 ${fmt(p.rate, 1)}。`);
    } else if (kind === 'correlation') {
      reset(svg);
      const rho = p.rho, L = 85, B = 275, scale = 160;
      for (let i = -2; i <= 2; i++) {
        line(svg, L, B - (i + 2) * 52, 700, B - (i + 2) * 52);
        line(svg, L + (i + 2) * 150, 65, L + (i + 2) * 150, B);
      }
      const noise = [0.6,-0.7,0.2,1,-0.5,0.4,-1,0.9,-0.2,0.3,0.8,-0.6,0.1,-0.9,0.5,0.2];
      noise.forEach((n, i) => {
        const x = (i - 7.5) / 4.2, y = rho * x + Math.sqrt(1 - rho * rho) * n;
        add(svg, 'circle', { cx: 390 + x * scale, cy: 168 - y * 76, r: 6, fill: blue, opacity: 0.8 });
      });
      line(svg, 90, 168 + rho * 140, 690, 168 - rho * 140, orange, 3);
      label(svg, 87, 35, '合成散点：设定趋势参数 ρ', { 'font-size': 15 });
      display(widget, `参数 ρ=${fmt(rho, 1)}；散点围绕线性趋势变化，不能据此断定因果方向。`);
    } else if (kind === 'fechner') {
      plot(svg, [1, 20, 0, 10], [{ name: 'S=k ln(I/I₀)', fn: x => p.k * Math.log(x) }],
        '刺激比 I/I₀', '感觉强度 S');
      display(widget, `I/I₀=10 时 S=${fmt(p.k * Math.log(10))}；对数增长意味着增量逐渐变小。`);
    } else if (kind === 'forgetting') {
      plot(svg, [0, 20, 0, 1.05], [
        { name: `τ=${fmt(p.tau, 0)} 的示意`, fn: t => Math.exp(-t / p.tau) },
        { name: '另一时间尺度', fn: t => Math.exp(-t / 10), dash: true }
      ], '时间（任意单位）', '相对保持程度');
      display(widget, `t=10 时相对保持程度约 ${fmt(100 * Math.exp(-10 / p.tau), 1)}%；不是实测记忆百分比。`);
    } else if (kind === 'bayes') {
      const { tp, fp, ppv } = math.bayes(p.prevalence / 100, p.sensitivity / 100, p.specificity / 100);
      bars(svg, [
        { name: '真阳性', value: tp * 10000 }, { name: '假阳性', value: fp * 10000 }
      ], Math.max(100, (tp + fp) * 11000), '人');
      display(widget, `假设 10000 人：真阳性约 ${fmt(tp * 10000, 0)}，假阳性约 ${fmt(fp * 10000, 0)}；阳性预测值 ${fmt(ppv * 100, 2)}%。`);
    } else if (kind === 'normal') {
      const z = (p.score - 100) / 15, density = x => Math.exp(-0.5 * ((x - 100) / 15) ** 2);
      plot(svg, [55, 145, 0, 1.05], [{ name: '正态密度（相对）', fn: density }],
        '标准化分数', '相对密度', [{ x: p.score, y: density(p.score), name: '示例值' }]);
      display(widget, `示例分数 ${p.score} 对应 z=${fmt(z)}；图形仅说明标准化分布。`);
    } else if (kind === 'bigfive') {
      reset(svg);
      const names = ['开放性', '尽责性', '外向性', '宜人性', '神经质'];
      const vals = [p.o, p.c, p.e, p.a, p.n], cx = 380, cy = 165;
      const point = (i, radius) => [cx + radius * Math.sin(i * 2 * Math.PI / 5), cy - radius * Math.cos(i * 2 * Math.PI / 5)];
      for (const radius of [35, 70, 105])
        add(svg, 'polygon', { points: names.map((_, i) => point(i, radius).join(',')).join(' '),
          fill: 'none', stroke: grid });
      names.forEach((name, i) => {
        const outer = point(i, 135), inner = point(i, 105);
        line(svg, cx, cy, inner[0], inner[1]);
        label(svg, outer[0], outer[1], name, { 'text-anchor': 'middle', 'font-size': 13 });
      });
      add(svg, 'polygon', { points: vals.map((v, i) => point(i, v * 1.05).join(',')).join(' '),
        fill: 'var(--viz-blue-bg)', stroke: blue, 'stroke-width': 3 });
      display(widget, `虚构维度数值：${names.map((name, i) => `${name} ${vals[i]}`).join('；')}。`);
    }
  }

  document.querySelectorAll('.social-widget').forEach(widget => {
    const inputs = [...widget.querySelectorAll('input[data-param]')];
    const update = () => {
      const params = {};
      inputs.forEach(input => {
        params[input.dataset.param] = Number(input.value);
        input.nextElementSibling.textContent = fmt(Number(input.value), 2);
      });
      draw(widget, params);
    };
    try {
      widget.querySelectorAll('[data-step]').forEach(button => button.addEventListener('click', () => {
        const total = JSON.parse(widget.dataset.steps).length;
        const next = Number(widget.dataset.stepIndex || 0) + (button.dataset.step === 'next' ? 1 : -1);
        widget.dataset.stepIndex = Math.max(0, Math.min(total - 1, next));
        update();
      }));
      inputs.forEach(input => input.addEventListener('input', update));
      update();
      widget.classList.add('widget-ready');
      widget.querySelector('.social-original').open = false;
    } catch (error) {
      console.error('Social widget failed; source figure remains visible.', error);
    }
  });
})();
