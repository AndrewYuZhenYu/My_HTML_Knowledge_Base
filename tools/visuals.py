"""Source-linked, offline SVG teaching diagrams inserted into generated articles.

These are supplemental illustrations. Markdown remains the authoritative text.
Each specification names an actual heading in the corresponding source note.
"""
from __future__ import annotations

from html import escape
from math import cos, exp, pi, sin, sqrt
from unicodedata import east_asian_width
from json import dumps


def e(value):
 return escape(str(value), quote=True)


def text(x,y,value,size=16,anchor='middle',color='var(--text)',weight=600):
 return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" font-size="{size}" font-weight="{weight}">{e(value)}</text>'


def rect(x,y,w,h,fill='var(--viz-blue-bg)',stroke='var(--viz-blue)',radius=10):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="1.7"/>'


def arrow(x1,y1,x2,y2,color='var(--viz-blue)'):
 length=sqrt((x2-x1)**2+(y2-y1)**2) or 1
 ux=(x2-x1)/length;uy=(y2-y1)/length;px=-uy;py=ux
 bx=x2-10*ux;by=y2-10*uy
 return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{color}" stroke-width="2.2"/>'
         f'<path d="M{bx+6*px:.1f} {by+6*py:.1f}L{x2:.1f} {y2:.1f}L{bx-6*px:.1f} {by-6*py:.1f}" fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')


def figure(spec,body,height=290):
 title=e(spec['title']);note=e(spec['note'])
 return (f'<figure class="concept-visual" data-visual="{e(spec["kind"])}">'
         f'<figcaption><span>{e(spec.get("label","知识图解"))}</span><strong>{title}</strong></figcaption>'
         f'<svg viewBox="0 0 760 {height}" role="img" aria-label="{title}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'
         f'<p class="concept-visual-note">{note}</p></figure>')


def _wrap_label(value,max_units):
 """Wrap SVG labels by approximate glyph width; CJK glyphs use two units."""
 lines=[]
 for segment in value.split('|'):
  current='';width=0
  for char in segment:
   size=2 if east_asian_width(char) in 'FWA' else 1
   if current and width+size>max_units:
    lines.append(current);current='';width=0
   current+=char;width+=size
  if current:lines.append(current)
 return lines or ['']


def flow(spec):
 nodes=spec['nodes'];n=len(nodes);gap=18;x0=26;boxw=(760-52-(n-1)*gap)/n
 body=''
 for i,label in enumerate(nodes):
  x=x0+i*(boxw+gap);lines=_wrap_label(label,max(9,int((boxw-18)/8)))
  body+=rect(round(x,1),70,round(boxw,1),112,'var(--viz-blue-bg)' if i%2==0 else 'var(--viz-green-bg)','var(--viz-blue)' if i%2==0 else 'var(--viz-green)')
  for j,line in enumerate(lines):body+=text(round(x+boxw/2,1),130+(j-(len(lines)-1)/2)*22,line,16)
  if i<n-1:body+=arrow(round(x+boxw+2,1),126,round(x+boxw+gap-3,1),126)
 return figure(spec,body,250)


