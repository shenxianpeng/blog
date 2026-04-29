---
title: 我又开始为爱发电了：正式维护 MkDocs 和 Material for MkDocs
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

上周，我在 GitHub 上创建了一个新的组织，叫 [MkDocs NG][mkdocs-ng-org]。

然后一口气往 PyPI 上发布了两个包：

- [`mkdocs-ng`][mkdocs-ng-pypi]
- [`mkdocs-ng-material`][mkdocs-ng-material-pypi]

简单来说，我 fork 了 MkDocs 和 Material for MkDocs，并开始维护它们。

这篇文章就简单聊聊：为什么我要做这件事，以及目前已经做了什么。

## 为什么是 MkDocs？

在开源社区的文档工具里，MkDocs + Material for MkDocs 一直是我最喜欢的组合。

Markdown 写文档，YAML 做配置，插件可以扩展，主题足够漂亮，部署也简单。

我自己的很多开源项目，文档都是用这套工具搭建的。对我来说，它几乎满足了一个开源项目文档站的全部需求。

但最近这两个项目的状态，确实不太理想。

MkDocs 从 2024 年 8 月后就没有新版本发布了；Material for MkDocs 从 2025 年 11 月也进入了维护模式。

最近 cpp-linter 的小伙伴也再次提到了这个问题：我们是不是应该切换到社区里的其他 fork，或者迁移到 Zensical？

Zensical 是 squidfunk 团队的新项目，也可以理解成 Material for MkDocs 之后的新方向。

![起因](./1.png)

我顺着这个问题看了一圈，也读了这篇文章：[The Slow Collapse of MkDocs][collapse-article]。

这篇文章把 MkDocs 这几年的维护问题梳理得比较完整。大概脉络是：原作者长期缺席，社区维护者接力维持项目；后来维护者之间出现分歧，原作者重新介入，但重点转向了不兼容现有插件生态的 MkDocs 2.0 重写。结果就是 MkDocs 1.x 的维护停滞，Material for MkDocs 进入维护模式，社区开始出现 ProperDocs、MaterialX、Zensical 等不同方向的替代路线。

细节比我这里写的复杂得多，感兴趣的可以自己去读原文。

但对我来说，结论其实很简单：

**我仍然喜欢 MkDocs 和 Material for MkDocs，也希望它们能继续被维护下去。**

如果一定要选一个替代方案，我可能会去尝试 Zensical。但它现在还不够成熟，生态也还没有完全起来。

所以对我来说，最现实的选择不是立刻迁移，而是继续维护现在这套已经被大量项目使用的工具。

既然还没有特别满意的替代方案，那就自己来维护。

于是就有了 MkDocs NG。

NG 是 Next Generation 的意思。

## 我做了什么？

说干就干。

上周末，我把两个项目都 fork 到了 MkDocs NG 组织下面：

- `mkdocs/mkdocs` → `mkdocs-ng/mkdocs`
- `squidfunk/material` → `mkdocs-ng/mkdocs-material`

这两个长期搭配使用的项目，现在终于放在同一个组织下面维护了。

然后我开始处理一些优先级比较高的问题：修 bug、升级依赖、适配新的 Python 版本，并发布了新版本。

目前进展是：

- [`mkdocs-ng`][mkdocs-ng-pypi] 从 `v1.7.0` 发布到 `v1.7.2`，一周内发了三个 bugfix 版本。
- [`mkdocs-ng-material`][mkdocs-ng-material-pypi] 完成了 rebrand、文档调整、Docker 镜像迁移到 GHCR，并发布了第一个 `9.7.7` 版本。

使用方式也很简单。

如果你之前安装的是：

```bash
mkdocs
mkdocs-material
```

现在可以换成：

```bash
mkdocs-ng
mkdocs-ng-material
```

CLI 命令仍然是：

```bash
mkdocs
```

配置文件还是：

```bash
mkdocs.yml
```

插件和主题的命名空间也保持不变。

也就是说，大多数情况下，你只需要改一下依赖包名，就可以继续使用原来的 MkDocs 工作流。

## 为什么不是其他 fork？

我也看到了社区里其他人做的 fork，比如 ProperDocs。

这里不想评价谁好谁坏。开源里每个人的目标、取舍和维护方式都不一样。

只是从我自己的需求出发，我更希望保留 MkDocs 和 Material for MkDocs 现有的使用体验，尽量减少迁移成本，同时继续修 bug、升依赖、发版本。

所以我选择自己维护一个 fork。

当然，我并不希望无意义地分裂社区。

我也已经在 [MkDocs Discussion #4010][discussion-4010] 里表达过：如果上游维护者愿意把我加入维护团队，我也很乐意直接在上游继续维护。

这对用户来说是最好的方式。

但在那之前，我会先把 MkDocs NG 维护下去。

## 最后，需要你帮忙

我能做的事情比较明确：

修 bug、升级依赖、适配新版本、发布新版本。

但做开源这些年，我越来越明显地感觉到：

**一个项目有没有影响力，代码只是前半段，后半段是人。**

有多少人知道它，多少人愿意试，多少人愿意顺手帮忙说一句，都会影响这个项目能不能继续走下去。

如果你正在使用 MkDocs 或 Material for MkDocs，下面几件事都可以帮到我：

1. 把 `mkdocs` 换成 `mkdocs-ng`，把 `mkdocs-material` 换成 `mkdocs-ng-material`，试试看新版本。
2. 遇到问题去 [GitHub][mkdocs-repo] 提 Issue，我会尽快回复，能修的我会尽量修掉。
3. 给仓库点个 Star。不是为了虚荣，而是 Star 多了，更多人会看到，更多人会愿意尝试。
4. 如果你身边也有人在用 MkDocs，可以转发给同事，或者在群里简单说一声。

我一个人可以把代码维护起来，但让更多人知道这件事，还是得靠大家。

最后，附上两个仓库：

- [mkdocs][mkdocs-repo]
- [mkdocs-material][mkdocs-material-repo]

欢迎试用、提 Issue、点 Star，也欢迎转发给正在使用 MkDocs 的朋友。

谢谢大家。

[mkdocs-ng-org]: https://github.com/mkdocs-ng
[mkdocs-ng-pypi]: https://pypi.org/project/mkdocs-ng/
[mkdocs-ng-material-pypi]: https://pypi.org/project/mkdocs-ng-material/
[collapse-article]: https://fpgmaas.com/blog/collapse-of-mkdocs/
[discussion-4010]: https://github.com/mkdocs/mkdocs/discussions/4010
[mkdocs-repo]: https://github.com/mkdocs-ng/mkdocs
[mkdocs-material-repo]: https://github.com/mkdocs-ng/mkdocs-material
