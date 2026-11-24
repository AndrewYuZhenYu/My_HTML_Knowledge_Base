# 第四章 串：存储表示、基本操作与 KMP 模式匹配

> [!abstract] 本章知识主线
> **字符串是什么 → 各种串操作如何准确规定 → 逻辑上的一串字符如何存入内存 → 朴素匹配怎样重复比较 → KMP 怎样凭借已匹配信息避免回退 → 如何独立推导 `next` 和 `nextval`。**
>
> 本章统一采用课程中的**字符位置从 1 开始**、`Index` 未找到返回 `0`、`next[1]=0` 的约定；代码下标将与之显式转换。模式串要求非空的地方会明确指出。字符串示例以单字节英文字符演示，UTF-8 中文多字节字符与“一个字节对应一个字符”的假设不同。

![ds04_logic_87d0b02e-4215-4ae3-a1a4-a47a5bdcf3bc](./_assets/eb6b48d020/ds04_logic_87d0b02e-4215-4ae3-a1a4-a47a5bdcf3bc.svg)

## 一、串的逻辑结构与基本术语

### 1.1 定义：字符组成的有限序列

**串（String）**是零个或多个字符组成的有限序列，记作 $S='a_1a_2\cdots a_n'$，其中 $n\ge0$ 是**串长**，字符 $a_i$ 允许是字母、数字、空格或其他字符。串与一般线性表的逻辑相似，区别在于元素被限制为字符；串操作往往把**整个串或连续子串**作为对象，而不是单个元素。

- **空串**：$n=0$，通常写作 `''` 或 `""`。它不包含任何字符。
- **空格串**：由一个或多个空格字符组成。例如 `"   "` 长度是 $3$，不是空串。
- **子串**：主串中**连续**的字符序列；包含它的原串叫**主串**。不连续但保持次序的字符集合一般只能称为子序列，不能当成本章的子串。
- **位置**：字符所在的序号；子串在主串中的位置取子串**首字符的序号**，本章为 $1$ 基位置。
- **相等**：两串长度相同，且相应位置的每一个字符均相同。`"abc"` 和 `"abC"` 并不相等。

![ds04_substring_36fe6d41-aa24-41d3-9a9f-836e21b5faf9](./_assets/eb6b48d020/ds04_substring_36fe6d41-aa24-41d3-9a9f-836e21b5faf9.svg)
![ds04_emptyspace_4a240b0f-f0ff-4d21-af37-dd1f1d8e6c35](./_assets/eb6b48d020/ds04_emptyspace_4a240b0f-f0ff-4d21-af37-dd1f1d8e6c35.svg)

> [!important] 关于子串的两项约定
> **空串是任意串的子串；任意串是自己的子串。** 不过这不意味着所有模式匹配算法都允许空模式：课内定义的 `Index(S,T,pos)` **要求模式串 T 非空**，必须区分概念命题与函数的合法输入条件。

> [!example] 例：`very difficult`
> 主串 `"very difficult"` 的长度为 $4+1+9=14$。子串 `"very"` 从第 $1$ 位开始；`"difficult"` 从第 $6$ 位开始。中间的空格是第 $5$ 个字符，不能忽略。

### 1.2 串与线性表、C 风格字符串、`std::string`

从抽象数据类型角度，串的元素依次相连，是一种特殊的线性结构。但要区分三层：**逻辑串**（字符序列及操作）、**存储结构**（定长/堆/块链）、**具体语言接口**（C 的 `char[]` 与 C++ 的 `std::string`）。逻辑串不自带 `\0`；C 风格字符串常在物理存储末尾设置 `\0` 终止符，该终止符不计入通常的串长。

例如 `"BOOK"` 有四个逻辑字符，C 字符数组要有足够位置容纳 `B O O K \0`，而课程讲义的定长 `SString` 则可采用**第 0 单元存长度、字符从第 1 单元开始**的不同布局。绝不能把这两个布局误认为完全相同。

## 二、串抽象数据类型及其基本操作

### 2.1 数据对象、顺序关系与操作族

串的数据对象为字符集的元素 $a_i$；数据关系是相邻字符之间的前驱和后继关系：

$$
D=\{a_i\mid a_i\in\mathrm{CharacterSet},\ 1\le i\le n\},\qquad R=\{(a_{i-1},a_i)\mid 2\le i\le n\}.
$$

课件给出的串操作可按语义归类：

| 操作 | 含义 | 重要条件或结果 |
|---|---|---|
| `StrAssign(&T,chars)` | 用字符序列为 T 赋值 | T 得到指定串值 |
| `StrCopy(&T,S)` | 复制 S 到 T | 必须正确处理旧目标空间 |
| `StrEmpty(S)` | 判空 | 仅串长为 0 时为真 |
| `StrLength(S)` | 求串长 | 返回逻辑字符个数 |
| `StrCompare(S,T)` | 按字典序比较 | 返回负数、0、正数表示小于、等于、大于 |
| `Concat(&T,S1,S2)` | 连接两串 | 结果为 S1 后接 S2 |
| `SubString(&Sub,S,pos,len)` | 截取连续子串 | 从第 pos 位起，共 len 字符 |
| `Index(S,T,pos)` | 模式匹配 | 从 pos 起找 T，成功返回首位置，失败 0 |
| `Replace(&S,T,V)` | 替换模式串 | 用 V 替换所有**不重叠**的 T |
| `StrInsert(&S,pos,T)` | 插入子串 | 在第 pos 个字符**之前**插入 T |
| `StrDelete(&S,pos,len)` | 删除子串 | 删除从 pos 起的 len 个字符 |
| `ClearString(&S)` | 清空串 | 逻辑上变为空串 |
| `DestroyString(&S)` | 销毁串 | 释放表示结构，不能再按有效对象操作 |

![ds04_adt_0747c74e-8cba-4cca-9748-35ec4fa245bd](./_assets/eb6b48d020/ds04_adt_0747c74e-8cba-4cca-9748-35ec4fa245bd.svg)

> [!note] “六个基本操作”与其他操作的关系
> 课件将 `StrAssign`、`StrCopy`、`StrCompare`、`StrLength`、`Concat` 和 `SubString` 归为用于构造其他操作的**最小操作子集**。这里不是说其余运算不重要，也不是 C++ 标准库的 API 清单。教材中把 `ClearString` 和 `DestroyString` 另作生命周期操作，因此不能直接从“六项”推导出完整操作总数。

![ds04_minsubset_9b69e83c-e98e-40e3-ab81-e5d04ec9236e](./_assets/eb6b48d020/ds04_minsubset_9b69e83c-e98e-40e3-ab81-e5d04ec9236e.svg)

### 2.2 字符位置、长度与边界

在课件的 `SubString(S,pos,len)` 约定下：

$$
1\le pos\le |S|,\qquad 0\le len\le |S|-pos+1.
$$

即使 $len=0$，结果也是合法空串；课程旧式接口仍要求 $pos$ 不超过已有串长。现代标准库可以采用不同边界规则：例如 C++ 的 `substr(pos,0)` 在 `pos=size()` 时合法。因此**实现前先写清采用哪一套契约**。

插入允许 $1\le pos\le |S|+1$，因为在串末尾追加也是一种插入；删除必须保证所删片段完全落在原串的合法范围内。

![ds04_range_ed2aab2f-fd4f-49c2-bdba-df920b7bc7af](./_assets/eb6b48d020/ds04_range_ed2aab2f-fd4f-49c2-bdba-df920b7bc7af.svg)

### 2.3 联接、截取、插入与删除

`Concat(T,S1,S2)` 按原顺序复制两个字符序列：先复制 S1，再紧接着复制 S2。例如 `"ABC"+"DE"="ABCDE"`。顺序不可交换：串的联接一般满足结合律但不满足交换律。

![ds04_concat_91c90800-4615-4e90-956f-d33e027cbc77](./_assets/eb6b48d020/ds04_concat_91c90800-4615-4e90-956f-d33e027cbc77.svg)

`SubString(Sub,S,pos,len)` 的关键不是“寻找相同字符”，而是从已知**起点**连续复制指定**长度**。例如 `SubString("command",4,3)="man"`。注意这个例子中第 $4,5,6$ 位依次是 `m,a,n`。

![ds04_subop_55bb567f-0fdb-471b-a0b8-e90b0095e07c](./_assets/eb6b48d020/ds04_subop_55bb567f-0fdb-471b-a0b8-e90b0095e07c.svg)

`StrInsert` 的位置参数表示**插入后新字符占据的开始位置**。例如 `StrInsert("chater",4,"rac")` 得到 `"character"`。如果底层是顺序数组，先将原来第 $4$ 位起的字符依次向后移动，再复制新增字符。

![ds04_insertion_a847f113-f8f8-47da-874c-f2d5e1171a60](./_assets/eb6b48d020/ds04_insertion_a847f113-f8f8-47da-874c-f2d5e1171a60.svg)

`StrDelete` 按已知的起点和长度删除一个连续区间，并让后面的字符向前填补空缺。例如从 `"ABXYZCD"` 的第 $3$ 位起删除 $3$ 位，结果为 `"ABCD"`。

![ds04_deletion_f291d7dc-edf0-413f-81fe-87c8fdc60a32](./_assets/eb6b48d020/ds04_deletion_f291d7dc-edf0-413f-81fe-87c8fdc60a32.svg)

