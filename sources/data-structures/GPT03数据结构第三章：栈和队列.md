# 数据结构第三章：栈和队列

> [!abstract] 本章学习路线
> 本章围绕两种**操作受限的线性表**展开：先理解栈与队列的逻辑特点，再学习顺序存储和链式存储的实现，最后把它们用于数制转换、括号匹配、表达式求值、迷宫回溯、递归、汉诺塔、N 皇后和循环队列等问题。
>
> **代码约定：** 示例统一使用标准 **C++17**；不使用 `typedef` 或类型别名；普通数据元素默认使用 `int`，确有需要时才使用 `char`、`string`、`bool` 等类型。动态内存使用 `new` / `delete`，不混用 C 的 `malloc` / `free`。代码中的关键步骤尽量配有行内注释。

> [!tip] 阅读算法的建议顺序
> 1. 先确认指针或下标代表什么。
> 2. 再确认空、满、越界等边界条件。
> 3. 逐行跟踪入栈、出栈、入队、出队后，数据和指针如何变化。
> 4. 最后分析时间复杂度与空间复杂度。

## 目录

- 1. 栈和队列：操作受限的线性表
- 2. 栈的定义与基本操作
- 3. 顺序栈：数组实现
- 4. 动态顺序栈与链栈
- 5. 栈的应用：数制转换、括号匹配、行编辑
- 6. 栈的应用：迷宫回溯
- 7. 表达式与栈
- 8. 递归与系统调用栈
- 9. 汉诺塔与 N 皇后
- 10. 队列的定义与基本操作
- 11. 顺序队列与假溢出
- 12. 循环队列
- 13. 链队列
- 14. k 阶斐波那契序列与循环队列
- 15. 栈和队列综合比较
- 16. 易错点与典型练习

---

# 1. 栈和队列：操作受限的线性表

## 1.1 为什么说栈和队列是线性表？

线性表中的数据元素按逻辑顺序排列，除首元素和尾元素外，每个元素都有唯一的直接前驱和直接后继。普通线性表允许在指定合法位置插入、删除元素；栈和队列则进一步限制了操作位置。

| 结构 | 插入位置 | 删除位置 | 访问规则 | 核心特点 |
|---|---|---|---|---|
| 普通线性表 | 合法位置 | 合法位置 | 取决于存储结构 | 操作位置较自由 |
| 栈（Stack） | 栈顶 | 栈顶 | 后进先出 | LIFO |
| 队列（Queue） | 队尾 | 队头 | 先进先出 | FIFO |

> [!important] 一句话记忆
> - **栈：从同一端进出，后进先出（LIFO）。**
> - **队列：一端进入、另一端离开，先进先出（FIFO）。**

## 1.2 两种结构的直观示意

```text
栈：同一端进出

        入栈 ↓    ↑ 出栈
             ┌───┐  ← 栈顶
             │ C │
             ├───┤
             │ B │
             ├───┤
             │ A │
             └───┘  ← 栈底

队列：队尾进入，队头离开

出队 ← 队头 ┌───┬───┬───┐ 队尾 ← 入队
            │ A │ B │ C │
            └───┴───┴───┘
```

> [!example] 生活类比
> - 一摞盘子：最后放上去的盘子通常最先拿走，符合栈。
> - 排队买票：先排队的人先办理，符合队列。

---

# 2. 栈的定义与基本操作

## 2.1 定义与术语

**栈（Stack）** 是限定仅在表尾进行插入和删除操作的线性表。

- **栈顶（top）**：允许插入和删除的一端。
- **栈底（bottom）**：栈的另一端。
- **空栈**：不包含任何数据元素的栈。
- **入栈（Push）**：将新元素放到栈顶。
- **出栈（Pop）**：删除栈顶元素，并通常把该元素的值交给调用者。
- **取栈顶（GetTop）**：读取栈顶元素，但不删除它。
- **栈上溢**：向已经满的固定容量栈继续入栈。
- **栈下溢**：从空栈出栈，或在空栈上执行要求栈非空的操作。

若入栈顺序为：

$$
a_1,a_2,\ldots,a_n
$$

则全部出栈时的顺序为：

$$
a_n,a_{n-1},\ldots,a_2,a_1
$$

> [!warning] “栈顶指针”的定义有两种常见约定
> - **下标式**：`top` 指向当前栈顶元素；空栈可令 `top = -1`。
> - **计数式 / 下一空位式**：`top` 表示当前元素个数，同时指向下一个可写位置；空栈令 `top = 0`。
>
> 两种约定都可以实现栈，但判空、判满、入栈和出栈的代码必须与所选约定一致。本文的固定数组栈统一采用**下一空位式**，避免在不同代码中混用规则。

## 2.2 抽象数据类型与基本操作

栈的逻辑定义不依赖它具体用数组还是链表存储。常见操作如下：

| 操作 | 作用 | 典型前置条件 |
|---|---|---|
| `InitStack` | 初始化为空栈 | 栈对象可用 |
| `DestroyStack` | 释放栈占用的资源 | 栈已初始化 |
| `ClearStack` | 删除全部元素，保留栈对象 | 栈已初始化 |
| `StackEmpty` | 判断是否为空 | 栈已初始化 |
| `StackLength` | 返回元素个数 | 栈已初始化 |
| `GetTop` | 读取栈顶元素 | 栈非空 |
| `Push` | 插入新栈顶元素 | 栈未满或能够扩容 |
| `Pop` | 删除并返回栈顶元素 | 栈非空 |

> [!important] 入栈、出栈的逻辑顺序
> - 入栈：先确保有空间，再写入新元素，最后更新栈顶状态。
> - 出栈：先检查栈非空，再取得栈顶元素，最后更新栈顶状态。
> - 取栈顶：只读取，不改变栈的长度。

## 2.3 栈的合法出栈序列

假设三个元素按 `1、2、3` 的顺序入栈，所有可能的出栈序列为：

| 出栈序列 | 入栈 / 出栈操作（`S` 表示入栈，`X` 表示出栈） |
|---|---|
| `1, 2, 3` | `S X S X S X` |
| `1, 3, 2` | `S X S S X X` |
| `2, 1, 3` | `S S X X S X` |
| `2, 3, 1` | `S S X S X X` |
| `3, 2, 1` | `S S S X X X` |

判断一条序列是否合法时，按给定入栈顺序模拟：需要某元素出栈时，如果它不在栈顶，就不能直接跳过上面的元素。

> [!tip] 快速判断
> 若元素 `1` 还压在元素 `2` 的下面，那么 `2` 可以先出栈，但 `1` 不能越过 `2` 直接出栈。**栈内元素只能从栈顶移除。**

---

# 3. 顺序栈：数组实现

## 3.1 存储思想

顺序栈使用一段连续的数组空间保存元素。数组下标连续，栈底位置固定，栈顶随入栈和出栈而变化。

本文采用 `top` 表示**栈内元素个数**，也就是下一个可写位置：

- 空栈：`top == 0`。
- 栈满：`top == STACK_CAPACITY`。
- 入栈：写入 `data[top]`，再执行 `top++`。
- 出栈：先执行 `top--`，再读取 `data[top]`。
- 栈长：`top`。

```text
容量为 5 的数组栈

下标：  0    1    2    3    4
      ┌────┬────┬────┬────┬────┐
空栈  │    │    │    │    │    │   top = 0
      └────┴────┴────┴────┴────┘

依次压入 10、20、30 后：
      ┌────┬────┬────┬────┬────┐
      │ 10 │ 20 │ 30 │    │    │   top = 3
      └────┴────┴────┴────┴────┘
                         ↑
                    下一个可写位置
```

## 3.2 固定容量顺序栈：完整实现

```cpp
#include <iostream>
using namespace std;

const int STACK_CAPACITY = 100;  // 数组栈最多保存 100 个整数

struct ArrayStack {
    int data[STACK_CAPACITY];   // 连续存放栈内元素
    int top;                    // 当前元素个数，也是下一个可写位置
};

void initStack(ArrayStack& s) {
    s.top = 0;                  // 初始化为空栈
}

bool isEmpty(const ArrayStack& s) {
    return s.top == 0;          // 元素个数为 0，说明栈空
}

bool isFull(const ArrayStack& s) {
    return s.top == STACK_CAPACITY; // 下一空位已经越过数组末尾
}

int stackLength(const ArrayStack& s) {
    return s.top;               // top 就是当前元素个数
}

bool push(ArrayStack& s, int value) {
    if (isFull(s)) {            // 写入前必须先检查容量
        return false;           // 固定容量栈无法继续入栈
    }

    s.data[s.top] = value;      // 把新元素放在下一个空位
    s.top++;                    // 更新元素个数和下一空位位置
    return true;
}

bool pop(ArrayStack& s, int& value) {
    if (isEmpty(s)) {           // 空栈没有可删除的栈顶元素
        return false;
    }

    s.top--;                    // 先回到原栈顶元素所在下标
    value = s.data[s.top];      // 取出元素值并交给调用者
    return true;
}

bool getTop(const ArrayStack& s, int& value) {
    if (isEmpty(s)) {           // 空栈不能读取栈顶
        return false;
    }

    value = s.data[s.top - 1];  // 栈顶元素位于 top - 1
    return true;                // 没有修改 top，因此元素仍留在栈内
}

void clearStack(ArrayStack& s) {
    s.top = 0;                  // 逻辑上清空，不必逐个擦除数组内容
}

int main() {
    ArrayStack s;
    initStack(s);               // 先建立空栈

    push(s, 10);                // 10 成为栈底元素
    push(s, 20);                // 20 位于 10 上方
    push(s, 30);                // 30 成为当前栈顶

    int value;
    if (getTop(s, value)) {
        cout << "栈顶：" << value << '\n'; // 输出 30，不删除它
    }

    if (pop(s, value)) {
        cout << "出栈：" << value << '\n'; // 输出 30，并删除它
    }

    cout << "当前长度：" << stackLength(s) << '\n'; // 输出 2
    clearStack(s);              // 将栈重新置空
    return 0;
}
```

