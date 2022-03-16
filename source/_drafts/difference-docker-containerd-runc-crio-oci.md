---
title: Docker、containerd、CRI-O、 之间的区别
tags:
  - containerd
  - Docker
  - CRI-O
  - runc
categories:
  - DevOps
author: shenxianpeng
date: 2022-02-19 20:52:42
---

自从 Docker 开启了使用容器的爆发式增长，有越来越多的工具和标准来帮助管理使用这项容器化技术，也同时造成了有很多术语让人感到困惑。
比如 Docker, Containerd, CRI, CRI-O, OCI, runc，本篇将介绍这些你听过但并不了解的术语，并解释容器生态系统是如何在一起工作的。

## 理解 Docker

Docker 公司、Docker 容器、Docker 镜像，我们都习惯的 Docker 开发者工具之间是有区别的。

这里最主要的是要明白的一点，Docker 并不是这个唯一的容器竞争者，容器也不再与 Docker 这个名字紧密联系在一起。

目前的容器工具中，docker 只是其中之一，其他著名的容器工具还包括。因此，如果你认为容器只是关于 Docker 的，那是片面的、不对的。

## 容器生态系统的解释

容器生态系统是由许多令人兴奋的技术、大量的专业术语和大公司相互争斗组成的。

幸运的是，这些公司偶尔会在休战中走到一起🤝，商定一些标准。这些标准有助于使这个生态系统在不同的平台和操作系统之间更具互操作性，并减少对单一公司或项目的依赖。

需要注意的主要标准有。

* Kubernetes Container Runtime Interface (CRI) 容器运行时接口，它定义了 Kubernetes 和容器运行时之间的 API。
* Open Container Initiative (OCI) 开放容器倡议，它发布了镜像和容器的规范。

这张图准确地显示了 Docker、Kubernetes、CRI、OCI、containerd 和 runc 在这个生态系统中是如何结合的。

![](difference-docker-containerd-runc-crio-oci/container-ecosystem.drawio.png)

## Docker

我们必须从Docker开始，因为它是处理容器的最流行的开发者工具。对很多人来说，"Docker "这个名字本身就是 "容器 "的同义词。

Docker 启动了这整个革命。Docker 创造了一个非常符合人体工程学（很好用）的工具来处理容器--也叫 docker。

docker 被设计成安装在工作站或服务器上，并附带了一堆工具，使其作为一个开发人员或 DevOps 人员能够轻松地构建和运行容器。

docker 命令行工具可以构建容器镜像，从注册表中提取它们，创建、启动和管理容器。

为了实现这一切，你所知道的 docker 的经验现在由这些项目组成（还有其他项目，但这些是主要的）。

docker-cli：这是一个命令行工具，你使用 docker ... 命令进行交互。

containerd：这是一个管理和运行容器的守护进程。它推送和拉动镜像，管理存储和网络，并监督容器的运行。

runc。这是低级别的容器运行时间（实际创建和运行容器的东西）。它包括 libcontainer，一个用于创建容器的基于 Go 的本地实现。

实际上，当你用 docker 运行一个容器时，你实际上是通过 Docker 守护程序、containerd 和 runc 来运行它。

## Dockershim: Kubernetes 中的 Docker

Kubernetes 包括一个名为 dockershim 的组件，使其能够支持 Docker。

Kubernetes 更倾向于通过任何支持其Container Runtime Interface (CRI)容器运行时接口的容器运行时来运行容器。

但 Docker 由于比 Kubernetes 更早，没有实现 CRI。所以这就是 dockershim 存在的原因，基本上是把 Docker 栓在 Kubernetes 上。或者 Kubernetes 到 Docker 上，无论你喜欢哪种方式。

什么是shim？

在现实世界中（！），垫片是。一个垫圈或薄薄的材料条，用于对齐零件，使其适合，或减少磨损。

在技术方面，垫片是软件系统中的一个组件，它作为不同 API 之间的桥梁，或作为一个兼容层。当你想使用一个第三方组件时，有时会添加一个垫片，但你需要一点胶水代码来使其工作。

今后，Kubernetes 将直接取消对 Docker 的支持，而倾向于只使用实现其容器运行时接口的容器运行时。这可能意味着使用containerd 或 CRI-O。

但这并不意味着 Kubernetes 将不能运行 Docker 格式的容器。containerd 和 CRI-O 都可以运行 Docker 格式（实际上是 OCI 格式）的镜像，它们只是无需使用 docker 命令或 Docker 守护程序。

## Docker图像

许多人所说的 Docker 镜像，实际上是以 Open Container Initiative（OCI）格式打包的镜像。

因此，如果你从 Docker Hub 或其他注册中心拉出一个镜像，你应该能够用 docker 命令使用它，或在 Kubernetes 集群上使用，或用 podman 工具，或任何其他支持 OCI 镜像格式规范的工具。

## Container Runtime Interface (CRI) 容器运行时接口

CRI 是 Kubernetes 用来控制创建和管理容器的不同运行时的 API。

