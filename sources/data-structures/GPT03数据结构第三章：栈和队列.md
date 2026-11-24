# 第三章　栈和队列

> [!abstract] 学习定位
> 栈与队列都是**运算受限制的线性表**，本章不仅要记住 LIFO、FIFO，还要能够跟踪每一次插入、删除、数组下标移动、链指针修改以及递归调用栈的变化。对于“执行过程”，每组插图都是按实际算法状态重新绘制的，不是将文字塞进框中。

## 1. 栈和队列究竟限制了什么

在线性表中，可以在许多合法位置插入或删除元素。栈把**插入、删除**都约束在同一端，队列则在**队尾插入、队头删除**。因此，二者的区别不在于底层是数组还是链表，而在于操作规则。

| 比较项目 | 栈（Stack） | 队列（Queue） |
|---|---|---|
| 数据组织原则 | 后进先出，LIFO | 先进先出，FIFO |
| 插入位置 | 栈顶 `top` | 队尾 `rear` |
| 删除位置 | 栈顶 `top` | 队头 `front` |
| 典型场景 | 撤销、括号、表达式、递归、回溯 | 任务排队、缓冲、广度优先处理 |

![960](./_assets/2a3ad6e332/ds3_stack_queue_order_49238055-29b4-431e-94ed-5dfbd317ce64.svg)

*图 155　栈和队列对比。*


> [!important] 一个贯穿全章的区别
> **逻辑结构**只描述允许执行哪些操作；**存储结构**决定操作在内存中怎样实现。顺序栈、链栈的出栈次序相同；循环队列、链队列的出队次序也相同。

---

## 2. 栈：定义、基本运算与出栈序列

### 2.1 栈的定义

设栈从栈底到栈顶为 $S=(a_1,a_2,\ldots,a_n)$。$a_1$ 是最先进入的元素，$a_n$ 是当前栈顶。只允许在 $a_n$ 一端执行 `Push` 和 `Pop`。

- `InitStack`：构造空栈。
- `DestroyStack`：销毁栈的存储资源。
- `ClearStack`：清空元素，保留可复用的栈对象。
- `StackLength`：返回元素个数。
- `StackEmpty`：判断是否为空。
- `GetTop`：只读取栈顶，不删除。
- `Push`：将一个元素压入栈顶。
- `Pop`：删除并返回栈顶元素。
- `StackTraverse`：按照指定顺序访问元素。

这些名称用于表达抽象数据类型的接口，实际 C++ 可使用 `std::stack` 或自行封装。

### 2.2 出栈序列不是输入序列的任意排列

假定输入顺序固定为 `1 → 2 → 3`。每次只能压入**下一个尚未输入的元素**，或者弹出当前栈顶。例如输出 `2,3,1` 可行，过程是 `Push(1), Push(2), Pop(2), Push(3), Pop(3), Pop(1)`。输出 `3,1,2` 则不可能：要先弹出 3，就必须先把 1、2 压在它下面，而弹完 3 后，2 必先于 1 出栈。

![960](./_assets/2a3ad6e332/ds3_stack_permutation_1_91f46c49-10e9-49f3-b343-41783d73ccf1.svg)

*图 1　出栈 [2, 3, 1]。*

![960](./_assets/2a3ad6e332/ds3_stack_permutation_2_f5de8589-4299-4693-b36c-c2a87038ea3c.svg)

*图 2　出栈 [1, 2, 3]。*

![960](./_assets/2a3ad6e332/ds3_stack_permutation_3_9e6381c1-b40c-4f18-9cce-cfddf15a99cd.svg)

*图 3　出栈 [3, 2, 1]。*


> [!tip] 判断出栈序列的通用办法
> 按要求输出的序列逐个检查：如果栈顶不是所需元素，就把后续输入元素依次压栈；若所有元素已经输入，栈顶仍不匹配，则该出栈序列不可能。

## 3. 顺序栈：把抽象操作落实为数组变化

### 3.1 `top` 两种含义必须分清

教材展示过两套顺序栈表示法，最常见的区别是 `top` 的含义。

- **约定 A：指向当前栈顶元素的下标。** 空栈 `top=-1`；压栈执行 `data[++top]=x`；出栈执行 `x=data[top--]`。
- **约定 B：指向栈顶之后的下一个空位置。** 空栈 `top=0`（或指针 `top=base`）；压栈执行 `data[top++]=x`；出栈执行 `x=data[--top]`。

![960](./_assets/2a3ad6e332/ds3_top_convention_0_4c84010b-82ed-41dc-9067-73413b3421f8.svg)

*图 4　top 指向栈顶元素。*

![960](./_assets/2a3ad6e332/ds3_top_convention_1_46abf014-8c9d-4d0e-bdac-fcaaec4bf478.svg)

*图 5　top 指向下一个空位。*


> [!warning] 容易混淆的细节
> 这两套约定都正确，但同一段算法**不能混用**。教材顺序栈的部分片段中采用 `top=-1`，另一部分采用 `top=base`，判断空栈和操作自增、自减时一定先确认所处的实现。

### 3.2 顺序栈九步连续操作

以容量为 8 的数组为例，观察 `top` 怎样跟随 `Push / Pop / GetTop` 移动。图片中的数组编号从 0 开始，`top=-1` 表示不存在栈顶元素。

![960](./_assets/2a3ad6e332/ds3_sequential_stack_01_73839710-e26f-4e2c-8dc2-20610b59deef.svg)

*图 6　初始化。*

![960](./_assets/2a3ad6e332/ds3_sequential_stack_02_fb5535a9-4eb9-4382-99be-049ec78a662f.svg)

*图 7　Push(A)。*

![960](./_assets/2a3ad6e332/ds3_sequential_stack_03_e8a6f0d7-8ef2-4f64-8a89-87c7221cc980.svg)

*图 8　Push(B)。*

![960](./_assets/2a3ad6e332/ds3_sequential_stack_04_a0da9199-c2e5-407f-b937-b868bcc7670b.svg)

*图 9　Push(C)。*

![960](./_assets/2a3ad6e332/ds3_sequential_stack_05_bb5a8706-9f73-4688-adb8-fc81f6050c19.svg)

*图 10　GetTop。*

![960](./_assets/2a3ad6e332/ds3_sequential_stack_06_f4950b74-ca9b-49a5-ac32-d1701a028f57.svg)

*图 11　Pop → C。*

![960](./_assets/2a3ad6e332/ds3_sequential_stack_07_3440c829-12a2-42ae-8625-7ec704345f7c.svg)

*图 12　Pop → B。*

![960](./_assets/2a3ad6e332/ds3_sequential_stack_08_2b4c191b-97ef-46a8-902d-275dc5dbd755.svg)

*图 13　Pop → A。*

![960](./_assets/2a3ad6e332/ds3_sequential_stack_09_6bd1fb4f-e173-43a7-a138-0064019679df.svg)

*图 14　再次 Pop（下溢）。*


> [!important] 顺序栈的复杂度
> 对于固定容量顺序栈，只修改一个数组单元及栈顶下标，`Push`、`Pop`、`GetTop` 都是 $O(1)$；若采用动态扩容数组，单次扩容可能是 $O(n)$，但按倍增扩容可获得均摊 $O(1)$ 压栈。

### 3.3 固定容量顺序栈的 C++ 实现

