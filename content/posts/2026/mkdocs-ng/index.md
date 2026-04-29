---
title: 我又开始为爱发电了，正式维护 MkDocs 和 Material for MkDocs 这两个文档项目了
summary: |
  MkDocs 快两年没更新了，Material for MkDocs 也进了维护模式。作为重度用户，我 fork 了这两个项目，发布了 mkdocs-ng 和 mkdocs-ng-material，更新一下包名就能继续用。
tags:
  - OpenSource
  - MkDocs
authors:
  - shenxianpeng
translate: false
date: 2026-04-29
---

上周我在 GitHub 上创建了一个新组织，叫 [MkDocs NG][mkdocs-ng-org]。

然后一口气往 PyPI 上发了两个包：[`mkdocs-ng`][mkdocs-ng-pypi] 和 [`mkdocs-ng-material`][mkdocs-ng-material-pypi]。

这篇文章就说说我为什么要维护 MkDocs 和 Material for MkDocs 这两个项目，以及我做了什么。

## 背景

开源社区的文档工具中，MkDocs 和 Material for MkDocs 是我最喜欢的组合了。

我自己很多开源项目的文档项目都是用这两个工具构建的，完全满足了我对项目文档的需求：Markdown 写文档，YAML 配置，插件扩展，主题定制，部署简单。

但这两个项目最近的状态都不太好。MkDocs 已经快两年没更新了，Material for MkDocs 也进入了维护模式。

最近 cpp-linter 的小伙伴再次提到了 MkDocs 的停更问题，问要不要更新社区其他 Fork 或是转到 Zensical 上。（Zensical 是 squidfunk 团队的新项目）。

![起因](./1.png)

在我看了这些备选方案，以及这篇文章 [The Slow Collapse of MkDocs][collapse-article] 之后，我觉得 MkDocs 的是非太多了，也太狗血了，喜欢八卦的可以自己去看看。大概的脉络是这样的：

MkDocs 原作者长期缺席，社区维护者接力维持项目；后来维护者之间发生冲突，原作者重新介入但重点转向不兼容现有插件生态的 MkDocs 2.0 重写，导致原有 MkDocs 1.x 维护停滞，Material for MkDocs 进入维护模式，社区开始分裂出 ProperDocs、MaterialX、Zensical 等替代路线。具体细节非常“精彩”，强推那篇文章。

言归正传，看了现在的备选方案也不太满意，如果硬要我选的话，我可能会去尝试 Zensical。但它其实也不太成熟，生态还不够丰富。

对于我来说，最好的选择就是继续用 MkDocs 和 Material for MkDocs，但前提是它们能继续维护下去。

既然没有好的选项，那就不如自己来维护。一来可继续使用这两个文档工具，二是能让社区继续用这个工具，三是能满足我喜欢维护开源项目的兴趣。

于是就有开头提到的 MkDocs NG（Next Generation 的意思）GitHub 组织和 PyPI 包了。

## 我做了什么

说干就干。上周末我就 fork 了这两个项目，把 mkdocs/mkdocs 和 squidfunk/material 这两个仓库都 fork 到了 MkDocs NG 下面。

现在它们分别是：mkdocs-ng/mkdocs 和 mkdocs-ng/mkdocs-material。

这两个好哥们现在终于在一起了。抱抱！

然后我就把挂了很多的优先级高的 Bug 基本上都修了，升了依赖，追了 Python 新版本的兼容性，最后发了新版本。

* [mkdocs-ng][mkdocs-ng-pypi] 从 v1.7.0 发到 v1.7.2，一周内，发了三次 bugfix 版本。
* [mkdocs-ng-material][mkdocs-ng-material-pypi] 这边做了 rebrand、修了文档、Docker 镜像迁移到了 GHCR，发布了第一个 9.7.7 版本。

怎么使用呢？非常简单。

之前你安装的是 `mkdocs` 和 `mkdocs-material`，现在换成 `mkdocs-ng` 和 `mkdocs-ng-material` 就行了。

CLI 命令还是 `mkdocs`。配置文件还是 `mkdocs.yml`。插件和主题的命名空间都不变。

我还看到有人在社区里也做了 MkDocs 的 fork，叫 ProperDocs，委婉点说就是跟我的喜好不一致，不是他们的问题，是我的问题，所以我就干脆自己来维护了。

说实话，除了 Zensical 以外，其他的备选方案我都不是很满意。这也就是我为什么要自己来维护的原因了。

但我也在 [Discussion #4010][discussion-4010] 里表达过，如果上游的维护者愿意把我加入到他们的维护团队里，我也很乐意在上游继续维护，毕竟这样更好，用户也更方便。

---

## 最后，需要你帮忙

我能做的事很明确：修 bug、升依赖、发版本。

我做开源这些年有一个体会：一个项目有没有影响力，代码只是前半段，后半段是人。有多少人知道它、多少人愿意试、多少人顺手帮忙说一声。

如果你在用 MkDocs 或者 Material for MkDocs，几件事可以帮到我：

1. 把 `mkdocs` 换成 `mkdocs-ng`，`mkdocs-material` 换成 `mkdocs-ng-material`，试试新版本。
2. 遇到问题去 [GitHub][mkdocs-repo] 提 Issue，我会第一时间回复，能修的我会尽快修掉。
3. 给仓库点个 Star。不是虚荣——Star 多了，更多人会看到，更多人会用，这个 fork 才会服务到更多人。
4. 转发给同事，或者在群里说一下。我一个人能把代码维护好，但让这件事被更多人知道，**还是得靠大家**。

最后，附上两个仓库的链接：

- [mkdocs][mkdocs-repo]
- [mkdocs-material][mkdocs-material-repo]

欢迎大家来试用，提 Issue，点 Star，转发给同事！谢谢！

[mkdocs-ng-org]: https://github.com/mkdocs-ng
[mkdocs-ng-pypi]: https://pypi.org/project/mkdocs-ng/
[mkdocs-ng-material-pypi]: https://pypi.org/project/mkdocs-ng-material/
[collapse-article]: https://fpgmaas.com/blog/collapse-of-mkdocs/
[discussion-4010]: https://github.com/mkdocs/mkdocs/discussions/4010
[mkdocs-repo]: https://github.com/mkdocs-ng/mkdocs
[mkdocs-material-repo]: https://github.com/mkdocs-ng/mkdocs-material