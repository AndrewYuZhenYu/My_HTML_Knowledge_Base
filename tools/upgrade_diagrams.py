"""Quantitative and structural replacements for earlier text-box illustrations.

Examples are explicitly labelled. Their equations come from the matching note.
"""
from __future__ import annotations

from math import comb, exp, pi, sqrt, sin
from visuals import arrow, e, figure, rect, text


UPGRADES={
 'physics/12 气体动理论.md':{
  '2.4.1 自由度':('equipartition','每个经典二次型自由度的能量','单原子气体示出三个平动自由度；双原子示意再加入两个转动自由度。','能量分配图'),
  '3.1.1 伽尔顿板实验':('galton','随机偏转的二项分布','默认 p=0.5 时，10 次偏转服从二项分布；调节概率可观察峰的位置变化。柱高是理论值，不是实验实测数据。','统计函数图'),
  '3.1.2 概率分布函数':('maxwell_area','速率区间对应曲线下面积','默认参数为氧气 300 K、速率区间 300–600 m/s；调节参数时，绿色面积与实时概率一同变化。','概率密度图'),
  '4.1.1 两个统计平均量':('collision_path','分子碰撞轨迹与平均自由程','折线路段只作碰撞路径示意；平均自由程是大量相邻碰撞间路程的统计均值。','微观轨迹图'),
 },
 'physics/13 热力学基础｜知识体系重构版.md':{
  '1.3 能量账本':('energy_sankey','第一定律的能量流','示例取吸热 100 J、内能增加 60 J、系统对外做功 40 J，满足 Q=ΔU+A。','能量流图'),
  '6.7 绝热自由膨胀':('free_expansion','绝热自由膨胀的初末状态','自由膨胀不可用准静态 p–V 曲线连接两端；理想气体在绝热条件下 Q=A=ΔU=0。','状态示意图'),
 },
 'physics/14 振动 扩充版.md':{
  '2.1 完整周期中的状态变化':('phase_timeline','一个周期内的位移与速度','以 x=A cos(ωt) 为例；端点速度为零，经过平衡位置时速度大小最大。','相位函数图'),
 },
 'data-structures/GPT02 数据结构第二章：线性表.md':{
  '3.4 插入：先找前驱':('linked_insert','单链表插入的指针改接','先令 e.next=q，再令 p.next=e；图中展示前后连接状态。','指针演示'),
  '3.5 删除：摘下结点':('linked_delete','单链表删除的指针改接','令 p.next=q.next，随后释放 q；图中展示连接从 p→q→r 变为 p→r。','指针演示'),
  '7.1 基本操作复杂度对照':('complexity','规模增长与访问代价','横轴 n=0–20，纵轴为对数刻度的示意操作次数；各曲线展示增长阶，常数因子因实现而异。','复杂度函数图'),
  '4.1 静态链表':('static_links','数组中的逻辑链','示例结点分散在下标 0、2、4，却由 next 字段连成 A→B→C。','存储结构图'),
 },
 'data-structures/GPT03数据结构第三章：栈和队列.md':{
  '6.1 基本思想':('maze','深度优先搜索的回溯路径','示例迷宫中实线为到达终点的路径，虚线表示探路后回退；与正文的回溯思想一致。','搜索路径图'),
  '9.1 汉诺塔问题':('hanoi','三层汉诺塔的起始与目标','示例 n=3，全部盘从 A 柱移至 C 柱；最少移动次数 2³−1=7。','递归状态图'),
  '8.2 为什么递归与栈有关':('call_stack','递归调用栈的压入与返回','以 f(3) 递归调用 f(2)、f(1) 为示意；每层保留自己的返回位置。','调用栈图'),
  '14.1 递推关系':('fib_growth','k 阶递推的数值增长','示例 k=3 且初值为 0,0,1；后项为前 3 项之和。','离散函数图'),
 },
 'data-structures/GPT04 数据结构第四章：串.md':{
  '5.1 块链存储的核心思想':('chunk_chain','块链串的结点与链接','示例每块容量为 3，顺序存储 ABC、DEF、G，再由 next 连接各块。','存储结构图'),
  '9.2 首先理解“前缀”与“后缀”':('prefix_bars','模式串的最长真前后缀','模式 ABABAC 各前缀的最长相等真前后缀长度为 0、0、1、2、3、0；这是 LPS，非本章教材 next 下标值。','前缀函数图'),
  '11.1 匹配时的两条规则':('kmp_shift','KMP 失配后的模式移动','主串 ABABAC、模式 ABAC：首轮已匹配 ABA 后失配，复用边界 A，将模式右移两位而主串不回退。','匹配过程图'),
  '7.5 BF的时间与空间复杂度':('complexity','BF 与 KMP 的增长阶','主串与模式长度同为 n 的简化对照：BF 最坏 O(n²)，KMP O(n)；纵轴为对数刻度示意操作次数。','复杂度函数图'),
 },
 'data-structures/GPT05 数据结构第五章：数组和广义表.md':{
  '2.4 $n$ 维数组':('strides','二维数组的两种线性偏移','2×3 数组示例：行优先偏移 i·3+j；列优先偏移 j·2+i。','地址映射图'),
  '4.8 十字链表':('crosslist','同一非零元的行链与列链','示例非零元 (1,2,7) 同时接入第 1 行和第 2 列的链表。','双向索引图'),
  '5.5 组合运算':('glist_ops','广义表的表头与表尾','对 L=((a,b),(c,d))：Head(L)=(a,b)，Tail(L)=((c,d))；括号层次决定结果。','递归结构图'),
  '4.4 稀疏矩阵转置':('transpose','稀疏矩阵转置的行列交换','示例三元组 (0,1,5)、(1,2,3)、(2,0,7) 转置后交换行列并按新行排序。','矩阵变换图'),
 },
 'discrete-math/GPT01命题逻辑基础：命题、联结词、命题公式与真值表.md':{
  '5.4 分层命题公式':('syntax_tree','公式 (P→Q)∧R 的语法树','先求子公式 P→Q，再与 R 作合取；树的父子关系决定运算顺序。','公式结构图'),
  '4.4 程序分支结构':('branch_gate','条件分支的两条路径','P=1 选择 Q，P=0 选择 R；输出等于 (P∧Q)∨(¬P∧R)。','逻辑电路图'),
 },
 'discrete-math/GPT02命题逻辑命题公式、逻辑等值式与联结词完备集.md':{
  '5. 四种新增的二元联结词':('nand_gate','与非门的逻辑结构','P↑Q=¬(P∧Q)；只有两个输入同真时输出为假。','逻辑电路图'),
  '3. 为什么 $\\{\\neg,\\to\\}$ 是完备集':('implication_gate','用 ¬ 与 → 构造析取','P∨Q=¬P→Q；输入四种赋值时两侧输出逐行一致。','逻辑电路图'),
 },
 'discrete-math/GPT03命题逻辑-范式：析取范式、合取范式与主范式.md':{
  '5. 方法二：真值表法求主析取范式':('kmap_true','排斥或的真值格与主析取范式','二变元示例 P⊕Q：真格 01、10 对应 m₁、m₂。','真值格图'),
  '6. 方法二：真值表法求主合取范式':('kmap_false','排斥或的假值格与主合取范式','同一示例假格 00、11 对应 M₀、M₃。','真值格图'),
 },
 'discrete-math/GPT04命题逻辑：推理的形式结构与有效性判定.md':{
  '2.3 有效推理的严格定义':('truth_space','有效推理不存在反例赋值','所有赋值中只需搜索“前提全真、结论假”区域；该区域为空则推理有效。','赋值空间图'),
  '6.1 标准证明思路':('proof_dag','从前提到结论的依赖关系','示例由 P→Q、Q→R、P 先得到 P→R，再由 P 得到 R。','证明依赖图'),
 },
 'discrete-math/GPT05命题逻辑：自然推理系统 P 与演绎证明.md':{
  '7.2 正确书写':('proof_scope','条件证明的假设作用域','临时假设 P，在作用域中推出 Q，解除假设后可写 P→Q。','证明作用域图'),
  '8.3 反证法的操作步骤':('contradiction_scope','反证法的假设作用域','为证 P 临时假设 ¬P，在作用域内推出矛盾，解除假设得 P。','证明作用域图'),
 },
}

