---
title: Jenkins privilege management
summary: 本文介绍了如何在 Jenkins 中进行权限管理，包括如何设置 Job 的访问权限和执行权限，以确保安全和高效的 CI/CD 流程。
tags:
  - Jenkins
date: 2019-09-24
author: shenxianpeng
---

如何针对 Jenkins 里的不同 Job 进行不同的策略管理。比如某个 Job 所有人都可以查看，但仅限于某些人可以执行，这时候就需要对 Job 行程权限设置。

这里用的插件是 Role-based Authorization Strategy。安装成功后，打开要设置的 Job, 设置如下：


![Enable project-based security](jenkins-privilege-management.png)