```cpp
#include <array>

class SeqStack {
private:
    std::array<int, 100> data{};  // 固定容量 100
    int top = -1;                 // top 指向栈顶元素

public:
    bool empty() const {
        return top == -1;
    }

    bool full() const {
        return top == 99;
    }

    int size() const {
        return top + 1;
    }

    bool push(int x) {
        if (full()) return false; // 防止数组越界
        data[++top] = x;          // 先修改 top，再写数据
        return true;
    }

    bool pop(int& x) {
        if (empty()) return false;
        x = data[top--];          // 先读取，再移动 top
        return true;
    }

    bool getTop(int& x) const {
        if (empty()) return false;
        x = data[top];            // 不改变 top
        return true;
    }
};
```

**上溢**表示固定容量栈已满还企图入栈；**下溢**表示空栈仍企图出栈。它们是操作前置条件不满足，而不等于“机器突然没有内存”。

## 4. 链栈：为什么入栈必须先连接旧栈顶

链栈通常让 `top` 指向第一个实际数据结点，不必专门设置头结点。链栈插入新元素就是**链表头插法在栈顶位置上的应用**；出栈就是删除第一个实际结点。

### 4.1 入栈与出栈的逐指针轨迹

1. 创建新结点 `p` 并填写 `p->data=x`。
2. 执行 `p->next=top`，先把新结点连接到旧链表。
3. 执行 `top=p`，再让栈顶指向新结点。
4. 弹栈时先令 `p=top` 保存旧栈顶，再 `top=top->next`，取值后释放 `p`。

![960](./_assets/2a3ad6e332/ds3_linked_stack_01_4e14a21f-941c-4475-a11c-28edd8b7bf12.svg)

*图 15　空链栈。*

![960](./_assets/2a3ad6e332/ds3_linked_stack_02_9b9809f9-41d9-4433-93ce-575e373dd7b1.svg)

*图 16　申请新结点 p。*

![960](./_assets/2a3ad6e332/ds3_linked_stack_03_b39c3c30-a10b-42be-b0a4-0cdd688581e2.svg)

*图 17　p->next=top。*

![960](./_assets/2a3ad6e332/ds3_linked_stack_04_93fb40cc-98b3-4112-8823-3bdd29cfe449.svg)

*图 18　top=p。*

![960](./_assets/2a3ad6e332/ds3_linked_stack_05_8e963ccd-0876-4247-819d-4d9cc0fe443c.svg)

*图 19　准备 Pop。*

![960](./_assets/2a3ad6e332/ds3_linked_stack_06_54d0372d-2dde-41e7-94dd-a8539ac72ac8.svg)

*图 20　top=top->next。*

![960](./_assets/2a3ad6e332/ds3_linked_stack_07_8685bb4e-268b-4d13-97e3-31421fbee669.svg)

*图 21　取值并释放 p。*


> [!danger] 指针顺序写反会丢链
> 不能先令 `top=p` 再写 `p->next=top`，否则新结点可能指向自己，旧栈顶链条丢失。删除结点时也不能先 `delete top` 再读 `top->next`，那会访问已释放的内存。

### 4.2 链栈的核心 C++ 代码

```cpp
struct Node {
    int data;
    Node* next;
};

bool push(Node*& top, int x) {
    Node* p = new Node{x, top};  // p->next 先指向旧 top
    top = p;                     // top 再改为新结点
    return true;
}

bool pop(Node*& top, int& x) {
    if (top == nullptr) return false;
    Node* p = top;               // 保存旧栈顶
    x = p->data;                 // 读取待删除的数据
    top = p->next;               // 保留其余结点的入口
    delete p;                    // 安全释放旧栈顶
    return true;
}

void clear(Node*& top) {
    int ignored;
    while (pop(top, ignored)) {  // 逐一回收结点
    }
}
```

链栈一般没有预先规定的固定最大容量，但仍可能因内存分配失败无法入栈。每次操作仅修改少量指针，因此时间复杂度为 $O(1)$。

---

## 5. 栈的应用一：进制转换——为什么余数要逆序

对于整数 $N$ 和目标进制 $d$，有

$$N=(N\operatorname{div}d)\times d+N\bmod d.$$

不断取余、整除，所得余数从**最低位到最高位**产生；数字的书写顺序正相反，所以用栈逆转余数。

例如将 $1348_{10}$ 转成八进制：

| 当前值 $N$ | 商 $N\operatorname{div}8$ | 余数 $N\bmod8$ |
|---:|---:|---:|
| 1348 | 168 | 4 |
| 168 | 21 | 0 |
| 21 | 2 | 5 |
| 2 | 0 | 2 |

![960](./_assets/2a3ad6e332/ds3_base_division_01_73a15408-170b-463a-bcee-acf6639444f4.svg)

*图 22　余数 4 入栈。*

![960](./_assets/2a3ad6e332/ds3_base_division_02_96bb9df1-8b21-46e5-9a97-8e8395ec9804.svg)

*图 23　余数 0 入栈。*

![960](./_assets/2a3ad6e332/ds3_base_division_03_f8603048-4c9c-4f04-94e2-7fa2181fd165.svg)

*图 24　余数 5 入栈。*

![960](./_assets/2a3ad6e332/ds3_base_division_04_c224dd33-6ad1-4dfb-8fbc-e316be5c3164.svg)

*图 25　余数 2 入栈。*

![960](./_assets/2a3ad6e332/ds3_base_output_09d76cf7-b1a0-4145-9e80-c4c556c4856d.svg)

*图 156　余数逆序输出。*


```cpp
#include <string>
#include <vector>
#include <algorithm>

std::string toBase(unsigned int n, unsigned int base) {
    const std::string digits = "0123456789ABCDEF";
    if (base < 2 || base > 16) return "";
    if (n == 0) return "0";
    std::string result;
    while (n > 0) {
        result.push_back(digits[n % base]); // 低位先产生
        n /= base;
    }
    std::reverse(result.begin(), result.end()); // 模拟逆序出栈
    return result;
}
```

这里用反转字符串演示与栈等价的逆序输出逻辑；也可以将余数放入 `std::stack<int>` 再逐个弹出。

## 6. 栈的应用二：括号匹配

核心规则是：遇左括号压栈；遇右括号时，它只能与**当前栈顶**的左括号配对。扫描结束时，栈必须为空。错误有三种：右括号多余、类型不匹配、左括号遗留。

### 6.1 逐字符处理 `[([])]`

![960](./_assets/2a3ad6e332/ds3_brackets_01_4f0a830a-0b9b-48ca-b02e-b53658c38476.svg)

*图 26　处理 [。*

![960](./_assets/2a3ad6e332/ds3_brackets_02_3bb80a5d-229d-43b8-899d-b78e46855e07.svg)

*图 27　处理 (。*

![960](./_assets/2a3ad6e332/ds3_brackets_03_885d0d34-bd2f-422e-9820-7435a4b183dd.svg)

*图 28　处理 [。*

![960](./_assets/2a3ad6e332/ds3_brackets_04_a724a45f-9fb8-43af-861d-127e0d3ac9a3.svg)

*图 29　处理 ]。*

![960](./_assets/2a3ad6e332/ds3_brackets_05_06f5e0f0-f68e-410d-a016-8b24c77420a6.svg)

*图 30　处理 )。*

![960](./_assets/2a3ad6e332/ds3_brackets_06_c618cde6-478b-41dc-9c38-01494c1f7f27.svg)

*图 31　处理 ]。*