> [!warning] 1 基与 0 基的快速对照
> 课内 `SubString(S,pos,len)` 对应 `std::string` 的 `S.substr(pos-1,len)`。课程中在第 `pos` 个字符前插入，C++ 中 `insert(pos-1,T)`。不能只照抄相同数字，否则结果整体偏移一位。

### 2.4 定位：`Index` 是一种特殊的子串查找

给定主串 S、非空模式 T 和合法起点 `pos`，`Index(S,T,pos)` 返回从**第 `pos` 位开始**的第一处完整匹配的 1 基位置，找不到则返回 $0$。课件文字个别地方使用“第 pos 个字符之后”，而其程序和例题把 `pos` 本身作为第一个可选起点；以下按这一可验证的一致用法解释。

例如 `S="abcaabcaaabc"`，`T="bca"`：从 $1$ 开始，结果为 $2$；从 $3$ 开始，结果为 $6$；从 $8$ 开始，未再出现完整匹配，结果为 $0$。

![ds04_index_rule_f4c4fa0d-fb03-43c1-81d6-61dba1fd916c](./_assets/eb6b48d020/ds04_index_rule_f4c4fa0d-fb03-43c1-81d6-61dba1fd916c.svg)
![ds04_indexex1_35e1e8eb-e8f7-4810-bf27-1db0361fbd44](./_assets/eb6b48d020/ds04_indexex1_35e1e8eb-e8f7-4810-bf27-1db0361fbd44.svg)
![ds04_indexex2_61cf72cc-5b37-412d-b3f6-e6d367890d90](./_assets/eb6b48d020/ds04_indexex2_61cf72cc-5b37-412d-b3f6-e6d367890d90.svg)

可以直接利用最小操作子集实现定位。若 $n=|S|$、$m=|T|$，则候选起点 $i$ 最大不能超过 $n-m+1$；对每个候选起点，截取长 $m$ 的子串并与 T 比较，相等就立即返回 $i$。

![ds04_indexcombine_28304caf-7dd6-4ccf-870a-33c075f908c9](./_assets/eb6b48d020/ds04_indexcombine_28304caf-7dd6-4ccf-870a-33c075f908c9.svg)

下面是直接按字符比较的 C++17 版本，返回值保持课程的 **1 基位置 / 未找到 0** 约定：

```cpp
#include <string>
#include <stdexcept>

int indexBF(const std::string& s, const std::string& p, int pos = 1) {
    if (p.empty() || pos < 1) {                     // 课程 Index 要求非空模式和合法起点
        throw std::invalid_argument("invalid pattern or position");
    }
    const int n = static_cast<int>(s.size());     // 主串长度
    const int m = static_cast<int>(p.size());     // 模式长度
    for (int start = pos - 1; start <= n - m; ++start) { // 0 基候选位置
        int j = 0;                                // 从模式头开始逐字比较
        while (j < m && s[start + j] == p[j]) {   // 两串对应字符相同
            ++j;                                  // 继续下一个字符
        }
        if (j == m) return start + 1;             // 全部相同，转成 1 基位置
    }
    return 0;                                     // 找不到完整匹配
}
```

该直接版本空间复杂度为 $O(1)$，时间复杂度最坏为 $O(nm)$。课件使用 `SubString` 和 `StrCompare` 组合实现的形式能解释 ADT 的封装思想，但若每次截取都产生新串，还会带来额外的临时拷贝开销。

### 2.5 不重叠置换 `Replace`

`Replace(&S,T,V)` 要用 V 替换 S 中所有**不重叠**的 T，T 不能为空。最容易误解的是两个匹配区间部分重叠时，不能都计为一次替换。例如 `"12121"` 中可从第 1 位和第 3 位看到 `"121"`，但它们重叠：按从左到右的非重叠策略，先替换最左的一次，得到 `"321"`；对 `"121121"` 则是两个不重叠 `"121"`，替换后得到 `"33"`。

![ds04_replacement_7ee0fd54-9253-4f2f-9f71-832c2d290d3b](./_assets/eb6b48d020/ds04_replacement_7ee0fd54-9253-4f2f-9f71-832c2d290d3b.svg)
![ds04_replace2_ff5444e4-6ad7-4017-a1a3-729da7898bb2](./_assets/eb6b48d020/ds04_replace2_ff5444e4-6ad7-4017-a1a3-729da7898bb2.svg)

课程另一例 `S="abcaabcaaabca"`、`T="bca"`，替换为 `"x"` 得到 `"axaxaax"`；替换为 `"bc"` 得到 `"abcabcaabc"`。结果可能比原串长，也可能短，因此定长串可能发生截断，堆分配串需管理容量。

![ds04_replacecombine_5c7be164-9dfd-4e11-86a6-589f3d6f0db7](./_assets/eb6b48d020/ds04_replacecombine_5c7be164-9dfd-4e11-86a6-589f3d6f0db7.svg)

为了避免替换后产生新匹配、又反复替换而产生不符合约定的结果，推荐**只扫描原始 S，一边扫描一边构造新串**：找到模式后消耗整段 T，再从原串下一个未消费位置继续。下面代码维持非重叠规则：

```cpp
#include <string>
#include <stdexcept>

std::string replaceAll(const std::string& s,
                       const std::string& target,
                       const std::string& value) {
    if (target.empty()) {                            // 空模式会产生歧义，主动拒绝
        throw std::invalid_argument("empty target");
    }
    std::string result;
    std::size_t from = 0;                           // 尚未处理的原串起点
    while (from < s.size()) {
        const std::size_t found = s.find(target, from); // 搜索下一处非重叠匹配
        if (found == std::string::npos) break;      // 剩余部分没有匹配
        result.append(s, from, found - from);       // 复制匹配前的原串内容
        result += value;                            // 追加替换内容
        from = found + target.size();               // 跳过完整模式，不再重用字符
    }
    result.append(s, from, s.size() - from);        // 保留最后剩余后缀
    return result;
}
```

> [!tip] 选择算法之前首先确认返回约定
> 教材的 `Index` 未命中返回 `0`；`std::string::find` 未命中返回 `std::string::npos`（无符号整数的特殊值）。教材下标从 $1$ 开始，`std::string` 的位置从 $0$ 开始。读写代码时需要**同时处理位置和失败值**。

## 三、串的物理存储：定长、堆分配与块链

逻辑上的一个串可采用不同的机内表示；**存储方式不同，某个操作的代价也可能完全不同**。本章三种典型方案是定长顺序存储、堆分配存储以及块链存储。

![ds04_storagecompare_9465df32-7d19-42b7-92ad-5dc9efed5e6c](./_assets/eb6b48d020/ds04_storagecompare_9465df32-7d19-42b7-92ad-5dc9efed5e6c.svg)

### 3.1 定长顺序存储 `SString`

定长顺序存储把串值顺序放在连续的一段空间内，并预留固定最大容量。课件采用一类 `SString` 布局：**0 号存储单元存串长，1 至 n 号存储单元存字符**。例如 `"student"` 长度为 $7$，第 0 单元填 7，第 1 至 7 单元填 `s,t,u,d,e,n,t`。

![ds04_fixedmem_f4b7de87-ad92-4720-a34c-6aeea31c70a3](./_assets/eb6b48d020/ds04_fixedmem_f4b7de87-ad92-4720-a34c-6aeea31c70a3.svg)
![ds04_cmem_832f0925-e3a3-4689-9f39-3e217497a0aa](./_assets/eb6b48d020/ds04_cmem_832f0925-e3a3-4689-9f39-3e217497a0aa.svg)

同样是顺序存储，还可以区分**非紧缩格式**（每个机器字仅放一个字符）和**紧缩格式**（一个机器字容纳多个字符）：紧缩格式的单位空间利用率更高，但字内字符提取可能需要额外处理。这一概念与“长度保存在第 0 号单元还是结尾用 `\0`”是两个不同的设计维度。

> [!note] 关于字符和内存单位
> 历史资料里的“字”“字符”与今天 C++ 的 `char` 字节单位不必一一对应。课件比较紧缩和非紧缩格式时强调的是**每个存储字容纳的字符数量**；实际工程中的文本编码、对齐和字符串对象还涉及其他因素，不宜直接拿课件图推算真实进程内存占用。

#### 3.1.1 拼接时的截断

如果最大串长为 `MAXSTRLEN=8`，连接 `"ABCDEF"` 与 `"XYZ"` 需要 $9$ 个字符，但物理容量只有 $8$，课件约定保存串的**前 8 个字符** `"ABCDEFXY"`，舍弃末尾的 `Z` 并报告“发生截断”。复制原串内容时必须更新串长，不能返回成功并悄悄忽略损失。

![ds04_fixedconcat_95a0638e-2232-4991-b914-11f6be4e577e](./_assets/eb6b48d020/ds04_fixedconcat_95a0638e-2232-4991-b914-11f6be4e577e.svg)
![ds04_truncation_6e8f67eb-7f7e-44a2-bbff-3428aba2c4ac](./_assets/eb6b48d020/ds04_truncation_6e8f67eb-7f7e-44a2-bbff-3428aba2c4ac.svg)

在 C++ 中可以用固定字符数组配合长度字段模拟课内结构，这里只展示拼接核心：

