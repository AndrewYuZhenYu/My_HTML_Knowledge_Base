# 命题逻辑：命题公式、逻辑等值式与联结词完备集

> [!abstract] 知识导航
> 本章的学习主线为：**命题公式与赋值 → 真值表 → 逻辑等值 → 基本等值律 → 等值演算 → 真值函数 → 联结词完备集 → 实际应用**。
>
> - **基础层**：看懂命题公式、计算真值、判定重言式与矛盾式。
> - **核心层**：理解 $\leftrightarrow$ 和 $\Leftrightarrow$ 的区别，熟练使用等值律证明、化简。
> - **提高层**：理解真值函数的数量、完备集的判定与构造，能够完成指定联结词集下的公式转换。
> - **应用层**：将语言条件抽象为公式，通过等值演算求解。

---

## 一、命题公式、真值指派与真值表

### 1. 逻辑联结词回顾

命题逻辑将命题的真值记为 **1（真）** 或 **0（假）**。常用五种联结词如下。

| 联结词 | 名称 | 公式 | 真值成立的条件 |
| --- | --- | --- | --- |
| $\neg$ | 否定 | $\neg p$ | $p$ 为假 |
| $\land$ | 合取 | $p\land q$ | $p,q$ 均真 |
| $\lor$ | 析取 | $p\lor q$ | $p,q$ 至少一个真 |
| $\to$ | 蕴涵 | $p\to q$ | **除 $p=1,q=0$ 外均为真** |
| $\leftrightarrow$ | 等价联结词 | $p\leftrightarrow q$ | $p,q$ 真值相同 |

| $p$ | $q$ | $\neg p$ | $p\land q$ | $p\lor q$ | $p\to q$ | $p\leftrightarrow q$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | 0 | 1 | 0 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 | 1 | 1 | 0 |
| 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 1 | 1 | 1 | 1 |

> [!warning] 蕴涵的关键特殊性
> $p\to q$ **仅在前件真、后件假时为假**。特别地，$p=0$ 时，无论 $q$ 真或假，整个蕴涵式均为真。数理逻辑中的联结词按真值定义，不要求连接的两个命题在日常意义上存在因果关系。

> [!example] 自然语言中的“只有”和“除非”
> 令 $p$：“今天是星期一”，$q$：“明天是星期二”。
>
> - “若今天是星期一，则明天是星期二”：$p\to q$。
> - “**只有**今天是星期一，明天**才**是星期二”：$q\to p$（“只有 $p$，才 $q$”中，$p$ 是必要条件）。
> - “今天是星期一当且仅当明天是星期二”：$p\leftrightarrow q$。
>
> 再令 $p$：“别人有困难”，$q$：“老王帮助别人”，$r$：“困难解决了”。
>
> “只要别人有困难，老王就帮助别人，除非困难解决了”可表示为：
>
> $$\neg r\to(p\to q)$$
>
> 或等值地写作：
>
> $$(p\land\neg r)\to q$$
>
> 这里“除非困难解决了”限定了前述帮助义务适用的情形。

### 2. 命题公式（合式公式）

**命题公式（well-formed formula，wff）**按下列规则递归构成：

1. 单个命题变项 $p,q,r,\dots$ 是命题公式。
2. 若 $A$ 是命题公式，则 $\neg A$ 也是命题公式。
3. 若 $A,B$ 是命题公式，则 $(A\land B)$、$(A\lor B)$、$(A\to B)$、$(A\leftrightarrow B)$ 也是命题公式。
4. **只有有限次应用以上规则得到的式子**才是命题公式。

括号用于明确联结范围；在不产生歧义时可依通常约定省略部分括号。

> [!note] 公式与具体命题的区别
> $p\land q$ 是一个符号形式。若未指定 $p,q$ 的真值，它不具有固定的真值；指定真值指派后，才能算出它在该指派下的真值。不要把“合式公式”与“恒真命题”混淆。

### 3. 真值指派、成真指派与成假指派

设公式 $A$ 涉及 $n$ 个不同的命题变项 $p_1,p_2,\dots,p_n$。

- 对所有变项逐个指定一个确定真值，称为 **真值指派（赋值）**。
- 若在某一指派下 $A=1$，该指派称为 **成真指派（成真赋值）**。
- 若在某一指派下 $A=0$，该指派称为 **成假指派（成假赋值）**。
- 每个变项有两种取值，所以 $n$ 元公式有 **$2^n$ 种不同的真值指派**。

$$\boxed{\text{真值指派数}=2^n}$$

例如，三元公式的指派可依 $(p,q,r)$ 的顺序写为 $(0,1,0)$，一共有 $2^3=8$ 种。

> [!example] 由蕴涵的成假条件直接求赋值
> 求 $A=(p\land q)\to\neg(q\lor r)$ 的成真、成假指派。
>
> 蕴涵式成假，必须前件为 1、后件为 0：
>
> $$p\land q=1,\qquad \neg(q\lor r)=0$$
>
> 因而 $p=q=1$，此时 $q\lor r=1$ 自动满足，$r$ 可以任取。
>
> **成假指派**（按 $p,q,r$ 顺序）：$(1,1,0)$、$(1,1,1)$。
>
> **成真指派**：$(0,0,0)$、$(0,0,1)$、$(0,1,0)$、$(0,1,1)$、$(1,0,0)$、$(1,0,1)$。

### 4. 公式的三类重要性质

设 $A$ 为 $n$ 元命题公式。

| 类型 | 定义 | 真值表末列 | 典型例子 |
| --- | --- | --- | --- |
| **重言式（永真式）** | 所有赋值下都为真 | 全 1 | $p\lor\neg p$、$p\to p$ |
| **矛盾式（永假式）** | 所有赋值下都为假 | 全 0 | $p\land\neg p$ |
| **可满足式** | 至少存在一个成真指派 | 至少一个 1 | $p$、$p\lor q$，也包括所有重言式 |

> [!important] 分类关系要分清
> - ==重言式一定是可满足式==，二者不是互斥类别。
> - **矛盾式不可满足**；反之，不可满足的公式就是矛盾式。
> - 若公式既有成真赋值也有成假赋值，则它是**可满足但非重言式**。
> - 判断“可满足”，只需找到一个成真赋值；判断“重言式”，必须证明**所有赋值**都为真。

**相关性质：**