```cpp
#include <stack>
#include <string>

bool bracketsValid(const std::string& s) {
    std::stack<char> st;
    for (char ch : s) {
        if (ch == '(' || ch == '[' || ch == '{') {
            st.push(ch);
        } else if (ch == ')' || ch == ']' || ch == '}') {
            if (st.empty()) return false;             // 右括号多余
            char open = st.top();
            st.pop();
            if (ch == ')' && open != '(') return false;
            if (ch == ']' && open != '[') return false;
            if (ch == '}' && open != '{') return false;
        }
    }
    return st.empty();                                // 排除左括号多余
}
```

> [!example] 匹配判断
> `[(])` 错在类型嵌套不匹配；`())` 错在多余右括号；`(([])` 错在左括号未配完。算法的时间复杂度为 $O(n)$，辅助空间最坏为 $O(n)$。

## 7. 栈的应用三：行编辑中的删除与撤销

课程约定输入字符 `#` 表示退格，`@` 表示**清空当前行**。正常字符入栈，输入 `#` 弹出一个字符；输入 `@` 清空缓冲栈。文本最终从栈底至栈顶构成有效内容。

### 7.1 字符序列的逐次处理

![960](./_assets/2a3ad6e332/ds3_line_editor_01_d819ece7-345c-45d7-90a5-9832c416d6f6.svg)

*图 32　读入 w。*

![960](./_assets/2a3ad6e332/ds3_line_editor_02_b63fb720-2a7b-4780-b1c9-fceb3c5829e5.svg)

*图 33　读入 h。*

![960](./_assets/2a3ad6e332/ds3_line_editor_03_9de7a155-bf3e-471f-a483-29d50c360119.svg)

*图 34　读入 l。*

![960](./_assets/2a3ad6e332/ds3_line_editor_04_30620213-9dbe-49e8-b5f5-d9497a8f9e58.svg)

*图 35　读入 i。*

![960](./_assets/2a3ad6e332/ds3_line_editor_05_22c8fb27-60b7-4e3b-bedc-6852ec272db4.svg)

*图 36　读入 #。*

![960](./_assets/2a3ad6e332/ds3_line_editor_06_7794434c-6135-405b-aa40-de8e8b14e7af.svg)

*图 37　读入 #。*

![960](./_assets/2a3ad6e332/ds3_line_editor_07_32ecc98a-f717-48e6-acd0-8d542633ea7b.svg)

*图 38　读入 i。*

![960](./_assets/2a3ad6e332/ds3_line_editor_08_87bce3c3-b341-4967-9561-9d26eff0f25f.svg)

*图 39　读入 l。*

![960](./_assets/2a3ad6e332/ds3_line_editor_09_f2114813-8cad-4fa1-88f0-c1551c1f7f71.svg)

*图 40　读入 r。*

![960](./_assets/2a3ad6e332/ds3_line_editor_10_83986885-20ef-464f-a700-504adb00a54a.svg)

*图 41　读入 #。*

![960](./_assets/2a3ad6e332/ds3_line_editor_11_3ada6e78-36aa-4794-b9e2-f366429b884b.svg)

*图 42　读入 e。*


```cpp
#include <string>

std::string editLine(const std::string& input) {
    std::string buffer;             // 使用字符串尾部模拟栈顶
    for (char ch : input) {
        if (ch == '#') {
            if (!buffer.empty()) buffer.pop_back();
        } else if (ch == '@') {
            buffer.clear();
        } else {
            buffer.push_back(ch);
        }
    }
    return buffer;
}
```

> [!note] 例子与约定
> `ab#c` 的有效内容是 `ac`；`abc@xy` 的有效内容是 `xy`。`#`、`@` 是这一行编辑问题的自定义指令，不是现代编辑器普遍使用的文本语法。

## 8. 栈的应用四：迷宫回溯不是在“随意试路线”

典型**深度优先搜索（DFS）**总是沿一条当前可行路径尽量向前。当碰到无路可走时，利用栈回到最近一个还存在未试方向的位置。课程中的方向可按东、南、西、北依次尝试：

1. **入栈**：当前格可通行、未访问，把格子及下一候选方向记入路径栈。
2. **继续探路**：按固定的方向顺序试探下一个格子。
3. **回溯**：当前格的四个方向都试过，弹出该格，回到栈顶前驱。
4. **结束**：抵达出口则得到路径；栈空仍未抵达出口则无路可达。

下面是按照真实 DFS 状态逐帧生成的迷宫和调用路径，而不是随机画一条线。

![960](./_assets/2a3ad6e332/ds3_maze_01_09f30328-049c-404d-a15b-7f93cd4ecaac.svg)

*图 43　迷宫搜索 1。*

![960](./_assets/2a3ad6e332/ds3_maze_02_8438fa0b-dd40-43cc-8b12-001171ae74e2.svg)

*图 44　迷宫搜索 2。*

![960](./_assets/2a3ad6e332/ds3_maze_03_9038fc73-6e11-4919-9bab-6a66a32fc930.svg)

*图 45　迷宫搜索 3。*

![960](./_assets/2a3ad6e332/ds3_maze_04_82105697-83eb-4171-95fb-20a6fa58ff78.svg)

*图 46　迷宫搜索 4。*

![960](./_assets/2a3ad6e332/ds3_maze_05_421791a6-def8-4151-9df2-8836a704622e.svg)

*图 47　迷宫搜索 5。*

![960](./_assets/2a3ad6e332/ds3_maze_06_45394552-15a2-4c30-9469-ba9fc9a7e16a.svg)

*图 48　迷宫搜索 6。*

![960](./_assets/2a3ad6e332/ds3_maze_07_7709e16e-ca98-4ce0-80f0-b578aa23d014.svg)

*图 49　迷宫搜索 7。*

![960](./_assets/2a3ad6e332/ds3_maze_08_6d182fab-b88d-4494-addc-a89154482059.svg)

*图 50　迷宫搜索 8。*

![960](./_assets/2a3ad6e332/ds3_maze_11_340346b7-2f81-4c41-b42c-9849c9f472da.svg)

*图 51　迷宫搜索 11。*

![960](./_assets/2a3ad6e332/ds3_maze_12_ab6b6542-d4fa-444a-af35-629464d16292.svg)

*图 52　迷宫搜索 12。*


> [!warning] “搜索访问过”与“最终路径”不同
> 死胡同在搜索时确实被访问过，但回溯后不会留在最终路径栈中。绘图用不同颜色标出当前路径与确认死路，不能把所有访问过的格子误认为答案路径。

```cpp
#include <vector>
#include <string>

struct Point { int r, c; };

bool findPath(const std::vector<std::string>& maze,
              int sr, int sc, int er, int ec,
              std::vector<Point>& path) {
    const int dr[4] = {0, 1, 0, -1}; // 东、南、西、北
    const int dc[4] = {1, 0, -1, 0};
    int rows = static_cast<int>(maze.size());
    if (rows == 0) return false;
    int cols = static_cast<int>(maze[0].size());
    std::vector<std::vector<bool>> used(rows, std::vector<bool>(cols, false));

    auto dfs = [&](auto&& self, int r, int c) -> bool {
        if (r < 0 || r >= rows || c < 0 || c >= cols) return false;
        if (maze[r][c] == '#' || used[r][c]) return false;
        used[r][c] = true;
        path.push_back({r, c});        // 相当于压入路径栈
        if (r == er && c == ec) return true;
        for (int d = 0; d < 4; ++d) {
            if (self(self, r + dr[d], c + dc[d])) return true;
        }
        path.pop_back();               // 四路不通，回溯
        return false;
    };
    path.clear();
    return dfs(dfs, sr, sc);
}
```

