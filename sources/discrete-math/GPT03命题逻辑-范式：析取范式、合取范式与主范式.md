# 命题逻辑｜范式：析取范式、合取范式与主范式

> [!abstract] 本章知识主线
> **命题公式与真值表 → 逻辑等值 → 文字与简单式 → 析取/合取范式 → 极小项/极大项 → 主析取/主合取范式 → 相互转化 → 判断与实际应用。**
>
> 学会范式不是为了机械展开括号，而是为了把任意命题公式的真假情况转化为可计算、可比较、可检验的统一表达。

## 一、为什么需要范式

### 1. 从逻辑等值到标准形式

两个公式在所有相关命题变项的赋值下，真值都相同，就称为**逻辑等值**，记为 $A\Leftrightarrow B$。

$$
A\Leftrightarrow B\quad\Longleftrightarrow\quad A\leftrightarrow B\text{ 为重言式}
$$

例如：

$$
\begin{aligned}
p\to(q\to r)
&\Leftrightarrow\neg p\lor(\neg q\lor r)\\
&\Leftrightarrow\neg p\lor\neg q\lor r,\\
(p\land q)\to r
&\Leftrightarrow\neg(p\land q)\lor r\\
&\Leftrightarrow\neg p\lor\neg q\lor r.
\end{aligned}
$$

两个公式写法不同，但表示相同的真值函数。范式要做的事，就是将公式改写为结构受到限制的形式，便于统一处理。

> [!warning] “范式”与“主范式”的唯一性不同
> **一般析取范式、合取范式都不唯一**；固定命题变项集合及其顺序后，**主析取范式、主合取范式各自唯一**（不计项的排列顺序与重复书写）。
>
> 因此不能把“同一真值函数具有相同的标准型”误读成“所有普通范式都唯一”。

### 2. 需要掌握的前置概念

设公式含有 $n$ 个不同的命题变项 $p_1,p_2,\ldots,p_n$。

- **赋值（真值指派）**：为这些变项分别指定 $0$（假）或 $1$（真）。共有 $2^n$ 种。
- **成真赋值**：在该赋值下公式为 $1$。
- **成假赋值**：在该赋值下公式为 $0$。
- **重言式（永真式）**：每一种赋值都使公式为真。
- **矛盾式（永假式）**：每一种赋值都使公式为假。
- **可满足式**：至少存在一种成真赋值；因此**重言式也属于可满足式**。

> [!note] 记号约定
> 本文用 $0,1$ 表示假与真；用 $\neg,\land,\lor,\to,\leftrightarrow$ 表示否定、合取、析取、蕴涵、双条件；用 $\Leftrightarrow$ 表示两公式逻辑等值（它**不是**构造公式的联结词）。
>
> 在涉及 $p,q,r$ 的编号时，始终按 **$p,q,r$** 的顺序写二进制位：$p$ 为高位，$r$ 为低位。

### 3. 转化范式所需的等值律

| 名称 | 等值关系 | 作用 |
| --- | --- | --- |
| 蕴涵等值式 | $A\to B\Leftrightarrow\neg A\lor B$ | 消去 $\to$ |
| 等价等值式 | $A\leftrightarrow B\Leftrightarrow(A\to B)\land(B\to A)$ | 消去 $\leftrightarrow$ |
| 双重否定律 | $\neg\neg A\Leftrightarrow A$ | 消去双重否定 |
| 德·摩根律 | $\neg(A\land B)\Leftrightarrow\neg A\lor\neg B$ | 否定号内移 |
| 德·摩根律 | $\neg(A\lor B)\Leftrightarrow\neg A\land\neg B$ | 否定号内移 |
| 分配律 | $A\land(B\lor C)\Leftrightarrow(A\land B)\lor(A\land C)$ | 转析取范式 |
| 分配律 | $A\lor(B\land C)\Leftrightarrow(A\lor B)\land(A\lor C)$ | 转合取范式 |
| 排中律 | $A\lor\neg A\Leftrightarrow1$ | 补入缺失变项 |
| 矛盾律 | $A\land\neg A\Leftrightarrow0$ | 补入缺失变项、判矛盾 |
| 吸收律 | $A\lor(A\land B)\Leftrightarrow A$ | 化简析取式 |
| 吸收律 | $A\land(A\lor B)\Leftrightarrow A$ | 化简合取式 |
| 幂等律 | $A\lor A\Leftrightarrow A$，$A\land A\Leftrightarrow A$ | 去重 |

## 二、文字、简单式、普通范式

### 1. 文字（Literal）

**命题变项及其否定统称为文字**，例如 $p,\neg p,q,\neg r$。

- $p$ 为正文字；$\neg p$ 为负文字。
- $\neg(p\land q)$ 不是文字；需要先由德·摩根律改写。

### 2. 简单析取式与简单合取式

**简单析取式**：由有限个文字用 $\lor$ 连起来的公式。

$$
p\lor\neg q\lor r
$$

**简单合取式**：由有限个文字用 $\land$ 连起来的公式。

$$
p\land\neg q\land r
$$

单独一个文字既是简单析取式，也是简单合取式。

