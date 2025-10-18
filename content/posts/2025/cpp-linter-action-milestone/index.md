---
title: 微软、NASA 都在用？我用业余时间维护了 4 年的项目破百了
summary: |
  cpp-linter-action 是一个 GitHub Action，提供 C/C++ 代码的格式化和静态分析功能。它使用 clang-format 和 clang-tidy，支持多种配置和自定义规则。项目自 2021 年创建以来，已被多个知名组织和开源项目使用。
tags:
  - clang-format
  - clang-tidy
  - clang
  - cpp-linter
authors:
  - shenxianpeng
date: 2025-04-15
---

上周，我创建并维护的开源项目 [cpp-linter-action](https://github.com/cpp-linter/cpp-linter-action) 迎来了一个小小的里程碑：

> 🌟 GitHub Star 数突破 100！

虽然这个数字不算大，但对我来说是一个小小的里程碑——这是我第一次有项目在 GitHub 上获得超过 100 个 Star，也可以算是对这个项目的认可，给了我持续维护的动力。

我在这个项目的第一次提交是在 **2021 年 4 月 26 日**，一晃将近 4 年过去了。回头看看这段时间，挺庆幸自己一直没有闲着，也留下了一些对别人有用的东西。

随着项目不断发展，用户也越来越多。根据粗略估算，目前已经有上千个项目在使用这个 Action。

其中不乏一些知名组织和开源项目，比如：

* Microsoft
* Apache
* NASA
* CachyOS
* nextcloud
* Jupyter

最重要的是，这个过程让我收获了很多新的技能和知识，也让我保持了一个「业余习惯」：

> 手机上除了刷微信、抖音，还有 GitHub。

这个项目也成为了我后续工作的一个起点。我后来创建了 [cpp-linter](https://github.com/cpp-linter) 组织，和其他开发者一起维护并发布 `clang-tools` 的二进制版本和 Docker 镜像。同时也开发了 [cpp-linter-hooks](https://github.com/cpp-linter/cpp-linter-hooks)，为用户提供 `clang-format` 和 `clang-tidy` 的 pre-commit hook，使用起来更加方便。

不谦虚的说：

> 如果你的项目是用 C/C++ 开发，如果想使用 `clang-format` 和 `clang-tidy`，那么 cpp-linter 会是一个绕不开的选项。

最后，欢迎大家提出意见或建议，也欢迎通过 [Issue](https://github.com/cpp-linter/cpp-linter-action/issues) 或 [Discussions](https://github.com/orgs/cpp-linter/discussions) 与我交流！

如果你觉得这个项目对你有帮助，也欢迎在公众号「DevOps攻城狮」留言或者去 GitHub 点个 Star，支持下这个项目～

—— 写于 2025-04-15 12:49 AM

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
