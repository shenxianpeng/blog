---
title: 什么是 Vagrant？Vagrant 和 Docker 到底有什么区别？
tags:
  - Docker
  - VirtualBox
  - Vagrant
categories:
  - Vagrant
date: 2022-01-23 22:57:27
author: shenxianpeng
---

## 什么是 Vagrant

Vagrant 是对传统虚拟机的一层封装，能让你更方便的使用虚拟机，主要解决的问题是开发和运维人员的环境配置问题。

它可以基于 VirtualBox，VMware，Hyper-V，甚至是 Docker 等提供商来来构建你的开发环境，提供易于配置、可重现和便携的工作环境，提高生产力和灵活性。

## 为什么要用 Vagrant

以前，我们在自己的电脑上安装一台虚拟机的步骤是：

1. 下载对应的 ISO 文件
2. 用 VirtualBox 或 VMware 来加载 ISO
3. 一步步的配置CPU、内存、磁盘，网络、用户等设置，然后等待安装完成

然而，使用 vagrant 来创建一台虚拟机，只需要两条命令，大概几十秒钟就可以完成了（第一次需要下载镜像，时间会长一点，取决于网速）。

```bash
# 初始化 Vagrant，这时会在你当前目录下生成一个 Vagrantfile
vagrant init hashicorp/bionic64
# 启动虚拟机
vagrant up
```

Vagrant 之所以可以这么方便，背后是它站在这些巨人的肩膀上，比如它支持 VirtualBox、VMware、AWS、OpenStack 或其他提供商，然后可以通过 Shell 脚本、Ansbile、Chef、Puppet 等行业标准配置工具自动在虚拟机上安装和配置软件。

Vagrant 可以说是创建、管理虚拟化环境的最简单、最快捷的方式！

## Vagrant 和 Docker 区别

不分场景而直接比对 Vagrant 和 Docker 是不恰当的。在一些简单场景中，它们两款产品作用是重复的，但在更多场景中，它们两款产品无法相互替代。

那么什么场景下应该用 Vagrant，什么情况下用 Docker？

> 所以如果你仅仅是想管理虚拟机，那么你应该使用 Vagrant；如果你想快速开发和部署应用，那么应该使用 Docker。

下面具体来说说为什么。

Vagrant 其实就是 VM 的管理工具，或是说编排工具。Docker 是用来构建、运行、管理容器的工具。那么这个问题其实就是虚拟机（VM）和 容器（Container）的区别。

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

回到最初的问题：Vagrant 和 Docker 的使用场景区别？

**Vagrant 设计使用来管理虚拟机的，而 Docker 设计是用来管理应用环境。**

Vagrant 更适合用来做开发、测试，解决环境一致性的问题；Docker 更适合做快速开发和部署（CI/CD）。

最后，Vagrant 和 Docker 都有大量社区贡献的 “Box” 和 “Image” 可供选择。