> [!important] 性质一：简单式判定
> - **简单析取式为重言式**，当且仅当同时包含某个变项及其否定，例如 $p\lor\neg p\lor q\Leftrightarrow1$。
> - **简单合取式为矛盾式**，当且仅当同时包含某个变项及其否定，例如 $p\land q\land\neg q\Leftrightarrow0$。

**为什么成立？** 对简单析取式，只要出现 $p\lor\neg p$，总有一个文字为真；若不存在正负配对，则可以把每个文字都赋为假，从而说明它不可能永真。简单合取式同理：正负配对无法同时为真；若不存在正负配对，则能让所有文字同时为真。

### 3. 析取范式（DNF）

由有限个**简单合取式**析取而成的公式，称为**析取范式**（Disjunctive Normal Form）。

$$
A=B_1\lor B_2\lor\cdots\lor B_k
$$

这里每个 $B_i$ 都是简单合取式。例如：

$$
(p\land q\land\neg r)\lor(p\land\neg q)\lor(p\land\neg p)
$$

虽含有矛盾项 $p\land\neg p$，它仍然具有析取范式的结构，只是可以进一步化简。

### 4. 合取范式（CNF）

由有限个**简单析取式**合取而成的公式，称为**合取范式**（Conjunctive Normal Form）。

$$
A=C_1\land C_2\land\cdots\land C_t
$$

这里每个 $C_i$ 都是简单析取式。例如：

$$
(p\lor q\lor\neg r)\land(p\lor\neg q)\land(p\lor\neg p)
$$

最后一项恒真，可删去而不改变整体真值。

| 比较 | 析取范式（DNF） | 合取范式（CNF） |
| --- | --- | --- |
| 整体联结词 | $\lor$ | $\land$ |
| 每一项的形式 | 简单合取式（$\land$） | 简单析取式（$\lor$） |
| 判断为真 | 至少有一项为真 | 所有项均为真 |
| 判断为假 | 所有项均为假 | 至少有一项为假 |
| 直观记忆 | ==外或内且== | ==外且内或== |

> [!tip] 识别范式：先看最外层
> $(p\land q)\lor(\neg p\land r)$：外面是“或”，每项里面是“且”→ 析取范式。
>
> $(p\lor q)\land(\neg p\lor r)$：外面是“且”，每项里面是“或”→ 合取范式。
>
> $p\lor q\lor\neg r$ 本身是一个简单析取式，因此也可以看作**只有一个项的合取范式**；每个文字都是简单合取式，因此它也是析取范式。两类范式并非完全互斥。

### 5. 范式存在定理及一般求法

> [!important] 范式存在定理
> **任意命题公式均存在与之逻辑等值的析取范式与合取范式。**

基本操作顺序：

1. **消去其他联结词**：将 $\to,\leftrightarrow$ 等转换为 $\neg,\land,\lor$。
2. **否定内移**：使用双重否定律及德·摩根律，让 $\neg$ 只直接作用于命题变项。
3. **按目标使用分配律**：求析取范式采用 $\land$ 对 $\lor$ 分配；求合取范式采用 $\lor$ 对 $\land$ 分配。
4. **按需化简**：用幂等律、吸收律、排中律、矛盾律消去多余项。

> [!warning] 分配律方向不能弄反
> - 求**析取**范式：$A\land(B\lor C)\Rightarrow(A\land B)\lor(A\land C)$。
> - 求**合取**范式：$A\lor(B\land C)\Rightarrow(A\lor B)\land(A\lor C)$。
>
> 这里的箭头表示演算方向，等式两边本质上是**逻辑等值**，并非单向逻辑推理。

### 6. 完整例题：同一公式的两种普通范式

> [!example] 例 1：求公式的析取范式与合取范式
> $$A=((p\lor q)\to r)\to p$$

先统一消去蕴涵：

$$
\begin{aligned}
A&\Leftrightarrow\neg\bigl(\neg(p\lor q)\lor r\bigr)\lor p\\
&\Leftrightarrow\bigl((p\lor q)\land\neg r\bigr)\lor p.
\end{aligned}
$$

**求析取范式**：

$$
\begin{aligned}
A&\Leftrightarrow(p\land\neg r)\lor(q\land\neg r)\lor p\\
&\Leftrightarrow\boxed{p\lor(q\land\neg r)}.
\end{aligned}
$$

第二步使用吸收律 $p\lor(p\land\neg r)\Leftrightarrow p$。

**求合取范式**：

$$
\begin{aligned}
A&\Leftrightarrow\bigl((p\lor q)\land\neg r\bigr)\lor p\\
&\Leftrightarrow(p\lor q\lor p)\land(\neg r\lor p)\\
&\Leftrightarrow\boxed{(p\lor q)\land(p\lor\neg r)}.
\end{aligned}
$$

这两个结果都正确；但还**不是主范式**，因为其中的简单项未必包含所有命题变项。

### 7. 对偶原理与两种范式的联系

在只含 $\neg,\land,\lor$ 和真值常量 $0,1$ 的公式中，把 $\land$ 与 $\lor$ 互换，同时把 $0$ 与 $1$ 互换（变项及其否定保持原样），得到原式的**对偶式**。

如果 $A\Leftrightarrow B$ 是一个有效的逻辑等值关系，那么对偶后的关系 $A^*\Leftrightarrow B^*$ 也成立。

