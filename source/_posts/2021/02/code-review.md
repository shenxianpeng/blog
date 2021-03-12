---
title: 关于 Code Review 我的三个实践
tags:
  - Review
  - PR
categories:
  - DevOps
date: 2021-02-25 17:10:14
author: shenxianpeng
---

这篇文章就是结合我的工作经历对 Code Review 的简短的介绍。末尾附 Google Code Review 总结。

Code Review 每个人都知道它很好，应该去好好做，但往往执行起来效果并不好。一来读别人代码需要花时间，往往还需要对方给你讲；二来自己手头的工作也很多，时间不允许。因此，需要先从流程、自动化以及对重要修改这三个主要的地方做好。

## 流程上规避任何不经 Review 的代码进入到主分支

> 我使用的是 Bitucket，因此下面都是以 Bitucket 为例。GitHub 以及 GitLab 在设置上大同小异。

* 打开分支权限设置里的选项 `Prevent changes without a pull request` 打开它。另外，这个选项里也可以添加 Exception，就是这些人可以不通过 Pull Reuqest 来提交代码。

* 在 Merge Check 里开启 `Minimum approvals` 这个选项，我的设置 Number of approvals = 1，及比如有一人点击 Approve 按钮才允许 Merge

## 通过 CI/CD，自动化进行编译和测试验证

* 建立自动化构建和自动化测试的 Pipeline，能够在创建 Pull Request 的时候，或是针对任何分支进行构建和测试。比如 Jenkins 的 Multi-branch pipeline 功能。

* 当上面的 Pipeline 已经稳定，开启在 Bitucket 的 Merge Check 里 `Minimum successful builds` 选项，以防止任何没有通过编译和测试的代码进入主分支。

* 可以通过写一个小工具来分析每次的 Pull Request 里有哪些文件做了修改，假定这些文件过往的历史中哪个人修改的次数最多，就认为这个人对这部分的代码最为熟悉，然后推荐他来作为 Reiewer。这里的推荐机制可以再完善，这里只是提供一个思路。


## Reivew代码是一种责任

每个人作为 Reviewer，在点击 Approve 那个按钮其实是一份责任的。因此，如果你对要 Reivew 的代码不是特别有把握，那就要建议提交者引入更 Senior 的工程师来一起查 Review。

---

以下是 Google 关于 Code Review 的具体法则的总结，供参考。

> https://google.github.io/eng-practices/review/reviewer/looking-for.html

Summary

In doing a code review, you should make sure that:

* The code is well-designed.
* The functionality is good for the users of the code.
* Any UI changes are sensible and look good.
* Any parallel programming is done safely.
* The code isn’t more complex than it needs to be.
* The developer isn’t implementing things they might need in the future but don’t know they need now.
* Code has appropriate unit tests.
* Tests are well-designed.
* The developer used clear names for everything.
* Comments are clear and useful, and mostly explain why instead of what.
* Code is appropriately documented (generally in g3doc).
* The code conforms to our style guides.

Make sure to review every line of code you’ve been asked to review, look at the context, make sure you’re improving code health, and compliment developers on good things that they do.