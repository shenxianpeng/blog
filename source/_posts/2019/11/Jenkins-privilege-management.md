---
title: Jenkins privilege management
tags:
  - Jenkins
  - Authorization
categories:
  - Jenkins
date: 2019-09-24 15:40:23
author: shenxianpeng
---

如何针对 Jenkins 里的不同 Job 进行不同的策略管理。比如某个 Job 所有人都可以查看，但仅限于某些人可以执行，这时候就需要对 Job 行程权限设置。

这里用的插件是 Role-based Authorization Strategy。安装成功后，打开要设置的 Job, 设置如下：

![Enable project-based security](Jenkins-privilege-management\jenkins-privilege-management.png)