def plot(spec):
 kind=spec['kind'];left=60;right=718;top=33;bottom=238
 if kind=='isotherm':
  domain=(.8,4);yrange=(0,3.2);series=[('T₂ 较高',lambda x:2.15/x,'var(--viz-blue)'),('T₁ 较低',lambda x:1.35/x,'var(--viz-orange)')];xlabel='体积 V';ylabel='压强 p'
 elif kind=='sho':
  domain=(0,4*pi);yrange=(-1.2,1.2);series=[('位移 x',lambda x:sin(x),'var(--viz-blue)'),('速度 v',lambda x:cos(x),'var(--viz-green)'),('加速度 a',lambda x:-sin(x),'var(--viz-orange)')];xlabel='时间 t';ylabel='归一化量'
 elif kind=='damping':
  domain=(0,13);yrange=(-1.15,1.15);series=[('欠阻尼位移',lambda x:exp(-.16*x)*cos(3*x),'var(--viz-blue)'),('上包络',lambda x:exp(-.16*x),'var(--viz-orange)'),('下包络',lambda x:-exp(-.16*x),'var(--viz-orange)')];xlabel='时间 t';ylabel='位移 x'
 elif kind=='resonance':
  domain=(0,2.5);yrange=(0,5.2);series=[('阻尼较小',lambda r:min(5,1/sqrt((1-r*r)**2+(.24*r)**2)),'var(--viz-blue)'),('阻尼较大',lambda r:1/sqrt((1-r*r)**2+(.66*r)**2),'var(--viz-orange)')];xlabel='驱动角频率 / 固有角频率';ylabel='相对振幅'
 elif kind=='beats':
  domain=(0,18*pi);yrange=(-2.2,2.2);series=[('合成振动',lambda x:2*cos(.09*x)*sin(x),'var(--viz-blue)'),('振幅包络',lambda x:2*abs(cos(.09*x)),'var(--viz-orange)'),('下包络',lambda x:-2*abs(cos(.09*x)),'var(--viz-orange)')];xlabel='时间 t';ylabel='位移 x'
 elif kind=='energy':
  domain=(0,2*pi);yrange=(0,1.2);series=[('动能 Eₖ',lambda x:sin(x)**2,'var(--viz-blue)'),('势能 Eₚ',lambda x:cos(x)**2,'var(--viz-orange)'),('总能量 E',lambda x:1,'var(--viz-green)')];xlabel='时间 t';ylabel='相对能量'
 elif kind=='damping_modes':
  def over(x):return (-2*exp(-.3*x)+.3*exp(-2*x))/(-1.7)
  domain=(0,8);yrange=(-.62,1.12);series=[('欠阻尼',lambda x:exp(-.35*x)*(cos(2.1*x)+.35/2.1*sin(2.1*x)),'var(--viz-blue)'),('临界阻尼',lambda x:(1+x)*exp(-x),'var(--viz-green)'),('过阻尼',over,'var(--viz-orange)')];xlabel='时间 t';ylabel='归一化位移'
 elif kind=='kinetic_temperature':
  domain=(0,800);yrange=(0,18);series=[('平均平动动能',lambda t:1.5*1.380649e-23*t/1e-21,'var(--viz-blue)')];xlabel='温度 T（K）';ylabel='能量（10⁻²¹ J）'
 elif kind=='rms_temperature':
  domain=(0,800);yrange=(0,3300);series=[('H₂',lambda t:sqrt(3*8.314*t/.002),'var(--viz-blue)'),('N₂',lambda t:sqrt(3*8.314*t/.028),'var(--viz-orange)')];xlabel='温度 T（K）';ylabel='方均根速率（m/s）'
 elif kind=='three_speeds':
  domain=(0,800);yrange=(0,850);series=[('最概然速率',lambda t:sqrt(2*8.314*t/.032),'var(--viz-orange)'),('平均速率',lambda t:sqrt(8*8.314*t/(pi*.032)),'var(--viz-green)'),('方均根速率',lambda t:sqrt(3*8.314*t/.032),'var(--viz-blue)')];xlabel='温度 T（K）';ylabel='O₂ 速率（m/s）'
 elif kind=='barometric':
  domain=(0,20);yrange=(0,1.05);series=[('300 K',lambda z:exp(-.029*9.81*z*1000/(8.314*300)),'var(--viz-blue)'),('600 K',lambda z:exp(-.029*9.81*z*1000/(8.314*600)),'var(--viz-orange)')];xlabel='高度 z（km）';ylabel='相对数密度 n/n₀'
 elif kind=='mean_free_path':
  const=1.380649e-23/(sqrt(2)*pi*(.37e-9)**2)
  domain=(20,200);yrange=(0,750);series=[('300 K',lambda p:const*300/(p*1000)*1e9,'var(--viz-blue)'),('600 K',lambda p:const*600/(p*1000)*1e9,'var(--viz-orange)')];xlabel='压强 p（kPa）';ylabel='平均自由程（nm）'
 elif kind=='isochore':
  domain=(0,600);yrange=(0,2.15);series=[('V 不变：p ∝ T',lambda t:t/300,'var(--viz-blue)')];xlabel='温度 T（K）';ylabel='相对压强 p/p₀'
 elif kind=='isobar':
  domain=(0,600);yrange=(0,2.15);series=[('p 不变：V ∝ T',lambda t:t/300,'var(--viz-green)')];xlabel='温度 T（K）';ylabel='相对体积 V/V₀'
 elif kind=='adiabat':
  domain=(.7,2.5);yrange=(0,1.75);series=[('等温 pV=常量',lambda v:1/v,'var(--viz-blue)'),('绝热 pVᵞ=常量',lambda v:1/v**1.4,'var(--viz-orange)')];xlabel='相对体积 V/V₀';ylabel='相对压强 p/p₀'
 elif kind=='polytropic':
  domain=(.7,2.5);yrange=(0,2);series=[('n=0：等压',lambda v:1,'var(--viz-green)'),('n=1：等温',lambda v:1/v,'var(--viz-blue)'),('n=1.4：多方',lambda v:1/v**1.4,'var(--viz-orange)')];xlabel='相对体积 V/V₀';ylabel='相对压强 p/p₀'
 elif kind=='cop':
  domain=(.1,.9);yrange=(0,10);series=[('可逆制冷系数',lambda r:r/(1-r),'var(--viz-blue)')];xlabel='温度比 T꜀/Tₕ';ylabel='制冷系数 ε'
 elif kind=='entropy_volume':
  domain=(.5,4);yrange=(-.85,1.55);series=[('等温理想气体',lambda r:__import__('math').log(r),'var(--viz-blue)')];xlabel='体积比 V₂/V₁';ylabel='熵变 ΔS/(νR)'
 elif kind=='hooke_line':
  domain=(-2,2);yrange=(-2.3,2.3);series=[('回复力 F=-kx',lambda x:-x,'var(--viz-blue)')];xlabel='相对位移 x';ylabel='相对回复力 F'
 elif kind=='omega_k':
  domain=(.25,4);yrange=(0,2.25);series=[('ω ∝ √k',lambda k:sqrt(k),'var(--viz-blue)')];xlabel='刚度比 k/k₀';ylabel='角频率比 ω/ω₀'
 elif kind=='pendulum_period':
  domain=(.25,4);yrange=(0,2.25);series=[('T ∝ √L',lambda length:sqrt(length),'var(--viz-green)')];xlabel='摆长比 L/L₀';ylabel='周期比 T/T₀'
 elif kind=='phase_lag':
  atan2=__import__('math').atan2
  domain=(0,2.5);yrange=(0,3.3);series=[('阻尼较小',lambda r:atan2(.3*r,1-r*r),'var(--viz-blue)'),('阻尼较大',lambda r:atan2(.8*r,1-r*r),'var(--viz-orange)')];xlabel='驱动频率 / 固有频率';ylabel='相位滞后 δ（rad）'
 elif kind=='resultant_amplitude':
  domain=(0,pi);yrange=(0,2.2);series=[('等振幅叠加',lambda delta:2*cos(delta/2),'var(--viz-blue)')];xlabel='相位差 Δφ（0 至 π）';ylabel='合振幅 / 单个振幅'
 elif kind=='carnot_efficiency':
  domain=(0,.9);yrange=(0,1.05);series=[('η=1−T꜀/Tₕ',lambda r:1-r,'var(--viz-blue)')];xlabel='冷/热源温度比';ylabel='可逆效率 η'
 else:raise ValueError(kind)
 xmin,xmax=domain;ymin,ymax=yrange
 X=lambda x:left+(x-xmin)/(xmax-xmin)*(right-left)
 Y=lambda y:bottom-(y-ymin)/(ymax-ymin)*(bottom-top)
 def tick(v):
  return f'{v:.0f}' if abs(v)>=20 else f'{v:.2f}'.rstrip('0').rstrip('.')
 body=''
 for i in range(5):
  y=top+i*(bottom-top)/4
  body+=f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="var(--border)" stroke-width="1"/>'
  body+=text(left-7,round(y+4,1),tick(ymax-i*(ymax-ymin)/4),11,'end','var(--soft)',500)
 body+=f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="var(--soft)" stroke-width="1.7"/>'
 body+=f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="var(--soft)" stroke-width="1.7"/>'
 for i in range(5):
  x=xmin+i*(xmax-xmin)/4
  body+=text(round(X(x),1),258,tick(x),11,'middle','var(--soft)',500)
 body+=text(27,29,ylabel,12,'start','var(--soft)',500)+text(715,269,xlabel,12,'end','var(--soft)',500)
 for i,(label,fn,color) in enumerate(series):
  points=[]
  for k in range(241):
   x=xmin+(xmax-xmin)*k/240
   points.append(f'{X(x):.1f},{Y(fn(x)):.1f}')
  dash=' stroke-dasharray="6 5"' if label in ('上包络','下包络','振幅包络') else ''
  body+=f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="2.5"{dash}/>'
  legendx=left+i*210
  body+=f'<line x1="{legendx}" y1="{287}" x2="{legendx+24}" y2="287" stroke="{color}" stroke-width="3"/>'+text(legendx+30,291,label,12,'start','var(--soft)',500)
 return figure(spec,body,310)