```cpp
#include <array>
#include <string>
#include <algorithm>

struct FixedString {
    std::array<char, 8> data{};                    // 最多保存 8 个有效字符
    int length = 0;                                // 逻辑串长独立维护
};

bool concatFixed(FixedString& out,
                 const std::string& a,
                 const std::string& b) {
    const std::string full = a + b;                // 需要保存的完整逻辑结果
    const int keep = std::min(8, static_cast<int>(full.size())); // 可容纳的长度
    FixedString temp;                              // 先写入临时结果，避免旧值残留
    for (int i = 0; i < keep; ++i) {
        temp.data[i] = full[i];                    // 复制可以容纳的前缀
    }
    temp.length = keep;                            // 记录实际保存长度
    out = temp;                                    // 提交新结果
    return keep == static_cast<int>(full.size()); // true 表示未截断
}
```

上例为简洁起见采用 C++ 固定数组及标准库临时串，**不是**课件中的 C 风格 `unsigned char SString[MAXSTRLEN+1]` 的逐行翻译；它展示同一截断行为。完整系统应对容量选择、返回状态和空串行为制定统一规范。

#### 3.1.2 求子串时的范围检查

求子串时需验证起点和长度，随后连续复制 $len$ 个字符。在定长数组中，因为 $len$ 受到合法原串范围约束，单次截取本身**不会比原串更长**，因此不会因截取而产生额外截尾。

![ds04_fixedsubstr_65aec1f6-3278-4c3d-a6c9-41308d9f3d14](./_assets/eb6b48d020/ds04_fixedsubstr_65aec1f6-3278-4c3d-a6c9-41308d9f3d14.svg)

```cpp
#include <string>
#include <stdexcept>

std::string substring1(const std::string& s, int pos, int len) {
    const int n = static_cast<int>(s.size());
    if (pos < 1 || pos > n || len < 0 || len > n - pos + 1) { // 课程边界
        throw std::out_of_range("invalid substring range");
    }
    return s.substr(static_cast<std::size_t>(pos - 1),
                    static_cast<std::size_t>(len)); // 转换为 0 基起点
}
```

> [!warning] 空子串合法不等于任意空子串起点合法
> `len=0` 在课件规则里合法，但 `pos` 仍必须落在课程许可的起点范围内。尤其对空主串如何截取空子串，课程 ADT 没有给出完整的特殊规则，写工程实现时可单独扩展，但不能把扩展规则伪装成讲义原始条件。

### 3.2 堆分配存储 `HString`

堆分配串仍然把字符连续保存在一段内存里，但这段内存大小由**运行时实际串长**决定。经典结构含有指向字符序列的 `ch` 指针与 `length` 长度字段。增加字符可能需要申请更大的空间并复制数据；与定长串相比不必因为预设最大串长而截尾。

![ds04_heapmem_1b50cf75-1741-47f0-9503-10e29dbdbb8f](./_assets/eb6b48d020/ds04_heapmem_1b50cf75-1741-47f0-9503-10e29dbdbb8f.svg)

课程旧式实现用 `malloc` / `realloc` / `free` 演示动态分配；现代 C++ 通常使用 `std::string`、`std::vector<char>` 或受资源管理对象控制的动态数组。它们并非在语义上等同于教材 `HString` 结构，而是更适合直接使用的实现方式。

- **复制**：为目标建立独立的字符存储空间，复制原串全部字符，更新目标长度。直接把裸指针赋给另一个对象只是浅拷贝，可能使两个对象错误地共同拥有同一块内存。
- **联接**：为两串总长度准备新空间，先复制前串、再复制后串。
- **插入**：先扩大空间，将插入点之后的字符**从尾到头后移**，最后填入新串。
- **求子串**：检查参数后分配恰好能容纳结果的空间，按顺序复制。

![ds04_heapcopy_db75b66d-031e-488e-aac6-9aa803597d23](./_assets/eb6b48d020/ds04_heapcopy_db75b66d-031e-488e-aac6-9aa803597d23.svg)
![ds04_heapconcat_32485d25-64c8-4be6-8753-977235241edb](./_assets/eb6b48d020/ds04_heapconcat_32485d25-64c8-4be6-8753-977235241edb.svg)
![ds04_heapinsert_915ca954-dd46-4380-ac4c-b6b3a758e384](./_assets/eb6b48d020/ds04_heapinsert_915ca954-dd46-4380-ac4c-b6b3a758e384.svg)
![ds04_shift_e3fdd456-3db9-4a47-9337-57152a0e0c26](./_assets/eb6b48d020/ds04_shift_e3fdd456-3db9-4a47-9337-57152a0e0c26.svg)

> [!warning] 旧式 `realloc` 的内存安全问题
> 课件例程使用 `S.ch=realloc(S.ch, ...)` 直接覆盖旧指针，这在分配失败时可能丢失旧内存地址。实际 C 程序应先用临时指针接收返回值，确认非空再赋值。若源串和目标串共享底层存储，还需谨慎处理内存重叠；现代 C++ 更推荐由容器和资源管理机制处理这些风险。

可以用两个不同的 C++ 代码片段理解“插入后移”与“深复制”的原理。下面的 `insert1` 使用现成的 `std::string`，其下标转换仍是本章最重要的细节：

```cpp
#include <string>
#include <stdexcept>

void insert1(std::string& s, int pos, const std::string& t) {
    if (pos < 1 || pos > static_cast<int>(s.size()) + 1) { // 1 基有效插入点
        throw std::out_of_range("invalid insertion position");
    }
    s.insert(static_cast<std::size_t>(pos - 1), t); // C++ 插入起点是 0 基
}
```

如果必须手动管理堆数组，可将新空间先分配成功、数据再拷贝完成，最后替换旧空间，从而避免操作中间失败损坏原值：

```cpp
#include <memory>
#include <algorithm>
#include <cstddef>

struct HeapString {
    std::unique_ptr<char[]> ch;                   // 使用独占所有权防止泄漏
    std::size_t length = 0;                       // 有效字符数
};

void copyHeap(HeapString& target, const HeapString& source) {
    auto temp = source.length ? std::make_unique<char[]>(source.length)
                              : std::unique_ptr<char[]>{}; // 先准备目标存储区
    if (source.length != 0) {
        std::copy_n(source.ch.get(), source.length, temp.get()); // 深复制全部有效字符
    }
    target.ch = std::move(temp);                  // 成功后提交，旧空间自动释放
    target.length = source.length;                // 更新长度
}
```

`HeapString` 采用 `unique_ptr`，因此默认不可直接复制；这与教材手工定义的普通 C 结构不同，特意以此避免无意识的裸指针浅拷贝。

### 3.3 块链存储 `LString`

**块链串**将字符分组放在若干个链结点中，每个结点保存 $k$ 个字符及指向下一结点的指针；可用头指针、尾指针和串长描述整个串。若串长不是 $k$ 的整数倍，最后一个结点可能有未用满的格子，可用 `#` 等占位符显示这些空位；**占位符不是实际串值的一部分**。

![ds04_chunk1_90442e69-bb9b-4e34-b01d-f5f2b84551d3](./_assets/eb6b48d020/ds04_chunk1_90442e69-bb9b-4e34-b01d-f5f2b84551d3.svg)
![ds04_chunk4_9c4680e1-3982-4645-83d3-91fec7ee2881](./_assets/eb6b48d020/ds04_chunk4_9c4680e1-3982-4645-83d3-91fec7ee2881.svg)
![ds04_chunk3_c5e8c53e-579d-421c-bc89-a4b5921d0aca](./_assets/eb6b48d020/ds04_chunk3_c5e8c53e-579d-421c-bc89-a4b5921d0aca.svg)

例如 `"ABCDEFGHI"` 有 $9$ 个字符：$k=1$ 需要 $9$ 个字符结点，$k=3$ 需要 $3$ 个结点，$k=4$ 需要 $3$ 个结点但最后一块只有 `I` 有效，余下 $3$ 格是空余容量。

```cpp
#include <array>

struct Chunk {
    std::array<char, 4> chars{};                 // 一个结点最多保存 4 个字符
    Chunk* next = nullptr;                       // 下一块的地址
};

struct ChunkString {
    Chunk* head = nullptr;                       // 首块指针
    Chunk* tail = nullptr;                       // 末块指针
    int curlen = 0;                              // 整个串的真实长度
};
```

> [!note] 此处代码是**结构声明**，并不是完整的链表管理器
> 一旦手工 `new` 结点，就需要相应的释放、拷贝与所有权规则。该段只用来学习 `head/tail/curlen` 和结点中的字符数组，不能直接当作完整可复制的 C++ 类使用。

在块链结构中，访问第 $i$ 个字符需要先定位第几个块，再进入块内第几个位置；插入、删除也可能触及块划分和结点调整。因此并非“链表就一定适合处理字符串”，还要考虑存储密度和操作代价。

![ds04_density_7a8b998c-22bb-4b08-8174-c74796915578](./_assets/eb6b48d020/ds04_density_7a8b998c-22bb-4b08-8174-c74796915578.svg)

**存储密度**可理解为有效数据所占空间与总实际分配空间的比值。减小块尺寸会减少每块内部的空位，但指针开销变多；增大块尺寸可能减少指针数量，却导致尾块或局部修改时的浪费。存储密度、遍历效率及修改成本应综合权衡。

## 四、模式匹配：BF 与首尾匹配