例如合取对析取的分配律：

$$
A\land(B\lor C)\Leftrightarrow(A\land B)\lor(A\land C)
$$

取对偶式便得到析取对合取的分配律：

$$
A\lor(B\land C)\Leftrightarrow(A\lor B)\land(A\lor C).
$$

这说明**析取范式与合取范式的结构和求法具有对偶性**，也是极小项与极大项、主析取范式与主合取范式成对出现的原因之一。

> [!warning] 对偶不等于取否定
> 例如 $(p\land q)^*=p\lor q$，但 $\neg(p\land q)\Leftrightarrow\neg p\lor\neg q$。二者不能混为一谈。含 $\to,\leftrightarrow$ 的公式要先消去这些联结词，再按上述规则作对偶变换。

## 三、极小项与主析取范式

### 1. 极小项的定义

对固定的 $n$ 个命题变项，一个简单合取式若满足：

1. **每个变项都出现**；
2. 每个变项只以正文字或负文字之一出现，且**恰好一次**；
3. 按约定的变项顺序排列；

就称为一个**极小项（Minterm）**，记为 $m_i$。

例如固定变项为 $p,q,r$ 时：

$$
\neg p\land q\land\neg r
$$

是极小项；而 $p\land q$ 缺少 $r$，不能算极小项。

### 2. 极小项编号：正为 1，负为 0

把极小项中的正文字记为 $1$、负文字记为 $0$，得到一组二进制位；按固定顺序转换为十进制，下标就是 $i$。

例如：

$$
\neg p\land q\land\neg r\ \longrightarrow\ 010_2=2_{10}\ \longrightarrow\ m_2
$$

**三变项极小项完整对应表：**

| 编号 | 赋值 $(p,q,r)$ | 极小项 | 记号 |
| --- | --- | --- | --- |
| 0 | 000 | $\neg p\land\neg q\land\neg r$ | $m_0$ |
| 1 | 001 | $\neg p\land\neg q\land r$ | $m_1$ |
| 2 | 010 | $\neg p\land q\land\neg r$ | $m_2$ |
| 3 | 011 | $\neg p\land q\land r$ | $m_3$ |
| 4 | 100 | $p\land\neg q\land\neg r$ | $m_4$ |
| 5 | 101 | $p\land\neg q\land r$ | $m_5$ |
| 6 | 110 | $p\land q\land\neg r$ | $m_6$ |
| 7 | 111 | $p\land q\land r$ | $m_7$ |

> [!important] 极小项的三个核心性质
> 1. $n$ 个变项对应 ==$2^n$ 个极小项==。
> 2. 每个 $m_i$ **恰好在编号为 $i$ 的那一种赋值下为真**，其余均为假。
> 3. 所有极小项析取为重言式：
>
> $$
> m_0\lor m_1\lor\cdots\lor m_{2^n-1}\Leftrightarrow1.
> $$

进一步，不同的极小项不可能同时为真，所以若 $i\ne j$，有 $m_i\land m_j\Leftrightarrow0$。

### 3. 主析取范式（PDNF）

> [!important] 定义
> 在固定变项集合下，若一个公式的析取范式中**每个简单合取项都是极小项**，则称它为**主析取范式**（Principal DNF）。
>
> 任一命题公式都有主析取范式，且在固定变项集合和顺序后**唯一**（不计排列顺序）。

示例：

$$
(p\land\neg q\land\neg r)\lor(p\land q\land\neg r)\lor(p\land q\land r)
$$

是主析取范式，即 $m_4\lor m_6\lor m_7$；而

$$
(p\land q)\lor(\neg p\land\neg r)
$$

不是主析取范式，因为两个项都缺少一个变项。

用 $\sum$ 表示极小项的析取（**不是算术求和**）：

$$
\boxed{m_1\lor m_2\lor m_5\Leftrightarrow\sum(1,2,5)}
$$

### 4. 方法一：等值演算法求主析取范式

在获得普通析取范式后：

1. 对缺少变项 $x$ 的简单合取项 $B$，补入 $x\lor\neg x$；
2. 用分配律拆为 $(B\land x)\lor(B\land\neg x)$；
3. 对所有项重复，直至每项都恰有全部 $n$ 个变项；
4. 消去矛盾项与重复项，按编号排序。

基本原理是：

$$
B\Leftrightarrow B\land(x\lor\neg x)
\Leftrightarrow(B\land x)\lor(B\land\neg x).
$$

> [!example] 例 2：由普通析取范式推导主析取范式
> 沿用 $A=((p\lor q)\to r)\to p$，已求得
>
> $$A\Leftrightarrow p\lor(q\land\neg r).$$
>
> 对第一项 $p$ 补齐 $q,r$：
>
> $$
> \begin{aligned}
> p&\Leftrightarrow p\land(q\lor\neg q)\land(r\lor\neg r)\\
> &\Leftrightarrow m_4\lor m_5\lor m_6\lor m_7.
> \end{aligned}
> $$
>
> 对第二项 $q\land\neg r$ 补齐 $p$：
>
> $$
> \begin{aligned}
> q\land\neg r
> &\Leftrightarrow(p\lor\neg p)\land q\land\neg r\\
> &\Leftrightarrow m_6\lor m_2.
> \end{aligned}
> $$
>
> 合并并删除重复的 $m_6$：
>
> $$
> \boxed{A\Leftrightarrow m_2\lor m_4\lor m_5\lor m_6\lor m_7
> \Leftrightarrow\sum(2,4,5,6,7)}.
> $$