INTERACTIVE_KINDS={'galton','maxwell_area','complexity','prefix_bars','strides','kmap_true','kmap_false'}


def _interactive_html(kind,html):
 controls={
  'galton':[('向右概率 p','p','.2','.8','.05','.5')],
  'maxwell_area':[('温度 T（K）','T','250','900','25','300'),('区间下界（m/s）','lo','200','500','25','300'),('区间上界（m/s）','hi','600','900','25','600')],
  'complexity':[('输入规模 n','n','1','20','1','10')],
  'prefix_bars':[('前缀长度 i','i','1','6','1','5')],
  'strides':[('行 i','i','0','1','1','1'),('列 j','j','0','2','1','2')],
  'kmap_true':[('P','p','0','1','1','0'),('Q','q','0','1','1','1')],
  'kmap_false':[('P','p','0','1','1','0'),('Q','q','0','1','1','0')],
 }[kind]
 fields=''.join(f'<label>{e(title)}<input type="range" data-parameter="{name}" min="{lo}" max="{hi}" step="{step}" value="{value}"><output>{value}</output></label>' for title,name,lo,hi,step,value in controls)
 html=html.replace('class="concept-visual"',f'class="concept-visual scientific-widget" data-science="{kind}"',1)
 return html.replace('<p class="concept-visual-note">',f'<div class="scientific-controls">{fields}</div><div class="scientific-readout" aria-live="polite"></div><p class="concept-visual-note">',1)