- 两个重言式的合取仍是重言式，其析取也仍是重言式。
- 两个矛盾式的合取、析取仍是矛盾式。
- 若 $A$ 与 $A\to B$ 均为重言式，则 $B$ 也是重言式。

> [!example] 直接化简判别矛盾式
> $$\begin{aligned}
> \neg(p\to q)\land q
> &\Leftrightarrow\neg(\neg p\lor q)\land q\\
> &\Leftrightarrow(p\land\neg q)\land q\\
> &\Leftrightarrow p\land(\neg q\land q)\\
> &\Leftrightarrow p\land0\\
> &\Leftrightarrow0
> \end{aligned}$$
>
> 因此其**成真指派为空**，四个二元指派全是成假指派。

### 5. 真值表的构造与用途

真值表按照每一种指派，逐层计算子公式的真值，并在最后一列记录目标公式的值。它可以用于：

1. 求公式的全部成真、成假指派。
2. 判断公式是重言式、矛盾式还是可满足但非重言式。
3. 比较两个公式在每个赋值下的真值，从而判断等值关系。

> [!tip] 构造真值表的标准步骤
> **列不同变项 → 按 $00\dots0$ 到 $11\dots1$ 枚举 → 计算内部子式 → 计算最外层式 → 观察最后一列。**
>
> 例如 $p\to(q\to r)$，先算 $q\to r$，再算外层蕴涵。不要从左到右不分括号地计算。

| $p$ | $q$ | $r$ | $q\to r$ | $p\to(q\to r)$ | $(p\land q)\to r$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | 0 | 0 | 1 | 1 | 1 |
| 0 | 0 | 1 | 1 | 1 | 1 |
| 0 | 1 | 0 | 0 | 1 | 1 |
| 0 | 1 | 1 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 | 1 | 1 |

两公式输出列完全相同，说明它们逻辑等值。这个结论也可用等值演算证明。

---

## 二、逻辑等值式的定义与判定

### 1. 什么叫“逻辑等值”

> [!important] 逻辑等值式的定义
> 若两个命题公式 $A,B$ 在**所有可能的真值指派下**均具有相同的真值，则称二者**逻辑等值（逻辑等价）**，记作：
>
> $$\boxed{A\Leftrightarrow B}$$
>
> 等价的判定条件是：
>
> $$\boxed{A\Leftrightarrow B\quad\text{当且仅当}\quad A\leftrightarrow B\text{是重言式}}$$

逻辑等值强调“真值函数相同”，而不是说两个表达式的文字长得一样。

### 2. 两种“等价”符号的严格区分

| 符号 | 性质 | 含义 | 举例 |
| --- | --- | --- | --- |
| $\leftrightarrow$ | **命题联结词** | 将 $A,B$ 连成新的命题公式，其真值依赖赋值 | $p\leftrightarrow q$ |
| $\Leftrightarrow$ | **等值关系符号** | 断言两侧的公式在所有赋值下取值相同 | $p\to q\Leftrightarrow\neg p\lor q$ |

> [!warning] 不要混用
> $p\leftrightarrow q$ 一般**不是**重言式；当 $p,q$ 不同真值时它为假。
>
> $p\to q\Leftrightarrow\neg p\lor q$ 是对两个公式的**全局等值关系**的陈述。写等值演算时，使用 $\Leftrightarrow$ 连接前后步骤；在构造一个具体命题公式时，使用 $\leftrightarrow$。

### 3. 判定公式等值的两种基本方法

**方法一：真值表法。** 列出所有指派，比较两个公式最终输出列。只要有一行不同，就**不等值**。

**方法二：等值演算法。** 依据基本等值式、代入规则、置换规则和等值关系的传递性，把一个公式逐步变形成另一个公式。

> [!example] 三个结构相近的蕴涵式
> 比较：
>
> $$A=p\to(q\to r)$$
> $$B=(p\to q)\to r$$
> $$C=(p\land q)\to r$$
>
> 按上一节真值表，$A,C$ 输出列完全相同，所以：
>
> $$\boxed{p\to(q\to r)\Leftrightarrow(p\land q)\to r}$$
>
> 但 $B$ 与前两者不等值。取 $(p,q,r)=(0,0,0)$：$A=C=1$，$B=0$，已构成反例。

> [!tip] 判断“不等值”更快
> ==证等值要求所有指派一致；证不等值只需找到一个反例指派。==
>
> 真值表法是可靠的穷举检验；等值演算法则更适合练习题中的“证明”“化简”和“大量变项”的场景。

---

## 三、常用逻辑等值律：分类、原理与使用

以下 $A,B,C$ **代表任意命题公式**，不只是单个变项。因而每一条同时代表无穷多条具体等值式，称为**等值式模式**。

### 1. 关于合取、析取的等值律

| 名称 | 等值式 |
| --- | --- |
| **幂等律** | $A\lor A\Leftrightarrow A$；$A\land A\Leftrightarrow A$ |
| **交换律** | $A\lor B\Leftrightarrow B\lor A$；$A\land B\Leftrightarrow B\land A$ |
| **结合律** | $(A\lor B)\lor C\Leftrightarrow A\lor(B\lor C)$；$(A\land B)\land C\Leftrightarrow A\land(B\land C)$ |
| **分配律：$\lor$ 对 $\land$** | $A\lor(B\land C)\Leftrightarrow(A\lor B)\land(A\lor C)$ |
| **分配律：$\land$ 对 $\lor$** | $A\land(B\lor C)\Leftrightarrow(A\land B)\lor(A\land C)$ |
| **吸收律** | $A\lor(A\land B)\Leftrightarrow A$；$A\land(A\lor B)\Leftrightarrow A$ |

> [!note] 理解“吸收律”
> $A\lor(A\land B)$ 的第二部分若为真，$A$ 必然已为真，所以第二部分没有增加新情况；$A\land(A\lor B)$ 同理，附加条件 $A\lor B$ 不再收紧结果。理解这一点比死记公式更有效。

> [!example] 结合律、分配律的典型应用
> $$\begin{aligned}
> (p\land r)\lor(q\land r)
> &\Leftrightarrow(p\lor q)\land r\\
> (p\lor q)\land(p\lor r)
> &\Leftrightarrow p\lor(q\land r)
> \end{aligned}$$
>
> 两式均可**双向**使用；证明时可以“展开”，化简时一般优先“提取公因式”。