> [!important] 为什么出栈要先 `top--`？
> `top` 指向的是下一个可写位置，而不是当前栈顶元素。若当前有 3 个元素，`top == 3`，栈顶元素下标是 `2`。所以出栈时先将 `top` 减为 `2`，再读取 `data[2]`。

## 3.3 顺序栈的时间复杂度

| 操作 | 时间复杂度 | 原因 |
|---|---:|---|
| 判空、判满、求长度 | `O(1)` | 只检查 `top` |
| 取栈顶 | `O(1)` | 直接访问 `data[top - 1]` |
| 入栈 | `O(1)` | 固定容量下只写入一个位置 |
| 出栈 | `O(1)` | 只更新 `top` 并读取一个元素 |
| 清空 | `O(1)` | 只将 `top` 设为 0 |

> [!warning] 固定容量栈的边界
> 入栈前必须判断是否已满；出栈和取栈顶前必须判断是否为空。不能先访问 `data[top]` 或 `data[top - 1]` 再判断，否则可能越界。

---

# 4. 动态顺序栈与链栈

## 4.1 动态顺序栈

固定容量数组需要提前确定最大长度。动态顺序栈仍使用连续数组，但容量不足时申请更大的数组，将原元素复制过去，再释放旧数组。

> [!note] 动态扩容的关键步骤
> 1. 发现栈满。
> 2. 申请更大的数组。
> 3. 将原有元素复制到新数组。
> 4. 释放旧数组。
> 5. 让栈指向新数组，并更新容量。
> 6. 再执行本次入栈。

```cpp
#include <iostream>
#include <new>
using namespace std;

struct DynamicStack {
    int* data;      // 指向动态申请的数组
    int top;        // 当前元素个数
    int capacity;   // 当前数组容量
};

bool initStack(DynamicStack& s, int initialCapacity) {
    if (initialCapacity <= 0) {
        return false;           // 容量必须是正数
    }

    s.data = new (nothrow) int[initialCapacity]; // 申请整数数组
    if (s.data == nullptr) {
        return false;           // 申请失败时不能继续使用数组
    }

    s.top = 0;                  // 初始为空栈
    s.capacity = initialCapacity;
    return true;
}

bool push(DynamicStack& s, int value) {
    if (s.top == s.capacity) {  // 没有空位，需要扩容
        int newCapacity = s.capacity * 2;
        int* newData = new (nothrow) int[newCapacity];
        if (newData == nullptr) {
            return false;       // 扩容失败，旧数组仍然有效
        }

        for (int i = 0; i < s.top; i++) {
            newData[i] = s.data[i]; // 复制所有有效元素
        }

        delete[] s.data;        // 复制完成后才能释放旧数组
        s.data = newData;       // 让栈改用新数组
        s.capacity = newCapacity;
    }

    s.data[s.top] = value;      // 在下一空位写入元素
    s.top++;
    return true;
}

bool pop(DynamicStack& s, int& value) {
    if (s.top == 0) {
        return false;           // 空栈不能出栈
    }

    s.top--;
    value = s.data[s.top];      // 读取原栈顶元素
    return true;
}

void destroyStack(DynamicStack& s) {
    delete[] s.data;            // 释放动态数组
    s.data = nullptr;           // 清除悬空指针，避免误用
    s.top = 0;
    s.capacity = 0;
}

int main() {
    DynamicStack s;
    if (!initStack(s, 2)) {     // 先申请只能存 2 个元素的数组
        cout << "初始化失败\n";
        return 1;
    }

    push(s, 10);
    push(s, 20);
    push(s, 30);                // 第三个元素会触发扩容

    int value;
    while (pop(s, value)) {     // 按后进先出顺序输出
        cout << value << ' ';
    }
    cout << '\n';

    destroyStack(s);            // 使用结束后释放数组
    return 0;
}
```

> [!warning] 动态数组的内存安全
> `delete[]` 释放的是由 `new[]` 申请的数组。不能在释放旧数组之前就丢失旧指针；否则旧数组无法再被访问，也无法正常释放。扩容申请失败时，应保留旧数组和原有数据。

## 4.2 链栈

链栈用链表结点保存元素，通常让**栈顶指针指向第一个数据结点**。入栈和出栈都在链表头部进行，因此不需要遍历整个链表。

```text
top
 ↓
┌────┬────┐    ┌────┬────┐    ┌────┬────┐
│ 30 │  ──┼──→ │ 20 │  ──┼──→ │ 10 │ null
└────┴────┘    └────┴────┘    └────┴────┘
 栈顶                              栈底
```

```cpp
#include <iostream>
#include <new>
using namespace std;

struct StackNode {
    int data;           // 结点保存的数据
    StackNode* next;    // 指向下一个结点
};

struct LinkedStack {
    StackNode* top;     // 指向当前栈顶；nullptr 表示空栈
};

void initStack(LinkedStack& s) {
    s.top = nullptr;    // 空链栈没有数据结点
}

bool isEmpty(const LinkedStack& s) {
    return s.top == nullptr;
}

bool push(LinkedStack& s, int value) {
    StackNode* node = new (nothrow) StackNode;
    if (node == nullptr) {
        return false;   // 申请结点失败，原栈保持不变
    }

    node->data = value;
    node->next = s.top; // 新结点先指向原栈顶
    s.top = node;       // 再让 top 指向新结点
    return true;
}

bool pop(LinkedStack& s, int& value) {
    if (isEmpty(s)) {
        return false;   // 空栈不能删除结点
    }

    StackNode* oldTop = s.top; // 暂存待删除结点的地址
    value = oldTop->data;      // 先取出数据
    s.top = oldTop->next;      // 栈顶移动到下一个结点
    delete oldTop;             // 最后释放原栈顶结点
    return true;
}

void clearStack(LinkedStack& s) {
    int value;
    while (pop(s, value)) {    // 反复出栈，逐个释放结点
        // 数据不需要保留，因此只需调用 pop。
    }
}

int main() {
    LinkedStack s;
    initStack(s);
    push(s, 10);
    push(s, 20);
    push(s, 30);

    int value;
    while (pop(s, value)) {
        cout << value << ' ';  // 输出 30 20 10
    }
    cout << '\n';
    return 0;                  // 栈已空，不再有动态结点需要释放
}
```

> [!important] 链栈入栈的指针顺序
> ```cpp
> node->next = s.top; // 新结点先接上原链表
> s.top = node;       // 再移动栈顶指针
> ```
> 如果先执行 `s.top = node`，再执行 `node->next = s.top`，就会让新结点指向自己，破坏链表结构。

## 4.3 顺序栈与链栈对比

| 比较项 | 顺序栈 | 链栈 |
|---|---|---|
| 存储空间 | 连续数组 | 动态结点，不要求连续 |
| 是否预设容量 | 固定栈需要；动态栈可扩容 | 通常不预设固定容量 |
| 入栈 / 出栈 | `O(1)`；动态扩容时单次可能为 `O(n)` | `O(1)` |
| 额外空间 | 数组通常没有每元素指针开销 | 每个结点需要指针域 |
| 主要风险 | 数组越界、扩容和复制 | 空指针、内存泄漏、错误释放 |
| 适用场景 | 容量可估计、希望存储紧凑 | 元素数量变化大、难以预估容量 |

---

# 5. 栈的应用：数制转换、括号匹配、行编辑

## 5.1 数制转换：为什么需要栈？

将非负十进制整数转换为 `d` 进制时，反复执行除法：

$$
N=(N\div d)\times d+(N\bmod d)
$$

其中余数就是当前最低位。每次得到的余数顺序是**从低位到高位**，但输出数字需要**从高位到低位**，因此可把余数依次入栈，再依次出栈输出。

