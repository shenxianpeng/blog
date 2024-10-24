---
title: DevOps 工作的每一天
tags:
  - DevOps
categories:
  - DevOps
date: 2024-09-20 00:00:00
author: shenxianpeng
---

这篇文章我想介绍一下作为 DevOps 工程师的每一天工作内容，与大家分享和交流。我也想知道你们每天都在做什么事情。

那就开始吧。

## 愿景

我是从 2018 年开始从事 DevOps 的相关工作的。刚开始我的岗位和职责主要是 Build Engineer，负责产品的日常构建和发布。

但当我接手这份工作之后，由于我之前有过 Jenkins 和自动化的经验，我觉得我可以做非常多的改善，我想彻底把 Build 和 Release 变成自动化，并且还要是最佳实践的做法，彻底解放掉手动工作。

可能有人会觉得这是出力不讨好或是亲手毁掉自己的饭碗，但我不这么认为，我能过程中我可以学到很多，从而将以前用在手动执行的时间花费在维护自动化的事情上，且还有更多时间来做其他事情。这就是我当时的愿景。

## 实施

有了这一目标，我就开始了 DevOps 最佳实践，帮助我自己以及团队获得更高的效率。

* 配置即代码 (CaC) - 将所有构建从手动或 Bamboo 转移到 Jenkins，并创建 Jenkins Shared Library，以更好地管理自动构建和扩展。这为团队提供了自助服务和拉取请求构建，节省了团队的时间，也节省了我的时间。一旦发生灾难，CaC 可以快速恢复。
* 基础设施即代码（IaC）- 创建了 ansible-playbooks 和 mv-infra 仓库，用于管理构建、Jenkins 服务器和开发环境，IaC 帮助我们的团队快速配置开发/构建环境，防止业务发生灾难。
* 容器化（Dockerization）- 创建 Docker 镜像仓库，将产品 Docker 化，实现容器化，并且应用了很多 DevOps 最新实践，比如：Docker buildx bake 构建镜像，使用健康检查、pytest 和 CI/CD 测试镜像，使用 Renenote bot 管理依赖关系，以及使用 Kubernetes 部署 docker 镜像。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