### 4.1 模式匹配问题的精确定义

对主串 $S$（长 $n$）、模式串 $T$（长 $m>0$），要寻找 T 在 S 中从指定位置起第一次完整出现的位置。如果起点是 $i$，对应关系是：

$$
S[i+j-1]=T[j],\quad 1\le j\le m.
$$

全部 $m$ 组相等即匹配成功。由于主串必须剩余至少 $m$ 个字符，最后一个可能起点为 $n-m+1$。若 $m>n$，直接判定找不到。

### 4.2 BF（Brute Force）朴素匹配

BF 的策略是**枚举起点，逐字符比较**。每一趟先把模式 T 的首字符与主串某一候选位置对齐，连续相等就比较后继字符；第一次不等则整趟失败，模式向右移动**一位**，重新从模式首字符开始。

给出课程同型例子：

$$S=\texttt{ababcabcacbab},\qquad T=\texttt{abcac}.$$

逐趟匹配图如下。橙/红色表示发生失配的位置，青绿色表示该趟中已经匹配过的字符。

![ds04_bf01_951aacef-16f8-46e9-8eb1-13bc695bb8fc](./_assets/eb6b48d020/ds04_bf01_951aacef-16f8-46e9-8eb1-13bc695bb8fc.svg)
![ds04_bf02_46b8a510-b5b0-40dd-8bf7-4ee3499d6ec3](./_assets/eb6b48d020/ds04_bf02_46b8a510-b5b0-40dd-8bf7-4ee3499d6ec3.svg)
![ds04_bf03_9af293b4-78a2-474e-a6b1-558972b175d4](./_assets/eb6b48d020/ds04_bf03_9af293b4-78a2-474e-a6b1-558972b175d4.svg)
![ds04_bf04_6f7ec333-89c9-405b-a9cc-086748a119f4](./_assets/eb6b48d020/ds04_bf04_6f7ec333-89c9-405b-a9cc-086748a119f4.svg)
![ds04_bf05_cd26d59e-b953-46db-83e9-e5586ff14889](./_assets/eb6b48d020/ds04_bf05_cd26d59e-b953-46db-83e9-e5586ff14889.svg)
![ds04_bf06_be56466b-b24a-4dbc-b246-a6d2d670e65f](./_assets/eb6b48d020/ds04_bf06_be56466b-b24a-4dbc-b246-a6d2d670e65f.svg)

依次尝试候选起点 $1,2,3,4,5,6$，最终在第 $6$ 位成功。这一过程不需要对模式进行预处理；它的不足是**明明已经比较过的重复内容，下一趟可能又从头比较**。

![ds04_bfmodel_fbfb82c9-5991-4f47-8437-1e900efc228c](./_assets/eb6b48d020/ds04_bfmodel_fbfb82c9-5991-4f47-8437-1e900efc228c.svg)

课件给出的双指针 BF 伪代码使用 `i=pos,j=1`，相等时两者自增；失配时执行 `i=i-j+2,j=1`。原因是此前已经匹配 $j-1$ 个字符，当前候选起点是 $i-j+1$，下一候选起点自然为 $i-j+2$。若采用 0 基下标，相应公式将发生变化，不能直接复制这一条表达式。

> [!example] 计算 BF 的下一候选起点
> 当前主串扫描到第 $i=7$ 位，模式指针为 $j=5$，说明已在这趟匹配了 $4$ 个字符而第 $5$ 个失配。原候选起点为 $7-5+1=3$，下一趟起点为 $3+1=4$，也就是 $i\leftarrow7-5+2=4$，$j\leftarrow1$。

### 4.3 BF 的复杂度

若主串长 $n$、模式长 $m$，最多尝试 $n-m+1$ 个完整候选起点；每个起点最多比较 $m$ 次，最坏时间为

$$
T(n,m)=O((n-m+1)m)=O(nm).
$$

极端例子是主串由大量 `a` 组成，仅末尾稍有变化，模式是 `aaa...ab`：每趟都匹配大量 `a` 后才失败，反复做近似相同的比较。若各候选起点一开始就不匹配，扫描过程可能接近 $O(n)$。只存储当前起点和字符指针时，额外空间为 $O(1)$。

![ds04_bfworst_96807a7b-a8ac-4015-bee7-5bd5e4a1c1e0](./_assets/eb6b48d020/ds04_bfworst_96807a7b-a8ac-4015-bee7-5bd5e4a1c1e0.svg)
![ds04_bfcomplex_0e177506-8fed-40a0-bd8c-2711089449f2](./_assets/eb6b48d020/ds04_bfcomplex_0e177506-8fed-40a0-bd8c-2711089449f2.svg)

### 4.4 首尾匹配

课件还介绍了**首尾匹配**：对每个候选起点先比模式第一个字符，再比模式最后一个字符；只有两端都相等，才检查中间的字符。这一安排可让首尾字符很有区分度的模式更快排除不可能起点，但本质仍是枚举候选起点，**最坏时间复杂度仍可达到 $O(nm)$**。

![ds04_firstlast_20da3c00-1c25-4160-b8dd-efb11ab937d5](./_assets/eb6b48d020/ds04_firstlast_20da3c00-1c25-4160-b8dd-efb11ab937d5.svg)
![ds04_firstlast1_51b5b71a-a2e1-40fa-8a76-03c72565ce48](./_assets/eb6b48d020/ds04_firstlast1_51b5b71a-a2e1-40fa-8a76-03c72565ce48.svg)
![ds04_firstlastlimits_8bae48f6-b124-414f-b4c6-7c7de3a28052](./_assets/eb6b48d020/ds04_firstlastlimits_8bae48f6-b124-414f-b4c6-7c7de3a28052.svg)

```cpp
#include <string>
#include <stdexcept>

int indexFirstLast(const std::string& s,
                   const std::string& p, int pos = 1) {
    if (p.empty() || pos < 1) {
        throw std::invalid_argument("invalid pattern or position");
    }
    const int n = static_cast<int>(s.size());
    const int m = static_cast<int>(p.size());
    for (int i = pos - 1; i + m <= n; ++i) {     // 枚举 0 基候选起点
        if (s[i] != p[0]) continue;              // 先比较模式首字符
        if (m > 1 && s[i + m - 1] != p[m - 1]) { // 再比较尾字符
            continue;
        }
        int j = 1;                               // 中间字符从第 2 位开始
        while (j < m - 1 && s[i + j] == p[j]) {
            ++j;                                  // 逐个检查中间位置
        }
        if (j == m - 1 || m == 1) return i + 1; // 所有需要比较的字符均相等
    }
    return 0;
}
```

## 五、KMP：从匹配历史到失败函数

### 5.1 为什么 KMP 不需要回退主串位置

KMP（Knuth–Morris–Pratt）是对单模式精确匹配的改进。它不是神奇地跳过所有不匹配字符，而是利用“已经匹配过的内容”决定下一次**模式串的指针从哪里继续**。主串指针 $i$ 不必回退，只有模式指针 $j$ 通过 `next` 数组回退。

![ds04_kmphigh_0d4e67df-433f-4134-aa09-8bb41acfbaba](./_assets/eb6b48d020/ds04_kmphigh_0d4e67df-433f-4134-aa09-8bb41acfbaba.svg)

当 $S[i]\ne T[j]$ 时，之前已成功匹配 $j-1$ 个字符：

$$
S[i-j+1\ldots i-1]=T[1\ldots j-1].
$$

若 $T[1\ldots k-1]$ 与 $T[j-k+1\ldots j-1]$ 相同，意味着**已匹配片段的尾部**已经等于模式**开头的部分**；那部分无需重新逐个比较，可保持 $i$ 不变，只令 $j\leftarrow k$。最大的可复用重叠长度会让模式在不漏解的前提下跳过更多重复尝试。

![ds04_prefixsuffix_6f03979e-3654-4159-bf68-15e19579b17c](./_assets/eb6b48d020/ds04_prefixsuffix_6f03979e-3654-4159-bf68-15e19579b17c.svg)

> [!important] 失配时唯一应该保留的是什么
> 保留主串当前指针 $i$，因为它指向的字符尚未被成功消耗；更新的是模式指针 $j$。若 `j` 最终退到 $0$，表示当前字符没有任何可以继续复用的模式前缀，下一步再同时执行 $i\leftarrow i+1,j\leftarrow1$。

### 5.2 真前缀、真后缀与 `next[j]`

对一个非空字符串 X，**真前缀**指从开头取但**不能等于整串**的前缀；**真后缀**指从末尾取但不能等于整串的后缀。空串通常视为二者共同的长度为 0 的候选。KMP 找的是这两类集合里**相等且最长**的长度。

在本课程的 **1 基 next** 约定中：

$$
\boxed{\operatorname{next}[1]=0},\qquad
\boxed{\operatorname{next}[j]=1+\operatorname{LPS}(T[1\ldots j-1])}\quad (j\ge2),
$$

其中 $\operatorname{LPS}(X)$ 表示 X 的**最长相等真前后缀长度**。注意求 `next[j]` 的对象是**第 $j$ 个字符之前的部分**，不是包含第 $j$ 个字符的完整前缀。

教材也可以写成位置式：令 `next[j]=k`，就表示在第 $j$ 个模式字符失配后，应回到模式的第 $k$ 个字符重试；如果不存在非空可复用重叠，则 $k=1$（若 $j=1$，特殊取 $0$）。

