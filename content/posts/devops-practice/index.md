---
title: DevOps 实践
summary: 本文介绍了 DevOps 实践的核心概念、目标和实施方法，强调了持续集成、持续交付和自动化的重要性。
date: 2018-04-14
tags:
- DevOps
translate: fase
author: shenxianpeng
---

我想大多数的团队都面临这样的问题：

1. 发布周期长
2. 开发和测试时间短

3. 开发和测试是两个独立的团队
4. 不稳定的交付质量
5. 低收益难维护的UI自动化测试脚本
6. 不合理的测试权重分配

解决方法：

引入 DevOps 和分层自动化

* 组件化产品
  * 产品开发引入模块化，数据驱动会使得产品更加容易实施 Unit，Server，UI 自动化测试
* 优化工程师
  * 开发和测试在未来将没有界限，他们都是开发者，都会产品的质量和客户负责
* 分层自动化
  * 更合理的测试权重分配，更底层的测试收益越高
* 引入工具
  * 实施DevOps引入必要的工具，Bitbucket, Jenkins, Sonar, Pipelines, Docker, test framework …