### 2. 否定相关等值律

| 名称 | 等值式 |
| --- | --- |
| **双重否定律** | $\neg\neg A\Leftrightarrow A$ |
| **德·摩根律（否定析取）** | $\neg(A\lor B)\Leftrightarrow\neg A\land\neg B$ |
| **德·摩根律（否定合取）** | $\neg(A\land B)\Leftrightarrow\neg A\lor\neg B$ |

> [!tip] 德·摩根律记忆法
> **否定进入括号，内部联结词互换，两个子式分别取否定。**
>
> $$\neg(A\lor B)\Leftrightarrow\neg A\land\neg B$$
> $$\neg(A\land B)\Leftrightarrow\neg A\lor\neg B$$
>
> 特别注意：$\neg(A\lor B)$ **不是** $\neg A\lor\neg B$。

### 3. 关于常量 0、1 的等值律

| 名称 | 等值式 | 含义 |
| --- | --- | --- |
| **零律** | $A\lor1\Leftrightarrow1$；$A\land0\Leftrightarrow0$ | 1 对析取、0 对合取起支配作用 |
| **同一律** | $A\lor0\Leftrightarrow A$；$A\land1\Leftrightarrow A$ | 0 对析取、1 对合取不改变结果 |
| **排中律** | $A\lor\neg A\Leftrightarrow1$ | $A$ 与其否定至少一真 |
| **矛盾律** | $A\land\neg A\Leftrightarrow0$ | $A$ 与其否定不可能同真 |

> [!warning] 零律与同一律容易记反
> - $\lor1$、$\land0$：**整个结果被锁死**，是零律。
> - $\lor0$、$\land1$：**保持原公式**，是同一律。
> - $A\lor\neg A$ 与 $A\land\neg A$ 体现排中律与矛盾律，不是零律。

### 4. 蕴涵与等价联结词的等值律

| 名称 | 等值式 |
| --- | --- |
| **蕴涵等值式** | $A\to B\Leftrightarrow\neg A\lor B$ |
| **假言易位（逆否等值）** | $A\to B\Leftrightarrow\neg B\to\neg A$ |
| **归谬论** | $(A\to B)\land(A\to\neg B)\Leftrightarrow\neg A$ |
| **等价等值式** | $A\leftrightarrow B\Leftrightarrow(A\to B)\land(B\to A)$ |
| **等价否定等值式** | $A\leftrightarrow B\Leftrightarrow\neg A\leftrightarrow\neg B$ |

课件还列出下列关于蕴涵、等价联结词的结构性等值式：

$$A\to(B\to C)\Leftrightarrow(A\to B)\to(A\to C)$$

$$(A\leftrightarrow B)\leftrightarrow C\Leftrightarrow A\leftrightarrow(B\leftrightarrow C)$$

以及等价联结词的交换律：

$$A\leftrightarrow B\Leftrightarrow B\leftrightarrow A$$

**两种常用的等价联结词展开形式：**

$$\begin{aligned}
A\leftrightarrow B
&\Leftrightarrow(A\to B)\land(B\to A)\\
&\Leftrightarrow(A\land B)\lor(\neg A\land\neg B)
\end{aligned}$$

> [!important] 全章最重要的两条“消去公式”
> $$\boxed{A\to B\Leftrightarrow\neg A\lor B}$$
> $$\boxed{A\leftrightarrow B\Leftrightarrow(A\to B)\land(B\to A)}$$
>
> 学会消去 $\to,\leftrightarrow$，是证明常见等值式、化简公式、构造完备集的共同起点。

> [!example] 归谬论的推导
> $$\begin{aligned}
> (A\to B)\land(A\to\neg B)
> &\Leftrightarrow(\neg A\lor B)\land(\neg A\lor\neg B)\\
> &\Leftrightarrow\neg A\lor(B\land\neg B)\\
> &\Leftrightarrow\neg A\lor0\\
> &\Leftrightarrow\neg A
> \end{aligned}$$
>
> 含义：如果假设 $A$ 成立，会同时得到 $B$ 和 $\neg B$，那么 $A$ 只能为假。

### 5. 等值式的使用顺序：先消去，再整理

> [!tip] 常见化简思路
> 1. 出现 $\leftrightarrow$ 时，按需要转换为 $\to,\land$。
> 2. 出现 $\to$ 时，考虑 $A\to B\Leftrightarrow\neg A\lor B$。
> 3. 出现否定整个括号时，用德·摩根律把否定推进。
> 4. 通过交换、结合、分配、吸收律整理相同项。
> 5. 找到 $A\lor\neg A$ 或 $A\land\neg A$，化为 $1$ 或 $0$。
> 6. 用零律、同一律、幂等律收尾。
>
> **这是一种便于解题的策略，不是必须遵循的唯一顺序。** 有时直接用吸收律或逆否等值会更快。

---

## 四、等值演算的规则与证明方法

### 1. 等值式模式

基本等值式中的 $A,B,C$ 都是任意命题公式。以蕴涵等值式为例：

$$A\to B\Leftrightarrow\neg A\lor B$$

取 $A=p\lor q\lor r$，$B=p\land q$，得到：

$$(p\lor q\lor r)\to(p\land q)\Leftrightarrow\neg(p\lor q\lor r)\lor(p\land q)$$

### 2. 代入规则

> [!important] 代入规则
> 如果 $T$ 是重言式，将 $T$ 中**同一个命题变项的所有出现**统一替换为**同一个命题公式**，所得公式仍是重言式。

例如已知 $p\leftrightarrow\neg\neg p$ 为重言式，将其中所有的 $p$ 统一替换成 $q\land r$：

$$(q\land r)\leftrightarrow\neg\neg(q\land r)$$

仍为重言式。

### 3. 置换规则

> [!important] 置换规则
> 若 $A\Leftrightarrow B$，则在任意较大公式中，把一个（或若干个）出现的子公式 $A$ 换成 $B$，得到的整个公式仍与原公式等值。

例如：

$$\begin{aligned}
((p\lor q)\land p)\lor(p\land r)
&\Leftrightarrow p\lor(p\land r) &&\text{吸收律}\\
&\Leftrightarrow p &&\text{吸收律}
\end{aligned}$$

这里是在更大公式的**局部**应用已知等值式。

### 4. 代入规则与置换规则的比较