![ds04_basenext_e53ec83a-cf78-4e1f-b6b7-ddee4374a664](./_assets/eb6b48d020/ds04_basenext_e53ec83a-cf78-4e1f-b6b7-ddee4374a664.svg)

> [!warning] `LPS` 和 `next` 在不同教材里并不总是相同数组
> 大量网络资料使用从 0 开始的 `lps[i]` 或 `pi[i]`，其值是前缀长度；本课的 `next[j]` 则是失配后下一次**要比较的位置**，字符下标从 1 开始。不能无条件把这些数组的每一格直接抄到课程题目里。

![ds04_numbering_b31b5323-387e-4850-8d40-94d953433695](./_assets/eb6b48d020/ds04_numbering_b31b5323-387e-4850-8d40-94d953433695.svg)

![ds04_samplenext_92579af4-3072-4770-a71a-d2022b66b43e](./_assets/eb6b48d020/ds04_samplenext_92579af4-3072-4770-a71a-d2022b66b43e.svg)

### 5.3 手算实例：`T=abaabcac`

这个模式的 1 基字符序号为 $1\ldots8$，按从左到右计算得到

$$
\operatorname{next}=[0,1,1,2,2,3,1,2].
$$

计算时可以对每个 $j$ 单独执行：“取前 $j-1$ 个字符 → 列出真前缀和真后缀 → 找最长相等部分 → 长度加一”。下列八张图分别展示每个位置的推导；**第一位是定义特判**，其余位置才用最长相等真前后缀公式。

![ds04_nextbase1_3c2d52a0-a83f-42ed-83e3-23fb1ce5cb9f](./_assets/eb6b48d020/ds04_nextbase1_3c2d52a0-a83f-42ed-83e3-23fb1ce5cb9f.svg)
![ds04_nextbase2_b4951eaa-c909-4462-b50d-2931d8183e43](./_assets/eb6b48d020/ds04_nextbase2_b4951eaa-c909-4462-b50d-2931d8183e43.svg)
![ds04_nextbase3_700ae7e9-d593-4409-ae96-8913157d2185](./_assets/eb6b48d020/ds04_nextbase3_700ae7e9-d593-4409-ae96-8913157d2185.svg)
![ds04_nextbase4_6a3035a0-77ef-422e-bbf0-9c0354ddac0d](./_assets/eb6b48d020/ds04_nextbase4_6a3035a0-77ef-422e-bbf0-9c0354ddac0d.svg)
![ds04_nextbase5_6704cd70-14d8-44a4-9929-53f66f4f4c0d](./_assets/eb6b48d020/ds04_nextbase5_6704cd70-14d8-44a4-9929-53f66f4f4c0d.svg)
![ds04_nextbase6_04e5915b-53ac-4f40-924e-d89c02c6122f](./_assets/eb6b48d020/ds04_nextbase6_04e5915b-53ac-4f40-924e-d89c02c6122f.svg)
![ds04_nextbase7_a908de28-b28c-4547-b826-870cfbcb799f](./_assets/eb6b48d020/ds04_nextbase7_a908de28-b28c-4547-b826-870cfbcb799f.svg)
![ds04_nextbase8_54700b40-a56b-4185-a949-e2dc591ae27a](./_assets/eb6b48d020/ds04_nextbase8_54700b40-a56b-4185-a949-e2dc591ae27a.svg)

> [!example] 为什么 `next[6]=3`
> 第 $6$ 位失配，**已匹配**的是前五字符 `"abaab"`。它的最长相等真前后缀是 `"ab"`，长度为 $2$，所以 `next[6]=2+1=3`。注意不能用第 6 位的 `c` 参与比较。

> [!example] 为什么 `next[7]=1`
> 第 $7$ 位之前的已匹配串为 `"abaabc"`。不存在非空的相等真前后缀，最长长度为 $0$，所以 `next[7]=1`；这与 `next[1]=0` 的特殊情况不同。

### 5.4 使用 KMP 真实执行一遍匹配

下面采用主串 `"acabaabaabcacaabc"` 与模式 `"abaabcac"`。主串从左向右扫描，**成功匹配从第 $6$ 位开始**。各图由同一份 KMP 逐步执行记录产生，显示真实的 $(i,j)$、成功/失配状态以及模式当前的对齐位置：

![ds04_kmprun01_2fd6ad21-1283-4621-93ef-93bcfe8a1dd4](./_assets/eb6b48d020/ds04_kmprun01_2fd6ad21-1283-4621-93ef-93bcfe8a1dd4.svg)
![ds04_kmprun02_9223ef2c-951b-411b-b285-e761582d39c6](./_assets/eb6b48d020/ds04_kmprun02_9223ef2c-951b-411b-b285-e761582d39c6.svg)
![ds04_kmprun03_354bf813-e9fe-4ea6-8222-5a690410883d](./_assets/eb6b48d020/ds04_kmprun03_354bf813-e9fe-4ea6-8222-5a690410883d.svg)
![ds04_kmprun04_5777eb75-ca99-46a7-9f81-395b86488ef6](./_assets/eb6b48d020/ds04_kmprun04_5777eb75-ca99-46a7-9f81-395b86488ef6.svg)
![ds04_kmprun05_abee625f-0cfc-4e25-b598-059985d0f09c](./_assets/eb6b48d020/ds04_kmprun05_abee625f-0cfc-4e25-b598-059985d0f09c.svg)
![ds04_kmprun06_6a5b6bb9-0738-4b82-b21b-4e818efa28ee](./_assets/eb6b48d020/ds04_kmprun06_6a5b6bb9-0738-4b82-b21b-4e818efa28ee.svg)
![ds04_kmprun07_5436015a-0cc3-48e1-95b9-048e19ec383a](./_assets/eb6b48d020/ds04_kmprun07_5436015a-0cc3-48e1-95b9-048e19ec383a.svg)
![ds04_kmprun08_55cb7103-08ef-44bb-89ae-47dca820906c](./_assets/eb6b48d020/ds04_kmprun08_55cb7103-08ef-44bb-89ae-47dca820906c.svg)
![ds04_kmprun09_31125657-8543-4579-b8d7-b23bd0e79c23](./_assets/eb6b48d020/ds04_kmprun09_31125657-8543-4579-b8d7-b23bd0e79c23.svg)
![ds04_kmprun10_4f3a8e31-4cf9-46d9-a344-8fa042bd48e7](./_assets/eb6b48d020/ds04_kmprun10_4f3a8e31-4cf9-46d9-a344-8fa042bd48e7.svg)
![ds04_kmprun11_cd4e973f-0619-4b42-8635-e2909916283e](./_assets/eb6b48d020/ds04_kmprun11_cd4e973f-0619-4b42-8635-e2909916283e.svg)
![ds04_kmprun12_f15b3e05-6cd3-4c07-835e-a1379a614cca](./_assets/eb6b48d020/ds04_kmprun12_f15b3e05-6cd3-4c07-835e-a1379a614cca.svg)
![ds04_kmprun13_59d7c625-4bba-4afd-8248-386fe1b26ad8](./_assets/eb6b48d020/ds04_kmprun13_59d7c625-4bba-4afd-8248-386fe1b26ad8.svg)
![ds04_kmprun14_b2a7f384-0987-457a-9e36-d3c08f2f1790](./_assets/eb6b48d020/ds04_kmprun14_b2a7f384-0987-457a-9e36-d3c08f2f1790.svg)
![ds04_kmprun15_ebf8c38c-1a04-4b5c-9a1f-6befa2ec9be0](./_assets/eb6b48d020/ds04_kmprun15_ebf8c38c-1a04-4b5c-9a1f-6befa2ec9be0.svg)
![ds04_kmprun16_02daf571-bcf1-406b-a758-292db26860d1](./_assets/eb6b48d020/ds04_kmprun16_02daf571-bcf1-406b-a758-292db26860d1.svg)

每当图中出现失配，观察主串当前位置是否仍是同一个 $i$；同时读取 `next[j]` 看新的模式位置。比起死记“失败后右移多少格”，更稳妥的方法是始终保持：**$i$ 指向下一位尚未成功匹配的主串字符，$j$ 指向下一位要比较的模式字符**。

### 5.5 `next` 的递推构造算法

如果每个位置都重新枚举所有前后缀，手算虽然可以，但算法并不高效。利用先前的 `next`，可以递推求得下一位：若已知第 $j$ 位和第 $k=next[j]$ 位字符相同，则 `next[j+1]=k+1`；否则继续把 $k$ 退到 `next[k]`，直至找到可扩展的重叠或退到 0。

![ds04_nextderive_ff646748-9ed7-485d-847d-6293e5a51d61](./_assets/eb6b48d020/ds04_nextderive_ff646748-9ed7-485d-847d-6293e5a51d61.svg)
![ds04_kmpproces_cbcda3e9-4b9e-4cc1-8cf7-286982543493](./_assets/eb6b48d020/ds04_kmpproces_cbcda3e9-4b9e-4cc1-8cf7-286982543493.svg)

以下代码完整采用**课件的 1 基数组 `next`**，但原始字符串 p 仍使用 C++ 自身的 0 基下标。这里 `next` 是变量名称而非 C++ 关键字，可以正常使用。

