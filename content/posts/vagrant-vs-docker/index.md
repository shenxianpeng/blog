---
title: Vagrant 和 Docker 的区别，该如何选？
summary: 本文介绍了 Vagrant 和 Docker 的区别，分析了它们各自的使用场景和优势，帮助读者选择合适的工具来管理虚拟机或容器。
tags:
  - Docker
  - VirtualBox
  - Vagrant
date: 2022-02-14
author: shenxianpeng
---

关于 Vagrant 的介绍，可以参看前一篇文章：[什么是 Vagrant? Vagrant 和 VirtualBox 的区别](https://shenxianpeng.github.io/2022/01/vagrant/)

## 什么是 Vagrant

关于 Vagrant 的介绍，可以参看前一篇文章：什么是 Vagrant? Vagrant 和 VirtualBox 的区别

## Vagrant 和 Docker 区别

关于 Vagrant 被问到最多的问题：Vagrant 和 Docker 之间有什么区别。

如果不分场景的直接比对 Vagrant 和 Docker 是不恰当的。在一些简单场景中，它们的作用是重复的，但在更多场景中，它们是无法相互替代的。

那么什么情况下应该用 Vagrant，什么情况下用 Docker 呢？

**所以如果你仅仅是想管理虚拟机，那么你应该使用 Vagrant；如果你想快速开发和部署应用，那么应该使用 Docker。**

下面具体来说说为什么。



Vagrant 是 VM 的管理工具，或是说编排工具；Docker 是用来构建、运行、管理容器的工具。那么这个问题其实落在了虚拟机（VM）和 容器（Container）的区别。

引用网络上一组照片来感受一下物理机（Host），虚拟机（VM）和 容器（Container）之间的区别。

物理机（Host）

![物理机](host.jpg)

虚拟机（VM）

![虚拟机](vm.jpg)

容器（Container）

![Docker](docker.jpg)

从图上我们更容易理解虚拟机（VM）和容器（Container）的这些不同：

| 特性     | 虚拟机 | 容器 |
| -------- | ----------- | --------- |
| 隔离级别  | 操作系统级  | 进程级别  |
| 隔离策略  | Hypervisor  | CGROUPS  |
| 系统资源  | 5 - 15%  | 0 - 5%  |
| 启动时间  | 分钟级  | 秒级  |
| 镜像存储  | GB  | MB  |

总结：Vagrant 和 Docker 的使用场景区别



**Vagrant 设计是用来管理虚拟机的，Docker 设计是用来管理应用环境。**

Vagrant 更适合用来做开发、测试，解决环境一致性的问题；Docker 更适合做快速开发和部署，CI/CD。

最后，Vagrant 和 Docker 都有大量社区贡献的 [“Box”](https://app.vagrantup.com/boxes/search) 和 [“Image”](https://hub.docker.com/) 可供选择。

---

欢迎扫码关注公众号「DevOps攻城狮」- 专注于DevOps领域知识分享。

![ ](https://github.com/shenxianpeng/shenxianpeng.github.io/blob/master/about/index/qrcode.jpg?raw=true)
