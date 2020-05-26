---
title: Artifactory Advanced Usage
tags:
  - Artifactory
  - JFrog
categories:
  - DevOps
date: 2020-05-08 10:43:46
author: shenxianpeng
---

在使用 Artifactory 有一段时间了，之前一直使用的是 OSS(OPEN SOURCE SOLUTIONS) 版本，也就是所有人都可以免费使用的版本。免费的好处就是能让你快速接触并使用这个工具，当然它会在一些功能上做限制。比如在 CI工具（这里以 Jenkins 为例）集成时，OSS 版本上无法通过 REST API/JFrog CLI/Jenkins Plugin 等方式实现以下几种常见的需求。

* 提供了通过 API/CLI/Plugsin 推送 Build 推送到 Artifactory 仓库，但不提供删除这些 Builds 以及对推送到不同仓库设置不同的保留策略 (Retention policy)
* 不提供通过 API/CLI/Plugsin 对 Build 添加属性。只能手动添加 build.status=SUCCESS 和 test.status=SUCCESS 等这样的属性
* 无法将通过 API/CLI/Plugsin 将你的构建从一个仓库 move/copy 到另外一个仓库等等

想了解 OSS/Professional/Enterprise 各个版本至今的有哪些细微的差别，可以访问官方的 REST API 连接 https://www.jfrog.com/confluence/display/JFROG/Artifactory+REST+API，搜索关键词 Requires Artifactory 进行比对。


接下来就是对以上三种常见的集成需求在 Artifactory Pro 或是更高的 Artifactory Enterprise+ 版本上的使用。

对于以上三个功能的实现是基于 Artifactory Enterprise 6.9.0 rev 60900900 版本。


## REST API


## JFrog CLI


## Jenkins Artifactory plugin 3.5.0

### 设置 Props

这里引用的是 jfrog 官方写的一个 project-examples 仓库供你参考。

https://github.com/shenxianpeng/cicd-project-examples/tree/master/jenkins-examples/pipeline-examples/declarative-examples/props-example

https://github.com/shenxianpeng/cicd-project-examples/tree/master/jenkins-examples/pipeline-examples/declarative-examples/props-single-file-example

### Promote

https://github.com/shenxianpeng/cicd-project-examples/tree/master/jenkins-examples/pipeline-examples/declarative-examples/promotion-example