```cpp
#include <string>
#include <vector>

std::vector<int> buildNext(const std::string& p) {
    const int m = static_cast<int>(p.size());
    std::vector<int> next(m + 1, 0);              // 只使用 1..m，next[0] 不参与
    if (m == 0) return next;                    // 便于独立调用的空串处理
    int j = 1;                                  // 已知 next[j]，准备计算下一格
    int k = 0;                                  // k=0 时直接建立第 2 格为 1
    while (j < m) {
        if (k == 0 || p[j - 1] == p[k - 1]) {    // 注意字符串实际下标要减 1
            ++j;                                // 推进到下一个 next 位置
            ++k;                                // 已匹配重叠增加一格
            next[j] = k;                        // 第 j 位发生失配时的回退位置
        } else {
            k = next[k];                        // 不能扩展则寻找更短的重叠
        }
    }
    return next;
}
```

这里返回长度为 $m+1$ 的 `vector<int>`，下标 $0$ 是未使用的占位，合法的课程 `next` 值存在下标 $1..m$。对于 `"abaabcac"` 结果依次为 `0,1,1,2,2,3,1,2`。

### 5.6 用 `next` 完成真正的 KMP 搜索

```cpp
#include <string>
#include <vector>
#include <stdexcept>

int indexKMP(const std::string& s, const std::string& p,
             int pos = 1) {
    if (p.empty() || pos < 1) {
        throw std::invalid_argument("invalid pattern or position");
    }
    const std::vector<int> next = buildNext(p); // 按课程 1 基规则预处理
    const int n = static_cast<int>(s.size());
    const int m = static_cast<int>(p.size());
    int i = pos;                                  // 主串当前位置，1 基
    int j = 1;                                    // 模式当前位置，1 基
    while (i <= n && j <= m) {
        if (j == 0 || s[i - 1] == p[j - 1]) {     // j=0 时不读取 p[-1]
            ++i;                                  // 消耗一个主串字符
            ++j;                                  // 前进到下一个模式字符
        } else {
            j = next[j];                          // 失配后主串位置 i 保持不变
        }
    }
    return j > m ? i - m : 0;                     // 成功给 1 基位置，失败返回 0
}
```

**时间复杂度**：求 `next` 花 $O(m)$，主串扫描花 $O(n)$，整体为 $O(n+m)$；`next` 数组占 $O(m)$ 辅助空间。即使主串出现大量重复字符、模式存在复杂前后缀结构，这一最坏量级也不变。`nextval` 只减少特定情况下的重复字符比较，并不改变复杂度阶。

![ds04_complexity_6ec9c8da-9455-47b2-bee7-35358bb20de1](./_assets/eb6b48d020/ds04_complexity_6ec9c8da-9455-47b2-bee7-35358bb20de1.svg)

![ds04_home1next_b055fc55-0a0e-4333-956d-f5f8ea988d4e](./_assets/eb6b48d020/ds04_home1next_b055fc55-0a0e-4333-956d-f5f8ea988d4e.svg)

### 5.7 另一道课堂手算实例：`abcabaa`

这道模式是练习递推法的典型例子：

$$
T=\texttt{abcabaa},\qquad \operatorname{next}=[0,1,1,1,2,3,2].
$$

不要看见两个 `a` 就直接认为所有位置的前后缀都相同。每个 `next[j]` 只依赖**当前失配之前的字符**，并必须从最长匹配的重叠开始考虑。

![ds04_abcnext_a202bdf0-a4a1-43b3-b6f1-b62304cc2244](./_assets/eb6b48d020/ds04_abcnext_a202bdf0-a4a1-43b3-b6f1-b62304cc2244.svg)
![ds04_nexthome1_88569e50-36e8-4e22-bfc4-abe6026e89d0](./_assets/eb6b48d020/ds04_nexthome1_88569e50-36e8-4e22-bfc4-abe6026e89d0.svg)
![ds04_nexthome2_4a48313e-acfb-4c2f-ace5-73d5b6697501](./_assets/eb6b48d020/ds04_nexthome2_4a48313e-acfb-4c2f-ace5-73d5b6697501.svg)
![ds04_nexthome3_be23077d-c3ff-4ac9-965a-5586dda3dded](./_assets/eb6b48d020/ds04_nexthome3_be23077d-c3ff-4ac9-965a-5586dda3dded.svg)
![ds04_nexthome4_068e8082-23df-4119-860a-0288d7d400f3](./_assets/eb6b48d020/ds04_nexthome4_068e8082-23df-4119-860a-0288d7d400f3.svg)
![ds04_nexthome5_a51ef56b-f313-4e20-8d0b-8e80fe69efba](./_assets/eb6b48d020/ds04_nexthome5_a51ef56b-f313-4e20-8d0b-8e80fe69efba.svg)
![ds04_nexthome6_c994fd51-2029-4f50-a7c3-15cc9e7ea67b](./_assets/eb6b48d020/ds04_nexthome6_c994fd51-2029-4f50-a7c3-15cc9e7ea67b.svg)
![ds04_nexthome7_4b625814-9f2b-4530-9002-079346444d6b](./_assets/eb6b48d020/ds04_nexthome7_4b625814-9f2b-4530-9002-079346444d6b.svg)

> [!warning] 不能混淆“最长公共前后缀长度”与“回退后的模式位置”
> 若一段已匹配前缀的最长相等真前后缀长度为 $k$，在课程 1 基约定中下一次比较的位置是 $k+1$。其中 $j=1$ 必须单独定义为 $0$，不适用这个加一公式。


## 六、改进失败函数 `nextval`：去掉注定失败的比较

### 6.1 `next` 为什么还有重复比较

KMP 的 `next` 已经保证主串指针不回退，但在一些连续重复字符模式上，还可能发生一连串**明知不可能相等的比较**。例如模式串

$$T=\texttt{aaaab},\qquad \operatorname{next}=[0,1,2,3,4].$$

假设当前模式第 $4$ 位字符 `a` 与主串当前字符失配，`next[4]=3` 让模式退到第 $3$ 位，但是第 $3$ 位也恰好是 `a`：既然主串字符已经不等于 `a`，再跟另一处 `a` 比较必然失败。退到第 $2$、$1$ 位同理，造成多余的字符比较。

![ds04_nextvalmotivation_99b7a57e-eff5-49c3-b03a-550c96ef8b27](./_assets/eb6b48d020/ds04_nextvalmotivation_99b7a57e-eff5-49c3-b03a-550c96ef8b27.svg)
![ds04_aaaanext_5350d0d0-027d-4866-a3f5-9f91a899e0bd](./_assets/eb6b48d020/ds04_aaaanext_5350d0d0-027d-4866-a3f5-9f91a899e0bd.svg)
![ds04_aaaaval_ec97b00b-fcd7-4196-9dcb-537e107943b1](./_assets/eb6b48d020/ds04_aaaaval_ec97b00b-fcd7-4196-9dcb-537e107943b1.svg)

改进 `nextval` 的思想：若**待失配位置的模式字符**和**普通 next 指向位置的模式字符相同**，就直接跳到那一位置的 `nextval`，跳过重复且注定失败的比较。

$$
\boxed{\mathrm{nextval}[1]=0},\qquad
\boxed{\mathrm{nextval}[j]=
\begin{cases}
\mathrm{nextval}[\mathrm{next}[j]],&T[j]=T[\mathrm{next}[j]],\\
\mathrm{next}[j],&T[j]\ne T[\mathrm{next}[j]],
\end{cases}}\quad(j\ge 2).
$$

上式以课程的 1 基 `next[j]` 为前提，并且对于 $j\ge2$，`next[j]` 必在 $1\ldots j-1$ 的有效范围内，因此右侧的 `nextval` 已经计算完成。

### 6.2 连续相同字符示例

模式 `"aaaab"` 的 `next` 和 `nextval` 分别是：

| 位置 j | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| 模式字符 | a | a | a | a | b |
| `next[j]` | 0 | 1 | 2 | 3 | 4 |
| `nextval[j]` | 0 | 0 | 0 | 0 | 4 |

例如第 $3$ 位失配时，本来 `next[3]=2`，但第 $3$ 位与第 $2$ 位都是 `a`，因此直接置 `nextval[3]=nextval[2]=0`，无需把已知不等于 `a` 的主串字符再同另一个 `a` 比较。第 $5$ 位是 `b`，而 `next[5]=4` 对应字符 `a`；二者不同，因此 `nextval[5]=4`。

下面五张图分别标明每个位置的比较和回退选择：

![ds04_nextvalaaaa1_a222423c-6566-44f3-b5d4-e47a4639b641](./_assets/eb6b48d020/ds04_nextvalaaaa1_a222423c-6566-44f3-b5d4-e47a4639b641.svg)
![ds04_nextvalaaaa2_c66769b9-be94-4c3d-b181-474d53729095](./_assets/eb6b48d020/ds04_nextvalaaaa2_c66769b9-be94-4c3d-b181-474d53729095.svg)
![ds04_nextvalaaaa3_e18a2d03-efa6-455d-b445-39b6d5aec4a7](./_assets/eb6b48d020/ds04_nextvalaaaa3_e18a2d03-efa6-455d-b445-39b6d5aec4a7.svg)
![ds04_nextvalaaaa4_209f7ef2-a821-49c7-ada3-e1b96d668259](./_assets/eb6b48d020/ds04_nextvalaaaa4_209f7ef2-a821-49c7-ada3-e1b96d668259.svg)
![ds04_nextvalaaaa5_54ab5e9a-c40e-44d1-9905-a5b09a4de73c](./_assets/eb6b48d020/ds04_nextvalaaaa5_54ab5e9a-c40e-44d1-9905-a5b09a4de73c.svg)

