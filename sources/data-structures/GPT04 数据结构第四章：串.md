# 第四章 串（String）——系统知识笔记

> [!abstract] 本章知识主线
> **串是什么 → 能进行哪些操作 → 字符如何存入内存 → 怎样查找一个子串 → 怎样避免重复比较。**
>
> 核心知识分为三组：①串的逻辑结构与基本操作；②定长顺序存储、堆分配存储、块链存储；③BF、首尾匹配和KMP，尤其是 **`next` 与 `nextval` 的手算、含义及代码实现**。
>
> **阅读约定**：解释课件中 `Index`、`SubString`、BF、KMP 时，位置均从 **1** 开始，匹配失败返回 **0**；C/C++ 内建数组及 `std::string` 的索引从 **0** 开始。两种编号在代码中明确转换，不混用。

> [!important] 为什么这一章重要？
> 串虽可看作特殊的线性表，但其基本操作通常针对**一段字符序列**，而不是单个元素。尤其在模式匹配中，怎样利用已经比较过的字符，是从朴素算法走向KMP算法的关键。

---

## 一、串的逻辑结构：概念与辨析

### 1.1 串的定义

**串（String，字符串）**是由零个或多个字符构成的有限序列，记为

$$
s='a_1a_2\cdots a_n'\qquad(n\ge 0)
$$

其中，$s$ 为串名，$a_i$ 为字符，第 $i$ 个字符的位序为 $i$，**串长**为 $n$。

例如：

- `"hello"`：长度为5。
- `"abc123"`：长度为6。数字 `1`、`2`、`3` 在这里是字符，并非数值。
- `""`：空串，长度为0。
- `"   "`：包含3个空格的空格串，长度为3。
- `"a a"`：长度为3，中间的空格也是实际字符。

> [!note] 课件中的单引号与编程语言的引号不同
> 课件写 `s='abc'` 是数学意义上的**串值记法**，单引号不属于串值。在C++里，字符串字面量使用 **双引号** `"abc"`；单引号 `'a'` 表示一个字符。不能直接把课件中所有的 `‘...’` 当作C++代码抄写。

**C++代码示例：比较空串与空格串**（可独立编译运行）：

```cpp
#include <iostream>
#include <string>

int main() {
    std::string a = "";       // 一个字符也没有。
    std::string b = " ";      // 一个空格字符。
    std::string c = "   ";    // 三个空格字符。

    std::cout << a.size() << '\n'; // 输出0。
    std::cout << b.size() << '\n'; // 输出1。
    std::cout << c.size() << '\n'; // 输出3。
}
```

### 1.2 子串、主串、字符位置和子串位置

- **子串**：从某个串中取出的**连续**字符序列；允许子串长度为0。
- **主串**：包含所查找子串的串。
- **字符位置**：该字符在串中的序号。
- **子串位置**：该子串的**第一个字符**在主串中的位置。

设主串 `S="datastructure"`，按课件的1基位置：

| 子串 | 起始位置 | 长度 | 说明 |
| --- | ---: | ---: | --- |
| `"data"` | 1 | 4 | 从第1个字符开始 |
| `"structure"` | 5 | 9 | 从第5个字符开始 |
| `"str"` | 5 | 3 | 在主串中连续出现 |
| `"atu"` | 不存在 | — | 虽含相关字母，却并非连续排列 |
| `""` | 按约定可取空子串 | 0 | 空串是任意串的子串 |
| `"datastructure"` | 1 | 13 | 每个串都是自身的子串 |

注意，**子串与子序列不是一个概念**：`"abcde"` 的 `"bcd"` 是子串，`"ace"` 是子序列但不是子串。教材在介绍子串时有时会使用“字符子序列”的表述，理解时必须保留“连续”的条件。

> [!example] 位置与长度练习
> 令 `S="computer"`，求：
> 
> 1. 从第4个字符开始、长度为3的子串是 `"put"`。
> 2. `"ter"` 的起始位置是第6位。
> 3. `"compute"` 是前7个字符。
> 4. `"cmt"` 不是子串，因为中间跳过了字符。

### 1.3 串相等与串的大小比较

两个串相等，当且仅当**长度相等**且**对应位置的字符逐一相等**。

例如，`"abc"` 与 `"abc"` 相等；`"abc"` 与 `"abC"` 不相等；`"abc"` 与 `"abc "` 不相等。

**串的比较（`StrCompare`）**通常按字符的顺序逐个比较：在第一个不同字符处决定大小；若共有前缀完全相同，则较短的串排在前面。这里比较的是编码意义上的字符顺序，不是自然语言的词典语义。

```cpp
#include <iostream>
#include <string>

int main() {
    std::string a = "abc";
    std::string b = "abd";
    std::string c = "abcde";

    std::cout << (a == "abc") << '\n'; // 1：相等。
    std::cout << (a < b) << '\n';      // 1：'c' 小于 'd'。
    std::cout << (a < c) << '\n';      // 1：相同前缀下短串更小。
    std::cout << a.compare(b) << '\n'; // 负值：a < b，具体数值不强求。
}
```

> [!warning] 比较字符串并非比较数字大小
> `"10"` 与 `"2"` 是两个字符串；按通常字符编码顺序，`"10" < "2"`，因为先比较首字符 `'1'` 与 `'2'`。若希望比较数值大小，应先将输入转换为数值并验证合法性。

### 1.4 串和线性表的联系与区别

| 比较维度 | 普通线性表 | 串 |
| --- | --- | --- |
| 逻辑结构 | 有序的线性序列 | 有序的线性序列 |
| 数据对象 | 可为某种一般数据元素 | **只能是字符** |
| 常见操作对象 | 单个元素 | 整个串或一段子串 |
| 典型操作 | 元素插入、删除、访问 | 拼接、求子串、比较、查找、替换 |
| 特有重点 | 元素位置的移动、链式关系 | **多字符的模式匹配** |

**关键认识**：逻辑结构相似不意味着算法研究重点也完全相同。串的模式匹配需要特别处理多个连续字符的比较关系。

---

## 二、串的抽象数据类型与基本操作

### 2.1 ADT String 的内容

课件将串定义为一个抽象数据类型：数据对象是字符序列，数据关系是相邻字符之间的先后关系。ADT用来规定**什么操作合法、产生什么结果**；它不是语言内置的 `ADT` 类型，也不要求在代码里额外定义一个抽象占位类型。

课件列出13种操作，其中有6种构成讨论中的**最小操作子集**。

| 分类 | 操作 | 作用 |
| --- | --- | --- |
| 基础构造 | `StrAssign(&T, chars)` | 以指定字符序列赋值给串T |
| 复制 | `StrCopy(&T, S)` | 将S复制给T |
| 判空 | `StrEmpty(S)` | 判断S是否为空串 |
| 比较 | `StrCompare(S, T)` | 返回比较结果（正/零/负） |
| 求长 | `StrLength(S)` | 返回S中的字符数量 |
| 清空 | `ClearString(&S)` | 将已有串变成空串 |
| 拼接 | `Concat(&T, S1, S2)` | 将S1、S2连接为T |
| 取子串 | `SubString(&Sub, S, pos, len)` | 从第pos个字符起复制len个字符 |
| 定位 | `Index(S, T, pos)` | 从指定位置起寻找T的首次出现 |
| 替换 | `Replace(&S, T, V)` | 将与T相等的非重叠子串用V替换 |
| 插入 | `StrInsert(&S, pos, T)` | 在第pos个字符前插入T |
| 删除 | `StrDelete(&S, pos, len)` | 删除指定位置与长度的子串 |
| 销毁 | `DestroyString(&S)` | 销毁串并释放相关资源 |

> [!important] 课件特别强调的6种基本操作
> **串赋值、串复制、串比较、求串长、串联接、求子串**。
>
> 可以以这些操作为基础构造定位、插入、替换等其他操作。清空和销毁涉及对象状态与存储资源管理，课件在讨论组合实现时将其单独排除。

课件使用的 `&S` 表示某种“通过参数修改S”的教材式接口，不等于把这些操作名称直接放进C程序就能执行；本笔记示例均改为标准C++的具体实现。

### 2.2 读取与操作：串长、赋值、复制、清空

```cpp
#include <iostream>
#include <string>

int main() {
    std::string s = "old";       // 创建并初始化串S。
    std::string t = "new";       // 创建串T。
    s = t;                       // 相当于StrCopy：复制T到S。
    std::cout << s.size() << '\n'; // 相当于StrLength：输出3。
    std::cout << s.empty() << '\n'; // 相当于StrEmpty：输出0。
    s.clear();                   // 相当于ClearString：逻辑上置为空串。
    std::cout << s.empty() << '\n'; // 输出1。
}
```

`clear()`与内存释放不应混同：`std::string::clear()`保证串长变为0，但**不保证立刻把容量还给系统**；这一点不同于课件抽象层面的“销毁”。

### 2.3 子串操作 `SubString`

教材规定：原串非空时，通常要求

$$
1\le pos\le \operatorname{StrLength}(S),\qquad 0\le len\le \operatorname{StrLength}(S)-pos+1.
$$

解释：

1. `pos`必须指向主串中存在的字符。
2. `len`不能为负数。
3. 剩余最多可以复制 `串长-pos+1` 个字符。
4. `len=0`允许返回空串。

例如，`S="command"`：

| 调用 | 结果 | 理由 |
| --- | --- | --- |
| `SubString(S,4,3)` | `"man"` | 第4～6位 |
| `SubString(S,1,7)` | `"command"` | 全部字符 |
| `SubString(S,7,1)` | `"d"` | 最后一个字符 |
| `SubString(S,5,0)` | `""` | 合法的0长度子串 |
| `SubString(S,6,3)` | 不合法 | 从第6位到末尾只剩2个字符 |

C++标准库中的 `substr` 从 **0** 开始计数：

```cpp
#include <iostream>
#include <string>

int main() {
    std::string s = "command";
    std::cout << s.substr(3, 3) << '\n'; // 输出man：教材第4位对应索引3。
    std::cout << s.substr(4, 0) << '\n'; // 空子串：不会显示可见字符。
    std::cout << s.substr(6, 1) << '\n'; // 输出d。
}
```

> [!warning] `std::string::substr` 的边界与教材不完全一样
> 标准库允许 `substr(s.size(), 0)`，结果为空串；课件的 `SubString` 初始条件通常把 `pos` 限制在 `1` 到 `StrLength(S)` 之间，因此若机械移植，需要主动选定边界规范。**题目问课件ADT时按课件约定；实际写标准库代码时按标准库的规则。**

### 2.4 串拼接 `Concat`

串拼接是**依次保存S1全部字符，再保存S2全部字符**，不在中间自动添加空格。