| 比较角度 | 代入规则 | 置换规则 |
| --- | --- | --- |
| 主要用途 | 从**重言式模式**产生新的重言式 | 对**任意公式的等值子式**进行变形 |
| 被操作的对象 | 命题变项 | 子公式 |
| 用来替换的内容 | 任意命题公式 | 与原子公式等值的公式 |
| 替换范围 | 同一命题变项的**全部出现** | 可只替换子公式的**部分出现** |
| 保证的结果 | 仍为重言式 | 变形前后整体等值 |

> [!warning] 关键区别
> **代入要求“同一变项、统一代换”**；置换允许只处理某个局部。例如已知 $p\Leftrightarrow\neg\neg p$，把公式 $p\land p$ 的左边一个 $p$ 置换为 $\neg\neg p$，得到 $(\neg\neg p)\land p$，二者仍等值；但这不应误称为“对重言式中的所有 $p$ 实行代入”。

### 5. 等值演算的常用证明

> [!example] 证明一：蕴涵与析取的转换
> $$\begin{aligned}
> (p\land q)\to r
> &\Leftrightarrow\neg(p\land q)\lor r &&\text{蕴涵等值式}\\
> &\Leftrightarrow(\neg p\lor\neg q)\lor r &&\text{德·摩根律}\\
> &\Leftrightarrow\neg p\lor\neg q\lor r &&\text{结合律}
> \end{aligned}$$
>
> 得到：$\boxed{(p\land q)\to r\Leftrightarrow\neg p\lor\neg q\lor r}$。

> [!example] 证明二：蕴涵的嵌套等值
> $$\begin{aligned}
> p\to(q\to r)
> &\Leftrightarrow\neg p\lor(\neg q\lor r)\\
> &\Leftrightarrow\neg p\lor\neg q\lor r
> \end{aligned}$$
>
> 又因为：
>
> $$\begin{aligned}
> (p\land q)\to r
> &\Leftrightarrow\neg(p\land q)\lor r\\
> &\Leftrightarrow\neg p\lor\neg q\lor r
> \end{aligned}$$
>
> 故：
>
> $$\boxed{p\to(q\to r)\Leftrightarrow(p\land q)\to r}$$

> [!example] 证明三：另一种嵌套形式
> 证明 $p\to(q\to r)\Leftrightarrow(p\to q)\to(p\to r)$。
>
> $$\begin{aligned}
> (p\to q)\to(p\to r)
> &\Leftrightarrow\neg(\neg p\lor q)\lor(\neg p\lor r)\\
> &\Leftrightarrow(p\land\neg q)\lor\neg p\lor r\\
> &\Leftrightarrow(p\lor\neg p\lor r)\land(\neg q\lor\neg p\lor r)\\
> &\Leftrightarrow1\land(\neg p\lor\neg q\lor r)\\
> &\Leftrightarrow\neg p\lor\neg q\lor r
> \end{aligned}$$
>
> 这与 $p\to(q\to r)$ 的化简结果相同，因此二者等值。倒数第二步使用**排中律及同一律**。

### 6. 判定公式类型：将公式化为 0 或 1

> [!example] 例一：证明公式为重言式
> 判断 $q\lor\neg((\neg p\lor q)\land p)$ 的类型。
>
> 先化简括号：
>
> $$\begin{aligned}
> (\neg p\lor q)\land p
> &\Leftrightarrow(\neg p\land p)\lor(q\land p)\\
> &\Leftrightarrow0\lor(p\land q)\\
> &\Leftrightarrow p\land q
> \end{aligned}$$
>
> 再化简全式：
>
> $$\begin{aligned}
> q\lor\neg((\neg p\lor q)\land p)
> &\Leftrightarrow q\lor\neg(p\land q)\\
> &\Leftrightarrow q\lor\neg p\lor\neg q\\
> &\Leftrightarrow\neg p\lor(q\lor\neg q)\\
> &\Leftrightarrow\neg p\lor1\\
> &\Leftrightarrow1
> \end{aligned}$$
>
> 因此是**重言式**。

> [!example] 例二：证明公式为矛盾式
> $$\begin{aligned}
> (p\lor\neg p)\to((q\land\neg q)\land r)
> &\Leftrightarrow1\to(0\land r)\\
> &\Leftrightarrow1\to0\\
> &\Leftrightarrow\neg1\lor0\\
> &\Leftrightarrow0
> \end{aligned}$$
>
> 因此是**矛盾式**。

### 7. 两道综合等值证明

> [!example] 综合题一：提取公共因子
> 证明：
>
> $$(\neg p\land(\neg q\land r))\lor(q\land r)\lor(p\land r)\Leftrightarrow r$$
>
> $$\begin{aligned}
> &\quad(\neg p\land\neg q\land r)\lor(q\land r)\lor(p\land r)\\
> &\Leftrightarrow[(\neg p\land\neg q)\lor q\lor p]\land r\\
> &\Leftrightarrow[\neg(p\lor q)\lor(p\lor q)]\land r\\
> &\Leftrightarrow1\land r\\
> &\Leftrightarrow r
> \end{aligned}$$
>
> 核心技巧：**先提取公共项 $r$，再构造 $A\lor\neg A$**。

> [!example] 综合题二：构造排中律
> 证明下式为重言式：
>
> $$E=((p\lor q)\land\neg(\neg p\land(\neg q\lor\neg r)))\lor(\neg p\land\neg q)\lor(\neg p\land\neg r)$$
>
> 令 $X=p\lor q$，$Y=p\lor r$。由德·摩根律与分配律：
>
> $$\begin{aligned}
> \neg(\neg p\land(\neg q\lor\neg r))
> &\Leftrightarrow p\lor(q\land r)\\
> &\Leftrightarrow(p\lor q)\land(p\lor r)\\
> &\Leftrightarrow X\land Y
> \end{aligned}$$
>
> 又有 $\neg p\land\neg q\Leftrightarrow\neg X$，$\neg p\land\neg r\Leftrightarrow\neg Y$，从而：
>
> $$\begin{aligned}
> E&\Leftrightarrow[X\land(X\land Y)]\lor\neg X\lor\neg Y\\
> &\Leftrightarrow(X\land Y)\lor\neg(X\land Y)\\
> &\Leftrightarrow1
> \end{aligned}$$
>
> 技巧：为较大的重复结构**引入辅助记号**，可显著减少书写量。

