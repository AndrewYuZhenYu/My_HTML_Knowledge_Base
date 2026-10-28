# 第五章 数组和广义表

> [!abstract] 本章知识主线
> **数组**解决“多下标元素怎样组织、怎样定位”；**矩阵的压缩存储**解决“怎样利用数据分布规律节省空间”；**稀疏矩阵**解决“非零元素少而分布不规则时怎样存储与运算”；**广义表**则把“线性表的元素”进一步推广为“原子或另一张表”。
>
> 学习顺序：数组的逻辑结构 → 多维数组与一维内存之间的映射 → 特殊矩阵下标变换 → 稀疏矩阵的三元组、快速转置和十字链表 → 广义表的递归定义、表头表尾、链式存储与递归运算。

> [!warning] 全章统一的下标约定
> 课件在不同例子中混用了**从 0 开始**与**从 1 开始**的下标。本文的数组地址公式、程序代码默认从 **0** 开始；遇到采用 **1** 开始的课后题，会专门注明。**不能把两种编号体系的公式直接混用。**

## 一、数组的逻辑结构与基本操作

### 1.1 数组的定义与特征

**数组（Array）**是有限个具有相同特性的数据元素的集合。一个元素由数组名与一组合法下标唯一确定。

- **一维数组**：可理解为元素具有顺序关系的线性表，如 $A=(a_0,a_1,\ldots,a_{n-1})$。
- **二维数组**：可理解为由 $m$ 个行向量构成的线性表，也可看成 $n$ 个列向量构成的线性表。
- **多维数组**：可以递归地看成元素为低一维数组的线性表。

例如，对于 $m$ 行、$n$ 列的数组 $A$，其元素为 $a_{ij}$，其中 $0\le i<m$、$0\le j<n$。每一组合法的 $(i,j)$ 恰好对应一个元素。

> [!note] 什么叫“数组是多维的结构”？
> 指数组元素需要多个下标才能定位，**不是**说内存本身具有多维形状。内存中的存储单元在地址意义上仍按一维顺序排列，这正是数组存储映射公式的由来。

### 1.2 数组的抽象数据类型（ADT）

用抽象数据类型描述数组，是为了刻画其**数据对象、数据关系和允许的操作**，并不意味着代码中要声明一个名为 `ADT` 的变量类型。

设 $n$ 维数组各维长度为 $b_1,b_2,\ldots,b_n$，则：

$$
D=\{a_{j_1j_2\cdots j_n}\mid 0\le j_i<b_i,\ 1\le i\le n\}
$$

数组包含各维方向上的相邻关系。以二维数组为例，可从两个维度理解：

- **列下标不变、行下标加 1**：$a_{ij}$ 与 $a_{i+1,j}$ 在行方向相邻。
- **行下标不变、列下标加 1**：$a_{ij}$ 与 $a_{i,j+1}$ 在列方向相邻。

课件使用 `ROW` 与 `COL` 描述这两类关系；其命名是对关系方向的描述，不需要强行对应于一种物理存储方式。

| 抽象操作 | 含义 | 使用条件 |
| --- | --- | --- |
| `InitArray` | 按维数和各维长度初始化数组 | 维数、维界合法 |
| `DestroyArray` | 销毁数组，释放其所占资源 | 数组已经建立 |
| `Value` | 根据下标读取指定元素 | 各维下标不越界 |
| `Assign` | 根据下标给指定元素赋值 | 各维下标不越界 |

这些名称是**课件中的 ADT 操作记法**，不是 C/C++ 自带函数；真正编程时应使用数组、容器或自己实现的具体函数。

对于传统的**固定维界数组**，创建后维数和各维长度保持不变，因此主要操作是**定位、访问与修改已有元素**，通常不讨论插入或删除一个数组位置。动态数组容器能够调整长度，但属于具体容器的扩容机制，不改变这里所研究的固定维界数组模型。

---

## 二、数组的顺序存储与地址计算

### 2.1 为什么必须约定存储次序？

二维数组在逻辑上按行、列排列，但要落到一段**连续的一维内存**中，必须先约定展开顺序。

| 存储方式 | 次序 | 二维数组示例 $2\times 3$ | 典型语言 |
| --- | --- | --- | --- |
| **行优先（行序为主序）** | 先存一整行，再存下一行 | $a_{00},a_{01},a_{02},a_{10},a_{11},a_{12}$ | C、C++ 内建二维数组 |
| **列优先（列序为主序）** | 先存一整列，再存下一列 | $a_{00},a_{10},a_{01},a_{11},a_{02},a_{12}$ | Fortran 的常规数组 |

设每个元素占 $L$ 字节，`LOC` 表示元素的起始地址，$\operatorname{LOC}(a_{00})$ 为基地址。**地址 = 基地址 + 前面元素的个数 $\times$ 单个元素大小。**

### 2.2 二维数组：行优先地址公式

对于 $A[m][n]$，行下标 $i$、列下标 $j$ 均从 0 开始：

- 第 $i$ 行之前共有 $i$ 行，每行 $n$ 个元素，共 $in$ 个。
- 第 $i$ 行内部，$a_{ij}$ 前还有 $j$ 个元素。

因此该元素在一维存储中的下标为：

$$
\boxed{k=in+j}
$$

存储地址为：

$$
\boxed{\operatorname{LOC}(a_{ij})=\operatorname{LOC}(a_{00})+(in+j)L}
$$

> [!example] 行优先地址计算
> 数组 $A[3][4]$ 中每个元素占 $4$ 字节，基地址为 $1000$，求 $a_{2,1}$ 的地址。
>
> $$
> k=2\times4+1=9
> $$
>
> $$
> \operatorname{LOC}(a_{2,1})=1000+9\times4=1036
> $$
>
> 含义：该元素之前已有 9 个元素，而非“地址加 9”。

### 2.3 二维数组：列优先地址公式

对于相同的 $A[m][n]$：

- 第 $j$ 列之前有 $j$ 列，每列 $m$ 个元素，共 $jm$ 个。
- 在第 $j$ 列内部，前面有 $i$ 个元素。

因此：

$$
\boxed{k=jm+i}
$$

$$
\boxed{\operatorname{LOC}(a_{ij})=\operatorname{LOC}(a_{00})+(jm+i)L}
$$

> [!warning] 行优先与列优先最易混淆的地方
> - 行优先：**行号乘列数**，即 $in+j$。
> - 列优先：**列号乘行数**，即 $jm+i$。
> - 不要把总行数 $m$ 与总列数 $n$ 互换。

### 2.4 $n$ 维数组的行优先映射

设数组维长为 $b_1,b_2,\ldots,b_n$，元素为 $a_{j_1j_2\cdots j_n}$，各维均从 0 开始。

$$
\boxed{
\begin{aligned}
k={}&j_1(b_2b_3\cdots b_n)\\
&+j_2(b_3b_4\cdots b_n)+\cdots+j_{n-1}b_n+j_n
\end{aligned}
}
$$

$$
\operatorname{LOC}(a_{j_1j_2\cdots j_n})
=\operatorname{LOC}(a_{0\cdots0})+kL
$$

本质上，**越靠前的维度变化一次，就要跨过越多元素**；最后一维变化一次只移动一个元素位置。

对于三维数组 $A[2][3][4]$：

$$
k=12i+4j+\ell
$$

例如 $A[1][2][3]$ 的下标：$k=1\times12+2\times4+3=23$。

另一种便于计算的**嵌套写法**为：

$$
k=(\cdots((j_1b_2+j_2)b_3+j_3)\cdots)b_n+j_n
$$

这与从左到右不断执行“已累计位置 $\times$ 当前维长 $+$ 当前下标”完全一致。

> [!tip] 反向还原二维下标
> 行优先的 $m\times n$ 数组中，已知一维下标 $k$：
>
> $$i=\left\lfloor\frac{k}{n}\right\rfloor,\qquad j=k\bmod n$$
>
> 这是把“一维坐标”还原成“行、列”，之后理解矩阵压缩存储的反向下标变换会更容易。

---

## 三、特殊矩阵的压缩存储

### 3.1 压缩存储的思想

对于特殊矩阵，如果矩阵元素中存在**规律性的重复值**或大量固定的零，就不必给每个逻辑位置都分配独立的存储单元。

- 具有重复值的若干位置，可以仅保存一次该值。
- 固定为零的逻辑位置可以不保存，读取时按照矩阵性质返回零。
- 需要建立**原矩阵行列下标 $(i,j)$ 与压缩数组下标 $k$ 的映射**。

> [!important] 所有压缩下标题的核心
> 先数**当前行之前已经存了多少元素**，再加上**当前行内还要跳过多少元素**。这一方法比机械背公式可靠。

### 3.2 对称矩阵

$n$ 阶矩阵 $A$ 满足：

$$
a_{ij}=a_{ji},\qquad 0\le i,j<n
$$

则称为**对称矩阵**。对角线两侧元素两两对应，因此只需保存**下三角（含主对角线）**或上三角中的一半。