def truth_table(spec):
 columns=spec['columns'];rows=spec['rows'];highlight=set(spec.get('highlight',[]));n=len(columns)
 x0=32;y0=32;w=696/n;rh=43
 body=''
 for j,label in enumerate(columns):
  x=x0+j*w
  body+=rect(round(x,1),y0,round(w,1),rh,'var(--viz-blue-bg)','var(--border)',0)
  body+=text(round(x+w/2,1),y0+27,label,13)
 for i,row in enumerate(rows):
  y=y0+(i+1)*rh
  for j,value in enumerate(row):
   fill='var(--viz-green-bg)' if i in highlight else 'var(--paper)'
   body+=rect(round(x0+j*w,1),y,round(w,1),rh,fill,'var(--border)',0)
   body+=text(round(x0+(j+.5)*w,1),y+27,value,14,color='var(--text)',weight=600 if i in highlight else 500)
 return figure(spec,body,y0+(len(rows)+1)*rh+20)


def trace(spec):
 """A sequence of concrete states, useful for data-structure operations."""
 rows=spec['rows'];count=max(len(cells) for _,cells in rows)
 if count>8 or len(rows)>5:raise ValueError('trace exceeds SVG bounds')
 cellw=min(82,(620-15*(count-1))/count);x0=138;body=''
 for j,(caption,cells) in enumerate(rows):
  y=26+j*61
  body+=text(125,y+34,caption,13,'end','var(--soft)',600)
  for i,cell in enumerate(cells):
   x=x0+i*(cellw+15)
   highlight=str(cell).startswith('*')
   value=str(cell).lstrip('*')
   body+=rect(round(x,1),y,round(cellw,1),44,'var(--viz-green-bg)' if highlight else 'var(--viz-blue-bg)','var(--viz-green)' if highlight else 'var(--viz-blue)',5)
   body+=text(round(x+cellw/2,1),y+29,value,15)
  if j<len(rows)-1:body+=arrow(742,y+19,742,y+58,'var(--viz-orange)')
 html=figure(spec,body,45+len(rows)*61)
 if spec.get('static_only'):return html
 payload=e(dumps(rows,ensure_ascii=False,separators=(',',':')))
 html=html.replace('class="concept-visual"',f'class="concept-visual trace-widget" data-rows="{payload}"',1)
 controls='<div class="trace-controls"><button type="button" data-step="prev">上一步</button><span class="trace-progress"></span><button type="button" data-step="next">下一步</button></div><p class="trace-explanation" aria-live="polite"></p>'
 return html.replace('<p class="concept-visual-note">',controls+'<p class="concept-visual-note">',1)


def matrix(spec):
 rows=spec['rows'];n=len(rows);m=len(rows[0]);highlights={tuple(x) for x in spec.get('highlight',[])}
 if n>6 or m>7 or any(len(row)!=m for row in rows):raise ValueError('matrix dimensions')
 cw=min(73,450/m);ch=42;x0=(760-m*cw)/2;y0=32;body=''
 for i,row in enumerate(rows):
  for j,value in enumerate(row):
   color=(i,j) in highlights;x=x0+j*cw;y=y0+i*ch
   body+=rect(round(x,1),y,round(cw,1),ch,'var(--viz-green-bg)' if color else 'var(--paper)','var(--viz-green)' if color else 'var(--border)',0)
   body+=text(round(x+cw/2,1),y+28,value,15)
 body+=text(380,y0+n*ch+30,spec.get('bottom',''),14,color='var(--soft)',weight=500)
 return figure(spec,body,y0+n*ch+58)


def equivalence(spec):
 left=spec['left'];right=spec['right'];body=''
 body+=rect(34,67,290,95,'var(--viz-blue-bg)','var(--viz-blue)',10)
 body+=rect(436,67,290,95,'var(--viz-green-bg)','var(--viz-green)',10)
 body+=text(179,124,left,19)+text(581,124,right,19)
 body+=text(380,125,'⇔',32,color='var(--viz-orange)')
 body+=text(380,210,spec.get('detail','所有赋值下结果相同'),14,color='var(--soft)',weight=500)
 return figure(spec,body,245)


def inference(spec):
 premises=spec['premises'];body='';n=len(premises);w=min(280,(690-(n-1)*30)/n);start=(760-(n*w+(n-1)*30))/2
 for i,p in enumerate(premises):
  x=start+i*(w+30)
  body+=rect(round(x,1),32,round(w,1),70,'var(--viz-blue-bg)','var(--viz-blue)',9)
  body+=text(round(x+w/2,1),77,p,18)
 body+='<line x1="140" y1="143" x2="620" y2="143" stroke="var(--viz-orange)" stroke-width="2.5"/>'
 body+=text(380,135,spec.get('rule','推理规则'),13,color='var(--soft)',weight=500)
 body+=rect(275,176,210,63,'var(--viz-green-bg)','var(--viz-green)',9)
 body+=text(380,216,spec['conclusion'],20)
 return figure(spec,body,275)