### 8. 等值演算的三类典型任务

| 题目要求 | 常用目标 | 解题重点 |
| --- | --- | --- |
| 证明 $A\Leftrightarrow B$ | 将两边化为同一式 | 每一步有等值依据 |
| 判断公式类型 | 化为常量 $1$、$0$，或给出真、假赋值 | 排中律、矛盾律、零律 |
| 求实际条件的唯一解 | 符号化约束、删去不可能情形 | 约束不能遗漏，如“互不并列” |

---

## 五、真值函数与所有可能的联结词

### 1. 真值函数的定义

一个 $n$ 元真值函数是从 $n$ 个真值输入到一个真值输出的函数：

$$\boxed{F:\{0,1\}^{n}\to\{0,1\}}$$

在命题逻辑中，**每个确定的联结词（或命题公式）都有对应的真值函数**。对于固定的一组 $n$ 个变项，一个真值函数由其真值表输出列唯一确定。

### 2. 为什么 $n$ 元真值函数共有 $2^{2^n}$ 个

- $n$ 个变项的真值指派有 $2^n$ 种，因此真值表有 $2^n$ 行。
- 对每一行，函数输出都可独立地选择 0 或 1，选择数为 2。
- 所以一共有：

$$\boxed{\underbrace{2\times2\times\cdots\times2}_{2^n\text{ 个}}=2^{2^n}}$$

| 元数 $n$ | 真值表输入组合数 $2^n$ | 不同真值函数数 $2^{2^n}$ |
| :---: | :---: | :---: |
| 1 | 2 | 4 |
| 2 | 4 | 16 |
| 3 | 8 | 256 |

> [!warning] 两个“指数”不能混淆
> **$2^n$ 是输入组合（真值指派）的数量；$2^{2^n}$ 是所有可能的输出列（真值函数）的数量。** 二元联结词对应四种输入，因此有 $2^4=16$ 种可能真值函数，而不是 4 种。

### 3. 一元真值函数：只有四种

| $p$ | 恒假 $F_1$ | 恒等 $F_2=p$ | 否定 $F_3=\neg p$ | 恒真 $F_4$ |
| :---: | :---: | :---: | :---: | :---: |
| 0 | 0 | 0 | 1 | 1 |
| 1 | 0 | 1 | 0 | 1 |

### 4. 二元真值函数：16 种全部列出

规定指派顺序始终是 $(p,q)=(0,0),(0,1),(1,0),(1,1)$。表格中的 **输出序列** 按这个顺序写出四位真值。

| 输出序列 | 相应真值函数／逻辑表达式 | 说明 |
| :---: | --- | --- |
| `0000` | $0$ | 永假 |
| `0001` | $p\land q$ | 合取 |
| `0010` | $p\land\neg q$ | $p\to q$ 的否定 |
| `0011` | $p$ | 取第一个输入 |
| `0100` | $\neg p\land q$ | $q\to p$ 的否定 |
| `0101` | $q$ | 取第二个输入 |
| `0110` | $p\mathbin{\nabla}q$ | 不可兼或（异或） |
| `0111` | $p\lor q$ | 析取 |
| `1000` | $p\downarrow q$ | 或非 |
| `1001` | $p\leftrightarrow q$ | 等价 |
| `1010` | $\neg q$ | 否定第二个输入 |
| `1011` | $q\to p$ | 反向蕴涵 |
| `1100` | $\neg p$ | 否定第一个输入 |
| `1101` | $p\to q$ | 蕴涵 |
| `1110` | $p\uparrow q$ | 与非 |
| `1111` | $1$ | 永真 |

其中 `0001` 表示仅在 $p=q=1$ 时输出 1，而 `1110` 表示除 $p=q=1$ 外输出均为 1。

### 5. 四种新增的二元联结词

| 名称 | 课件符号 | 定义 | 何时为真 |
| --- | --- | --- | --- |
| **不可兼或（异或）** | $p\nabla q$ | $\neg(p\leftrightarrow q)$ | 两个输入真值不同 |
| **蕴涵否定** | $p\not\to q$ | $\neg(p\to q)$ | 仅 $p=1,q=0$ |
| **与非（NAND）** | $p\uparrow q$ | $\neg(p\land q)$ | 除两者都真外 |
| **或非（NOR）** | $p\downarrow q$ | $\neg(p\lor q)$ | 仅两者都假 |

> [!note] 符号说明
> 课件采用 $\nabla$ 表示“不可兼或”，采用在蕴涵符号上加否定标识表示“蕴涵否定”。由于不同字体中后一符号不完全统一，笔记以 $\not\to$ 表示，最稳妥的定义始终是 $\neg(p\to q)$。

其四种真值列为：

| $p$ | $q$ | $p\nabla q$ | $p\not\to q$ | $p\uparrow q$ | $p\downarrow q$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | 0 | 0 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 | 1 | 0 |
| 1 | 0 | 1 | 1 | 1 | 0 |
| 1 | 1 | 0 | 0 | 0 | 0 |

> [!note] 真值函数与主范式的联系
> 课件指出：一个给定真值函数可以由唯一的**主析取范式**和唯一的**主合取范式**（相对于固定的变项集合和顺序）来表示。由此可理解：即使原公式写法不同，只要真值函数相同，它们就逻辑等值。
>
> 这里仅建立联系，不展开主范式的系统求法；主范式计算应放在相关章节集中学习。

---

## 六、联结词完备集与极小完备集

### 1. 联结词完备集的定义

> [!important] 定义：联结词完备集
> 设 $S$ 是一个联结词集合。如果**任意命题公式**都能找到一个与之逻辑等值、且**只使用 $S$ 中联结词**的公式，则称 $S$ 为**联结词完备集（functionally complete set）**。

这意味着：即使只保留很少几种联结词，也可能表示所有命题真值函数。这里的“完备”指**表达能力足够**，不是说集合必须包含所有已知联结词。

> [!important] 定义：极小完备集
> 若 $S$ 是完备集，且 **$S$ 的任何真子集都不是完备集**，则称 $S$ 为**极小完备集**。
>
> 注意“极小”强调**删掉任一必要成员即不再完备**，不表示元素数一定最少。例如二元的极小完备集仍存在，而 $\{\uparrow\}$、$\{\downarrow\}$ 是只有一个元素的极小完备集。

