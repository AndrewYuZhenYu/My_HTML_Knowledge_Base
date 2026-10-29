# GitHub Pages 图片缺失与章节 404：故障日志

> 事件日期：2026-10-29  
> 仓库：<https://github.com/AndrewYuZhenYu/My_HTML_Knowledge_Base>  
> 站点：<https://andrewyuzhenyu.github.io/My_HTML_Knowledge_Base/>  
> 本文记录当时的故障、取证范围和修复后的复核结果。文中的“历史版本”与“当前版本”必须分开阅读；过去的 404 不代表现在仍然存在。

## 1. 故障摘要

历史发布版本的首页、侧栏和部分物理讲义已经生成了指向新内容的链接，但同一发布树里缺少这些链接指向的文件：

- 第 12～14 章讲义共引用 110 张 PNG；发布树中没有 `assets/imported/physics/` 目录。
- 首页和全站侧栏已经链接第 15 章正文 `subjects/physics/15-waves.html` 及其思维导图 `subjects/physics/15-waves-mindmap.html`；两个 HTML 当时均未进入发布树。
- 因此本地文件齐全时能正常浏览，线上却出现图片裂图和章节 404。浏览器页面能打开，并不意味着它引用的每个图片 URL 都已发布。

**主因是发布内容不同步**：导航和讲义 HTML 先到达发布版本，新增的图片与两个页面没有同时到达。初次排查时，本地 `main` 比记录的 `origin/main` 超前一个提交；远程仓库页面也显示当时的 `main` 没有 `assets/imported/physics/` 路径。这个证据比单凭浏览器“图片不显示”更能定位问题。

## 2. 时间线与版本对照

| 版本 | 可核实的文件状态 | 结果 |
|---|---|---|
| `6d8223c`（`2026.10.29.1`，历史故障快照） | 首页已含第 15 章链接；第 12～14 章 HTML 已引用 PNG；`assets/imported/physics/` 中有 0 个文件；第 15 章正文和导图均不存在 | 旧讲义页面可打开，新增图片和第 15 章链接失败 |
| `02e3a86`（`2026.10.29.2`，排查时的本地提交） | 本地增加 145 张导入图片及第 15 章两个 HTML，但当时 `origin/main` 仍停在 `6d8223c` | 解释了“本地正常、线上异常”的差异；仅本地存在不等于已发布 |
| `296130b`（`2026.10.29.3`，当前版本） | 本地 `main` 与 `origin/main` 指向同一提交；生成路径改为可重现命名；新增资源完整性检查与验证工作流 | 当前本地扫描无缺失；线上第 15 章及其图片已抽查恢复 |

上述“发布树缺少”指当时可见的仓库/Pages 内容；GitHub Pages 的 Settings 页面所设的具体发布方式没有取得授权视图，因此本文不把“`main` 根目录部署”写成已经核实的设置。

## 3. 历史快照的可重复检查

将提交 `6d8223c` 用 `git archive` 解到临时目录，再用当前[完整性检查器](../tools/check_site_integrity.py)扫描该快照，得到：

| 指标 | 历史快照结果 | 口径 |
|---|---:|---|
| 生成的 HTML | 30 个 | 首页、课程/笔记/思维导图及预览页；不含构建模板 |
| 本地引用 | 2663 条 | 包括页面、图片、脚本、样式、搜索索引等引用 |
| 图片引用 | 110 条 | 第 12～14 章的新增 PNG |
| `missing_file` 报错 | 232 次 | 同一个目标可能被首页、侧栏、导图多次引用 |
| 不同的缺失图片目标 | **110 个** | 不是 232 张图片 |
| 不同的缺失 HTML 目标 | **2 个** | 第 15 章正文与思维导图 |

这里的 **110** 是历史线上快照中实际存在的页面所引用、却未发布的图片数量。后来本地第 15 章加入的 **35** 张图，使待同步的图片总数变成 **145**；但由于第 15 章页面当时整个缺失，不能把 145 张都说成“已在历史线上页面中逐张看见裂图”。这是两个不同统计口径。

复现命令（在仓库根目录执行；只写入临时目录）：

```bash
SNAPSHOT_DIR=$(mktemp -d)
git archive 6d8223c | tar -x -C "$SNAPSHOT_DIR"
python tools/check_site_integrity.py --root "$SNAPSHOT_DIR"
```

典型历史引用：

- `subjects/physics/14-oscillations.html` 中的 `../../assets/imported/physics/ae5e482e26-physics_vibration_shm_cosine_2c9dcf77-6f5a-4746-8c4b-1fb9cc5b7bea.png`。相对层级本身正确，但目标文件当时不在发布树。
- 首页中的 `subjects/physics/15-waves.html`。链接指向的文件当时不存在。
- 排查当时直接访问上述图片和第 15 章 URL，GitHub Pages 均显示“404 / File not found”；第 14 章 HTML 可打开，但其中已加载完成的图片有 `naturalWidth = 0`。

## 4. 根因链：为什么本地正常、线上失败