def _cell_row(labels,y,x0=80,width=88,highlight=-1):
 body=''
 for i,label in enumerate(labels):
  x=x0+i*width
  body+=rect(x,y,width-5,54,'var(--viz-green-bg)' if i==highlight else 'var(--viz-blue-bg)','var(--viz-green)' if i==highlight else 'var(--viz-blue)',5)
  body+=text(x+(width-5)/2,y+34,label,17)
 return body


def schematic(spec):
 kind=spec['kind'];body=''
 if kind=='work_area':
  body+='<path d="M115 235 L115 103 C240 112 374 145 590 190 L590 235 Z" fill="var(--viz-blue-bg)" stroke="none"/>'
  body+='<path d="M115 103 C240 112 374 145 590 190" fill="none" stroke="var(--viz-blue)" stroke-width="3"/>'
  body+=arrow(82,235,82,35)+arrow(82,235,675,235)
  body+=text(93,45,'p',17,'start')+text(673,260,'V',17,'end')+text(115,256,'V₁',13)+text(590,256,'V₂',13)
  body+=text(342,199,'体积功 W = ∫p dV',19,color='var(--viz-blue)')
  return figure(spec,body,285)
 if kind=='ts_area':
  body+=rect(144,95,410,140,'var(--viz-green-bg)','var(--viz-green)',0)
  body+=arrow(82,235,82,35)+arrow(82,235,675,235)
  body+=text(92,45,'T',17,'start')+text(674,259,'S',17,'end')+text(123,99,'T₀',14,'end')
  body+=text(144,257,'S₁',13)+text(554,257,'S₂',13)+text(349,174,'Qᵣₑᵥ = ∫T dS',20,color='var(--viz-green)')
  return figure(spec,body,285)
 if kind=='pv_cycle':
  body+='<rect x="190" y="72" width="350" height="150" fill="var(--viz-blue-bg)" stroke="var(--viz-blue)" stroke-width="3"/>'
  body+=arrow(82,235,82,35)+arrow(82,235,675,235)
  body+=text(96,45,'p',17,'start')+text(670,258,'V',17,'end')
  body+=text(365,122,'→ 等压膨胀',16,color='var(--viz-blue)')+text(365,217,'← 等压压缩',16,color='var(--viz-blue)')
  body+=text(365,162,'净功 = 包围面积',19,color='var(--viz-blue)')
  return figure(spec,body,285)
 if kind=='phasor_add':
  body+=arrow(145,225,350,100,'var(--viz-blue)')+arrow(350,100,615,170,'var(--viz-orange)')+arrow(145,225,615,170,'var(--viz-green)')
  body+=text(249,150,'A₁',17,color='var(--viz-blue)')+text(492,116,'A₂',17,color='var(--viz-orange)')+text(385,226,'合矢量 A',18,color='var(--viz-green)')
  body+=text(380,271,'同频振动可用旋转矢量的首尾相接法合成',14,color='var(--soft)',weight=500)
  return figure(spec,body,295)
 if kind=='springs':
  for x,title,formula in [(130,'串联','1/kₑ=1/k₁+1/k₂'),(485,'并联','kₑ=k₁+k₂')]:
   body+=rect(x,44,255,177,'var(--viz-blue-bg)' if x==130 else 'var(--viz-green-bg)','var(--viz-blue)' if x==130 else 'var(--viz-green)',12)
   body+=text(x+127,86,title,22)+text(x+127,130,'弹簧 1 + 弹簧 2',15)+text(x+127,181,formula,17)
  return figure(spec,body,266)
 if kind=='phase_portrait':
  cx=380;cy=143;rx=182;ry=92
  body+=f'<line x1="95" y1="{cy}" x2="670" y2="{cy}" stroke="var(--soft)" stroke-width="1.5"/>'
  body+=f'<line x1="{cx}" y1="24" x2="{cx}" y2="263" stroke="var(--soft)" stroke-width="1.5"/>'
  points=' '.join(f'{cx+rx*cos(2*pi*i/240):.1f},{cy+ry*sin(2*pi*i/240):.1f}' for i in range(241))
  body+=f'<polyline points="{points}" fill="none" stroke="var(--viz-blue)" stroke-width="3"/>'
  body+=text(676,139,'位移 x',14,'start','var(--soft)',500)+text(385,29,'速度 v',14,'start','var(--soft)',500)
  body+=text(380,283,'无阻尼简谐振动：归一化的 x–v 轨迹闭合',13,color='var(--soft)',weight=500)
  return figure(spec,body,311)
 if kind=='rotating_vector':
  cx=270;cy=155;r=93;a=-.7;ex=cx+r*cos(a);ey=cy+r*sin(a)
  body+=f'<line x1="95" y1="{cy}" x2="650" y2="{cy}" stroke="var(--soft)" stroke-width="1.5"/>'
  body+=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="var(--border)" stroke-width="1.6"/>'
  body+=f'<line x1="{cx}" y1="{cy}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="var(--viz-blue)" stroke-width="3"/>'
  body+=f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="5" fill="var(--viz-blue)"/>'
  body+=f'<line x1="{ex:.1f}" y1="{ey:.1f}" x2="{ex:.1f}" y2="{cy}" stroke="var(--viz-orange)" stroke-dasharray="5 5" stroke-width="2"/>'
  body+=text(266,135,'θ',17)+text(357,112,'旋转矢量 A',15,'start','var(--viz-blue)')
  body+=text(518,120,'投影随角度变化',17)+text(518,154,'x = A cos θ',20,color='var(--viz-orange)')
  return figure(spec,body,289)
 if kind=='lissajous':
  for j,(delta,label) in enumerate([(0,'同相：斜线'),(pi/2,'相差 π/2：圆'),(pi,'反相：反斜线')]):
   cx=132+j*248;cy=150;r=75
   body+=f'<line x1="{cx-r-10}" y1="{cy}" x2="{cx+r+10}" y2="{cy}" stroke="var(--border)"/>'
   body+=f'<line x1="{cx}" y1="{cy-r-10}" x2="{cx}" y2="{cy+r+10}" stroke="var(--border)"/>'
   points=' '.join(f'{cx+r*sin(2*pi*i/240):.1f},{cy-r*sin(2*pi*i/240+delta):.1f}' for i in range(241))
   body+=f'<polyline points="{points}" fill="none" stroke="var(--viz-blue)" stroke-width="2.8"/>'
   body+=text(cx,263,label,13,color='var(--soft)',weight=500)
  return figure(spec,body,296)
 if kind=='carnot_cycle':
  cards=[(84,40,'高温等温膨胀','吸热 Qₕ'),(443,40,'绝热膨胀','温度下降'),(443,177,'低温等温压缩','放热 Q꜀'),(84,177,'绝热压缩','温度上升')]
  for i,(x,y,heading,sub) in enumerate(cards):
   body+=rect(x,y,234,82,'var(--viz-blue-bg)' if i%2==0 else 'var(--viz-green-bg)','var(--viz-blue)' if i%2==0 else 'var(--viz-green)',11)
   body+=text(x+117,y+35,heading,17)+text(x+117,y+61,sub,13,color='var(--soft)',weight=500)
  body+=arrow(320,81,438,81)+arrow(560,127,560,172)+arrow(439,218,323,218)+arrow(200,171,200,128)
  return figure(spec,body,298)
 if kind=='array_insert':
  body+=text(25,67,'插入前',14,'start','var(--soft)')+_cell_row(['A','B','C','D','空'],38,110)
  body+=text(25,182,'插入后',14,'start','var(--soft)')+_cell_row(['A','X','B','C','D'],153,110,highlight=1)
  for i in (1,2,3):body+=f'<path d="M{110+i*88+38} 98 L{110+(i+1)*88+38} 145" stroke="var(--viz-orange)" stroke-width="2" fill="none"/>'
  body+=text(593,129,'原有元素右移',13,'end','var(--soft)',500)
  return figure(spec,body,245)
 if kind=='linked_list':
  body+=text(55,75,'头指针',14,'start','var(--soft)')+arrow(103,83,151,83)
  for i,label in enumerate(['A','B','C']):
   x=155+i*180
   body+=rect(x,52,130,65,'var(--viz-blue-bg)','var(--viz-blue)',7)
   body+=f'<line x1="{x+83}" y1="52" x2="{x+83}" y2="117" stroke="var(--viz-blue)"/>'
   body+=text(x+42,93,label,18)+text(x+107,93,'→' if i<2 else '∅',18)
   if i<2:body+=arrow(x+132,85,x+175,85)
  body+=text(380,183,'结点 = 数据域 + 指针域；空间不必连续',16)
  return figure(spec,body,225)
 if kind=='stack_queue':
  body+=text(185,38,'栈：后进先出',18)+text(564,38,'队列：先进先出',18)
  for i,label in enumerate(['C','B','A']):body+=rect(142,58+i*55,88,48,'var(--viz-blue-bg)','var(--viz-blue)',5)+text(186,89+i*55,label)
  body+=text(270,85,'栈顶 ↔',13,'start','var(--soft)',500)
  body+=_cell_row(['A','B','C'],105,432,89)
  body+=text(428,199,'队头',13,'start','var(--soft)',500)+text(694,199,'队尾',13,'end','var(--soft)',500)
  return figure(spec,body,237)
 if kind=='circular_queue':
  for i in range(8):
   a=-pi/2+2*pi*i/8;x=380+103*cos(a);y=148+103*sin(a)
   body+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="26" fill="{"var(--viz-green-bg)" if 1<=i<=4 else "var(--viz-blue-bg)"}" stroke="var(--viz-blue)" stroke-width="1.7"/>'
   body+=text(round(x,1),round(y+6,1),str(i),15)
  body+=text(380,151,'循环复用',18)+text(380,176,'数组空间',13,color='var(--soft)',weight=500)
  body+=text(610,77,'front → 1',15,'start','var(--viz-green)')+text(610,109,'rear → 5',15,'start','var(--viz-orange)')
  body+=text(52,273,'示意：元素占用 1–4，rear 指向下一个可写位置。',13,'start','var(--soft)',500)
  return figure(spec,body,303)
 if kind=='bf_match':
  body+=text(70,48,'主串',14,'start','var(--soft)')+_cell_row(list('ABABC'),20,153,76)
  for step,shift in enumerate((0,1,2)):
   y=87+step*70
   body+=text(70,y+34,f'对齐 {step+1}',14,'start','var(--soft)')+_cell_row(list('ABC'),y,153+shift*76,76,highlight=2 if step==2 else -1)
  return figure(spec,body,315)
 if kind=='prefix_border':
  body+=text(87,52,'模式串',15,'start','var(--soft)')+_cell_row(list('ABAB'),20,238,70)
  body+=text(87,143,'真前缀',15,'start','var(--soft)')+_cell_row(list('AB'),111,238,70,highlight=0)
  body+=text(87,229,'真后缀',15,'start','var(--soft)')+_cell_row(list('AB'),197,378,70,highlight=0)
  body+=text(602,171,'共同边界：AB',15,'start','var(--viz-green)')
  return figure(spec,body,282)
 if kind=='row_major':
  body+=text(194,37,'二维数组',17)
  for i,row in enumerate((['a₀₀','a₀₁','a₀₂'],['a₁₀','a₁₁','a₁₂'])):body+=_cell_row(row,57+i*65,75,81)
  body+=arrow(344,124,418,124)
  body+=text(584,38,'顺序存储',17)
  body+=_cell_row(['a₀₀','a₀₁','a₀₂','a₁₀','a₁₁','a₁₂'],96,420,51)
  body+=text(380,228,'先存完第 0 行，再存第 1 行：LOC(aᵢⱼ) = LOC(a₀₀) + (i·列数+j)·元素大小',13,color='var(--soft)',weight=500)
  return figure(spec,body,255)
 if kind=='sparse':
  body+=text(205,34,'稀疏矩阵',17)
  matrix=[['0','5','0'],['0','0','3'],['7','0','0']]
  for i,row in enumerate(matrix):body+=_cell_row(row,50+i*56,74,82,highlight=1 if i==0 else 2 if i==1 else 0)
  body+=arrow(341,133,430,133)
  body+=text(573,34,'三元组 (行, 列, 值)',17)
  for i,row in enumerate(['(0, 1, 5)','(1, 2, 3)','(2, 0, 7)']):body+=rect(467,51+i*56,217,44,'var(--viz-green-bg)','var(--viz-green)',6)+text(575,79+i*56,row,15)
  return figure(spec,body,260)
 if kind=='generalized_list':
  nodes=[(380,48,'L = (a,(b,c),d)'),(160,150,'a'),(380,150,'(b,c)'),(600,150,'d'),(312,249,'b'),(448,249,'c')]
  for x1,y1,x2,y2 in [(380,64,160,134),(380,64,380,134),(380,64,600,134),(380,166,312,233),(380,166,448,233)]:body+=f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="var(--viz-blue)" stroke-width="2"/>'
  for x,y,label in nodes:
   w=174 if x==380 and y==48 else 100
   body+=rect(x-w/2,y-23,w,46,'var(--viz-green-bg)' if label=='(b,c)' else 'var(--viz-blue-bg)','var(--viz-green)' if label=='(b,c)' else 'var(--viz-blue)',23)+text(x,y+6,label,15)
  return figure(spec,body,308)
 raise ValueError(kind)