例如：

- `Concat("data","base") = "database"`
- `Concat("data"," base") = "data base"`
- `Concat("", "hello") = "hello"`

```cpp
#include <iostream>
#include <string>

int main() {
    std::string s1 = "data";
    std::string s2 = "base";
    std::string t = s1 + s2; // '+' 对std::string执行拼接。
    std::cout << t << '\n';  // database
    t += " system";          // 把附加文本接到原串后面。
    std::cout << t << '\n';  // database system
}
```

### 2.5 定位操作 `Index`：特别注意起始位置

`Index(S,T,pos)`表示：**从主串的第pos个字符起**，向右查找与非空模式串T相等的子串，返回第一次出现的 **1基位置**，若不存在则返回0。

课件给出的典型例子：

`S="abcaabcaaabc"`、`T="bca"`。

| 操作 | 结果 | 原因 |
| --- | ---: | --- |
| `Index(S,T,1)` | 2 | 第2位首次出现 `"bca"` |
| `Index(S,T,3)` | 6 | 跳过第2位的匹配，找到第6位 |
| `Index(S,T,8)` | 0 | 从第8位向后找不到匹配 |

```cpp
#include <iostream>
#include <string>

// pos 与返回值都按教材的1基位置，失败返回0。
int index1(const std::string& s, const std::string& t, int pos) {
    if (pos < 1 || pos > static_cast<int>(s.size()) || t.empty()) return 0;
    std::size_t found = s.find(t, static_cast<std::size_t>(pos - 1));
    return found == std::string::npos ? 0 : static_cast<int>(found) + 1;
}

int main() {
    std::string s = "abcaabcaaabc";
    std::cout << index1(s, "bca", 1) << '\n'; // 2。
    std::cout << index1(s, "bca", 3) << '\n'; // 6。
    std::cout << index1(s, "bca", 8) << '\n'; // 0。
}
```

### 2.6 插入与删除：位置表示什么？

`StrInsert(S,pos,T)`是在 **第pos个字符之前** 插入T，允许 `pos=串长+1`，表示在末尾附加。

例如：`"chater"`在第4位前插入`"rac"`，得到`"character"`：

```cpp
#include <iostream>
#include <string>

int main() {
    std::string s = "chater";
    s.insert(3, "rac"); // 0基索引3：教材第4位之前插入。
    std::cout << s << '\n'; // character。

    s.erase(3, 3);       // 从0基索引3起删除3个字符。
    std::cout << s << '\n'; // chater。
}
```

对于课件的 `StrDelete(S,pos,len)`，从第pos位起删除len个字符。实践中需验证 `len>=0`、`pos>=1`、删除区间不越过串末尾。

> [!tip] 直接记住位置转换
> 教材第 `pos` 位 ⇔ C++的索引 `pos-1`。当调用 `std::string::erase(pos-1, len)` / `insert(pos-1, text)` / `substr(pos-1,len)` 时，特别检查 `pos` 是否合法。

### 2.7 替换 `Replace`：为什么强调“不重叠”？

用 `Replace(S,T,V)` 把主串S中与T相同的**不重叠**片段替换为V。通常从原串左到右扫描，每替换一处就**跳过该次匹配的全部字符**。

例1：`S="121121"`、`T="121"`、`V="3"`，结果 `"33"`。

例2：`S="12121"`、`T="121"`、`V="3"`，结果 `"321"`。原来第3位开始的另一个 `"121"` 与第1位开始的匹配**重叠**，因此不能将两个都替换。

例3：`S="aaaaa"`、`T="aa"`、`V="X"`，左到右进行不重叠替换得到 `"XXa"`。

**标准C++实现：**

```cpp
#include <iostream>
#include <stdexcept>
#include <string>

std::string replaceAll(const std::string& s,
                       const std::string& pattern,
                       const std::string& replacement) {
    if (pattern.empty()) throw std::invalid_argument("模式串不能为空");
    std::string result;
    std::size_t start = 0;

    while (start < s.size()) {
        std::size_t found = s.find(pattern, start);  // 在尚未处理的原串中寻找。
        if (found == std::string::npos) break;      // 没有下一处匹配。
        result.append(s, start, found - start);      // 保留匹配前的原文。
        result += replacement;                       // 写入替换后的文本。
        start = found + pattern.size();              // 跳过整个原匹配，杜绝重叠。
    }
    result.append(s, start, s.size() - start);        // 追加最后一段原文。
    return result;
}

int main() {
    std::cout << replaceAll("12121", "121", "3") << '\n'; // 321。
    std::cout << replaceAll("121121", "121", "3") << '\n'; // 33。
    std::cout << replaceAll("aaaaa", "aa", "X") << '\n';   // XXa。
}
```

> [!warning] 替换后的内容是否继续参与查找？
> 上面实现始终从**原串**寻找下一处，替换文本不会再次参与匹配。否则可能出现重复替换、规则冲突，甚至在 `"a"→"aa"` 时不断增长。采用原串顺序不重叠替换，是本章讨论的明确语义。

### 2.8 用最小操作子集构造 `Index`

从操作组合的角度看，`Index(S,T,pos)`可以只用**求串长 + 求子串 + 串比较**来实现：把主串每个可能位置上、长度与T相同的子串取出来，再判断是否相等。

```cpp
#include <iostream>
#include <string>

int indexBySubstring(const std::string& s, const std::string& t, int pos) {
    if (t.empty() || pos < 1 || pos > static_cast<int>(s.size())) return 0;
    int n = static_cast<int>(s.size());             // 主串长度。
    int m = static_cast<int>(t.size());             // 模式串长度。
    for (int i = pos; i <= n - m + 1; ++i) {     // 每次测试一个合法起点。
        std::string sub = s.substr(i - 1, m);     // 取出m个连续字符。
        if (sub.compare(t) == 0) return i;       // 两串相等，返回1基位置。
    }
    return 0;                                      // 遍历所有起点仍未找到。
}

int main() {
    std::cout << indexBySubstring("abcabc", "bca", 1) << '\n'; // 2。
}
```

这种写法容易理解，但每次 `substr` 都可能复制若干字符，在长文本匹配时不如不生成子串的指针式算法合适。这正引出本章的BF与KMP。

---

## 三、串的存储结构：定长顺序存储

### 3.1 三类存储结构先建立整体概念

| 存储结构 | 核心方式 | 长度限制 | 适用特点 |
| --- | --- | --- | --- |
| **定长顺序存储** | 固定容量的连续数组 | 存在固定上界 | 访问方便、实现直接，可能截断 |
| **堆分配存储** | 运行时动态申请连续存储区 | 可按需要重新分配 | 容量灵活、复制和移动要管理内存 |
| **块链存储** | 链表的每个结点存一个或多个字符 | 可逐块增长 | 拼接等结点操作可方便，但指针和空位有额外开销 |

注意，三者都可以表达**同一个串逻辑值**；差异来自内存组织方式，不是字符串本身的含义变化。

### 3.2 非紧缩与紧缩存储

以 `"programming"`（11个字符）为例：

- **非紧缩格式**：一个存储单元只放一个字符。
- **紧缩格式**：一个较大的存储单元内部放多个字符，例如每个单元放4个字符。

| 存储单元 | 非紧缩示意 | 紧缩示意（每单元4字符） |
| --- | --- | --- |
| 第1单元 | `p` | `p r o g` |
| 第2单元 | `r` | `r a m m` |
| 第3单元 | `o` | `i n g [空位]` |
| …… | 继续逐字符存储 | — |

这里的“一个存储单元”是教材为比较格式而使用的抽象单位，不应错误理解为现代C++的 `char` 必然占用一个完整CPU机器字。实际C/C++里 `char` 使用一个字节大小的存储单位（`sizeof(char)==1`）；CPU字长可能更大。

### 3.3 课件的定长串表示方法

课件采取：**下标0的单元放长度，下标1至255放字符内容**。

例如串 `"student"`：

| 单元下标 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 存储值 | 7 | s | t | u | d | e | n | t |

这是一种**长度前置**的存储表示，不同于C语言以 `\0` 结束的字符串。

> [!important] 两种长度记录方式必须区分
> - **课件定长串**：`S[0]`存长度，`S[1]`是第1个字符。
> - **传统C字符串**：`s[0]`是第1个字符；末尾额外有 `\0`；`strlen(s)`从开头逐个寻找终止符。
> - **C++ `std::string`**：长度由对象管理，`s[0]`是第1个字符，`s.size()`可快速取得长度。

### 3.4 完整可运行的定长串：赋值、求长、输出

这里用 `std::array<unsigned char, 256>` 直接对应课件256个存储单元，不需要引入 `typedef` 或没有实际意义的类型别名。

```cpp
#include <array>
#include <iostream>
#include <string>

struct FixedString {
    std::array<unsigned char, 256> data{}; // 下标0存长度，1~255放字符。
};

bool assign(FixedString& s, const std::string& text) {
    std::size_t n = text.size() < 255 ? text.size() : 255; // 超长只保留前255个。
    s.data[0] = static_cast<unsigned char>(n);             // 写入实际保存的长度。
    for (std::size_t i = 0; i < n; ++i) {
        s.data[i + 1] = static_cast<unsigned char>(text[i]); // 从data[1]开始存字符。
    }
    return text.size() <= 255;                            // true表示没有截断。
}

int main() {
    FixedString s;
    bool complete = assign(s, "student");
    std::cout << static_cast<int>(s.data[0]) << '\n'; // 7。
    std::cout << static_cast<char>(s.data[1]) << '\n'; // s。
    std::cout << complete << '\n';                     // 1：数据完整。
}
```

> [!note] 为什么使用 `unsigned char` 存长度？
> 在常见的8位字节平台上，单个 `unsigned char` 能表达0～255，正好覆盖课件给出的最大串长255。如果改成有符号的 `char`，存储大于其表示上限的长度可能出现错误。该方案是对课件模型的**具体实现**，不是说所有系统的字符编码都只需一个字节。

### 3.5 定长串的拼接及其截断

设最大长度为255，则结果可能出现三种情况：

1. `S1长+S2长≤255`：两串完整拼接。
2. `S1长<255`，但两串合计超长：保留全部S1，再保留**S2的前面一部分**。
3. `S1长=255`：S1已经占满，S2全部无法写入。

> [!example] 小容量示例更容易理解
> 假设上限不是255而是 **8**：
>
> - `"abc" + "def"` → `"abcdef"`，完整。
> - `"abcdef" + "XYZ"` → `"abcdefXY"`，把S2尾部的`Z`截断。
> - `"abcdefgh" + "XYZ"` → `"abcdefgh"`，S2无法加入。

