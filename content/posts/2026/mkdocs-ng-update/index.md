---
title: mkdocs-ng 维护进展：v1.7.x 修复总结与下一步计划
summary: |
  从接手 mkdocs-ng 维护以来发了四个版本，修了十几个 Bug，去掉了 mergedeep 依赖。接下来 v1.8.0 会是一个功能版本，计划去掉旧 Python 版本支持、移除内置主题的 CDN 依赖、提供稳定的 Python API。
tags:
  - OpenSource
  - MkDocs
authors:
  - shenxianpeng
date: 2026-05-14
series: ["MkDocs NG"]
series_order: 2
---

大家好，我是沈工。

上个月我写了那篇[正式维护 MkDocs 的文章](mkdocs-ng)，宣布 fork 了 MkDocs 并开始在 mkdocs-ng 下发包。

当时发的是 v1.7.0。到现在已经发了四个版本，一路到了 v1.7.3。这篇文章就是把这几个版本的改动整理一下，同步给社区，顺便聊聊 v1.8.0 的计划。

## 版本更新总览

从 4 月 24 日到 5 月 9 日，发布了四个版本：

| 版本 | 日期 | 主要改动 |
|------|------|---------|
| v1.7.0 | 2026-04-24 | 首次发布：rebrand 为 mkdocs-ng，支持 Python 3.13/3.14 |
| v1.7.1 | 2026-04-25 | Bug 修复：anchor 校验、serve 清理、颜色模式；移除 mergedeep |
| v1.7.2 | 2026-04-27 | Bug 修复：symlink、IPv6 格式 URL、导航下拉箭头 |
| v1.7.3 | 2026-05-09 | Bug 修复：Click 兼容、livereload、搜索 HTML 标签；新增 content_title API |

下面按版本详细介绍。

---

## v1.7.0（2026-04-24）

这是 mkdocs-ng 的第一个版本。主要改动是 rebrand：包名从 `mkdocs` 变为 `mkdocs-ng`，文档和仓库链接更新到 mkdocs-ng 组织下。CLI 命令仍然是 `mkdocs`，配置文件仍然是 `mkdocs.yml`。

此外：

- 修复了 `mkdocs serve --livereload` 参数无法识别的问题
- 添加了 Python 3.13 和 3.14 的支持（声明及 CI 测试）
- 搭建了维护基础设施：issue 模板、Dependabot、Release Drafter、pre-commit hooks

安装方式：

```bash
pip install -U mkdocs-ng
```

---

## v1.7.1（2026-04-25）

四个 Bug 修复和一个依赖清理。

**`--strict` 模式下的 anchor 校验**