def proof(spec):
 kind=spec['kind'];body=''
 if kind=='modus_ponens':
  premises=['P','P → Q'];conclusion='Q';rule='→ 消去 / 肯定前件'
 elif kind=='conditional_proof':
  premises=['[P] 临时假设','⋮  推导出 Q'];conclusion='P → Q';rule='解除假设（CP）'
 elif kind=='contradiction':
  premises=['[¬P] 临时假设','⋮  推导出 ⊥'];conclusion='P';rule='反证法'
 else:raise ValueError(kind)
 for i,label in enumerate(premises):
  x=108+i*291
  body+=rect(x,51,245,66,'var(--viz-blue-bg)','var(--viz-blue)',9)+text(x+122,92,label,17)
 body+=f'<line x1="165" y1="161" x2="595" y2="161" stroke="var(--viz-blue)" stroke-width="2.4"/>'
 body+=text(380,149,rule,13,color='var(--soft)',weight=500)
 body+=rect(287,183,186,58,'var(--viz-green-bg)','var(--viz-green)',9)+text(380,220,conclusion,20)
 return figure(spec,body,276)


def S(match,kind,title,note,**kwargs):
 return {'match':match,'kind':kind,'title':title,'note':note,**kwargs}


SPECS={
 'physics/12 气体动理论.md':[
  S('2.2.2 压强公式','flow','从微观碰撞到压强','大量分子碰撞器壁的统计平均，连接微观运动与宏观压强。',nodes=['分子碰撞器壁','动量变化','单位面积|平均冲力','宏观压强 p']),
  S('2.3.1 温度与平均平动动能','kinetic_temperature','温度与分子平均平动动能','按〈εₖ〉=3kT/2 绘制；零点对应绝对零度。'),
  S('2.3.3 方均根速率','rms_temperature','分子方均根速率随温度变化','按 √(3RT/M) 绘制；同温下摩尔质量较小的气体速率较大。'),
  S('2.4.2 能量均分定理','flow','自由度与理想气体内能','每个二次型自由度平均分得 ½kT；具有 i 个自由度时，理想气体内能为 iνRT/2。',nodes=['分子自由度 i','每自由度|½kT','单分子平均能量|i·kT/2','气体内能|i·νRT/2']),
  S('3.2.3 三种统计速率','three_speeds','三种统计速率的温度关系','以 O₂ 为例；三者都随 √T 增长，方均根速率最大。'),
  S('3.3.2 玻尔兹曼密度分布','barometric','重力场中数密度随高度衰减','以空气摩尔质量 29 g/mol 为例；假设等温大气，显示归一化数密度。'),
  S('4.1.2 公式','mean_free_path','平均自由程随压强变化','按硬球模型 λ=kT/(√2πd²p) 绘制；示例取分子直径 0.37 nm。'),
 ],
 'physics/13 热力学基础｜知识体系重构版.md':[
  S('1.5 体积功的计算','work_area','p–V 曲线下面积表示体积功','准静态过程中 W=∫p dV；不同路径下的面积可不同。'),
  S('1.9 摩尔定体与定压热容','flow','定压与定体热容的差别','理想气体定压升温时还要对外做膨胀功，因此 Cₚ=Cᵥ+R。',nodes=['同样升温 ΔT','定体：不做体积功','定压：额外膨胀功','Cₚ = Cᵥ + R']),
  S('2.2 体积固定：等体过程','isochore','等体过程中压强与温度','理想气体体积固定，压强与热力学温度成正比。'),
  S('2.3 压强固定：等压过程','isobar','等压过程中体积与温度','理想气体压强固定，体积与热力学温度成正比。'),
  S('2.4 温度固定：等温过程','isotherm','等温线的 p–V 关系','理想气体等温过程满足 pV 为常量；较高温度对应较高的等温线。'),
  S('2.5.3 可逆绝热线与等温线的比较','adiabat','同一起点的绝热线与等温线','γ=1.4 示意；膨胀时绝热线下降更快，压缩时上升更快。'),
  S('2.6 多方过程','polytropic','多方指数改变 p–V 曲线','统一写为 pVⁿ=常量；n=0 为等压，n=1 为等温。'),
  S('3.1 循环的结构','pv_cycle','p–V 循环围成面积表示净功','顺时针循环的面积对应系统对外做的净功；矩形仅作几何示意。'),
  S('5.1 卡诺循环为什么','carnot_cycle','卡诺循环的四个可逆过程','循环依次经历高温等温膨胀、绝热膨胀、低温等温压缩、绝热压缩。'),
  S('5.3 卡诺效率只依赖热源温度','carnot_efficiency','卡诺效率与冷热源温度比','η=1−T꜀/Tₕ，温度须使用 K；此处展示可逆上限。'),
  S('5.4 反向运行','cop','可逆制冷系数与温度比','ε=T꜀/(Tₕ−T꜀)；接近等温时系数增大。'),
  S('6.4 理想气体三种熵变公式','entropy_volume','等温过程的熵变与体积比','等温理想气体 ΔS=νR ln(V₂/V₁)；膨胀为正，压缩为负。'),
  S('6.8 熵增原理','flow','熵增判据看总体系','判断自发过程的方向时，要考虑系统与环境组成的孤立总体系。',nodes=['系统 + 环境','孤立总体系','自发不可逆过程','总熵不减']),
  S('6.9 ','ts_area','T–S 图中的可逆热量','可逆过程中 δQᵣₑᵥ=T dS；等温过程的面积为 TΔS。'),
 ],
 'physics/14 振动 扩充版.md':[
  S('1. 线性回复力与运动微分方程','hooke_line','回复力与位移的线性关系','胡克定律 F=−kx；负号表示回复力总指向平衡位置。'),
  S('2. 弹簧振子的固有频率与周期','omega_k','弹簧刚度与固有角频率','固定质量时 ω=√(k/m)，刚度提高四倍则角频率提高两倍。'),
  S('3. 单摆的小角度振动','pendulum_period','单摆周期与摆长','小角度近似下 T=2π√(L/g)；摆长增为四倍时周期增为两倍。'),
  S('1. 弹簧分段、串联、并联','springs','弹簧串联与并联的等效刚度','串联柔度相加，并联刚度相加；图中是线性弹簧模型。'),
  S('1.2 稳态响应的相位为什么会落后于驱动力','phase_lag','受迫振动的相位滞后','按 δ=atan2(2ζr,1−r²) 绘制；相位跨过共振区由近 0 趋向 π。'),
  S('1. 合成原理与旋转矢量加法','phasor_add','旋转矢量首尾相接','同频振动的合成可转化为矢量相加；相位差决定合矢量长度。'),
  S('2. 同相、反相与一般相位差','resultant_amplitude','等振幅同频叠加的合振幅','两分振动振幅相同且相位差为 Δφ 时，合振幅为 2A|cos(Δφ/2)|。'),
 ],
 'data-structures/GPT02 数据结构第二章：线性表.md':[
  S('2.4 插入：后面的元素向右移动','array_insert','顺序表插入时的元素移动','在 B 前插入 X 时，原有元素从后向前右移，为新元素腾出连续空间。'),
  S('3. 单链表：用指针连接结点','linked_list','单链表由指针连接结点','每个结点含数据域与指针域；结点在内存中无须连续。'),
 ],
 'data-structures/GPT03数据结构第三章：栈和队列.md':[
  S('1.2 两种结构的直观示意','stack_queue','栈与队列的访问方向','栈只在栈顶进出，后进先出；队列从队尾进入、队头离开，先进先出。'),
  S('7.3 中缀表达式转后缀表达式','flow','中缀转后缀的处理路径','操作数直接输出；运算符根据优先级入栈或弹出，最后得到后缀表达式。',nodes=['读取中缀符号','操作数直接输出','运算符按优先级|入栈或弹出','得到后缀表达式']),
  S('12.1 循环队列的核心思想','circular_queue','循环队列复用数组空间','下标到达数组末尾后回绕到开头；图中 front 指队头，rear 指向下一个可写位置。'),
 ],
 'data-structures/GPT04 数据结构第四章：串.md':[
  S('7.1 BF算法的基本思想','bf_match','BF 模式匹配逐位尝试','主串 ABABC 与模式 ABC：从左到右依次对齐，前两次失配，第三次匹配成功。'),
  S('九、KMP：为什么失配时主串指针可以不回退','flow','KMP 失配后的处理','利用模式串已有的前后缀信息移动模式串；主串扫描位置无须回退。',nodes=['已匹配一段前缀','出现失配','查询可复用的|前后缀信息','移动模式串|主串不回退']),
  S('十、next函数：定义、手工计算、代码实现','prefix_border','共同前后缀决定可复用部分','ABAB 的真前缀与真后缀都含 AB。next 的具体下标约定以正文定义为准。'),
 ],
 'data-structures/GPT05 数据结构第五章：数组和广义表.md':[
  S('2.2 二维数组：行优先地址公式','row_major','二维数组的行优先存储','每一行连续存放，前一行全部元素位于后一行之前。'),
  S('四、稀疏矩阵：存储、转置与链式结构','sparse','只记录稀疏矩阵的非零元','三元组表记录非零元的行、列和值；示意图使用 0-based 下标。'),
  S('五、广义表的定义、基本性质与表头表尾','generalized_list','广义表的嵌套结构','L=(a,(b,c),d) 含三个顶层元素，其中第二个元素本身也是表。'),
 ],
 'discrete-math/GPT01命题逻辑基础：命题、联结词、命题公式与真值表.md':[
  S('三、五种基本逻辑联结词','truth_table','五种基本联结词的真值','1 表示真，0 表示假；蕴涵 P→Q 仅在 P 真而 Q 假时为假。',columns=['P','Q','¬P','P∧Q','P∨Q','P→Q','P↔Q'],rows=[['0','0','1','0','0','1','1'],['0','1','1','0','1','1','0'],['1','0','0','0','1','0','0'],['1','1','0','1','1','1','1']]),
  S('七、真值表的构造与使用','flow','构造真值表的步骤','先枚举全部赋值，再计算子公式与整式，最后按末列判断公式类型。',nodes=['列出变元赋值','计算子公式','得到整式真值','判断重言、矛盾|或可满足']),
 ],
 'discrete-math/GPT02命题逻辑命题公式、逻辑等值式与联结词完备集.md':[
  S('二、逻辑等值式的定义与判定','truth_table','蕴涵式的等值改写','P→Q 与 ¬P∨Q 的每一行真值完全相同，因此二者逻辑等值。',columns=['P','Q','P→Q','¬P∨Q'],rows=[['0','0','1','1'],['0','1','1','1'],['1','0','0','0'],['1','1','1','1']],highlight=[0,1,2,3]),
  S('六、联结词完备集与极小完备集','flow','从 {¬,→} 表达常见联结词','例如 P∨Q = ¬P→Q，P∧Q = ¬(P→¬Q)；由此可构造任意真值函数。',nodes=['¬ 与 →','构造 P∨Q','构造 P∧Q','表达任意|真值函数']),
 ],
 'discrete-math/GPT03命题逻辑-范式：析取范式、合取范式与主范式.md':[
  S('三、极小项与主析取范式','truth_table','从真行写主析取范式','示例函数 P⊕Q 在 01、10 两行取真，因此主析取范式为 (¬P∧Q)∨(P∧¬Q)。',columns=['P','Q','P⊕Q','对应极小项'],rows=[['0','0','0','—'],['0','1','1','¬P∧Q'],['1','0','1','P∧¬Q'],['1','1','0','—']],highlight=[1,2]),
  S('四、极大项与主合取范式','truth_table','从假行写主合取范式','同一示例函数 P⊕Q 在 00、11 两行取假，因此主合取范式为 (P∨Q)∧(¬P∨¬Q)。',columns=['P','Q','P⊕Q','对应极大项'],rows=[['0','0','0','P∨Q'],['0','1','1','—'],['1','0','1','—'],['1','1','0','¬P∨¬Q']],highlight=[0,3]),
 ],
 'discrete-math/GPT04命题逻辑：推理的形式结构与有效性判定.md':[
  S('三、判断推理有效性的基本方法','truth_table','用真值表寻找推理反例','以前提 P 与 P→Q 推出 Q 为例：唯一前提同真的赋值是 P=1、Q=1，此时结论也真。',columns=['P','Q','P→Q','两前提同真','结论 Q'],rows=[['0','0','1','否','0'],['0','1','1','否','1'],['1','0','0','否','0'],['1','1','1','是','1']],highlight=[3]),
  S('五、九条基本推理定律','modus_ponens','肯定前件规则','由 P 与 P→Q，可以有效地推出 Q。'),
 ],
 'discrete-math/GPT05命题逻辑：自然推理系统 P 与演绎证明.md':[
  S('三、自然推理系统','modus_ponens','自然推理中的规则应用','把前提写在线上、结论写在线下，表示一次有效的推理规则应用。'),
  S('七、附加前提证明法（CP 规则）','conditional_proof','附加前提证明的作用域','为证明 P→Q，临时假设 P，推导出 Q，再解除这一临时假设。'),
  S('八、反证法与公式集合的相容性','contradiction','反证法的推理框架','为证明 P，临时假设 ¬P 并导出矛盾，再解除该假设。'),
 ],
}


