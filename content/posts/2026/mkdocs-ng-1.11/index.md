---
title: MkDocs NG 1.11.0 发布：维护 MkDocs 这半年，比我预想的走得更远
summary: |
  接手维护 MkDocs 半年，上游点赞最多的 15 个 open issue 修掉了 10 个，1.11.0 支持一个 mkdocs.yml 构建多语言站点，干净构建比上游 1.6.1 和 Rust 写的 Zensical 都快。顺便介绍 MkDocs NG 自己的主题 Sumi。
tags:
  - Open Source
  - Documentation
authors:
  - shenxianpeng
date: 2026-11-04
series: ["MkDocs NG"]
series_order: 4
---

半年前，我写了一篇《[我又开始为爱发电了：正式维护 MkDocs 和 Material for MkDocs](/zh-cn/posts/2026/mkdocs-ng/)》，开始维护 MkDocs。之后又陆续写了 [v1.7.x 的进展](/zh-cn/posts/2026/mkdocs-ng-update/)和 [1.8.0 的发布](/zh-cn/posts/2026/mkdocs-ng-1.8/)。

11 月 4 日，MkDocs NG 1.11.0 发布了，正好借这个机会，聊聊这半年发生了什么。

## MkDocs 现在的处境

我相信很多人做项目、写文档时都用过 MkDocs。Markdown 写内容，YAML 做配置，插件随便装，再配上 Material 主题，几分钟就能搭出一个像样的文档站。

但这两年，MkDocs 出了两个问题。

**一是 1.x 不再维护了。** 上游最后一个 1.x 版本是 2024 年 8 月的 1.6.1，之后两年多没有新版本，社区报告的 bug 也就一直挂在那里。

**二是 2.0 是一次彻底的重写。** 上游把精力放在了 MkDocs 2.0 上，但它目前还是预发布版本（最新是 2026 年 9 月的 2.0.dev6），没有插件、没有主题，遇到 `mkdocs.yml` 会直接报错退出。现有的站点没法直接升级上去，整个插件生态也跟不过去。

对用户来说，要么停在一个不再修 bug 的老版本上，要么承担很高的迁移成本。

社区里也出现了几个方向：

