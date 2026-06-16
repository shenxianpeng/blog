---
title: 原本只想提个文档 PR，结果项目进了 Jenkins 官方组织
summary: |
  我写了一个验证 Jenkinsfile 的小工具，原本只是想让它出现在 Jenkins 官方的开发工具列表里。结果 Jenkins 维护者提议：不如直接把项目转进 jenkinsci 组织？这篇文章记录了从 PR 到 transfer 再到官方博客的完整过程，包括中间踩的一个很有意思的坑。
tags:
  - Jenkins
  - Open Source
  - pre-commit
  - Pipeline
authors:
  - shenxianpeng
date: 2026-06-09
---

大家好，我是沈工。

最近我维护的一个个人项目 [jenkinsfilelint](https://github.com/jenkinsci/jenkinsfilelint)，正式从我的 GitHub 账号下搬到了 [jenkinsci](https://github.com/jenkinsci) 官方组织。

整个过程前后大概两周，中间遇到的一些问题也挺有意思的。今天就写一篇文章来聊聊这个过程。

首先先介绍一下 jenkinsfilelint 这个工具。

简单说，它是一个 [pre-commit](https://pre-commit.com/) hook，能在你 `git commit` 的时候自动把 Jenkinsfile 发到你自己的 Jenkins 服务器上做语法校验。

```bash
% git commit -m "Update Jenkinsfile"
jenkinsfilelint..........................................................Failed
- hook id: jenkinsfilelint
- exit code: 1

Errors encountered validating Jenkinsfile:
WorkflowScript: 17: Expected a step @ line 17, column 11.
             test
             ^
```

底层原理是它调用 Jenkins 自带的 Pipeline Linter API：

```
$JENKINS_URL/pipeline-model-converter/validate
```

类似于你手动去 Jenkins 服务器上的 "Pipeline Syntax" 页面粘贴你的 Jenkinsfile 测试是否有语法问题，

这个项目是将这个过程的体验更好，在你修改并提交 Jenkinsfile 之前就能发现语法错误。

项目从去年 11 月开始写，到今年 5 月已经发了几个版本，PyPI 上也能装：

```bash
pip install jenkinsfilelint
```

我自己用着挺顺手，我就想，可以让更多 Jenkins 用户也用上这个工具。

于是我就开了一个 PR 想把它放到 Jenkins 官方的开发工具列表里 [Pipeline Development Tools](https://www.jenkins.io/doc/book/pipeline/development/) 页面。

于是 5 月 30 号，我给 jenkins.io 仓库提了一个 PR：[jenkins-infra/jenkins.io#9183](https://github.com/jenkins-infra/jenkins.io/pull/9183)，把 jenkinsfilelint 加到 Development Tools 页面里。

PR 提交之后，Jenkins 社区的维护者 [dduportal](https://github.com/dduportal) 和 [krisstern](https://github.com/krisstern) 很快就给了反馈。

他们的担心我能理解：这个项目只有我一个人维护，质量怎么样？能不能长期维护下去？直接放到官方文档里推荐，是不是不够稳妥？

但接下来 dduportal 提了一个我完全没想到的建议：

> thinking aloud, I am not sure about the exact process but what would you think about moving the project into jenkinsci?

他问我是否想把项目直接转到 Jenkins 官方组织下面。

我看到这一回复心里的第一反应是：什么时候转？😂

这比放在我个人账号下有更多的曝光，另外还是我继续维护，何乐而不为？

事后想想可能是几个原因促使他提这个建议：

1. Jenkins 官方生态中确实没有一个 pre-commit hook 来校验 Jenkinsfile 的语法，这个工具填了一个空白
2. 或许是我在 Jenkins 社区里已经有了一定的信用积累（因为维护 Explain Error Plugin）

总之，这个提议我当然不会拒绝，于是回复：

> I'd be honored to transfer jenkinsfilelint to the jenkinsci organization and continue maintaining it there.

确定了要贡献这个项目到官方组织之后，接下来就是怎么把项目转过去了。

我是希望通过 GitHub 的仓库 transfer 功能直接转过去的，因为如果官方 fork + detach 的话，release history、issue、PR 这些都没了，这对已经有发布历史的项目来说不够友好。

但我发现我没有权限直接把仓库转到 jenkinsci 下面，即使我是 jenkinsci 的成员也不行。会直接报错。

> You don't have the permission to create public repositories on jenkinsci

那怎么办？

后来 Jenkins 社区有人回复我说，可以先将项目转到 jenkinsci-transfer 这个 org 下面，然后再由 Jenkins 管理员从 jenkinsci-transfer 转到 jenkinsci。

流程大概是这样的：

1. Jenkins 管理员先把我邀请进 jenkinsci-transfer
2. 我把仓库从我个人账号 transfer 到 jenkinsci-transfer
3. Jenkins 管理员再把仓库从 jenkinsci-transfer transfer 到 jenkinsci

这个流程虽然多了一个步骤，但可能是目前唯一可行的方式。它的好处：

- **解决了权限问题**：我不需要在 jenkinsci 里有更高的权限，只需要被邀请进 jenkinsci-transfer 就行，那下面一个仓库都没有。
- **解决了信任问题**：我不可能把仓库 transfer 给一个陌生人 —— jenkinsci-transfer 是 Jenkins 官方认证的 org，不是某个人的小号。我的仓库转过去之后不会丢，也不会被截胡
- **保留了完整历史**：两次 transfer 都不会丢失 commit、release、issue、PR 等任何数据

转完之后我就被“踢”出 jenkinsci-transfer 了，仓库留在了 jenkinsci 下面了。

如果你以后也需要将项目贡献给某个大型开源社区，这套流程或许能作为一个参考。

好了，项目转到 jenkinsci 下面了，但还没有在 Jenkins 官方文档里出现，这个工具的曝光度还是有限的。

于是就有了我在 jenkins.io 的第一篇 blog 了。[Introducing jenkinsfilelint: Catch Jenkinsfile Errors Before You Commit](https://www.jenkins.io/blog/2026/06/08/jenkinsfilelint-pre-commit/)

这篇博客的内容主要是介绍 jenkinsfilelint 是什么、为什么要用它、怎么用它。

我觉得这个事情给我带来了以下几个思考：

1. 如果你有一些项目解决了一个特定的问题，或许可以把它贡献给或者提案给更有影响力的社区。虽然不是每个社区都像 Jenkins 这么友好、能够接受你的项目，但不试试怎么知道呢？不试试你不知道未来会发生什么。

2. 在 AI 出现的时候，我有很长一段时间觉得开源没有前途了，或者不想做开源了。但是最近，或者说是过了那段时间之后，我又回到了开源的初心上面，还是觉得喜欢做开源，喜欢做有影响力的事情。

我觉得开源是一个比较漫长的事情，可能你现在做了不会激起任何浪花，但可能在一两年之后才可能慢慢结果。

---

最后

jenkinsfilelint 现在已经在 [github.com/jenkinsci/jenkinsfilelint](https://github.com/jenkinsci/jenkinsfilelint) 了。功能上还是那个功能，但位置不一样了——从一个人的 side project，变成了 Jenkins 官方生态里的一员。

如果你也在用 Jenkins Pipeline，不妨试试把它加到你的 `.pre-commit-config.yaml` 里。提交之前就能发现语法错误，比你 push 上去等 CI 跑完才发现快多了。

老司机们，我们下期见～

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
