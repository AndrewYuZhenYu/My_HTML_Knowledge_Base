# GitHub Pages 知识库发布规范：路径、构建、提交与验收

> 适用项目：`My_HTML_Knowledge_Base`  
> 站点前缀：`/My_HTML_Knowledge_Base/`  
> 版本：2026-10-29  
> 目的：保证新笔记、新插图和导航在本地、Git 提交树与线上站点中指向同一批真实文件。故障实例和证据见[故障复盘日志](GitHub_Pages_图片与页面404_故障复盘.md)。

## 1. 先区分五种“存在”

一个文件在本机看得见，不能据此宣布它已经上线：

| 层次 | 含义 | 检查方式 |
|---|---|---|
| 工作目录 | 文件位于当前磁盘，`file://` 可以读取 | `test -f 路径`、本地完整性检查 |
| Git 索引 | 文件已 `git add`，准备进入下次提交 | `git ls-files`、完整性检查 `--require-tracked` |
| 本地提交 `HEAD` | 文件已成为本地提交的一部分 | `git ls-tree -r --name-only HEAD`、`--git-ref HEAD` |
| 远程分支 `origin/main` | 最近一次获取到的远程树含该文件 | 先 `git fetch origin main`，再用 `--git-ref origin/main` |
| GitHub Pages 实际发布内容 | 浏览器能够从最终站点 URL 取得文件 | 线上 URL、Network 状态码、图片 `naturalWidth` |

五层按顺序核对。**`--require-tracked` 通过只说明 Git 索引完整，不说明已经提交、推送或部署。** `origin/main` 如果没有刷新，也只能代表本机记录的旧远程状态。线上最终是否成功仍以 Pages 实际 URL 为准。

## 2. 文件职责与单一维护入口

| 路径 | 职责 | 日常操作 |
|---|---|---|
| `sources/<course>/*.md` | 正文权威来源 | 在这里新增或修改笔记 |
| `sources/<course>/_assets/...` | 原始图片/附件 | 随 Markdown 一起保留原文件与质量 |
| `config/courses.json` | 课程与输出文件名配置 | 新课程、新章节需要固定友好文件名时更新 |
| `tools/build.py` | Markdown、图片、导航、公式和搜索的构建逻辑 | 修路径生成问题时修改这里 |
| `assets/imported/<course>/` | 构建器复制的可发布图片 | 与引用它的 HTML 一同纳入 Git |
| `subjects/<course>/*.html`、`index.html` | 生成的页面与导航 | 构建产物；不要只手改这里 |
| `assets/search-data.js`、`docs/conversion-report.json` | 生成的搜索索引与转换报告 | 构建后同步检查、提交 |
| `tools/check_site_integrity.py` | 静态资源与发布树检查 | 每次发布前运行 |
| `.github/workflows/validate-site.yml` | 推送和 PR 时运行验证 | **只验证，不负责 Pages 部署** |
| `.nojekyll` | 防止 Jekyll 过滤 `_assets` 等下划线目录 | 保留在发布根目录 |

**不要只修生成 HTML**：下一次运行构建器会覆盖它。若图片路径、章节文件名、导航地址有系统性问题，先修 `sources/`、`config/` 或 `tools/build.py`，再整站重建。

## 3. 站内 URL 的统一写法

### 3.1 一律按“当前文件所在目录”写相对路径

站内图片、页面、CSS、JS、原始 Markdown 和导图链接都使用相对 URL。示例以 `subjects/physics/15-waves.html` 为当前位置：

```html
<img src="../../assets/imported/physics/图片文件名.png" alt="波动示意图">
<a href="../../index.html">返回首页</a>
<a href="15-waves-mindmap.html">查看本章思维导图</a>
<link rel="stylesheet" href="../../assets/style.css">
```

这些地址既可在本地 `file:///.../My_HTML_Knowledge_Base/index.html` 下使用，也会在 Pages 的 `https://andrewyuzhenyu.github.io/My_HTML_Knowledge_Base/` 前缀内解析。构建器负责计算层级；新增内容时优先让构建器生成链接，不要手工猜测 `../` 的个数。

以下站内写法禁止进入发布版：

- `/assets/foo.png`、`/subjects/physics/foo.html`：会指向域名根目录，漏掉项目站点前缀。
- `file:///Users/...`、`/Users/...`、`C:\\...`：只能在某台电脑上使用。
- `http://localhost:...`、`http://127.0.0.1:...`：只在开发者本机可达。
- 仅大小写不同的文件名，例如引用 `Plot.PNG` 而实际文件叫 `plot.png`。macOS 本地磁盘可能容忍，Pages 的文件名匹配不能依赖这一点。
- 直接粘贴带空格、中文或 `#`、`?` 的路径而不验证。构建器和检查器会按 URL 编码拆分路径、查询和锚点；手写链接必须检查解码后目标是否真实存在。