**核心代码（代码段依赖上一节的`FixedString`定义）：**

```cpp
// 将两个长度前置的定长串拼接，返回是否未截断。
bool concat(FixedString& out, const FixedString& a, const FixedString& b) {
    FixedString result;            // 使用临时结果，避免out与输入别名带来覆盖。
    int used = 0;

    for (int i = 1; i <= a.data[0] && used < 255; ++i) {
        result.data[++used] = a.data[i]; // 先复制a。
    }
    for (int i = 1; i <= b.data[0] && used < 255; ++i) {
        result.data[++used] = b.data[i]; // 有空位时再复制b。
    }
    result.data[0] = static_cast<unsigned char>(used); // 更新实际长度。
    bool complete = static_cast<int>(a.data[0]) + static_cast<int>(b.data[0]) <= 255;
    out = result;
    return complete;
}
```

**解释**：`used`既是当前已复制字符数，也是下一次写入位置的基础。`++used`后才访问数组，因此首字符在下标1。判断截断时，两段长度先转成`int`避免将小范围字符值当成最终串长保存。

### 3.6 定长串求子串：校验 + 按序复制

```cpp
#include <stdexcept>

// 此函数代码段与本节的FixedString定义配套。
FixedString substring(const FixedString& s, int pos, int len) {
    if (pos < 1 || pos > s.data[0] || len < 0 ||
        len > static_cast<int>(s.data[0]) - pos + 1) {
        throw std::out_of_range("位置或长度不合法");
    }

    FixedString result;
    result.data[0] = static_cast<unsigned char>(len); // 记录子串的长度。
    for (int i = 0; i < len; ++i) {
        result.data[i + 1] = s.data[pos + i];         // 将指定范围搬到新串。
    }
    return result;
}
```

例如 `"student"` 的第3位起长度4：复制的是 `u d e n`，新串第0位记录长度4。

### 3.7 定长存储的运算代价

| 操作 | 主要工作 | 时间量级 |
| --- | --- | --- |
| 查串长 | 读取第0个长度单元 | $O(1)$ |
| 读取指定字符 | 按下标访问 | $O(1)$ |
| 复制或拼接 | 逐字符复制 | $O(n)$（与所复制的字符数量有关） |
| 求长度为$k$的子串 | 复制$k$个字符 | $O(k)$ |
| 指定位置插入 | 给字符腾位置，移动后缀 | 最坏$O(n)$ |
| 删除指定区间 | 将后面的字符向前移动 | 最坏$O(n)$ |

> [!warning] 定长串最大的局限是**截断和容量溢出**
> “截断”是本章课件为了演示定长存储而使用的一种策略，不等于任何实际程序都应默默丢掉输入。真实业务中更安全的设计往往是返回错误、拒绝写入或改用动态存储，以免数据无声丢失。

---

## 四、串的堆分配存储：动态申请连续空间

### 4.1 为什么要使用堆分配？

定长串的容量在设计时固定；运行时生成的字符串可能无法预知长度，例如用户输入、文件内容、拼接结果。堆分配存储在运行过程中**按照所需字符数申请一段连续空间**，其串值仍然连续存放，只是空间大小可以调整。

教材采用的结构思想是：

```cpp
struct HeapString {
    char* ch = nullptr;       // 指向动态申请的字符序列。
    std::size_t length = 0;   // 实际字符个数。

    HeapString() = default;                               // 允许正常建立空串对象。
    HeapString(const HeapString&) = delete;             // 禁止危险的浅复制。
    HeapString& operator=(const HeapString&) = delete;
    ~HeapString() { delete[] ch; }                      // 对象销毁时归还内存。
};
```

这里的 `ch` 和 `length` 是**两种不同的信息**：前者告诉程序数据放在哪，后者告诉程序有多少个字符。单靠指针不能知道串长。

### 4.2 内存分配、复制、释放的过程

以 `"data"` 为例：

1. 申请4个字符的空间；
2. 将`d a t a`复制到这4个单元；
3. `ch`指向首地址、`length=4`；
4. 需要更新时，通常申请新空间、复制数据、释放旧空间。

C语言教材使用 `malloc`、`realloc`、`free`；C++也允许相应C库函数，但本章C++实现使用配对的 `new[]`/`delete[]`，并用 `std::unique_ptr` 暂时管理新申请的内存，避免中途异常导致泄漏。**`new[]`必须用`delete[]`释放，不能和`free`混用。**

下面是一个独立的最小示例：

```cpp
#include <iostream>

int main() {
    char* p = new char[4]; // 为4个字符动态分配连续空间。
    p[0] = 'd';           // 将字符写入第0个位置。
    p[1] = 'a';
    p[2] = 't';
    p[3] = 'a';

    std::cout.write(p, 4); // 明确写出4个字符，不要求末尾有'\0'。
    std::cout << '\n';
    delete[] p;            // 归还整段数组空间。
    p = nullptr;           // 防止留下悬空指针。
}
```

> [!warning] `char*` 不必然是C字符串
> 上例没有为 `\0` 分配第5个单元，所以不能调用 `std::cout << p` 或 `std::strlen(p)` 并指望它正确终止。教材的`HString`是**指针 + 明确长度**，并不要求字符数据一定以`\0`结尾。若需要C字符串接口，须额外分配终止符空间并正确写入。

### 4.3 堆分配下的拼接

新串长度为

$$
\operatorname{len}(T)=\operatorname{len}(S_1)+\operatorname{len}(S_2).
$$

依次将两串复制进新空间，再让目标串指向它。和定长串相比，不需要因为某个预先规定的最大串长而进行截断；仍然可能受到可用内存与整数范围限制。

**关键实现片段（依赖本章 `HeapString`、`<memory>`、`<cstddef>`）：**

```cpp
void concat(HeapString& out, const HeapString& first, const HeapString& second) {
    std::size_t newLength = first.length + second.length; // 新串的真实长度。
    std::unique_ptr<char[]> temp(newLength == 0 ? nullptr : new char[newLength]);

    for (std::size_t i = 0; i < first.length; ++i) {
        temp[i] = first.ch[i];              // 前半段写入first的字符。
    }
    for (std::size_t i = 0; i < second.length; ++i) {
        temp[first.length + i] = second.ch[i]; // 后半段写入second。
    }

    delete[] out.ch;                        // 释放目标串过去的存储空间。
    out.ch = temp.release();                // 接管已构造好的新存储空间。
    out.length = newLength;                 // 同步更新串长。
}
```

> [!note] 理解 `std::unique_ptr<char[]>` 与 `release()`
> `temp`先保管新申请的数组；若分配或其他步骤发生异常，它会负责释放。`release()`只移交指针的所有权，而不释放内存，因此随后由 `out`负责在将来释放。配套完整程序显式禁止`HeapString`的默认浅复制，避免两个对象同时拥有同一块空间而重复释放。

### 4.4 堆分配下的插入：前段 + 插入串 + 后段

例：原串 `S="ABCDE"`，在第3位之前插入 `"12"`。

- 前段：`"AB"`。
- 插入串：`"12"`。
- 后段：`"CDE"`。
- 结果：`"AB12CDE"`，新长度为7。

采用新缓冲区的实现尤其容易理解：

```cpp
// 依赖本章的HeapString，以及<memory>、<string>、<stdexcept>。
void insert(HeapString& s, int pos, const std::string& text) {
    if (pos < 1 || static_cast<std::size_t>(pos) > s.length + 1) {
        throw std::out_of_range("插入位置不合法");
    }

    std::size_t left = static_cast<std::size_t>(pos - 1); // 原串前段长度。
    std::size_t newLength = s.length + text.size();      // 新串的目标长度。
    std::unique_ptr<char[]> temp(newLength == 0 ? nullptr : new char[newLength]);

    for (std::size_t i = 0; i < left; ++i) temp[i] = s.ch[i];
    for (std::size_t i = 0; i < text.size(); ++i) temp[left + i] = text[i];
    for (std::size_t i = left; i < s.length; ++i) {
        temp[i + text.size()] = s.ch[i];                // 原后段整体向后移动。
    }

    delete[] s.ch;
    s.ch = temp.release();
    s.length = newLength;
}
```

> [!tip] 用“三区域复制”记忆插入算法
> **原串左部不动 → 插入文本放中间 → 原串右部整体右移**。若在原缓冲区直接移动字符，为防止数据覆盖，通常应**从后往前**移动后缀；重新分配独立新缓冲区则可以按上述顺序复制。

### 4.5 为什么堆分配不一定所有操作都快？

“堆分配”解决的是**容量灵活**，并不保证插入、删除都是$O(1)$。由于有效字符要求连续，若在串中间插入或删除，仍可能需要移动后续字符。并且重新分配和复制也有开销。

| 需求 | 定长串 | 堆分配串 |
| --- | --- | --- |
| 不改变长度地读取字符 | 直接访问 | 直接访问 |
| 动态变长 | 可能被容量限制 | 可重新分配 |
| 拼接较长结果 | 可能截断 | 可申请足够空间 |
| 中间插入 | 需要移动后缀 | 通常同样需要复制/移动后缀 |
| 实现复杂性 | 较低 | 要管理内存与对象所有权 |

---

## 五、串的块链存储

### 5.1 块链存储的核心思想

可以将串分散到多个链表结点。每个结点不是必须只存一个字符，还可以存固定数量的字符，这个数量称为**结点大小（块大小）**。

以串 `"ABCDEFGHI"`、每块放4个字符为例：

```text
head
 ↓
[A B C D | next] → [E F G H | next] → [I # # # | null]
                                          ↑
                                         tail
```

这个 `text` 块是**存储布局示意图**，不是程序或伪代码。最后一个块的`#`为填充符，不属于串的有效字符；有效长度仍为9。

> [!example] 块大小变化会发生什么？
> 同一个9字符的串：
>
> - 每块1个字符：需要9个结点；没有尾部无效字符位置，但要存很多指针。
> - 每块3个字符：需要3个结点，正好填满。
> - 每块4个字符：需要3个结点，最后一块有3个空位。
> - 每块10个字符：只需1个结点，却有1个未填满位置。

### 5.2 结点、头指针、尾指针与串长

```cpp
#include <cstddef>

struct Chunk {
    static constexpr std::size_t SIZE = 4; // 单个结点的字符容量。
    char ch[SIZE]{'#', '#', '#', '#'}; // 每块容纳4个字符。
    Chunk* next = nullptr;        // 下一块的地址。
};

struct ChunkString {
    Chunk* head = nullptr;        // 链表起始结点。
    Chunk* tail = nullptr;        // 最后一个结点，便于追加。
    std::size_t length = 0;      // 有效字符个数。
};
```

