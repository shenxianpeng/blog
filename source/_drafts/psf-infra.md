---
title: Python 软件基金会 (PFS) 基础设施概览 
tags:
  - Python
  - Infrastructure
categories:
  - DevOps
author: shenxianpeng
date: 2024-01-21 11:27:18
---

继上次看完了 Apache 的基础设施介绍，本篇文章我们来看看 PFS 的基础设施。

## PSF 基础设施概述

PSF 运行各种基础设施服务来支持其使命，从 [PyCon 站点](https://us.pycon.org/) 到 [CPython Mercurial](https://hg.python.org/) 服务器。本页的目标是列举所有这些服务，它们在哪里运行，以及主要联系人是谁。

## 基础架构团队

基础架构团队最终负责维护 PSF 基础设施。但是，它不需要成为运行 PSF 服务的基础设施。事实上，大多数的日常运营服务由不在基础设施团队中的人员处理。这基础设施团队可以协助建立新服务并为维护人员提供建议的个别服务。其成员通常还处理对敏感的更改全球系统，例如 DNS。目前的团队成员是：

* Alex Gaynor (has no responsibilities)
* Benjamin Peterson
* Benjamin W. Smith
* Donald Stufft
* Ee Durbin (PSF Director of Infrastructure)
* Noah Kantrowitz

联系基础架构团队的最佳方式是发送邮件 infrastructure-staff@python。也经常有人在 [Libera](https://libera.chat/) 的 #python-infra 频道联系他们。

## 基础设施提供商

PSF 为其基础架构使用多个不同的云提供商和服务。

**Fastly**
Fastly 慷慨捐赠其内容分发网络（CDN）到 PSF。我们最高的流量服务（即 PyPI、www.python.org、docs.python.org）使用此 CDN 来改善最终用户延迟。

**DigitalOcean**
DigitalOcean 是当前的主要托管对于大多数基础设施，此处部署的服务 由 Salt 管理。

Heroku
Heroku 托管了许多 CPython 核心工作流机器人，、短暂的或概念验证的应用程序，以及其他良好的 Web 应用程序适合它的平台。

Gandi
[Gandi](https://www.gandi.net/en-US) 是我们的域名注册之星

Amazon Route 53
[Amazon Route 53](https://aws.amazon.com/route53/) 托管所有域的 DNS。它目前由基础设施人员手动管理。

DataDog
[DataDog](https://www.datadoghq.com/) 提供指标、仪表板和警报。

Pingdom
[Pingdom](https://www.pingdom.com/) 提供监控并向我们投诉 当服务中断时。

PagerDuty
[PagerDuty](https://www.pagerduty.com/) 用于 PSF 的待命轮换基础设施员工在一线，志愿者作为后援。

OSUOSL
俄勒冈州立大学开源实验室举办一个 PSF 的硬件服务器，speed.python.org 用于运行基准测试 此主机是使用 [Chef](www.getchef.com) 和 他们的配置管理位于 [PSF-Chef Git](https://github.com/python/psf-chef) 存储库中。

### 数据中心

| PSF DC |    Provider   | Region |
|:------:|:-------------:|:------:|
| ams1   | Digital Ocean | AMS3   |
| nyc1   | Digital Ocean | NYC3   |
| sfo1   | Digital Ocean | SFO2   |

## 各种服务的详细信息

本部分列举了 PSF 服务、有关其托管的一般情况以及所有者的联系信息。

**Buildbot**

[buildbot](https://www.python.org/dev/buildbot/) master 是由 python-dev@python 运行的服务。特别是 Antoine Pitrou and Zach Ware.

**bugs.python.org**

bugs.python.org 由 PSF 在 DigitalOcean 上托管，由 Roundup 提供支持。 它还举办 bugs.jython.org 和 issues.roundup-tracker.org。

**docs.python.org**

Python 文档托管在 DigitalOcean 上，通过 Fastly 提供。 由 Julien Palard 拥有。

**hg.python.org**

CPython Mercurial 存储库托管在 Digital Ocean VM 上。服务 由 Antoine Pitrou 和 Georg Brandl 拥有。

**mail.python.org**
python.org Mailman 实例托管在 https://mail.python.org 和 SMTP（Postfix） 上。所有查询都应定向到 postmaster@python。

**planetpython.org 和 planet.jython.org**

它们托管在 DigitalOcean VM 上。Planet 代码和配置托管在 GitHub 上，并由团队在 planet@python。

**pythontest.net**

pythontest.net 托管 Python 测试套件。python-dev@python。对其最终负责保养。

**speed.python.org**
speed.python.org 是一个跟踪 Python 性能的 [Codespeed 实例](https://github.com/zware/codespeed)。 Web 界面托管在 DigitalOcean VM 上，基准测试在 strongfy 上运行 机器在 OSUOSL 上，由 Buildbot 主节点调度。由 speed@python 和 Zach Ware 维护。

**wiki.python.org**
它托管在 DigitalOcean VM 上。Marc-André Lemburg拥有它。

**www.jython.org**
这是从 Amazon S3 存储桶托管的。设置非常简单，不应该 需要很多调整，但基础设施工作人员可以被戳进去。

**www.python.org**
主要的 Python 网站是一个 Django 应用程序，托管在 Heroku。它的源代码可以在 [GitHub](https://github.com/python/pythondotorg) 上找到，并且该网站的问题可能是报告给 [GitHub 问题跟踪器](https://github.com/python/pythondotorg/issues)。Python 下载 （即 https://www.python.org/ftp/ 下的所有内容）都托管在单独的 DigitalOcean 虚拟机。整个网站都在 Fastly 后面。还有用于测试站点的 https://staging.python.org。http://legacy.python.org 是从静态镜像托管的旧网站。

**PyCon**
PyCon 网站托管在 Heroku 上。联系地址是 pycon-site@python。

**PyPI**
Python 包索引的负载最多 任何 PSF 服务。它的源代码可在 [GitHub](https://github.com/pypa/warehouse) 上找到。它的所有基础设施都在 由 [pypi-infra](https://github.com/pypi/infra) 配置的 AWS， 它以 Fastly 为首。基础设施Ee Durbin, Donald Stufft, and Dustin Ingram。联系地址是 admin@pypi。

PyPy properties
[PyPy 网站](pypy.org)托管在 DigitalOcean VM 上并进行维护 作者：pypy-dev@python。

> 为了文章的可读性，本文做了部分修改和删减。原文在[这里](https://infra.psf.io/overview.html)。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