外部 `https://...` 链接不按本地文件判断，但它的可访问性、授权和长期稳定性仍需单独审查。

### 3.2 Markdown 图片与附件

原始 Markdown 中使用相对于 **该 MD 所在目录** 的引用，例如：

```markdown
![驻波示意图](./_assets/zip15/images/standing_wave.png)
```

图片必须真实位于所写相对路径。构建器会复制到 `assets/imported/<course>/`，并把生成 HTML 的 `src` 改为从 HTML 所在目录出发的相对路径。导入 ZIP 时使用现有[导入脚本](../tools/import_physics_zips.py)或等效校验流程，先确认压缩包内每一处图片引用都能匹配到附件。Obsidian 的 `![[图片]]` 语法需要在导入时转换；不要指望标准 Markdown 渲染器自动识别。

不通过删除、降采样、重新压缩图片来“修复”路径问题。`tests/smoke.py` 会核对现有四章 145 张导入图片与源文件的字节一致。新增章节应增加相应的内容或资源测试，而不是只检查页面能打开。

### 3.3 输出名称与可重复构建

同一章节的 `sources/` 文件名、`config/courses.json` 输出覆盖项、`subjects/` 生成文件名必须一致。课程导航、导图、首页和搜索索引由构建器根据当前文档列表生成。当前 `build.py` 使用**仓库内相对源路径**计算导入图片的哈希前缀；禁止再用 `/Users/...` 等本机绝对目录计算文件名，否则另一台机器重建后图片 URL 会改变。

新增章节应一次性检查：

1. 课程页有新笔记。
2. 首页/侧栏导航指向已生成的 HTML。
3. 本章导图文件存在，节点锚点在正文中存在。
4. 搜索结果链接能打开同一章。
5. 图片 `src` 对应文件既存在于磁盘，也会进入 Git 提交。

## 4. 标准发布流程

### 阶段 A：准备构建环境

首次在一台机器上构建时，按[项目 README](../README.md)安装 Python 依赖及 Node.js 的 MathJax 依赖。推荐：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
npm ci
```

这些依赖只用于生成站点，读者打开静态页面不需要安装它们。

### 阶段 B：从源文件重建并做本地验收

```bash
python tools/build.py --check
python tests/smoke.py
python tests/test_site_integrity.py
python tools/check_site_integrity.py
```

放行标准：所有命令退出码为 0，`conversion-report.json` 没有数学渲染错误或未处理的资源警告；检查器显示问题类型为 `none`。`build.py --check` 也会调用完整性检查器。若任何一项失败，先修源文件/构建器并重新构建，不能靠手改生成页面绕过检查。

检查器当前扫描首页、`subjects/` 和 `docs/` 的**生成 HTML**，解析图片、`srcset`、CSS、JS 静态字面量、SVG 外部引用、搜索索引以及页面锚点。它会报告缺文件、大小写错误、根绝对路径、越出站点目录和本地专用 URL。模板 `tools/shell.html`、`templates/` 含有占位符，不作为已生成页面扫描。对于任意运行时动态拼接且无法静态推断的 JS URL，仍需浏览器抽查。

需要完整机器可读报告时：

```bash
python tools/check_site_integrity.py --json-out /tmp/knowledge-base-links.json
```

### 阶段 C：确认 Git 将发布全部目标

构建产物与源文件必须成组处理。先用 `git status -sb` 看新增和修改，再**只对本次相关文件**执行 `git add -- ...`；不要不经检查就把整个工作目录打包或依赖自动忽略规则。针对新增物理章节，至少核对：

```bash
git status -sb
git ls-files subjects/physics/15-waves.html
git ls-files assets/imported/physics
python tools/check_site_integrity.py --require-tracked
git diff --cached --stat
git diff --cached --check
```

`git ls-files` 和 `--require-tracked` 只证明“已经进入索引”。提交前还要检查 `git diff --cached --stat` 是否同时含源 Markdown、所有新图片、对应 HTML、导航/搜索索引和构建代码。不要把 `node_modules/`、`venv/`、`netlify-upload/` 当成 GitHub Pages 发布内容。`.gitignore` 当前只排除这类构建环境和临时目录，没有排除 PNG/HTML；若将来改动忽略规则，必须重新审查。

提交与推送由项目维护者决定；完成后刷新远程分支并核对：

```bash
git fetch origin main
git status -sb
python tools/check_site_integrity.py --git-ref HEAD
python tools/check_site_integrity.py --git-ref origin/main
```

`HEAD` 与 `origin/main` 的检查均为 0，才说明最近一次获取的远程树具有全部目标文件。如果 `git fetch` 因网络或鉴权失败，远程状态记为“未验证”，不能把本机旧的 `origin/main` 当作实时事实。

### 阶段 D：确认实际 Pages 发布

在仓库 **Settings → Pages** 核对当前真实的发布来源（分支及目录，或 Actions）；维护记录里写清该设置。不要因为遇到 404 就擅自改换架构。本项目的 `validate-site.yml` 只做 CI 验证，并没有 `deploy-pages` 步骤；如果 Pages 直接从分支发布，**CI 失败本身不一定阻止 Pages 更新**，除非仓库还配置了相应的分支保护规则。

部署完成后，从实际站点抽查首页、各课程总览、新章节、导图和图片。示例：

```bash
curl -L -s -o /dev/null -w '%{http_code}\n' \
  'https://andrewyuzhenyu.github.io/My_HTML_Knowledge_Base/subjects/physics/15-waves.html'