**重要的是三者角色不同**：`head`为遍历起点，`tail`为快速找到最后一块，`length`帮助区分真实字符与填充内容。

### 5.3 追加字符时怎样申请新块？

- 如果目前还没有结点或最后一块已满，分配一个新结点并接到尾部。
- 将新字符写入当前尾结点中下一个空槽位。
- 更新串长。

**以下为完整工程中成员函数的实际代码段：**

```cpp
void append(char c) {
    if (length % Chunk::SIZE == 0) {             // 当前字符数恰为块大小的整数倍。
        Chunk* node = new Chunk;                 // 新建一块。
        if (tail != nullptr) tail->next = node; // 存在旧尾结点，则连接新块。
        else head = node;                       // 这是第一个结点。
        tail = node;                            // 新块成为尾结点。
    }
    tail->ch[length % Chunk::SIZE] = c;          // 写入尾块的对应槽位。
    ++length;                                   // 真实长度增加1。
}
```

这段代码依赖配套源码中 `Chunk::SIZE`、`head`、`tail`、`length` 所在的类定义；它本身是**合法的C++成员函数体**，并非伪代码。完整可直接编译的程序见配套 `04_chunk_string.cpp`。

### 5.4 存储密度与结点大小的权衡

课件给出的存储密度：

$$
\boxed{\text{存储密度}=\frac{\text{存放有效数据实际占用的存储量}}{\text{总分配的存储量}}}
$$

这个比值反映**有效数据占比**。讨论块链存储时应同时考虑：块内未使用的位置、指针字段及实现需要的管理开销。

> [!example] 理解相同串长的不同存储开销
> 假设一个指针占8字节、每字符占1字节（仅用于示例，不代表所有机器）：
>
> - 每块1字符：9个结点，单结点1+8字节，合计约81字节（不计内存分配器开销）。
> - 每块4字符：3个结点，单结点4+8字节，合计约36字节。
> - 每块16字符：1个结点，单结点16+8字节，合计约24字节，但有效字符只有9个。
>
> 实际结构体还可能因内存对齐增加占用，以上只是说明“块越大不一定总是越好”的计算模型。

块链结构对部分拼接、逐块增长操作有优势，但其指针管理、按位置访问、碎片与空间开销，使它并不普遍优于连续存储。

---
## 六、串的模式匹配：从问题定义开始

### 6.1 什么是模式匹配？

在主串 `S` 中寻找与给定串 `T` 值完全相同的连续字符片段，称为**串的模式匹配**（Pattern Matching）。其中：

- `S`：主串，也叫文本串。
- `T`：模式串，需要在主串中寻找。
- `pos`：开始查找的主串位置。
- **成功**：返回第一次匹配的起始位置（本章按1基编号）。
- **失败**：返回0。

例如：

`S="abcabcabc"`，`T="cab"`，则首次匹配开始于第3位：

```text
主串位置  1 2 3 4 5 6 7 8 9
主串 S    a b c a b c a b c
模式 T        c a b
             ↑
           起始位置3
```

### 6.2 最直接的思路：每个位置都试一次

设主串长为$n$、模式串长为$m$，长度$m$的模式串能放进主串的最后一个起点是：

$$
\boxed{n-m+1}
$$

比如主串长度10、模式串长度4，合法起点只有1～7，**不能**从第8位开始测试4个字符，否则会越界。

> [!example] 起点范围的几种边界
> - $n=10,m=4$：最多测试起点1～7。
> - $n=5,m=5$：只有起点1。
> - $n=3,m=5$：连1个完整模式都放不下，直接失败。
> - $m=1$：任何有效主串字符位置都可能是匹配起点。

---

## 七、BF算法（朴素模式匹配）

### 7.1 BF算法的基本思想

**BF（Brute Force）算法**对每个可能的起始位置，依次比较模式串的各个字符：

1. 从主串第 `pos` 位开始，用模式串第1个字符比较。
2. 若相等，比较后一对字符。
3. 一旦失配，模式串回到第1个字符，主串的**本趟匹配起点向后移动一位**。
4. 重复，直到完全匹配或主串已经没有足够字符可匹配。

**BF最大的特征是：失配时可能回退主串比较指针。**

### 7.2 逐趟匹配示例：看懂“回退”

设：

`S="ababcabcacbab"`，`T="abcac"`。

| 尝试起点 | 逐字符比较情况 | 结果 |
| ---: | --- | --- |
| 1 | `ab`匹配，第三位主串`a`与模式`c`不等 | 失配 |
| 2 | 主串`b`与模式首字符`a`不等 | 失配 |
| 3 | `abca`匹配，第5个模式字符`c`与主串`b`不等 | 失配 |
| 4 | 主串`b`不等于`a` | 失配 |
| 5 | 主串`c`不等于`a` | 失配 |
| **6** | `a b c a c`五个字符全部相等 | **成功，返回6** |

> [!note] 为什么起点3的匹配很浪费？
> 从第3位开始时，已经验证 `abca` 相同，但因为第5个字符失配，BF下一轮又要从新的候选起点检查。已经比较过的信息没被系统地保留下来。KMP正是针对这件事进行优化。

### 7.3 BF中的两个指针与回退公式

采用课件的1基编号：

- `i`：当前待比较的主串字符位置。
- `j`：当前待比较的模式串字符位置。

匹配成功一对字符时：`++i; ++j;`。

失配后：

$$
\boxed{i=i-j+2,\qquad j=1}
$$

**公式为什么是 `i-j+2`？**

假设本趟起点为$a$，已经匹配了$j-1$个字符，则失配时主串指针为

$$
i=a+j-1.
$$

下一趟应从$a+1$开始，因此：

$$
a+1=i-j+2.
$$

> [!example] 代入数字验证回退
> 假设从主串第3位起匹配，前4个字符相等，到模式第5个字符失配，则$i=7,j=5$。
>
> $$i'=7-5+2=4,\qquad j'=1.$$
>
> 即下一次从主串第4位重新尝试，而不是从失配处第7位开始。这就是**主串指针回溯**。

### 7.4 BF的完整标准C++实现

```cpp
#include <iostream>
#include <string>

// 1基位置；模式串非空；若失败返回0。
int indexBF(const std::string& s, const std::string& p, int pos) {
    int n = static_cast<int>(s.size()); // 主串长度。
    int m = static_cast<int>(p.size()); // 模式串长度。
    if (m == 0 || pos < 1 || pos > n) return 0;

    int i = pos; // 主串当前待比较字符的1基位置。
    int j = 1;   // 模式串当前待比较字符的1基位置。

    while (i <= n && j <= m) {
        if (s[i - 1] == p[j - 1]) { // C++数组索引必须减1。
            ++i;                   // 当前两个字符相等，向后比较。
            ++j;
        } else {
            i = i - j + 2;        // 恢复本轮起点，再把起点后移1位。
            j = 1;                // 模式串重新从首字符开始比较。
        }
    }

    if (j > m) return i - m;      // 模式全部匹配，算出起始位置。
    return 0;                     // 主串耗尽仍未完成匹配。
}

int main() {
    std::cout << indexBF("ababcabcacbab", "abcac", 1) << '\n'; // 6。
    std::cout << indexBF("hello", "abc", 1) << '\n';           // 0。
    std::cout << indexBF("aaaa", "aa", 2) << '\n';            // 2。
}
```

### 7.5 BF的时间与空间复杂度

设主串长$n$，模式串长$m$：

- **最好情况**：从第一个候选位置起直接匹配成功，比较$m$次，为$O(m)$；如果多数尝试在首字符便失配，扫描接近$O(n)$。
- **最坏情况**：每个候选起点都比较了很多字符才失配，时间复杂度为$O(nm)$。
- **额外空间**：只使用少量下标变量，为$O(1)$。

> [!example] BF的典型最坏输入
> `S="aaaaaaaaaaaaab"`，`T="aaaab"`。
>
> 对于许多候选起点，BF都要连续比较几个`a`，直到最后一位才发现不匹配。两个串的字符重复性越高，这种重复比较越明显。

> [!warning] 不要把“BF是$O(nm)$”解释成任何情况下都要做$n\times m$次比较
> $O(nm)$描述的是最坏情况的渐近上界。实际输入可能在第一轮就匹配成功，也可能每次比较首字符就失败，运行时间会小得多。

---

## 八、首尾匹配算法

### 8.1 核心思想

课件介绍的**首尾匹配**是一种改变比较顺序的方法：对当前候选起点先检查模式串**首字符**，再检查**尾字符**，最后检查中间字符。

若首、尾任何一个不相等，就直接尝试下一个起点，避免无意义地逐个比较中间字符。

比如模式串为 `"abcde"`，候选片段为 `"abcdf"`：BF会依次比较`a、b、c、d`，最后才发现`e≠f`；首尾匹配在检查首字符`a`成功之后，立刻检查`e`和`f`，就能更早失配。

### 8.2 首尾匹配代码

```cpp
#include <iostream>
#include <string>

int indexFirstLast(const std::string& s, const std::string& p, int pos) {
    int n = static_cast<int>(s.size()); // 主串长度。
    int m = static_cast<int>(p.size()); // 模式串长度。
    if (m == 0 || pos < 1 || pos > n) return 0;

    for (int i = pos; i <= n - m + 1; ++i) {
        if (s[i - 1] != p[0]) continue;          // 第一步：检查首字符。
        if (m == 1) return i;                     // 单字符模式不需要尾部或中间比较。
        if (s[i + m - 2] != p[m - 1]) continue;  // 第二步：检查尾字符。

        int j = 1;                                // 模式中间部分从0基索引1开始。
        while (j < m - 1 && s[i - 1 + j] == p[j]) {
            ++j;                                 // 第三步：逐个匹配中间字符。
        }
        if (j == m - 1) return i;                 // 中间字符全部相等，匹配成功。
    }
    return 0;
}

int main() {
    std::cout << indexFirstLast("ababcabcacbab", "abcac", 1) << '\n'; // 6。
    std::cout << indexFirstLast("x", "x", 1) << '\n';               // 1。
    std::cout << indexFirstLast("xyz", "yz", 1) << '\n';           // 2。
}
```

### 8.3 首尾匹配的特点与限制

- 常见情况下可能比BF少比较一些中间字符。
- 它依然可能对每一个起点都进行接近$m$次的比较，**最坏时间复杂度仍是$O(nm)$**。
- 它并没有利用模式串内部的**公共前后缀结构**，因此不是KMP的等价替代品。

> [!tip] 三种匹配的第一印象
> **BF：每轮从头逐个比。首尾匹配：每轮先比头和尾。KMP：失配时复用已匹配的信息，主串指针不回退。**

