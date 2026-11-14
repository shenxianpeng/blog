---
title: MkDocs 停更之后，现有站点该往哪儿走
summary: |
  PyPI 上的 mkdocs 包一周还有 430 万次下载，最后一个版本却停在 2024 年 8 月。现有站点能走的路有五条：留在 1.6.1、上游 2.0、ProperDocs、Zensical 和 MkDocs NG。这篇用公开可查的数据把它们放在一起比：插件能不能跑、命令和 CI 要不要改、构建速度、谁在维护、能维护多久。
tags:
  - Open Source
  - Documentation
authors:
  - shenxianpeng
date: 2026-11-14
series: ["MkDocs NG"]
series_order: 5
---

过去 7 天，PyPI 上的 `mkdocs` 包被下载了 430 万次。它最后一次发版是 1.6.1，2024 年 8 月 30 日。

1.6.1 今天照样能构建，但新报的 bug 没人修，声明支持的 Python 只到 3.12。和它一起装得最多的主题 Material for MkDocs 也进入了维护模式，[2027 年 5 月 5 日停止维护](https://zensical.org/upcoming-changes/)，从 9.8.0 起每次构建都会打印一条通知提醒这件事。

这篇想回答一个具体的问题：手上已经有一个 MkDocs 站点，2026 年该怎么选。

先交代立场：我是 [MkDocs NG](https://mkdocs-ng.org/) 的维护者，下面比较的对象里就有我自己的项目。所以我只写能查证的事实，数字都附来源或复现方法，对其他项目的描述以它们自己的文档为准。事实核对于 2026 年 11 月 14 日。写错或过时的地方，欢迎在评论区或 [issue](https://github.com/mkdocs-ng/mkdocs/issues) 里指出，我会改。

## 五条路

1. **留在 MkDocs 1.6.1**，什么都不改。
2. **上游 MkDocs 2.0**。它以预发布版的形式发在 `mkdocs` 包下，最新是 2.0.dev6（2026-09-15）。这是一次重写：没有配置文件、插件和主题，看到 `mkdocs.yml` 会报错退出。现有站点用不了它，下文不再展开。要提防的是 `pip install --pre` 或 `uv --prerelease allow` 会把它装进来。
3. **[ProperDocs](https://properdocs.org/)**，MkDocs 1.6 的 fork。按它自己的介绍，团队成立于 2026 年 3 月，前身是 mkdocs-community 组织，目标是保留 MkDocs 1.x 和它的功能。有自己的包名和命令 `properdocs`。
4. **[Zensical](https://zensical.org/)**，Material for MkDocs 团队做的新生成器，核心用 Rust 写，能读现有的 `mkdocs.yml`。11 月 5 日发布 0.1.0，进入为期三个月的 beta，之后转为稳定版。
5. **MkDocs NG**，我维护的 MkDocs 1.x fork，包名 `mkdocs-ng`，命令和配置都不变。

彻底换到 Docusaurus、Starlight 或 Sphinx 也是一条路，但那等于重写站点，不在这篇的范围里。

## 一张表看现状

| | MkDocs 1.6.1 | ProperDocs | Zensical | MkDocs NG |
| --- | --- | --- | --- | --- |
| 版本 | 1.6.1 | 1.6.7 | 0.1.1 | 1.11.2 |
| 发布日期 | 2024-08-30 | 2026-03-20 | 2026-11-10 | 2026-11-11 |
| 包名 | `mkdocs` | `properdocs` | `zensical` | `mkdocs-ng` |
| 命令 | `mkdocs` | `properdocs` | `zensical` | `mkdocs` |
| 配置文件 | `mkdocs.yml` | `properdocs.yml` 或 `mkdocs.yml` | `mkdocs.yml` 或 `zensical.toml` | `mkdocs.yml` |
| MkDocs 插件 | 能 | 能 | 不能，原生重写了 33 个 | 能 |
| MkDocs 主题 | 能 | 能 | 不能，自带主题读 Material 的配置 | 能 |
| `hooks` 和 `gh-deploy` | 有 | 有 | 不支持 | 有 |
| Python | 3.8–3.12 | 3.9+ | 3.11+ | 3.10+ |
| 近 7 天下载量 | 430 万 | 54.5 万 | 51.2 万 | 616 |

下载量来自 [pypistats.org](https://pypistats.org/)（11 月 14 日查询），统计的是安装次数，不是站点数，被其他包当作依赖装进来的也算在内。比如 `mkdocs-redirects`、`mkdocs-gen-files`、`mkdocs-literate-nav`、`mkdocs-section-index` 这几个常用插件现在同时依赖 `mkdocs` 和 `properdocs`，装它们就会把两个都装上。

MkDocs NG 那一栏的 616 次也说明了一件事：它现在用的人很少。这一点先放在前面说清楚。

## 选之前，先回答四个问题

### 1. 你的站点用了哪些插件？

这一条最先看。打开 `mkdocs.yml`，看 `plugins:` 和 `hooks:` 两段。

ProperDocs 和 MkDocs NG 都直接运行 MkDocs 插件，插件不用换。

Zensical 不运行 MkDocs 插件。它把常用的插件用原生方式重新实现了一遍，目前[清单](https://zensical.org/docs/compatibility/mkdocs/plugins/)上有 33 个，另有 3 个 git 相关的插件在计划中。它的文档写明，不在清单上的插件，配置会被静默忽略，构建不报错，所以迁移前要逐个对一遍。

我拿 MkDocs NG 兼容性测试里的 26 个热门插件对照了一下 Zensical 的清单：

- **13 个已支持**：mkdocstrings、macros、glightbox、mike、redirects、rss、markdown-exec、include-markdown、minify、awesome-nav、literate-nav、markdownextradata、autorefs。
- **2 个在计划中**：git-revision-date-localized、git-authors。
- **11 个不在清单上**：techdocs-core、mkdocs-jupyter、mermaid2、monorepo、awesome-pages、encryptcontent、static-i18n、bibtex、kroki、swagger-ui-tag、gen-files。其中有的可以替代，比如 Mermaid 图 Material 主题本来就内置支持，用不着 mermaid2。

只用了前 13 个的站点，Zensical 是一条走得通的路。用了后面那些的，要么找替代，要么选能跑插件的工具。

### 2. 能不能改命令和 CI？

MkDocs NG 只换包名：依赖里把 `mkdocs` 换成 `mkdocs-ng`，`mkdocs build`、`mkdocs.yml`、CI 脚本和 `.readthedocs.yaml` 都不用动。插件的依赖里写着 `mkdocs` 也没关系，`mkdocs-ng` 和它装在一起时，运行的是 MkDocs NG。

ProperDocs 要换成 `properdocs` 命令，Zensical 要换成 `zensical build` 和 `zensical serve`，CI 里调用命令的地方要跟着改。两者都能读现有的 `mkdocs.yml`。Zensical 不提供 `gh-deploy`，部署要换成别的方式，比如 GitHub Actions 的 Pages 部署。

### 3. 用的是什么主题？

大多数 MkDocs 站点用的是 Material for MkDocs。它 2027 年 5 月 5 日之后不再维护，在那之前要定一个去向：

- **Zensical**：同一个团队做的，外观和配置延续 Material，最接近"原厂"路线。Material 的模板覆盖（`overrides/`）基于 9.6.18 及以后版本的，[一般能直接用](https://zensical.org/docs/compatibility/mkdocs/migration/)；更老或改动很多的要对比测试，因为它的模板引擎是 MiniJinja，不能调用 Python 函数。
- **[MkDocs NG Material](https://material.mkdocs-ng.org/)**（`mkdocs-ng-material`）：我在 NG 组织下维护的 Material fork。主题名还是 `material`，换两行依赖。2027 年 5 月 5 日之后继续修安全和兼容问题，不加新功能。
- **[MaterialX](https://github.com/jaywhj/mkdocs-materialx)**：另一个延续 Material 的项目，加了自己的新功能，依赖 ProperDocs。
- **[Sumi](https://sumi.mkdocs-ng.org/)**：我给 MkDocs NG 做的新主题，现在是 0.4.0，还很年轻。

用 MkDocs 内置主题或其他第三方主题的站点，Zensical 跑不了，ProperDocs 和 MkDocs NG 都能跑。用内置主题的站点换到 ProperDocs 时，还要多装一个 `properdocs-theme-mkdocs` 包，ProperDocs 构建时会提示。

### 4. 需要它维护多久，谁在维护？

这一条最难量化，我把能查到的列出来：

- **Zensical** 背后是 Zensical LLC，也就是 Material 的原班团队，部分开发经费来自 Spark、Studio 这些付费产品。全职团队、有资金，这是它最大的优势。
- **ProperDocs** 由 ProperDocs 团队维护，最近一次发版是 2026 年 3 月 20 日的 1.6.7。
- **MkDocs NG** 在[版本与支持](https://mkdocs-ng.org/about/release-notes/#versioning-and-support)里承诺：1.x 的 bug、安全和兼容修复至少持续到 **2028 年 12 月 31 日**；如果出了新的大版本，1.x 还会再收至少 12 个月安全修复，而且无论如何不会早于这个日期结束。发版由 GitHub Actions 通过 PyPI 可信发布完成，每个文件都有签名证明。弱点也写在[治理文档](https://mkdocs-ng.org/about/governance/)里：目前只有我一个维护者，找第二个维护者是项目最重要的待办。

## 插件兼容是怎么测的

MkDocs NG 仓库里有一套[兼容性测试](https://github.com/mkdocs-ng/mkdocs/tree/main/compat)：从[插件目录](https://catalog.mkdocs-ng.org/)里按热度挑出 32 个常用的插件、主题和 Markdown 扩展，每个搭一个小站点，分别用上游 MkDocs 1.6.1 和 MkDocs NG 以 `--strict` 模式构建，有警告也算失败。每个 PR 都会跑，每周一还定时跑一次，赶上插件的新版本。

11 月 11 日 1.11.2 发版那次的结果：MkDocs 1.6.1 通过 32/32，MkDocs NG 通过 32/32。

这套测试也有边界：它只证明这些插件在小站点上能构建成功，覆盖不了每个插件的所有选项；PlantUML 和 Kroki 两个只验证到能加载，因为渲染要连外部服务。你的站点用了什么特别的组合，还是要自己构建一次才算数。

## 构建速度

速度不该是选型的第一标准，但总有人问，所以测了。

同一份 1000 页的生成站点、同一台 4 核 Linux 机器、Python 3.13，每个工具清空输出后构建 5 次，取中位数。测试时间 2026 年 11 月 14 日，脚本是 MkDocs NG 仓库里的 [`benchmarks/compare.py`](https://github.com/mkdocs-ng/mkdocs/tree/main/benchmarks)，可以在自己的机器上复现。

| 工具 | 主题 | 耗时 |
| --- | --- | --- |
| MkDocs NG 1.11.2 | 内置 `mkdocs` | 6.4 秒 |
| MkDocs NG 1.11.2 | Material（`mkdocs-ng-material` 9.8.1） | 8.7 秒 |
| MkDocs NG 1.11.2 | Sumi 0.4.0 | 9.3 秒 |
| Zensical 0.1.1 | 自带主题（基于 Material） | 12.4 秒；保留缓存 4.6 秒 |
| ProperDocs 1.6.7 | 内置 `mkdocs` | 13.0 秒 |
| MkDocs 1.6.1 | 内置 `mkdocs` | 13.3 秒 |
| ProperDocs 1.6.7 | Material 9.8.1 | 24.1 秒 |
| MkDocs 1.6.1 | Material 9.8.1 | 25.7 秒 |

几点要一起看：

- **Zensical 有构建缓存**。保留缓存、没有改动时重新构建，它最快。MkDocs NG 目前没有跨构建的缓存。
- **比较要同类对同类**。Zensical 的主题基于 Material，所以最接近的对比是带 Material 的那几行。
- **规模变了，排序也会变**。11 月初在 5000 页的站点上（当时是 MkDocs NG 1.11.0rc1 和 Zensical 0.0.74），带 Material 的 MkDocs NG 要 134.5 秒，Zensical 清空缓存 185.7 秒、保留缓存 59.2 秒。Material 每一页都带着完整导航，这个站点光 HTML 就有 4 GB 多。
- **`mkdocs serve` 改一页到看到结果**，11 月 4 日测的 1000 页站点上，Zensical 和 MkDocs NG（内置主题）都是 1.2 秒，带 Material 的 MkDocs NG 是 2.7 秒，MkDocs 1.6.1 和 ProperDocs 每次都整站重建，要 18 秒左右。

这只是一种生成出来的站点，你的站点结果可能不同。如果你发现哪个工具的配置测得不公平，告诉我，我改。

## 怎么选

按上面四个问题，大致可以这样分：

- **站点要原样继续构建，插件一个不换**：MkDocs NG 或 ProperDocs。区别在于 MkDocs NG 保留 `mkdocs` 命令，ProperDocs 换成 `properdocs`。
- **用 Material，插件都在 Zensical 的清单上，也愿意换工具**：Zensical。原班团队、有资金、带缓存的构建很快，是 Material 用户最自然的去向。
- **用 Material，但用了 Zensical 不支持的插件或 `hooks`，或者现在不想换工具**：MkDocs NG 加 `mkdocs-ng-material`，换两行依赖，2027 年 5 月 5 日之后也有人修。
- **暂时留在 1.6.1**：短期能用，但要清楚 bug 不再修，新的 Python 版本不在它声明的支持范围里。

不管选哪个，都可以先在一个分支上试，不影响线上：

```sh
# MkDocs NG：加一个包，命令不变
pip install mkdocs-ng
mkdocs build --strict

# ProperDocs
pip install properdocs
properdocs build --strict

# Zensical
pip install zensical
zensical build --strict
```

`--strict` 会把警告当成错误，最容易暴露迁移问题。构建通过后，再打开几个用到插件的页面对比一下。想退回去，卸掉新装的包就行。

MkDocs NG 的详细迁移步骤在[切换到 MkDocs NG](https://mkdocs-ng.org/user-guide/migrating/)，和其他项目更完整的对比在[对比页面](https://mkdocs-ng.org/about/comparison/)，Material 用户可以看 [Material for MkDocs 停止维护后怎么办](https://mkdocs-ng.org/user-guide/material-end-of-life/)。

用 MkDocs NG 迁移时遇到问题，请开 [issue](https://github.com/mkdocs-ng/mkdocs/issues)；这篇文章里对其他项目的描述有不准确的地方，也请告诉我。