### 2. 五种常用联结词并非缺一不可

从最常用的集合开始：

$$S_0=\{\neg,\land,\lor,\to,\leftrightarrow\}$$

利用：

$$A\to B\Leftrightarrow\neg A\lor B$$

$$A\leftrightarrow B\Leftrightarrow(A\to B)\land(B\to A)$$

可以将 $\to$、$\leftrightarrow$ 全部消去，因此：

$$\boxed{\{\neg,\land,\lor\}\text{ 是完备集}}$$

进一步使用德·摩根律：

$$A\lor B\Leftrightarrow\neg(\neg A\land\neg B)$$

$$A\land B\Leftrightarrow\neg(\neg A\lor\neg B)$$

于是得到两个**极小完备集**：

$$\boxed{\{\neg,\land\}\qquad\{\neg,\lor\}}$$

### 3. 为什么 $\{\neg,\to\}$ 是完备集

只需证明该集合可以表达已经知道完备的 $\{\neg,\lor\}$：

$$\boxed{p\lor q\Leftrightarrow\neg p\to q}$$

右侧只用到了 $\neg$ 和 $\to$，因此：

$$\boxed{\{\neg,\to\}\text{ 是完备集}}$$

如果需要合取，还可以：

$$p\land q\Leftrightarrow\neg(p\to\neg q)$$

> [!tip] 证明“是完备集”的通用路线
> **不必直接重建 16 种二元真值函数。** 只需在目标联结词集下表示出一组**已知完备**的联结词，例如 $\{\neg,\lor\}$ 或 $\{\neg,\land\}$，就可完成证明。

### 4. 为什么 $\{\neg,\leftrightarrow\}$ 不是完备集

课件给出的判据是：由 $p,q$ 构成、仅使用 $\neg,\leftrightarrow$ 的二元公式，其真值表中**1 的个数与 0 的个数均为偶数**（可能为 0、2 或 4）。

但 $p\land q$ 的输出列为 `0001`，有 **1 个 1 和 3 个 0**，不可能由此类公式表示。因此：

$$\boxed{\{\neg,\leftrightarrow\}\text{ 不是完备集}}$$

> [!note] 为什么这个判据可以用于证明
> 仅用 $\neg$ 与 $\leftrightarrow$ 构成的二元公式，真值列只会出现恒值、$p$、$q$、各自否定、异或及等价等形式；相应输出列的 1 的数量只能是 0、2 或 4，永远凑不出 $p\land q$ 的 1 个 1。
>
> **这个“偶数个”性质的前提是研究固定 $p,q$ 两个输入上的完整四行真值表**，不可脱离变量数和真值表范围随意推广。

### 5. 为什么 $\{\land,\lor,\to,\leftrightarrow\}$ 不是完备集

此集合的所有联结词都满足：**当输入全为 1 时，其输出为 1**。由这些联结词反复组成的任意公式，在全部命题变项取 1 时也必为 1。

但 $\neg p$ 在 $p=1$ 时输出 0，所以根本不可能用该集合表示 $\neg p$：

$$\boxed{\{\land,\lor,\to,\leftrightarrow\}\text{ 不是完备集}}$$

> [!tip] 证明“不是完备集”的通用路线
> 找出目标联结词集所具有的**共同性质**，证明这种性质在复合公式中始终保持，再举出一个**不满足该性质**的真值函数。
>
> 本例中的共同性质是“**全 1 输入必输出 1**”；而 $\neg p$ 构成反例。

单独的 $\{\land\}$、$\{\lor\}$、$\{\neg\}$、$\{\to\}$、$\{\leftrightarrow\}$ 均不是完备集。

### 6. 一个联结词就能构成完备集：与非、或非

**与非**定义：

$$p\uparrow q\Leftrightarrow\neg(p\land q)$$

先用与非表示否定：

$$\boxed{\neg p\Leftrightarrow p\uparrow p}$$

再用与非表示合取：

$$\boxed{p\land q\Leftrightarrow(p\uparrow q)\uparrow(p\uparrow q)}$$

因此 $\{\uparrow\}$ 能实现 $\{\neg,\land\}$，所以**与非单独就构成完备集**。

**或非**定义：

$$p\downarrow q\Leftrightarrow\neg(p\lor q)$$

同理：

$$\boxed{\neg p\Leftrightarrow p\downarrow p}$$

$$\boxed{p\lor q\Leftrightarrow(p\downarrow q)\downarrow(p\downarrow q)}$$

所以 $\{\downarrow\}$ 能实现 $\{\neg,\lor\}$，**或非单独也构成完备集**。

> [!important] 两个最值得记忆的单元素完备集
> $$\boxed{\{\uparrow\}\quad\text{与}\quad\{\downarrow\}}$$
>
> ==与非、或非都能单独表示所有命题公式==。证明时的核心是先构造**否定**，再构造**合取**或**析取**。

### 7. 联结词集判定速查

| 联结词集 | 是否完备 | 主要依据 |
| --- | :---: | --- |
| $\{\neg,\land,\lor,\to,\leftrightarrow\}$ | 是 | 原始常用集合 |
| $\{\neg,\land,\lor\}$ | 是 | 可消去 $\to,\leftrightarrow$ |
| $\{\neg,\land\}$ | 是 | 德·摩根律构造 $\lor$ |
| $\{\neg,\lor\}$ | 是 | 德·摩根律构造 $\land$ |
| $\{\neg,\to\}$ | 是 | $p\lor q\Leftrightarrow\neg p\to q$ |
| $\{\uparrow\}$ | 是 | 构造 $\neg$ 和 $\land$ |
| $\{\downarrow\}$ | 是 | 构造 $\neg$ 和 $\lor$ |
| $\{\neg,\leftrightarrow\}$ | 否 | 二元真值列的 1 数量只能为偶数 |
| $\{\land,\lor,\to,\leftrightarrow\}$ | 否 | 全 1 输入时必输出 1 |
| $\{\land\},\{\lor\},\{\neg\},\{\to\},\{\leftrightarrow\}$ | 否 | 各自表达能力不足 |

---

## 七、限定联结词集下的公式转换

### 1. 问题的本质

题目要求把 $C$ 写成仅由某集合 $S$ 中联结词构成的公式，且保持：