---

## 九、KMP：为什么失配时主串指针可以不回退？

### 9.1 KMP的改进目标

KMP由Knuth、Morris、Pratt共同提出，其核心是：

> [!important] KMP最重要的一句话
> **主串当前位置不回退；当模式字符失配时，利用模式串自身的相等前后缀关系，决定模式串指针应该回退到哪里。**

因此，已比较成功的主串字符信息不需要像BF那样从不同候选起点重新验证一遍。

KMP的理论时间复杂度为$O(n+m)$：构造模式串的辅助表$O(m)$，完成匹配$O(n)$。

### 9.2 首先理解“前缀”与“后缀”

对于字符串 `"ababa"`：

- 真前缀（不取全串）：`"a"`、`"ab"`、`"aba"`、`"abab"`。
- 真后缀（不取全串）：`"a"`、`"ba"`、`"aba"`、`"baba"`。
- 既是前缀又是后缀的非空串：`"a"`、`"aba"`。
- **最长相等真前后缀**为 `"aba"`，长度是3。

这个“最长相等前后缀长度”常称为**最长边界长度（border）**；注意只比较**同一个串的开头和结尾**，而不是任意两段相同子串。

| 串 | 最长相等真前后缀 | 长度 |
| --- | --- | ---: |
| `"a"` | 空串 | 0 |
| `"ab"` | 空串 | 0 |
| `"aba"` | `"a"` | 1 |
| `"abab"` | `"ab"` | 2 |
| `"ababa"` | `"aba"` | 3 |
| `"aaaa"` | `"aaa"` | 3 |
| `"abcab"` | `"ab"` | 2 |
| `"abcd"` | 空串 | 0 |

> [!warning] 最重要的两个“不能”
> 1. 最长相等前后缀**不能取整个串本身**；否则毫无意义。
> 2. `"abcab"`的`"ab"`是有效公共前后缀，但中间某个`"bc"`出现过并不代表它是前缀或后缀。

### 9.3 KMP失配时到底知道了什么？

按课件1基编号，设模式串为$P$，在比较$S[i]$与$P[j]$时发生失配。

因为第$j$个模式字符才失配，已经能够确定：

$$
S[i-j+1\,\ldots\,i-1]=P[1\,\ldots\,j-1].
$$

也就是说，主串里**紧挨着当前失配位置的$j-1$个字符**，已经与模式开头$j-1$个字符完全相等。

如果模式的这段已匹配部分中存在长度$k-1$的相等前后缀：

$$
P[1\,\ldots\,k-1]=P[j-k+1\,\ldots\,j-1],
$$

则失配时可以直接把模式的第$k$位拿来与$S[i]$重新比较，**主串指针$i$保持不变**。

这就是课件 `next[j]=k` 的逻辑含义。

> [!example] 直观示例：模式 `"ababac"`
> 假如已经匹配成功 `"ababa"`，下一位期望字符是`c`，但主串当前位置不是`c`。
>
> 已匹配部分`"ababa"`最长相等真前后缀为`"aba"`，长度3，因此可保留这3个字符的匹配结论，无需从模式首字符重新比较。下一次应当尝试模式第4位，故这里 `next[6]=4`。
>
> 这里“保留匹配结论”不是凭空忽略主串字符，而是利用了前后缀重合部分必然已经相等这一事实。

### 9.4 KMP与BF在失配时的根本区别

| 失配后的处理 | BF | KMP |
| --- | --- | --- |
| 主串当前比较位置 | 可能回退 | **保持不变**（除`j=0`的特殊前进） |
| 模式串比较位置 | 重设为1 | 调整为`next[j]` |
| 是否重用已成功比较的信息 | 基本没有 | 是 |
| 最坏匹配复杂度 | $O(nm)$ | $O(n)$（不含预处理） |
| 是否需要模式辅助表 | 否 | 是 |

---

## 十、`next`函数：定义、手工计算、代码实现

### 10.1 首先明确：本章采用教材的哪一种`next`？

**非常重要**：不同教材、网络文章有多种`next`、`pi`、`lps`的编号与定义，得到的数字**可能不同**，但都能实现相应的KMP。

本章严格采用课件中的 **1基、`next[1]=0`** 版本。

> [!important] 教材版 `next[j]` 的定义
> - `next[1]=0`。
> - 当$j\ge2$时，只看模式中 **第1位到第$j-1$位** 这一段已经匹配的字符。
> - 找出这段字符最长的**相等真前后缀**，设其长度为$k$。
> - 则
>
> $$\boxed{next[j]=k+1\quad (j\ge2)}$$
>
> 其中$k$允许为0，因此无相等非空前后缀时`next[j]=1`。

**为什么不看第$j$个字符？** 因为第$j$个字符正是即将比较失败的字符，已经确定相等的只有前$j-1$个字符。

### 10.2 第一份最重要的完整手算例子：`abaabcac`

模式串为：

| 位置$j$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 字符 | a | b | a | a | b | c | a | c |
| **`next[j]`** | **0** | **1** | **1** | **2** | **2** | **3** | **1** | **2** |

逐位拆开：

| 计算位置$j$ | 只看前$j-1$个字符 | 最长相等真前后缀 | 长度$k$ | `next[j]` |
| ---: | --- | --- | ---: | ---: |
| 1 | 没有已匹配字符 | 特殊定义 | — | 0 |
| 2 | `a` | 无 | 0 | 1 |
| 3 | `ab` | 无 | 0 | 1 |
| 4 | `aba` | `a` | 1 | 2 |
| 5 | `abaa` | `a` | 1 | 2 |
| 6 | `abaab` | `ab` | 2 | 3 |
| 7 | `abaabc` | 无 | 0 | 1 |
| 8 | `abaabca` | `a` | 1 | 2 |

> [!tip] 考试手算最简单的流程
> **每个$j$都只看其左侧已经匹配的部分 → 找最长相等真前后缀 → 长度加1**。不要把整段模式串看成一个整体求前后缀，也不要把`next[j]`误认为“从主串头向后跳过多少字符”。

### 10.3 第二个手算例子：`abcabaa`

| 位置$j$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 字符 | a | b | c | a | b | a | a |
| **`next[j]`** | **0** | **1** | **1** | **1** | **2** | **3** | **2** |

重点关注第5～7位：

- `next[5]`只看`"abca"`，首尾都为`a`，最长长度1，因此值2。
- `next[6]`只看`"abcab"`，首尾相同的最长一段为`"ab"`，长度2，因此值3。
- `next[7]`只看`"abcaba"`，虽然之前出现过`"ab"`，但**串尾最后两位为`"ba"`**，并不等于开头`"ab"`；最长相等真前后缀仅为`"a"`，所以值2。

> [!warning] 手算第7位的典型错误
> 误把中间的`"ab"`当作后缀，填`next[7]=3`。注意后缀必须**紧贴这一段已匹配字符串的末尾**，不能跳过字符。

### 10.4 第三个例子：高度重复的 `aaaab`

| 位置$j$ | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| 字符 | a | a | a | a | b |
| **`next[j]`** | **0** | **1** | **2** | **3** | **4** |

原因是：已匹配的前缀可能分别是`"a"`、`"aa"`、`"aaa"`、`"aaaa"`，最长相等真前后缀长度依次为0、1、2、3。

这个例子也提示：**大量重复字符虽使普通`next`逐级回退，但也为`nextval`优化提供了空间。**

### 10.5 根据前一项推导后一项：递推思路

如果已经知道`next[j] = k`：

- 若$k=0$，说明当前没有可继续延用的位置，可以进入下一项的基础状态。
- 若$P[j]=P[k]$，原来的相等前后缀可同时延长一个字符，因此 `next[j+1]=k+1`。
- 若$P[j]\ne P[k]$，说明这段候选前后缀无法再延长，应令`k=next[k]`尝试更短的一组候选，再判断。

> [!example] `abcabaa`的末尾如何通过回退算出来？
> 已知 `next[6]=3`，希望求`next[7]`：
>
> - 检查`P[6]='a'`与`P[3]='c'`，不相等；
> - 回退`k=next[3]=1`；
> - 再检查`P[6]='a'`与`P[1]='a'`，相等；
> - 所以`next[7]=1+1=2`。
>
> **这里回退的是模式串中候选前后缀的长度状态，不是主串字符位置。**

### 10.6 `next`数组的实际C++计算代码

**下方是完整可运行程序**，遵循教材1基`next`定义。

```cpp
#include <iostream>
#include <string>
#include <vector>

std::vector<int> buildNext(const std::string& p) {
    int m = static_cast<int>(p.size());         // 模式串的字符个数。
    std::vector<int> next(m + 1, 0);           // 下标0不用，下标1~m有效。
    if (m == 0) return next;                    // 空模式的安全处理。

    int j = 1;                                  // 已知next[j]，准备计算next[j+1]。
    int k = 0;                                  // 当前候选匹配位置。

    while (j < m) {
        if (k == 0 || p[j - 1] == p[k - 1]) {  // 无可回退位置，或字符可延长匹配。
            ++j;                               // 前进到下一项。
            ++k;                               // 候选相等前后缀延长1位。
            next[j] = k;                       // 写入next的下一项。
        } else {
            k = next[k];                       // 不能延长，尝试更短前后缀。
        }
    }
    return next;
}

int main() {
    std::string pattern = "abaabcac";
    std::vector<int> next = buildNext(pattern);
    for (int j = 1; j <= static_cast<int>(pattern.size()); ++j) {
        std::cout << next[j] << ' ';            // 0 1 1 2 2 3 1 2
    }
    std::cout << '\n';
}
```

**值得反复理解的语句：**

`k = next[k]` 是利用短前缀的信息避免从头重算；它并不是随意向前跳。发生不等时，不修改`j`，而是调整`k`，直到找到能延长的候选状态。

### 10.7 `next` 与常见LPS表有什么区别？

网络教材可能使用从0开始的LPS（最长相等真前后缀长度）数组。例如模式 `"abaabcac"` 的0基LPS为：

| 0基位置 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 字符 | a | b | a | a | b | c | a | c |
| `LPS` | 0 | 0 | 1 | 1 | 2 | 0 | 1 | 0 |

这是针对**截至当前位置的前缀**计算的，跟教材“失配于第$j$位时，回退到哪一位”的`next`具有偏移关系。对于$j\ge2$：

$$
\boxed{next[j]=LPS[j-2]+1}
$$

这里的`LPS`按0基索引。两者**绝不能直接当成同一个数组使用**，否则很容易匹配错误或死循环。

---

## 十一、KMP的完整匹配过程与实现

### 11.1 匹配时的两条规则