### 5. 方法二：真值表法求主析取范式

> [!tip] 最稳妥的考试方法
> **真值为 $1$ 的每一行，写一个同编号的极小项；最后用 $\lor$ 连起来。**
>
> 例如行 $101$ 的真值为 $1$，就取 $m_5=p\land\neg q\land r$。求编号时一定先固定变量顺序。

> [!example] 例 3：$(p\land q)\to r$
> 只有在 $p=q=1,r=0$，即 $110$ 时，蕴涵才为假，因此只有 $m_6$ 不出现。
>
> $$
> \boxed{(p\land q)\to r\Leftrightarrow
> \sum(0,1,2,3,4,5,7)}.
> $$

### 6. 主析取范式为何唯一

每个极小项只对应一种成真赋值。只要知道公式在哪些赋值下为真，就已经唯一确定了它要包含哪些极小项。

> [!note] 唯一性证明思路（反证法）
> 假设等值的两个主析取范式 $B,C$ 所含极小项集合不同。必有某个 $m_i$ 仅出现于其中一个范式中。令赋值取 $i$ 的二进制编码，则 $m_i$ 为真，其他极小项全为假，于是 $B,C$ 在此赋值下真值不同，矛盾。故它们只能包含相同的极小项。

> [!warning] 唯一性的前提
> 比较两个公式的主范式时，要先取它们所涉及变项的**并集**，统一变量集合。例如只含 $p$ 的公式 $p$，在变量集 $\{p\}$ 下写为 $m_1$，在变量集 $\{p,q\}$ 下写为 $m_2\lor m_3$；两种表示不矛盾。

## 四、极大项与主合取范式

### 1. 极大项的定义

对固定的 $n$ 个命题变项，一个简单析取式若满足：

1. **每个变项都出现**；
2. 每个变项的正文字与负文字恰好出现一个，且仅出现一次；
3. 按约定顺序排列；

就称为一个**极大项（Maxterm）**，记为 $M_i$。

例如 $p\lor\neg q\lor r$ 是在 $p,q,r$ 三个变项下的极大项；$p\lor\neg q$ 因缺少 $r$，不是极大项。

### 2. 极大项编号：正为 0，负为 1

和极小项恰好相反：极大项采用**正文字记 $0$，负文字记 $1$**。为什么？因为析取式想为假，里面每一个文字都必须为假：

- 正文字 $p$ 为假，需要 $p=0$；
- 负文字 $\neg p$ 为假，需要 $p=1$。

因此，极大项的编号二进制串，恰好就是**令它取假的赋值**。

例如：

$$
p\lor\neg q\lor r\ \longrightarrow\ 010_2=2_{10}\ \longrightarrow\ M_2.
$$

**三变项极大项完整对应表：**

| 编号 | 成假赋值 $(p,q,r)$ | 极大项 | 记号 |
| --- | --- | --- | --- |
| 0 | 000 | $p\lor q\lor r$ | $M_0$ |
| 1 | 001 | $p\lor q\lor\neg r$ | $M_1$ |
| 2 | 010 | $p\lor\neg q\lor r$ | $M_2$ |
| 3 | 011 | $p\lor\neg q\lor\neg r$ | $M_3$ |
| 4 | 100 | $\neg p\lor q\lor r$ | $M_4$ |
| 5 | 101 | $\neg p\lor q\lor\neg r$ | $M_5$ |
| 6 | 110 | $\neg p\lor\neg q\lor r$ | $M_6$ |
| 7 | 111 | $\neg p\lor\neg q\lor\neg r$ | $M_7$ |

> [!important] 极大项的三个核心性质
> 1. $n$ 个变项对应 ==$2^n$ 个极大项==。
> 2. 每个 $M_i$ **恰好在编号为 $i$ 的那一种赋值下为假**，其余均为真。
> 3. 所有极大项合取为矛盾式：
>
> $$
> M_0\land M_1\land\cdots\land M_{2^n-1}\Leftrightarrow0.
> $$

若 $i\ne j$，则 $M_i$ 和 $M_j$ 不可能同时为假，因此 $M_i\lor M_j\Leftrightarrow1$。

### 3. 极小项与极大项的对应关系

由德·摩根律，对同一下标的两个项有：

$$
\boxed{m_i\Leftrightarrow\neg M_i,\qquad M_i\Leftrightarrow\neg m_i.}
$$

例如（固定 $p,q,r$）：

$$
\begin{aligned}
m_2&=\neg p\land q\land\neg r,\\
\neg m_2&\Leftrightarrow p\lor\neg q\lor r=M_2.
\end{aligned}
$$

> [!warning] 最容易弄混的地方
> $m_2$ 和 $M_2$ 并不是使用相同正负号的合取式与析取式：它们是**互相否定**的两个公式。
>
> 对编号 $010$，$m_2$ 要在 $010$ **为真**；$M_2$ 要在 $010$ **为假**。因此前者是 $\neg p\land q\land\neg r$，后者是 $p\lor\neg q\lor r$。