$$\boxed{C\Leftrightarrow C'}$$

这里 $C'$ 不能出现集合 $S$ 以外的联结词，但允许出现原命题变项与必要的括号。

### 2. 典型题：转换到 $S=\{\neg,\to\}$

将：

$$C=(p\land\neg q)\lor r$$

变成仅用 $\neg,\to$ 的公式。

**方法一：按课件的分配—消去路线。**

$$\begin{aligned}
C&=(p\land\neg q)\lor r\\
&\Leftrightarrow(p\lor r)\land(\neg q\lor r)\\
&\Leftrightarrow(\neg p\to r)\land(q\to r)\\
&\Leftrightarrow\neg\bigl(\neg(\neg p\to r)\lor\neg(q\to r)\bigr)\\
&\Leftrightarrow\boxed{\neg\bigl((\neg p\to r)\to\neg(q\to r)\bigr)}
\end{aligned}$$

**方法二：更简短的等值转换。**

因为 $p\land\neg q\Leftrightarrow\neg(p\to q)$，所以：

$$\begin{aligned}
C&\Leftrightarrow\neg(p\to q)\lor r\\
&\Leftrightarrow\boxed{(p\to q)\to r}
\end{aligned}$$

> [!important] 两种结果都正确
> 两个答案写法不同，但真值函数完全一样，都是所要求的 $\{\neg,\to\}$ 上的公式。**第二种更简洁**，考试通常优先选步数少且理由清楚的形式。

### 3. 限定联结词集题的检查方法

> [!tip] 两次检查
> **检查 1：联结词合法。** 最终公式中不能残留集合以外的 $\land,\lor,\leftrightarrow$ 等符号。
>
> **检查 2：真值等值。** 通过已知等值律逐步推导，必要时用真值表检验所有赋值。只检查最终结构而不检查等值是不够的。

---

## 八、逻辑等值式的应用题

### 1. 百米竞赛：由“各对一半”求名次

> [!example] 题意
> $A,B,C,D$ 四人参加百米比赛，没有并列名次。三人作出预测：
>
> - 甲：$C$ 第一，$B$ 第二。
> - 乙：$C$ 第二，$D$ 第三。
> - 丙：$A$ 第二，$D$ 第四。
>
> **每个人的两项判断恰好有一项正确**。求实际名次。

令 $A_i,B_i,C_i,D_i$ 分别表示相应选手获得第 $i$ 名（$i=1,2,3,4$）。

“恰好对一半”不是两个判断均真或均假，而是**恰好一个真**。因此有：

$$\begin{aligned}
\text{甲：}&\quad(C_1\land\neg B_2)\lor(\neg C_1\land B_2)\\
\text{乙：}&\quad(C_2\land\neg D_3)\lor(\neg C_2\land D_3)\\
\text{丙：}&\quad(A_2\land\neg D_4)\lor(\neg A_2\land D_4)
\end{aligned}$$

**推理：**

1. 假设 $D$ 不是第三，则按乙的预测 $C$ 必为第二。
2. $C$ 已为第二，故甲预测中的“$C$ 第一”为假，于是 $B$ 必须第二，与 $C$ 第二冲突。
3. 所以 $D$ **第三**，乙的另一个判断“$C$ 第二”为假。
4. $D$ 既然第三，就不是第四；根据丙的预测，$A$ **第二**。
5. $A$ 已第二，因此 $B$ 不可能第二；根据甲的预测，$C$ **第一**。
6. 剩下 $B$ 为第四。

$$\boxed{C\text{ 第一},\quad A\text{ 第二},\quad D\text{ 第三},\quad B\text{ 第四}}$$

> [!warning] 本题必须保留“无并列名次”条件
> 只列三名观众的判断还不够。推理过程中多次用到“同一人不能占两个名次”和“两人不能同时占同一个名次”。忽略这些约束可能得到不合理的候选解。

### 2. 土耳其商人与帽子：利用他人的沉默推理

> [!example] 题意
> 桌上有 **2 顶红帽子、3 顶黑帽子**。商人和两位应聘者各戴一顶；两位应聘者均看到商人戴着**红帽子**。过了一会儿，其中一人断言：“我戴的是黑帽子。”判断其推理是否成立。

**分析：**

- 已经看到商人戴红帽子，故两位应聘者中**至多一人**还能戴红帽子。
- 如果说话的人也戴红帽子，那么另一位应聘者就能看见**两顶红帽子**（商人与说话者），会立刻知道自己只能戴黑帽子。
- 题意是过了一会儿另一位仍未抢先回答；在**双方都会及时说出能够确定的答案**这一前提下，可排除“说话者戴红帽子”。
- 因而说话的人应戴**黑帽子**。

> [!note] 推理隐含的前提
> “沉默”本身不是逻辑联结词。上述判断需要假定另一位应聘者能看到所有人的帽子、正确推理，且一旦能确定便会作答。若没有这些行为条件，仅从“两人看见商人红帽”无法独立确定每人的帽色。

### 3. 趣味思考：只能问一个是非问题，且对方可能说谎

> [!question] 题意与条件辨析
> 一方手持黑色或白色围棋子，另一方只能问一个可回答“是/否”的问题；持子者可以说真话，也可以说假话。能否**保证**通过一个回答确定棋子的颜色？
>
> **按题面的字面条件，不能保证。** 如果回答者可以对同一个问题随意决定说真或说假，则一个“是”或“否”的回答并没有稳定的判别意义；必须再增加例如“始终诚实”或“始终撒谎”的一致性规则，才能构造通用问法。
>
> 若额外约定回答者属于**始终讲真话**或**始终撒谎**两类之一，可问：“**如果我问你‘棋子是白色的吗？’，你会回答‘是’吗？**”在此额外假设下，回答“是”对应白棋，“否”对应黑棋。这个附加设定不应误认为原题已经明确给出。

### 4. 信号优先输出线路

> [!example] 题意
> 线路有三个输入 $A,B,C$，优先级依次为 $A>B>C$。同一时刻最多允许**一个**输出信号：若多个输入同时出现，优先输出高优先级信号。要求在 $\{\neg,\land\}$ 中表示三个输出。

令 $p$ 表示 $A$ 有输入，$q$ 表示 $B$ 有输入，$r$ 表示 $C$ 有输入。

- **$A$ 的输出：** 只要 $A$ 输入，就一定优先选中它，不受 $B,C$ 影响。
- **$B$ 的输出：** 要求 $B$ 输入，且 $A$ 没有输入；$C$ 的情况无关。
- **$C$ 的输出：** 要求 $C$ 输入，且 $A,B$ 都没有输入。

$$\boxed{\begin{aligned}
F_A&=p\\
F_B&=\neg p\land q\\
F_C&=\neg p\land\neg q\land r
\end{aligned}}$$

它们只使用了允许的 $\neg,\land$，且不会出现两个输出同时为 1 的情况。

**完整输入/输出检验表：**

| $p$ | $q$ | $r$ | $F_A$ | $F_B$ | $F_C$ | 优先结果 |
| :---: | :---: | :---: | :---: | :---: | :---: | --- |
| 0 | 0 | 0 | 0 | 0 | 0 | 无输出 |
| 0 | 0 | 1 | 0 | 0 | 1 | $C$ |
| 0 | 1 | 0 | 0 | 1 | 0 | $B$ |
| 0 | 1 | 1 | 0 | 1 | 0 | $B$ |
| 1 | 0 | 0 | 1 | 0 | 0 | $A$ |
| 1 | 0 | 1 | 1 | 0 | 0 | $A$ |
| 1 | 1 | 0 | 1 | 0 | 0 | $A$ |
| 1 | 1 | 1 | 1 | 0 | 0 | $A$ |

> [!tip] 将“优先级”翻译成逻辑公式
> 某个输入能获得输出的条件是：**它自身有效，且所有比它优先级更高的输入全部无效**。用这一句话，就能直接写出本题三个公式，而不必先列很长的析取式再化简。

---

## 九、综合易错点与方法整理

### 1. 最容易混淆的六组概念

| 容易混淆 | 正确区分 |
| --- | --- |
| $A\leftrightarrow B$ / $A\Leftrightarrow B$ | 前者是新公式；后者表示逻辑等值关系 |
| 成真赋值 / 重言式 | 前者指**某一个**赋值下为真；后者指**所有**赋值下为真 |
| 重言式 / 可满足式 | 重言式包含在可满足式中，不是并列互斥关系 |
| 真值指派数 / 真值函数数 | 分别是 $2^n$ / $2^{2^n}$ |
| 代入规则 / 置换规则 | 统一代换全部同名变项 / 可以局部置换等值子式 |
| 完备集 / 极小完备集 | 能表达所有公式 / 还要求任何真子集都不完备 |

### 2. 常见解题错误

> [!warning] 错误检查清单
> 1. 将 $p\to q$ 误认为“前件为假时整个式子为假”。
> 2. 把 $p\to(q\to r)$ 写成 $(p\to q)\to r$，无视括号。
> 3. 把德·摩根律写成 $\neg(p\lor q)=\neg p\lor\neg q$。
> 4. 将 $A\lor\neg A$ 与 $A\land\neg A$ 的结果弄反。
> 5. 将“找到一个成真赋值”误当成“证明了重言式”。
> 6. 证明公式不等值时硬做完整真值表，而不先寻找反例。
> 7. 证明完备集时只列出若干例子，没有证明可构造一组已知完备的联结词。
> 8. 公式转换完毕后仍残留题目禁止使用的联结词。

### 3. 复习速查：公式最小核心集

> [!summary] 必须熟练调用的等值式
> $$\begin{aligned}
> A\to B&\Leftrightarrow\neg A\lor B\\
> A\leftrightarrow B&\Leftrightarrow(A\to B)\land(B\to A)\\
> \neg(A\land B)&\Leftrightarrow\neg A\lor\neg B\\
> \neg(A\lor B)&\Leftrightarrow\neg A\land\neg B\\
> A\lor\neg A&\Leftrightarrow1\\
> A\land\neg A&\Leftrightarrow0\\
> A\lor(A\land B)&\Leftrightarrow A\\
> A\land(A\lor B)&\Leftrightarrow A
> \end{aligned}$$
>
> **做证明题**：消去联结词 → 推进否定 → 交换结合分配 → 吸收与化常量。
>
> **做完备集题**：要证明“完备”就构造已知完备集；要证明“不完备”就寻找共同保留性质及反例。
>
> **做应用题**：先用命题变项表达全部约束，再检查唯一性和题目限定条件。

---

## 十、自测练习与答案

### A. 自测题

1. 不使用真值表，判断 $\neg(p\to q)\lor p$ 属于哪一类公式。
2. 证明 $(p\to q)\land(p\to\neg q)\Leftrightarrow\neg p$。
3. 判断 $p\to(q\to r)$ 与 $(p\to q)\to r$ 是否等值，并给出一种证明方法。
4. 一个四元真值函数具有多少种真值指派？一共有多少种不同的四元真值函数？
5. 说明 $\{\neg,\lor\}$ 为什么是完备集。
6. 把 $p\lor q$ 转换为只含 $\uparrow$ 的公式。
7. 按照 $A>B>C$ 优先级，若输入为 $(p,q,r)=(0,1,1)$，求 $(F_A,F_B,F_C)$。

### B. 参考答案与关键步骤

> [!example]- 参考答案（可折叠）
> **1.** $\neg(p\to q)\lor p\Leftrightarrow(p\land\neg q)\lor p\Leftrightarrow p$，是**可满足但非重言式**。
>
> **2.** $(\neg p\lor q)\land(\neg p\lor\neg q)\Leftrightarrow\neg p\lor(q\land\neg q)\Leftrightarrow\neg p$。
>
> **3.** 不等值。取 $(p,q,r)=(0,0,0)$：前者为 1，后者为 0。
>
> **4.** $2^4=16$ 种指派；$2^{16}=65536$ 种四元真值函数。
>
> **5.** 由德·摩根律，$p\land q\Leftrightarrow\neg(\neg p\lor\neg q)$。可构造 $\{\neg,\land,\lor\}$，因此完备。
>
> **6.** 先构造否定：$\neg p\Leftrightarrow p\uparrow p$。再由 $p\lor q\Leftrightarrow\neg(\neg p\land\neg q)$，得：
>
> $$p\lor q\Leftrightarrow(p\uparrow p)\uparrow(q\uparrow q)$$
>
> **7.** $F_A=p=0$；$F_B=\neg p\land q=1$；$F_C=\neg p\land\neg q\land r=0$。故 $(0,1,0)$，即输出 $B$。