主串当前字符位置`i`，模式当前字符位置`j`，两者均按课件1基计数。

**规则A：匹配相等，或者`j==0`。**

```cpp
++i; // 主串前进到下一字符。
++j; // 模式串也前进到下一字符。
```

**规则B：匹配不等且`j>0`。**

```cpp
j = next[j]; // 主串i不变，只调整模式串j。
```

> [!note] 为什么`j==0`要特殊处理？
> 这表示模式串第1位也匹配失败，已经没有更短的有效前缀可利用。此时只能让主串指针前进一位、模式指针复原为1，继续尝试。没有`j==0`条件会错误访问模式串的“第0个字符”或陷入循环。

### 11.2 完整的KMP跟踪例子

主串：`S="acabaabaabcacaabc"`。

模式：`P="abaabcac"`。

`next = [0,1,1,2,2,3,1,2]`（列出的8项对应位置1～8）。

| 阶段 | 比较/失配位置 | 下一步 | 意义 |
| --- | --- | --- | --- |
| 1 | `i=1,j=1`：`a=a` | `i=2,j=2` | 正常匹配 |
| 2 | `i=2,j=2`：`c≠b` | `j=next[2]=1` | 主串仍在第2位 |
| 3 | `i=2,j=1`：`c≠a` | `j=next[1]=0` | 无可用相等前后缀 |
| 4 | `j=0` | `i=3,j=1` | 主串才向后移动一位 |
| 5 | `i=3`开始，连续匹配 `abaab` | 到`i=8,j=6` | 已确认5个字符 |
| 6 | `i=8,j=6`：`a≠c` | `j=next[6]=3` | 复用已匹配前缀`ab`，主串不动 |
| 7 | `i=8,j=3`：`a=a` | `i=9,j=4` | 继续在当前位置匹配 |
| 8 | 后续依次匹配`a b c a c` | `i=14,j=9` | 模式8个字符全部匹配 |

最终位置为：

$$
\boxed{i-m=14-8=6}
$$

所以匹配结果为**第6位**。

> [!important] 读懂这张表最关键的一行
> 在`i=8,j=6`失配时，不是重新寻找主串第4位或第5位，而是立即令`j=3`，再用**同一个主串字符**`S[8]='a'`比较模式`P[3]='a'`。这就是KMP节省重复比较的直接体现。

### 11.3 完整可运行的KMP函数

```cpp
#include <iostream>
#include <string>
#include <vector>

std::vector<int> buildNext(const std::string& p) {
    std::vector<int> next(p.size() + 1, 0);
    int j = 1, k = 0;
    while (j < static_cast<int>(p.size())) {
        if (k == 0 || p[j - 1] == p[k - 1]) {
            ++j; ++k;
            next[j] = k;
        } else {
            k = next[k];
        }
    }
    return next;
}

int indexKMP(const std::string& s, const std::string& p, int pos) {
    int n = static_cast<int>(s.size()); // 主串长度。
    int m = static_cast<int>(p.size()); // 模式串长度。
    if (m == 0 || pos < 1 || pos > n) return 0;

    std::vector<int> next = buildNext(p); // 先完成模式的预处理。
    int i = pos;                          // 主串当前比较位置。
    int j = 1;                            // 模式当前比较位置。

    while (i <= n && j <= m) {
        if (j == 0 || s[i - 1] == p[j - 1]) {
            ++i;                          // 相等时主串向后走。
            ++j;                          // 模式同步向后走。
        } else {
            j = next[j];                  // 失配时只回退模式串指针。
        }
    }
    return j > m ? i - m : 0;            // 完全匹配则返回1基起点。
}

int main() {
    std::cout << indexKMP("acabaabaabcacaabc", "abaabcac", 1) << '\n'; // 6。
    std::cout << indexKMP("ababcabcacbab", "abcac", 1) << '\n';       // 6。
    std::cout << indexKMP("hello", "world", 1) << '\n';               // 0。
}
```

### 11.4 KMP正确性的直观理由

当已匹配部分出现失配时：

1. **已匹配部分全部是确定事实**，不必重新检查这些主串字符。
2. 任何能成为下一次有效匹配起点的候选，必须与模式头部形成合适的重叠，因此只能与某段**相等前后缀**有关。
3. `next[j]`优先选取能够保留最多已匹配字符的候选；若仍失配，再考虑更短的候选。
4. `j`不能再回退时，主串才前进。因此不会遗漏本该找到的匹配位置。

### 11.5 时间复杂度为什么能到$O(n+m)$？

构造`next`需要$O(m)$时间。真正匹配时：

- 主串指针`i`始终**单向增加**，最多跨过$n$个字符。
- 模式指针`j`虽可能回退，但回退次数受到此前前进次数的约束，总操作次数与扫描长度同阶。

因此匹配阶段$O(n)$，加上预处理：

$$
\boxed{T(n,m)=O(n+m),\qquad S(m)=O(m)}
$$

其中空间$O(m)$主要来自`next`辅助数组。

---

## 十二、改进`next`：`nextval`的意义与计算

### 12.1 为什么已有`next`还要改进？

假设模式串为`"aaaab"`，`next = [0,1,2,3,4]`。

当第4个模式字符`a`与主串当前字符失配时，如果根据`next`回退到第3位，仍然是`a`；再回退到第2位还是`a`，又回退到第1位仍是`a`。

**已知当前主串字符不等于`a`，却反复用同一个`a`去比较**，这几次比较显然没有意义。

`nextval`在预处理阶段把这样必然失败的回退步骤提前压缩，减少匹配时的冗余比较。

### 12.2 `nextval`的计算规则

仍然采用课件1基位置，`nextval[1]=0`。

令`k=next[j]`：

- 若`k=0`：`nextval[j]=0`。
- 若`P[j]≠P[k]`：`nextval[j]=next[j]`。
- 若`P[j]=P[k]`：`nextval[j]=nextval[k]`。

> [!important] 一眼判断`nextval`如何填
> 先有**完整正确的`next`表**。对每个位置$j$：
>
> **先看模式第$j$个字符，与模式第`next[j]`个字符是否相等；相等则沿`nextval[next[j]]`继续跳，不等则直接抄`next[j]`。**

### 12.3 手算例子一：`aaaab`

| $j$ | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| 字符 | a | a | a | a | b |
| `next` | 0 | 1 | 2 | 3 | 4 |
| **`nextval`** | **0** | **0** | **0** | **0** | **4** |

逐位分析：

- `j=2`：`P[2]=a=P[1]`，故`nextval[2]=nextval[1]=0`。
- `j=3`：`P[3]=a=P[2]`，故`nextval[3]=nextval[2]=0`。
- `j=4`：同理得0。
- `j=5`：`P[5]=b`与`P[next[5]]=P[4]=a`不等，所以`nextval[5]=next[5]=4`。

`nextval`从`0 1 2 3 4`变为`0 0 0 0 4`，跳过了失配后本来还要用相同`a`做的重复比较。

### 12.4 手算例子二：`abaabcac`

| 位置$j$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 字符 | a | b | a | a | b | c | a | c |
| `next[j]` | 0 | 1 | 1 | 2 | 2 | 3 | 1 | 2 |
| **`nextval[j]`** | **0** | **1** | **0** | **2** | **1** | **3** | **0** | **2** |

重点看这几个位置：

- `j=3`：`P[3]='a'`，`next[3]=1`，`P[1]='a'`，所以`nextval[3]=nextval[1]=0`。
- `j=4`：`P[4]='a'`，`next[4]=2`，`P[2]='b'`，两者不等，所以`nextval[4]=2`。
- `j=5`：`P[5]='b'`，`next[5]=2`，`P[2]='b'`，所以`nextval[5]=nextval[2]=1`。
- `j=7`：`P[7]='a'`，`next[7]=1`，`P[1]='a'`，所以`nextval[7]=0`。

> [!warning] `nextval`不能直接用“公共前后缀长度+1”求
> 那是求**普通next**的规则。`nextval`额外考虑**失配字符与回退目标字符是否相同**，因此它的值可能更小，甚至是0。

### 12.5 `nextval`的代码实现

```cpp
#include <iostream>
#include <string>
#include <vector>

std::vector<int> buildNext(const std::string& p) {
    std::vector<int> next(p.size() + 1, 0);
    int j = 1, k = 0;
    while (j < static_cast<int>(p.size())) {
        if (k == 0 || p[j - 1] == p[k - 1]) {
            ++j; ++k;
            next[j] = k;
        } else {
            k = next[k];
        }
    }
    return next;
}

std::vector<int> buildNextVal(const std::string& p,
                              const std::vector<int>& next) {
    int m = static_cast<int>(p.size());
    std::vector<int> nextval(m + 1, 0);           // 与课件一致：1基位置。

    for (int j = 2; j <= m; ++j) {
        int k = next[j];                          // 普通next的回退位置。
        if (k != 0 && p[j - 1] == p[k - 1]) {
            nextval[j] = nextval[k];              // 相同字符必然还会失配，继续跳。
        } else {
            nextval[j] = k;                       // 不同字符：保留普通next回退值。
        }
    }
    return nextval;
}

int main() {
    std::string p = "abaabcac";
    std::vector<int> next = buildNext(p);
    std::vector<int> nextval = buildNextVal(p, next);

    for (int j = 1; j <= static_cast<int>(p.size()); ++j) {
        std::cout << nextval[j] << ' ';            // 0 1 0 2 1 3 0 2
    }
    std::cout << '\n';
}
```

### 12.6 KMP使用`nextval`，主体循环是否需要改变？

**不需要。** KMP主体只要求“失配时得到一个合法的回退位置”，因而可以将普通`next`替换为`nextval`。本章配套的 `05_match_algorithms.cpp` 用统一的KMP函数分别接收两种表，并验证返回位置一致。

```cpp
// 已有 indexKMP(s, p, fallback, pos) 与两个构表函数的定义时：
std::string s = "acabaabaabcacaabc";
std::string p = "abaabcac";
std::vector<int> next = buildNext(p);
std::vector<int> nextval = buildNextVal(p, next);

int answer1 = indexKMP(s, p, next, 1);    // 使用普通next，结果6。
int answer2 = indexKMP(s, p, nextval, 1); // 使用改进nextval，结果仍为6。
```

注意，该代码块展示的是**合法的C++语句片段**，并在注释中明确了其依赖；完整独立运行环境包含在配套源码中。

### 12.7 `nextval`的优化究竟意味着什么？

普通KMP已经是$O(n+m)$。`nextval`减少的是**重复字符造成的无效比较次数**，不意味着时间复杂度从$O(n+m)$降低为某个更低的渐近量级。两者通常仍为线性复杂度。