ASSET_DIAGRAMS={
 '01_位移速度加速度.png':S('','sho','位移、速度和加速度的相位关系','依据本章公式重绘的归一化示意图，非原始配图。速度超前位移四分之一周期，加速度与位移反相。'),
 '07_位移速度相轨迹.png':S('','phase_portrait','简谐振动的位移–速度相轨迹','依据本章公式重绘的示意图，非原始配图。无阻尼情形下轨迹闭合，归一化坐标下可画成圆。'),
 '02_旋转矢量.png':S('','rotating_vector','旋转矢量的投影','依据本章文字重绘的示意图，非原始配图。匀速旋转矢量在坐标轴上的投影呈简谐变化。'),
 '03_能量转化.png':S('','energy','弹簧振子的动能与势能转化','依据本章公式重绘的归一化示意图，非原始配图。无阻尼时动能与势能周期互换，总机械能保持不变。'),
 '08_三种阻尼模式.png':S('','damping_modes','欠阻尼、临界阻尼与过阻尼','依据本章概念重绘的示意图，非原始配图。三条曲线采用相同初始位移与初速度；临界阻尼最快无振荡地回零。'),
 '04_共振曲线.png':S('','resonance','不同阻尼条件下的稳态振幅响应','依据本章公式重绘的归一化示意图，非原始配图。阻尼越小，共振峰越高且越尖锐。'),
 '05_拍现象.png':S('','beats','拍现象与振幅包络','依据本章公式重绘的示意图，非原始配图。频率接近的振动叠加后，振幅缓慢增强与减弱。'),
 '06_垂直同频合成.png':S('','lissajous','垂直同频振动合成的轨迹','依据本章公式重绘的示意图，非原始配图。等振幅同频振动的轨迹随相位差改变。'),
}


def render(spec):
 kind=spec['kind']
 if kind=='flow':return flow(spec)
 if kind=='truth_table':return truth_table(spec)
 if kind=='trace':return trace(spec)
 if kind=='matrix':return matrix(spec)
 if kind=='equivalence':return equivalence(spec)
 if kind=='inference':return inference(spec)
 if kind in {'isotherm','sho','damping','resonance','beats','energy','damping_modes','kinetic_temperature','rms_temperature','three_speeds','barometric','mean_free_path','isochore','isobar','adiabat','polytropic','cop','entropy_volume','hooke_line','omega_k','pendulum_period','phase_lag','resultant_amplitude','carnot_efficiency'}:return plot(spec)
 if kind in {'modus_ponens','conditional_proof','contradiction'}:return proof(spec)
 return schematic(spec)