总存储量从 $n^2$ 个元素变为：

$$
\boxed{\frac{n(n+1)}2}
$$

采用**下三角、行优先**时，各行分别存 $1,2,3,\ldots,n$ 个元素。

若 $i\ge j$：

$$
\boxed{k=\frac{i(i+1)}2+j}
$$

若 $i<j$，因为 $a_{ij}=a_{ji}$，改用对称位置 $(j,i)$：

$$
\boxed{k=\frac{j(j+1)}2+i}
$$

综合写成：

$$
\boxed{k=\frac{p(p+1)}2+q,\quad p=\max(i,j),\ q=\min(i,j)}
$$

> [!example] 对称矩阵下标变换
> 一个 $4\times4$ 对称矩阵，按下三角行优先存储。求 $a_{1,3}$ 的压缩位置。
>
> 将其映射为 $a_{3,1}$：
>
> $$k=\frac{3\times4}{2}+1=7$$
>
> **从 0 开始**的压缩数组第 7 号位置保存的是这一对对称元素的公共值。

### 3.3 上、下三角矩阵

**下三角矩阵**的严格上三角区域（$i<j$）全部为一个常数 $c$（常见情形为 $c=0$）。**上三角矩阵**则是严格下三角区域（$i>j$）全部为 $c$。

要保存的三角区域需要 $n(n+1)/2$ 个元素；如果外部区域是一个非零常数 $c$，可再用一个位置保存它：

$$
\boxed{\frac{n(n+1)}2+1\text{ 个存储单元}}
$$

若外部区域约定永远为零，可直接通过规则返回零，无须额外占用这个存储单元。

**下三角，行优先**（$i\ge j$）：

$$
\boxed{k=\frac{i(i+1)}2+j}
$$

**上三角，行优先**（$i\le j$）：第 $0,1,\ldots,i-1$ 行分别有 $n,n-1,\ldots,n-i+1$ 个元素，因此：

$$
\begin{aligned}
k&=\sum_{r=0}^{i-1}(n-r)+(j-i)\\
&=\boxed{\frac{i(2n-i+1)}2+j-i}
\end{aligned}
$$

> [!warning] 三角矩阵与对称矩阵不一样
> 对称矩阵的另一半通过“交换 $i,j$”找到相同值；三角矩阵的另一半**并不等于相对位置元素**，而是预定的常数 $c$。因此访问未压缩区域时，应返回 $c$，不能套用对称映射。

### 3.4 对角矩阵与三对角矩阵

课程中讨论的**带状对角矩阵**，只有主对角线及附近有限条对角线允许出现非零元素。最典型的是**三对角矩阵**：

$$
a_{ij}=0\qquad (|i-j|>1)
$$

可以存储的只有：

- 主对角线：$i=j$；
- 上邻对角线：$j=i+1$；
- 下邻对角线：$j=i-1$。

$n$ 阶三对角矩阵共有：

$$
\boxed{n+(n-1)+(n-1)=3n-2}
$$

个可能非零的位置。若按照**原矩阵的行序**存入 $B[0\ldots3n-3]$，且原矩阵的 $(i,j)$ 从 0 开始，在合法区域内：

$$
\boxed{k=2i+j\qquad(|i-j|\le1)}
$$

反过来，由 $k$ 还原位置：

$$
\boxed{i=\left\lfloor\frac{k+1}{3}\right\rfloor,\qquad j=k-2i}
$$

如果题目中的 $i,j$ 改成从 **1** 开始，而 $B[k]$ 仍从 **0** 开始，则：

$$
\boxed{k=2i+j-3}
$$

> [!example] 三对角矩阵的正向与反向定位
> $n=5$，给定**从 0 开始**的原矩阵位置 $(2,3)$：
>
> $$k=2\times2+3=7$$
>
> 反过来给定 $B[7]$：
>
> $$i=\left\lfloor\frac{7+1}{3}\right\rfloor=2,\quad j=7-2\times2=3$$
>
> 所以 $B[7]$ 对应 $a_{2,3}$，两次变换互相验证。

### 3.5 准对角矩阵：沿主对角线排列的 $2\times2$ 小方块

课程习题还包含由 $m$ 个 $2\times2$ 方块构成的 $2m$ 阶**准对角矩阵**。非零元只能出现在这些小方块内部，其余位置是零。

每个方块 4 个位置，一共只需 $4m$ 个位置。在每个小方块内部采用行优先次序、方块之间也按顺序存储。

当 $(i,j)$ 从 0 开始且属于同一个方块，即 $\lfloor i/2\rfloor=\lfloor j/2\rfloor$ 时：

$$
\boxed{k=4\left\lfloor\frac i2\right\rfloor+2(i\bmod2)+(j\bmod2)}
$$

不属于同一个方块的元素逻辑值为 0，不在压缩数组中占位置。

---

## 四、稀疏矩阵：存储、转置与链式结构

### 4.1 稀疏矩阵及稀疏因子

对于 $m$ 行、$n$ 列的矩阵，若非零元个数为 $t$，定义**稀疏因子**：

$$
\boxed{\delta=\frac{t}{mn}}
$$

$\delta$ 越小，非零元占比越低。课件给出 $\delta\le0.05$ 作为常见的稀疏判断参考；这是一种**经验阈值**，不是所有问题中统一的数学定义。

特殊矩阵和稀疏矩阵的区别：

| 比较点 | 特殊矩阵 | 稀疏矩阵 |
| --- | --- | --- |
| 主要特征 | 零元/重复元素的位置具有规律 | 非零元很少，通常没有简单位置规律 |
| 定位方法 | 套用下标变换公式 | 显式保存非零元位置，必要时借助索引 |
| 典型结构 | 对称矩阵、三角矩阵、三对角矩阵 | 三元组表、行位置表、十字链表 |
| 节省空间的依据 | 已知代数与分布性质 | 非零元数量 $t\ll mn$ |

> [!important] 稀疏矩阵存储的三个目标
> **少保存零元、少做无意义的零值运算、能够高效定位同一行或同一列的非零元。**

### 4.2 稀疏矩阵支持的基本运算

| 操作 | 核心功能 | 前提 |
| --- | --- | --- |
| 创建 / 销毁 | 建立、释放稀疏矩阵 | 维度等参数合法 |
| 输出 / 复制 | 输出或复制矩阵内容 | 源矩阵存在 |
| 加法 / 减法 | $Q=M\pm N$ | 两矩阵行数、列数分别相同 |
| 乘法 | $Q=MN$ | $M$ 的列数等于 $N$ 的行数 |
| 转置 | $T=M^\mathsf T$ | $T$ 行列数交换，$t$ 不变 |

课件以 `CreateSMatrix`、`DestroySMatrix`、`PrintSMatrix`、`CopySMatrix`、`AddSMatrix`、`SubSMatrix`、`MultSMatrix`、`TransSMatrix` 标记这些抽象操作；它们不是标准库现成函数。

### 4.3 顺序存储：三元组表

**三元组（Triple）**用三个信息完整描述一个非零元：

$$
\boxed{(i,j,v)}
$$

其中 $i$ 为行下标，$j$ 为列下标，$v$ 为元素值。把所有非零元按**原矩阵行优先**排列成连续的三元组表。

以 $5\times5$ 矩阵为例：

$$
M=\begin{bmatrix}
3&0&0&0&7\\
0&0&-1&0&0\\
-1&-2&0&0&0\\
0&0&0&0&0\\
0&0&0&2&0
\end{bmatrix}
$$

其三元组（**从 0 开始**）为：

| 顺序 | 行 $i$ | 列 $j$ | 值 $v$ |
| ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 3 |
| 1 | 0 | 4 | 7 |
| 2 | 1 | 2 | -1 |
| 3 | 2 | 0 | -1 |
| 4 | 2 | 1 | -2 |
| 5 | 4 | 3 | 2 |

此例 $t=6$。如果三项所占存储单元相同，三元组数据约需 $3t$ 个单元，另需少量空间保存行数、列数等元信息。真实程序中的结构体大小还受类型大小及内存对齐影响。

> [!warning] 两个编号体系必须分清
> 课件的三元组举例经常以 $(1,1)$ 作为第一个位置，并预留 `data[0]`；下文的 C++ 程序统一采用 $(0,0)$ 为第一个位置、`data[0]` 为第一条有效三元组。二者**只差编号规则**，不是矩阵含义不同。

#### 为什么不能直接照抄课件中的三元组结构定义？

课件的相关示例把三元组数组与 `mu`、`nu`、`tu` 放入了同一个 **`union`**。但联合体成员**共享同一片内存**，写入矩阵行列数量会覆盖三元组数组中的相应数据。这与需要同时保存三元组表及矩阵元信息的目标矛盾。

**正确实现应使用普通的 `struct`**，而非 `union`；同时将未定义的抽象类型落实为 `int` 等真实元素类型。后面的完整可运行程序已按这一原则实现。

### 4.4 稀疏矩阵转置：为什么不能只交换行列下标？

