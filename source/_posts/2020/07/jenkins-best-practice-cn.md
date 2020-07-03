---
title: Jenkins 的三个最佳实践
tags:
  - Jenkins
  - DevOps
categories:
  - Jenkins
date: 2020-07-03 18:57:02
author: shenxianpeng
---

在用 Jenkins 做了几年的 CI/CD，我有三个最重要的实践想和你分享。

1. Configuration as Code（配置即代码）
2. Jenkins shared libraries（Jenkins 共享库）
3. Multi-Branch Pipeline（多分支流水线）

## Configuration as Code

Configuration as Code 是一种在代码仓库里管理配置的方法。

它有什么好处呢？

第一，Jenkins Job透明化。对于哪些使用过使用 Bamboo（或 Jenkins 1.0 的人）的人来说，你们都知道想要从 GUI 页面熟悉一个构建 job 的逻辑是多么的困难，尤其是对于不太了解这个工具的人更是难上加难。因此当我从 Bamboo 迁移到 Jenkins 的时候，我就决定使用 Configuration as Code，因为代码对于工程师来说更易读和了解其中的逻辑。

第二，可追溯性。对于 GUI 页面来说另外一个重要问题就是无法追溯修改历史，来看到别人做了什么。能看到别人修改了什么这种功能对于一些很重要的 Job 是非常重要的，像是 Build Jobs 等。Configuration as Code 我们可以把配置




