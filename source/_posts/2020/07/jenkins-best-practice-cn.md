---
title: Jenkins 三个最佳实践
tags:
  - Jenkins
  - DevOps
categories:
  - Jenkins
date: 2020-07-03 18:57:02
author: shenxianpeng
---

在使用 Jenkins 做了一年多的 CI/CD，我有三个最重要的实践想和你分享。

1. Configuration as Code（配置即代码）
2. Jenkins shared libraries（Jenkins 共享库）
3. Multi-Branch Pipeline（多分支流水线）

## Configuration as Code

Configuration as Code 是一种在代码仓库里管理配置的方法。

它有什么好处呢？

### 1. 作业透明化

<!-- more -->

对于哪些使用过使用 Bamboo（或 Jenkins 1.0 的人）的人来说，你们都知道想要从 GUI 页面熟悉一个构建 job 的逻辑是多么的困难，尤其是对于不太了解这个工具的人更是难上加难。因此当我从 Bamboo 迁移到 Jenkins 的时候，我就决定使用 Configuration as Code，因为代码对于工程师来说更易读和了解其中的逻辑。

### 2. 可追溯性

对于 GUI 页面来说另外一个重要问题就是无法追溯修改历史，来看到别人做了什么。能看到别人修改了什么这种功能对于一些很重要的 Job 是非常重要的，像是 Build Jobs 等。把 Jenkins 的配置当作项目代码来管理，这样做的好处不仅在于可跟踪性，还在于在需要时可以回滚到特定版本。

### 3. 快速恢复

将配置作为代码使用还有另一个好处，即能够在硬件问题上快速恢复Jenkins作业。但是，如果 Jenkins 作业是通过 GUI 配置的，当托管 Jenkins 的服务器损坏时，你的业务可能面临丢失与 Jenkins 相关的所有东西的风险。所以，从业务连续性角度来看，它也暗示我们使用配置代码。

## Jenkins Shared Libraries

接下来是 Jenkins 共享库。就像编写任何应用程序代码一样，我们需要创建函数、子例程以实现重用和共享。同样的逻辑也适用于 Jenkins 的配置代码。发送电子邮件、打印日志、将 build 放到 FTP/Artifactory 等功能都可以放到 Jenkins 共享库中。Jenkins 共享库也是在代码仓库中管理的。

如你所见，这些 groovy 文件是所谓的共享库，完成了发送电子邮件、git 操作、更新开源等工作。
因此，我们为什么要使用共享库变得非常清楚，因为它可以减少重复代码。

```bash
xshen@localhost MINGW64 /c/workspace/cicd/src/org/devops (develop)
$ ls -l
total 28
-rw-r--r-- 1 xshen 1049089 5658 Jun 18 09:23 email.groovy
-rw-r--r-- 1 xshen 1049089  898 Jun 13 20:05 git.groovy
-rw-r--r-- 1 xshen 1049089 1184 Jun  8 12:10 opensrc.groovy
-rw-r--r-- 1 xshen 1049089 1430 Jul  3 10:33 polaris.groovy
-rw-r--r-- 1 xshen 1049089 2936 Jul  3 10:32 trigger.groovy
drwxr-xr-x 1 xshen 1049089    0 Jun  8 12:10 utils/
-rw-r--r-- 1 xshen 1049089  787 May 12 13:24 utils.groovy
```

它也更容易维护，因为我们不需要更新多个位置，而只需要在需要更改时更新共享库。最后它鼓励重用和跨团队共享。例如，我创建的共享库也被公司其他团队使用。

## Multi-branch pipeline

接下来多分支流水线。在下面这张图中，开发的每个 Pull Request 将触发自动构建，这对开发工程师非常有帮助，因为除它的分支代码通过构建测试和冒烟测试，否则他们的更改将不会合并到主干分支上。

![Pull Request 流程图](jenkins-best-practice-cn/pull-request.png)

在幕后工作的东西叫做 Jenkins 多分支流水线。在进入细节之前，让我们先看看它是什么样子的。

![Multi-Branch Pepeline Branches](jenkins-best-practice-cn/multi-branches.png)

所以，你可以从这个页面看到，有很多 Jenkins Job。这是因为对于 Bitbucket 中的每个 bugfix 或 feature 分支，这个多分支流水线会自动为它们创建一个 Jenkins Job。

> 注意：如果你的分支已经删掉了，这些分支则会从这个多分支 Job 里删除掉，或是像上面那样显示划掉状态，这取决你 Jenkins 的设置。

![Multi-Branch Pepeline Pull Requests](jenkins-best-practice-cn/multi-pull-request.png)

> 注意：如果你的 Pull Request 不是 Open 状态，那么这个 PR-xx Job 将会从这里删除，或是像上面那样显示划掉状态，这取决你 Jenkins 的设置。

因此，当开发人员完成他们的工作时，他们可以使用这些 Jenkins Job 来自己创建正式的构建，而不需要构建工程师的参与。然而，过去的情况并非如此。在我们还没有这些自助服务工作的时候，开发人员总是向构建工程师寻求帮助，为他们创建构建。我们的团队中有大约 20 名开发人员，可以想象满足这些需求所需的努力。

因此，我刚刚介绍了这个多分支流水线的第一个好处，它为团队创建了一个自助服务，节省了他们的时间，也节省了我的时间。

这种自助式构建和安装的另一个好处是：使我们的主分支将更加稳定，并节省我们花费在调查谁的提交存在问题上的时间，因为只有通过构建、安装和冒烟测试的代码才会合并到主分支中。

现在，您可能想知道这项工作的价值，比如这个自动构建和安装测试发现了多少问题。

以我们最近一个月的开发为例，上个月合并了大约 30 个 Pull Request，发现其中 6 个在某些平台上存在 Build 问题。

大家都知道，如果我们能在开发阶段就发现问题，而不是被测试、支持人员甚至客户发现，那么这种质量成本就会非常低。

这就是我今天的分享。你对此有什么问题或是觉得有帮助欢迎评论或转发。