转置的数学定义为：

$$
T_{ji}=M_{ij},\qquad M\in\mathbb{R}^{m\times n},\quad T\in\mathbb{R}^{n\times m}
$$

对三元组 $(i,j,v)$，只需要变成 $(j,i,v)$，**但转置结果还必须按新矩阵的行优先顺序排列**。如果只交换每条三元组的行列位置，结果通常不是有序的三元组表。

#### 方法一：普通转置（按原矩阵的列依次扫描）

核心流程：

1. 交换结果矩阵的行数、列数。
2. 从原矩阵第 0 列到第 $n-1$ 列依次处理。
3. 对每一列，完整扫描一次三元组表；凡列下标相同，就交换行、列后追加到结果表。

因为原三元组表本来按行优先有序，在处理同一原列时，先找到的原行号较小，因而其转置后的列号也较小，输出顺序天然正确。

- 总共扫描 $n$ 列，每列扫描 $t$ 个三元组。
- **时间复杂度：$O(nt)$**；这里 $n$ 是原矩阵列数，$t$ 是非零元个数。
- 额外存储主要用于结果三元组表。

#### 方法二：快速转置（统计列数 + 前缀和定位）

方法一的浪费在于“每列都重复扫描整张三元组表”。快速转置先算清楚结果表中各行的存放起点，原三元组便能够**逐条直接放到目的位置**。

需要两个辅助数组：

- `num[col]`：原矩阵第 `col` 列的非零元个数。
- `cpot[col]`：该列转换为转置结果中的一行后，**第一个非零元应放的位置**。

按课件使用的 **1-based 三元组下标**：

$$
\boxed{\operatorname{cpot}[1]=1}
$$

$$
\boxed{\operatorname{cpot}[c]=\operatorname{cpot}[c-1]+\operatorname{num}[c-1]\quad(c\ge2)}
$$

按本文**0-based 程序下标**：

$$
\boxed{\operatorname{start}[0]=0}
$$

$$
\boxed{\operatorname{start}[c]=\operatorname{start}[c-1]+\operatorname{count}[c-1]\quad(c\ge1)}
$$

这就是**前缀和**：某列的起始位置 = 所有前面列的非零元个数之和。

对于上面的 $5\times5$ 示例：

| 原列下标 `col` | 0 | 1 | 2 | 3 | 4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `count[col]` | 2 | 1 | 1 | 1 | 1 |
| `start[col]` 初始值 | 0 | 2 | 3 | 4 | 5 |

例如原三元组 $(2,1,-2)$：

1. 它在新矩阵中变成 $(1,2,-2)$。
2. 原列 `1` 在结果表中的起点为 `start[1]=2`。
3. 其位置使用后，`start[1]` 增加 1，指向该结果行的下一可用位置。

实际处理时，`start` 会在写入过程中变化，所以表中显示的是**写入前的起始值**，不能将写入后的变化误认为原始 `cpot` 表。

> [!important] 快速转置的复杂度
> 统计列频次 $O(t)$ + 计算前缀和 $O(n)$ + 定位写入 $O(t)$，因此：
>
> $$\boxed{T(n,t)=O(n+t)}$$
>
> 辅助计数、位置数组共为 $O(n)$；加上结果表则还需 $O(t)$。

### 4.5 完整 C++ 实现：三元组与两种转置算法

以下程序使用 **C++17**，所有三元组坐标均从 0 开始。它还生成“每一行的起始位置表”，以便理解后面的行逻辑链接顺序表。

**执行思路：** 三元组按行排序 → 普通转置反复按列查找 → 快速转置先统计列数、再求起始位置 → 同一个例子对比两种结果。

```cpp
#include <iostream>                             // 提供输出操作
#include <stdexcept>                            // 提供参数错误异常
#include <vector>                               // 连续存储三元组和辅助数组

struct Triple {                                  // 一个非零元素的三个信息
    int row;                                     // 从 0 开始的行下标
    int col;                                     // 从 0 开始的列下标
    int value;                                   // 该非零元素的具体数值
};

struct SparseMatrix {                            // 一个完整的稀疏矩阵
    int rows;                                    // 矩阵行数
    int cols;                                    // 矩阵列数
    std::vector<Triple> data;                   // 按行优先排列的非零元素
};

// 普通转置：依次扫描原矩阵的各列，每列遍历一次三元组表。
SparseMatrix ordinaryTranspose(const SparseMatrix& source) {
    SparseMatrix result{source.cols, source.rows, {}};  // 交换行数与列数
    for (int col = 0; col < source.cols; ++col) {      // 按原矩阵的列顺序处理
        for (const Triple& item : source.data) {        // 每一列都扫描所有非零元
            if (item.col == col) {                      // 找到属于本列的非零元
                result.data.push_back({item.col, item.row, item.value});
            }
        }
    }
    return result;                                     // 数据已按新矩阵行序排列
}

// 快速转置：计算每列非零元数量与其在结果中的起始下标。
SparseMatrix fastTranspose(const SparseMatrix& source) {
    SparseMatrix result{source.cols, source.rows,
                        std::vector<Triple>(source.data.size())}; // 预留所有位置
    std::vector<int> count(source.cols, 0);            // count[c] 为第 c 列非零元数
    std::vector<int> start(source.cols, 0);            // start[c] 为结果中第 c 行起点

    for (const Triple& item : source.data) {          // 第一遍扫描：统计每列数量
        ++count[item.col];                            // 原来的列就是转置后的行
    }
    for (int col = 1; col < source.cols; ++col) {     // 累计求出各列的起始位置
        start[col] = start[col - 1] + count[col - 1];   // 前缀和，采用从 0 开始的下标
    }
    for (const Triple& item : source.data) {          // 第二遍扫描：直接定位写入
        int position = start[item.col];               // 当前三元组在结果中的位置
        result.data[position] = {item.col, item.row, item.value};
        ++start[item.col];                            // 同一结果行的下一空位后移
    }
    return result;                                    // 结果仍保持行优先顺序
}

// 行位置表：rowStart[r] 表示第 r 行非零元的起始位置。
std::vector<int> buildRowStart(const SparseMatrix& matrix) {
    std::vector<int> rowStart(matrix.rows + 1, 0);  // 最后一个位置作结束哨兵
    for (const Triple& item : matrix.data) {       // 先统计每行的元素数
        ++rowStart[item.row + 1];                  // 数量暂存到下一格
    }
    for (int r = 1; r <= matrix.rows; ++r) {      // 将计数转换为前缀和
        rowStart[r] += rowStart[r - 1];           // 得到第 r 行的起始下标
    }
    return rowStart;                               // 第 r 行对应 [r, r+1) 区间
}

void printTriples(const SparseMatrix& matrix) {     // 按顺序输出非零元
    std::cout << matrix.rows << " x " << matrix.cols << '\n';
    for (const Triple& item : matrix.data) {       // 遍历每个三元组
        std::cout << '(' << item.row << ", " << item.col
                  << ", " << item.value << ")\n";
    }
}

int main() {
    SparseMatrix matrix{5, 5, {                    // 构造 5x5 的稀疏矩阵
        {0, 0, 3}, {0, 4, 7}, {1, 2, -1},
        {2, 0, -1}, {2, 1, -2}, {4, 3, 2}
    }};
    SparseMatrix slow = ordinaryTranspose(matrix);   // 使用普通三元组转置
    SparseMatrix fast = fastTranspose(matrix);       // 使用快速转置
    std::cout << "Ordinary transpose:\n";
    printTriples(slow);                              // 显示普通转置结果
    std::cout << "Fast transpose:\n";
    printTriples(fast);                              // 显示快速转置结果
    std::vector<int> starts = buildRowStart(matrix); // 生成原矩阵行位置表
    std::cout << "Row starts:";
    for (int position : starts) {                    // 输出每一行的起始位置
        std::cout << ' ' << position;
    }
    std::cout << '\n';
    return 0;
}
```

示例程序运行后，两种转置算法都应输出相同的六个非零元，顺序为：

$(0,0,3)$，$(0,2,-1)$，$(1,2,-2)$，$(2,1,-1)$，$(3,4,2)$，$(4,0,7)$。

> [!tip] 怎样判断“快速转置”是否真的正确？
> 不只检查六个数值有没有变化，还要检查：**新矩阵行、列对调；每个元素的行列互换；新三元组按行优先有序；非零元个数保持不变。**

### 4.6 行逻辑链接的顺序表

三元组表适合**按行连续遍历**，但要随机找到某一行的全部元素，如果没有辅助信息，往往需要从头查找。

改进方案：在三元组数据外增加**行位置表** `rpos`，存储每行第一个非零元的位置。

例如上例按 0 开始编号，可以采用长度为 $m+1$ 的数组：

$$
\operatorname{rowStart}=[0,2,3,5,5,6]
$$

任意一行 $r$ 的三元组恰好落在：

$$
\boxed{[\operatorname{rowStart}[r],\ \operatorname{rowStart}[r+1])}
$$

