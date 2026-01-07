---
title: Git 分支策略
summary: |
  介绍大型项目的 Git 分支策略，包括 master、develop、release 和 hotfix 分支的作用和使用方法，帮助团队更好地管理代码和版本发布。
date: 2019-07-28
aliases:
  - /2019/07/git-branching-strategy/
tags: 
  - Git
  - DevOps
authors:
  - shenxianpeng
---

随着近些年 Git 的快速普及，想必无论开发还是测试在日常工作中都要用到 Git。

对于刚刚接触的 Git 的人来说，打开一个 Git 仓库，面对十几个甚至几十个分支时，有的人不理解，有的人云里雾里，为什么会创建这么多分支？

对于开发需要知道如何通过 Git 分支来管理产品的开发和发布，尤其是对于大型的项目的开发，只有 master 和 develop 分支是无法满足产品管理和发布要求的，我们还需要其他分支以便更好的管理产品代码。

对于测试更多的了解开发过程及分支管理有助于测试及开展自动化测试用例，可以针对不同的分支进行测试用例的编写，在以后回归测试里可以通过分支或是 tag 找到对应的测试用例。

## Git 分支策略

这是一个大型的项目的 Git 分支管理策略，了解这张图可以涵盖 99% 的产品需求。

![大型项目的 Git 分支策略图](diagram.png)

上面这张图大体上分为 master, hotfix, release, develop 分支：

* master - 只用于存放稳定版本的提交，且只限于 merge 操作。每次发布成功后，要将 release 分支的代码 merge 到 master 和 develop 分支，并且在 master 上打上相应的 tag，如图里的 v1.1, v1.1.01 等。

* develop - 开发分支是所有开发者最常用的分支，当前的 Bug 和 Features 都需要修复到这个分支上面去。需要每次创建 bugfix 或 feature 类型的分支，创建 Pull Request 进行代码 review，然后才能 merge 分支到 develop 分支上。

* release - 发布分支是在产品 code freeze 后创建的， 这时候测试要开始大规模的测试了，新创建的 release 分支是不允许开发再往里面添加有关 feature 的代码，只有测试发现 bug 并被开发修复的代码才允许通过 Pull Request 的方式 merge 到 release 分支里。如果开发要提交 feature 的代码只能提交到 develop 分支里。等到产品成功发布后会将 release 分支 merge 到 master 分支并打上相应的 tag （版本号），还要将 release 分支 merge 到 develop 分支。

* develop - 开发分支是所有开发者最常用的分支，当前的 Bug 和 Features 都需要修复到这个分支上面去。

这个图有几个关键点：

* hotfix 分支是从最新的 hotfix 分支上创建的
* hotfix 分支发布后将会合并到 develop 分支
* release 分支是从 develop 分支上创建的
* release 分支发布后将会合并到 develop 和 master 分支
* release 分支上发现的缺陷将会修复到 release 分支

如果你是那 1% 不能满足的产品需求，欢迎留言。