> [!important] `nextval` 不代表简单“把 next 中重复数字变成 0”
> 它不是从序列形状直接删数，而是比较 **$T[j]$ 与 $T[\mathrm{next}[j]]$ 的字符是否相等**。只有相等时才沿失败链接继续跳过；否则必须保留原 `next[j]` 值。

### 6.3 `abaabcac` 的逐位 `nextval`

已知

$$
T=\texttt{abaabcac},\qquad
\operatorname{next}=[0,1,1,2,2,3,1,2].
$$

根据刚才的字符判断规则，最终得到

$$
\boxed{\operatorname{nextval}=[0,1,0,2,1,3,0,2]}.
$$

![ds04_baseval_706b96d4-c615-409a-b028-6e3471c9a6ef](./_assets/eb6b48d020/ds04_baseval_706b96d4-c615-409a-b028-6e3471c9a6ef.svg)

逐位计算时，不是只对最后结果做一个不透明的表格，而是看每一个 $j$ 对应的 `next[j]` 指向了哪个位置，判断两处字符是否一样。下列图可将推理完整走一遍：

![ds04_nextvalbase1_42568c67-e712-4e41-8ae2-f9955d05acf2](./_assets/eb6b48d020/ds04_nextvalbase1_42568c67-e712-4e41-8ae2-f9955d05acf2.svg)
![ds04_nextvalbase2_d614d9cf-dcd1-4655-9a6f-24a418248bf4](./_assets/eb6b48d020/ds04_nextvalbase2_d614d9cf-dcd1-4655-9a6f-24a418248bf4.svg)
![ds04_nextvalbase3_2969372b-173e-4086-aa05-14caf5e093c9](./_assets/eb6b48d020/ds04_nextvalbase3_2969372b-173e-4086-aa05-14caf5e093c9.svg)
![ds04_nextvalbase4_cedcf15d-7104-4dab-8957-06d4f925023d](./_assets/eb6b48d020/ds04_nextvalbase4_cedcf15d-7104-4dab-8957-06d4f925023d.svg)
![ds04_nextvalbase5_0dfd015c-e417-4c9b-bf52-5b2d4703255f](./_assets/eb6b48d020/ds04_nextvalbase5_0dfd015c-e417-4c9b-bf52-5b2d4703255f.svg)
![ds04_nextvalbase6_5da8c066-6644-43fc-ac98-6cb3abb6b7da](./_assets/eb6b48d020/ds04_nextvalbase6_5da8c066-6644-43fc-ac98-6cb3abb6b7da.svg)
![ds04_nextvalbase7_0bf53157-1067-4246-b3e8-962a2288763d](./_assets/eb6b48d020/ds04_nextvalbase7_0bf53157-1067-4246-b3e8-962a2288763d.svg)
![ds04_nextvalbase8_99b98193-1af5-4097-aed0-09eff20b716b](./_assets/eb6b48d020/ds04_nextvalbase8_99b98193-1af5-4097-aed0-09eff20b716b.svg)

特别是：

- $j=3$，`T[3]=a`，`next[3]=1`，而 `T[1]=a`，因此 `nextval[3]=nextval[1]=0`。
- $j=5$，`T[5]=b`，`next[5]=2`，而 `T[2]=b`，因此 `nextval[5]=nextval[2]=1`。
- $j=8$，`T[8]=c`，`next[8]=2`，`T[2]=b`，不相等，保留 `nextval[8]=2`。

![ds04_sampleval_05e8dcea-1c02-4e77-9596-f6d9bba3cf22](./_assets/eb6b48d020/ds04_sampleval_05e8dcea-1c02-4e77-9596-f6d9bba3cf22.svg)

### 6.4 `nextval` 的完整构造代码

下面代码直接使用上面已经定义的 `buildNext` 函数。输入模式串 p，输出**1 基**的 `nextval` 表，仍然使用下标 0 作未使用占位：

```cpp
#include <string>
#include <vector>

std::vector<int> buildNextVal(const std::string& p) {
    const int m = static_cast<int>(p.size());
    const std::vector<int> next = buildNext(p); // 先得到课程的 1 基 next
    std::vector<int> nextval(m + 1, 0);        // nextval[1] 特判为 0
    for (int j = 2; j <= m; ++j) {            // 从第二个模式字符开始
        const int k = next[j];                // 普通失败回退位置 k
        if (p[j - 1] == p[k - 1]) {           // 当前字符与回退后字符相同
            nextval[j] = nextval[k];          // 跳过注定失败的重复比较
        } else {
            nextval[j] = k;                   // 不同则维持普通失败链接
        }
    }
    return nextval;
}
```

用 `nextval` 完成搜索时，只需要把上一节 `indexKMP` 里预处理所用的 `buildNext(p)` 换成 `buildNextVal(p)`；其他匹配循环、匹配成功条件、返回位置都可以保持不变。

> [!warning] KMP 失配时的三个不同情形
> （1）当前 `S[i]==T[j]`：两个指针一起后移；（2）字符不等且 `j>0`：**仅 j 根据 next 或 nextval 跳转**；（3）`j=0`：说明没有任何可复用前缀，下一轮才将主串位置前进一位并将模式指针改为 1。把三种情形混成一个 `i++` 会漏掉匹配结果。

### 6.5 为什么优化没有改变复杂度阶

两种失败数组都可以在 $O(m)$ 的时间内构造；搜索均为 $O(n)$，故 KMP 整体最坏时间仍然是 $O(n+m)$。改进收益是**减少某些重复字符导致的无效字符比较次数**，而不是把渐进复杂度改写成 $O(1)$ 或 $O(\log n)$。

![ds04_nexttraps_bfd2af1f-a20f-4b92-92e6-eb3c210381e6](./_assets/eb6b48d020/ds04_nexttraps_bfd2af1f-a20f-4b92-92e6-eb3c210381e6.svg)

### 6.6 降低混淆：几个模式的回退链

遇到失配时可以只看失败函数，沿着 `j→next[j]→next[next[j]]→…→0` 画出递减链。这条链完全由**模式自身**决定，和主串的具体字符没有关系；是否在某一级提前匹配成功，才由主串当前字符决定。以下独立小图帮助识别不同的模式前后缀结构：

![ds04_fallaaaa_e11d736f-ee1c-4c1b-9ce9-b8f15cc2e7d7](./_assets/eb6b48d020/ds04_fallaaaa_e11d736f-ee1c-4c1b-9ce9-b8f15cc2e7d7.svg)
![ds04_fallaaab_40647cca-d613-47fe-91cb-701e4447067a](./_assets/eb6b48d020/ds04_fallaaab_40647cca-d613-47fe-91cb-701e4447067a.svg)
![ds04_fallabab_88923710-44e7-491c-b20b-011e21aaa610](./_assets/eb6b48d020/ds04_fallabab_88923710-44e7-491c-b20b-011e21aaa610.svg)
![ds04_fallabcac_7bb1d6f0-0372-426b-8fce-8e1429359f87](./_assets/eb6b48d020/ds04_fallabcac_7bb1d6f0-0372-426b-8fce-8e1429359f87.svg)
![ds04_fallabaabcac_5b5802c6-a665-49b8-b3af-33dba743d284](./_assets/eb6b48d020/ds04_fallabaabcac_5b5802c6-a665-49b8-b3af-33dba743d284.svg)

## 七、典型例题、课程练习与参考答案

### 7.1 基本串运算综合例题

给定

$$
s=\texttt{'I AM A STUDENT'},\qquad
 t=\texttt{'GOOD'},\qquad
q=\texttt{'WORKER'}.
$$

这里单引号用于表示串值，并不包含在实际字符内。特别注意空格位置：

| 位序 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 字符 | I | 空格 | A | M | 空格 | A | 空格 | S | T | U | D | E | N | T |

![ds04_exercise1_bdb37642-5d32-4b56-b655-f0aa7f9a132f](./_assets/eb6b48d020/ds04_exercise1_bdb37642-5d32-4b56-b655-f0aa7f9a132f.svg)

据此，可按课件位置约定逐项算出：

| 操作 | 结果 | 说明 |
|---|---|---|
| `StrLength(s)` | $14$ | 有 3 个空格也要计数 |
| `StrLength(t)` | $4$ | `GOOD` 4 个字符 |
| `SubString(s,8,7)` | `STUDENT` | 第 8–14 位 |
| `SubString(t,2,1)` | `O` | 第 2 位字符 |
| `Index(s,'A')` | $3$ | 第一个 A 在第 3 位 |
| `Index(s,t)` | $0$ | `GOOD` 未出现 |
| `Replace(s,'STUDENT',q)` | `I AM A WORKER` | 用 WORKER 替换 STUDENT |
| `Concat(SubString(s,6,2), Concat(t,SubString(s,7,8)))` | `A GOOD STUDENT` | 依次得到 `A `、`GOOD`、` STUDENT` |