例如第 2 行占 $[3,5)$，对应两条三元组；第 3 行占 $[5,5)$，为空行。**空行并不会使这种表示方法失效。**

这种设计保留了顺序表存储紧凑的优点，也支持直接定位指定行。在实际程序中使用“每行起始偏移 + 末尾哨兵”比逐行扫描更方便。

### 4.7 行指针向量单链表

还可以为每一行建立一条链表：每个结点保存**列下标、元素值、指向同行下一个非零元的指针**；另设 $m$ 个行头指针。

- 好处：可以直接访问某一行的非零元素；局部插入和删除更方便。
- 局限：按列访问需要跨行查找，不够方便。
- 课件按理想化字段个数估算存储为 $3t+m$ 个单元；实际内存大小还取决于指针大小、对齐等因素。

把每一列建立链表也可得到**列指针向量单链表**，行访问与列访问的方便程度正好相反。

### 4.8 十字链表：同时建立行链与列链

**十字链表（行—列表示法）**把行链表、列链表结合起来：**同一个非零结点**既属于一条行链，也属于一条列链。

每个非零结点保存五个字段：

| 字段 | 作用 |
| --- | --- |
| `row` | 原矩阵中的行下标 |
| `col` | 原矩阵中的列下标 |
| `value` | 非零元的数值 |
| `right` | 同一行的下一个非零元 |
| `down` | 同一列的下一个非零元 |

此外配备两组表头：`rhead`（长度 $m$）和 `chead`（长度 $n$）。课件按字段个数估计所需存储为：

$$
\boxed{5t+m+n}
$$

与“两个独立链表各保存一套非零元”不同，十字链表的**非零元只创建一次**，两条链通过不同指针指向同一个结点。

> [!example] 查找 $(2,1)$ 位置的元素
> - 从 `rhead[2]` 沿 `right` 移动，可在第 2 行中寻找列号 `1`。
> - 从 `chead[1]` 沿 `down` 移动，也可在第 1 列中寻找行号 `2`。
> - 这两个路径最终应到达**同一个**值为 $-2$ 的结点，而不是两份副本。

### 4.9 完整 C++ 实现：十字链表的插入与双向遍历

以下程序实际建立十字链表，并展示**按行遍历**和**按列遍历**。教学重点是两个不同链表指针 `right` / `down` 如何连接同一个结点。

```cpp
#include <iostream>                             // 提供输入输出
#include <stdexcept>                            // 提供越界与重复元素异常
#include <vector>                               // 存放行、列的头指针

struct CrossNode {                               // 十字链表中的一个非零元
    int row;                                     // 所在行的下标
    int col;                                     // 所在列的下标
    int value;                                   // 非零元的数值
    CrossNode* right;                           // 指向本行的下一个非零元
    CrossNode* down;                            // 指向本列的下一个非零元
};

class OrthogonalMatrix {                        // 管理一张十字链表矩阵
private:
    int rows;                                    // 原矩阵行数
    int cols;                                    // 原矩阵列数
    std::vector<CrossNode*> rowHead;            // 每行链表的第一个结点
    std::vector<CrossNode*> colHead;            // 每列链表的第一个结点

public:
    OrthogonalMatrix(int r, int c)
        : rows(r), cols(c), rowHead(r > 0 ? r : 0, nullptr),
          colHead(c > 0 ? c : 0, nullptr) {
        if (r <= 0 || c <= 0) {                  // 非法维度不能构造矩阵
            throw std::invalid_argument("invalid matrix size");
        }
    }

    OrthogonalMatrix(const OrthogonalMatrix&) = delete; // 禁止默认浅拷贝
    OrthogonalMatrix& operator=(const OrthogonalMatrix&) = delete;

    void insert(int r, int c, int value) {       // 向指定位置插入非零元
        if (r < 0 || r >= rows || c < 0 || c >= cols || value == 0) {
            throw std::out_of_range("invalid nonzero element");
        }
        CrossNode** rowPosition = &rowHead[r];   // 沿当前行寻找插入位置
        while (*rowPosition != nullptr && (*rowPosition)->col < c) {
            rowPosition = &((*rowPosition)->right);
        }
        if (*rowPosition != nullptr && (*rowPosition)->col == c) {
            throw std::invalid_argument("duplicate matrix position");
        }
        CrossNode** colPosition = &colHead[c];   // 沿当前列寻找插入位置
        while (*colPosition != nullptr && (*colPosition)->row < r) {
            colPosition = &((*colPosition)->down);
        }
        CrossNode* node = new CrossNode{r, c, value, *rowPosition, *colPosition};
        *rowPosition = node;                     // 将结点接入行链表
        *colPosition = node;                     // 将同一个结点接入列链表
    }

    void printRows() const {                    // 沿行链表输出全部非零元
        for (int r = 0; r < rows; ++r) {        // 按原矩阵行序遍历
            std::cout << "Row " << r << ':';
            for (CrossNode* p = rowHead[r]; p != nullptr; p = p->right) {
                std::cout << " (" << p->col << ',' << p->value << ')';
            }
            std::cout << '\n';
        }
    }

    void printColumn(int c) const {             // 验证按列访问也十分方便
        if (c < 0 || c >= cols) {
            throw std::out_of_range("invalid column");
        }
        std::cout << "Column " << c << ':';
        for (CrossNode* p = colHead[c]; p != nullptr; p = p->down) {
            std::cout << " (" << p->row << ',' << p->value << ')';
        }
        std::cout << '\n';
    }

    ~OrthogonalMatrix() {                      // 每个结点只沿行链表释放一次
        for (CrossNode* first : rowHead) {     // 各行之间没有共享的结点
            while (first != nullptr) {
                CrossNode* next = first->right; // 保存下一个结点再释放当前结点
                delete first;
                first = next;
            }
        }
    }
};

int main() {
    OrthogonalMatrix matrix(5, 5);              // 创建 5x5 十字链表矩阵
    matrix.insert(0, 0, 3);                     // 插入六个示例非零元
    matrix.insert(0, 4, 7);
    matrix.insert(1, 2, -1);
    matrix.insert(2, 0, -1);
    matrix.insert(2, 1, -2);
    matrix.insert(4, 3, 2);
    matrix.printRows();                         // 分别按行遍历非零元素
    matrix.printColumn(0);                     // 查找第 0 列的两个非零元
    return 0;
}
```

代码中采用 `CrossNode**` 保存“准备被改写的指针所在位置”。它可以指向行头指针或已有结点的 `right` 字段，从而**用同一套逻辑处理头部插入与中间插入**。程序刻意禁止默认复制矩阵对象，是为了避免两个对象误认为自己独占同一批动态分配的结点而重复释放。

### 4.10 几种稀疏存储方式的选择

| 表示方法 | 主要特点 | 适合操作 | 主要局限 |
| --- | --- | --- | --- |
| 三元组顺序表 | 按行有序，连续存储，结构简单 | 顺序处理、转置 | 随机访问某一行需查找 |
| 行逻辑链接顺序表 | 三元组 + 行起始位置表 | 快速定位某行 | 动态插入删除可能移动后续数据 |
| 行指针单链表 | 每一行是一条链 | 按行处理、局部修改 | 不便直接按列处理 |
| 十字链表 | 一个结点同时串联到行链和列链 | 频繁按行/列处理、动态修改 | 指针多，维护更复杂 |

课件还列举了**带辅助行向量的二元组、伪地址表示、多链表示、散列存储**等名称，但未系统展开算法。当前以课件真正重点讲授的三元组、行位置表、行链表和十字链表为主，不把只提到名称的结构扩展成另一门课程。

---

## 五、广义表的定义、基本性质与表头表尾

### 5.1 广义表的递归定义

**广义表（Generalized List）**是线性表的推广：线性表中的元素通常作为单个数据对象处理，而广义表中的元素不仅可以是**原子**，还可以是**另一张广义表（子表）**。

记作：

$$
\boxed{LS=(\alpha_1,\alpha_2,\ldots,\alpha_n)}
$$

这里：

- $LS$：广义表的名称。
- $n$：广义表的**长度**，即最外层包含的元素个数。
- $\alpha_i$：第 $i$ 个元素，可能是一个不可再分的**原子（Atom）**，也可能是一个**子表（Sublist）**。

课件习惯使用**大写字母表示广义表名称**、**小写字母表示原子**。子表可以继续包含子表，因此广义表本身就是一种**递归定义的多层次线性结构**。

> [!example] 五个典型广义表
> 设：
>
> - $A=()$：空表。
> - $B=(e)$：含一个原子 $e$。
> - $C=(a,(b,c,d))$：含原子 $a$ 和子表 $(b,c,d)$。
> - $D=(A,B,C)$：含三张子表。
> - $E=(a,E)$：第二个元素再次引用自己，是递归表。
>
> 展开 $D$：
>
> $$D=((),(e),(a,(b,c,d)))$$
>
> 此处 $D$ 最外层有三个元素，**长度是 3**，而不是把内部所有原子加起来。

