---
title: 在 GitHub 上开源一个 Python 项目需要考虑哪些
tags:
  - GitHub
  - OpenSource
categories:
  - DevOps
date: 2020-07-15 11:38:24
author: shenxianpeng
---

现如今越来越多的公司如果选择开源，他们的首选发布的代码管理仓储就是 GitHub。

与个人在 GitHub 上发布开源项目不同，公司在做开源之前需要考虑如下这些问题。

1. 是否要放到公司级的 GitHub 的公共账户上？

    通常是把代码放在一个公司级的账户上面，公司的 GitHub 管理员将你的个人账户作为 Member 加到 GitHub 这个组里。

2. Python 项目如果要发布到 PyPI 上，使用公共账户发布吗？

    据我观察，这个取决于公司。比如Amazon, IBM 他们一些发布到 PyPI 上 Python 项目使用的是个人账户，像是苹果和微软，他们有一些指定的账户用来发布。

    Amazon：[emukit](https://github.com/amzn/emukit) 的发布使用的是个人账户 [apaleyes](https://pypi.org/user/apaleyes/) 和 [mmahsereci](https://pypi.org/user/mmahsereci/)

    IBM：以这个项目 [causallib](https://github.com/IBM/causallib) 为例使用的是私人账户 [ehudk](https://pypi.org/user/ehudk/) 和 [yishais](https://pypi.org/user/yishais/)

    Apple：这个项目 [coremltools](https://github.com/apple/coremltools) 使用的是一个指定账户 [coremltools](https://pypi.org/user/coremltools/)

    Microsoft：使用一些直送的账户来发布到 PyPI 上，比如 [nni](https://pypi.org/user/nni/) 和 [glep](https://pypi.org/user/glep/)

    因此，这取决于公司的流程和安全策略。

3. 使用允许用户的 bugfix 或 feature 分支的 Pull Request 合并到主分支？

    目前 GitHub 无法关闭 Pull Request 的功能。

4. 内部开发者是直接使用 GitHub 还是使用内部的代码管理工具，将更新同步到 GitHub 上？

    如果接受用户的 Pull Request 当然内部开发者直接在 GitHub 工作更为方便，而无需同步不同仓库之间的代码来减少合并冲突和不必要的流程。

5. 是否允许用户在 GitHub 上创建 Issues？

    绝大多数的项目都会默认允许用户在 GitHub 上创建 Issue，有一些项目是例外的（GitHub 的 Issue 功能可以手动关闭），比如 [Jenkins](https://github.com/jenkinsci/jenkins)，他们只允许用户在他们自己的 Jira 系统里提 [issue](http://issues.jenkins-ci.org/)

    好处：保持原有流程不变；Jira 更加强大的过滤以及生成 Dashboard 功能。
    不足：用户提 Issue 前需要先注册，提高创建 issue 门槛。

6. 版本号是如何规定的？从 `0.1.0` 开始呢还是从 `1.0.0` 开始？

7. 使用什么样的 Lincense？是 MIT 还是 Apache-2.0 License 等等。