1. [构建器](../tools/build.py)把 Markdown 转为 HTML，并把源图片复制到 `assets/imported/physics/`；导航和搜索索引也引用生成的页面。
2. 本地浏览器按当前磁盘目录解析 `../../assets/...`。只要本地图片和 HTML 存在，就能正常显示，无法证明 Git 提交或 Pages 发布包含它们。
3. 历史提交 `6d8223c` 包含“引用方”，却缺少“被引用方”。Pages 只提供已发布的文件，所以图片请求和第 15 章导航请求返回 404。
4. 旧版 `build.py --check` 主要检查当前本地文件和部分 `src`/`href`，没有把“文件是否在待发布 Git 树中”作为独立门槛。于是本地构建通过仍可能漏发资源。
5. 早期不少图解是直接嵌入 HTML 的 SVG，不依赖独立 PNG 路径；新增章节大量使用独立 PNG，文件同步遗漏的影响因此更集中地出现在新内容上。

## 5. 已确认问题与非主因

### 已确认

- **Git 文件同步不完整**：历史版本缺少 110 个当时已被引用的 PNG 和两个已被导航引用的 HTML。
- **构建命名存在跨机器隐患**：旧[构建代码](../tools/build.py)曾以本机绝对路径计算导入图片的哈希前缀。不同电脑上的绝对目录不同，重新构建可能生成不同图片名。这是确实存在的可复现性问题，但没有证据证明它就是历史版本缺文件的直接触发点。
- **检查范围不足**：旧的本地链接检查没有覆盖 Git 发布树、`srcset`、CSS `url(...)`、SVG 外部引用和搜索索引等全部场景。

### 检查后未作为本次主因

- `.gitignore` 未忽略 PNG 或生成的 HTML；故障不是图片被忽略规则排除。
- 历史图片链接的 `../../assets/...` 相对层级正确，不是 GitHub Pages 项目子路径 `/My_HTML_Knowledge_Base/` 被漏加。
- 缺少 `.nojekyll` 可能影响带下划线的原始 `sources/physics/_assets/` 目录，但故障讲义引用的路径是 `assets/imported/physics/`，其目录名不以下划线开头，因此不能把 Jekyll 规则误写为这 110 张讲义图片的主因。
- 未取得 Pages Settings 和部署日志的完整视图，不对具体的分支/目录或 Actions 发布模式下结论。

## 6. 当前修复与验证结果

当前[构建器](../tools/build.py)用**仓库内相对源路径**计算图片文件名；[完整性检查器](../tools/check_site_integrity.py)检查本地链接，并可用 `--require-tracked` 检查 Git 索引、用 `--git-ref origin/main` 对比最近一次获取的远程树。[验证工作流](../.github/workflows/validate-site.yml)在推送或 PR 时重新构建、运行测试并检查生成文件是否随提交同步。根目录 `.nojekyll` 保证采用 Jekyll 分支发布时，带下划线的原始附件目录也不会被默认排除；它没有改变发布架构。

2026-10-29 复核：

- 在新增本复盘文档之前，`git status -sb` 显示 `main...origin/main` 且工作区干净；两者都指向 `296130b`。文档创建后会作为未提交新文件出现，不影响这个版本对照结论。
- `python tools/check_site_integrity.py --require-tracked` 与 `--git-ref origin/main` 均扫描 **32 个 HTML、2833 条本地引用**，返回 **0 个问题**。其中图片引用 145 条、页面引用 2543 条；其余为脚本、样式、原文等资源引用。
- 线上第 15 章页面已能打开；浏览器实测该页 **35/35 张正文图片 `naturalWidth > 0`**。这说明抽查页面和图片恢复。**没有对全站全部 145 张图片逐个执行 HTTP 状态检查**，不能把这次抽查写成全站逐项线上验收。
- 完整构建、`tests/smoke.py` 和 `tests/test_site_integrity.py` 已通过。测试核对四章 145 张图片与源图片字节一致；没有通过压缩或降低画质“修复”路径。

## 7. 以后遇到相同症状时先看什么

| 现象 | 第一检查点 | 典型处理 |
|---|---|---|
| 本地与线上都缺图 | 检查源 Markdown 的图片相对路径、源图片文件、`build.py --check` 的警告 | 补齐源图片并重新构建 |
| 本地正常、Git 索引检查失败 | `python tools/check_site_integrity.py --require-tracked` | 将生成的 HTML、图片及相关索引一起加入提交 |
| Git 索引通过、远程树检查失败 | 刷新 `origin/main` 后执行 `--git-ref origin/main` | 核对哪些提交尚未推送；不要只推源码 |
| 远程树含文件、Pages 仍 404 | Pages Settings、部署日志、文件名大小写、`.nojekyll`、缓存及实际发布目录 | 按真实发布方式排查；不要盲目切换架构 |
| 页面能开但图裂开 | 浏览器 Network 中图片请求的完整 URL、状态码与 `naturalWidth` | 回到具体引用和发布树定位目标文件 |

后续固定操作流程见[《GitHub Pages 知识库发布规范》](GitHub_Pages_知识库发布规范.md)。

