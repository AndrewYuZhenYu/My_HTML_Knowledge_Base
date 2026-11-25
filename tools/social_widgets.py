"""Hand-authored, source-aligned interactive redraws for social-science notes.

Each model replaces one referenced ZIP figure. The original vector remains in
an expandable fallback, so the knowledge point is readable without JavaScript.
"""
from __future__ import annotations

import json
from html import escape


def C(label, key, low, high, step, value):
    return (label, key, low, high, step, value)


def W(prefix, kind, title, note, controls=(), steps=()):
    return dict(prefix=prefix, kind=kind, title=title, note=note,
                controls=controls, steps=steps)


WIDGETS = {
    'social-sciences/01 世界法学知识体系.md': [
        W('law_civilcommon_', 'steps', '两种法律分析路径', '这是研究路径示意；实际规则及适用法域须依具体资料判断。', steps=[
            ('识别问题', '先确认争议事实和法律问题。'),
            ('成文法路径', '查找条文、解释构成条件，再将事实纳入规则。'),
            ('判例路径', '寻找相关权威判例，提取规则并比较重要事实。'),
            ('综合判断', '两种路径可以结合，不由某一种法系独占。')]),
        W('law_flow32_', 'steps', '合同成立与履行的阶段', '流程为教学结构，不表示所有合同都须有相同的书面形式。', steps=[
            ('磋商', '了解交易对象、价格、条件和合作可能性。'),
            ('要约', '检查交易条件的确定性及缔约意图。'),
            ('承诺', '研究接受行为是否满足适用规则。'),
            ('成立与效力', '区分是否达成合意与是否具有预期法律约束力。'),
            ('履行', '依据有效约定及适用规则完成义务。')]),
        W('law_causation_', 'steps', '从事实关联到归责范围', '事实上的因果联系与法律上的归责范围应分开研究。', steps=[
            ('行为', '识别可能相关的行为或不作为。'),
            ('事件链', '列出中间事件与其他可能原因。'),
            ('事实因果', '分析行为与损害之间的事实联系。'),
            ('法律归责', '进一步研究规则保护目的与责任边界。')]),
        W('law_grid59_', 'steps', '证据评价的六个维度', '逐项审视并不等于证据已经达到特定法域的证明标准。', steps=[
            ('关联性', '与待证事实是否相关？'), ('真实性', '来源及内容是否可靠？'),
            ('合法性', '取得和使用是否满足程序条件？'), ('证明力', '支持待证事实的程度如何？'),
            ('完整性', '是否遗漏关键上下文？'), ('相互印证', '是否存在独立来源的支持？')]),
        W('law_dilution_', 'dilution', '股权稀释：新增股份改变比例', '忽略优先权、不同股权类别及其他交易条款。', [
            C('原有股份（万股）', 'old', 50, 300, 10, 100),
            C('新增股份（万股）', 'new', 0, 200, 5, 25)]),
    ],
    'social-sciences/02 政治学知识体系.md': [
        W('politics_dhondt_', 'dhondt', 'D’Hondt：逐席比较商值', '虚构票数；不含门槛及特殊规则，同商值按 A、B、C 顺序处理。', [
            C('A 票数', 'a', 50, 500, 10, 300), C('B 票数', 'b', 50, 500, 10, 210),
            C('C 票数', 'c', 10, 300, 10, 120), C('议席总数', 'seats', 3, 12, 1, 7)]),
        W('politics_prisoner_', 'prisoner', '囚徒困境收益矩阵', '采用正文的虚构收益 (3,3)、(0,5)、(5,0)、(1,1)。', [
            C('A：0 合作 / 1 不合作', 'a', 0, 1, 1, 0), C('B：0 合作 / 1 不合作', 'b', 0, 1, 1, 0)]),
        W('politics_did_', 'did', '双重差分：比较两组变化', '虚构数据；只有平行趋势等识别条件满足时才可解释为政策效果。', [
            C('实施组政策后（%）', 'treated', 65, 90, 1, 80),
            C('对照组政策后（%）', 'control', 65, 85, 1, 73)]),
        W('politics_poll_', 'poll', '抽样误差的近似范围', '仅为简单随机抽样下的二项比例近似，不含设计效应和非抽样误差。', [
            C('样本量 n', 'n', 100, 5000, 100, 1000), C('样本比例（%）', 'p', 10, 90, 5, 50)]),
        W('politics_effective_', 'effective', '有效政党数量', '先把三个虚构份额归一化，再计算 1/Σpᵢ²。', [
            C('A 相对份额', 'a', 1, 100, 1, 45), C('B 相对份额', 'b', 1, 100, 1, 35),
            C('C 相对份额', 'c', 1, 100, 1, 20)]),
    ],
    'social-sciences/03 经济学知识体系.md': [
        W('econ_demand_', 'supply_demand', '需求移动与市场均衡', '线性供需是教学示例；滑块改变需求截距，价格变动则沿同一需求曲线移动。', [
            C('需求强度', 'demand', 45, 95, 5, 70), C('供给斜率', 'slope', 0.2, 1, 0.1, 0.5)]),
        W('econ_profit_', 'breakeven', '收入、成本与盈亏平衡', '假设单价与单位变动成本在所示产量范围内稳定。', [
            C('单价', 'price', 60, 150, 5, 100), C('单位变动成本', 'variable', 10, 90, 5, 60),
            C('固定成本', 'fixed', 1000, 8000, 500, 4000)]),
        W('econ_lorenz_', 'lorenz', '洛伦兹曲线与基尼系数', '用 L(p)=pᵏ 的合成分布演示面积法，不代表任何国家的实际数据。', [
            C('曲线指数 k', 'k', 1, 4, 0.1, 2)]),
    ],
    'social-sciences/04 金融学知识体系.md': [
        W('fin_timevalue_', 'compound', '现值与终值：复利曲线', '固定本金 1000，按年复利，无追加投入或费用。', [
            C('年利率（%）', 'rate', 0, 15, 0.5, 5), C('年数', 'years', 1, 30, 1, 15)]),
        W('fin_bondprice_', 'bond', '债券价格与要求收益率', '面值 100、年付息、到期偿还面值且现金流确定的简化债券。', [
            C('年票息率（%）', 'coupon', 1, 12, 0.5, 5),
            C('到期年数', 'years', 1, 20, 1, 5), C('要求收益率（%）', 'yield', 1, 15, 0.5, 6)]),
        W('fin_frontier_', 'portfolio', '两资产组合的风险曲线', '用标准差和相关系数计算组合波动率；输入为假设值。', [
            C('资产 A 权重（%）', 'weight', 0, 100, 5, 50),
            C('相关系数 ρ', 'rho', -1, 1, 0.1, 0.2)]),
        W('fin_drawdown_', 'drawdown', '价格路径与最大回撤', '固定示例路径，调整一次下跌幅度以比较最高点到后续低点的距离。', [
            C('中段冲击（%）', 'shock', 0, 40, 2, 20)]),
    ],
    'social-sciences/05 股票投资与证券交易.md': [
        W('invest_compound_', 'compound', '复利与长期结果', '纯数学情景，不预测未来收益；忽略税费和波动。', [
            C('年收益率（%）', 'rate', -5, 15, 0.5, 5), C('年数', 'years', 1, 30, 1, 20)]),
        W('invest_ohlc_', 'candle', 'K 线：开高低收的几何关系', '一根自拟 K 线，仅展示四价之间的约束，不提供形态预测。', [
            C('开盘价', 'open', 80, 120, 1, 100), C('收盘相对开盘', 'change', -20, 20, 1, 8),
            C('上影线长度', 'upper', 0, 15, 1, 5), C('下影线长度', 'lower', 0, 15, 1, 4)]),
        W('invest_vwap_extra_', 'vwap', '成交量加权平均价', '五笔虚构成交，VWAP=Σ价格×成交量/Σ成交量。', [
            C('第三笔成交量倍数', 'volume', 0.5, 5, 0.5, 2)]),
        W('invest_position_calc_', 'position', '风险预算与理论持股数', '仅用于理解 Q=Ar/(P−S)；未计交易单位、费用、跳空及组合风险。', [
            C('资金 A（万元）', 'capital', 1, 100, 1, 10),
            C('计划风险比例（%）', 'risk', 0.2, 5, 0.2, 1),
            C('止损价差 P−S（元）', 'gap', 1, 30, 1, 5)]),
        W('invest_break_even_extra_', 'winrate', '盈亏比与理论盈亏平衡胜率', '把每次亏损设为 1 单位；成本以同一单位计。', [
            C('盈利 / 亏损比 b', 'ratio', 0.5, 5, 0.1, 2),
            C('每次交易成本（亏损单位）', 'cost', 0, 0.3, 0.01, 0)]),
        W('invest_leveraged_etf_', 'leveragepath', '每日重置杠杆的路径依赖', '两日示例不包含融资费和跟踪误差；长期表现不是简单倍数。', [
            C('首日指数涨幅（%）', 'up', 2, 20, 1, 10),
            C('次日指数跌幅（%）', 'down', 2, 20, 1, 10),
            C('每日杠杆倍数', 'factor', 1, 3, 0.5, 2)]),
    ],
    'social-sciences/06 会计学知识体系.md': [
        W('accounting_balance_', 'balance', '会计恒等式：资产与资金来源', '资产=负债+所有者权益；金额单位为万元。', [
            C('负债', 'liability', 0, 900, 25, 400), C('所有者权益', 'equity', 100, 900, 25, 600)]),
        W('accounting_line_5cbcb66a', 'depreciation', '直线法折旧与账面价值', '忽略减值及其他调整，年度折旧=(原价−残值)/使用年限。', [
            C('原价（万元）', 'cost', 50, 500, 10, 200),
            C('残值（万元）', 'salvage', 0, 100, 5, 20), C('使用年限', 'years', 2, 15, 1, 5)]),
        W('accounting_breakeven_', 'breakeven', '本量利分析：盈亏平衡点', '简化模型；单价和单位变动成本在相关范围内恒定。', [
            C('单价（元）', 'price', 60, 150, 5, 100),
            C('单位变动成本（元）', 'variable', 10, 90, 5, 60),
            C('固定成本（元）', 'fixed', 100000, 800000, 50000, 400000)]),
        W('accounting_ccc_', 'ccc', '现金转换周期：三个时间段', 'CCC=DIO+DSO−DPO；负值仅代表计算结果，仍需结合业务模式解释。', [
            C('存货天数 DIO', 'dio', 10, 120, 5, 60),
            C('应收天数 DSO', 'dso', 10, 120, 5, 45),
            C('应付天数 DPO', 'dpo', 0, 120, 5, 30)]),
        W('accounting_tree_f334', 'dupont', '杜邦分析：ROE 三因素分解', 'ROE=销售净利率×总资产周转率×权益乘数。', [
            C('净利率（%）', 'margin', 2, 25, 1, 10),
            C('资产周转率', 'turnover', 0.3, 3, 0.1, 1.2),
            C('权益乘数', 'multiplier', 1, 5, 0.1, 2)]),
        W('accounting_npv_', 'npv', '项目现金流折现与净现值', '等额年末净现金流的示例；预测值和折现率均为假设。', [
            C('初始投入（万元）', 'initial', 50, 200, 10, 100),
            C('每年净现金流（万元）', 'cashflow', 10, 60, 2, 30),
            C('折现率（%）', 'rate', 0, 20, 1, 10),
            C('年数', 'years', 2, 10, 1, 5)]),
        W('accounting_leverage_', 'finleverage', '债务比例与股东回报', '假设资产固定、EBIT 和税率固定，忽略财务困境成本；仅展示杠杆的双向作用。', [
            C('债务金额（万元）', 'debt', 0, 800, 25, 400),
            C('EBIT（万元）', 'ebit', 20, 200, 10, 120),
            C('债务利率（%）', 'rate', 2, 15, 1, 6)]),
    ],
    'social-sciences/07 管理学知识体系.md': [
        W('management_weighted_', 'weighted', '多目标决策：权重如何改变排序', 'A(90,65,70)、B(70,90,85)、C(80,80,75) 为虚构评分；权重自动归一化。', [
            C('成本权重', 'cost', 1, 10, 1, 4), C('质量权重', 'quality', 1, 10, 1, 4),
            C('交付权重', 'delivery', 1, 10, 1, 2)]),
        W('management_ltv_', 'ltv', '订阅业务的简化单位经济', '月贡献毛益/月流失率仅适用于稳定流失等简化假设，不等于实际客户价值。', [
            C('月贡献毛益（元）', 'margin', 20, 300, 10, 100),
            C('月流失率（%）', 'churn', 1, 20, 1, 5),
            C('获客成本（元）', 'cac', 100, 3000, 100, 800)]),
        W('management_eoq_', 'eoq', '经济订货量与两类成本', '经典 EOQ 假设需求及成本稳定，不含折扣、缺货和安全库存。', [
            C('年需求 D', 'demand', 500, 10000, 500, 4000),
            C('每次订货成本 S', 'order', 50, 500, 25, 200),
            C('单位年持有成本 H', 'holding', 2, 30, 1, 10)]),
        W('management_evm_', 'evm', '项目挣值：PV、EV、AC 的关系', 'CV=EV−AC，SV=EV−PV，CPI=EV/AC，SPI=EV/PV。', [
            C('计划价值 PV', 'pv', 20, 200, 10, 100),
            C('挣得价值 EV', 'ev', 20, 200, 10, 90),
            C('实际成本 AC', 'ac', 20, 200, 10, 110)]),
        W('management_bep_', 'breakeven', '本量利分析：数量与利润', '简化模型；忽略多产品组合和产能约束。', [
            C('单价', 'price', 60, 150, 5, 100),
            C('单位变动成本', 'variable', 10, 90, 5, 60),
            C('固定成本', 'fixed', 1000, 8000, 500, 4000)]),
        W('management_pareto_', 'pareto', '帕累托图：先处理主要类别', '虚构的 100 项软件缺陷；条形为频次，折线为累计占比。', [
            C('显示前几类', 'top', 1, 5, 1, 2)]),
        W('management_scurve_', 'sigmoid', '技术 S 曲线的参数演示', 'Logistic 曲线仅用于说明增长阶段，不预测真实技术扩散。', [
            C('增长速率', 'rate', 0.3, 2, 0.1, 0.9),
            C('拐点时间', 'mid', 2, 8, 0.5, 5)]),
    ],
    'social-sciences/08 心理学知识体系.md': [
        W('psych_correlation_', 'correlation', '相关系数与散点形状', '固定的合成随机序列；相关不能单独证明因果。', [
            C('设定相关趋势 r', 'rho', -0.9, 0.9, 0.1, 0.5)]),
        W('psych_fechner_', 'fechner', '费希纳定律的对数曲线', 'S=k ln(I/I₀) 仅在相应假设及刺激范围内适用。', [
            C('比例常数 k', 'k', 0.5, 3, 0.1, 1.5)]),
        W('psych_forget_', 'forgetting', '遗忘与间隔复习的概念曲线', 'e⁻ᵗ/τ 只是可调示意，不存在人人适用的固定遗忘比例。', [
            C('示意时间尺度 τ', 'tau', 1, 14, 1, 5)]),
        W('psych_bayes_', 'bayes', '基础概率与阳性预测值', '虚构的检测统计学示例，不对应任何实际医学检测。', [
            C('基础发生率（%）', 'prevalence', 0.5, 20, 0.5, 1),
            C('敏感度（%）', 'sensitivity', 50, 99, 1, 90),
            C('特异度（%）', 'specificity', 50, 99, 1, 95)]),
        W('psych_iq_', 'normal', '标准化分数的正态示例', '展示均值 100、标准差 15 的数学模型；不能用作个人评估。', [
            C('示例分数', 'score', 55, 145, 5, 115)]),
        W('psych_radar_', 'bigfive', '大五维度组合示意', '五个数值完全虚构，不是人格测验或诊断。', [
            C('开放性', 'o', 0, 100, 5, 70), C('尽责性', 'c', 0, 100, 5, 55),
            C('外向性', 'e', 0, 100, 5, 65), C('宜人性', 'a', 0, 100, 5, 75),
            C('神经质', 'n', 0, 100, 5, 40)]),
    ],
}


