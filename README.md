# 知栈 V3｜HTML 阅读优先知识库

> 已将大学物理、离散数学、数据结构共 13 篇 Markdown 笔记导入本地网页；源文件保存在 `sources/`，阅读页由构建器生成。

## 当前收录

- 大学物理：第 12 章气体动理论、第 13 章热力学基础、第 14 章振动、第 15 章波动。四章正文和 145 张配图以对应 ZIP 为准。
- 离散数学：命题逻辑第 1–5 讲。
- 数据结构：第 2–5 章。

每篇笔记都有双侧思维导图，节点可直接跳转到正文；导图根据当前 Markdown 标题层级生成。新版大学物理四章分别含 40、28、42、35 张 ZIP 原配图，并保留第 12～14 章已有的 10 个参数交互图与麦克斯韦速率分布实验室。其余课程的原有图解和交互组件继续保留。四个 ZIP 导入时只将图片引用改写为本地相对路径，并将 Obsidian `![[图片]]` 引用改为标准 Markdown 图片语法；正文文字与公式来自 ZIP。

直接打开根目录的 `index.html`，即可从首页进入所有课程页面。新版第 14 章的图片已随 ZIP 导入；详情见 `docs/conversion-report.json`。

## 直接体验（不需要安装依赖）

1. 解压完整 ZIP，保持目录结构。
2. 用 Safari、Chrome 或 Edge 双击根目录 `index.html`。
3. 点击首页任一课程方框，进入该课程总览，再选择具体笔记；在大学物理中可打开**第12章 气体动理论**检查正文、公式和彩色 Callout。
4. 在任意讲义中点击**本章思维导图**：知识节点可点击跳转到对应原文；点击主分支标题折叠。
5. 顶部两个侧栏按钮可收起或展开课程导航与本页目录；`Aa` 可调整字号、行距、阅读宽度，也可切换深色模式。全屏按钮会请求浏览器全屏；当前窗口不支持时切换为专注阅读布局。
6. 大学物理讲义中可拖动滑块观察等温线、自由程、绝热线、卡诺效率、振动与共振等曲线；数据结构讲义可逐步查看插入、循环队列、BF 匹配和稀疏矩阵转置；离散数学讲义可切换赋值并定位真值表行。
7. 代码块使用离线语法配色和较大的等宽字体；点击顶部「复制代码」可保留原始缩进与换行。

不需要安装 Mermaid、Markmap，也不需要联网加载公式字体库。导图即使 JavaScript 不运行，也能显示全部节点与链接；交互图会保留对应静态 SVG。

## 首次准备构建环境

macOS 终端，在解压目录下执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm install
python tools/build.py --check
```

Windows PowerShell（已经安装 Python / Node.js）：

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
npm install
python tools/build.py --check
```

> 若 PowerShell 拒绝激活脚本，可使用 `.venv\Scripts\python.exe -m pip install -r requirements.txt` 和 `.venv\Scripts\python.exe tools\build.py --check`，无需更改全局执行策略。

## 后续如何批量导入

将原始 Markdown 放在对应课程文件夹：

```text
sources/physics/13 热力学基础｜知识体系重构版.md
sources/physics/14 振动 扩充版.md
sources/physics/15 波动.md
sources/discrete-math/01 命题逻辑.md
sources/data-structures/02 线性表.md
```

接着在项目根目录运行：

```bash
python tools/build.py --check
```

构建器会自动生成独立 HTML、分级课程导航、搜索索引、公式 SVG、Callout 语义色样式，并输出迁移报告到 `docs/conversion-report.json`。后续可重复执行；不会修改 `sources/` 原文，但会**覆盖自动生成的 HTML**。

若需重新导入第 12～15 章的四个权威 ZIP，运行 `python tools/import_physics_zips.py "ZIP 所在文件夹"`，再重新构建。导入脚本会验证四个压缩包中的配图引用是否齐全。

需要增加一个课程文件夹时，先在 `config/courses.json` 中添加该课程的 `id`、`name` 和 `order`。

## Netlify 手动部署

不要把整个开发项目文件夹拖到 Netlify：其中的 `node_modules/`、`.build-deps/`、构建脚本和配置文件都不是网站发布内容。完成本地构建后运行：

```bash
python tools/prepare_netlify.py
```

这会生成 `netlify-upload/`，其中 `index.html` 位于根目录，课程页面及所需的样式、脚本、原始 Markdown 链接和预览页面都已包含。把 **`netlify-upload` 文件夹**拖到 [Netlify Drop](https://app.netlify.com/drop)。每次更新笔记后，先运行 `python tools/build.py --check`，再运行准备脚本并重新上传。准备脚本会检查发布目录内的本地链接。

## 技术结构

- `sources/`：Markdown 权威源文件。
- `subjects/`：生成的完整 HTML 课程笔记。
- `assets/style.css`：统一版式和多色 Callout 主题。
- `assets/app.js`：字号、行距、搜索、主题、页内目录。
- `assets/mindmap.js`：导图增强；内容主体不依赖此脚本。
- `assets/lab.js`：实时函数图绘制。
- `assets/physics-widgets.js`：大学物理第 12～14 章正文的 10 幅可调参数曲线。
- `assets/learning-widgets.js`：数据结构的算法步骤演示和离散数学的赋值交互真值表。
- `assets/trace-widgets.js`：将算法状态序列变为逐步操作图。
- `assets/concept-interactions.js`：概率分布、复杂度、前缀函数、地址映射与真值格的参数交互。
- `assets/code-copy.js`：代码块复制按钮，兼容本地文件浏览时的复制回退。
- `tools/code_blocks.py`：构建时为 C++、Shell 代码生成离线语法配色和工具栏。
- `tools/visual_catalog.py`：逐章审核过的专题图解配置；构建时校验标题匹配和每篇至少 15 幅。
- `tools/upgrade_diagrams.py`：以定量函数图与结构图替换早期文字框图。
- `tools/build.py`：Python 批量构建。
- `tools/prepare_netlify.py`：生成并检查轻量的手动上传目录。
- `tools/render_math.js`：MathJax 构建阶段转换 LaTeX 为 SVG。
- `config/courses.json`：课程导航配置。

**依赖**：Python 3.11+、Mistune、BeautifulSoup4、Node.js（LTS）、MathJax 3。只是重建页面时需要这些依赖，阅读 HTML 无需依赖构建环境。

## 当前边界

- 支持常见 Markdown 标题、正文、列表、表格、代码、`$...$` 和 `$$...$$`、标准 Obsidian Callout，以及普通相对图片/附件链接。
- 不保证支持 Obsidian 所有插件私有语法，尤其是 `[[双链]]` 和 `![[附件]]`；建议批量迁移前检查。
- 第 12 章保留麦克斯韦交互函数图；四章导图均依据新版 Markdown 标题层级生成。ZIP 配图为静态图片，参数交互图仍由 `tools/physics_widgets.py` 配置。其他课程的补充图解仍由 `tools/visuals.py` 等文件配置。
- 直接双击 HTML 可以阅读和使用当前内置搜索。完整跨站部署或更复杂的浏览器接口可能需要本地 HTTP 服务。

完整设计与限制见包外的《HTML知识库_V3_整体规范与技术说明.md》。
