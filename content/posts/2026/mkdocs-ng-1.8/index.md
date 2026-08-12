---
title: mkdocs-ng v1.8.0 发布：修复上游遗留问题，构建提速约 14%
summary: |
  mkdocs-ng v1.8.0 发布了，这是 fork 以来的第一个功能版本。内置主题不再复制多余的 highlight.js 资源，clean build 快约 14%，产物少约 440 个文件；搜索终于能搜到 while、if 这类编程关键词。1.9.0 将针对 mkdocs serve 做增量构建优化。
tags:
  - Open Source
  - Documentation
authors:
  - shenxianpeng
date: 2026-08-13
series: ["MkDocs NG"]
series_order: 3
---

mkdocs-ng v1.8.0 在 8 月 13 日发布了（UTC 时间是 12 日晚上），这是 fork 以来的第一个功能版本。v1.7.0 到 v1.7.3 的四个版本都在修 bug、打基础，1.8.0 开始兑现之前承诺的功能。

先给新读者交代一下背景：MkDocs 上游从 2024 年 8 月起就没有新版本了，维护基本停滞。我 fork 了它，在 mkdocs-ng 组织下继续维护，包名是 mkdocs-ng，但 CLI 命令、配置文件、插件生态全部不变。为什么做这件事、v1.7.x 修了哪些问题，[前两篇文章](https://shenxianpeng.github.io/posts/2026/mkdocs-ng/)（[v1.7.x 总结](https://shenxianpeng.github.io/posts/2026/mkdocs-ng-update/)）讲过，这里不重复。

这篇文章说三件事：接手以来解决了哪些上游遗留问题，1.8.0 的性能提升有多大，以及 1.9.0 打算做什么。

## 上游遗留的问题，修了一批

维护以来，文档里多了一个 [Fixed Upstream Issues](https://mkdocs-ng.github.io/mkdocs/about/fixed-upstream-issues/) 页面，专门跟踪「上游报告了但一直没人修」的问题，目前列了 10 个，都已解决。挑几个影响面大的说。

**mkdocs serve 不监听文件变化（[上游 #4032](https://github.com/mkdocs/mkdocs/issues/4032)）。** 这是上游目前点赞最多的 open issue：66 个赞、31 条评论。Click 8.2 之后默认参数的处理逻辑变了，`mkdocs serve` 不再监听文件变化，livereload 只有显式传 `--livereload` 才生效。症状很诡异，不少用户把它误诊成 WSL 的问题。mkdocs-ng 从根因上修掉了它，不需要 pin 住 Click 的旧版本；同源的 `use_directory_urls` 被意外覆盖也一并解决。

**编辑器临时文件触发无意义重建（[上游 #2519](https://github.com/mkdocs/mkdocs/issues/2519)）。** vim 的 swap 文件、`~` 备份、Emacs 的 auto-save，每次变动都会触发一次 rebuild，写文档时页面不停刷新。1.7.3 起这些文件被忽略了。

**搜索搜不到编程关键词（[上游 #4167](https://github.com/mkdocs/mkdocs/issues/4167)）。** `while`、`if`、`for`、`from` 在技术文档里是实打实的关键词，搜索却把它们当英语停用词过滤掉，搜出来是空的。1.8.0 起这些词默认参与索引；想恢复旧行为，给 search 插件配 `stop_words: true` 即可。

**anchor 校验的两个老问题。** 一是假阳性：`pymdownx.tabbed` 这类扩展在渲染后期生成的锚点，会被误报为无效链接（[上游 #3690](https://github.com/mkdocs/mkdocs/issues/3690)）。二是提示太弱：锚点大小写不一致时只报「不存在」，不告诉你怎么改（[上游 #3703](https://github.com/mkdocs/mkdocs/issues/3703)）。后者现在会给出 `did you mean '#conflicts'?` 这样的建议。

**内置主题的第三方依赖（[上游 #2171](https://github.com/mkdocs/mkdocs/issues/2171)，18 个赞）。** 主题资源原本从 CDN 加载，离线部署、内网部署直接失效，访客数据也会暴露给第三方。1.8.0 把 highlight.js 打包进主题，两个内置主题不再有任何 CDN 引用；同时删掉了 2023 年就关停的 Universal Analytics 代码段（[上游 #3630](https://github.com/mkdocs/mkdocs/issues/3630)）。

**稳定的 Python API（[上游 #1240](https://github.com/mkdocs/mkdocs/issues/1240)，10 个赞）。** 以前想在代码里触发构建，只能走 `subprocess` 或 import 私有函数。现在 `mkdocs.build()` 和 `mkdocs.serve()` 是文档化的公开 API，CI 脚本和构建系统可以直接调用。

崩溃类问题也修了几个：`<<>>` 这类边界 markup 在 Python 3.13.5+ 上会触发 `html.parser` 的 `AssertionError` 中断构建（[上游 #4001](https://github.com/mkdocs/mkdocs/issues/4001)）；文档目录里一个损坏的 symlink 会让整个 build 崩掉；格式错误的 IPv6 URL 也会。这些在 v1.7.x 都处理完了。

## 性能：构建快约 14%，产物少约 440 个文件

1.8.0 最大的一项性能改动，起因是一次 profiling：对一个 204 页的站点做分析时发现，472 个被复制的静态文件里，444 个来自 highlight.js——192 种语言语法和约 250 个样式。而一个站点实际只会用到配置里选中的几种语言、一两个样式。对小站点来说这个固定成本尤其扎眼：10 页的站点，接近一半的构建时间花在复制这些永远不会被加载的语法文件上。

修复方式很直接：内置主题现在只复制配置实际引用的资源——`hljs_languages` 里列的语言、`hljs_style` 选的样式；没开 `highlightjs` 就什么都不复制。用 `custom_dir` 覆盖主题的站点不受影响，过滤逻辑会跳过第三方主题和自定义目录。

实测数据（本地 wall time）：

| 场景 | 之前 | 之后 |
|------|------|------|
| clean build，10 页 | 200 ms | 172 ms（−14%）|
| clean build，200 页 | 2.99 s | 2.54 s（−15%）|
| 每个站点复制的文件数 | 512 | 74 |

产物少了约 440 个文件、约 2 MB，部署上传更快，托管空间也更干净。

这个 PR 还消除了一处浪费：搜索插件配了 `indexing: titles` 时，之前仍会解析整页 HTML，而解析结果根本用不上，现在跳过了，索引输出完全一致。

另外，从 1.8.0 开始，每个 PR 都会在 CodSpeed 上跑性能基准测试，构建速度出现回归会在合并前被拦住。没有度量支撑的「性能优化」很容易改完又退化，我们希望把这件事制度化。

## 1.9.0 预告：性能优化的下一站是 serve

性能工作还没结束。1.9.0 的重点会放在 `mkdocs serve` 的构建管线上，方向是增量构建和更聪明的文件监听。这个需求来自[上游 #3695](https://github.com/mkdocs/mkdocs/issues/3695)，由 Material for MkDocs 的维护者提出，15 个赞、22 条评论，也是 mkdocs-ng 功能计划里排在最前面的开放项。

为什么要做这件事，可以用一组数据说明。我们做了一个规模测试：100 页、400 页、1600 页的站点，每页平均构建成本分别是 7.8 ms、9.3 ms、22.1 ms。成本不是线性的，页面越多单页越贵——这正是 #3695 描述的 O(N²) 导航渲染问题。文档站越大，serve 的体验越差。

CodSpeed 基线已经铺好，优化工作正在进行。等 1.9.0 发布，希望这组数字能明显降下来。也欢迎去 [feature plan](https://github.com/mkdocs-ng/mkdocs/issues/59) 留言，说说你在 serve 上最痛的点。

## 怎么切过来

还在用上游 `mkdocs` 包的话：

```bash
pip uninstall mkdocs
pip install -U mkdocs-ng
```

CLI、配置、插件都不变，只换包名。有一点要注意：1.8.0 起要求 Python 3.10+，Python 3.8、3.9 都已 EOL，这两个版本上 pip 会自动安装 1.7.x，不受影响。

如果你正在用 MkDocs，这几件事都能帮到项目：把依赖换成 `mkdocs-ng` 试试，遇到问题去 [GitHub](https://github.com/mkdocs-ng/mkdocs) 提 issue，给仓库点个 Star。愿意的话，也欢迎转给还在用 MkDocs 的同事，让他们知道上游之外还有一个在维护的选择。

仓库：[mkdocs-ng/mkdocs](https://github.com/mkdocs-ng/mkdocs) · 发布说明：[Release Notes](https://mkdocs-ng.github.io/mkdocs/about/release-notes/) · 上游问题修复清单：[Fixed Upstream Issues](https://mkdocs-ng.github.io/mkdocs/about/fixed-upstream-issues/) · 功能计划：[Feature Plan](https://github.com/mkdocs-ng/mkdocs/issues/59)

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