def render_widget(spec: dict, src: str, alt: str) -> str:
    prefix = spec['prefix'].rstrip('_')
    controls = ''.join(
        '<label>' + escape(label) + ' <input type="range" data-param="' + escape(key) +
        f'" min="{low}" max="{high}" step="{step}" value="{value}">' +
        f'<output>{value}</output></label>'
        for label, key, low, high, step, value in spec['controls']
    )
    steps = escape(json.dumps(spec['steps'], ensure_ascii=False), quote=True)
    buttons = ('<div class="social-step-actions"><button type="button" data-step="prev">上一步</button>'
               '<button type="button" data-step="next">下一步</button></div>') if spec['steps'] else ''
    return (
        f'<figure class="concept-visual social-widget" id="social-{escape(prefix)}" '
        f'data-widget="{escape(spec["kind"])}" data-steps="{steps}">'
        f'<figcaption><span>交互重绘</span><strong>{escape(spec["title"])}</strong></figcaption>'
        f'<div class="social-controls">{controls}{buttons}</div>'
        f'<svg role="img" aria-label="{escape(spec["title"])}" viewBox="0 0 760 330"></svg>'
        '<div class="social-readout" aria-live="polite"></div>'
        f'<p class="concept-visual-note">{escape(spec["note"])}</p>'
        '<details class="social-original" open><summary>查看静态重绘图</summary>'
        f'<img src="{escape(src, quote=True)}" alt="{escape(alt, quote=True)}" loading="lazy"></details>'
        '</figure>'
    )