---
## 十三、课件练习与完整解答

### 13.1 作业4.3：基本操作综合练习

题设：

```text
s = "I AM A STUDENT"
t = "GOOD"
q = "WORKER"
```

先将`s`按**1基位置**列出，防止错算空格：

| 位置 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 字符 | I | 空格 | A | M | 空格 | A | 空格 | S | T | U | D | E | N | T |

**各题答案（每个表达式默认按原始题设分别计算，互不修改其他表达式所用的原串）：**

| 表达式 | 结果 | 简要分析 |
| --- | --- | --- |
| `StrLength(s)` | **14** | 11个字母？实际14个字符，其中11个非空格字符、3个空格；按位置1～14数 |
| `StrLength(t)` | **4** | `GOOD`共4个字符 |
| `SubString(s,8,7)` | **`"STUDENT"`** | 从第8位起连续取7位 |
| `SubString(t,2,1)` | **`"O"`** | 第2位是字母O |
| `Index(s,"A")` | **3** | 从默认首位查找，首次A在第3位 |
| `Index(s,t)` | **0** | 主串不含`GOOD` |
| `Replace(s,"STUDENT",q)` | **`"I AM A WORKER"`** | 用`WORKER`替换`STUDENT` |
| `Concat(SubString(s,6,2),Concat(t,SubString(s,7,8)))` | **`"A GOOD STUDENT"`** | `"A " + ("GOOD" + " STUDENT")` |

> [!warning] 作业4.3最容易出错的是**空格**
> 题设原串`"I AM A STUDENT"`包含3个空格；`SubString(s,6,2)`实际上为 `"A "`（后面有空格），`SubString(s,7,8)`实际上为 `" STUDENT"`（前面有空格）。两段拼接后才得到自然的`"A GOOD STUDENT"`。

**对应的可运行C++代码：**

```cpp
#include <iostream>
#include <string>

int main() {
    const std::string s = "I AM A STUDENT"; // 保留原始主串供各小题使用。
    const std::string t = "GOOD";
    const std::string q = "WORKER";

    std::cout << s.size() << '\n';                  // 14。
    std::cout << t.size() << '\n';                  // 4。
    std::cout << s.substr(7, 7) << '\n';           // STUDENT，1基8对应0基7。
    std::cout << t.substr(1, 1) << '\n';           // O。
    std::cout << s.find("A") + 1 << '\n';          // 3，此处明确知道A存在。
    std::cout << (s.find(t) == std::string::npos) << '\n'; // 1：说明找不到。

    std::string modified = s;                       // 不修改原始s。
    std::size_t found = modified.find("STUDENT");
    if (found != std::string::npos) {
        modified.replace(found, 7, q);             // 从找到的位置替换7个字符。
    }
    std::cout << modified << '\n';                // I AM A WORKER。

    std::string expression = s.substr(5, 2) + t + s.substr(6, 8);
    std::cout << expression << '\n';              // A GOOD STUDENT。
}
```

注意 `std::string::find()` 未找到时返回 `std::string::npos`，不可直接把它加1转换为课件的失败返回0。上面只在已经知道`A`存在的那个表达式里使用了`find()+1`，其他情况必须先判断是否为`npos`。

### 13.2 作业4.7：三个模式的`next`、`nextval`

三个模式分别为：

- `s = "aaab"`；
- `t = "abcabaa"`；
- `u = "abcaabbabcabaacbacba"`。

**统一采用本章课件的1基定义，`next[1]=nextval[1]=0`。**

**（1）模式串`s="aaab"`**

| $j$ | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| 字符 | a | a | a | b |
| `next` | **0** | **1** | **2** | **3** |
| `nextval` | **0** | **0** | **0** | **3** |

`nextval[2]`、`nextval[3]`因为回退位置仍然是`a`而直接设成0；第4位字符`b`与回退位置的`a`不同，故保持3。

**（2）模式串`t="abcabaa"`**

| $j$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 字符 | a | b | c | a | b | a | a |
| `next` | **0** | **1** | **1** | **1** | **2** | **3** | **2** |
| `nextval` | **0** | **1** | **1** | **0** | **1** | **3** | **2** |

逐项检查`nextval`中的变化：

- `j=4`：`next[4]=1`，`P[4]=a=P[1]`，故改成`nextval[1]=0`。
- `j=5`：`next[5]=2`，`P[5]=b=P[2]`，故改成`nextval[2]=1`。
- `j=6`：`next[6]=3`，`P[6]=a≠P[3]=c`，所以仍为3。
- `j=7`：`next[7]=2`，`P[7]=a≠P[2]=b`，所以仍为2。

**（3）模式串`u="abcaabbabcabaacbacba"`**

这是较长的综合练习，推荐把字符位置、普通`next`和改进`nextval`分开记录后逐项核对。

| $j$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 字符 | a | b | c | a | a | b | b | a | b | c |
| `next` | 0 | 1 | 1 | 1 | 2 | 2 | 3 | 1 | 2 | 3 |
| `nextval` | 0 | 1 | 1 | 0 | 2 | 1 | 3 | 0 | 1 | 1 |

| $j$ | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 字符 | a | b | a | a | c | b | a | c | b | a |
| `next` | 4 | 5 | 3 | 2 | 2 | 1 | 1 | 2 | 1 | 1 |
| `nextval` | 0 | 5 | 3 | 2 | 2 | 1 | 0 | 2 | 1 | 0 |

合并写成完整数列，便于默写、查错：

`next`：`0,1,1,1,2,2,3,1,2,3,4,5,3,2,2,1,1,2,1,1`

`nextval`：`0,1,1,0,2,1,3,0,1,1,0,5,3,2,2,1,0,2,1,0`

> [!tip] 长模式的手算建议
> 先一口气标好20个位置，再计算所有`next`，最后只根据`next`与当前位置字符计算`nextval`。不要在没算完`next`时交叉计算，会特别容易把`P[j]`和`P[next[j]]`看错。

**可运行的批量验算程序：**配套源码 `05_match_algorithms.cpp` 的`showTable()`使用已验证的`buildNext()`与`buildNextVal()`，输出这三个模式的完整结果。手算训练时可先不看结果，最后再运行程序核对。

### 13.3 作业4.13：删除串s中所有与串t相同的子串

题目：**编写算法，从串s中删除所有与串t相同的子串。**

这道题要区分两种可能的处理语义：

1. **一次性原串、不重叠删除**：从原串左到右定位，删除原串中选定的互不重叠匹配，不再检查删除后拼接处产生的新匹配。这与第2.7节的“原串不重叠替换为空串”一致。
2. **反复删除直到找不到**：每删去一处就对**删除后的新串**重新定位，直到最终串中不存在模式串。这更符合“删除所有与t相同的子串”在最终结果层面的理解。

由于题目没有额外限定“一次性原串处理”，下面优先给出**反复删除直到不存在**的实现，并保留前一种操作供对比。

**算法流程：**在当前串中查找t → 找到就删去 → 对更新后的串继续查找 → 没找到就停止。

**完整可运行代码：**

```cpp
#include <iostream>
#include <stdexcept>
#include <string>

std::string deleteAll(std::string s, const std::string& t) {
    if (t.empty()) throw std::invalid_argument("待删除的串不能为空");

    std::size_t pos = s.find(t);                  // 查找当前串里第1次出现的位置。
    while (pos != std::string::npos) {           // 若仍存在完整模式串。
        s.erase(pos, t.size());                  // 从pos起删除t.size()个字符。
        pos = s.find(t);                         // 重新检查修改后的整串。
    }
    return s;                                    // 返回不再包含t的串。
}

int main() {
    std::cout << deleteAll("abcXXabcXX", "abc") << '\n'; // XXXX。
    std::cout << deleteAll("aaaaa", "aa") << '\n';       // a。
    std::cout << '"' << deleteAll("aababa", "aba") << '"' << '\n'; // ""。
}
```

> [!example] 为什么“重新寻找”有时很重要？
> 取 `s="aababa"`、`t="aba"`：
>
> - 初始串中从第2位发现`"aba"`，删掉后变为`"aba"`。
> - 这时**新串里仍含有`"aba"`**，若题目要求“最终完全没有t”，必须再删一次，得到空串。
> - 而一次性原串左到右不重叠删除只会删除原来第2～4位的匹配，留下`"aba"`。
>
> 因此两种语义在有重叠、拼接产生新匹配时会产生不同结果，不能混为一谈。

**复杂度**：这份教学实现可能多次从头执行`find`，同时`erase`又可能搬移后续字符，因此最坏时间可显著高于一次线性扫描。在只需处理原串非重叠匹配时，可以采用第2.7节的单趟生成结果策略；题目若明确追求高性能，再进一步讨论批量匹配及存储结构优化。

---

## 十四、延伸的典型编程例子与常见边界

### 14.1 例：统计模式串在主串里出现多少次

要先决定是否允许**重叠**。

例如`s="aaaaa"`，`t="aa"`：

- 允许重叠：起点1、2、3、4，共4次。
- 不允许重叠：按从左到右优先选择起点1、3，共2次。

```cpp
#include <iostream>
#include <string>

int countMatches(const std::string& s, const std::string& t, bool allowOverlap) {
    if (t.empty()) return 0;                  // 本例约定不统计空模式。
    int count = 0;
    std::size_t pos = 0;
    while ((pos = s.find(t, pos)) != std::string::npos) {
        ++count;                              // 又发现一次匹配。
        pos += allowOverlap ? 1 : t.size();  // 允许重叠时仅前进一步。
    }
    return count;
}

int main() {
    std::cout << countMatches("aaaaa", "aa", true) << '\n';  // 4。
    std::cout << countMatches("aaaaa", "aa", false) << '\n'; // 2。
}
```

### 14.2 例：判断一个串是否为另一个串的子串

```cpp
#include <iostream>
#include <string>

bool contains(const std::string& s, const std::string& t) {
    return s.find(t) != std::string::npos; // 标准库约定空串也可找到。
}

int main() {
    std::cout << contains("datastructure", "str") << '\n'; // 1。
    std::cout << contains("datastructure", "xyz") << '\n'; // 0。
    std::cout << contains("data", "") << '\n';            // 1。
}
```

这里故意展示了**标准库对空模式的处理**，它与课件`Index`要求T非空的初始条件不同。实际写题时先判断使用的是哪套API约定。

### 14.3 例：最长相等真前后缀长度的直接验证程序

学习KMP前，可以先用一份简单直接的程序验证“前后缀相等”的含义，它的目标是**帮助手算**，不追求最优复杂度。

