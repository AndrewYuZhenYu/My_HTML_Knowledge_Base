# 知栈 V3｜HTML 阅读优先知识库

> 已将大学物理、离散数学、数据结构共 12 篇 Markdown 笔记导入本地网页；原始文件保存在 `sources/`，阅读页由构建器生成。

## 当前收录

- 大学物理：第 12 章气体动理论、第 13 章热力学基础、第 14 章振动。
- 离散数学：命题逻辑第 1–5 讲。
- 数据结构：第 2–5 章。

每篇笔记都有双侧思维导图，节点可直接跳转到正文；第 12 章气体动理论保留人工编排的导图，其余导图根据原始标题层级生成。按统一的正文图解计数，12 篇笔记各有 20 个本地 SVG 图解或交互组件，共 240 个；原有麦克斯韦速率分布交互图另计。大学物理占 60 个，其中 10 个可调参数；数据结构占 80 个，其中 4 个算法步骤演示；离散数学占 100 个，其中 5 个交互真值表。图解是辅助阅读内容，原始 Markdown 仍是知识来源。

直接打开根目录的 `index.html`，即可从首页进入所有课程页面。第 14 章原笔记引用的 8 张 `振动_Obsidian_配图/*.png` 未随笔记提供；网页在原引用位置放入依据正文重绘的示意图，并注明不是原图。详情见 `docs/conversion-report.json`。

## 直接体验（不需要安装依赖）

1. 解压完整 ZIP，保持目录结构。
2. 用 Safari、Chrome 或 Edge 双击根目录 `index.html`。
3. 点击首页任一课程方框，进入该课程总览，再选择具体笔记；在大学物理中可打开**第12章 气体动理论**检查正文、公式和彩色 Callout。
4. 在任意讲义中点击**本章思维导图**：知识节点可点击跳转到对应原文；点击主分支标题折叠。
5. 顶部两个侧栏按钮可收起或展开课程导航与本页目录；`Aa` 可调整字号、行距、阅读宽度，也可切换深色模式。全屏按钮会请求浏览器全屏；当前窗口不支持时切换为专注阅读布局。
6. 大学物理讲义中可拖动滑块观察等温线、自由程、绝热线、卡诺效率、振动与共振等曲线；数据结构讲义可逐步查看插入、循环队列、BF 匹配和稀疏矩阵转置；离散数学讲义可切换赋值并定位真值表行。

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
sources/physics/13 热力学基础.md
sources/physics/14 振动.md
sources/discrete-math/01 命题逻辑.md
sources/data-structures/02 线性表.md
```

接着在项目根目录运行：

```bash
python tools/build.py --check
```

构建器会自动生成独立 HTML、分级课程导航、搜索索引、公式 SVG、Callout 语义色样式，并输出迁移报告到 `docs/conversion-report.json`。后续可重复执行；不会修改 `sources/` 原文，但会**覆盖自动生成的 HTML**。

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
- `assets/physics-widgets.js`：大学物理正文的 10 幅可调参数曲线。
- `assets/learning-widgets.js`：数据结构的算法步骤演示和离散数学的赋值交互真值表。
- `tools/visual_catalog.py`：逐章审核过的专题图解配置；构建时校验标题匹配和每篇至少 15 幅。
- `tools/build.py`：Python 批量构建。
- `tools/prepare_netlify.py`：生成并检查轻量的手动上传目录。
- `tools/render_math.js`：MathJax 构建阶段转换 LaTeX 为 SVG。
- `config/courses.json`：课程导航配置。

**依赖**：Python 3.11+、Mistune、BeautifulSoup4、Node.js（LTS）、MathJax 3。只是重建页面时需要这些依赖，阅读 HTML 无需依赖构建环境。

## 当前边界

- 支持常见 Markdown 标题、正文、列表、表格、代码、`$...$` 和 `$$...$$`、标准 Obsidian Callout，以及普通相对图片/附件链接。
- 不保证支持 Obsidian 所有插件私有语法，尤其是 `[[双链]]` 和 `![[附件]]`；建议批量迁移前检查。
- 第12章气体动理论保留人工编排的双侧导图和麦克斯韦交互函数图。其余 11 篇的导图依据 Markdown 标题层级自动生成，忠实反映原有章节结构；正文 SVG 图解和物理交互图依据指定知识点绘制，新增笔记需分别在 `tools/visuals.py` 和 `tools/physics_widgets.py` 中配置。
- 直接双击 HTML 可以阅读和使用当前内置搜索。完整跨站部署或更复杂的浏览器接口可能需要本地 HTTP 服务。

完整设计与限制见包外的《HTML知识库_V3_整体规范与技术说明.md》。