例如，将十进制 `1348` 转换为八进制：

| 当前数值 | 除以 8 的商 | 余数 |
|---:|---:|---:|
| 1348 | 168 | 4 |
| 168 | 21 | 0 |
| 21 | 2 | 5 |
| 2 | 0 | 2 |

余数产生顺序是 `4、0、5、2`；出栈后输出 `2504`。

```cpp
#include <iostream>
using namespace std;

const int STACK_CAPACITY = 64; // 足够保存 int 的二进制位数

struct IntStack {
    int data[STACK_CAPACITY];
    int top;                    // 指向下一个空位
};

bool push(IntStack& s, int value) {
    if (s.top == STACK_CAPACITY) return false;
    s.data[s.top++] = value;    // 写入后，栈顶位置加 1
    return true;
}

bool pop(IntStack& s, int& value) {
    if (s.top == 0) return false;
    value = s.data[--s.top];    // 先减 1，再取出栈顶值
    return true;
}

int main() {
    int number, base;
    cout << "输入非负十进制整数和目标进制（2 到 10）：";
    cin >> number >> base;

    if (number < 0 || base < 2 || base > 10) {
        cout << "输入范围不合法\n";
        return 1;
    }

    IntStack s;
    s.top = 0;                  // 初始化为空栈

    if (number == 0) {
        push(s, 0);              // 特别处理 0，否则 while 不会执行
    }

    while (number > 0) {
        int remainder = number % base; // 取出当前最低位
        if (!push(s, remainder)) {
            cout << "栈空间不足\n";
            return 1;
        }
        number /= base;          // 继续处理更高位
    }

    cout << "转换结果：";
    int digit;
    while (pop(s, digit)) {
        cout << digit;           // 逆序弹出余数，恢复正确位序
    }
    cout << '\n';
    return 0;
}
```

> [!warning] 两个边界
> - `number == 0` 时，结果应输出 `0`，不能输出空字符串。
> - 上面示例限定目标进制为 2 到 10，所以每一位都能用字符 `0` 到 `9` 表示；若要转换为十六进制，还需处理 `A` 到 `F`。

## 5.2 括号匹配

括号匹配不仅要统计左右括号数量，还要保证**嵌套顺序正确**。

例如：

- `([]())`：匹配正确。
- `([)]`：左右括号数量相同，但嵌套顺序错误。
- `(()`：左括号有剩余。
- `())`：遇到多余的右括号。

算法思想：

1. 遇到左括号 `(`、`[`、`{`，将它压入栈。
2. 遇到右括号，先检查栈是否为空；若为空，说明右括号多余。
3. 若栈非空，检查栈顶左括号是否与当前右括号匹配；匹配则出栈，否则失败。
4. 扫描结束后，只有栈为空才算全部匹配。

```cpp
#include <iostream>
#include <string>
using namespace std;

bool isLeftBracket(char ch) {
    return ch == '(' || ch == '[' || ch == '{';
}

bool isRightBracket(char ch) {
    return ch == ')' || ch == ']' || ch == '}';
}

bool matches(char left, char right) {
    // 每种右括号只能与对应种类的左括号匹配
    return (left == '(' && right == ')') ||
           (left == '[' && right == ']') ||
           (left == '{' && right == '}');
}

bool bracketsMatch(const string& expression) {
    string s;                   // 用字符串尾部模拟栈

    for (char ch : expression) {
        if (isLeftBracket(ch)) {
            s.push_back(ch);    // 左括号入栈，等待对应右括号
        } else if (isRightBracket(ch)) {
            if (s.empty()) {
                return false;   // 没有未匹配的左括号可对应
            }

            if (!matches(s.back(), ch)) {
                return false;   // 栈顶括号类型不匹配
            }

            s.pop_back();       // 匹配成功，消去这一对括号
        }
        // 非括号字符不影响括号匹配，可直接忽略
    }

    return s.empty();           // 若还有左括号未匹配，则失败
}

int main() {
    string expression;
    cout << "输入表达式：";
    getline(cin, expression);

    if (bracketsMatch(expression)) {
        cout << "括号匹配正确\n";
    } else {
        cout << "括号匹配错误\n";
    }
    return 0;
}
```

> [!important] 为什么不能只数左右括号？
> `([)]` 中左右括号数量相同，但第一个右括号 `)` 不能与栈顶的 `[` 匹配。栈能保存“最近尚未匹配的左括号”，因此能够检查嵌套顺序。

## 5.3 行编辑程序

行编辑程序允许用户在一行输入过程中纠错。这里约定：

- 普通字符：加入当前缓冲区。
- `#`：删除当前行最后一个字符；若缓冲区为空，则不操作。
- `@`：清空当前行缓冲区。
- 换行符：提交当前行并清空缓冲区。

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string buffer;              // 当前行的输入缓冲区
    char ch;

    while (cin.get(ch)) {       // 逐字符读取，保留空格等普通字符
        if (ch == '\n') {
            cout << buffer << '\n'; // 一行输入结束，输出修正后的内容
            buffer.clear();          // 为下一行重新准备缓冲区
        } else if (ch == '#') {
            if (!buffer.empty()) {
                buffer.pop_back();   // 删除最近输入且尚未提交的字符
            }
        } else if (ch == '@') {
            buffer.clear();          // 整行作废，但不影响已经提交的行
        } else {
            buffer.push_back(ch);    // 普通字符放到缓冲区末尾
        }
    }

    // 如果文件结束时还有未换行的内容，也将它输出。
    if (!buffer.empty()) {
        cout << buffer << '\n';
    }
    return 0;
}
```

> [!note] 为什么缓冲区适合用栈的思想？
> 退格只影响最近输入的字符，撤销顺序是“最后输入的字符最先被删除”，符合后进先出的特点。`string` 的 `push_back()` 和 `pop_back()` 正好模拟了栈顶操作。

---

# 6. 栈的应用：迷宫回溯

## 6.1 基本思想

迷宫求解可使用深度优先搜索和回溯：

1. 当前位置可通，就把它加入当前路径。
2. 按指定方向顺序寻找下一个可通位置。
3. 若当前位置四周都无法继续，则从路径栈中删除当前位置，回到上一个位置尝试其他方向。
4. 到达出口时，栈中保存的就是一条路径；栈退空仍未找到出口，则没有找到通路。

> [!important] 栈在迷宫中的作用
> 栈不仅保存“走过的格子”，还保存探索过程中需要返回的位置。**走不通就回退到最近一个仍有其他方向可试的位置**，这正是后进先出的应用。

## 6.2 可运行的迷宫搜索示例

下面用 `#` 表示墙，`.` 表示可通行位置，`S` 表示入口，`E` 表示出口。搜索方向依次为东、南、西、北，与顺时针尝试方向的思路一致。

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct Cell {
    int row;        // 当前格子的行号
    int col;        // 当前格子的列号
    int nextDir;    // 下一次准备尝试的方向编号
};

bool inside(const vector<string>& maze, int row, int col) {
    return row >= 0 && row < static_cast<int>(maze.size()) &&
           col >= 0 && col < static_cast<int>(maze[0].size());
}

