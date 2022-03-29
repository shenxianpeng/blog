---
title: 一篇文章搞懂什么是 Docker，containerd，CRI，CRI-O，OCI，runc
tags:
  - containerd
  - Docker
  - CRI-O
  - runc
categories:
  - DevOps
author: shenxianpeng
date: 2022-03-29 20:52:42
---

自 Docker 开启了使用容器的爆发式增长，有越来越多的工具和标准来帮助管理和使用这项容器化技术，与此同时也造成了有很多术语让人感到困惑。

比如 Docker, containerd, CRI, CRI-O, OCI, runc，本篇将介绍这些你听过但并不了解的术语，并解释容器生态系统是如何在一起工作的。

## 容器生态系统

容器生态系统是由许多令人兴奋的技术、大量的专业术语和大公司相互争斗组成的。

幸运的是，这些公司偶尔会在休战中走到一起合作，商定一些标准，这些标准有助于使这个生态系统在不同的平台和操作系统之间更具互操作性，并减少对单一公司或项目的依赖。

这张图显示了 Docker、Kubernetes、CRI、OCI、containerd 和 runc 在这个生态系统中是如何结合的。

![](container-ecosystem/container-ecosystem.png)

其工作流程简单来说是这样的：

1. Docker，Kubernetes 等工具来运行一个容器时会调用容器运行时（CRI）比如 containerd，CRI-O
2. 通过容器运行时来完成容器的创建、运行、销毁等实际工作
    * Docker 使用的是 containerd 作为其运行时；Kubernetes 支持 containerd，CRI-O 等多种容器运行时
    * 这些容器运行时都遵循了 OCI 规范，并通过 runc 来实现与操作系统内核交互来完成容器的创建和运行

下面就分别介绍图中所提到的术语和规范。

<!-- more -->

## Docker

首先我们从大家都很熟悉的 Docker 开始，因为它是管理容器的最流行的工具。对很多人来说"Docker"这个名字本身就是"容器"的代名词。

Docker 启动了整个容器的革命，它创造了一个很好用的工具来处理容器也叫 Docker，这里最主要的要明白：

* Docker 并不是这个唯一的容器竞争者
* 容器也不再与 Docker 这个名字紧密联系在一起