之前用 `mkdocs build -v --strict` 严格检查链接时，有两个问题：被 exclude 的页面仍然会被检查，导致误报；anchor 缺失只输出 WARNING 而没有返回非零退出码，CI 里拦不住。这两个问题都修了。（[#30](https://github.com/mkdocs-ng/mkdocs/issues/30)、[#32](https://github.com/mkdocs-ng/mkdocs/issues/32)）

**`mkdocs serve` 退出时清理临时目录**

`mkdocs serve` 退出后会在 `/tmp` 下留下构建产生的临时目录，之前只在正常退出时清理，收到 `SIGTERM` 时不会。现在 `SIGTERM` 也会触发清理了。（[#36](https://github.com/mkdocs-ng/mkdocs/issues/36)）

**禁用 highlightjs 时颜色模式切换失效**

内置主题的深色/浅色模式切换按钮依赖于 highlightjs 的加载状态。如果你在 `mkdocs.yml` 里禁用了 `highlightjs`，切换按钮就会失效。现在两者解耦了。（[#39](https://github.com/mkdocs-ng/mkdocs/issues/39)）

**移除 mergedeep 依赖**

`mergedeep` 是一个不再维护的第三方库，被替换成了内联的 deep-merge 工具函数。少了一个外部依赖，也消除了潜在的供应链风险。（[#29](https://github.com/mkdocs-ng/mkdocs/issues/29)）

---

## v1.7.2（2026-04-27）

三个 Bug 修复。

**损坏的 symlink 导致构建崩溃**

文档目录里如果有一个指向已删除文件的符号链接（dangling symlink），整个 `mkdocs build` 会直接崩溃。现在这种 symlink 会被跳过，构建继续进行。（[#46](https://github.com/mkdocs-ng/mkdocs/issues/46)、[#43](https://github.com/mkdocs-ng/mkdocs/issues/43)）

**格式错误的 URL 导致构建崩溃**

`mkdocs.yml` 里如果配了一个格式不对的 URL——比如不完整的 IPv6 地址 `https://[::1`——整个构建也会崩溃。现在改成了输出清晰的 warning，不再中断构建。（[#45](https://github.com/mkdocs-ng/mkdocs/issues/45)）

**导航栏下拉子菜单箭头不可见**

Material 主题的导航栏中，有子菜单的项右侧应该有一个小箭头图标。之前这个箭头莫名消失了，用户看不出那里有子菜单。已修复。（[#44](https://github.com/mkdocs-ng/mkdocs/issues/44)）

---

## v1.7.3（2026-05-09）

四个 Bug 修复，一个新增 API。

**新版 Click 导致 CLI 默认值异常**

从 Click 8.3.0 开始，默认参数的处理逻辑变了，导致 `mkdocs serve` 的 `--livereload`、`mkdocs build` 的 `--strict` 和 `--use-directory-urls` 等参数行为异常——你在 `mkdocs.yml` 里配好的值会被命令行默认值覆盖。修了。（[#60](https://github.com/mkdocs-ng/mkdocs/issues/60)）

**Livereload 对编辑器临时文件过度敏感**

vim 的 swap 文件（`.md.swp`）、Emacs 的自动保存文件（`#file.md#`）、tilde 备份文件（`file.md~`）这些编辑器产生的临时文件每次变更都会触发 livereload 重建。现在这些文件被忽略了，写文档时不再频繁刷页面。（[#55](https://github.com/mkdocs-ng/mkdocs/issues/55)）

**边界 case 的 HTML markup 导致构建崩溃**

Markdown 里写了 `<<>>` 这种边界标记时，Python 标准库的 `html.parser` 会抛出 `AssertionError`，导致整个构建中断。已修复。（[#51](https://github.com/mkdocs-ng/mkdocs/issues/51)）

**搜索结果中显示原始 HTML 标签**

页面的 title 里如果包含 HTML 标签（比如 `` `<code>` `` 包裹的命令名），搜索索引会原样收录这些标签，导致搜索结果中出现一坨 HTML 源码。现在搜索索引里的标题会自动 strip HTML 标签。（[#53](https://github.com/mkdocs-ng/mkdocs/issues/53)）

**新增 `page.content_title` 属性**

给 plugin 开发者提供了一个新 API：`page.content_title`，可以直接拿到页面第一个标题的纯文本（HTML 标签已被 strip）。以前 plugin 作者得自己在 `on_page_content` 里写正则解析 H1，现在直接访问属性就行。（[#52](https://github.com/mkdocs-ng/mkdocs/issues/52)）

---

完整 changelog 见：[mkdocs-ng Release Notes](https://mkdocs-ng.github.io/mkdocs/about/release-notes/)

---

## 关于 v1.8.0

v1.7.x 系列的核心任务是修 Bug、稳定基础。现在这些差不多了，接下来的 v1.8.0 会是一个含功能改动的版本。以下是目前的计划。

**放弃 Python 3.8 和 3.9**

Python 3.8 已经在 2024 年 10 月 EOL，3.9 也即将在 2025 年 10 月 EOL。v1.8.0 会把这些已经失去官方支持的 Python 版本从支持矩阵里去掉，把最低支持版本提到 Python 3.10。这意味着可以用 `|` 类型联合语法、`match`/`case` 等更现代的写法，对后续维护和功能开发都有好处。（[#33](https://github.com/mkdocs-ng/mkdocs/issues/33)）

**移除内置主题的外部 CDN 依赖**

`mkdocs` 和 `readthedocs` 两个内置主题会从 Google Fonts 和 CDN 加载字体和 CSS。对于需要完全离线或注重隐私的部署场景来说，这是个长期痛点（上游 issue 18 个 👍）。v1.8.0 计划把必需的资源打包进主题里，不再发起第三方请求。（[mkdocs/mkdocs#2171](https://github.com/mkdocs/mkdocs/issues/2171)）

**提供稳定的 Python API**

MkDocs 目前没有一个官方支持的 Python API——想在代码里调用构建或 serve，要么用内部函数，要么走 `subprocess`。v1.8.0 计划提供一个文档化的公开 API（比如 `mkdocs.build()`、`mkdocs.serve()`），方便 CI 脚本和 build system 集成。（[mkdocs/mkdocs#1240](https://github.com/mkdocs/mkdocs/issues/1240)）

**自动生成的导航使用 index 页面标题**

当 `mkdocs.yml` 没有显式配置 `nav` 时，MkDocs 会用目录名作为导航栏的分组标题。改成用 index 页面的标题会更自然——比如 `about/` 目录下 `index.md` 标题是「关于本项目」，导航栏就显示「关于本项目」而不是 `about`。（[#54](https://github.com/mkdocs-ng/mkdocs/issues/54)）

**清理更多过期依赖**

继 v1.7.1 去掉 `mergedeep` 之后，v1.8.0 计划继续审计和清理不再维护的依赖项，减少外部依赖的总体数量。

完整的功能计划在 [MkDocs-NG Feature Plan](https://github.com/mkdocs-ng/mkdocs/issues/59) 里持续更新。如果你在用的 MkDocs 有什么一直想修但上游没动静的问题，可以到那个 issue 下面留言，或者在仓库里单独提 issue。

---

## 怎么切过来

如果你之前在用的还是上一代的 `mkdocs` 包：

```bash
pip uninstall mkdocs
pip install mkdocs-ng
```

CLI 命令、配置文件、插件命名空间——全部保持不变。唯一的变化是包名从 `mkdocs` 变成了 `mkdocs-ng`。

如果用的是 `requirements.txt` 或 `pyproject.toml`：

```diff
- mkdocs>=1.6.0
+ mkdocs-ng>=1.7.3
```

Material for MkDocs 用户也一样：

```bash
pip uninstall mkdocs-material
pip install mkdocs-ng-material
```

---

仓库地址：

- [mkdocs-ng/mkdocs](https://github.com/mkdocs-ng/mkdocs)
- [mkdocs-ng/mkdocs-material](https://github.com/mkdocs-ng/mkdocs-material)

欢迎提 issue、给 Star，也欢迎转给还在用 MkDocs 的朋友。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