int main() {
    vector<string> maze = {
        "#########",
        "#S...#..#",
        "#.#..#E.#",
        "#.#.....#",
        "#.......#",
        "#########"
    };

    const int dr[4] = {0, 1, 0, -1}; // 东、南、西、北的行变化量
    const int dc[4] = {1, 0, -1, 0}; // 东、南、西、北的列变化量
    int rows = static_cast<int>(maze.size());
    int cols = static_cast<int>(maze[0].size());
    vector<vector<int>> visited(rows, vector<int>(cols, 0));

    int startRow = -1, startCol = -1;
    int endRow = -1, endCol = -1;

    // 先扫描地图，找到入口和出口。
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (maze[r][c] == 'S') {
                startRow = r;
                startCol = c;
            }
            if (maze[r][c] == 'E') {
                endRow = r;
                endCol = c;
            }
        }
    }

    if (startRow == -1 || endRow == -1) {
        cout << "地图缺少入口或出口\n";
        return 1;
    }

    vector<Cell> path;          // vector 尾部充当栈顶，保存当前搜索路径
    path.push_back({startRow, startCol, 0});
    visited[startRow][startCol] = 1;
    bool found = false;

    while (!path.empty()) {
        Cell& current = path.back(); // 只处理当前路径最末端的格子

        if (current.row == endRow && current.col == endCol) {
            found = true;           // 已到出口，栈内就是一条完整路径
            break;
        }

        if (current.nextDir == 4) {
            path.pop_back();        // 四个方向都尝试过，回退到上一个格子
            continue;
        }

        int dir = current.nextDir;  // 记录本次要尝试的方向
        current.nextDir++;          // 下次回到这里时尝试下一个方向

        int nr = current.row + dr[dir];
        int nc = current.col + dc[dir];

        if (!inside(maze, nr, nc)) continue; // 越界位置不可走
        if (maze[nr][nc] == '#') continue;   // 墙不可走
        if (visited[nr][nc]) continue;       // 避免在搜索中反复绕圈

        visited[nr][nc] = 1;                 // 标记已探索，避免重复访问
        path.push_back({nr, nc, 0});         // 进入新格子，方向从东重新开始
    }

    if (!found) {
        cout << "没有找到通路\n";
        return 0;
    }

    cout << "找到的路径坐标（行, 列）：\n";
    for (const Cell& cell : path) {
        cout << '(' << cell.row << ", " << cell.col << ") ";
        if (maze[cell.row][cell.col] == '.') {
            maze[cell.row][cell.col] = '*';  // 用 * 标记找到的路径
        }
    }
    cout << "\n\n";

    for (const string& row : maze) {
        cout << row << '\n';               // 输出标记后的迷宫
    }
    return 0;
}
```

> [!warning] 回溯时为什么要记住 `nextDir`？
> 如果只保存行列坐标，回到某个格子时就不知道哪些方向已经试过。`nextDir` 记录下次要尝试的方向，保证回溯后能够接着试，而不是永远重复同一方向。

---

# 7. 表达式与栈

## 7.1 表达式的三种表示方法

设 `S1`、`S2` 是两个子表达式，`OP` 是运算符：

| 表示方法 | 结构 | 示例 `a + b` |
|---|---|---|
| 前缀表达式（波兰式） | `OP S1 S2` | `+ a b` |
| 中缀表达式 | `S1 OP S2` | `a + b` |
| 后缀表达式（逆波兰式） | `S1 S2 OP` | `a b +` |

对表达式 `a * b + (c - d / e) * f`：

- 前缀：`+ * a b * - c / d e f`
- 中缀：`a * b + (c - d / e) * f`
- 后缀：`a b * c d e / - f * +`

> [!important] 三种表达式的核心区别
> - 操作数之间的相对顺序通常保持一致。
> - 运算符的位置不同。
> - 中缀表达式依赖优先级和括号确定运算次序；前缀、后缀表达式可以按固定规则扫描，不必依赖括号来消除歧义。

## 7.2 算符优先级

对于只有 `+`、`-`、`*`、`/` 和括号的普通算术表达式，通常遵循：

1. 先计算括号内的表达式。
2. 乘除优先于加减。
3. 同级运算符从左向右结合。

| 运算符 | 优先级 | 说明 |
|---|---:|---|
| `(` | 特殊 | 作为隔离符，阻止括号外运算符越过它 |
| `*`、`/` | 2 | 高于加减 |
| `+`、`-` | 1 | 低于乘除 |
| `)` | 特殊 | 触发弹出运算符，直到对应左括号 |

算符优先法通常使用两个栈：

- **OPTR（运算符栈）**：保存运算符和括号。
- **OPND（操作数栈）**：保存操作数以及阶段性计算结果。

比较当前读入的运算符与 OPTR 栈顶运算符：

- 当前运算符优先级更高：当前运算符入栈。
- 栈顶运算符优先级更高或相等：先弹出栈顶运算符并计算，再继续比较当前运算符。
- 遇到右括号：计算到对应左括号为止，然后丢弃这一对括号。

> [!warning] 进行二元运算时，弹出顺序不能弄反
> 对 `a - b` 或 `a / b`，先弹出的数是右操作数 `b`，后弹出的数才是左操作数 `a`。正确的计算形式是 `a - b` 或 `a / b`，不是反过来。

## 7.3 中缀表达式转后缀表达式

转换规则：

1. 操作数直接加入后缀结果。
2. 左括号直接入运算符栈。
3. 右括号到来时，弹出运算符直到左括号，并丢弃括号。
4. 普通运算符到来时，弹出栈中优先级**大于或等于**当前运算符的运算符，再把当前运算符入栈。这里的“大于或等于”体现 `+ - * /` 的左结合规则。
5. 扫描结束后，将剩余运算符依次弹出；若仍有括号，则表达式不合法。

下面的完整程序支持**非负整数、空格、`+ - * /` 和圆括号**；不处理一元负号和小数，除法按整数除法处理。

```cpp
#include <cctype>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

bool isOperator(char ch) {
    return ch == '+' || ch == '-' || ch == '*' || ch == '/';
}

int precedence(char op) {
    if (op == '+' || op == '-') return 1; // 加减优先级较低
    if (op == '*' || op == '/') return 2; // 乘除优先级较高
    return 0;                             // 括号不参与普通比较
}

bool infixToPostfix(const string& expression, string& postfix) {
    vector<char> operators;               // 尾部作为运算符栈顶
    postfix.clear();

    for (size_t i = 0; i < expression.size();) {
        char ch = expression[i];

        if (isspace(static_cast<unsigned char>(ch))) {
            i++;                           // 忽略空格
        } else if (isdigit(static_cast<unsigned char>(ch))) {
            // 将连续数字作为一个完整整数读取，支持 123 这样的操作数。
            while (i < expression.size() &&
                   isdigit(static_cast<unsigned char>(expression[i]))) {
                postfix += expression[i];
                i++;
            }
            postfix += ' ';                // 空格用于分隔后缀表达式的数字
        } else if (ch == '(') {
            operators.push_back(ch);       // 左括号先入栈，隔离括号内运算
            i++;
        } else if (ch == ')') {
            bool foundLeft = false;
            while (!operators.empty()) {
                char op = operators.back();
                operators.pop_back();

                if (op == '(') {
                    foundLeft = true;      // 找到与当前右括号匹配的左括号
                    break;
                }
                postfix += op;
                postfix += ' ';            // 依次输出括号内的运算符
            }
            if (!foundLeft) return false;  // 右括号没有对应左括号
            i++;
        } else if (isOperator(ch)) {
            // 左结合运算符：栈顶优先级相等时也要先计算栈顶。
            while (!operators.empty() && operators.back() != '(' &&
                   precedence(operators.back()) >= precedence(ch)) {
                postfix += operators.back();
                postfix += ' ';
                operators.pop_back();
            }
            operators.push_back(ch);       // 当前运算符等待后续操作数
            i++;
        } else {
            return false;                  // 出现不支持的字符
        }
    }

    while (!operators.empty()) {
        if (operators.back() == '(') {
            return false;                  // 有左括号没有匹配的右括号
        }
        postfix += operators.back();
        postfix += ' ';
        operators.pop_back();
    }
    return !postfix.empty();
}

bool evaluatePostfix(const string& postfix, int& result) {
    istringstream input(postfix);          // 以空格分隔后缀表达式的各个 token
    vector<int> values;                    // 操作数栈
    string token;

    while (input >> token) {
        if (token.size() == 1 && isOperator(token[0])) {
            if (values.size() < 2) return false; // 二元运算至少需要两个数

            int right = values.back();
            values.pop_back();              // 先弹出右操作数
            int left = values.back();
            values.pop_back();              // 再弹出左操作数
            int answer = 0;

            switch (token[0]) {
                case '+': answer = left + right; break;
                case '-': answer = left - right; break;
                case '*': answer = left * right; break;
                case '/':
                    if (right == 0) return false; // 防止除以 0
                    answer = left / right;        // 本程序采用整数除法
                    break;
            }
            values.push_back(answer);       // 中间结果作为新操作数入栈
        } else {
            // 转换函数只输出非负整数 token，因此可用 stoi 转成 int。
            try {
                size_t used = 0;
                int number = stoi(token, &used);
                if (used != token.size()) return false;
                values.push_back(number);
            } catch (...) {
                return false;               // 数字超出范围或格式不正确
            }
        }
    }

    if (values.size() != 1) return false;   // 合法表达式最终只剩一个结果
    result = values.back();
    return true;
}