### 5.2 长度、深度与空表

**长度（Length）**：最外层逗号分隔的元素数量，子表无论内部含多少元素，都只算**一个**最外层元素。

**深度（Depth）**：最大层次的括号嵌套数量。课程约定：

$$
\boxed{\operatorname{Depth}(\text{原子})=0}
$$

$$
\boxed{\operatorname{Depth}(())=1}
$$

非空表的深度等于最深子元素的深度再加一：

$$
\boxed{\operatorname{Depth}(LS)=1+\max_i\operatorname{Depth}(\alpha_i)}
$$

可对照以下例子理解：

| 广义表 | 长度 | 深度 | 理由 |
| --- | ---: | ---: | --- |
| $A=()$ | 0 | 1 | 空表只有外层括号 |
| $B=(e)$ | 1 | 1 | 仅有一层括号 |
| $C=(a,(b,c,d))$ | 2 | 2 | 子表带来第二层括号 |
| $D=((),(e),(a,(b,c,d)))$ | 3 | 3 | 最深路径在最后一个子表内部 |
| $F=((()))$ | 1 | 3 | 三层括号，但最外层只有一个元素 |
| $G=((),())$ | 2 | 2 | 两个空表分别作为一个元素 |

> [!warning] 三个经常弄错的表达式
> - `()` 是**空表**，长度 0，深度 1。
> - `(())` 是**含一个空表的表**，长度 1，深度 2。
> - `((()))` 是**含一个 `(())` 子表的表**，长度 1，深度 3。
>
> `()` 和 `(())` 不是一回事；**空表作为元素时，仍要算作一个元素。**

### 5.3 广义表的共享与递归

广义表允许**共享子表**。例如 $D=(A,B,C)$，可以使 $D$ 的有关结点直接引用现有的 $A,B,C$，而不必复制这些子表。共享不同于递归：

- **共享**：多张表引用同一张已存在的子表，逻辑结构仍可为有限的非循环嵌套。
- **递归**：表的定义直接或间接引用自身，例如 $E=(a,E)$，会形成循环引用。

对于 $E=(a,E)$，最外层仍只有**两个元素**——原子 $a$ 和子表引用 $E$；但如果不断展开嵌套层次，会得到无限延伸：

$$
E=(a,(a,(a,\ldots)))
$$

因此课件强调：**递归表可以长度有限，但深度为无穷。** 不能把无限展开后的原子数量当成最外层的长度。

> [!note] 程序实现边界
> 后面的教学程序处理一般的、有限且无环的广义表表达式，如 `(a,(b,c))`。它没有把 `E=(a,E)` 这种**自引用结构**当作普通字符串反复展开；若需要表示自引用，则必须额外管理结点身份、循环和遍历终止条件。

### 5.4 表头（Head）与表尾（Tail）

对于任意**非空**广义表：

$$
LS=(\alpha_1,\alpha_2,\ldots,\alpha_n)
$$

其表头与表尾分别是：

$$
\boxed{\operatorname{Head}(LS)=\alpha_1}
$$

$$
\boxed{\operatorname{Tail}(LS)=(\alpha_2,\ldots,\alpha_n)}
$$

这两个操作在返回值类型上有一个关键差别：

- **表头**可以是原子，也可以是子表。
- **表尾一定是一张表**，即使它没有元素，也应写成空表 `()`。

> [!important] 记住表头、表尾的本质
> **Head 取出第一个元素；Tail 去掉第一个元素后，把剩余部分仍然用一对括号装起来。**
>
> 因此 $\operatorname{Tail}((a))=()$，而不是原子、空字符串或“不存在”。

> [!example] 连续拆解一个广义表
> 取 $C=(a,(b,c,d))$：
>
> $$\operatorname{Head}(C)=a$$
>
> $$\operatorname{Tail}(C)=((b,c,d))$$
>
> 对这个结果继续操作：
>
> $$\operatorname{Head}(\operatorname{Tail}(C))=(b,c,d)$$
>
> $$\operatorname{Tail}(\operatorname{Tail}(C))=()$$
>
> 第一次得到的 `((b,c,d))` 是**包含一个子表的表**；第二次 `Head` 才真正把子表 `(b,c,d)` 取出。

### 5.5 组合运算：先做内层，再做外层

给定：

$$
L=((a,b),(c,d))
$$

可以依次计算：

| 表达式 | 结果 | 解释 |
| --- | --- | --- |
| $\operatorname{Head}(L)$ | $(a,b)$ | 第一个元素本身是一张子表 |
| $\operatorname{Tail}(L)$ | $((c,d))$ | 只剩一张子表，需要保留外层括号 |
| $\operatorname{Head}(\operatorname{Tail}(L))$ | $(c,d)$ | 先得 `((c,d))`，再取其第一个元素 |
| $\operatorname{Tail}(\operatorname{Head}(L))$ | $(b)$ | 先得 `(a,b)`，再去掉 `a` |
| $\operatorname{Head}(\operatorname{Tail}(\operatorname{Head}(L)))$ | $b$ | 三次操作最后得到原子 |
| $\operatorname{Tail}(\operatorname{Head}(\operatorname{Tail}(L)))$ | $(d)$ | 最后得到只含原子 `d` 的表 |

> [!warning] 表头、表尾不是“取第一个字符、删第一个字符”
> 例如 `((a,b),(c,d))` 的第一个元素是整个 `(a,b)`，绝不能仅仅取出最左边的 `a`。运算应按**括号层级和最外层元素**进行。

### 5.6 广义表的抽象操作

从 ADT 角度，课件列出以下能力：

| 功能类别 | 对应操作 | 含义 |
| --- | --- | --- |
| 建立/销毁 | `InitGList`、`DestroyGList`、`CreateGList`、`CopyGList` | 创建、释放、解析、复制广义表 |
| 状态查询 | `GListLength`、`GListDepth`、`GListEmpty` | 查询长度、深度、是否为空 |
| 分解 | `GetHead`、`GetTail` | 取得表头或表尾 |
| 修改 | `InsertFirst_GL`、`DeleteFirst_GL` | 在表首插入/删除一个元素 |
| 遍历 | `Traverse_GL` | 访问表内的原子或子表 |

这些均为描述操作能力的**抽象接口名**。真实实现时，必须指定具体元素类型、结点结构、参数和内存管理方式。

---

## 六、广义表的链式存储结构

### 6.1 为什么顺序表不方便表示广义表？

普通顺序表的数据元素性质相对统一，按位置排列即可；广义表的元素则可能是：

- 原子（如 `a`）。
- 子表（如 `(b,c,d)`）。
- 空表（如 `()`）。
- 引用已有的子表，甚至引用自己。

因此一个位置保存的内容不仅要标明“是什么类型”，还需要能够**指向更深层次**的数据。课件主要使用**带类型标记的链式结点**来实现。

### 6.2 两种基本结点

**原子结点**保存实际原子，**表结点**负责指向子表或组织列表。通过标记域 `tag` 区分：

| 结点 | `tag` | 其他字段 | 意义 |
| --- | ---: | --- | --- |
| 原子结点 | 0 | `atom` | 保存一个具体原子 |
| 表结点 | 1 | `hp`、`tp` | `hp` 指向表头，`tp` 指向表尾或下一个相关结点 |

注意：`hp`、`tp` 的**准确含义依赖于采用哪种广义表分析法**，不是所有表示方法都能机械地把它们解释为同样的关系。

### 6.3 方法一：表头—表尾分析法

把一个非空广义表反复分解为**第一个元素（表头）**与**剩余元素组成的表（表尾）**。这是结构分解关系，而不是把 `Tail` 的一对括号当作一个新的最外层元素。

在这种表示法中：

- 每个**非空列表**的指针指向一个表结点。
- 表结点的 `hp` 指向第一个元素：可以是原子结点，也可以是另一个表结点。
- 表结点的 `tp` 指向该表剩余元素形成的列表；若为空表则指向空指针 `NIL`。
- 空表 `()` 本身用 `NIL` 表示。

以 $C=(a,(b,c,d))$ 为例：

1. 最外层第一结点的 `hp` 指向原子 `a`。
2. 第一结点的 `tp` 指向第二个表结点，表示只剩下一个元素 `(b,c,d)` 的外层表。
3. 第二结点的 `hp` 指向子表 `(b,c,d)` 的首个表结点。
4. 子表内部再用相同规则分解为原子 `b`、`c`、`d`。

这样一来，**外层有几个元素，就有几个属于该层次的表结点**。因此最外层沿 `tp` 走过的表结点数恰好是广义表长度。

> [!tip] 表头—表尾法的优点与不足
> - **优点**：`Head`、`Tail`、长度统计和递归遍历都很自然；可以直接对表尾递归处理。
> - **不足**：每个层次每个元素通常都需要表结点，结点数量较多。

### 6.4 方法二：子表分析法