代码采用**递归调用栈 + 显式路径向量**来表达与教材迭代回溯等价的思想：调用栈保留“下一步尝试哪个方向”的信息，`path` 则保存仍在当前路线上的格子。为简化代码，假设迷宫各行等宽、起终点下标合法。

## 9. 栈的应用五：算符优先与双工作栈

求值 `4+2*3-10/5`，必须遵守“先括号、再乘除、后加减；同一优先级从左至右”的运算规则。

课程采用两个工作栈：

- **OPTR**：运算符栈，保存尚未完成计算的运算符。
- **OPND**：操作数栈，保存数字和中间结果。

读入操作数时直接压 OPND；读入运算符时比较其与 OPTR 栈顶的优先级。若栈顶运算符优先级不低于当前运算符，则先从 OPND 依次弹出右操作数 `b`、左操作数 `a`，计算 `a op b`，再将结果压回 OPND。若为左括号，先压入 OPTR；遇右括号，则规约到左括号，并弹出成对括号。

### 9.1 双栈真实状态变化

![960](./_assets/2a3ad6e332/ds3_expression_01_e13f0e3c-4209-4b37-a48e-121a4972b212.svg)

*图 53　读入操作数 4。*

![960](./_assets/2a3ad6e332/ds3_expression_02_a54cdd96-3e41-47d2-a6d8-d70f7581771a.svg)

*图 54　运算符 + 入 OPTR。*

![960](./_assets/2a3ad6e332/ds3_expression_03_2c2e3e62-9a78-4dd2-bfef-6727146a149e.svg)

*图 55　读入操作数 2。*

![960](./_assets/2a3ad6e332/ds3_expression_04_121efdef-102b-484c-8fda-298ee65d4915.svg)

*图 56　运算符 * 入 OPTR。*

![960](./_assets/2a3ad6e332/ds3_expression_05_cc98201a-5311-4a35-9031-769c357822ab.svg)

*图 57　读入操作数 3。*

![960](./_assets/2a3ad6e332/ds3_expression_06_e905be00-fcb1-4fb1-88ea-423befdd97e0.svg)

*图 58　计算 2*3=6。*

![960](./_assets/2a3ad6e332/ds3_expression_07_437d299d-561b-4d05-9fdd-67f1d3d4ecce.svg)

*图 59　计算 4+6=10。*

![960](./_assets/2a3ad6e332/ds3_expression_08_96893754-295f-4ead-8fa3-4314af60c228.svg)

*图 60　运算符 - 入 OPTR。*

![960](./_assets/2a3ad6e332/ds3_expression_09_a13eb0f1-0ea5-4f66-b7b1-6de033c2d443.svg)

*图 61　读入操作数 10。*

![960](./_assets/2a3ad6e332/ds3_expression_10_25e0665f-20bb-45a3-8098-46727cad3d06.svg)

*图 62　运算符 / 入 OPTR。*

![960](./_assets/2a3ad6e332/ds3_expression_11_6a479aba-0b2b-4073-ad2e-499784af929b.svg)

*图 63　读入操作数 5。*

![960](./_assets/2a3ad6e332/ds3_expression_12_63559432-bb4f-433c-a681-bc01c0e42567.svg)

*图 64　计算 10/5=2。*

![960](./_assets/2a3ad6e332/ds3_expression_13_a7035936-2de4-44cf-8b65-11cc29e6cb92.svg)

*图 65　计算 10-2.0=8。*


> [!important] 为什么弹出的顺序很重要
> 对 `a-b` 和 `a/b`，从操作数栈中**第一个弹出的是右操作数** `b`，第二个才是左操作数 `a`。把顺序颠倒会产生错误的计算结果。这个例题最终结果为 $4+6-2=8$。

### 9.2 前缀、中缀与后缀表达式

以 `a*b+(c-d/e)*f` 为例：

| 表示方式 | 表达式 |
|---|---|
| 前缀 | `+ * a b * - c / d e f` |
| 中缀 | `a * b + (c - d / e) * f` |
| 后缀 | `a b * c d e / - f * +` |

后缀表达式不需要括号就能确定运算次序。从左到右扫描：数字压栈；遇运算符，弹出两个数计算，再把结果压栈。

### 9.3 后缀式逐符号求值

对应本章前面的数值例题，后缀式是 `4 2 3 * + 10 5 / -`。

![960](./_assets/2a3ad6e332/ds3_postfix_01_be9419d4-e604-4a6f-b07f-bc0d764c2cec.svg)

*图 66　后缀处理 4。*

![960](./_assets/2a3ad6e332/ds3_postfix_02_52d67053-dab6-41c9-beb1-93d3aea7a69e.svg)

*图 67　后缀处理 2。*

![960](./_assets/2a3ad6e332/ds3_postfix_03_d0b47eb2-64c7-490c-ba57-eb6023c5d35b.svg)

*图 68　后缀处理 3。*

![960](./_assets/2a3ad6e332/ds3_postfix_04_56714c4b-6a52-4677-9ca3-e009915d60f0.svg)

*图 69　后缀处理 *。*

![960](./_assets/2a3ad6e332/ds3_postfix_05_28c57d23-950d-4943-980e-116cf865f22e.svg)

*图 70　后缀处理 +。*

![960](./_assets/2a3ad6e332/ds3_postfix_06_6c3dbb48-2399-4e2e-a9f5-bc07164221b1.svg)

*图 71　后缀处理 10。*

![960](./_assets/2a3ad6e332/ds3_postfix_07_2d553ea4-3ed8-4994-9c23-93b60b43794a.svg)

*图 72　后缀处理 5。*

![960](./_assets/2a3ad6e332/ds3_postfix_08_8f6037c0-b047-4ba3-bbcb-43105ec7a728.svg)

*图 73　后缀处理 /。*

![960](./_assets/2a3ad6e332/ds3_postfix_09_ddb4530d-77db-444e-a3a7-448607cecde5.svg)

*图 74　后缀处理 -。*


```cpp
#include <stack>
#include <vector>
#include <string>
#include <stdexcept>

int evalPostfix(const std::vector<std::string>& tokens) {
    std::stack<int> nums;
    for (const std::string& t : tokens) {
        if (t != "+" && t != "-" && t != "*" && t != "/") {
            nums.push(std::stoi(t));
            continue;
        }
        if (nums.size() < 2) throw std::invalid_argument("缺少操作数");
        int b = nums.top(); nums.pop(); // 先弹右操作数
        int a = nums.top(); nums.pop(); // 后弹左操作数
        int result = 0;
        if (t == "+") result = a + b;
        if (t == "-") result = a - b;
        if (t == "*") result = a * b;
        if (t == "/") {
            if (b == 0) throw std::domain_error("除数为零");
            result = a / b;             // 本例只演示整除结果
        }
        nums.push(result);
    }
    if (nums.size() != 1) throw std::invalid_argument("表达式不完整");
    return nums.top();
}
```

> [!warning] 教学代码的适用范围
> 此程序用整数类型，除法按 C++ 整数除法执行；不负责把包含括号的中缀表达式切成多位数 token，也没有处理一元负号。表达式求值的通用解析器还需要词法分析与运算符合法性检查。

## 10. 栈的应用六：递归调用记录与汉诺塔

递归中的“栈”是**程序运行时的调用栈**。一次函数调用都要保留当前参数、局部变量、返回地址等；当被调用函数返回，最新的调用记录先移除，因此仍然是后进先出。

### 10.1 逐层进入、逐层返回