int main() {
    string expression;
    cout << "输入算术表达式：";
    getline(cin, expression);

    string postfix;
    if (!infixToPostfix(expression, postfix)) {
        cout << "表达式格式不正确或包含不支持的字符\n";
        return 1;
    }

    cout << "后缀表达式：" << postfix << '\n';

    int result;
    if (!evaluatePostfix(postfix, result)) {
        cout << "表达式无法求值（可能存在除以 0 或操作数不足）\n";
        return 1;
    }

    cout << "计算结果：" << result << '\n';
    return 0;
}
```

> [!example] 手动跟踪：`4+2*3-10/5`
> - `2*3` 先算，得到 `6`。
> - `10/5` 得到 `2`。
> - 再算 `4+6-2`，结果为 `8`。
> - 后缀表达式为 `4 2 3 * + 10 5 / -`。

## 7.4 后缀表达式如何求值？

从左向右扫描后缀表达式：

1. 读到操作数，就入栈。
2. 读到二元运算符，就先弹出右操作数，再弹出左操作数。
3. 计算 `左操作数 运算符 右操作数`，并把结果压回栈。
4. 扫描结束后，栈中应当只剩一个数，它就是表达式的值。

> [!tip] 为什么后缀表达式适合用栈？
> 每个运算符都作用于它之前已经准备好的两个操作数。栈顶正好保存最近得到的操作数或中间结果，因此可以逐步归约表达式，无须反复查找括号。

---

# 8. 递归与系统调用栈

## 8.1 什么是递归？

**递归**是函数直接或间接调用自身的过程。一个正确的递归算法通常包含：

- **递归出口**：规模足够小时直接给出结果，避免无限调用。
- **递归关系**：将当前问题转化为规模更小、结构相同的子问题。
- **规模递减**：每次递归都朝递归出口推进。

> [!danger] 缺少有效递归出口会导致调用不断加深
> 递归并不等于“函数里面再调用函数”这么简单。必须确保子问题规模会缩小，且存在可终止的基本情况，否则可能出现无限递归，最终耗尽调用栈空间。

## 8.2 为什么递归与栈有关？

一次函数调用通常需要保存参数、局部变量、返回地址以及恢复执行所需的信息。函数调用时，系统建立新的调用记录；函数返回时，移除当前调用记录。

```text
调用过程：先调用的函数在下面，后调用的函数在上面

┌────────────────────┐
│ main 的调用记录     │  最早调用
├────────────────────┤
│ functionA 的记录    │
├────────────────────┤
│ functionB 的记录    │  最近调用，当前正在执行
└────────────────────┘

返回过程：functionB → functionA → main
```

> [!important] 后调用先返回
> 函数嵌套调用遵循后进先出。递归每深入一层，就需要保留这一层的参数、局部状态和返回位置；递归返回时再逐层恢复。因此，理解递归的关键之一是跟踪**每一层调用的参数与返回时机**。

## 8.3 用递归改写循环

下面的循环依次输出 `n、n-1、...、2`：

```cpp
#include <iostream>
using namespace std;

void printDescending(int n) {
    if (n <= 1) {
        return;                 // n 小于等于 1 时停止递归
    }

    cout << n << ' ';           // 先输出当前值
    printDescending(n - 1);     // 再处理规模更小的子问题
}

int main() {
    printDescending(5);         // 输出 5 4 3 2
    cout << '\n';
    return 0;
}
```

## 8.4 用显式栈改写递归

若递归调用只是在逐层读取整数，遇到 `0` 后再从内层向外层累计，那么可以用一个显式栈保存递归过程中尚未处理的整数。

递归版本的行为是：读入一个数；若为 `0`，令总和为 `0`；否则递归读取下一个数，返回后再把当前数加到总和中并输出。非递归版本可先把所有非零输入压栈，读到 `0` 后从栈顶依次取出并累计。

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> values;         // 用 vector 尾部模拟显式栈
    int x;

    cout << "连续输入整数，以 0 结束：\n";
    while (cin >> x && x != 0) {
        values.push_back(x);    // 保存递归返回时还要处理的当前值
    }

    int sum = 0;                // 对应递归到达 x == 0 时的初始总和
    cout << sum << '\n';        // 最内层调用先输出 0

    while (!values.empty()) {
        sum += values.back();   // 取出最晚读入、最先返回处理的整数
        values.pop_back();
        cout << sum << '\n';   // 模拟每一层递归返回后的输出
    }
    return 0;
}
```

> [!note] 递归与非递归的关系
> 将递归改成非递归时，常常需要自己保存递归原本由系统调用栈保存的信息，例如参数、处理进度和返回后要执行的步骤。显式栈并不是唯一方法，但它是理解递归执行过程的直接方式。

---

# 9. 汉诺塔与 N 皇后

## 9.1 汉诺塔问题

有三根柱子 `X`、`Y`、`Z`，`X` 上有 `n` 个大小不同的圆盘。目标是把全部圆盘移动到 `Z`，移动过程中遵守：

1. 每次只能移动一个圆盘。
2. 每次只能移动某根柱子最上方的圆盘。
3. 任何时刻都不能把大圆盘放在小圆盘上面。

递归拆分：

1. 把上面的 `n-1` 个圆盘从 `X` 移到 `Y`，借助 `Z`。
2. 把第 `n` 个（最大的）圆盘从 `X` 移到 `Z`。
3. 把 `Y` 上的 `n-1` 个圆盘移到 `Z`，借助 `X`。

```cpp
#include <iostream>
using namespace std;

void moveDisk(int disk, char from, char to) {
    // 输出一次合法移动：把编号为 disk 的圆盘从 from 移到 to。
    cout << "移动圆盘 " << disk << "：" << from << " -> " << to << '\n';
}

void hanoi(int n, char from, char auxiliary, char to) {
    if (n == 1) {
        moveDisk(1, from, to);  // 只有一个圆盘时，直接移动即可
        return;                 // 基本情况：不再产生子调用
    }

    hanoi(n - 1, from, to, auxiliary); // 先把上方 n-1 个移到辅助柱
    moveDisk(n, from, to);             // 再移动当前最大的圆盘
    hanoi(n - 1, auxiliary, from, to);  // 最后把 n-1 个移到目标柱
}

int main() {
    int n;
    cout << "输入圆盘数量：";
    cin >> n;

    if (n <= 0) {
        cout << "圆盘数量必须为正数\n";
        return 1;
    }

    hanoi(n, 'X', 'Y', 'Z');    // 把 X 上的圆盘整体移动到 Z
    return 0;
}
```

设移动 `n` 个圆盘所需的最少移动次数为 `T(n)`，则：

$$
T(1)=1,\qquad T(n)=2T(n-1)+1
$$

因此：

$$
T(n)=2^n-1
$$

> [!tip] 跟踪递归调用
> 对 `hanoi(3, X, Y, Z)`，先执行 `hanoi(2, X, Z, Y)`，然后移动最大圆盘 `3`，最后执行 `hanoi(2, Y, X, Z)`。不要把三个参数的含义固定成某三根柱子；每次调用时，参数位置代表的角色会变化。

## 9.2 N 皇后问题

在 `n × n` 棋盘上放置 `n` 个皇后，使任意两个皇后都不在同一行、同一列或同一条对角线上。

可以按行逐个放置皇后。由于每一行恰好放一个皇后，只需记录每一行皇后的列号：`position[row] = col`。

新位置 `(row, col)` 合法，当且仅当它与所有已经放置的皇后都满足：

- 列号不同：`position[previousRow] != col`。
- 不在同一条对角线：`abs(position[previousRow] - col) != abs(previousRow - row)`。

```cpp
#include <cmath>
#include <iostream>
using namespace std;

const int MAX_N = 20;
int position[MAX_N];           // position[row] 保存该行皇后的列号
int solutionCount = 0;         // 统计找到的合法布局数量

bool canPlace(int row, int col) {
    for (int previousRow = 0; previousRow < row; previousRow++) {
        int previousCol = position[previousRow];

        if (previousCol == col) {
            return false;      // 同一列已有皇后
        }

        if (abs(previousRow - row) == abs(previousCol - col)) {
            return false;      // 行差等于列差，说明位于同一条对角线
        }
    }
    return true;
}

void solveQueens(int row, int n) {
    if (row == n) {
        solutionCount++;
        cout << "解 " << solutionCount << "：";
        for (int r = 0; r < n; r++) {
            cout << position[r] + 1 << ' '; // 输出时改成从 1 开始的列号
        }
        cout << '\n';
        return;                  // 当前布局完整，返回上一层继续搜索
    }

    for (int col = 0; col < n; col++) {
        if (canPlace(row, col)) {
            position[row] = col; // 试放当前行皇后
            solveQueens(row + 1, n); // 合法则继续放下一行
            // 返回后覆盖 position[row] 即可，相当于撤销当前选择
        }
    }
}

int main() {
    int n;
    cout << "输入皇后数量（1 到 " << MAX_N << "）：";
    cin >> n;

    if (n < 1 || n > MAX_N) {
        cout << "输入范围不合法\n";
        return 1;
    }

    solveQueens(0, n);           // 从第 0 行开始尝试
    cout << "合法布局总数：" << solutionCount << '\n';
    return 0;
}
```

> [!important] 回溯的三步
> **尝试一个选择 → 递归检查后续 → 返回后尝试下一个选择。**
>
> N 皇后通过逐行试放并检查冲突进行回溯；迷宫通过逐格探索并在走不通时退回；汉诺塔则利用规模更小的同类子问题完成任务。三者都涉及递归调用，但求解策略不同。

---

# 10. 队列的定义与基本操作

## 10.1 定义与术语

**队列（Queue）** 是只允许在一端插入、在另一端删除的线性表。

- **队头（front）**：删除元素的一端。
- **队尾（rear）**：插入元素的一端。
- **入队（EnQueue）**：在队尾添加元素。
- **出队（DeQueue）**：删除队头元素，并返回其值。
- **队空**：队列中没有数据元素。
- **队列下溢**：从空队列删除元素。
- **队列上溢**：固定容量的队列没有可用空间却仍要插入元素。

