---
title: 通过 Jenkins-X 社区最终进入到 Jenkins 基础设施团队成为 SRE 的经历
summary: 本文介绍了 Hervé Le Meur 如何通过 Jenkins-X 社区的贡献，最终成为 Jenkins 基础设施团队的一名 SRE，并分享了他的经历和对 Jenkins 的看法。
tags:
  - Jenkins
  - Contributor
translate: false
author: shenxianpeng
date: 2024-04-21
---

今天翻译一篇我在 [Jenkins Contributors](https://contributors.jenkins.io/) 页面上看到的一篇文章。

其作者是 Hervé Le Meur，我早在关注 Jenkins-Infra 的项目的时候就关注到他，他是一个法国人。以下是关于他如何通过 Jenkins-X 社区最终进入到 Jenkins 基础设施团队成为 SRE 的经历。

**说实话有点羡慕。希望这个分享能给每一个想加入开源、并且在开源组织中找到一份全职工作带来一点启发。**

以下是我对[原文](https://contributors.jenkins.io/pages/contributors/herve-le-meur/)的翻译：

---

Hervé Le Meur 是一名 SRE（网站可靠性工程师），目前是 Jenkins 基础设施团队的成员。他是通过 Jenkins X 进入开源社区的，随后转到 Jenkins 基础设施工作。

Hervé 的父亲是一名木匠，母亲是一名室内装潢师，他出身于一个模拟技术背景的家庭，但在六岁时就通过 Amstrad CPC 464 电脑第一次真正接触到了技术。

如今，在不从事 Jenkins 任务的时候，Hervé 喜欢和家人一起到户外散步、阅读和观看自己喜欢的节目。


## 在加入 Jenkins 之前，你的背景是什么？

大学毕业后，我在一家小型 B2B 营销咨询公司工作了 10 年，当时我是开发我们所用工具的万事通，但那里既没有 CI/CD，也没有开源。

之后，我进入一家建筑信息建模（BIM）软件公司，从软件开发人员做起。有些团队在使用 Jenkins，但对他们来说，当时的 Jenkins 看起来既麻烦又缓慢。

随着我逐渐成长为软件架构师，我的任务是基于 Jenkins X 建立一个新的 CI/CD，这花了我几个月的时间。
由于 Jenkins X 刚刚出炉，而我又是 Kubernetes 的新手，这项任务比预期的要困难得多，尤其是 Jenkins X 进入测试阶段后，我不得不多次重做大部分工作。

通过这项工作，我学到了很多关于 Kubernetes 和 CI/CD 的知识，同时也为 Jenkins X 做出了不少贡献。
被这份工作解雇后，我联系了 [James Strachan](https://www.jenkins.io/blog/authors/jstrachan/) 和 [James Rawlings](https://www.jenkins.io/blog/authors/jrawlings/)，他们给了我一个链接，让我从 CloudBees 公司的 [Oleg Nenashev](https://www.jenkins.io/blog/authors/oleg_nenashev/) 那里获得一个职位空缺，也就是我现在的职位。

在我的脑海中，我是一名程序员，而不是系统管理员。因此，当 [Mark Waite](https://www.jenkins.io/blog/authors/markewaite/) 解释说最后一轮面试将与人际网络有关时，我有点害怕。
我以为我会因此失去机会，因为这可能是不可能完成的任务。然而，当我与 Mark、[Damien Duportal](https://www.jenkins.io/blog/authors/dduportal/) 和 [Olivier Vernin](https://www.jenkins.io/blog/authors/olblak/) 面谈时，他们却问我如何将 CI/CD 与 Jenkins X 集成：这真是一次奇妙的经历。我们进行了有意义的讨论，这让我感觉更舒服，也让我更容易做出决定。

面试前15分钟，我收到了另一家公司（ Damien 和 [Jean-Marc Meessen](https://www.jenkins.io/blog/authors/jmmeessen/) 之前恰好在这家公司工作过）的最终录用通知，当时我犹豫了一下，但结果是最好的，因为我现在仍然是 Jenkins 项目的一员，这可以说是我梦寐以求的工作。

我还有过主持在线论坛的经验，所以社区部分的工作对我来说很熟悉。

## 你使用 Jenkins 多久了？

我从 Jenkins X 开始，但从未接触过 Jenkins 本身。除了共享 Jenkins 的名称外，它们没有任何共同之处。
我对 Jenkins 的预想是负面的。我认为它是一个笨重、过时、复杂的 Java 程序。这些印象都是我在以前的公司里从其他使用它的人那里听来的。然而，当我开始使用 Jenkins 后，这种对比简直是天壤之别。
我的先入之见是，与其他程序相比，它既笨重又缓慢。我并不是唯一一个认为 Jenkins 不一定是最好、最快或最新的项目的人，但事实证明，一旦我开始使用这个项目，我就错了。

## 为什么选择 Jenkins 而不是其他项目？

我并不一定选择 Jenkins，因为它是我工作的主要部分。当我开始查看 Tyler、Olivier、Damien 和 Mark 为 Jenkins 基础设施所做的工作时，我意识到 Jenkins 比我想象的要完善和高效得多。
我还喜欢我们使用 Jenkins 开发和发布 Jenkins 的事实。这种用法是独一无二的，因为大多数开源工具都不具备转发成功的能力。
Jenkins 花费了大量的时间和精力，以配合开发人员的流程和功能。在我看来，这是 Jenkins 成功的主要原因之一。Jenkins 还集成了 Terraform、Puppet、Kubernetes 和 Helmfile 等其他工具，但 Jenkins 仍然是这些工具的协调者。

对我来说，为 Jenkins 工作是我的最高成就，因为我一直喜欢创建和开发工具，即使不是开发 Jenkins 的核心。

## 加入 Jenkins 项目后，你看到 Jenkins 有哪些增长？

我们已经有越来越多的实例被定义为代码。因此，我们可以重新创建任何实例，而无需手动配置设置，这大大提高了我们的恢复能力。我们还在慢慢实现将 ci.jenkins.io 定义为代码并进行管理。

## 你对 Jenkins 的哪方面特别感兴趣？

现在，我正在重构 Jenkins 控制器和代理的官方 Docker 镜像的构建过程，这让我感到非常有趣。
我也喜欢在贡献者方面工作，因为这就像一个谜题，知道我需要达到什么目标以及我的起点会让我更愉快。

## 什么样的贡献最成功或最有影响力？

[Basil Crow](https://www.jenkins.io/blog/authors/basil/) 提出了使用 SQLite 代替文件系统的有趣想法。改用 JDK 17 非常成功，随着 JDK 21 的推出，Jenkins 可以在更新的平台上运行，并跟上时代的进步。
由于我们喜欢让 Jenkins 基础架构保持领先（例如始终运行最新的 Jenkins Weekly），下一步将引入 JDK22。插件健康分数标识对于可视化整个插件生态系统的健康状况非常有用。

## 给新开发人员和开源社区新成员的建议

首先要提醒我的是项目的庞大性，并指示我一开始要选择一件事来专注。

不要犹豫，大胆尝试；开源意味着对所有人开放。不要害怕提交 pull request，它并不需要完美无缺。

你可能最终会喜欢它，并继续提交贡献！

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