![960](./_assets/2a3ad6e332/ds3_recursion_frame_01_53c1e5c7-6d4a-4a1b-b590-f902859de2cb.svg)

*图 75　递归层 1。*

![960](./_assets/2a3ad6e332/ds3_recursion_frame_02_f9b193ad-7d8b-470d-8b7b-24d4aec3bb0b.svg)

*图 76　递归层 2。*

![960](./_assets/2a3ad6e332/ds3_recursion_frame_03_e3999070-7680-4f97-8ead-d05d4e576dc9.svg)

*图 77　递归层 3。*

![960](./_assets/2a3ad6e332/ds3_recursion_frame_04_d0bb07db-2d5a-4b7b-b5e4-4a8952e21e81.svg)

*图 78　递归层 4。*

![960](./_assets/2a3ad6e332/ds3_recursion_frame_05_411ae6c5-98ab-4875-8f04-f06ace63df10.svg)

*图 79　递归层 5。*


> [!important] 递归的两个方向
> 进入递归时规模逐步缩小；递归触底后才逐级返回。不同层次的局部变量即使同名，也分别存于自己的调用记录。递归层数过大可能导致调用栈溢出。

### 10.2 汉诺塔三步分治

移动 $n$ 个圆盘，从 `X` 经 `Y` 移至 `Z`，规则是一次只能移动一个盘，且大盘不能压小盘。对于 $n>1$：

1. 把上面 $n-1$ 个盘从 `X` 移到 `Y`，暂借 `Z`。
2. 把底部第 $n$ 个盘从 `X` 移到 `Z`。
3. 把 $n-1$ 个盘从 `Y` 移到 `Z`，暂借 `X`。

于是 $T(n)=2T(n-1)+1$，由 $T(1)=1$ 得

$$T(n)=2^n-1.$$

### 10.3 三层汉诺塔全部七步

![960](./_assets/2a3ad6e332/ds3_hanoi_01_3dc391ba-5d16-4b4f-8256-13bebce08480.svg)

*图 80　移动 1 0->2。*

![960](./_assets/2a3ad6e332/ds3_hanoi_02_f11ad4ab-0888-40ef-9dfd-cb16d131cbf6.svg)

*图 81　移动 2 0->1。*

![960](./_assets/2a3ad6e332/ds3_hanoi_03_feb486f4-2688-4efb-8d8a-da6d41c2c304.svg)

*图 82　移动 1 2->1。*

![960](./_assets/2a3ad6e332/ds3_hanoi_04_f152af59-7881-4668-8433-46484a4abc4f.svg)

*图 83　移动 3 0->2。*

![960](./_assets/2a3ad6e332/ds3_hanoi_05_26cbc29d-cb53-41b5-ac0b-833b7d77b6d0.svg)

*图 84　移动 1 1->0。*

![960](./_assets/2a3ad6e332/ds3_hanoi_06_48277c53-018b-42e1-95c5-cee327411fe9.svg)

*图 85　移动 2 1->2。*

![960](./_assets/2a3ad6e332/ds3_hanoi_07_d31d165c-43e7-4f9e-b4ab-17f3662cb996.svg)

*图 86　移动 1 0->2。*


```cpp
#include <iostream>

void hanoi(int n, char from, char aux, char to) {
    if (n <= 0) return;
    hanoi(n - 1, from, to, aux);
    std::cout << "移动圆盘 " << n << ": " << from << " -> " << to << '\n';
    hanoi(n - 1, aux, from, to);
}
```

递归深度为 $O(n)$，总移动次数为 $2^n-1$。其中两次子问题调用分别具有不同的辅助塔座次序，不能简单交换参数。

## 11. 栈的应用七：N 皇后与回溯

在 $n\times n$ 棋盘上放置 $n$ 个皇后，使任意两个皇后不在同一行、同一列或同一斜线上。可以按行递归放置：每进入新的一层，只尝试本行的每一列；发现冲突就换列，所有列都失败就回上一行更换位置。

若一行至多放一个皇后，只需记录每行皇后的列坐标 $x_i$。对已放置的第 $i$、$j$ 行皇后，合法条件为

$$x_i\neq x_j,\qquad |x_i-x_j|\neq |i-j|.$$

### 11.1 四皇后尝试、冲突与回溯的连续过程

![960](./_assets/2a3ad6e332/ds3_queens_01_50e86461-0a74-4b65-94d2-075edb19cde0.svg)

*图 87　回溯 尝试。*

![960](./_assets/2a3ad6e332/ds3_queens_02_e1631044-112d-43ba-b7bf-33985c74cb16.svg)

*图 88　回溯 放置。*

![960](./_assets/2a3ad6e332/ds3_queens_03_c53f9986-0b90-4eaa-9885-77717d78133d.svg)

*图 89　回溯 冲突。*

![960](./_assets/2a3ad6e332/ds3_queens_04_8127ad5d-c2c5-4480-8abe-54c208e612b0.svg)

*图 90　回溯 冲突。*

![960](./_assets/2a3ad6e332/ds3_queens_05_c8965e04-046d-4de4-a378-c6224f1c5b46.svg)

*图 91　回溯 尝试。*

![960](./_assets/2a3ad6e332/ds3_queens_06_678de403-4fa1-436e-ad02-60e0d9b12d25.svg)

*图 92　回溯 放置。*

![960](./_assets/2a3ad6e332/ds3_queens_07_8ee47065-5783-4b76-b570-a16bfbd993bf.svg)

*图 93　回溯 冲突。*

![960](./_assets/2a3ad6e332/ds3_queens_08_1b1212d7-aefd-47b7-82dd-58f9788da4c7.svg)

*图 94　回溯 冲突。*

![960](./_assets/2a3ad6e332/ds3_queens_09_6518c4a8-e579-4108-94df-69bb7459e1e3.svg)

*图 95　回溯 冲突。*

![960](./_assets/2a3ad6e332/ds3_queens_10_07bd1332-9b98-47ba-b386-c71675f68def.svg)

*图 96　回溯 冲突。*

![960](./_assets/2a3ad6e332/ds3_queens_11_b13b2ccb-5705-42d5-95bd-e62ea07b7e73.svg)

*图 97　回溯 回溯。*

![960](./_assets/2a3ad6e332/ds3_queens_12_ecc36f95-a457-4b04-9dc2-b95fa570393b.svg)

*图 98　回溯 尝试。*

![960](./_assets/2a3ad6e332/ds3_queens_13_f8547c19-ac55-44ae-81c0-61df7cff29b4.svg)

*图 99　回溯 放置。*

![960](./_assets/2a3ad6e332/ds3_queens_14_be1f02ee-8edc-477d-95be-f6540c9bcf6a.svg)

*图 100　回溯 冲突。*

![960](./_assets/2a3ad6e332/ds3_queens_15_fb923525-3f3e-4c1a-a630-8937333a3035.svg)

*图 101　回溯 尝试。*

![960](./_assets/2a3ad6e332/ds3_queens_16_0f32f5f6-5cc5-4561-a36c-eca54e65f87d.svg)

*图 102　回溯 放置。*

![960](./_assets/2a3ad6e332/ds3_queens_17_c6a684d8-b98d-4d5f-83ae-0dcc7e853e28.svg)

*图 103　回溯 冲突。*

![960](./_assets/2a3ad6e332/ds3_queens_18_42e8cee6-db21-4a14-811b-df13bf76e747.svg)

*图 104　回溯 冲突。*

![960](./_assets/2a3ad6e332/ds3_queens_19_fe771d7b-71e1-4153-a2ab-513637341ed0.svg)