```cpp
#include <iostream>
#include <string>

int longestBorder(const std::string& s) {
    int n = static_cast<int>(s.size());
    for (int len = n - 1; len >= 1; --len) { // 从可能的最长真前后缀开始试。
        if (s.substr(0, len) == s.substr(n - len, len)) {
            return len;                       // 首次找到的就是最长长度。
        }
    }
    return 0;                                // 没有非空相等真前后缀。
}

int main() {
    std::cout << longestBorder("ababa") << '\n';  // 3，对应aba。
    std::cout << longestBorder("abaab") << '\n';  // 2，对应ab。
    std::cout << longestBorder("abcd") << '\n';   // 0。
}
```

> [!warning] `std::string`对中文UTF-8字符的长度计算
> 本章课件的例子主要用单字节英文字符，字符数量与字节数量可以直接对应。但对于UTF-8编码的中文文本，`std::string::size()`通常返回**字节数**，不等于肉眼看到的汉字个数。直接按字节做子串操作可能把一个汉字拆开。涉及多语言字符时，要先约定编码及“字符”的计数单位，不能原封不动套用英文串的所有操作。

### 14.4 例：判断两个串是否具有相同的前缀

```cpp
#include <iostream>
#include <string>

bool samePrefix(const std::string& a, const std::string& b, int count) {
    if (count < 0 || count > static_cast<int>(a.size()) ||
        count > static_cast<int>(b.size())) return false;
    return a.compare(0, static_cast<std::size_t>(count),
                     b, 0, static_cast<std::size_t>(count)) == 0;
}

int main() {
    std::cout << samePrefix("abcde", "abcxy", 3) << '\n'; // 1。
    std::cout << samePrefix("abcde", "abcxy", 4) << '\n'; // 0。
}
```

这段练习把串的比较、长度校验和前缀概念联系起来，可用来帮助理解`next`中的公共前缀。

---

## 十五、考前速查与知识联系

### 15.1 串的基本操作速查

| 概念或操作 | 考试应记内容 | C++常用对应方法 |
| --- | --- | --- |
| 串长 | 字符个数，空格也算 | `s.size()` |
| 空串 | 长度0 | `s.empty()` |
| 串比较 | 按对应字符依次比较 | `s.compare(t)`、`==`、`<` |
| 拼接 | 将两个字符序列连接 | `s+t`、`s+=t` |
| 求子串 | 从`pos`开始取`len`个字符 | `s.substr(pos-1,len)`（教材1基转换） |
| 定位 | 返回首次出现位置 | `s.find(t)`（0基，失败`npos`） |
| 插入 | 在指定字符之前添加串 | `s.insert(pos-1,t)` |
| 删除 | 删除指定区间 | `s.erase(pos-1,len)` |
| 替换 | 原串不重叠替换 | 可结合`find`与构造新串 |

### 15.2 三种存储方式速查

| 对比项 | 定长顺序 | 堆分配 | 块链 |
| --- | --- | --- | --- |
| 物理结构 | 连续 | 连续 | 链表各块可分散 |
| 串长是否受固定上限限制 | 是 | 一般按需分配 | 可逐块扩展 |
| 按位置读取 | 方便 | 方便 | 往往需定位到相应结点 |
| 串增长 | 可能截断 | 重新分配或扩容 | 可申请新结点 |
| 典型管理开销 | 固定容量中的空闲位置 | 分配、释放、复制 | 指针、块内空位 |
| 本章抓手 | **0号放长度、1号起存字符** | **`ch`与`length`** | **`head`、`tail`、`length`** |

### 15.3 BF、首尾匹配、KMP速查

| 算法 | 失配后的处理 | 预处理 | 最坏时间 |
| --- | --- | --- | --- |
| BF | 主串尝试起点后移1位，模式回到开头 | 不需要 | $O(nm)$ |
| 首尾匹配 | 先查首、尾，失败则换下一候选起点 | 不需要 | $O(nm)$ |
| KMP | 主串不回退，模式指针按`next`或`nextval`回退 | 需要模式辅助表 | $O(n+m)$（含构表） |

### 15.4 `next`与`nextval`速查

> [!summary] KMP考前必须掌握的五句话
> 1. **`next[1]=0`**，这是本课件的1基定义。
> 2. 对$j\ge2$，`next[j] = 模式前(j-1)个字符的最长相等真前后缀长度 + 1`。
> 3. 失配时**`i`不动、`j=next[j]`**；若`j`退到0，则下一轮`i`、`j`同时加1。
> 4. `nextval`在普通`next`基础上，跳过会与当前失配字符重复比较的相同模式字符。
> 5. `next`、`nextval`是两套回退表，**返回的匹配位置必须相同**，它们改变的是内部比较次数，不是匹配的定义。

### 15.5 一份统一例子：四种表格记忆

| 模式 | `next` | `nextval` |
| --- | --- | --- |
| `aaab` | `0 1 2 3` | `0 0 0 3` |
| `aaaab` | `0 1 2 3 4` | `0 0 0 0 4` |
| `abcabaa` | `0 1 1 1 2 3 2` | `0 1 1 0 1 3 2` |
| `abaabcac` | `0 1 1 2 2 3 1 2` | `0 1 0 2 1 3 0 2` |

这四个模式能覆盖：没有公共前后缀、公共前后缀逐步增长、失配后多次回退，以及大量重复字符引发的`nextval`优化。

### 15.6 最容易出现的九类错误

| 错误 | 正确认识 |
| --- | --- |
| 认为空串和空格串一样 | 空串长度0，空格串长度大于0 |
| 忽略空格参与计数 | 所有实际字符都占一个串位置 |
| 子串可以不连续 | 子串必须连续，任意抽取是子序列 |
| 教材第1位直接写成`s[1]` | C++标准字符串第1个字符是`s[0]` |
| 把课件`S[0]`和C字符串`s[0]`当成同一含义 | 前者课件长度前置，后者通常是首字符 |
| `Index`找不到返回`npos` | 课件定义返回0，标准库返回`npos` |
| BF失配后从当前主串字符继续匹配模式首字符 | BF下一轮从**本趟起点+1**开始 |
| `next[j]`根据模式前$j$个字符计算 | 只看**前$j-1$个已匹配字符** |
| 把普通`next`和`nextval`的数值混用 | 两者根据不同规则计算，必须与算法匹配 |

### 15.7 自测：按知识依赖关系练习

> [!question] 自我检测
> 1. 对`S="ababa"`，分别列出`"aba"`出现的所有起点，以及从`pos=3`起的首次匹配位置。
> 2. 为什么定长串的第0位保存长度后，第1个字符不在`S[0]`？
> 3. 为什么`S="aaaaa"`、`T="aa"`的**重叠出现次数**与**不重叠出现次数**不同？
> 4. 给模式`"ababac"`手算`next`，说出第6位失配时模式指针回退到哪里。
> 5. 对`"aaaab"`分别求`next`和`nextval`，解释为什么后者能减少无意义比较。
> 6. 串在堆分配存储下为什么仍可能需要$O(n)$时间完成中间插入？

<details>
<summary>展开自测参考答案</summary>

1. `"aba"`起点为1、3；从`pos=3`起返回3。
2. 因为课程采用“长度前置”方案，`S[0]`特意留给串长，字符从`S[1]`开始。
3. 重叠匹配起点为1、2、3、4共4次；不重叠从左到右选1、3，共2次。
4. `"ababac"`的`next`为`0 1 1 2 3 4`；在第6位失配，`j=next[6]=4`。
5. `next=0 1 2 3 4`，`nextval=0 0 0 0 4`；因前4位都是`a`，知道当前字符不等于`a`后不必反复拿`a`比较。
6. 因为字符数据要求连续，插入时必须挪动或重新复制插入位置后面的字符。

</details>

---

## 十六、代码阅读与使用说明

> [!warning] 原课件中的代码示意与正式程序要区分
> 课件部分页面主要用于说明算法思想，不能直接复制为合法、可编译的C/C++源码。整理时已保持**算法含义与接口语义**，而把具体实现改为标准程序：
>
> - 课件中 `T[1..n] = S[1..n]` 这样的**区间赋值表达方式**不是C/C++的合法数组语法；实际程序必须用循环、`std::copy`等明确复制字符。
> - `strcpy(str1,str2,k)`并不是标准C库`strcpy`的函数签名，标准`strcpy`只接受目标和源两个参数；复制有界字符序列更应显式校验容量。
> - `gets`是不安全的过时接口，已从C11标准移除，不应拿来作为可执行的输入示例。
> - 把`realloc`的返回值直接覆盖原指针，会在分配失败时丢失旧指针；正常实现应先保留返回结果、检查成功后再替换。本笔记的C++实现用更直观的重新申请与安全交接方式。
> - 课件有的代码采用未给出定义的`Status`、`SString`或范围赋值形式，属于**不完整的教学片段**；本笔记的配套工程全部使用已明确声明的真实类型，不使用人为造出的抽象占位符。
>
> 这不是改变课程知识点，而是把抽象说明转成真正可检查、可运行的具体程序。

本文代码以 **C++17** 为主。之所以保留`FixedString`、`HeapString`、`ChunkString`等具体结构，是因为它们分别对应本章需要学习的**实际存储模型**；并非为了把简单整数或字符人为包装成ADT别名。

- **短代码块**：用于展示一个核心操作、成员函数或合法的C++语句片段；在紧邻正文中说明所依赖的类型和函数。
- **完整代码块**：可以单独保存为`.cpp`，按标准C++17编译。
- **配套独立程序**：提供五个可单独编译的`.cpp`源文件，覆盖本章存储结构、基本操作、BF、首尾匹配、KMP、`next`、`nextval`与课后题；每份都包含`main()`和测试断言。

Mac（Clang）或使用g++的环境可按如下命令编译：

```bash
clang++ -std=c++17 -Wall -Wextra -pedantic 05_match_algorithms.cpp -o match_algorithms
./match_algorithms
```

Windows下可将编译器命令改为：

```bash
g++ -std=c++17 -Wall -Wextra -pedantic 05_match_algorithms.cpp -o match_algorithms.exe
./match_algorithms.exe
```

> [!abstract] 本章的最终知识网络
> **逻辑结构**决定串是什么、子串和基本操作的语义；**存储结构**决定串长、拼接、插入、删除等操作怎样付出时间与空间代价；**模式匹配**从BF逐个试起点出发，经首尾比较的短路优化，最终利用模式内部公共前后缀得到KMP；`next`描述失配后的回退位置，`nextval`进一步消除重复字符的无效回退。
>
> 真正理解本章，应当能够：**准确计数与定位 → 写出三类存储的核心表示 → 独立实现BF → 手算教材版`next` → 在`next`基础上算`nextval` → 解释KMP的每一次指针变化**。