若元素按 `a1, a2, ..., an` 的顺序入队，出队时也只能按 `a1, a2, ..., an` 的顺序离开，因此队列是**先进先出（FIFO）**结构。

## 10.2 队列的基本操作

| 操作 | 作用 |
|---|---|
| `InitQueue` | 初始化空队列 |
| `DestroyQueue` | 销毁队列并释放资源 |
| `ClearQueue` | 清空队列元素 |
| `QueueEmpty` | 判断队列是否为空 |
| `QueueLength` | 返回队列长度 |
| `GetHead` | 读取队头元素但不删除 |
| `EnQueue` | 从队尾插入元素 |
| `DeQueue` | 从队头删除并返回元素 |
| `QueueTravers` | 从队头到队尾访问元素 |

> [!warning] 栈和队列的方向不能混淆
> - 栈：入栈和出栈都发生在栈顶。
> - 队列：入队发生在队尾，出队发生在队头。
>
> 对链队列而言，删除的是 `front->next` 指向的数据结点，而不是头结点本身。

---

# 11. 顺序队列与假溢出

## 11.1 普通顺序队列

顺序队列使用数组存储元素，并设置两个下标：

- `front` 指向当前队头元素。
- `rear` 指向下一个可插入位置。
- 初始化时 `front = rear = 0`。
- 队空条件为 `front == rear`。
- 入队后 `rear++`；出队后 `front++`。

```text
数组容量为 5，rear 指向下一个可插入位置

下标：  0    1    2    3    4
      ┌────┬────┬────┬────┬────┐
      │ A  │ B  │ C  │ D  │ E  │
      └────┴────┴────┴────┴────┘
       ↑                        ↑
     front=0                  rear=5（下一空位已越界）
```

## 11.2 线性顺序队列的完整实现

```cpp
#include <iostream>
using namespace std;

const int QUEUE_CAPACITY = 5;

struct LinearQueue {
    int data[QUEUE_CAPACITY];
    int front;                  // 指向当前队头元素
    int rear;                   // 指向下一个可插入位置
};

void initQueue(LinearQueue& q) {
    q.front = 0;
    q.rear = 0;                 // front == rear 表示空队列
}

bool isEmpty(const LinearQueue& q) {
    return q.front == q.rear;
}

bool enqueue(LinearQueue& q, int value) {
    if (q.rear == QUEUE_CAPACITY) {
        return false;           // 数组末尾没有下一个可写位置
    }

    q.data[q.rear] = value;     // 在队尾空位写入元素
    q.rear++;                   // 队尾指针后移
    return true;
}

bool dequeue(LinearQueue& q, int& value) {
    if (isEmpty(q)) {
        return false;           // 队空，不能删除
    }

    value = q.data[q.front];   // 读取队头元素
    q.front++;                 // 队头指针后移，逻辑上删除元素
    return true;
}

int main() {
    LinearQueue q;
    initQueue(q);

    enqueue(q, 10);
    enqueue(q, 20);
    enqueue(q, 30);
    enqueue(q, 40);
    enqueue(q, 50);             // 此时 rear == QUEUE_CAPACITY

    int value;
    dequeue(q, value);          // 删除 10，front 变为 1
    dequeue(q, value);          // 删除 20，front 变为 2

    // 逻辑上已经空出两个数组位置，但 rear 仍在数组末尾。
    if (!enqueue(q, 60)) {
        cout << "无法入队：普通顺序队列出现假溢出\n";
    }
    return 0;
}
```

## 11.3 什么是假溢出？

普通顺序队列中，出队只移动 `front`，不会自动把剩余元素搬到数组前面。多次出队后，数组前部可能已有空位，但 `rear` 已经到达数组末尾，新的元素仍无法插入。这种“数组尾部没有空间，但队列实际元素并未占满整个数组”的现象称为**假溢出**。

解决方法主要有两种：

1. 将已有元素整体左移，腾出队尾空间，但可能需要移动大量元素。
2. 把数组首尾连接起来，形成逻辑上的环，即使用循环队列。

> [!important] 为什么普通顺序队列不适合反复入队、出队？
> 因为 `front` 和 `rear` 只向后移动，不会循环利用已经释放的数组位置。循环队列通过取模运算解决这个问题。

---

# 12. 循环队列

## 12.1 循环队列的核心思想

循环队列仍使用数组，但把数组的最后一个位置视为紧邻第一个位置。指针移动时使用取模运算：

$$
rear=(rear+1)\bmod MAXQSIZE
$$

$$
front=(front+1)\bmod MAXQSIZE
$$

这样指针到达数组末尾后可以回到下标 `0`，重复使用已经出队的空间。

## 12.2 如何区分队空和队满？

若只使用 `front` 和 `rear` 两个指针，那么队空和队满都可能出现 `front == rear`，必须采用一种额外约定。

常见方法：

1. 增加标志位，记录上一次操作是入队还是出队。
2. **少用一个数组位置**：规定 `rear` 的下一个位置等于 `front` 时队满。

本文采用第二种方法：

- 队空：`front == rear`。
- 队满：`(rear + 1) % CAPACITY == front`。
- 可存储的最大元素数：`CAPACITY - 1`。

> [!important] 循环队列最重要的两个条件
> ```cpp
> front == rear                         // 队空
> (rear + 1) % CAPACITY == front        // 队满
> ```
> 队满公式中的 `rear + 1` 必须取模，否则队尾在数组最后一个位置时无法正确回到下标 `0`。

## 12.3 循环队列完整实现

```cpp
#include <iostream>
using namespace std;

const int QUEUE_CAPACITY = 6; // 实际最多保存 5 个元素，留一个空位区分队满

struct CircularQueue {
    int data[QUEUE_CAPACITY];
    int front;                 // 指向队头元素
    int rear;                  // 指向下一个可插入位置
};

void initQueue(CircularQueue& q) {
    q.front = 0;
    q.rear = 0;                // 两指针重合，表示队空
}

bool isEmpty(const CircularQueue& q) {
    return q.front == q.rear;
}

bool isFull(const CircularQueue& q) {
    // 队尾前进一步后若追上队头，说明只剩下用于区分状态的空位。
    return (q.rear + 1) % QUEUE_CAPACITY == q.front;
}

int queueLength(const CircularQueue& q) {
    // 取模处理队尾绕回数组开头的情况。
    return (q.rear - q.front + QUEUE_CAPACITY) % QUEUE_CAPACITY;
}

bool enqueue(CircularQueue& q, int value) {
    if (isFull(q)) {
        return false;          // 队满，不能覆盖队头元素
    }

    q.data[q.rear] = value;    // 在队尾位置写入新元素
    q.rear = (q.rear + 1) % QUEUE_CAPACITY; // 队尾循环后移
    return true;
}

bool dequeue(CircularQueue& q, int& value) {
    if (isEmpty(q)) {
        return false;          // 队空，不能出队
    }

    value = q.data[q.front];   // 读取当前队头元素
    q.front = (q.front + 1) % QUEUE_CAPACITY; // 队头循环后移
    return true;
}

bool getHead(const CircularQueue& q, int& value) {
    if (isEmpty(q)) {
        return false;
    }

    value = q.data[q.front];   // 只读取，不改变 front
    return true;
}

int main() {
    CircularQueue q;
    initQueue(q);

    for (int value = 10; value <= 50; value += 10) {
        enqueue(q, value);      // 依次入队 10、20、30、40、50
    }

    int value;
    dequeue(q, value);          // 删除 10，front 前进
    dequeue(q, value);          // 删除 20，front 再前进
    enqueue(q, 60);             // rear 可绕回数组前部复用空位
    enqueue(q, 70);

    cout << "当前队列长度：" << queueLength(q) << '\n';
    cout << "从队头到队尾：";
    while (dequeue(q, value)) {
        cout << value << ' ';   // 按入队先后顺序输出剩余元素
    }
    cout << '\n';
    return 0;
}
```

## 12.4 用下标跟踪循环队列

假设 `CAPACITY = 6`，有效数据容量为 5：

- 初始：`front = 0, rear = 0`，队空。
- 入队 10、20、30：数据写入下标 0、1、2，`rear = 3`。
- 出队两次：`front = 2`，队头变为 30。
- 再入队 40、50、60：当 `rear` 到达数组末尾后，会通过取模回到 0。
- 当 `(rear + 1) % 6 == front` 时，队满；不能再入队。

> [!warning] 容量不要算错
> 数组长度为 `6` 并不代表这种循环队列可以保存 `6` 个元素。为了用 `front == rear` 唯一表示队空，本文的约定始终保留一个空位，因此最大有效容量是 `5`。

---

# 13. 链队列

## 13.1 结构与空队列

链队列通过链表结点保存元素，并使用两个指针确定队列：