另一种方法不必把每张非空表不断拆成独立的“表头 + 表尾”，而是围绕**一个表结点所包含的所有同级元素**组织链接。

在课件采用的子表分析结构中：

- **每个子表自身**用一个表结点表达，`hp` 指向该表的第一个元素。
- 同一层的不同元素通过 `tp` 串起来。
- 因此**原子结点也需要 `tp` 字段**，用来指向同层下一个元素。
- 空表可由 `hp`、`tp` 均为空的表结点表示。

以 $C=(a,(b,c,d))$ 为例，可以理解为：最外层表结点的 `hp` 连接到原子 `a`，原子 `a` 的 `tp` 再连接到代表子表 `(b,c,d)` 的表结点；该子表的 `hp` 则引出 `b→c→d` 的同级元素链。

> [!important] 两种方法的关键区别
> **表头—表尾法**：更强调“第一个元素”和“余下的表”，适合递归处理。
>
> **子表分析法**：更强调“一个表结点代表一对括号”，同级元素由 `tp` 串接，表结点更少，但递归算法的组织不如前者直接。

| 比较项目 | 表头—表尾分析法 | 子表分析法 |
| --- | --- | --- |
| 主要划分思路 | 递归拆成表头与表尾 | 按子表与同级元素分层 |
| 空表常见表示 | `NIL` 空指针 | 单独表结点，相关指针为空 |
| 原子结点 | `tag`、`atom` | `tag`、`atom`、`tp` |
| 表结点数量 | 相对较多 | 相对较少，通常与括号对数一致 |
| 常用操作 | `Head`、`Tail`、递归分解方便 | 存储更紧凑，但递归写法较复杂 |

### 6.5 用递归解决广义表问题

广义表的递归算法来自其定义：**一个表中的元素仍可能是表**。典型递归问题包括深度、遍历、复制，以及表头、表尾的分解。

以广义表深度为例，其思想是：

1. 遇到原子，深度为 $0$。
2. 遇到空表，深度为 $1$。
3. 遇到非空表，逐一求每个最外层元素的深度。
4. 取所有元素深度中的最大值，再加 $1$。

> [!warning] 递归一定要区分两种终止条件
> **原子**的深度为 $0$，**空表**的深度为 $1$，不能二者都返回同一个值；同时，对有循环自引用的递归表，不能直接采用无环树结构的深度递归，否则会无穷递归。

### 6.6 完整 C++ 实现：解析广义表、求长度和深度、表头表尾

本程序采用**表头—表尾分析法**：

- `Node` 用 `isAtom` 识别原子结点与表结点。
- 表结点拥有 `head` 与 `tail`，分别指向第一个元素与余下列表。
- `nullptr` 表示空表；转换为字符串时输出 `()`。
- 先将形如 `((a,b),(c,d))` 的字符串解析为**实际链式结构**，然后对该结构执行长度、深度、Head、Tail 操作。

为防止教学示例陷入手动分配/释放指针的噪音，这里使用 C++ 标准库的 `std::shared_ptr` 管理**无环**结点。它是标准、真实的内存管理类型，不是人为制造的 ADT 占位符；对于程序目前所处理的无环广义表，结点可以被正常释放。

```cpp
#include <algorithm>                              // 使用 std::max 计算最大深度
#include <cctype>                                 // 识别字母、数字和空白字符
#include <iostream>                               // 输出广义表与查询结果
#include <memory>                                 // 智能指针自动管理结点内存
#include <stdexcept>                              // 处理无效的表达式或操作
#include <string>                                 // 存储广义表的原子与输入
#include <vector>                                 // 暂存当前表的所有元素

struct Node {                                     // 表头-表尾方式的结点
    bool isAtom = false;                          // true 表示原子，false 表示表结点
    std::string atom;                             // 只有原子结点使用该字段
    std::shared_ptr<Node> head;                   // 表结点指向当前表头
    std::shared_ptr<Node> tail;                   // 表结点指向剩余部分形成的表
};

std::shared_ptr<Node> makeAtom(const std::string& value) {
    std::shared_ptr<Node> node = std::make_shared<Node>(); // 创建原子结点
    node->isAtom = true;                          // 设置结点类型为原子
    node->atom = value;                           // 保存具体的原子名称
    return node;
}

std::shared_ptr<Node> makeCons(std::shared_ptr<Node> head,
                               std::shared_ptr<Node> tail) {
    std::shared_ptr<Node> node = std::make_shared<Node>(); // 创建表结点
    node->head = head;                            // 表头既可能是原子，也可能是子表
    node->tail = tail;                            // 表尾始终为剩余元素组成的表
    return node;
}

class Parser {                                    // 将字符串解析为广义表链表
private:
    std::string text;                             // 待解析的输入字符串
    std::size_t position = 0;                     // 当前读取位置

    void skipSpaces() {                           // 忽略表达式中可选的空格
        while (position < text.size() &&
               std::isspace(static_cast<unsigned char>(text[position]))) {
            ++position;
        }
    }

    std::shared_ptr<Node> parseElement() {        // 元素可能是子表或原子
        skipSpaces();
        if (position < text.size() && text[position] == '(') {
            return parseList();                   // 遇到左括号则递归解析子表
        }
        std::size_t start = position;              // 记录原子名称的起始位置
        while (position < text.size()) {
            unsigned char c = static_cast<unsigned char>(text[position]);
            if (!std::isalnum(c) && c != '_') {    // 原子允许字母、数字和下划线
                break;
            }
            ++position;
        }
        if (start == position) {                   // 没有识别到有效原子
            throw std::invalid_argument("invalid atom");
        }
        return makeAtom(text.substr(start, position - start));
    }

    std::shared_ptr<Node> parseList() {           // 读取一对括号包围的完整列表
        if (position >= text.size() || text[position] != '(') {
            throw std::invalid_argument("missing opening parenthesis");
        }
        ++position;                                // 越过左括号
        skipSpaces();
        if (position < text.size() && text[position] == ')') {
            ++position;                            // 空表 () 不包含任何元素
            return nullptr;                       // 用空指针表示空表
        }
        std::vector<std::shared_ptr<Node>> elements; // 收集最外层各元素
        while (true) {
            elements.push_back(parseElement());   // 读取下一个原子或子表
            skipSpaces();
            if (position >= text.size()) {
                throw std::invalid_argument("missing closing parenthesis");
            }
            if (text[position] == ')') {
                ++position;                        // 当前列表已读取完整
                break;
            }
            if (text[position] != ',') {
                throw std::invalid_argument("missing comma");
            }
            ++position;                            // 越过逗号，继续读取后续元素
        }
        std::shared_ptr<Node> result = nullptr;   // 从空表开始逐个建立表结点
        for (std::size_t i = elements.size(); i > 0; --i) {
            result = makeCons(elements[i - 1], result); // 从右向左生成表头-表尾链
        }
        return result;
    }

public:
    explicit Parser(const std::string& input) : text(input) {}

    std::shared_ptr<Node> parse() {               // 入口：输入必须是一个完整列表
        skipSpaces();
        std::shared_ptr<Node> list = parseList();
        skipSpaces();
        if (position != text.size()) {            // 不能残留额外字符
            throw std::invalid_argument("trailing input");
        }
        return list;
    }
};

std::string toString(const std::shared_ptr<Node>& node) {
    if (node == nullptr) {                        // 空表表示为 ()
        return "()";
    }
    if (node->isAtom) {                           // 原子直接显示自身名称
        return node->atom;
    }
    std::string result = "(";                     // 非空表用括号包围
    for (std::shared_ptr<Node> p = node; p != nullptr; p = p->tail) {
        if (p != node) {                          // 只在相邻元素之间输出逗号
            result += ",";
        }
        result += toString(p->head);              // 递归处理嵌套的子表
    }
    return result + ")";
}

int listLength(const std::shared_ptr<Node>& list) {
    int length = 0;                               // 只统计最外层的元素数量
    for (std::shared_ptr<Node> p = list; p != nullptr; p = p->tail) {
        ++length;                                 // 每经过一个表结点，长度加一
    }
    return length;
}

int listDepth(const std::shared_ptr<Node>& node) {
    if (node == nullptr) {                        // 空表 () 的深度为 1
        return 1;
    }
    if (node->isAtom) {                           // 原子的深度为 0
        return 0;
    }
    int maxChildDepth = 0;                        // 保存所有表头中最大的深度
    for (std::shared_ptr<Node> p = node; p != nullptr; p = p->tail) {
        maxChildDepth = std::max(maxChildDepth, listDepth(p->head));
    }
    return maxChildDepth + 1;                    // 最外层括号使深度再加一
}

std::shared_ptr<Node> getHead(const std::shared_ptr<Node>& list) {
    if (list == nullptr || list->isAtom) {        // 空表和原子没有合法的表头
        throw std::invalid_argument("head requires a nonempty list");
    }
    return list->head;                            // 表头可以是原子或列表
}

std::shared_ptr<Node> getTail(const std::shared_ptr<Node>& list) {
    if (list == nullptr || list->isAtom) {        // 空表和原子没有合法的表尾
        throw std::invalid_argument("tail requires a nonempty list");
    }
    return list->tail;                            // 表尾一定是一个表，包括空表
}

int main() {
    Parser parser("((a,b),(c,d))");              // 解析一个有两层括号的广义表
    std::shared_ptr<Node> list = parser.parse();  // 构建真实的表头-表尾链表
    std::cout << "List: " << toString(list) << '\n';
    std::cout << "Length: " << listLength(list) << '\n';
    std::cout << "Depth: " << listDepth(list) << '\n';
    std::cout << "Head: " << toString(getHead(list)) << '\n';
    std::cout << "Tail: " << toString(getTail(list)) << '\n';
    std::cout << "Head(Tail): " << toString(getHead(getTail(list))) << '\n';
    std::cout << "Tail(Head): " << toString(getTail(getHead(list))) << '\n';
    return 0;
}
```