### 4. 主合取范式（PCNF）

> [!important] 定义
> 在固定变项集合下，若一个公式的合取范式中**每个简单析取项都是极大项**，则称它为**主合取范式**（Principal CNF）。
>
> 任意命题公式都有主合取范式，且在固定变项集合和顺序后**唯一**（不计排列顺序）。

用 $\prod$ 表示极大项的合取（**不是算术连乘**）：

$$
\boxed{M_0\land M_2\land M_5\Leftrightarrow\prod(0,2,5)}.
$$

### 5. 方法一：等值演算法求主合取范式

先求出普通合取范式。若简单析取项 $C$ 缺少变项 $x$，则利用矛盾律补入 $x\land\neg x$：

$$
\begin{aligned}
C&\Leftrightarrow C\lor(x\land\neg x)\\
&\Leftrightarrow(C\lor x)\land(C\lor\neg x).
\end{aligned}
$$

之后消去重言项、重复文字、重复极大项，并排序编号。

> [!example] 例 4：由合取范式求主合取范式
> 继续考虑
>
> $$A=((p\lor q)\to r)\to p.$$
>
> 前面已得到
>
> $$A\Leftrightarrow(p\lor q)\land(p\lor\neg r).$$
>
> 第一项缺少 $r$：
>
> $$
> \begin{aligned}
> p\lor q
> &\Leftrightarrow(p\lor q)\lor(r\land\neg r)\\
> &\Leftrightarrow(p\lor q\lor r)\land(p\lor q\lor\neg r)\\
> &\Leftrightarrow M_0\land M_1.
> \end{aligned}
> $$
>
> 第二项缺少 $q$：
>
> $$
> \begin{aligned}
> p\lor\neg r
> &\Leftrightarrow(p\lor\neg r)\lor(q\land\neg q)\\
> &\Leftrightarrow(p\lor q\lor\neg r)\land(p\lor\neg q\lor\neg r)\\
> &\Leftrightarrow M_1\land M_3.
> \end{aligned}
> $$
>
> 合并去重后：
>
> $$
> \boxed{A\Leftrightarrow M_0\land M_1\land M_3
> \Leftrightarrow\prod(0,1,3)}.
> $$
>
> **校正注意**：主合取范式的极大项之间必须用 $\land$，不能写成 $M_0\lor M_1\lor M_3$。后者并不等值于原公式。

### 6. 方法二：真值表法求主合取范式

> [!tip] 关键规则
> **真值为 $0$ 的每一行，写一个同编号的极大项；最后用 $\land$ 连起来。**
>
> 与主析取范式正好相反：主析取从**真值为 $1$** 的行取项；主合取从**真值为 $0$** 的行取项。

> [!example] 例 5：$(p\land q)\to r$
> 唯一的成假赋值为 $110$，其下标为 $6$。
>
> 因此：
>
> $$
> \boxed{(p\land q)\to r\Leftrightarrow M_6
> =\neg p\lor\neg q\lor r\Leftrightarrow\prod(6)}.
> $$
>
> 特别注意：单独一个 $M_6$ 已经是主合取范式，不需要再增加其他项。

### 7. 方法三：由主析取范式直接构造主合取范式

假设整个固定变项集合共有 $2^n$ 个下标 $0,1,\ldots,2^n-1$。

- 先列出主析取范式**没有出现**的 $m_i$ 下标；
- 用这些下标写出同编号的 $M_i$；
- 将它们用 $\land$ 连接，即得主合取范式。

例如：

$$
A\Leftrightarrow\sum(1,3)\quad(n=2).
$$

全部下标为 $\{0,1,2,3\}$，缺少 $0,2$，因此：

$$
\boxed{A\Leftrightarrow\prod(0,2)=M_0\land M_2}.
$$

> [!warning] 为什么“下标取补集”，但不改变下标数字
> 需要互补的是 **出现的下标集合**，而不是把二进制 $0$ 与 $1$ 逐位翻转。
>
> 从 $\sum(1,3)$ 变成 $\prod(0,2)$，**不等于**把 $m_1,m_3$ 逐个换成 $M_1,M_3$。后者是 $\neg A$ 的主合取范式，而非 $A$ 的主合取范式。

## 五、两种主范式的内在关系

### 1. 一个公式对应两种互补的下标集合

设命题公式 $A$ 在固定 $n$ 个变项下：

- 成真赋值的编号集合为 $T$；
- 成假赋值的编号集合为 $F$；
- 全部编号集合为 $U=\{0,1,\ldots,2^n-1\}$。

则：

$$
T\cap F=\varnothing,\qquad T\cup F=U,\qquad F=U\setminus T.
$$

其主析取范式由 $T$ 中的极小项组成，主合取范式由 $F$ 中的极大项组成：

$$
\boxed{A\Leftrightarrow\bigvee_{i\in T}m_i
\Leftrightarrow\bigwedge_{j\in F}M_j.}
$$

> [!important] 互补定理
> 如果 $A$ 在固定变项集合下有主析取范式 $\sum T$，那么它的主合取范式就是 $\prod(U\setminus T)$。
>
> 反过来，若 $A\Leftrightarrow\prod F$，则 $A\Leftrightarrow\sum(U\setminus F)$。