- `front` 指向头结点。
- `rear` 指向最后一个数据结点；空队列时也指向头结点。
- 头结点不保存有效数据，只用于简化插入和删除操作。
- 空队列条件：`front == rear`，同时 `front->next == nullptr`。

```text
空链队列：
front
  ↓
┌─────────┐
│ 头结点  │ ← rear
└────┬────┘
     ↓
   nullptr

非空链队列：
front                              rear
  ↓                                  ↓
┌─────────┐   ┌────┬────┐   ┌────┬────┐
│ 头结点  ├──→│ 10 │  ──┼──→│ 30 │null
└─────────┘   └────┴────┘   └────┴────┘
                  ↑
               队头数据
```

## 13.2 链队列完整实现

```cpp
#include <iostream>
#include <new>
using namespace std;

struct QueueNode {
    int data;           // 数据域，保存队列元素
    QueueNode* next;    // 指针域，指向下一个结点
};

struct LinkedQueue {
    QueueNode* front;   // 指向头结点，不直接指向队头数据结点
    QueueNode* rear;    // 指向最后一个数据结点；空队列时等于 front
};

bool initQueue(LinkedQueue& q) {
    q.front = new (nothrow) QueueNode;
    if (q.front == nullptr) {
        q.rear = nullptr;
        return false;              // 头结点申请失败，队列无法初始化
    }

    q.front->next = nullptr;       // 头结点后面暂时没有数据结点
    q.rear = q.front;              // 空队列时，头尾指针指向同一结点
    return true;
}

bool isEmpty(const LinkedQueue& q) {
    return q.front == q.rear;      // 没有数据结点时头尾指针重合
}

bool enqueue(LinkedQueue& q, int value) {
    QueueNode* node = new (nothrow) QueueNode;
    if (node == nullptr) {
        return false;              // 申请失败，原队列保持不变
    }

    node->data = value;
    node->next = nullptr;          // 新结点将成为最后一个结点
    q.rear->next = node;           // 原队尾指向新结点
    q.rear = node;                 // 更新队尾指针
    return true;
}

bool dequeue(LinkedQueue& q, int& value) {
    if (isEmpty(q)) {
        return false;              // 空队列没有可删除的数据结点
    }

    QueueNode* oldHead = q.front->next; // 第一个数据结点才是队头
    value = oldHead->data;              // 先保存队头数据
    q.front->next = oldHead->next;      // 头结点越过原队头，接上后继

    if (q.rear == oldHead) {
        q.rear = q.front;          // 原队列只有一个元素，删除后恢复为空
    }

    delete oldHead;                // 释放已删除的数据结点
    return true;
}

void destroyQueue(LinkedQueue& q) {
    QueueNode* current = q.front;
    while (current != nullptr) {
        QueueNode* nextNode = current->next; // 释放前先保存后继地址
        delete current;
        current = nextNode;
    }

    q.front = nullptr;             // 清除已经失效的头指针
    q.rear = nullptr;              // 清除已经失效的尾指针
}

int main() {
    LinkedQueue q;
    if (!initQueue(q)) {
        cout << "初始化失败\n";
        return 1;
    }

    enqueue(q, 10);
    enqueue(q, 20);
    enqueue(q, 30);

    int value;
    while (dequeue(q, value)) {
        cout << value << ' ';      // 输出 10 20 30，体现先进先出
    }
    cout << '\n';

    destroyQueue(q);               // 释放头结点及所有剩余结点
    return 0;
}
```

## 13.3 链队列最容易出错的地方

> [!important] 删除队头时要单独处理“只剩一个元素”的情况
> 假设队列只有一个数据结点 `p`，此时 `rear == p`。删除 `p` 后，队列变空，必须把 `rear` 重新指向头结点：
>
> ```cpp
> q.front->next = oldHead->next;
> if (q.rear == oldHead) {
>     q.rear = q.front;
> }
> delete oldHead;
> ```
>
> 如果忘记更新 `rear`，它就会指向已经释放的结点。之后再入队时访问 `rear->next` 会造成未定义行为。

## 13.4 循环队列与链队列比较

| 比较项 | 循环队列 | 链队列 |
|---|---|---|
| 存储方式 | 固定数组 | 动态链表结点 |
| 空间是否连续 | 是 | 不要求连续 |
| 容量 | 数组长度固定；本文约定下可存 `容量 - 1` 个元素 | 受可用内存限制 |
| 入队 / 出队 | `O(1)` | `O(1)`，前提是已有头尾指针 |
| 额外开销 | 需要处理循环下标和队满规则 | 每个数据结点有指针域，并需动态分配、释放 |
| 常见问题 | 队空、队满条件混淆 | 忘记更新尾指针、内存管理错误 |

---

# 14. k 阶斐波那契序列与循环队列

## 14.1 递推关系

k 阶斐波那契序列可定义为：

$$
f_0=f_1=\cdots=f_{k-2}=0,\qquad f_{k-1}=1
$$

从第 `k` 项开始，每一项等于前面 `k` 项之和：

$$
f_n=f_{n-1}+f_{n-2}+\cdots+f_{n-k}
$$

把相邻两项的递推式相减，可以得到更适合循环更新的公式：

$$
f_{i+1}=2f_i-f_{i-k}
$$

这个公式的含义是：下一项等于当前项的两倍，再减去窗口中即将被移出的一项。因此，可以用容量为 `k+1` 的循环数组保留必要的历史项，更新时不必每次重新累加全部 `k` 项。

> [!note] 为什么循环队列适合这类问题？
> 计算新项时只需要最近的若干项，较早的项不再需要。循环数组可以重复使用固定的存储位置，避免不断移动数组中的元素。

## 14.2 用循环数组生成 k 阶斐波那契序列

下面的示例假定 `k >= 2`、`max >= 1`，并输出所有不超过 `max` 的项。为了保留最近 `k` 项，使用长度为 `k` 的循环数组；每次先求出窗口中 `k` 项之和，再覆盖最旧的一项。代码用 `long long` 保存求和中间值，避免 `int` 加法在比较 `max` 之前就溢出；存入窗口的项仍不超过 `max`，因此可安全转换为 `int`。

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int k, maxValue;
    cout << "输入阶数 k（k >= 2）和上限 max（max >= 1）：";
    cin >> k >> maxValue;

    if (k < 2 || maxValue < 1) {
        cout << "输入范围不合法\n";
        return 1;
    }

    vector<int> ring(k, 0);     // 循环数组保存最近 k 项
    ring[k - 1] = 1;             // 初始项为 0,0,...,0,1
    int rear = k - 1;             // rear 指向窗口中最新的一项
    int index = k - 1;            // 当前最新项的序号

    cout << "不超过上限的序列项：";
    for (int i = 0; i < k - 1; i++) {
        cout << 0 << ' ';         // 输出初始的 k-1 个零
    }
    cout << 1 << ' ';             // 输出 f[k-1]

    while (true) {
        long long nextValue = 0;
        for (int i = 0; i < k; i++) {
            nextValue += ring[i]; // 当前窗口中的 k 项相加得到下一项
        }

        if (nextValue > maxValue) {
            break;                // 下一项超出上限，停止生成
        }

        rear = (rear + 1) % k;    // 指向最旧项所在的位置并循环移动
        ring[rear] = static_cast<int>(nextValue); // 用新项覆盖最旧项
        index++;
        cout << ring[rear] << ' ';
    }
    cout << '\n';

    cout << "窗口中最后保留的 k 项（从旧到新）：";
    int oldest = (rear + 1) % k;  // rear 的下一个位置是窗口最旧项
    for (int i = 0; i < k; i++) {
        cout << ring[(oldest + i) % k] << ' ';
    }
    cout << '\n';
    cout << "最后一项的序号：" << index << '\n';
    return 0;
}
```

> [!warning] 序列项可能快速增长
> 如果上限很大，必须考虑整数溢出。上面的程序用 `long long` 计算中间和，并在新项不超过 `maxValue` 后才将其存入 `int` 窗口。若修改数据类型或上限，应重新检查溢出风险。


## 14.3 优化更新：用 k+1 个位置实现差分递推

若使用

$$
f_{i+1}=2f_i-f_{i-k}
$$

计算下一项，只需要知道当前项 `f_i` 和即将被窗口淘汰的旧项 `f_{i-k}`。因此，可以用长度为 `k+1` 的循环数组保存最近 `k+1` 项：`rear` 指向当前项，`(rear + 1) % (k + 1)` 指向下一次将被覆盖的最旧项。

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int k, maxValue;
    cout << "输入阶数 k（k >= 2）和上限 max（max >= 1）：";
    cin >> k >> maxValue;

    if (k < 2 || maxValue < 1) {
        cout << "输入范围不合法\n";
        return 1;
    }

    vector<int> ring(k + 1, 0); // 长度为 k+1，保留差分公式需要的历史项
    ring[k - 1] = 1;            // f[k-1] = 1
    ring[k] = 1;                // f[k] = 1，是初始项之后的第一项
    int rear = k;               // rear 指向当前最新项 f[k]
    int index = k;              // 当前最新项的序号

    cout << "不超过上限的序列项：";
    for (int i = 0; i < k - 1; i++) {
        cout << 0 << ' ';       // 输出 f[0] 到 f[k-2]
    }
    cout << 1 << ' ' << 1 << ' '; // 输出 f[k-1] 和 f[k]

    while (true) {
        int oldest = (rear + 1) % (k + 1); // 即将被覆盖的最旧项 f[i-k]
        long long nextValue = 2LL * ring[rear] - ring[oldest];
        // 使用 long long 计算中间结果，避免乘 2 时先发生 int 溢出。
        if (nextValue > maxValue) {
            break;              // 下一项超过上限，不再写入循环数组
        }

        ring[oldest] = static_cast<int>(nextValue); // 用新项覆盖最旧项
        rear = oldest;          // 新项成为当前最新项
        index++;
        cout << ring[rear] << ' ';
    }
    cout << '\n';

    cout << "循环数组中保留的 k+1 项（从旧到新）：";
    int oldest = (rear + 1) % (k + 1);
    for (int i = 0; i < k + 1; i++) {
        cout << ring[(oldest + i) % (k + 1)] << ' ';
    }
    cout << '\n';
    cout << "最后一项的序号：" << index << '\n';
    return 0;
}
```