运行结果应为：

| 查询 | 输出 |
| --- | --- |
| 原始广义表 | `((a,b),(c,d))` |
| 长度 | `2` |
| 深度 | `2` |
| 表头 | `(a,b)` |
| 表尾 | `((c,d))` |
| 表尾的表头 | `(c,d)` |
| 表头的表尾 | `(b)` |

程序中的核心递归发生在两个地方：

- `parseElement()` 遇到 `(` 时进入 `parseList()`，完成嵌套解析。
- `listDepth()` 为每一个表头递归求深度，并取最大值；`toString()` 同样递归打印嵌套元素。

需要注意，`listLength()` **不递归进入每个子表**，因为广义表的长度只统计最外层元素。这个对照非常适合用于理解**长度与深度的本质区别**。

---

## 七、教学代码与下标变换的统一实践

### 7.1 一份程序串联主要下标公式

下面的 C++ 程序分别验证：多维数组的行优先展开、对称矩阵下标、上三角矩阵下标、三对角矩阵正反向变换、$2\times2$ 准对角方块下标。

**所有代码中的数组行列下标均从 0 开始。** `rowMajorIndex()` 用数组维长和目标下标作参数，所以无需为 2 维、3 维、4 维分别写一套展开公式。

```cpp
#include <iostream>             // 提供标准输出
#include <stdexcept>            // 提供参数越界异常
#include <vector>               // 使用连续存储的动态数组

// 将 n 维数组的下标转换为按行优先存储时的一维下标。
std::size_t rowMajorIndex(const std::vector<int>& dims,
                          const std::vector<int>& indices) {
    if (dims.empty() || dims.size() != indices.size()) { // 维数必须相同且非零
        throw std::invalid_argument("invalid dimensions");
    }

    std::size_t position = 0;                        // 当前累计的一维下标
    for (std::size_t i = 0; i < dims.size(); ++i) { // 从第一维依次处理到最后一维
        if (dims[i] <= 0 || indices[i] < 0 || indices[i] >= dims[i]) {
            throw std::out_of_range("index out of range"); // 检查维界与下标
        }
        position = position * dims[i] + indices[i];   // 逐维展开行优先下标
    }
    return position;                                  // 返回从 0 开始的位置
}

// n 阶对称矩阵：只存储下三角（含主对角线），按行排列。
int symmetricIndex(int n, int i, int j) {
    if (n <= 0 || i < 0 || j < 0 || i >= n || j >= n) {
        throw std::out_of_range("invalid symmetric index");
    }
    if (i < j) {                                      // 上三角元素映射到其对称位置
        int temp = i;
        i = j;
        j = temp;
    }
    return i * (i + 1) / 2 + j;                      // 前 i 行元素数加本行偏移
}

// n 阶上三角矩阵：仅存储 i <= j 的元素，按行排列。
int upperIndex(int n, int i, int j) {
    if (n <= 0 || i < 0 || j < i || j >= n) {
        throw std::out_of_range("index is not in upper triangle");
    }
    return i * (2 * n - i + 1) / 2 + (j - i);        // 前 i 行总数加行内偏移
}

// n 阶三对角矩阵：只存储 |i-j| <= 1 的元素，按行排列。
int tridiagonalIndex(int n, int i, int j) {
    if (n <= 0 || i < 0 || j < 0 || i >= n || j >= n ||
        (i - j > 1) || (j - i > 1)) {
        throw std::out_of_range("index is outside three diagonals");
    }
    return 2 * i + j;                                // 适用于从 0 开始的行列下标
}

// 将三对角矩阵压缩后的下标，还原为原矩阵的行列下标。
void inverseTridiagonalIndex(int n, int k, int& i, int& j) {
    if (n <= 0 || k < 0 || k >= 3 * n - 2) {
        throw std::out_of_range("invalid compressed index");
    }
    i = (k + 1) / 3;                                 // 整数除法确定原来的行
    j = k - 2 * i;                                   // 利用 k=2i+j 求原来的列
}

// 由 m 个 2x2 方块沿主对角线组成的准对角矩阵。
int blockDiagonalIndex(int m, int i, int j) {
    if (m <= 0 || i < 0 || j < 0 || i >= 2 * m || j >= 2 * m ||
        i / 2 != j / 2) {
        throw std::out_of_range("index is outside nonzero blocks");
    }
    return 4 * (i / 2) + 2 * (i % 2) + (j % 2);    // 块偏移加块内行优先偏移
}

int main() {
    std::vector<int> dimensions{2, 3, 4};           // 三维数组形状为 2x3x4
    std::vector<int> coordinates{1, 2, 3};          // 查询 A[1][2][3]
    std::cout << "3D row-major index: "
              << rowMajorIndex(dimensions, coordinates) << '\n';
    std::cout << "Symmetric A[1][3]: " << symmetricIndex(4, 1, 3) << '\n';
    std::cout << "Upper A[1][3]: " << upperIndex(4, 1, 3) << '\n';
    std::cout << "Tridiagonal A[2][3]: " << tridiagonalIndex(5, 2, 3) << '\n';

    int i = 0;                                      // 接收反向变换的行下标
    int j = 0;                                      // 接收反向变换的列下标
    inverseTridiagonalIndex(5, 7, i, j);            // 将压缩下标 7 还原
    std::cout << "Tridiagonal B[7]: (" << i << ", " << j << ")\n";
    std::cout << "Block A[3][2]: " << blockDiagonalIndex(3, 3, 2) << '\n';
    return 0;                                       // 正常结束程序
}
```

关键运行结果：

- $A[2][3][4]$ 的 `A[1][2][3]` 对应一维下标 `23`。
- $4\times4$ 对称矩阵的 `A[1][3]` 对应下三角下标 `7`。
- $4\times4$ 上三角矩阵的 `A[1][3]` 对应下标 `6`。
- 五阶三对角矩阵的 `A[2][3]` 对应下标 `7`；从 `B[7]` 还原得到 `(2,3)`。

> [!tip] 编译运行
> 四个程序彼此独立，每个源文件单独编译。例如：
>
> `g++ -std=c++17 -Wall -Wextra -pedantic 01_index_mapping.cpp -o index_mapping`
>
> `./index_mapping`
>
> 在 Windows 的 PowerShell 中执行编译命令后，可以用 `./index_mapping.exe` 或 `.\index_mapping.exe` 运行生成的程序。其他三个程序只需替换源文件名和输出文件名。

---

## 八、典型习题与完整解答

### 8.1 上三角矩阵下标变换

**题意**：一个 $n$ 阶上三角矩阵，将上三角元素逐行存入一维数组，求 $k=f_1(i)+f_2(j)+c$ 的表达式，并要求 $f_1,f_2$ 中不包含常数项。

为与本章推导保持一致，先统一采用**原矩阵下标从 1 开始、压缩数组 $B$ 的下标从 0 开始**。

第 $i$ 行之前总共存储：

$$
\sum_{r=1}^{i-1}(n-r+1)
=(i-1)(n+1)-\frac{i(i-1)}2
$$

本行从 $a_{ii}$ 存到 $a_{ij}$，在该行内偏移 $j-i$。

因此：

$$
\begin{aligned}
k&=(i-1)(n+1)-\frac{i(i-1)}2+(j-i)\\
&=-\frac12i^2+\left(n+\frac12\right)i+j-n-1
\end{aligned}
$$

可取：

$$
\boxed{f_1(i)=-\frac12i^2+\left(n+\frac12\right)i}
$$

$$
\boxed{f_2(j)=j,\qquad c=-n-1}
$$

> [!note] 如果题目改用 $B[1],B[2],\ldots$ 编号
> 上述结果整体加 1 即可，成为 $c=-n$。题目未明确起始下标时，**必须先声明采用哪一套编号规则**。

### 8.2 三对角矩阵的正反向变换

**题意**：$n$ 阶三对角矩阵逐行压缩到 $B[3n-2]$，求原下标到 $k$、$k$ 到原下标的双向公式。

若 $(i,j)$ 采用 **1-based**，$k$ 采用 **0-based**：