def _line(x1,y1,x2,y2,color='var(--border)',width=1.5,dash=''):
 return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{f" stroke-dasharray=\"{dash}\"" if dash else ""}/>'


def _circle(x,y,r,fill='var(--viz-blue-bg)',stroke='var(--viz-blue)'):
 return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>'


def _poly(points,stroke='var(--viz-blue)',fill='none',width=2.7):
 return f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in points)}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round"/>'


def _axes(xlabel,ylabel,xticks=(),yticks=(),left=74,right=706,top=34,bottom=234):
 body=''
 for x,label in xticks:
  body+=_line(x,top,x,bottom)+text(x,bottom+21,label,11,color='var(--soft)',weight=500)
 for y,label in yticks:
  body+=_line(left,y,right,y)+text(left-8,y+4,label,11,'end','var(--soft)',500)
 body+=_line(left,top,left,bottom,'var(--soft)')+_line(left,bottom,right,bottom,'var(--soft)')
 body+=text(right,bottom+48,xlabel,12,'end','var(--soft)',500)+text(left,23,ylabel,12,'start','var(--soft)',500)
 return body


def render_upgrade(source_key,spec):
 config=UPGRADES.get(source_key,{}).get(spec['match'])
 if not config:return None
 kind,title,note,label=config
 upgraded={**spec,'kind':kind,'title':title,'note':note,'label':label}
 body='';height=290
 if kind=='galton':
  values=[comb(10,k)/1024 for k in range(11)];peak=max(values)
  body+=_axes('向右偏转次数 k','理论概率 P(k)',[(90+i*60,str(i)) for i in range(11)],[(234,'0'),(134,'0.15'),(34,'0.30')],left=75,right=710)
  for k,p in enumerate(values):
   h=p/.3*200;x=82+k*60
   body+=rect(x,234-h,25,h,'var(--viz-blue-bg)','var(--viz-blue)',2)
  body+=text(380,285,'二项分布：P(k)=C(10,k)/2¹⁰',13,color='var(--soft)',weight=500);height=310
 elif kind=='maxwell_area':
  M=.032;R=8.314;T=300
  f=lambda v:4*pi*(M/(2*pi*R*T))**1.5*v*v*exp(-M*v*v/(2*R*T))
  vmax=1200;ymax=.0022;X=lambda v:76+v/1200*630;Y=lambda v:234-f(v)/ymax*190
  body+=_axes('速率 v（m/s）','概率密度 f(v)',[(76+i*157.5,str(i*300)) for i in range(5)],[(234,'0'),(234-200*.001/ymax,'0.001'),(234-200*.002/ymax,'0.002')],left=76)
  area=[(X(v),Y(v)) for v in range(300,601,5)]
  body+=_poly([(X(300),234),*area,(X(600),234)],'var(--viz-green)','var(--viz-green-bg)',1.5)
  body+=_poly([(X(v),Y(v)) for v in range(0,1201,5)])
  body+=text(380,286,'P(300≤v≤600)=∫₃₀₀⁶⁰⁰f(v)dv',14,color='var(--viz-green)');height=313
 elif kind=='equipartition':
  labels=['平动 x','平动 y','平动 z','转动 1','转动 2'];colors=['var(--viz-blue)']*3+['var(--viz-green)']*2
  body+=_axes('自由度','每个自由度平均能量（kT）',yticks=[(234,'0'),(139,'0.25'),(44,'0.5')])
  for i,lbl in enumerate(labels):
   x=100+i*122;body+=rect(x,44,58,190,'var(--viz-blue-bg)' if i<3 else 'var(--viz-green-bg)',colors[i],3)+text(x+29,258,lbl,13)
  body+=text(380,287,'每个经典二次型自由度贡献 ½kT',13,color='var(--soft)',weight=500);height=313
 elif kind=='collision_path':
  points=[(78,190),(178,91),(264,177),(382,76),(482,164),(610,101),(690,155)]
  body+=_poly(points)
  for i,(x,y) in enumerate(points):body+=_circle(x,y,8,'var(--viz-orange-bg)','var(--viz-orange)')+text(x,y-17,str(i),12)
  body+=arrow(264,218,382,218,'var(--viz-green)')+text(325,243,'一段自由程',14,color='var(--viz-green)')
  body+=text(380,282,'λ = 大量相邻碰撞间路程的平均值',14,color='var(--soft)',weight=500);height=307
 elif kind=='energy_sankey':
  body+=rect(70,87,160,110,'var(--viz-blue-bg)','var(--viz-blue)')+text(150,138,'吸热 Q',18)+text(150,169,'100 J',16)
  body+=_poly([(235,92),(410,92),(490,50),(490,110),(410,152),(235,152)],'var(--viz-blue)','var(--viz-blue-bg)',1.8)
  body+=_poly([(235,152),(410,152),(490,180),(490,220),(410,192),(235,192)],'var(--viz-orange)','var(--viz-orange-bg)',1.8)
  body+=rect(500,50,198,60,'var(--viz-green-bg)','var(--viz-green)')+text(599,77,'ΔU',18)+text(599,100,'60 J',16)
  body+=rect(500,180,198,40,'var(--viz-orange-bg)','var(--viz-orange)')+text(599,205,'对外功 A = 40 J',15)
  return figure(upgraded,body,288)
 elif kind=='free_expansion':
  for x,divider,caption in [(65,235,'初态：气体占一半'),(425,None,'末态：气体占全部')]:
   body+=rect(x,58,280,154,'var(--paper)','var(--viz-blue)',3)
   if divider:body+=_line(divider,58,divider,212,'var(--viz-orange)',2)
   for j in range(12):
    px=x+24+(j*67%(135 if divider else 250));py=75+(j*41%120)
    body+=_circle(px,py,3,'var(--viz-blue)','var(--viz-blue)')
   body+=text(x+140,251,caption,15)
  body+=text(380,284,'端点可计算 ΔS；中间没有准静态过程曲线',13,color='var(--soft)',weight=500);height=309
 elif kind=='phase_timeline':
  X=lambda u:75+u*630;Y=lambda u:145-90*sin(2*pi*u+pi/2)
  body+=_axes('时间 t / T','位移 x / A',[(X(i/4),str(i)+'T/4' if i else '0') for i in range(5)],[(235,'−1'),(145,'0'),(55,'1')])
  body+=_poly([(X(i/240),Y(i/240)) for i in range(241)])
  for i in range(5):body+=_circle(X(i/4),Y(i/4),5,'var(--viz-orange)','var(--viz-orange)')
  body+=text(380,286,'端点 v=0；平衡位置 |v| 最大',13,color='var(--soft)',weight=500);height=311
 elif kind in ('linked_insert','linked_delete'):
  labels=['p','q','r'] if kind=='linked_delete' else ['p','q','e'];xs=[140,360,580]
  body+=text(80,64,'操作前',15,'start','var(--soft)',500)
  for x,lbl in zip(xs,labels):body+=rect(x-52,80,104,54,'var(--viz-blue-bg)','var(--viz-blue)',6)+text(x,114,lbl,18)
  body+=arrow(195,107,302,107)
  if kind=='linked_delete':body+=arrow(415,107,522,107)
  else:body+=text(580,68,'待插入结点',12,color='var(--soft)',weight=500)
  body+=text(80,200,'操作后',15,'start','var(--soft)',500)
  if kind=='linked_delete':
   body+=rect(140,189,104,54,'var(--viz-green-bg)','var(--viz-green)',6)+text(192,223,'p',18)
   body+=rect(540,189,104,54,'var(--viz-green-bg)','var(--viz-green)',6)+text(592,223,'r',18)
   body+=arrow(248,216,534,216,'var(--viz-green)')+text(390,195,'跨过 q',13,color='var(--soft)',weight=500)
  else:
   for x,lbl in zip([140,360,580],['p','e','q']):body+=rect(x-52,189,104,54,'var(--viz-green-bg)','var(--viz-green)',6)+text(x,223,lbl,18)
   body+=arrow(195,216,302,216,'var(--viz-green)')+arrow(415,216,522,216,'var(--viz-green)')
  height=270
 elif kind=='complexity':
  log10=__import__('math').log10;log2=__import__('math').log2
  body+=_axes('输入规模 n','示意操作次数（对数轴）',[(74+i*158,str(i*5)) for i in range(5)],[(234,'0'),(157,'9'),(80,'99'),(34,'400')])
  X=lambda n:74+n/20*632;Y=lambda v:234-log10(1+v)/log10(401)*200
  for label,fn,color in [('O(1)',lambda n:1,'var(--viz-green)'),('O(log n)',lambda n:log2(1+n),'var(--viz-orange)'),('O(n)',lambda n:n,'var(--viz-blue)'),('O(n²)',lambda n:n*n,'#b25c67')]:
   body+=_poly([(X(i/5),Y(fn(i/5))) for i in range(101)],color)+text(X(17),Y(fn(17))-8,label,13,color=color)
  height=277
 elif kind=='static_links':
  body+=text(95,47,'物理下标',13,'start','var(--soft)',500)
  for i,(v,nxt) in enumerate([('A','2'),('空','—'),('B','4'),('空','—'),('C','∅')]):
   x=110+i*126;body+=text(x+48,47,str(i),14)+rect(x,64,100,72,'var(--viz-green-bg)' if v!='空' else 'var(--paper)','var(--viz-green)' if v!='空' else 'var(--border)',4)
   body+=text(x+50,94,v,17)+text(x+50,123,'next='+nxt,12)
  body+=arrow(165,193,390,193)+arrow(395,193,620,193)
  body+=text(165,179,'A',18)+text(395,179,'B',18)+text(625,179,'C',18)
  body+=text(380,245,'物理位置 0 → 2 → 4；逻辑顺序 A → B → C',13,color='var(--soft)',weight=500);height=273
 elif kind=='call_stack':
  for i,name in enumerate(['f(3)','f(2)','f(1)','基本情形']):
   x=100+i*140;y=55+i*36
   body+=rect(x,y,130,70,'var(--viz-blue-bg)' if i%2==0 else 'var(--viz-green-bg)','var(--viz-blue)' if i%2==0 else 'var(--viz-green)',7)
   body+=text(x+65,y+30,name,17)+text(x+65,y+54,'独立调用帧',11,color='var(--soft)',weight=500)
   if i<3:body+=arrow(x+132,y+36,x+146,y+72)
  body+=text(380,281,'调用时逐层压入；返回时逆序弹出',14,color='var(--soft)',weight=500);height=305
 elif kind=='hanoi':
  for cx,title,disks in [(220,'起始 A',3),(540,'目标 C',3)]:
   body+=_line(cx,72,cx,220,'var(--soft)',4)+_line(cx-90,220,cx+90,220,'var(--soft)',4)
   for i in range(disks):
    y=188-i*33;w=145-i*38
    body+=rect(cx-w/2,y,w,28,'var(--viz-blue-bg)' if cx==220 else 'var(--viz-green-bg)','var(--viz-blue)' if cx==220 else 'var(--viz-green)',4)
   body+=text(cx,258,title,16)
  body+=arrow(315,148,440,148,'var(--viz-orange)')+text(380,137,'最少 7 步',14,color='var(--viz-orange)');height=290
 elif kind=='maze':
  grid=['S..##','#.#.#','#...#','###.#','#..E#'];x0=174;y0=24;size=44
  path=[(0,0),(0,1),(1,1),(2,1),(2,2),(2,3),(3,3),(4,3)]
  for i,row in enumerate(grid):
   for j,v in enumerate(row):
    x=x0+j*size;y=y0+i*size
    fill='var(--soft)' if v=='#' else 'var(--viz-green-bg)' if (i,j) in path else 'var(--paper)'
    body+=rect(x,y,size,size,fill,'var(--border)',0)
    if v in 'SE':body+=text(x+size/2,y+29,v,17)
  body+=_poly([(x0+j*size+size/2,y0+i*size+size/2) for i,j in path],'var(--viz-green)')
  body+=_line(x0+3*size+size/2,y0+2*size+size/2,x0+3*size+size/2,y0+1*size+size/2,'var(--viz-orange)',2,'5 4')
  body+=text(565,85,'S 起点',15,'start')+text(565,119,'E 终点',15,'start')+text(565,153,'实线：成功路径',13,'start','var(--viz-green)',500)+text(565,182,'虚线：探路后回退',13,'start','var(--viz-orange)',500)
  height=274
 elif kind=='chunk_chain':
  for idx,chunk in enumerate(['ABC','DEF','G··']):
   x=76+idx*235
   body+=text(x+85,51,f'块 {idx+1}',15)
   for j,ch in enumerate(chunk):body+=rect(x+j*55,82,51,62,'var(--viz-blue-bg)' if ch!='·' else 'var(--paper)','var(--viz-blue)',3)+text(x+j*55+25,121,ch,18)
   body+=text(x+85,182,'next →' if idx<2 else 'next = ∅',13,color='var(--soft)',weight=500)
   if idx<2:body+=arrow(x+170,114,x+226,114)
  body+=text(380,235,'物理块分散；逻辑字符顺序由块链接保持',14,color='var(--soft)',weight=500);height=260
 elif kind=='prefix_bars':
  word='ABABAC';vals=[0,0,1,2,3,0]
  body+=_axes('前缀长度 i','最长相等真前后缀长度 LPS[i]',[(117+i*103,str(i+1)) for i in range(6)],[(234,'0'),(170,'1'),(106,'2'),(42,'3')])
  for i,(char,val) in enumerate(zip(word,vals)):
   x=98+i*103
   body+=rect(x,234-val*64,39,val*64 or 2,'var(--viz-green-bg)','var(--viz-green)',2)
   body+=text(x+20,219-val*64,char,15)
  body+=text(380,287,'ABABA 的最长共同边界是 ABA；ABABAC 的为 0',13,color='var(--soft)',weight=500);height=310
 elif kind=='kmp_shift':
  main='ABABAC';pattern='ABAC'
  for j,ch in enumerate(main):
   x=115+j*91;body+=rect(x,32,72,44,'var(--viz-blue-bg)','var(--viz-blue)',3)+text(x+36,61,ch,17)
  body+=text(59,61,'主串',13,'start','var(--soft)',500)
  for row,shift in enumerate((0,2)):
   y=103+row*79
   for j,ch in enumerate(pattern):
    x=115+(j+shift)*91
    color='var(--viz-orange)' if row==0 and j==3 else 'var(--viz-green)' if row==1 else 'var(--viz-blue)'
    fill='var(--viz-orange-bg)' if row==0 and j==3 else 'var(--viz-green-bg)' if row==1 else 'var(--viz-blue-bg)'
    body+=rect(x,y,72,44,fill,color,3)+text(x+36,y+29,ch,17)
   body+=text(48,y+29,'失配' if row==0 else '匹配',13,'start','var(--soft)',500)
  body+=text(380,268,'已匹配 ABA 的最长边界 A；模式右移 2 位，主串不回退',13,color='var(--soft)',weight=500);height=295
 elif kind=='strides':
  vals=[['a₀₀','a₀₁','a₀₂'],['a₁₀','a₁₁','a₁₂']]
  for i,row in enumerate(vals):
   for j,v in enumerate(row):body+=rect(73+j*74,50+i*55,67,49,'var(--viz-blue-bg)','var(--viz-blue)',2)+text(106+j*74,81+i*55,v,15)
  body+=text(180,191,'逻辑矩阵 2×3',16)
  body+=arrow(308,104,392,104)
  for row,labels in [(43,['00','01','02','10','11','12']),(139,['00','10','01','11','02','12'])]:
   body+=text(419,row-8,'行优先' if row==43 else '列优先',13,'start','var(--soft)',500)
   for j,v in enumerate(labels):body+=rect(419+j*49,row,44,40,'var(--viz-green-bg)' if row==43 else 'var(--viz-orange-bg)','var(--viz-green)' if row==43 else 'var(--viz-orange)',2)+text(441+j*49,row+26,v,12)
  body+=text(380,240,'相同二维下标，在两种布局中的线性偏移可能不同',13,color='var(--soft)',weight=500);height=265
 elif kind=='crosslist':
  body+=rect(68,108,126,58,'var(--viz-blue-bg)','var(--viz-blue)',5)+text(131,143,'第 1 行头',16)
  body+=rect(348,22,126,58,'var(--viz-orange-bg)','var(--viz-orange)',5)+text(411,57,'第 2 列头',16)
  body+=rect(332,117,160,67,'var(--viz-green-bg)','var(--viz-green)',6)+text(412,149,'(1,2,7)',18)+text(412,171,'right / down',11,color='var(--soft)',weight=500)
  body+=arrow(200,137,327,137)+arrow(411,83,411,111,'var(--viz-orange)')
  body+=arrow(497,149,636,149)+arrow(411,189,411,245,'var(--viz-orange)')
  body+=text(614,136,'同行后继',12)+text(501,238,'同列后继',12);height=285
 elif kind=='glist_ops':
  body+=text(380,47,'L = ((a,b),(c,d))',20)
  body+=arrow(305,67,200,119)+arrow(455,67,560,119)
  body+=rect(99,123,200,60,'var(--viz-blue-bg)','var(--viz-blue)',7)+text(199,159,'Head(L) = (a,b)',16)
  body+=rect(459,123,220,60,'var(--viz-green-bg)','var(--viz-green)',7)+text(569,159,'Tail(L) = ((c,d))',16)
  body+=text(380,222,'表尾保留外层括号；它是表，不是最后一个元素',14,color='var(--soft)',weight=500);height=250
 elif kind=='transpose':
  left=[['0','5','0'],['0','0','3'],['7','0','0']];right=[['0','0','7'],['5','0','0'],['0','3','0']]
  for rows,x0 in [(left,90),(right,450)]:
   for i,row in enumerate(rows):
    for j,v in enumerate(row):
     active=v!='0';x=x0+j*60;y=45+i*52
     body+=rect(x,y,54,46,'var(--viz-green-bg)' if active else 'var(--paper)','var(--viz-green)' if active else 'var(--border)',1)+text(x+27,y+30,v,16)
  body+=arrow(302,118,424,118,'var(--viz-orange)')+text(365,105,'Aᵀ',20,color='var(--viz-orange)')
  body+=text(180,246,'原矩阵 A',16)+text(540,246,'转置矩阵 Aᵀ',16);height=275
 elif kind=='syntax_tree':
  for x,y,v in [(380,46,'∧'),(250,136,'→'),(510,136,'R'),(172,231,'P'),(328,231,'Q')]:
   body+=_circle(x,y,30,'var(--viz-green-bg)' if v in '∧→' else 'var(--viz-blue-bg)','var(--viz-green)' if v in '∧→' else 'var(--viz-blue)')+text(x,y+6,v,19)
  for x1,y1,x2,y2 in [(359,67,271,114),(401,67,489,114),(230,158,190,209),(270,158,310,209)]:body+=_line(x1,y1,x2,y2,'var(--viz-blue)',2)
  height=275
 elif kind=='branch_gate':
  body+=_circle(130,130,32)+text(130,136,'P',19)
  body+=arrow(165,116,295,62)+arrow(165,143,295,206)
  body+=text(229,71,'P=1',13,color='var(--viz-blue)')+text(229,200,'P=0',13,color='var(--viz-orange)')
  body+=_circle(331,57,29,'var(--viz-green-bg)','var(--viz-green)')+text(331,64,'Q',18)
  body+=_circle(331,211,29,'var(--viz-orange-bg)','var(--viz-orange)')+text(331,218,'R',18)
  body+=arrow(365,57,582,127,'var(--viz-green)')+arrow(365,211,582,145,'var(--viz-orange)')
  body+=rect(594,106,112,62,'var(--viz-blue-bg)','var(--viz-blue)',6)+text(650,143,'输出',17);height=268
 elif kind in ('nand_gate','implication_gate'):
  inputs=[('P',65),('Q',177)]
  for name,y in inputs:
   body+=_circle(105,y,25)+text(105,y+6,name,17)
  if kind=='nand_gate':
   body+=arrow(131,65,302,96)+arrow(131,177,302,148)
   body+=rect(305,89,144,69,'var(--viz-blue-bg)','var(--viz-blue)',20)+text(377,132,'AND',18)
   body+=_circle(463,123,9,'var(--paper)','var(--viz-orange)')+arrow(474,123,610,123,'var(--viz-orange)')
   body+=text(650,128,'P↑Q',19)
  else:
   body+=rect(179,41,104,50,'var(--viz-orange-bg)','var(--viz-orange)',7)+text(231,73,'NOT',15)
   body+=arrow(132,65,174,65)+arrow(285,65,385,108,'var(--viz-orange)')+arrow(132,177,385,139)
   body+=rect(391,95,130,66,'var(--viz-blue-bg)','var(--viz-blue)',20)+text(456,135,'→',22)
   body+=arrow(526,128,627,128)+text(672,135,'P∨Q',18)
   body+=text(380,237,'输入为 ¬P 与 Q；¬P→Q 与 P∨Q 等值',13,color='var(--soft)',weight=500)
  height=269
 elif kind in ('kmap_true','kmap_false'):
  active={(0,1),(1,0)} if kind=='kmap_true' else {(0,0),(1,1)}
  body+=text(236,44,'列 Q=0',14)+text(390,44,'列 Q=1',14)
  for i in range(2):
   body+=text(92,112+i*92,f'行 P={i}',14)
   for j in range(2):
    x=160+j*154;y=60+i*92;on=(i,j) in active
    body+=rect(x,y,145,82,'var(--viz-green-bg)' if on else 'var(--paper)','var(--viz-green)' if on else 'var(--border)',3)
    body+=text(x+72,y+34,str(i)+str(j),15)+text(x+72,y+61,('m' if kind=='kmap_true' else 'M')+str(2*i+j),17,color='var(--viz-green)' if on else 'var(--soft)')
  body+=text(590,106,'选中真格' if kind=='kmap_true' else '选中假格',16,color='var(--viz-green)')
  body+=text(590,142,'01 与 10' if kind=='kmap_true' else '00 与 11',15)
  body+=text(380,274,'主析取范式读真格；主合取范式读假格',13,color='var(--soft)',weight=500);height=299
 elif kind=='truth_space':
  for i,(p,q) in enumerate([(0,0),(0,1),(1,0),(1,1)]):
   x=95+i*165;prem=int(bool(p) and (not p or bool(q)));counter=prem and not q
   body+=_circle(x+45,117,43,'var(--viz-green-bg)' if prem else 'var(--paper)','var(--viz-green)' if prem else 'var(--border)')
   body+=text(x+45,111,f'P={p}',14)+text(x+45,132,f'Q={q}',14)
   body+=text(x+45,185,'前提同真' if prem else '前提未同真',13,color='var(--viz-green)' if prem else 'var(--soft)')
  body+=text(380,248,'示例 MP：仅 11 行前提同真，且该行结论 Q 也真；反例区为空',13,color='var(--soft)',weight=500);height=279
 elif kind=='proof_dag':
  nodes=[(83,35,'P→Q'),(308,35,'Q→R'),(550,35,'P'),(277,154,'P→R'),(550,154,'R')]
  for x,y,v in nodes:body+=rect(x,y,128,57,'var(--viz-blue-bg)' if y==35 else 'var(--viz-green-bg)','var(--viz-blue)' if y==35 else 'var(--viz-green)',7)+text(x+64,y+35,v,17)
  body+=arrow(153,98,304,149)+arrow(370,98,344,149)+arrow(409,182,543,182)+arrow(614,98,614,150)
  body+=text(380,265,'两条条件先合成，再与 P 配合得到 R',13,color='var(--soft)',weight=500);height=290
 elif kind in ('proof_scope','contradiction_scope'):
  assumption='P' if kind=='proof_scope' else '¬P';inside='Q' if kind=='proof_scope' else '⊥';result='P→Q' if kind=='proof_scope' else 'P'
  body+=rect(90,32,420,193,'var(--viz-blue-bg)','var(--viz-blue)',8)
  body+=text(115,56,'临时假设作用域',13,'start','var(--viz-blue)')
  body+=rect(135,79,130,50,'var(--paper)','var(--viz-orange)',5)+text(200,111,'假设 '+assumption,16)
  body+=arrow(270,105,365,105)
  body+=rect(371,79,105,50,'var(--paper)','var(--viz-green)',5)+text(423,111,'推出 '+inside,16)
  body+=arrow(510,135,581,176,'var(--viz-green)')
  body+=rect(582,161,130,57,'var(--viz-green-bg)','var(--viz-green)',5)+text(647,196,result,18)
  body+=text(380,260,'解除假设后，不能再把临时假设当作独立前提',13,color='var(--soft)',weight=500);height=287
 elif kind=='fib_growth':
  vals=[0,0,1]
  for i in range(3,11):vals.append(sum(vals[-3:]))
  body+=_axes('项序号 n','fₙ（k=3）',[(75+i*63,str(i)) for i in range(11)],[(234,'0'),(134,'42'),(34,'85')])
  for i,v in enumerate(vals):
   x=75+i*63;y=234-v/85*200;body+=_line(x,234,x,y,'var(--viz-blue)',2)+_circle(x,y,4,'var(--viz-blue)','var(--viz-blue)')
  height=277
 else:
  return None
 html=figure(upgraded,body,height)
 return _interactive_html(kind,html) if kind in INTERACTIVE_KINDS else html