**证明要点：** 没出现在 $A$ 主析取范式中的极小项，恰好描述 $\neg A$ 的全部成真赋值。因此，若

$$
\neg A\Leftrightarrow\bigvee_{j\in F}m_j,
$$

则两边取否定并用德·摩根律：

$$
\begin{aligned}
A&\Leftrightarrow\neg\left(\bigvee_{j\in F}m_j\right)\\
&\Leftrightarrow\bigwedge_{j\in F}\neg m_j\\
&\Leftrightarrow\bigwedge_{j\in F}M_j.
\end{aligned}
$$

### 2. $A$ 与 $\neg A$ 的主范式关系

在同一变项集合下：

$$
A\Leftrightarrow\sum T
\quad\Longrightarrow\quad
\neg A\Leftrightarrow\sum(U\setminus T).
$$

同理：

$$
A\Leftrightarrow\prod F
\quad\Longrightarrow\quad
\neg A\Leftrightarrow\prod(U\setminus F).
$$

即**$A$ 与 $\neg A$ 的主析取项集合互补，主合取项集合也互补**。

### 3. 例题：直接用一类主范式求另一类

> [!example] 例 6：$((p\to q)\land\neg p)\to\neg q$
> 固定 $p,q$ 两个变项，先化简：
>
> $$
> \begin{aligned}
> A&=((p\to q)\land\neg p)\to\neg q\\
> &\Leftrightarrow((\neg p\lor q)\land\neg p)\to\neg q\\
> &\Leftrightarrow\neg p\to\neg q\qquad\text{（吸收律）}\\
> &\Leftrightarrow p\lor\neg q.
> \end{aligned}
> $$
>
> $p\lor\neg q$ 只在 $(p,q)=(0,1)$，即下标 $1$ 下为假，故
>
> $$
> \boxed{A\Leftrightarrow M_1\Leftrightarrow\prod(1)}.
> $$
>
> 全部下标为 $0,1,2,3$；除 $1$ 外皆为成真赋值，因此
>
> $$
> \boxed{A\Leftrightarrow m_0\lor m_2\lor m_3
> \Leftrightarrow\sum(0,2,3)}.
> $$

### 4. 重言式、矛盾式与空范式

对于固定 $n$ 个变项：

| 公式类型 | 主析取范式 | 主合取范式 |
| --- | --- | --- |
| 重言式 $1$ | $\sum(0,1,\ldots,2^n-1)$ | $1$（空合取） |
| 矛盾式 $0$ | $0$（空析取） | $\prod(0,1,\ldots,2^n-1)$ |
| 既非永真亦非永假的可满足式 | 非空且不含全部极小项 | 非空且不含全部极大项 |

> [!note] 为什么空析取写成 $0$、空合取写成 $1$
> 析取的单位元是 $0$：$A\lor0\Leftrightarrow A$；合取的单位元是 $1$：$A\land1\Leftrightarrow A$。因此没有任何项的析取定义为 $0$，没有任何项的合取定义为 $1$。这是处理恒真和恒假公式所需的边界约定。

## 六、利用范式解决问题

### 1. 判断公式的类型

> [!important] 判定公式类型的充要条件
> - **重言式**：主析取范式包含全部 $2^n$ 个极小项；等价地，主合取范式是 $1$。
> - **矛盾式**：主析取范式是 $0$；等价地，主合取范式包含全部 $2^n$ 个极大项。
> - **可满足式**：主析取范式至少含一个极小项；等价地，主合取范式少于 $2^n$ 个极大项。

要区分“可满足式”与“非永真”：可满足式可能就是永真式；只有既可满足又不永真的公式，才有成真赋值、成假赋值两种。

> [!example] 例 7：三种公式类型
> **（1）矛盾式：**
>
> $$
> \begin{aligned}
> \neg(p\to q)\land q
> &\Leftrightarrow\neg(\neg p\lor q)\land q\\
> &\Leftrightarrow(p\land\neg q)\land q\\
> &\Leftrightarrow0.
> \end{aligned}
> $$
>
> **（2）重言式：**
>
> $$((p\to q)\land p)\to q.$$
>
> 这是假言推理的有效形式，在 $p,q$ 的四种赋值下都为真：
>
> $$\sum(0,1,2,3)\Leftrightarrow1.$$
>
> **（3）可满足但非重言：**
>
> $$
> (p\to q)\land q
> \Leftrightarrow q
> \Leftrightarrow\sum(1,3)
> \Leftrightarrow\prod(0,2).
> $$
>
> 因为有两种成真赋值和两种成假赋值，所以它既非重言式也非矛盾式。

### 2. 判断两个公式是否等值

步骤：

1. 找出两公式涉及的全部命题变项，统一顺序；
2. 求各自的主析取范式，或各自的主合取范式；
3. 比较两边的下标集合是否相同。

同一种主范式的下标集合相同，当且仅当两个公式逻辑等值。

