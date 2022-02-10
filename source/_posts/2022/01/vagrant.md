---
title: Vagrant 介绍
tags:
  - VirtualBox
  - Vagrant
categories:
  - Vagrant
author: shenxianpeng
date: 2022-01-27 23:00:57
---

## 什么是 Vagrant

Vagrant 是一种[开源](https://github.com/hashicorp/vagrant)软件产品，用来方便构建和维护虚拟软件开发环境。

例如，它可以基于 VirtualBox、VMware、KVM、Hyper-V 和 AWS 甚至是 Docker 等提供商来构建开发环境。它通过简化虚拟化的软件配置管理，来提高开发效率。

Vagrant 是用 Ruby 语言开发的，但它的生态系统支持使用其他几种语言进行开发。

简单来说 Vagrant 是对传统虚拟机的一层封装，能够让你更方便的使用虚拟开发环境。

## Vagrant 的发展史

Vagrant 最初是由 [Mitchell Hashimoto](https://www.hashicorp.com/about?name=mitchell-hashimoto) 于 2010 年 1 月作为个人项目启动的。

Vagrant 的第一个版本于 2010 年 3 月发布。2010 年 10 月，Engine Yard 宣布他们将赞助 Vagrant 项目。

Vagrant 的第一个稳定版本 Vagrant 1.0 于 2012 年 3 月发布，正好是原始版本发布两年后。

同年 11 月，Mitchell 成立了 HashiCorp 公司，以支持 Vagrant 的全职开发。Vagrant 仍然是开源软件，HashiCorp 公司致力于创建商业版本，并为 Vagrant 提供专业支持和培训。

现在 HashiCorp 已经成为世界顶级开源公司，它通过一些列的产品，包括 Vagrant，Packer（打包），Momad（部署），Terraform（配置云环境），Vault（权限管理） 以及 Consul（监控），从端到端重新定义了整个 DevOps。

Vagrant 最初支持 VirtualBox，在 1.1 版增加了对其他虚拟化软件（如 VMware 和 KVM）的支持，以及对 Amazon EC2 等服务器环境的支持。从 1.6 版开始，Vagrant 原生支持 Docker 容器，在某些情况下可以替代完全虚拟化的操作系统。

## 如何使用 Vagrant

使用 Vagrant 的前提条件：

1. 安装 Vagrant。下载[Vagrant](https://www.vagrantup.com/downloads)
2. 安装 [VirtualBox](https://www.virtualbox.org/)

当以上两个都准备好了，你就可以通过命令行创建并使用你的虚拟机了。

比如你需要一个 [Ubuntu 18.04 LTS 64-bit](https://app.vagrantup.com/hashicorp/boxes/bionic64)的虚拟机。更多其他的虚拟机可以到 [Box](https://app.vagrantup.com/boxes/search) 网站上去搜索查找，它类似于 Docker Hub，用户可以在上面下载和上传各种 Vagrant Box。

你只需执行一些简单的命令就可以完成启动、登录、退出、及销毁。

初始化 Vagrant

```bash
vagrant init hashicorp/bionic64
```

启动虚拟机。大概几十秒钟就可以完成了（第一次需要下载镜像，时间会长一点，取决于网速）。

```bash
vagrant up
```

登录你的虚拟机，然后可以使用你创建的 Ubuntu 虚拟机了

```bash
vagrant ssh
```

当你不想用的时候，执行 `logout` 就可以退出登录了。

## Vagrant 和传统虚拟机软件的区别

<!-- more -->

Vagrant 相比传统使用虚拟机的方式要方便的多，我们来看看传统方式是怎样创建一台虚拟机的。

还是以 VirtualBox 为例，假设你已经安装好了 VirtualBox，使用传统方式要创建一个虚拟机的动作是这样的：

首先，下载对应的 ISO 文件
然后，用 VirtualBox 或 VMware 来加载 ISO
最后，通过一步步的配置 CPU、内存、磁盘，网络、用户等设置，等待安装完成安装

这种方式配置起来就非常繁琐，需要一步步的进行。这些配置的步骤往往还会写一个文档来记录下来才能保证以后能够创建出来“一摸一样”的虚拟开发环境。

相信通过对比你已经大概了解 Vagrant 是怎么使用的，以及它和传统使用虚拟机之间的一些区别了。

## 总结

Vagrant 相比于传统使用虚拟机的优势：提供易于配置、可重现和便携的工作环境，从而提高生产力和灵活性。

**Vagrant 可以说是创建、管理虚拟化环境的最简单、最快捷的方式！**

它之所以可以这么方便是站在了这些巨人（VirtualBox、VMware、AWS、OpenStack 或其他提供商）的肩膀上，然后通过 Shell 脚本、Ansbile、Chef、Puppet 等工具实现自动在虚拟机上安装和配置软件。

下一篇将介绍 Vagrant 和 Docker 之间的[区别](https://shenxianpeng.github.io/2022/01/vagrant-vs-docker/)。

---

欢迎扫码关注公众号「DevOps攻城狮」- 专注于DevOps领域知识分享。

![ ](https://github.com/shenxianpeng/shenxianpeng.github.io/blob/master/about/index/qrcode.jpg?raw=true)
