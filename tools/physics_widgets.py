"""Interactive physics figures, each attached to one source heading.

The SVG rendered by visuals.py stays visible if JavaScript is unavailable.
"""
from html import escape
from visuals import S, render


def W(match, kind, title, note, fallback, controls):
 return dict(match=match, kind=kind, title=title, note=note, fallback=fallback, controls=controls)


WIDGETS={
 'physics/12 气体动理论.md':[
  W('1.3.4 物态方程的形式','gas_isotherm','等温线：改变温度','保持物质的量不变，理想气体 p∝T/V；曲线用相对量表示。','isotherm',[('温度比 T/T₀','temperature',0.5,2,0.1,1)]),
  W('3.3.2 玻尔兹曼密度分布','gas_barometric','密度随高度衰减：改变温度','等温、定重力加速度的近似模型；n(z)/n₀=exp(−Mg z/RT)。','barometric',[('温度 T（K）','temperature',220,700,20,300)]),
  W('4.1.2 公式','gas_mfp','平均自由程：改变温度','示例取分子直径 0.37 nm；λ=kT/(√2πd²p)。','mean_free_path',[('温度 T（K）','temperature',250,700,25,300)]),
 ],
 'physics/13 热力学基础｜知识体系重构版.md':[
  W('2.5.3 可逆绝热线与等温线的比较','thermo_adiabat','绝热线：改变绝热指数','从相同的初始状态出发，对照 pVᵞ 与 pV 保持常量的曲线。','adiabat',[('绝热指数 γ','gamma',1.1,1.7,0.05,1.4)]),
  W('3.1 循环的结构','thermo_cycle','p–V 循环：改变围成面积','矩形示意循环中，顺时针净功 W=Δp·ΔV；1 kPa·L=1 J。','pv_cycle',[('压强差 Δp（kPa）','dp',20,100,5,50),('体积差 ΔV（L）','dv',1,5,0.25,2)]),
  W('5.3 卡诺效率只依赖热源温度','thermo_carnot','卡诺效率：改变热源温度','η=1−T꜀/Tₕ；仅讨论可逆热机上限，温度单位为 K。','carnot_efficiency',[('热源 Tₕ（K）','hot',550,900,25,600),('冷源 T꜀（K）','cold',200,500,25,300)]),
 ],
 'physics/14 振动 扩充版.md':[
  W('2. 三个特征量：振幅、角频率、初相位','vib_sho','简谐振动：调节三个特征量','位移 x=A cos(ωt+φ)；观察振幅、周期和初相位分别改变什么。','sho',[('振幅 A','amplitude',0.3,1.5,0.1,1),('角频率 ω','omega',0.5,2,0.1,1),('初相位 φ（rad）','phase',0,6.28,0.1,0)]),
  W('2. 共振的发生与条件','vib_resonance','共振曲线：改变阻尼','归一化稳态幅频响应；阻尼增大会降低并展宽峰值。','resonance',[('阻尼比 ζ','zeta',0.05,0.5,0.025,0.15)]),
  W('2. 拍频与拍周期','vib_beats','拍现象：改变频率差','等振幅、接近频率的两振动叠加；包络变化频率由两者频率差决定。','beats',[('频率差 Δf（Hz）','delta',0.1,0.8,0.05,0.3)]),
  W('1. 同频率：一般形成椭圆轨迹','vib_lissajous','李萨如轨迹：改变相位差','两个等振幅、同频率且相互垂直的简谐振动合成。','lissajous',[('相位差 δ（rad）','phase',0,6.28,0.1,1.57)]),
 ],
}


def render_widget(spec):
 fallback=S('',spec['fallback'],spec['title'],spec['note'])
 html=render(fallback)
 html=html.replace('class="concept-visual"',f'class="concept-visual physics-widget" data-widget="{escape(spec["kind"])}"',1)
 controls=''.join(
  f'<label>{escape(label)} <input type="range" data-param="{escape(name)}" min="{low}" max="{high}" step="{step}" value="{value}"><output>{value}</output></label>'
  for label,name,low,high,step,value in spec['controls'])
 html=html.replace('<p class="concept-visual-note">','<div class="physics-controls" aria-label="图像参数">'+controls+'</div><div class="physics-live" aria-live="polite"></div><p class="concept-visual-note">',1)
 return html