> [!example] 例 8：比较两个带有双条件的公式
> $$
> A=p\leftrightarrow(q\leftrightarrow r),\qquad
> B=(p\leftrightarrow q)\leftrightarrow(p\leftrightarrow r).
> $$
>
> 按 $p,q,r$ 的顺序，求其主合取范式：
>
> $$
> A\Leftrightarrow\prod(0,3,5,6),
> $$
>
> $$
> B\Leftrightarrow\prod(1,2,5,6).
> $$
>
> 因为成假下标集合不相同，故 $\boxed{A\not\Leftrightarrow B}$。
>
> 也可以用一个反例迅速验证：$p=q=r=0$ 时，$A=0$、$B=1$，因而不可能等值。

> [!warning] 等值判定的常见混淆
> $\leftrightarrow$ 是公式内部的**双条件联结词**；$\Leftrightarrow$ 是说明**两个公式逻辑等值**的元语言记号。一个双条件公式本身未必为重言式。

### 3. 真值表与两类主范式互相转换

设 $F=(p\to q)\land q$。由等值演算可知 $F\Leftrightarrow q$，其真值表为：

| $p$ | $q$ | $F$ | 赋值编号 | 对应主范式项 |
| --- | --- | --- | --- | --- |
| 0 | 0 | **0** | 0 | $M_0$ |
| 0 | 1 | **1** | 1 | $m_1$ |
| 1 | 0 | **0** | 2 | $M_2$ |
| 1 | 1 | **1** | 3 | $m_3$ |

从真值表直接得：

$$
\boxed{F\Leftrightarrow\sum(1,3)\Leftrightarrow\prod(0,2)}.
$$

反过来，只要已知 $\sum(1,3)$，就可直接填写编号 $1,3$ 的真值为 $1$，其余为 $0$；已知 $\prod(0,2)$，则填写编号 $0,2$ 的真值为 $0$，其余为 $1$。

> [!tip] 真值表与主范式，四个字记忆
> - ==成真取小==：真值为 $1$ → 极小项 → 主析取。
> - ==成假取大==：真值为 $0$ → 极大项 → 主合取。
> - “小”项之间用 $\lor$；“大”项之间用 $\land$。
> - 由 $\sum$ 与 $\prod$ 互转，使用**编号补集**。

### 4. 实际问题：青年教师选派

> [!example] 例 9：用主析取范式求合法选派方案
> 某高校拟从青年教师 A、B、C 中选派 **1～2 人**进修，条件如下：
>
> - 如果 A 去，则 C 必须去；
> - 如果 B 去，则 C 不能去；
> - 如果 C 不去，则 A 或 B 中至少一人去。
>
> 问有哪些选派方案？

**第一步：命题符号化。**

令 $p$ 表示“A 去”，$q$ 表示“B 去”，$r$ 表示“C 去”。三个条件分别是：

$$
p\to r,\qquad q\to\neg r,\qquad\neg r\to(p\lor q).
$$

用合取表示所有条件同时成立：

$$
S=(p\to r)\land(q\to\neg r)\land(\neg r\to(p\lor q)).
$$

**第二步：分析两种情况。**

- 当 $r=1$（C 去）时，$q\to\neg r$ 迫使 $q=0$，而 $p$ 可为 $0$ 或 $1$，得到 $001$（只派 C）和 $101$（派 A、C）。
- 当 $r=0$（C 不去）时，$p\to r$ 迫使 $p=0$；$\neg r\to(p\lor q)$ 又迫使 $q=1$，得到 $010$（只派 B）。

**第三步：写出主析取范式。**

$$
\begin{aligned}
S\Leftrightarrow{}& (\neg p\land\neg q\land r)\\
&\lor(\neg p\land q\land\neg r)\\
&\lor(p\land\neg q\land r).
\end{aligned}
$$

$$
\boxed{S\Leftrightarrow m_1\lor m_2\lor m_5
\Leftrightarrow\sum(1,2,5)}.
$$

**结论：** 合法方案为 **只派 C、只派 B、派 A 和 C**，共三种。三种方案的人数均在 1～2 人范围内，因此额外人数要求也得到满足。

> [!note] 题目措辞与符号化边界
> 此处将第三条条件理解为“若 C 不去，A、B 至少一人必须去”，所以写成 $\neg r\to(p\lor q)$。如果日常语言中的“可以去”仅表示**允许**而非**必须**，那就不能自动得到这个蕴涵式；本例按照题目给定的逻辑约束求解。

## 七、四种方法与解题策略

### 1. 对照速查表

| 目标 | 优先选择的方法 | 具体操作 |
| --- | --- | --- |
| 求普通析取范式 | 等值演算 | 消联结词 → 否定内移 → $\land$ 对 $\lor$ 分配 |
| 求普通合取范式 | 等值演算 | 消联结词 → 否定内移 → $\lor$ 对 $\land$ 分配 |
| 求主析取范式 | 真值表法或补变量法 | 取成真行的 $m_i$，或将简单合取项补齐 |
| 求主合取范式 | 真值表法或补变量法 | 取成假行的 $M_i$，或将简单析取项补齐 |
| 两类主范式互转 | 编号补集 | 在 $\{0,\ldots,2^n-1\}$ 中取剩余下标 |
| 判定公式类型 | 比较项数或看空范式 | 全部真、全部假、至少一个真 |
| 判定等值 | 比较同一种主范式 | 固定同一变量集合，比较下标集合 |
| 应用题列举方案 | 命题符号化 + 主析取范式 | 每一个极小项对应一种可行赋值/方案 |