*图 105　回溯 冲突。*

![960](./_assets/2a3ad6e332/ds3_queens_20_5b07e233-0dbe-48d8-90a0-a2f379e109ae.svg)

*图 106　回溯 冲突。*

![960](./_assets/2a3ad6e332/ds3_queens_21_cd23387f-2c8f-4408-a35d-a60197499854.svg)

*图 107　回溯 回溯。*

![960](./_assets/2a3ad6e332/ds3_queens_22_4204289c-a088-4845-8de9-4b42594f2a52.svg)

*图 108　回溯 冲突。*

![960](./_assets/2a3ad6e332/ds3_queens_23_4fd552e9-ea2e-48fa-aa1f-3ceb7bdd415f.svg)

*图 109　回溯 冲突。*

![960](./_assets/2a3ad6e332/ds3_queens_solution_1_c680ac25-2012-4d98-a1c3-c4967372ed12.svg)

*图 110　解 1。*

![960](./_assets/2a3ad6e332/ds3_queens_solution_2_50ab7f45-b70b-4a84-89bf-6f745273d869.svg)

*图 111　解 2。*


```cpp
#include <vector>
#include <cstdlib>

void solveQueens(int n, int row,
                 std::vector<int>& col,
                 std::vector<std::vector<int>>& answers) {
    if (row == n) {
        answers.push_back(col);             // 保存一个完整布局
        return;
    }
    for (int c = 0; c < n; ++c) {
        bool valid = true;
        for (int r = 0; r < row; ++r) {
            if (col[r] == c || std::abs(col[r] - c) == row - r) {
                valid = false;
                break;
            }
        }
        if (!valid) continue;
        col.push_back(c);                  // 进入下一层递归
        solveQueens(n, row + 1, col, answers);
        col.pop_back();                   // 回溯，恢复本层状态
    }
}
```

> [!note] 复杂度
> 回溯算法实际搜索数量依赖剪枝效果。简单按行枚举的搜索树上界可用 $O(n!)$ 量级估计，不等于每种输入都实际检查 $n!$ 个完整棋盘。

---

## 12. 队列的定义与基本操作

队列规定新元素只能从 `rear` 一端进入，旧元素只能从 `front` 一端退出。定义 $Q=(a_1,a_2,\ldots,a_n)$ 时，$a_1$ 是队头，$a_n$ 是队尾。

常用的抽象操作包括 `InitQueue`、`DestroyQueue`、`QueueEmpty`、`QueueLength`、`GetHead`、`ClearQueue`、`EnQueue`、`DeQueue` 和 `QueueTraverse`。其中 `GetHead` 读取但不删除队头；`DeQueue` 则真正使队头离开队列。

## 13. 普通顺序队列为什么会发生“假溢出”

数组长度为 8，约定 `front` 指向**当前队头数据**，`rear` 指向**下一可入队位置**。初始 `front=rear=0`。入队使 `rear++`，出队使 `front++`。

若先放入 `A,B,C,D,E`，再出队 `A,B,C`，数组的前 3 个槽已经空闲，但 `rear` 仍在较右的位置。继续添加新元素直到 `rear=8` 后，即使前面的槽空着，仍无法直接入队；这是**假溢出**而不是真正占满了所有存储空间。

![960](./_assets/2a3ad6e332/ds3_linear_queue_01_c41e0d66-4994-410d-be20-dace978005c1.svg)

*图 112　初始化。*

![960](./_assets/2a3ad6e332/ds3_linear_queue_02_3b9f81b7-e56e-4388-b7ca-a16860cb5ba2.svg)

*图 113　依次入队 A,B,C,D,E。*

![960](./_assets/2a3ad6e332/ds3_linear_queue_03_deb244c1-be15-4f17-8138-c4cae7851550.svg)

*图 114　A,B,C 出队。*

![960](./_assets/2a3ad6e332/ds3_linear_queue_04_f6a19a2a-c672-4407-a137-bd2d77c8cc07.svg)

*图 115　再入队 F,G,H。*

![960](./_assets/2a3ad6e332/ds3_linear_queue_05_5ae0fa20-14f9-4bfe-a0c8-4b218c62462f.svg)

*图 116　尝试入队 I 被拒绝。*

![960](./_assets/2a3ad6e332/ds3_linear_queue_06_854f8301-75cf-4a90-b67a-383cabfed8ee.svg)

*图 117　D 到 H 全出队。*


> [!warning] 逻辑空与物理数组仍有旧数据不是一回事
> 队列逻辑为空的条件是 `front==rear`。数组曾经存放的旧字符是否被清零，与它们是否属于队列无关。

## 14. 循环队列：空间复用与取模运算

把数组首尾视为相连的环，入队、出队时分别执行

$$rear=(rear+1)\bmod N,\qquad front=(front+1)\bmod N.$$

这里 $N$ 是物理数组长度。若仅凭 `front==rear`，可能同时代表“刚入满绕回”与“队空”，因此必须补充约定。

### 14.1 两种可行的判满方案

**方案一：额外保存状态。** 可记录最近一次操作类型或独立元素个数；例如维护 `count`，空为 `count==0`，满为 `count==N`。

**方案二：牺牲一个数组槽位。** 令 `front==rear` 表示空，`(rear+1)%N==front` 表示满。实际最多存 $N-1$ 个元素。这是课堂重点方案。

![960](./_assets/2a3ad6e332/ds3_one_space_vs_count_210b0a6f-703d-4a23-8c75-9a27264f5113.svg)

*图 157　判满方案对比。*

![960](./_assets/2a3ad6e332/ds3_circular_full_empty_0_dc417cdf-816c-4a7e-9861-4a0372d6d2d8.svg)

*图 118　队空：front=rear，逻辑长度为 0。*

![960](./_assets/2a3ad6e332/ds3_circular_full_empty_1_f1fefb26-274c-40db-a948-3162f1b0ef5d.svg)

*图 119　队满：rear 的下一个位置恰好等于 front。*


### 14.2 14 帧环绕入队与出队演示

下面的圆形每格对应**真实数组下标**，不是抽象环形装饰。`front` 标记即将出队的元素位置，`rear` 标记下一次可以写入的位置。颜色变化与下标取模结果一致。

![960](./_assets/2a3ad6e332/ds3_circular_queue_01_0323a845-97d3-434e-8879-fc461cd6c6e8.svg)

*图 120　初始。*

![960](./_assets/2a3ad6e332/ds3_circular_queue_02_284c4578-258b-45fb-a4ee-6b0b7b1581e8.svg)

*图 121　入队 A。*

![960](./_assets/2a3ad6e332/ds3_circular_queue_03_dc46114b-e650-4c77-99c9-2a7ff0d8b5eb.svg)

*图 122　入队 B。*

![960](./_assets/2a3ad6e332/ds3_circular_queue_04_0b7730c5-ef79-4719-bc08-19545179bb3c.svg)

*图 123　入队 C。*

![960](./_assets/2a3ad6e332/ds3_circular_queue_05_17fa32da-16d7-495d-aa0b-022071e08cca.svg)

*图 124　入队 D。*

![960](./_assets/2a3ad6e332/ds3_circular_queue_06_ef19e9c4-8438-4ba1-9778-0ecdbfa1951a.svg)

*图 125　入队 E。*

![960](./_assets/2a3ad6e332/ds3_circular_queue_07_9b9e3ed8-3a89-4e08-a1f7-94496775c6a0.svg)

*图 126　出队 A。*