> [!tip] 计算嵌套操作的原则
> 自内向外展开。不要为了“看起来顺眼”就删除中间空格：`SubString(s,6,2)` 为 `"A "`，末尾有一个空格；`SubString(s,7,8)` 是 `" STUDENT"`，开头也有一个空格。

### 7.2 手算 `next` / `nextval`：`aaab`

对模式 `"aaab"`，课程 1 基字符位置为 $1,2,3,4$：

$$
\operatorname{next}=[0,1,2,3],\qquad
\operatorname{nextval}=[0,0,0,3].
$$

![ds04_examaaab_2a9d518f-18cb-4e79-8616-6b967829c797](./_assets/eb6b48d020/ds04_examaaab_2a9d518f-18cb-4e79-8616-6b967829c797.svg)
![ds04_examvalaaab_80f28321-e375-48b6-9a08-9e418813f92c](./_assets/eb6b48d020/ds04_examvalaaab_80f28321-e375-48b6-9a08-9e418813f92c.svg)

因为三个连续的 `a` 会使 `next` 在它们之间逐级回退，`nextval` 可把这些“已经确定失败”的重复比较直接压掉；但在末位 `b` 失配时，回退位置的 `a` 与 `b` 不同，所以保留 $3$。

![ds04_home1val_003d66fb-db60-4ed0-994a-d7358d9efec9](./_assets/eb6b48d020/ds04_home1val_003d66fb-db60-4ed0-994a-d7358d9efec9.svg)

### 7.3 手算 `next` / `nextval`：`abcabaa`

这道题比全相同字符更接近真实 KMP：

$$
\begin{aligned}
T&=\texttt{abcabaa},\\
\operatorname{next}&=[0,1,1,1,2,3,2],\\
\operatorname{nextval}&=[0,1,1,0,1,3,2].
\end{aligned}
$$

![ds04_examabcabaa_53d8dddc-bdc7-4b22-94e5-a599818ef138](./_assets/eb6b48d020/ds04_examabcabaa_53d8dddc-bdc7-4b22-94e5-a599818ef138.svg)
![ds04_examvalabcabaa_2c6e054b-b0aa-4193-a3b0-6e4bc221581b](./_assets/eb6b48d020/ds04_examvalabcabaa_2c6e054b-b0aa-4193-a3b0-6e4bc221581b.svg)
![ds04_abcval_29e787ed-a4c3-42c5-a54f-f8b3555148c9](./_assets/eb6b48d020/ds04_abcval_29e787ed-a4c3-42c5-a54f-f8b3555148c9.svg)

注意第 $4$ 位字符是 `a`，普通 `next[4]=1`，对应第 $1$ 位也是 `a`，故 `nextval[4]=nextval[1]=0`。第 $6$ 位是 `a`，`next[6]=3` 对应 `c`，不同，所以保留 $3$。

### 7.4 较长模式的 `next` / `nextval`

对模式 `"abcaabbabcabaacbacba"`，字符串共 $20$ 位，结果是：

$$
\begin{aligned}
\operatorname{next}={}&[0,1,1,1,2,2,3,1,2,3,4,5,3,2,2,1,1,2,1,1],\\
\operatorname{nextval}={}&[0,1,1,0,2,1,3,0,1,1,0,5,3,2,2,1,0,2,1,0].
\end{aligned}
$$

![ds04_examabcaabbabcabaacbacba_27ec8668-1e49-4e8b-846b-7b127b7f83c5](./_assets/eb6b48d020/ds04_examabcaabbabcabaacbacba_27ec8668-1e49-4e8b-846b-7b127b7f83c5.svg)
![ds04_examvalabcaabbabcabaacbacba_d38e4017-715a-4f05-a295-ddd906a49c4c](./_assets/eb6b48d020/ds04_examvalabcaabbabcabaacbacba_d38e4017-715a-4f05-a295-ddd906a49c4c.svg)

对长模式不推荐一口气直接写出整排数值。逐位维护一个 `k`，若当前模式字符与可扩展位置相等就把有效前后缀延长，否则沿失败链缩短；最后再独立判断下一次失败能否使用 `nextval` 跳过相同字符。**建议把下一格的求解理由写在草稿上，而不是靠看图猜规律。**

### 7.5 练习：从 s 中删除全部等于 t 的非重叠子串

问题：给定主串 s 和**非空**模式 t，删除 s 中所有与 t 完全相同且不重叠的连续片段，保留其他字符的相对次序。例如 `s="abXXabYYab"`、`t="ab"`，结果为 `"XXYY"`。

![ds04_deleteall_cfa2563b-7b95-47ac-b978-80c6afdcedbb](./_assets/eb6b48d020/ds04_deleteall_cfa2563b-7b95-47ac-b978-80c6afdcedbb.svg)

可以逐次 `find`，只把匹配之间的普通字符拼进结果；发现一次匹配后移动到它的末尾之后。下面给出正确的 C++ 实现：

```cpp
#include <string>
#include <stdexcept>

std::string removeAll(const std::string& s, const std::string& t) {
    if (t.empty()) {                              // 删除空模式没有明确语义
        throw std::invalid_argument("empty pattern");
    }
    std::string result;
    std::size_t from = 0;                         // 原串未处理区间的起点
    while (from < s.size()) {
        const std::size_t at = s.find(t, from);   // 找下一处匹配
        if (at == std::string::npos) break;       // 找不到则只需处理剩余字符
        result.append(s, from, at - from);        // 追加非匹配的原串前缀
        from = at + t.size();                     // 完整跳过本段 t
    }
    result.append(s, from, s.size() - from);      // 将剩余的普通字符追加
    return result;                                // 返回删除后的新串
}
```

> [!warning] “不重叠删除”和“反复对新串查找”并不总是等价
> 如果删除某段后让原先分隔的字符在新串里相邻，就可能产生在**原串中不存在**的新匹配。若题意采用课程的非重叠模式语义，应扫描原串一次而不是无限循环直至新串再也没有 t。只有当题目明确规定“反复删除直到无法继续”时，才采用后者。

### 7.6 验证题：BF 与 KMP 的结果必须一致

无论模式具有多少重复前后缀，只要两种算法对输入约定一致，**同一主串、同一模式、同一起点**应返回相同的位置或都返回 0。可以使用以下用例核对：

| 主串 S | 模式 T | 预期 Index | 用途 |
|---|---|---:|---|
| `ababcabcacbab` | `abcac` | 6 | 多次试探后成功 |
| `acabaabaabcacaabc` | `abaabcac` | 6 | 包含 KMP 失配与复用 |
| `aaaaaaab` | `aaaab` | 4 | 长重复前缀 |
| `abcabcabc` | `abcd` | 0 | 没有完整匹配 |
| `zzabczzabc`，从第 4 位开始 | `abc` | 8 | 指定搜索起点 |

最后一行从第 4 位开始：第 3 位那次匹配不属于合法搜索范围，找到的是后面的第 8 位。推荐采用**穷举短字符串**的方法做程序一致性测试：枚举二字符字母表上的所有较短主串、非空模式和合法起点，逐个比较 `IndexBF`、`indexKMP` 与对应约定的标准库 `find` 结果。

## 八、知识结构和速查

![ds04_review_87a53265-88ab-41d9-8a90-e9a1ac7ef422](./_assets/eb6b48d020/ds04_review_87a53265-88ab-41d9-8a90-e9a1ac7ef422.svg)

### 8.1 操作与边界速查

| 要记住的内容 | 课堂约定或核心公式 |
|---|---|
| 空串 | 长度 $0$，不同于空格串 |
| 子串 | 主串中**连续**的字符序列 |
| 匹配起点 | 从第 `pos` 位（包含）起尝试 |
| `Index` 失败 | 返回 `0` |
| `SubString` | 起点 `pos`、长度 `len`，结果可为空串 |
| 定长串 | 0 号单元可保存长度，字符从 1 号单元开始 |
| 堆分配串 | 动态分配一段**连续**的字符内存 |
| 块链串 | 一个结点保存一个或多个字符，并有后继指针 |
| BF | 失配后重新枚举下一个主串起点，最坏 $O(nm)$ |
| KMP | 主串指针不回退，最坏 $O(n+m)$ |
| `next[1]` | 特殊定义为 $0$ |
| `next[j]`，$j\ge2$ | 已匹配 $T[1..j-1]$ 的最长相等真前后缀长度 $+1$ |
| `nextval[j]` | 通过比较 $T[j]$ 和 $T[next[j]]$ 决定是否跳过重复失败 |
| 典型易错 | 教材 1 基下标 / `std::string` 0 基下标不可混用 |

### 8.2 算法选择

一般小规模、单次匹配或课堂算法验证时，BF 简单且容易检查；当模式较长、主串规模较大、数据含大量重复前后缀时，KMP 能提供线性最坏时间保证。首尾匹配可能减少候选起点处的平均字符比较，但不能承诺 KMP 的最坏复杂度。若只是完成普通 C++ 项目里的子串查找，通常优先使用 `std::string::find`，无需重复实现底层算法；若课程要求实现 KMP，则应严格使用约定的 `next`、`nextval` 和失败处理逻辑。

> [!summary] 结束复盘
> 本章应能做到三件事：**准确计算每种串操作的结果和参数范围；能够画出并解释三种存储结构；给定一个模式串，可独立计算每一位 `next`、`nextval`，写出 BF/KMP 的匹配状态变化与时间复杂度。**