- **[Zensical](https://zensical.org/)**：Material for MkDocs 原班团队的新项目，核心用 Rust 写，目前是 0.0.74。它能读 `mkdocs.yml`，但不运行 MkDocs 插件，而是把三十个左右常用插件用原生方式重新实现。
- **[ProperDocs](https://properdocs.org/)**：MkDocs 前维护者发起的 1.6 fork，换了包名和命令名。最后一个版本 1.6.7 发布于 2026 年 3 月，之后七个多月没有新版本。

每个项目都有自己的目标和取舍，这里不评价谁好谁坏。我只说说我自己的看法。

## 我更在意愿力

很多人看一个 fork，第一反应是：是不是原班人马？

我觉得这没那么重要。原作者可以离开，原班人马也可以有新的方向，这都很正常。一个项目能不能走下去，要看有没有人**愿意**长期维护、持续改进。没有这份意愿，原班人马也一样会停下来。

我为什么有这份愿力？

因为我做开源这些年，几乎每个项目的文档都是用 MkDocs 搭的。我是它的重度用户，它好不好用、哪里卡手，我有切身的感受。

所以接手的时候，我没想着给它变出什么新花样。目标很朴素，就是**这条供应链不能断**。我自己还要继续用 MkDocs 构建文档，大家的插件也要能继续用。

## 上游的高赞 Issue，基本清完了

接手以来，我花时间最多的，是修上游遗留的问题，尤其是点赞最多的那些。

把上游现在还开着的 Issue 按点赞数排序，前 15 个里：

- **10 个已经在 MkDocs NG 里修掉了**。比如点赞最多的 `mkdocs serve` 不监听文件变化（[#4032](https://github.com/mkdocs/mkdocs/issues/4032)，70 个赞）、livereload 必须手动加参数（[#4055](https://github.com/mkdocs/mkdocs/issues/4055)）、内置主题依赖 CDN（[#2171](https://github.com/mkdocs/mkdocs/issues/2171)）、没有可编程调用的 Python API（[#1240](https://github.com/mkdocs/mkdocs/issues/1240)）、`INHERIT` 只能继承一个文件（[#2624](https://github.com/mkdocs/mkdocs/issues/2624)）、外链没有 `rel="external"`（[#3914](https://github.com/mkdocs/mkdocs/issues/3914)）。
- **1 个大幅改善**：`mkdocs serve` 的性能和写作体验（[#3695](https://github.com/mkdocs/mkdocs/issues/3695)），下面会讲到。
- 剩下 4 个：一个是玩笑贴（[#892](https://github.com/mkdocs/mkdocs/issues/892)，"No beer me button"），另外三个是缓存清除、搜索插件拆包、主题与核心解耦，属于架构层面的改动，排在 1.12。

完整的清单在 [Fixed Upstream Issues](https://mkdocs-ng.org/about/fixed-upstream-issues/) 页面，目前列了 27 个上游 Issue。

## 1.11.0 带来了什么

1.11.0 是 1.9.0 之后的第一个正式版，没有破坏性变更，1.9 能用的配置、主题和插件都照常工作。几个重点：

- **一个 `mkdocs.yml` 搞定多语言。** 新的 `languages` 配置项，默认语言放在站点根目录，其他语言放到 `/zh/`、`/de/` 下面。翻译文件就放在原文旁边（`page.zh.md`），没翻译的页面自动回退到默认语言，链接不会断。每种语言都是一次普通构建，插件不需要做任何改动。详见 [Multi-language Sites](https://mkdocs-ng.org/user-guide/multi-language-sites/)。
- **`mkdocs serve` 快了很多。** 没变的页面不再重新转换、重新渲染。1000 页的站点，保存后看到修改的时间从 5.1 秒降到了 0.9 秒左右（默认主题）。
- **装什么插件都不会把 MkDocs NG 换掉。** 以前装某些插件或主题，会把 MkDocs NG 悄悄换回上游 1.6.1；有些插件还会打印"请切换到 ProperDocs"的警告。现在这两个问题都没有了。
- **为编辑器和 AI 做好准备。** `mkdocs new` 生成的新站点自带 `llms.txt` 和 `AGENTS.md`；`mkdocs.yml` 有了 JSON Schema，编辑器能自动补全和校验配置。
- 还有一些小改进：GitHub 风格的 `> [!NOTE]` 提示框能直接渲染、8000 端口被占用时自动换一个端口、`docs_dir: .` 可以用了。

完整内容见 [Release Notes](https://mkdocs-ng.org/about/release-notes/)。

## 最大的意外：AI

这半年最大的意外，是 AI 带来的变化。

以前一个人维护一个项目，精力是最大的瓶颈。现在我只要把愿景和取舍讲清楚：要什么、不要什么、什么绝对不能破坏，AI 就能帮我把实现、测试、文档一起做出来。

举个例子：从 10 月 31 日到 11 月 4 日，五天里 MkDocs NG 发了 1.9.0、1.10.0rc1、1.11.0rc1 和 1.11.0 四个版本。放在以前，一个人业余时间根本做不到。

当然，方向还是要我自己来定。不改命令名、不改配置文件名、不破坏插件，这几条从第一天起就没变过。AI 也提过加一个 `mkdocs-ng` 命令，被我否了。

## 没想到，它成了最快的那一个

另一个意外是性能。

在这么多 fork 和替代品里，MkDocs NG 的干净构建反而是最快的。这跟我一直盯着性能有关。

从 1.8.0 开始，每个 PR 都会在 [CodSpeed](https://codspeed.io/) 上跑性能基准测试，只要有一点性能下降，合并之前就会被揪出来。在这个前提下不断优化：导航渲染从 O(N²) 降下来、`serve` 复用没变的页面、搜索插件读取页面快了三倍，一点一点把速度提上来了。

我们用同一份 1000 页的 Markdown，在同一台 4 核机器上，对各个工具做了干净构建（不带缓存）：

![1000 页站点的干净构建时间对比：MkDocs NG + Material 11.5 秒，Zensical 17.4 秒，MkDocs 1.6.1 + Material 34.8 秒](build-speed.svg)

| 工具 | 主题 | 时间 |
| --- | --- | --- |
| MkDocs NG 1.11 | 默认主题 | 7.9 秒 |
| MkDocs NG 1.11 | Material | 11.5 秒 |
| MkDocs NG 1.11 | Sumi | 12.0 秒 |
| Zensical 0.0.74 | 自带（基于 Material） | 17.4 秒 |
| ProperDocs 1.6.7 | 默认主题 | 18.8 秒 |
| MkDocs 1.6.1 | 默认主题 | 18.9 秒 |
| MkDocs 1.6.1 | Material | 34.8 秒 |

同样用 Material 主题，MkDocs NG 是 11.5 秒，上游 1.6.1 是 34.8 秒，时间只要原来的三分之一；不带缓存时，也比 Rust 写的 Zensical（17.4 秒）快。

但也要说清楚几点，免得误导：

- Zensical 有构建缓存，**保留缓存时**它只要 6.4 秒，比我们快。MkDocs NG 目前没有跨构建的缓存。
- `serve` 热更新上，Zensical 是 0.8 秒，我们在 1.11.0 里做到了 0.9 秒左右，基本追平，但还没超过。
- Zensical 还在 0.0.x，后面肯定也会继续变快。

测试方法和脚本都公开在 [Build speed](https://mkdocs-ng.org/about/comparison/#build-speed)，欢迎在自己的机器上复现。

从 1.6.1 到 1.11，语言没换，还是 Python。快出来的部分，全是导航不再每页重渲染、没变的页面不再重算这类改动。

## Sumi：MkDocs NG 自己的主题

最后介绍一下 [Sumi](https://sumi.mkdocs-ng.org/zh/)。

Sumi 是日语"墨"的意思：纸、墨与一方朱印。它是我为 MkDocs NG 做的文档主题，设计理念借鉴了 [Oink](https://oink.pgsty.com/)。几个特点：

- **组件就是原生 Markdown。** 提示框是 `> [!NOTE]`，步骤是带 `{.steps}` 的列表，标签页是带 `{tab="…"}` 的代码块。没有 MDX、没有短代码，源文件在 GitHub 上一样好读。
- **本地优先。** 字体、2000 个图标、搜索、Mermaid、KaTeX 都随主题一起发布，不依赖 CDN，内网也能用。Mermaid 和 KaTeX 只在用到的页面加载。
- **⌘K 搜索，中文日文都能搜。** 搜索框同时也是命令面板。
- **也为 AI 而写。** 每个页面都有一份干净的 Markdown 副本，站点有 `llms.txt`，一键复制为 Markdown。
- **一套设计覆盖整个项目站。** 文档、首页、博客、发布下载页、整站打印版，都在一起。
- **保留你的 MkDocs 内容。** Admonition、`pymdownx` 标签页、`mike` 多版本、Material 的 `extra` 配置都能继续用。

MkDocs NG 的[官网](https://mkdocs-ng.org/)、Sumi 自己的文档、[插件目录](https://catalog.mkdocs-ng.org/)，都是用 Sumi 搭的。

试一下只需要三步：

```sh
pip install mkdocs-sumi
```

```yaml
# mkdocs.yml
theme:
  name: sumi
  locale: zh

plugins:
  - search
  - llms_txt
  - sumi
```

```sh
mkdocs serve
```

## 怎么切过来

如果你的站点还在用上游 `mkdocs`，可以先用 uv 在临时环境里试一下，不会动你现有的环境：

```sh
uvx --from mkdocs-ng --with-requirements requirements.txt mkdocs build --strict
```

没问题的话，正式切换只要一行，不需要先卸载 `mkdocs`：

```sh
pip install -U mkdocs-ng
```

命令还是 `mkdocs`，配置还是 `mkdocs.yml`，插件和主题都不用改。想切回去，也是一行。详见[迁移指南](https://mkdocs-ng.org/user-guide/migrating/)。

## 最后

半年前那篇文章里我说过：一个项目有没有影响力，代码只是前半段，后半段是人。

代码这半年我已经尽力了，接下来需要你的帮忙：

- **试一试 Sumi 和 MkDocs NG**，把你的文档站跑起来看看。
- **遇到问题、有需求，就去提 [Issue](https://github.com/mkdocs-ng/mkdocs/issues)**。路线图在 [#59](https://github.com/mkdocs-ng/mkdocs/issues/59)，欢迎留言说说你最想要什么。
- **欢迎贡献**，不管是代码、文档、翻译，还是在[插件目录](https://catalog.mkdocs-ng.org/)里补一个你常用的插件。
- 如果觉得有用，给 [mkdocs-ng/mkdocs](https://github.com/mkdocs-ng/mkdocs) 和 [mkdocs-ng/mkdocs-sumi](https://github.com/mkdocs-ng/mkdocs-sumi) 点个 Star，或者转发给身边还在用 MkDocs 的朋友。

官网：[mkdocs-ng.org](https://mkdocs-ng.org/) · Sumi：[sumi.mkdocs-ng.org](https://sumi.mkdocs-ng.org/zh/) · 插件目录：[catalog.mkdocs-ng.org](https://catalog.mkdocs-ng.org/)

谢谢大家。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