![960](./_assets/2a3ad6e332/ds3_circular_queue_08_b4972948-d8b7-4d88-8d08-90c1cd840524.svg)

*图 127　出队 B。*

![960](./_assets/2a3ad6e332/ds3_circular_queue_09_f01ea7f6-b413-476a-83e6-9fbeb933c9e4.svg)

*图 128　入队 F。*

![960](./_assets/2a3ad6e332/ds3_circular_queue_10_f8480c5c-241e-4c1d-83e0-fa93299b9c93.svg)

*图 129　入队 G。*

![960](./_assets/2a3ad6e332/ds3_circular_queue_11_86ab49e3-667f-4539-a5e7-32be60dfc331.svg)

*图 130　入队 H。*

![960](./_assets/2a3ad6e332/ds3_circular_queue_12_ca70df20-9a5a-4be2-9a10-942afb8a9738.svg)

*图 131　入队 I。*

![960](./_assets/2a3ad6e332/ds3_circular_queue_13_6d72cd13-80fa-43e5-bd6d-0424156226a6.svg)

*图 132　尝试入队 J（队满）。*

![960](./_assets/2a3ad6e332/ds3_circular_queue_14_a9b5b259-a824-4b90-8463-dcf8721575c0.svg)

*图 133　出队 C。*


### 14.3 预留一格法的完整 C++ 实现

```cpp
#include <array>

class CircularQueue {
private:
    static constexpr int CAP = 8;
    std::array<int, CAP> data{};
    int front = 0;               // 指向当前队头
    int rear = 0;                // 指向下一个入队位置

public:
    bool empty() const {
        return front == rear;
    }

    bool full() const {
        return (rear + 1) % CAP == front;
    }

    int size() const {
        return (rear - front + CAP) % CAP;
    }

    bool enqueue(int x) {
        if (full()) return false;
        data[rear] = x;          // 先写再移动 rear
        rear = (rear + 1) % CAP;
        return true;
    }

    bool dequeue(int& x) {
        if (empty()) return false;
        x = data[front];         // 先读再移动 front
        front = (front + 1) % CAP;
        return true;
    }
};
```

> [!tip] 做循环队列计算题的固定流程
> 先写物理容量 $N$、当前 `front`/`rear`，判断操作合法性，再根据操作更新其中一个指针，**每一步都取模**。千万不要在“未预留空位的队列”和“预留一格的队列”之间混用判满公式。

## 15. 链队列：入队要改两个位置，删除最后一个元素更要谨慎

教材采用**带头结点的链队列**。`front` 指向头结点，`rear` 指向实际队尾结点；空队列时二者都指向头结点，头结点的 `next` 为 `nullptr`。

### 15.1 入队步骤

1. 创建新结点 `p`，令 `p->data=x`、`p->next=nullptr`。
2. 原尾结点的 `next` 指向 `p`：`rear->next=p`。
3. 更新 `rear=p`。

### 15.2 出队步骤

1. 先用 `p=front->next` 记住第一个实际数据结点。
2. 更新 `front->next=p->next`，从链中越过 `p`。
3. 如果 `rear==p`，说明删除的是**唯一数据结点**，必须让 `rear=front`。
4. 读取并释放 `p`。

### 15.3 13 帧指针前后状态图

![960](./_assets/2a3ad6e332/ds3_linked_queue_01_5fb6c082-ec34-412a-8223-a10f6b740e6a.svg)

*图 134　初始空队列。*

![960](./_assets/2a3ad6e332/ds3_linked_queue_02_9c51aa9c-c1e7-4612-aec5-c4d82f3f8d8b.svg)

*图 135　EnQueue(A) · 分配新结点。*

![960](./_assets/2a3ad6e332/ds3_linked_queue_03_8ab47099-2740-4620-8960-0b9da2e0a64b.svg)

*图 136　EnQueue(A) · 链接结点。*

![960](./_assets/2a3ad6e332/ds3_linked_queue_04_f97486be-a014-4aac-9450-11574db53833.svg)

*图 137　EnQueue(A) · 移动尾指针。*

![960](./_assets/2a3ad6e332/ds3_linked_queue_05_d5be0390-06c5-4cec-b13a-0a6b93f8f995.svg)

*图 138　EnQueue(B) · 准备。*

![960](./_assets/2a3ad6e332/ds3_linked_queue_06_9c917ac2-2db0-4565-b33b-923a44d29c02.svg)

*图 139　EnQueue(B) · 完成。*

![960](./_assets/2a3ad6e332/ds3_linked_queue_07_4b814653-45a0-40c5-a9db-d21211c7f2ee.svg)

*图 140　DeQueue(A) · 定位。*

![960](./_assets/2a3ad6e332/ds3_linked_queue_08_c7610433-0750-4dab-9460-3ff30c732710.svg)

*图 141　DeQueue(A) · 越过 A。*

![960](./_assets/2a3ad6e332/ds3_linked_queue_09_ce73dab0-20c3-458a-8353-3156678bd2e2.svg)

*图 142　DeQueue(A) · 释放。*

![960](./_assets/2a3ad6e332/ds3_linked_queue_10_716b7a4b-a55e-4cd5-a949-a3915659d501.svg)

*图 143　DeQueue(B) · 定位。*

![960](./_assets/2a3ad6e332/ds3_linked_queue_11_e35804ad-f191-4d4f-b293-799e23ae8efd.svg)

*图 144　DeQueue(B) · 越过 B。*

![960](./_assets/2a3ad6e332/ds3_linked_queue_12_01953281-5629-4776-935e-58448fcb122b.svg)

*图 145　DeQueue(B) · 修正 rear。*

![960](./_assets/2a3ad6e332/ds3_linked_queue_13_a0aabd28-351f-4c5d-9284-4cd73a5238b3.svg)

*图 146　DeQueue(B) · 释放。*


> [!danger] 最后一个结点出队时的致命遗漏
> 如果仅写 `front->next=p->next; delete p;`，而忘记 `rear=front`，`rear` 就指向已释放的内存。之后再入队执行 `rear->next=p` 会产生未定义行为。这也是链队列区别于普通链表删除操作的高频考点。

### 15.4 链队列 C++ 核心实现

```cpp
struct QueueNode {
    int data;
    QueueNode* next;
};

class LinkedQueue {
private:
    QueueNode* front;
    QueueNode* rear;

public:
    LinkedQueue() {
        front = new QueueNode{0, nullptr}; // 只作头结点
        rear = front;
    }

    ~LinkedQueue() {
        int x;
        while (dequeue(x)) {             // 释放所有实际数据结点
        }
        delete front;                    // 最后释放头结点
    }

    LinkedQueue(const LinkedQueue&) = delete;
    LinkedQueue& operator=(const LinkedQueue&) = delete;

    bool empty() const {
        return front == rear;
    }

    void enqueue(int x) {
        QueueNode* p = new QueueNode{x, nullptr};
        rear->next = p;                  // 先链接
        rear = p;                        // 再更新尾指针
    }

    bool dequeue(int& x) {
        if (empty()) return false;
        QueueNode* p = front->next;      // 指向首元结点
        x = p->data;
        front->next = p->next;           // 越过待删除结点
        if (rear == p) rear = front;     // 删除唯一元素时修正尾指针
        delete p;
        return true;
    }
};
```

该实现用头结点统一了“空队列”和“非空队列”的插入逻辑；为了避免浅拷贝引发重复释放，明确禁止复制。全部操作 $O(1)$。

## 16. 课堂综合应用：用循环队列保存 $k$ 阶斐波那契最近 $k$ 项

