---
title: Docker 版本概述
tags:
  - Docker
categories:
  - Docker
date: 2019-12-01 15:20:43
author: shenxianpeng
---

## Docker 可分为三个版本

* Docker Engine - Community
* Docker Engine - Enterprise
* Docker Enterprise

Docker Engine - Community 是希望开始使用 Docker 并尝试基于容器的应用程序的个人开发人员和小型团队的理想选择。

Docker Engine - Enterprise 专为企业开发容器运行时而设计，同时考虑了安全性和企业级SLA。

Docker Enterprise 专为企业开发和IT团队而设计，他们可以大规模构建，交付和运行关键业务应用程序。

| 能力  | Docker Engine - Community | Docker Engine - Enterprise  | Docker Enterprise|
|---|---|---|---|
| 容器引擎和内建的编配，网络，安全 | √ | √ | √ |
| [认证的基础设施，插件和ISV容器](https://docs.docker.com/ee/supported-platforms/#docker-enterprise) | |  √ | √ |
| [镜像管理](https://docs.docker.com/ee/dtr/) | | | √ |
| [容器应用程序管理](https://docs.docker.com/ee/ucp/) | | | √ |
| [镜像安全扫描](https://docs.docker.com/ee/dtr/user/manage-images/scan-images-for-vulnerabilities/) | | | √ |

## 安装 Docker 社区版本

* 以 CentOS 安装为例： https://docs.docker.com/install/linux/docker-ce/centos/

## 其他 Docker 版本安装

* 参考 Docker 官网：https://docs.docker.com/install/overview/