curl -L -s -o /dev/null -w '%{http_code}\n' \
  'https://andrewyuzhenyu.github.io/My_HTML_Knowledge_Base/subjects/physics/15-waves-mindmap.html'
```

图片 URL 应从**当前生成 HTML 的 `src` 复制**，不要凭旧哈希文件名猜测。浏览器 DevTools 的 Network 面板应无本地图片/脚本/样式 404；对可见图片可检查 `img.complete === true` 且 `img.naturalWidth > 0`。若当前终端的代理或 DNS 无法访问 GitHub Pages，可改用浏览器检查并注明“终端 HTTP 未验证”，不能把失败的命令写成通过。若 Pages 可能尚未完成发布，应先查看部署状态，再做最终验收。

## 5. 故障分流表

| 发现点 | 含义 | 正确下一步 |
|---|---|---|
| `build.py --check` 报 `missing_file` | 生成 HTML 引用的本地文件不存在 | 修 Markdown 图片路径、资源位置或构建逻辑，重新构建 |
| 报 `case_mismatch` | 本地文件名与 URL 大小写不完全相同 | 改为文件系统上的精确拼写，重新构建 |
| 报 `root_absolute_url` / `local_only_or_unsafe_url` | URL 不兼容项目子路径或线上环境 | 改为相对路径，不在生成 HTML 中临时替换 |
| 本地检查通过，`--require-tracked` 失败 | 文件存在但未进入 Git 索引 | 核对并加入相关 HTML/图片/附件 |
| `--git-ref HEAD` 失败 | 文件尚未进入本地提交 | 检查提交内容；不要误把“已暂存”当成“已提交” |
| `--git-ref origin/main` 失败 | 最近获取的远程树缺少目标 | 确认 fetch 是否成功、相关提交是否推送 |
| 远程树通过，线上仍 404 | 发布来源、部署结果、Jekyll、大小写、缓存或 URL 仍有差异 | 查 Settings → Pages、部署日志与请求 URL，不盲目重构 |
| HTML 可打开但图片裂开 | 页面自身存在、图片请求失败 | 在 Network 里取出图片实际 URL，逐级查本地→Git→Pages |
| 搜索能找到标题但跳转 404 | 搜索索引新于已发布页面 | 连同生成 HTML 一起提交；复核 `assets/search-data.js` |

## 6. 发布完成的判定标准

一次发布只有在以下条件同时满足时，才可记录为“完成”：

- 构建、smoke test、资源完整性检查均退出 0；没有未处理的资源警告。
- 本地生成的页面、图片、CSS、JS 和源附件进入目标 Git 提交；`HEAD` 与刷新后的远程树检查没有缺失。
- Pages 当前发布来源已核实，部署过程成功；实际站点首页、至少一篇不同目录深度的课程笔记、导图及新加图片返回成功并正常显示。
- 对新增含大量配图的章节，至少核对首图、正文中部图、末图；关键章节可逐图核验。抽样通过应写成“抽样通过”，不能写成“全站全部图片逐项 HTTP 验收”。

**Netlify 的 `netlify-upload/` 是另一套手动发布副本，不等于 GitHub Pages 的发布树。** GitHub Pages 的验收必须对准它实际配置的源目录和线上 URL。