设 $k\ge2$，初始值及递推式为

$$f_0=f_1=\cdots=f_{k-2}=0,\quad f_{k-1}=1,$$

$$f_n=f_{n-1}+f_{n-2}+\cdots+f_{n-k}\qquad(n\ge k).$$

仅需最近的 $k$ 项即可计算下一项；把最旧的元素从队首逻辑移除，再把新元素写到它占过的位置。由于**窗口始终恰有 $k$ 项**，可以用循环数组配合一个 `start` 下标和固定 `count=k`，而不是使用“预留一格判满”的队列方案。

### 16.1 以 $k=3$ 为例逐次更新

![960](./_assets/2a3ad6e332/ds3_fibonacci_01_45a6adcb-b0cd-49ce-b3fa-22c0f2c8ac57.svg)

*图 147　第 1 次滑动。*

![960](./_assets/2a3ad6e332/ds3_fibonacci_02_580191b8-bed5-43cc-8f41-c607bce969a7.svg)

*图 148　第 2 次滑动。*

![960](./_assets/2a3ad6e332/ds3_fibonacci_03_73e0293d-7fab-4235-8df1-f6d88ccd9ba4.svg)

*图 149　第 3 次滑动。*

![960](./_assets/2a3ad6e332/ds3_fibonacci_04_d595c1a8-a1fd-480e-9740-24037ca328ef.svg)

*图 150　第 4 次滑动。*

![960](./_assets/2a3ad6e332/ds3_fibonacci_05_23a56508-cf9d-49ad-9569-c402509d7623.svg)

*图 151　第 5 次滑动。*

![960](./_assets/2a3ad6e332/ds3_fibonacci_06_87ad21de-d62d-4b37-afd2-61afa8aae5b7.svg)

*图 152　第 6 次滑动。*

![960](./_assets/2a3ad6e332/ds3_fibonacci_07_67b125cf-918c-471c-b96f-c79d529ce485.svg)

*图 153　第 7 次滑动。*

![960](./_assets/2a3ad6e332/ds3_fibonacci_08_44f5d620-3343-49b5-997b-0c0a1028481f.svg)

*图 154　第 8 次滑动。*


由相邻递推式相减还可得到

$$f_{n+1}=2f_n-f_{n-k},$$

这在使用滚动窗口时可作为更新与核验的另一种形式，但应保证相应下标上的旧值在覆盖前已经保存。

```cpp
#include <vector>
#include <stdexcept>
#include <climits>

// 返回 f_0 ... f_n 中最后的 k 项，满足 f_n<=limit, f_(n+1)>limit。
std::vector<long long> lastKTerms(int k, long long limit) {
    if (k < 2 || limit < 1) throw std::invalid_argument("参数范围非法");
    std::vector<long long> ring(k, 0);
    ring[k - 1] = 1;                    // f_(k-1)=1
    int oldest = 0;                    // 环形窗口的最旧项下标
    long long windowSum = 1;           // 当前 k 项之和 = 下一项
    while (windowSum <= limit) {
        long long next = windowSum;
        long long old = ring[oldest];   // 先保存即将被覆盖的值
        ring[oldest] = next;
        oldest = (oldest + 1) % k;      // 窗口向前移动
        if (windowSum > LLONG_MAX - next + old) {
            throw std::overflow_error("递推值过大");
        }
        windowSum = windowSum - old + next;
    }
    std::vector<long long> result;
    for (int i = 0; i < k; ++i) {
        result.push_back(ring[(oldest + i) % k]);
    }
    return result;
}
```

> [!warning] 数值边界
> 这段代码把 `limit>=1` 作为前提，并使用 `long long`。若下一项超出整数范围，需要更严格的溢出保护或大整数类型。这里“容量恰好是 k”不意味着可以直接套用预留空格法，否则只存得下 $k-1$ 项。

---

## 17. 典型练习与参考解答

### 17.1 练习：把递推输出改写为递归

要求按照 `n,n-1,...,2` 的顺序输出整数，直到 `n<=1` 停止。可以在递归调用**之前输出**，由此保持由大到小的顺序。

```cpp
#include <iostream>

void printDescending(int n) {
    if (n <= 1) return;           // 递归终止条件
    std::cout << n << ' ';       // 先输出，再缩小问题
    printDescending(n - 1);
}
```

### 17.2 练习：把递归读入、回退累加改为非递归

题意为：不断读取整数，遇到 `0` 停止；原递归函数在最深层先输出 `0`，然后回溯过程中依次输出逆序累加值。非递归写法必须先用容器保存读入的值，再从末尾向前计算。

```cpp
#include <iostream>
#include <vector>

void reverseAccumulation() {
    std::vector<int> values;
    int x;
    while (std::cin >> x && x != 0) values.push_back(x);
    int sum = 0;
    std::cout << sum << '\n';
    for (auto it = values.rbegin(); it != values.rend(); ++it) {
        sum += *it;
        std::cout << sum << '\n';
    }
}
```

例如输入 `1 2 3 0`，打印顺序是 `0,3,5,6`，不是从前向后的前缀和 `1,3,6`。

### 17.3 练习：三类括号混合检查

答案参见前文 `bracketsValid`，它支持 `()[]{}` 的任意合法嵌套，复杂度 $O(n)$。

### 17.4 练习：循环队列判空、判满与长度

在**留一空格**方案，数组长度 $N$、队头下标 $f$、队尾下标 $r$：

$$\text{空：}f=r;\quad\text{满：}(r+1)\bmod N=f;$$

$$\text{当前长度：}(r-f+N)\bmod N.$$

例如 $N=8,f=6,r=2$，逻辑元素位于 `6,7,0,1` 四个槽，队列长度为 $4$；下一次入队写在下标 `2`。

### 17.5 练习：顺序栈与链队列的边界

**问**：一个固定容量为 6 的顺序栈，按“`top` 指向栈顶元素”约定，初始 `top` 是多少？`Push` 四次后是多少？

**答**：初始 $-1$；入栈四次后为 $3$；判满条件是 `top==5`。

**问**：带头结点的链队列只有一个实际结点，删除后应该怎样处理？

**答**：令 `front->next=nullptr`，再令 `rear=front`，之后释放原数据结点。

## 18. 重点速查：用一个结构表收束本章

| 对象 / 约定 | 空条件 | 满条件（如适用） | 插入 / 删除更新 |
|---|---|---|---|
| 顺序栈，`top` 指向栈顶元素 | `top==-1` | `top==CAP-1` | `data[++top]` / `data[top--]` |
| 顺序栈，`top` 指向下一空位 | `top==0` | `top==CAP` | `data[top++]` / `data[--top]` |
| 无头结点链栈 | `top==nullptr` | 取决于内存分配 | 结点头插 / 头删 |
| 普通线性顺序队列 | `front==rear` | `rear==CAP`（可能假溢出） | `rear++` / `front++` |
| 循环队列，留一空格 | `front==rear` | `(rear+1)%CAP==front` | 指针取模加一 |
| 带头结点链队列 | `front==rear` | 取决于内存分配 | 尾插 / 删首元，最后一元另修正 `rear` |

> [!summary] 全章复盘
> 栈适合**撤销、嵌套与回溯**，队列适合**排队与循环缓冲**。做题时不要直接背语句：先说清 **结点/数组长什么样、指针具体指哪里、这一步先改谁后改谁、什么时候判空判满**，再写代码。对复杂过程优先按图中的每一帧亲自模拟一次。