### 2. 常见失误集中排查

> [!warning] 易错点 1：把普通范式当作主范式
> $p\lor(q\land\neg r)$ 是析取范式，但不是在 $p,q,r$ 下的主析取范式。主范式**要求每个项都出现全部变量**。

> [!warning] 易错点 2：极大项的正负规则照搬极小项
> 极小项：**正 $1$，负 $0$**，下标对应成真赋值。
>
> 极大项：**正 $0$，负 $1$**，下标对应成假赋值。

> [!warning] 易错点 3：$\sum$、$\prod$ 记号与联结词不匹配
> $\sum$ 表示把 $m_i$ **析取**（$\lor$），$\prod$ 表示把 $M_i$ **合取**（$\land$）。绝不可将 $M_0\lor M_2$ 标成主合取范式；正确写法为 $M_0\land M_2$。

> [!warning] 易错点 4：忘记变量顺序和变量集合
> 编号 $010$ 在 $p,q,r$ 顺序下是 $p=0,q=1,r=0$。换一种变量顺序就可能得到不同下标。比较主范式时必须统一约定。

> [!warning] 易错点 5：混淆“可满足”与“非重言”
> 重言式至少有一个成真赋值，当然**可满足**。可满足的反面是**矛盾式**，不是重言式。

> [!warning] 易错点 6：转化时错用补集
> $\sum(1,3)$ 在二元变量集下是 $\prod(0,2)$，而不是 $\prod(1,3)$。不清楚变量个数时，先写出完整编号集合再取补集。

## 八、巩固练习（题目与答案分离）

### 练习题

**1. 识别范式。** 固定变项为 $p,q,r$，分别判断下列公式是否为析取范式、合取范式，以及是否为主范式。

- （a）$(p\land q)\lor\neg r$
- （b）$(p\lor q)\land(\neg p\lor r)$
- （c）$(p\land\neg q\land r)\lor(\neg p\land q\land\neg r)$

**2. 求两种主范式。** $A=p\to q$，按 $p,q$ 编号。

**3. 求两种主范式。** $B=p\leftrightarrow q$，按 $p,q$ 编号。

**4. 用补集转换。** 已知 $C\Leftrightarrow\sum(0,2,5,7)$，含 $p,q,r$ 三个变项，求主合取范式和 $\neg C$ 的主析取范式。

**5. 由公式判断方案。** 在 $p,q,r$ 下求 $D=p\land(q\lor r)$ 的主析取范式，并写出所有成真赋值。

### 参考答案

> [!example] 练习 1
> （a）是析取范式，不是合取范式；由于两项缺少变项，不是主析取范式。
>
> （b）是合取范式，不是析取范式；两个简单析取项均缺少一个变项，因此不是主合取范式。
>
> （c）两个简单合取项都包含 $p,q,r$，是主析取范式，编号分别为 $101_2=5$ 和 $010_2=2$：$\sum(2,5)$。

> [!example] 练习 2
> $p\to q$ 仅在 $p=1,q=0$，即 $10_2=2$ 时为假，其余为真。
>
> $$
> \boxed{A\Leftrightarrow\sum(0,1,3)\Leftrightarrow\prod(2)}.
> $$

> [!example] 练习 3
> $p\leftrightarrow q$ 当且仅当 $p,q$ 真值相同才为真，成真赋值为 $00,11$，成假赋值为 $01,10$。
>
> $$
> \boxed{B\Leftrightarrow\sum(0,3)\Leftrightarrow\prod(1,2)}.
> $$

> [!example] 练习 4
> 三变项的全部下标为 $\{0,1,2,3,4,5,6,7\}$，已知成真集合 $\{0,2,5,7\}$，其补集为 $\{1,3,4,6\}$。
>
> $$
> \boxed{C\Leftrightarrow\prod(1,3,4,6)},\qquad
> \boxed{\neg C\Leftrightarrow\sum(1,3,4,6)}.
> $$

> [!example] 练习 5
> 当 $p=1$ 且 $q,r$ 至少一人取 $1$ 时，$D$ 为真。因此成真赋值是 $101,110,111$。
>
> $$
> \boxed{D\Leftrightarrow\sum(5,6,7)}.
> $$

## 九、最后速查：一眼确定怎么写

> [!summary] 全章压缩记忆
> **形式结构：** 析取范式 = 简单合取项的析取；合取范式 = 简单析取项的合取。
>
> **主范式：** 普通范式 + 每项包含全部固定变项 = 主范式，且唯一。
>
> **极小项：** 正 $1$、负 $0$；仅在编号赋值下为真；$m_i$ 组合成 $\sum$。
>
> **极大项：** 正 $0$、负 $1$；仅在编号赋值下为假；$M_i$ 组合成 $\prod$。
>
> **真值表：** 真行取 $m_i$ 作析取；假行取 $M_i$ 作合取。
>
> **互补：** $m_i\Leftrightarrow\neg M_i$；同一公式的 $\sum$、$\prod$ 下标集合互补。
>
> **判定：** 主析取全项 = 永真；主析取无项 = 永假；主析取有项 = 可满足。