目前的容器工具中，Docker 只是其中之一，其他著名的容器工具还包括：[Podman](https://podman.io/)，[LXC](https://linuxcontainers.org/lxd/introduction/)，[containerd](https://containerd.io/)，[Buildah](https://buildah.io/) 等。

因此，如果你认为容器只是关于 Docker 的，那是片面的不对的。

### Docker 组成

Docker 可以轻松地构建容器镜像，从 Docker Hub 中拉取镜像，创建、启动和管理容器。实际上，当你用 Docker 运行一个容器时实际上是通过 Docker 守护程序、containerd 和 runc 来运行它。

![](container-ecosystem/docker.png)

为了实现这一切，Docker 是由这些项目组成（还有其他项目，但这些是主要的）。

* docker-cli：这是一个命令行工具，它是用来完成 `docker pull`, `build`, `run`, `exec` 等命令进行交互。
* containerd：这是一个管理和运行容器的守护进程。它推送和拉动镜像，管理存储和网络，并监督容器的运行。
* runc：这是低级别的容器运行时间（实际创建和运行容器的东西）。它包括 libcontainer，一个用于创建容器的基于 Go 的本地实现。

### Docker 镜像

许多人所说的 Docker 镜像，实际上是以 Open Container Initiative（OCI）格式打包的镜像。

因此，如果你从 Docker Hub 或其他注册中心拉出一个镜像，你应该能够用 docker 命令使用它，或在 Kubernetes 集群上使用，或用 podman 工具以及任何其他支持 OCI 镜像格式规范的工具。

### Dockershim

在 Kubernetes 包括一个名为 dockershim 的组件，使它能够支持 Docker。但 Docker 由于比 Kubernetes 更早，没有实现 CRI，所以这就是 dockershim 存在的原因，它支持将 Docker 被硬编码到 Kubernetes 中。随着容器化成为行业标准，Kubernetes 项目增加了对额外运行时的支持，比如通过 Container Runtime Interface (CRI) 容器运行时接口的容器来支持运行容器。因此 dockershim 成为了 Kubernetes 项目中的一个异类，对 Docker 和 dockershim 的依赖已经渗透到云原生计算基金会（CNCF）生态系统中的各种工具和项目中，导致代码脆弱。

2022 年 4 月 dockershim 将会从 Kubernetes 1.24 中完全移除。今后 Kubernetes 将取消对 Docker 的直接支持，而倾向于只使用实现其容器运行时接口的容器运行时，这可能意味着使用 containerd 或 CRI-O。这并不意味着 Kubernetes 将不能运行 Docker 格式的容器。containerd 和 CRI-O 都可以运行 Docker 格式（实际上是 OCI 格式）的镜像，它们只是无需使用 docker 命令或 Docker 守护程序。

## Container Runtime Interface (CRI)

CRI（容器运行时接口）是 Kubernetes 用来控制创建和管理容器的不同运行时的 API，它使 Kubernetes 更容易使用不同的容器运行时。它一个插件接口，这意味着任何符合该标准实现的容器运行时都可以被 Kubernetes 所使用。

Kubernetes 项目不必手动添加对每个运行时的支持，CRI API 描述了 Kubernetes 如何与每个运行时进行交互，由运行时决定如何实际管理容器，因此只要它遵守 CRI 的 API 即可。

![](container-ecosystem/cri.png)

你可以使用你喜欢的 containerd 来运行你的容器，也可以使用 CRI-O 来运行你的容器，因为这两个运行时都实现了 CRI 规范。

## containerd

containerd 是一个来自 Docker 的高级容器运行时，并实现了 CRI 规范。它是从 Docker 项目中分离出来，之后 containerd 被捐赠给云原生计算基金会（CNCF）为容器社区提供创建新容器解决方案的基础。

所以 Docker 自己在内部使用 containerd，当你安装 Docker 时也会安装 containerd。

containerd 通过其 CRI 插件实现了 Kubernetes 容器运行时接口（CRI），它可以管理容器的整个生命周期，包括从镜像的传输、存储到容器的执行、监控再到网络。

## CRI-O

CRI-O 是另一个实现了容器运行时接口（CRI）的高级别容器运行时，可以使用 OCI（开放容器倡议）兼容的运行时，它是 containerd 的一个替代品。

CRI-O 诞生于 RedHat、IBM、英特尔、SUSE、Hyper 等公司。它是专门从头开始创建的，作为 Kubernetes 的一个容器运行时，它提供了启动、停止和重启容器的能力，就像 containerd 一样。

## Open Container Initiative (OCI)

OCI 开放容器倡议，是一个由科技公司组成的团体，其目的是围绕容器镜像和运行时创建开放的行业标准。他们维护容器镜像格式的规范，以及容器应该如何运行。

OCI 背后的想法是，你可以选择符合规范的不同运行时，这些运行时都有不同的底层实现。

例如，你可能有一个符合 OCI 的运行时用于你的 Linux 主机，另一个用于你的 Windows 主机。这就是拥有一个可以由许多不同项目实施的标准的好处。这种同样的 "一个标准，多种实现" 的方法其实还有很多都在使用，从蓝牙设备到 Java APIs。

## runc

runc 是轻量级的通用运行时容器，它遵守 OCI 规范，是实现 OCI 接口的最低级别的组件，它与内核交互创建并运行容器。

runc 为容器提供了所有的低级功能，与现有的低级 Linux 功能交互，如命名空间和控制组，它使用这些功能来创建和运行容器进程。

runc 的几个替代品：

* [crun](https://github.com/containers/crun) 一个用 C 语言编写的容器运行时（相比之下，runc 是用Go编写的。）
* 来自 Katacontainers 项目的 [kata-runtime](https://github.com/kata-containers/kata-containers)，它将 OCI 规范实现为单独的轻量级虚拟机（硬件虚拟化）。
* Google 的 [gVisor](https://gvisor.dev/)，它创建了拥有自己内核的容器。它在其运行时中实现了 OCI，称为 runsc。

runc 是一个在 Linux 上运行容器的工具，所以这意味着它可以在 Linux 上、裸机上或虚拟机内运行。

在 Windows 上，它略有不同，与 runc 相当的是微软的主机计算服务（HCS），它包括一个叫 [runhcs](https://docs.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/containerd) 的工具，它本身是 runc 的一个分叉，也实现了开放容器倡议的规范。

## 总结

在本篇中，我们看到 Docker 只是容器生态系统中的一个小部分。另外还有一堆开放的标准，这就使得不同的实现互相之间是可替换的。

这就是为什么有 CRI 和 OCI 标准，以及 containerd、runc 和 CRI-O 等项目存在的原因了。

现在你知道了关于容器这个有趣而又略显复杂的世界的一切，下次和别人讨论时，不要说你在使用 "Docker 容器" :)

## 参考

> [The differences between Docker, containerd, CRI-O and runc](https://www.tutorialworks.com/difference-docker-containerd-runc-crio-oci/)

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