> [!tip] 两种循环数组算法如何选择？
> - **长度为 `k`**：每次把窗口中的 `k` 项全部相加，思路直观，适合先理解递推定义。
> - **长度为 `k+1`**：利用 `f(i+1) = 2f(i) - f(i-k)`，每次只做常数次算术运算，减少重复求和。
>
> 两种方法都要正确维护循环下标，并在计算下一项后先检查上限，再决定是否更新窗口。

---

# 15. 栈和队列综合比较

## 15.1 结构特征对比

| 维度 | 栈 | 队列 |
|---|---|---|
| 操作限制 | 只能在栈顶插入和删除 | 队尾插入、队头删除 |
| 顺序原则 | 后进先出 LIFO | 先进先出 FIFO |
| 主要操作 | `Push`、`Pop`、`GetTop` | `EnQueue`、`DeQueue`、`GetHead` |
| 顺序存储常见实现 | 固定 / 动态顺序栈 | 普通顺序队列、循环队列 |
| 链式存储常见实现 | 链栈 | 链队列 |
| 典型应用 | 回溯、括号匹配、表达式、递归调用 | 排队处理、任务缓冲、滑动窗口、循环序列 |

## 15.2 如何选择？

> [!tip] 根据数据的处理顺序选择结构
> - 如果最新加入的元素需要最先处理，考虑栈。
> - 如果最早加入的元素需要最先处理，考虑队列。
> - 如果数据量固定且希望使用连续空间，可考虑数组实现。
> - 如果元素数量变化大，且不便预估容量，可考虑链式实现。
> - 如果队列需要反复出队、入队并持续复用数组空间，应考虑循环队列。

## 15.3 常见操作的复杂度

| 结构 | 操作 | 时间复杂度 |
|---|---|---:|
| 固定顺序栈 | 入栈、出栈、取栈顶 | `O(1)` |
| 链栈 | 入栈、出栈、取栈顶 | `O(1)` |
| 循环队列 | 入队、出队、取队头 | `O(1)` |
| 链队列 | 入队、出队、取队头 | `O(1)` |
| 栈 / 队列遍历 | 访问全部元素 | `O(n)` |
| 汉诺塔 | 输出全部移动步骤 | `O(2^n)` |
| N 皇后 | 回溯搜索 | 最坏情况下呈指数级增长，实际取决于剪枝效果 |

> [!note] 复杂度的前提
> 链栈和链队列的入栈、出栈、入队、出队均假设已经有相应的栈顶或头尾指针。若先要遍历链表寻找位置，复杂度就可能上升到 `O(n)`。

---

# 16. 易错点与典型练习

## 16.1 高频易错点

> [!danger] 错误 1：把栈顶指针的含义混在一起
> 如果 `top` 表示元素个数，栈顶下标就是 `top - 1`；如果 `top` 表示当前栈顶下标，则空栈常用 `-1` 表示。两种写法不能混搭。

> [!danger] 错误 2：出栈时先读错下标
> 对“下一空位式”顺序栈，应先 `top--`，再读取 `data[top]`；读取 `data[top]` 后才减 1，会访问下一个空位。

> [!danger] 错误 3：括号匹配只比较数量
> 左右括号数量相等不代表嵌套正确。必须将最近尚未匹配的左括号保存在栈顶，并与当前右括号比较。

> [!danger] 错误 4：后缀表达式运算顺序颠倒
> 计算 `a - b` 时，先弹出的值是 `b`，后弹出的是 `a`。弹出顺序和运算顺序并不相同。

> [!danger] 错误 5：循环队列队满条件少写取模
> 正确条件为 `(rear + 1) % CAPACITY == front`。若不取模，队尾从数组最后一个位置回到开头时会判断错误。

> [!danger] 错误 6：忘记链队列只剩一个元素时更新 rear
> 删除唯一数据结点后，必须令 `rear = front`，使空队列的头尾指针重新重合。

> [!danger] 错误 7：递归只有调用，没有有效终止条件
> 递归函数必须明确基本情况，并保证递归规模朝基本情况缩小。分析时还要区分“递归深入时执行的语句”和“递归返回后执行的语句”。

## 16.2 练习一：判断括号是否配对

**要求：** 判断输入表达式中的 `()`、`[]`、`{}` 是否正确配对。普通字符不影响结果，括号允许任意嵌套。

**解题思路：** 使用左括号栈。遇到左括号就入栈；遇到右括号就检查栈顶；类型不匹配或栈为空时立即失败；最后栈必须为空。

参考实现见“5.2 括号匹配”。该算法扫描每个字符一次，时间复杂度为 `O(n)`，最坏情况下栈空间为 `O(n)`。

## 16.3 练习二：把递归过程改为非递归过程

**要求：** 反复读取整数，遇到 `0` 停止；从停止点开始，按递归返回的顺序逐层累加并输出累计值。

**解题思路：** 将每次读到的非零整数压栈。读到 `0` 后，令总和为 `0` 并先输出；然后依次弹出栈中整数并累加，模拟递归函数逐层返回的过程。

参考实现见“8.4 用显式栈改写递归”。若输入为 `1 2 3 0`，输出的累计值依次为 `0、3、5、6`。

## 16.4 练习三：分析汉诺塔的调用顺序

**要求：** 写出 `hanoi(3, 'X', 'Y', 'Z')` 的递归调用结构，并计算最少移动次数。

**解题思路：** 每次调用按“移动 `n-1` 个到辅助柱 → 移动最大盘 → 移动 `n-1` 个到目标柱”的顺序执行。移动次数满足 `T(n) = 2T(n-1) + 1`，因此 `T(3) = 7`。

## 16.5 练习四：循环队列状态判断

**要求：** 循环数组容量为 `8`，采用保留一个空位的队满判断方法。写出队空、队满条件，并求最大可存元素数。

**答案：**

- 队空：`front == rear`。
- 队满：`(rear + 1) % 8 == front`。
- 最大可存元素数：`8 - 1 = 7`。

## 16.6 练习五：k 阶斐波那契序列

**要求：** 给定 `k` 和上限 `max`，生成不超过 `max` 的 k 阶斐波那契序列，并用循环数组保留最近 `k` 项。

**解题思路：** 每次将窗口中的 `k` 项相加得到下一项；若超过上限就停止，否则让循环下标前进一格并覆盖最旧的一项。若使用差分公式 `f(i+1) = 2f(i) - f(i-k)`，则需要准确确认下标对应的“当前项”和“即将移出的旧项”。

参考实现见“14.2 用循环数组生成 k 阶斐波那契序列”。

---

> [!summary] 本章最终速记
> **栈：LIFO，同一端进出。**
>
> - 下一空位式顺序栈：空 `top == 0`，满 `top == capacity`，入栈后 `top++`，出栈先 `top--`。
> - 链栈：新结点先指向原栈顶，再更新栈顶指针。
> - 栈的典型应用：数制转换、括号匹配、行编辑、迷宫回溯、表达式处理、递归、汉诺塔、N 皇后。
>
> **队列：FIFO，队尾入队、队头出队。**
>
> - 普通顺序队列可能出现假溢出。
> - 保留一个空位的循环队列：空 `front == rear`，满 `(rear + 1) % capacity == front`，有效容量为数组长度减 1。
> - 链队列：通常带头结点；删除唯一数据结点后要令 `rear = front`。
>
> **做题时优先检查：空 / 满条件、指针更新顺序、递归出口、运算数弹出顺序和数组边界。**