$$
\boxed{k=2i+j-3}\qquad(|i-j|\le1)
$$

由前文公式或从各行依次占 $2,3,\ldots,3,2$ 个位置推得：

$$
\boxed{i=\left\lfloor\frac{k+1}{3}\right\rfloor+1}
$$

$$
\boxed{j=k-2i+3}
$$

如果两边全部使用**从 0 开始**的行列下标，则改写成：

$$
\boxed{k=2i+j,\quad i=\left\lfloor\frac{k+1}{3}\right\rfloor,\quad j=k-2i}
$$

合法范围是 $0\le k<3n-2$，以及原矩阵中的 $|i-j|\le1$。不能对三对角带之外的位置调用压缩映射。

### 8.3 $2\times2$ 准对角矩阵的下标变换

**题意**：矩阵由 $m$ 个 $2\times2$ 小方块沿主对角线排列，按每块行优先依次存入 $B[4m]$，求 $(i,j)$ 到 $k$ 的公式。

当原下标 $(i,j)$ 均从 **1** 开始，压缩下标 $k$ 从 **0** 开始：

$$
\boxed{k=4\left\lfloor\frac{i-1}{2}\right\rfloor
+2((i-1)\bmod2)+((j-1)\bmod2)}
$$

条件是：

$$
\boxed{\left\lfloor\frac{i-1}{2}\right\rfloor
=\left\lfloor\frac{j-1}{2}\right\rfloor}
$$

因为只有属于同一个 $2\times2$ 小方块的元素才被存储。

> [!example] 检查一个元素
> 取 $a_{4,3}$，属于第二个方块（行列 3、4）。
>
> $$k=4\times1+2\times1+0=6$$
>
> 它对应压缩数组中从 0 开始的第 6 号位置，顺序为该方块中的第三个元素。

### 8.4 表头、表尾八个组合运算

按课件习题的顺序整理：

| 序号 | 表达式 | 结果 |
| ---: | --- | --- |
| 1 | `Head((p,h,w))` | `p` |
| 2 | `Tail((b,k,p,h))` | `(k,p,h)` |
| 3 | `Head(((a,b),(c,d)))` | `(a,b)` |
| 4 | `Tail(((a,b),(c,d)))` | `((c,d))` |
| 5 | `Head(Tail(((a,b),(c,d))))` | `(c,d)` |
| 6 | `Tail(Head(((a,b),(c,d))))` | `(b)` |
| 7 | `Head(Tail(Head(((a,b),(c,d)))))` | `b` |
| 8 | `Tail(Head(Tail(((a,b),(c,d)))))` | `(d)` |

其中 5～8 题只要遵守**从最内层到最外层**逐步运算，就不会误删括号。

### 8.5 两个广义表的深度

**题（1）**：

$$
L_1=((()),a,((b,c),(),d),(((e))))
$$

最深的元素为 `(((e)))`，单独看具有三层括号，再被最外层 $L_1$ 包含，故：

$$
\boxed{\operatorname{Depth}(L_1)=4}
$$

**题（2）**：

$$
L_2=((((a),b)),(((),d),(e,f)))
$$

最大括号嵌套层数仍为四层，因此：

$$
\boxed{\operatorname{Depth}(L_2)=4}
$$

> [!tip] 怎样快速检查广义表深度？
> 由左向右扫描表达式：遇到 `(` 时当前层数加 1，遇到 `)` 时减 1；扫描过程中达到的**最大层数**，就是普通有限广义表的深度。空表 `()` 仍然会贡献一层括号。

### 8.6 根据链式存储图恢复广义表

按照课件给出的**表头—表尾结点结构**读取：`tag=1` 为表结点，`tag=0` 为原子结点，`hp` 向下指向当前表头，`tp` 指向该层剩余元素，`^` 表示空指针。

- **图（1）**：最外层有两个元素。第一元素为 `(x,(y))`；第二元素为 `((),(z))`。故为：

  $$\boxed{((x,(y)),((),(z)))}$$

- **图（2）**：最外层有三个元素。它们分别是 `((a,b),())`、`(a,(b))` 和 `()`。故为：

  $$\boxed{(((a,b),()),(a,(b)),())}$$

> [!warning] 读结构图时必须辨认指针归属
> 同一张图中向下的 `hp` 与横向的 `tp` 不能交换理解；空指针既可能表示**表尾已经结束**，也可能出现在用专门表结点表示的**空子表**内。尤其不能因为某个元素是空表，就把这一层的整个元素删掉。

---

## 九、课件中的代码与概念需要注意的地方

> [!warning] 课件示意代码与可执行程序的区别
> 1. 三元组示例中的 `elemtype` 未具体定义，本身不是标准 C/C++ 类型，应换成实际需要的 `int`、`double` 等。
> 2. 稀疏矩阵整体结构不应把三元组数组与矩阵维数成员放进同一个 `union`，应使用 `struct` 同时保存这些信息。
> 3. 某些算法片段省略了变量声明、头文件、函数完整上下文，或存在排版丢失的分号；它们用于课堂说明算法思想，不能直接作为独立程序编译。本文给出可独立运行的具体实现。
> 4. `data[0]` 是否占用、行列下标是否从 1 开始，属于实现约定。必须与所使用的 `num`、`cpot` 或 `rowStart` 公式一致。
> 5. 广义表的 `E=(a,E)` 是自引用结构，不能当作普通有限子表无限复制，也不能对其直接使用无环递归遍历。

---

## 十、全章速查与复习重点

### 10.1 主要公式速查

以下前六行默认原行列下标**均从 0 开始**；三对角公式中 $k$ 也从 0 开始。

| 场景 | 核心公式 | 使用条件 |
| --- | --- | --- |
| 二维数组行优先 | $k=in+j$ | $A[m][n]$ |
| 二维数组列优先 | $k=jm+i$ | $A[m][n]$ |
| $n$ 维数组行优先 | $k=j_1b_2\cdots b_n+\cdots+j_n$ | 各维维长为 $b_1,\ldots,b_n$ |
| 对称矩阵，下三角存储 | $k=p(p+1)/2+q$ | $p=\max(i,j)$、$q=\min(i,j)$ |
| 上三角矩阵，行优先 | $k=i(2n-i+1)/2+j-i$ | $i\le j$ |
| 三对角矩阵，行优先 | $k=2i+j$ | $\lvert i-j\rvert\le1$ |
| 三对角矩阵，反向 | $i=\lfloor(k+1)/3\rfloor,\ j=k-2i$ | $0\le k<3n-2$ |
| 稀疏因子 | $\delta=t/(mn)$ | $t$ 为非零元个数 |
| 快速转置位置数组 | $\operatorname{start}[c]=\operatorname{start}[c-1]+\operatorname{count}[c-1]$ | 下标从 0 开始，`start[0]=0` |
| 广义表深度 | $1+\max\operatorname{Depth}(\text{各元素})$ | 非空、有限、无环广义表 |

### 10.2 概念区别速查

| 易混淆概念 | 核心区分 |
| --- | --- |
| 数组的逻辑维数 vs 物理地址 | 元素用多个下标描述，但存储空间按一维顺序排列 |
| 行优先 vs 列优先 | 行优先的跨行步长是列数；列优先的跨列步长是行数 |
| 对称矩阵 vs 三角矩阵 | 对称位置值相同；三角矩阵的另一半是固定常数 |
| 特殊矩阵 vs 稀疏矩阵 | 前者依靠分布规律计算位置；后者显式记录不规则非零元 |
| 普通转置 vs 快速转置 | 前者按列反复扫描，后者通过计数和前缀和一次定位 |
| 三元组表 vs 十字链表 | 前者连续存储；后者通过行、列指针双向组织非零元 |
| 广义表长度 vs 深度 | 长度数最外层元素；深度数最大括号嵌套层次 |
| 原子 vs 空表 | 原子深度为 0；空表深度为 1、长度为 0 |
| 表头 vs 表尾 | 表头可以是原子或表；表尾一定是表 |
| 共享表 vs 递归表 | 共享可以无环；递归自引用形成循环结构 |

> [!summary] 复习检查清单
> - [ ] 能独立推导二维、多维数组的行优先存储地址。
> - [ ] 能从“前面存多少 + 本行偏移”推导对称、上三角、三对角矩阵的压缩下标。
> - [ ] 能区分原矩阵与压缩数组的 0-based、1-based 约定。
> - [ ] 能写出三元组表，并解释为什么转置还要重排三元组顺序。
> - [ ] 能手算 `num` 和 `cpot`，理解快速转置为什么是 $O(n+t)$。
> - [ ] 能解释行位置表、行链表、十字链表的差别及使用场景。
> - [ ] 能判断广义表的长度、深度，正确处理 `()`、`(())`。
> - [ ] 能连续计算 `Head`、`Tail`，并从链式结构图恢复括号表达式。
> - [ ] 能读懂广义表递归运算的终止条件，知道自引用情况需要特殊处理。

#数据结构/数组与广义表
