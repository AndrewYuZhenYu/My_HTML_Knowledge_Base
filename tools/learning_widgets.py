"""Source-aligned algorithm steppers and truth-table explorers."""
from html import escape
from itertools import product
from json import dumps
from visuals import S, render


def step(match,title,note,mode,states):
 return dict(match=match,title=title,note=note,mode=mode,states=states)


STEPS={
 'data-structures/GPT02 数据结构第二章：线性表.md':step('2.4 插入：后面的元素向右移动','交互演示 · 顺序表插入','从后往前移动，才能保留尚未复制的元素。','slots',[
  dict(label='初始',cells=['A','B','C','D','·'],detail='在 B 前插入 X，先留出末尾空位。'),
  dict(label='移动 D',cells=['A','B','C','·','D'],detail='把最后一个元素 D 右移一格。'),
  dict(label='移动 C',cells=['A','B','·','C','D'],detail='继续从后向前移动 C。'),
  dict(label='移动 B',cells=['A','·','B','C','D'],detail='B 的原位置空出来。'),
  dict(label='写入 X',cells=['A','X','B','C','D'],detail='插入完成，后续元素相对顺序不变。')]),
 'data-structures/GPT03数据结构第三章：栈和队列.md':step('12.4 用下标跟踪循环队列','交互演示 · 循环队列回绕','容量 5，采用预留一个空位的约定；front 指队头，rear 指下一个可写位置。','queue',[
  dict(label='初始',cells=['A','B','C','·','·'],front=0,rear=3,detail='已有 A、B、C；rear=3。'),
  dict(label='出队 A、B',cells=['·','·','C','·','·'],front=2,rear=3,detail='前部留下可复用的空位。'),
  dict(label='入队 D',cells=['·','·','C','D','·'],front=2,rear=4,detail='D 写入下标 3。'),
  dict(label='入队 E',cells=['·','·','C','D','E'],front=2,rear=0,detail='rear 从数组末尾回绕到 0。'),
  dict(label='入队 F',cells=['F','·','C','D','E'],front=2,rear=1,detail='此时 (rear+1)%5=front，队列已满。')]),
 'data-structures/GPT04 数据结构第四章：串.md':step('7.2 逐趟匹配示例','交互演示 · BF 模式匹配','主串 ABABC 与模式 ABC；失配后主串起点右移一位。','match',[
  dict(label='起点 1',shift=0,detail='ABA 与 ABC 在第三个字符处失配。'),
  dict(label='起点 2',shift=1,detail='BAB 与 ABC 在第一个字符处失配。'),
  dict(label='起点 3',shift=2,detail='ABC 与 ABC 全部匹配，返回起始位置 3（1-based）。')]),
 'data-structures/GPT05 数据结构第五章：数组和广义表.md':step('4.4 稀疏矩阵转置','交互演示 · 三元组转置','交换行列下标后，按目标行顺序排列三元组。','triples',[
  dict(label='原矩阵',cells=['(0,1,5)','(1,2,3)','(2,0,7)'],detail='按原矩阵行序列出三个非零元。'),
  dict(label='交换下标',cells=['(1,0,5)','(2,1,3)','(0,2,7)'],detail='逐项执行 (i,j,v)→(j,i,v)，此时顺序尚未调整。'),
  dict(label='按新行排序',cells=['(0,2,7)','(1,0,5)','(2,1,3)'],detail='按新行号重新排列，得到转置矩阵的三元组表。')]),
}


def truth(match,title,note,variables,columns,fn):
 rows=[]
 for assignment in product((0,1),repeat=len(variables)):
  rows.append([*map(str,assignment),*map(str,fn(*assignment))])
 return dict(match=match,title=title,note=note,variables=variables,columns=columns,rows=rows)


