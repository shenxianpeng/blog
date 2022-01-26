---
title: 什么是 Vagrant？Vagrant 和 Docker 该怎么选？
tags:
  - Docker
  - VirtualBox
  - Vagrant
categories:
  - Vagrant
date: 2022-01-26 22:57:27
author: shenxianpeng
---

## 什么是 Vagrant

Vagrant 是对传统虚拟机的一层封装，能够让你更方便的使用虚拟机，主要解决环境配置的问题。它可以基于 VirtualBox，VMware，Hyper-V，甚至是 Docker 等提供商来构建你的环境。

## 为什么要用 Vagrant

对比按照传统模式如果我们需要在自己的电脑上安装一台虚拟机时，步骤如下：

首先，下载对应的 ISO 文件
然后，用 VirtualBox 或 VMware 来加载 ISO
最后，通过一步步的配置 CPU、内存、磁盘，网络、用户等设置，等待安装完成安装

如果使用 vagrant 来创建一台虚拟机，只需要两条命令

```bash
# 初始化 Vagrant，这时会在你当前目录下生成一个 Vagrantfile
vagrant init hashicorp/bionic64
# 启动虚拟机
vagrant up
```

大概几十秒钟就可以完成了（第一次需要下载镜像，时间会长一点，取决于网速）。

Vagrant 之所以可以这么方便，其实是它站在了这些巨人（VirtualBox、VMware、AWS、OpenStack 或其他提供商）的肩膀上，然后通过 Shell 脚本、Ansbile、Chef、Puppet 等工具实现自动在虚拟机上安装和配置软件。

好处就是：提供易于配置、可重现和便携的工作环境，提高生产力和灵活性。

Vagrant 可以说是创建、管理虚拟化环境的最简单、最快捷的方式！

## Vagrant 和 Docker 区别

如果不分场景而直接比对 Vagrant 和 Docker 是不恰当的。在一些简单场景中，它们的作用是重复的，但在更多场景中，它们是无法相互替代的。

那么什么情况下应该用 Vagrant，什么情况下用 Docker 呢？

**所以如果你仅仅是想管理虚拟机，那么你应该使用 Vagrant；如果你想快速开发和部署应用，那么应该使用 Docker。**

下面具体来说说为什么。

<!-- more -->

Vagrant 是 VM 的管理工具，或是说编排工具。Docker 是用来构建、运行、管理容器的工具。那么这个问题其实落在了虚拟机（VM）和 容器（Container）的区别。

引用网络上一组照片来感受一下物理机（Host），虚拟机（VM）和 容器（Container）之间的区别。

物理机（Host）

![物理机](vagrant-vs-docker/host.jpg)

虚拟机（VM）

![虚拟机](vagrant-vs-docker/vm.jpg)

容器（Container）

![Docker](vagrant-vs-docker/docker.jpg)

从图上我们更容易理解虚拟机（VM）和容器（Container）的这些不同：

| 特性     | 虚拟机 | 容器 |
| -------- | ----------- | --------- |
| 隔离级别  | 操作系统级  | 进程级别  |
| 隔离策略  | Hypervisor  | CGROUPS  |
| 系统资源  | 5~15%  | 0~5%  |
| 启动时间  | 分钟级  | 秒级  |
| 镜像存储  | GB  | MB  |

总结：Vagrant 和 Docker 的使用场景区别

**Vagrant 设计使用来管理虚拟机的，而 Docker 设计是用来管理应用环境。**

Vagrant 更适合用来做开发、测试，解决环境一致性的问题；Docker 更适合做快速开发和部署（CI/CD）。

最后，Vagrant 和 Docker 都有大量社区贡献的 [“Box”](https://app.vagrantup.com/boxes/search) 和 [“Image”](https://hub.docker.com/) 可供选择。

---

![ ](https://github.com/shenxianpeng/shenxianpeng.github.io/blob/master/about/index/qrcode.jpg?raw=true)
