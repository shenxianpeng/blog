---
title: 代码审查（Code Review）法则以及我的思考和实践
tags:
  - Review
  - PR
  - Code
categories:
  - DevOps
date: 2021-03-20 17:10:14
author: shenxianpeng
---

## 背景

代码审查，也称 Code Review 是让别人帮助你审查你的代码。

中国有句古话：三人行必有我师焉。Code Review 也一样，别人或许会有不一样的思考和简介，另外人总会犯错误的。Code Review 可以让合并到产品里的代码尽可能已最好的方式去实现，减同时少犯错误的几率，从而提高产品的代码质量。

既然 Code Review 的优势显而易见的好处多多，但现实中往往执行起来并不那么容易，效果也不见得那么好。那么问题出在哪里呢？

我认为主要是以下两点导致的：

首先，读别人代码需要花时间，往往还需要对方带着业务给你讲一遍代码，更行成本高。如果是远程或是跨时区则更加不易；
其次，如果Reviewers手头的工作也很多，工作压力大，在时间不允许，也很容易造成执行不到位。

那么如何才能比较好的开展Code Review？首先让我们先来看看大公司是怎么做的。Google 的这篇关于 Code Review 的文章里面提到了很多他们在具体的 Review 法则。

## Google 的代码审查法则

在进行代码审查时，应确保：

* 代码经过精心设计
* 该功能对代码用户很有帮助
* 任何 UI 更改都是明智的，并且看起来不错
* 任何并行编程都是安全完成的
* 代码没有比需要的复杂
* 开发人员没有实现他们将来可能需要的东西，但不知道他们现在需要什么
* 代码具有适当的单元测试。
* 测试经过精心设计
* 开发人员对所有内容使用了清晰的名称。
* 注释清晰实用，并且主要说明Why而不是What
* 代码已正确文档化（通常在g3doc中，Google内部工程文档平台）。
* 该代码符合我们的样式指南

确保检查要求你检查的每一行代码，查看上下文，确保你在改善代码运行状况，并称赞开发人员所做的出色工作。

> 原文：https://google.github.io/eng-practices/review/reviewer/looking-for.html

## 代码审查法的落地

可见，想要更好的落地Code Review，需要先要确立法则。作为技术Leader应传达既定的法则，让开发者有统一的编码意识。作为 Reviewers 应该熟知 Review 时候应当关注的点。

另外，结合我的经验，应该把法则里的具体规则通过流程、自动化则纳入到 Pull Request 的检查中。以下是一些不完全实践，供参考。
### 流程

**规避任何不经 Review 的代码进入到主分支**

> 以 Bitucket 为例。GitHub，GitLab 在设置上大同小异。

* 打开分支权限设置里的选项 `Prevent changes without a pull request` 打开它。另外，这个选项里也可以添加 Exception，就是这些人可以不通过 Pull Reuqest 来提交代码。

* 在 Merge Check 里开启 `Minimum approvals` 这个选项。比如设置 Number of approvals = 1，这样需要至少有一个 Reviewers 点击 Approve 按钮才允许 Merge。

### 自动化

**通过CI流水线验证编译和测试**

* 建立自动化构建和测试的 Pipeline，能够在创建 Pull Request 的时候，或是针对任何分支进行构建和测试。比如创建 Jenkins 的 Multi-branch pipeline。

* 开启 Bitucket 的 Merge Check 里 `Minimum successful builds` 选项，验证编译/测试结果，以防止任何没有通过编译和测试的代码进入主分支。

* 另外，可以通过自行编写工具来实现，或可以集成CI工具来做更多检查：

  * 针对 Pull Request 的修改历史来分析提交历史并推荐 Reiewer
  * 通过 Lint 工具来检查编码规范
  * 通过 REST API 检查是否需要压缩 Commits
  * 比如通过 SonarQube 检查 Quality Gate 等。

这样可以让 Reviewers 将审查的工作精力放在代码的具体实现上，其他交给工具来检查。

### 其他

Code Review做的好不好，团队的技术氛围也很重要。一个团队需要有位有领导力，有“品位”的技术大牛，这样的人会将他的“品味”影响到普通程序员的身上。

- 想象一下如果团队里绝大多数都是技术追求者，以写出优秀的代码乐此不疲，他们喜欢自己的产品... 他们提交的、Review过的代码不会差。

- 相反，那些仅仅为了完成绩效而不顾产品发展的“短期”的糟糕实现，不考虑重构... Review也就是走走过场。

如果你还有什么不同意见或建议，欢迎留言分享你的观点。