implies=lambda p,q: int(not p or q)
TRUTHS={
 'discrete-math/GPT01命题逻辑基础：命题、联结词、命题公式与真值表.md':truth('7.2 三元公式','交互真值表 · 三元公式','切换 P、Q、R，定位对应行；F=(P→Q)∧R。',['P','Q','R'],['P','Q','R','P→Q','F'],lambda p,q,r:(implies(p,q),int(implies(p,q) and r))),
 'discrete-math/GPT02命题逻辑命题公式、逻辑等值式与联结词完备集.md':truth('二、逻辑等值式的定义与判定','交互真值表 · 蕴涵消去','四行逐一对照 P→Q 与 ¬P∨Q；结果总相同。',['P','Q'],['P','Q','P→Q','¬P∨Q'],lambda p,q:(implies(p,q),int(not p or q))),
 'discrete-math/GPT03命题逻辑-范式：析取范式、合取范式与主范式.md':truth('三、极小项与主析取范式','交互真值表 · 排斥或的主析取范式','F=P⊕Q；真行 01 与 10 对应两个极小项。',['P','Q'],['P','Q','P⊕Q','(¬P∧Q)∨(P∧¬Q)'],lambda p,q:(p^q,int((not p and q) or (p and not q)))),
 'discrete-math/GPT04命题逻辑：推理的形式结构与有效性判定.md':truth('4.1 “如果','交互真值表 · 肯定前件','检查 (P∧(P→Q))→Q；每一行都为真。',['P','Q'],['P','Q','前提同真','推理条件式'],lambda p,q:(int(p and implies(p,q)),implies(int(p and implies(p,q)),q))),
 'discrete-math/GPT05命题逻辑：自然推理系统 P 与演绎证明.md':truth('4.6 假言三段论','交互真值表 · 假言三段论','检查 ((P→Q)∧(Q→R))→(P→R)；每一行都为真。',['P','Q','R'],['P','Q','R','两前提同真','推理条件式'],lambda p,q,r:(int(implies(p,q) and implies(q,r)),implies(int(implies(p,q) and implies(q,r)),implies(p,r)))),
}


def _attributes(spec,kind):
 if kind=='stepper':
  payload=dumps(spec['states'],ensure_ascii=False,separators=(',',':'))
  return f'data-mode="{escape(spec["mode"])}" data-states="{escape(payload,quote=True)}"'
 payload=dumps(spec['rows'],ensure_ascii=False,separators=(',',':'))
 names=dumps(spec['columns'],ensure_ascii=False,separators=(',',':'))
 return f'data-rows="{escape(payload,quote=True)}" data-columns="{escape(names,quote=True)}"'


def render_widget(spec,kind):
 if kind=='stepper':
  if spec['mode']=='match':fallback=S('', 'bf_match',spec['title'],spec['note'])
  elif spec['mode']=='triples':fallback=S('', 'trace',spec['title'],spec['note'],rows=[(s['label'],s['cells']) for s in spec['states']])
  else:fallback=S('', 'trace',spec['title'],spec['note'],rows=[(s['label'],s['cells']) for s in (spec['states'][0],spec['states'][-1])])
 else:fallback=S('', 'truth_table',spec['title'],spec['note'],columns=spec['columns'],rows=spec['rows'])
 html=render(fallback)
 html=html.replace('class="concept-visual"',f'class="concept-visual learning-widget" data-kind="{kind}" {_attributes(spec,kind)}',1)
 if kind=='stepper':
  controls='<div class="learning-controls"><button type="button" data-action="prev">上一步</button><span class="learning-progress"></span><button type="button" data-action="next">下一步</button></div>'
 else:
  checks=''.join(f'<label><input type="checkbox" data-var="{escape(v)}">{escape(v)} = <output>0</output></label>' for v in spec['variables'])
  controls=f'<div class="learning-controls learning-switches">{checks}</div>'
 html=html.replace('<p class="concept-visual-note">',controls+'<div class="learning-status" aria-live="polite"></div><p class="concept-visual-note">',1)
 return html