CRI 使 Kubernetes 更容易使用不同的容器运行时。Kubernetes 项目不必手动添加对每个运行时的支持，CRI API 描述了Kubernetes 如何与每个运行时进行交互。因此，由运行时决定如何实际管理容器，只要它遵守 CRI 的 API 即可。

因此，如果你喜欢使用 containerd 来运行你的容器，你可以。或者，如果你喜欢使用 CRI-O，那么你也可以。这是因为这两个运行时都实现了 CRI 规范。

如果你是一个终端用户，实现方式大多不重要。这些 CRI 实现的目的是可插拔和无缝改变的。

如果你花钱从供应商那里获得支持（安全、错误修复等），你对运行时的选择可能会很重要。例如，红帽的 OpenShift 使用 CRI-O，并提供对它的支持。Docker 为他们自己的 containerd 提供支持。

### 如何在 Kubernetes 中检查你的容器运行时间

在Kubernetes架构中，kubelet（在每个节点上运行的代理）负责向容器运行时发送指令以启动和运行容器。

你可以通过查看每个节点上的kubelet参数来检查你正在使用哪个容器运行时。有一个选项--container-runtime和--container-runtime-endpoint，用来配置使用哪个运行时。

## containerd

containerd 是一个来自 Docker 的高级容器运行时，并实现了 CRI 规范。它从注册中心提取镜像，管理它们，然后交给低级别的运行时，由它实际创建和运行容器进程。

containerd 从 Docker 项目中分离出来，以使 Docker 更加模块化。

所以 Docker 自己在内部使用 containerd。当你安装 Docker 时，它也会安装 containerd。

containerd 通过其 cri 插件实现了 Kubernetes 容器运行时接口（CRI）。

## CRI-O

CRI-O 是另一个实现了容器运行时接口（CRI）的高级别容器运行时。它是 containerd 的一个替代品。它从注册表中提取容器镜像，在磁盘上管理它们，并启动一个低级别的运行时来运行容器进程。

是的，CRI-O 是另一个容器运行时。它诞生于红帽、IBM、英特尔、SUSE等公司。

它是专门从头开始创建的，作为 Kubernetes 的一个容器运行时。它提供了启动、停止和重启容器的能力，就像 containerd 一样。

## Open Container Initiative (OCI) 开放容器倡议

OCI 是一个由科技公司组成的团体，他们维护容器镜像格式的规范，以及容器应该如何运行。

OCI 背后的想法是，你可以选择符合规范的不同运行时。这些运行时都有不同的底层实现。

例如，你可能有一个符合 OCI 的运行时用于你的 Linux 主机，另一个用于你的 Windows 主机。

这就是拥有一个可以由许多不同项目实施的标准的好处。这种同样的 "一个标准，多种实现" 的方法到处都在使用，从蓝牙设备到Java APIs。

## runc

runc 是一个兼容 OCI 的容器运行时间。它实现了 OCI 规范并运行容器进程。

runc 被称为 OCI 的参考实现。

什么是参考实现？

runc 为容器提供了所有的低级功能，与现有的低级 Linux 功能交互，如命名空间和控制组。它使用这些功能来创建和运行容器进程。

runc 的几个替代品是。

[crun](https://github.com/containers/crun) 一个用 C 语言编写的容器运行时（相比之下，runc 是用Go编写的。）

来自Katacontainers项目的[kata-runtime](https://github.com/kata-containers/kata-containers)，它将 OCI 规范实现为单独的轻量级虚拟机（硬件虚拟化）。

Google的 [gVisor](https://gvisor.dev/)，它创建了拥有自己内核的容器。它在其运行时中实现了 OCI，称为 runsc。

### Windows上的runc相当于什么？

runc 是一个在 Linux 上运行容器的工具。所以这意味着它可以在 Linux 上、裸机上或虚拟机内运行。

在 Windows 上，它略有不同。与 runc 相当的是微软的主机计算服务（HCS）。它包括一个叫 [runhcs](https://docs.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/containerd) 的工具，它本身是 runc 的一个分叉，也实现了开放容器倡议的规范。

## 总结

就这样了。在这篇文章中，我们看到 Docker 只是容器生态系统中的一个小部分。

有一堆开放的标准，这使得不同的实现更容易被交换。这就是我们得到 CRI 和 OCI 标准，以及 containerd、runc 和 CRI-O 等项目的原因。

由于每个人都在忙着研究这些新技术，随着事情的进展，预计这将迅速改变。

现在你知道了关于容器这个有趣而又略显复杂的世界的一切。

但下次你参加聚会时🎈，不要说你在使用 " Docker容器 "....。

> https://www.tutorialworks.com/difference-docker-containerd-runc-crio-oci/
> https://thenewstack.io/a-security-comparison-of-docker-cri-o-and-containerd/

---

![ ](https://github.com/shenxianpeng/shenxianpeng.github.io/blob/master/about/index/qrcode.jpg?raw=true)

关注公众号「DevOps攻城狮」

（转载本站文章请注明作者和出处，请勿用于任何商业用途）
