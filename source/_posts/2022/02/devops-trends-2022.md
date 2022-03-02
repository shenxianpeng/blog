---
title: 2022 年最值得关注的 DevOps 趋势和问答
tags:
  - DevOps
  - Kubernetes
  - DevSecOps
categories:
  - DevOps
author: shenxianpeng
date: 2022-02-24 11:27:18
---

DevOps 是 IT 界最近几年的一个热门话题，而且还会越来越热。

最近有幸和一位做传播咨询的读者朋友交流关于 2022 年最值得关注的 DevOps 趋势以及一些问题和回答，分享给大家。

## 行业趋势

### 趋势一：转向无服务器计算

无服务器计算是一种新兴趋势，实际上已经存在了十多年。企业购买无服务器框架需要一段时间，主要是因为对行业支持和对投资回报的担忧。

无服务器具有许多越来越难以忽视的优势，主要的两个最大好处是效率和可靠性。没有基础设施管理的负担，企业可以将资源集中在正重要的事项上。此外，无服务器还降低了传统框架可能出现的潜在维护问题的风险。

无服务器提供固有的可扩展性和可靠性并自动化开发人员不喜欢的日常操作任务，2022 年无服务器计算会经历下一次发展。

### 趋势二：微服务架构增长

随着无服务器计算在 2022 年的发展，微服务也将如此。

微服务架构是将单体应用分化为小的独立单元，或服务，从而为大型团队提供了更大的灵活性。它有以下优势：

* 为企业提供比单体应用程序更好的可扩展性和敏捷性
* 开发人员可以使用他们熟悉的编程语言和工具，消除传统应用程序开发的局限
* 开发人员能够在不破坏整个代码库的情况下部署小的特性或功能
* DevOps 团队可以根据业务需求来扩展每个应用部分，而不是一次性扩展整个应用
* 出现问题微服务可以轻松控制问题，而不会中断整个应用程序

当然也必须认识到微服务的一个弊端，如果实施不佳可能导致严重问题，包括数据丢失、可靠性差和安全风险。

### 趋势三：Kubernetes 成为基础架构

Kubernetes，也称 K8s，是容器编排开源平台，它能够与容器组交互，同时管理更多集群。除了容器管理，还提供安全、网络和存储服务，自我监控，节点和容器的健康状况检查。它可以处理从虚拟机集群管理到负载平衡等所有方方面面，提高生产力，简化 DevOps 开发、测试和部署流程。

根据 Flexera 的 2021 年云计算状况报告，48% 的企业使用 Kubernetes，另有 25% 的企业计划使用它。另外 53% 的组织使用 Docker，21% 的组织计划使用。

### 趋势四：DevSecOps 成为重要组成部分

安全性正在成为 DevOps 领域的另一个日益关注的问题。

为了避免网络攻击，许多大型企业正在将安全性集成到他们的 DevOps 流程中。从 DevOps 到 DevSecOps 的转变预计在 2022 会有更多公司在软件开发生命周期的早期加入安全控制。
这使 DevOps 团队能够在开发阶段持续监控和修复安全缺陷，从而提高交付速度和质量。DevSecOps 正在成为许多公司组织结构图的重要组成部分。

## 行业问答

<!-- more -->

### 问题一: DevOps 整个目前行业头部本土和国际玩家有哪些（GitLab)？

以我所在的外企而言通常是选择国际玩家，以最常用的代码管理和项目管理的工具为例：

* 上了年头的外企大公司通常在使用 Atlassian 家的 Jira 和 Bitbucket。船大难掉头，选择 GitLab，GitHub 这样一站式的 DevOps 迁移成本很高，需要有足够的理由才可能换工具。
* 对于年轻的公司，GitLab 和 GitHub 都是很好的选择。GitLab 在企业内部建立私服居多；GitHub 也提供企业版私服，但对于开源项目而言 GitHub 依然是代码托管的首选。

其他用到的付费级 DevOps 工具还包括 Synopsys (Polaris, Blackduck)，Jfrog (Artifactory)，SonarQube 等。

### 问题二: 行业目前有哪些重点趋势？比如安全这块，是不是目前行业关注度比较高？有哪些工具？

安全领域的关注度在逐年升高，尤其在外企很注重安全这块，他们愿意花钱来购买安全扫描工具来扫描代码，甚至还会要求所有的发布的产品代码中不能有高危漏洞。

一些常用的工具包括：静态代码扫描，比如 Polaris, Veracode, Snyk, SonarQube, PVS-Studio；代码组成分析，比如 Blackduck，X-Ray 等等。

### 问题三：企业在选择 DevOps 平台时主要考虑的因素有哪些？比如数据库安全，公司成熟度，海外知名度，等等

我认为主要考虑公司的知名度，其次产品的知名度，如果是开源产品会着重关注 GitHub 上的 Contributors 数量，它更能代表社区的活跃度，其次是 Fork 和 Star 数量。

### 问题四：目前 DevOps 处于哪个阶段? 未来的发展机会是在哪里？

DevOps 市场目前处在相对成熟的阶段，每个细分领域都有很多工具可以选择。未来基础设施会更多的向容器云方向发展。

具有创新的 DevOps 产品依然会很有市场，像是 GitLab，HashiCorp 等公司的产品，他们在短短十年内成为世界级的软件公司。

### 问题五：有哪些主流或平时重点关注的行业媒体号或自媒体公众号？

会经常看一些 DevOps 相关的以及 InfoQ，阿里、腾讯、美团等技术公众号。

还会看 YouTube 上一些 DevOps 的个人及公司频道：TechWorld with Nana, CloudBeesTV，CNCF，DevOps Paradox，DevOps Toolkit 等。

### 问题六：除了公众号外，你平时会上哪些行业社区？比如说 GitHub 或 CSDN？

最常看的是 GitHub 以及 GitHub Trending 来看最近受关注的项目。还会

社区会定期去看 [DEV Community](https://dev.to/), [Medium](https://medium.com), [InfoQ](https://www.infoq.cn/) 。会看知乎上一些话题下的精华，很少看 CSDN，懂得都懂。

## 参考

* [Top DevOps Trends to Watch in 2022](https://www.itbusinessedge.com/development/devops-trends-2022/)
* [DevOps Trends To Look Out for in 2022](https://blog.qasource.com/devops-trends-to-look-out-for-in-2022)

---

![ ](https://github.com/shenxianpeng/shenxianpeng.github.io/blob/master/about/index/qrcode.jpg?raw=true)

关注公众号「DevOps攻城狮」（转载本站文章请注明作者和出处，请勿用于任何商业用途）