---
title: 2021 年务必知道的最好用的 14 款 CI/CD 工具
summary: 本文列出了市场上最流行的 14 种 CI/CD 工具，包括 Jenkins、CircleCI、TeamCity 等，并介绍了它们的主要特性和使用场景。
tags:
  - CICD
date: 2020-03-29
author:
---

"Quality at Speed" 是软件开发中的新规范。

企业正在朝着 DevOps 方法论和敏捷文化迈进，以加快交付速度并确保产品质量。在 DevOps 中，连续和自动化的交付周期使快速可靠的交付成为可能的基础。

这导致我们需要适当的持续集成和持续交付（CI/CD）工具。 一个好的 CI/CD 工具可以利用团队当前的工作流程，以最佳利用自动化功能并创建可靠的 CI/CD 管道为团队发展提供所需的动力。

随着市场上大量 CI/CD 工具的出现，团队可能难以做出艰难的决定来挑选合适的工具。该列表包含市场上最好的 14 种 CI/CD 工具及其主要特性，使你和团队在选择过程中更加轻松。



以下罗列出了目前市场上最流行的 14 种最佳 CI/CD 工具，希望该列表为你在选择 CI/CD 前提供了足够的信息，更多详细信息你也可以查看官网做更深入的了解。最终结合你的需求以及现有基础架构以及未来潜力和改进的空间是将影响你最终选择的因素，帮助你选择到最适合你的规格的 CI/CD 软件。

## Jenkins

Jenkins 是一个开源自动化服务器，在其中进行集中构建和持续集成。它是一个独立的基于 Java 的程序，带有 Windows，macOS，Unix 的操作系统的软件包。Jenkins 支持软件开发项目的构建，部署和自动化，以及成百上千的插件来满足你的需求。它是市场上最具影响力的 CI/CD 工具之一。

Jenkins 主要特性：

* 易于在各种操作系统上安装和升级
* 简单易用的界面
* 可通过社区提供的巨大插件资源进行扩展
* 在用户界面中轻松配置环境
* 支持主从架构的分布式构建
* 根据表达式构建时间表
* 在预构建步骤中支持 Shell 和 Windows 命令执行
* 支持有关构建状态的通知

许可：免费。Jenkins 是一个拥有活跃社区的开源工具。

主页：<https://jenkins.io/>

## CircleCI

CircleCI 是一种 CI/CD 工具，支持快速的软件开发和发布。CircleCI 允许从代码构建，测试到部署的整个用户管道自动化。

你可以将 CircleCI 与 GitHub，GitHub Enterprise 和 Bitbucket 集成，以在提交新代码行时创建内部版本。CircleCI 还可以通过云托管选项托管持续集成，或在私有基础架构的防火墙后面运行。

CircleCI 主要特性:

* 与 Bitbucket，GitHub 和 GitHub Enterprise 集成
* 使用容器或虚拟机运行构建
* 简易调试
* 自动并行化
* 快速测试
* 个性化的电子邮件和IM通知
* 连续和特定于分支机构的部署
* 高度可定制
* 自动合并和自定义命令以上传软件包
* 快速设置和无限构建

许可：Linux 计划从选择不运行任何并行操作开始。开源项目获得了另外三个免费容器。在注册期间，将看到价格以决定所需的计划。

主页： <https://circleci.com/>

## TeamCity

TeamCity 是 JetBrains 的构建管理和持续集成服务器。

TeamCity 是一个持续集成工具，可帮助构建和部署不同类型的项目。 TeamCity 在 Java 环境中运行，并与 Visual Studio 和 IDE 集成。该工具可以安装在 Windows 和 Linux 服务器上，支持 .NET 和开放堆栈项目。

TeamCity 2019.1 提供了新的UI和本机 GitLab 集成。它还支持 GitLab 和 Bitbucket 服务器拉取请求。该版本包括基于令牌的身份验证，检测，Go测试报告以及 AWS Spot Fleet 请求。

TeamCity主要特性:

* 提供多种方式将父项目的设置和配置重用到子项目
* 在不同环境下同时运行并行构建
* 启用运行历史记录构建，查看测试历史记录报告，固定，标记以及将构建添加到收藏夹
* 易于定制，交互和扩展服务器
* 保持CI服务器正常运行
* 灵活的用户管理，用户角色分配，将用户分组，不同的用户身份验证方式以及带有所有用户操作的日志，以透明化服务器上所有活动

许可：TeamCity 是具有免费和专有许可证的商业工具。

主页： <https://www.jetbrains.com/teamcity/>

## Bamboo

Bamboo 是一个持续集成服务器，可自动执行软件应用程序版本的管理，从而创建了持续交付管道。Bamboo 涵盖了构建和功能测试，分配版本，标记发行版，在生产中部署和激活新版本。

Bamboo主要特性:

* 支持多达 100 个远程构建代理
* 并行运行批次测试并快速获得反馈
* 创建图像并推送到注册表
* 每个环境的权限，使开发人员和测试人员可以在生产保持锁定状态的情况下按需部署到他们的环境中
* 在 Git，Mercurial，SVN Repos 中检测新分支，并将主线的CI方案自动应用于它们
* 触发器基于在存储库中检测到的更改构建。 推送来自 Bitbucket 的通知，已设置的时间表，另一个构建的完成或其任何组合。

许可：Bamboo 定价层基于代理（Slave）而不是用户，代理越多，花费越多。

主页：<https://www.atlassian.com/software/bamboo>

## GitLab

GitLab 是一套用于管理软件开发生命周期各个方面的工具。 核心产品是基于 Web 的 Git 存储库管理器，具有问题跟踪，分析和 Wiki 等功能。

GitLab 允许你在每次提交或推送时触发构建，运行测试和部署代码。你可以在虚拟机，Docker 容器或另一台服务器上构建作业。

GitLab主要特性:

* 通过分支工具查看，创建和管理代码以及项目数据
* 通过单个分布式版本控制系统设计，开发和管理代码和项目数据，从而实现业务价值的快速迭代和交付
* 提供真实性和可伸缩性的单一来源，以便在项目和代码上进行协作
* 通过自动化源代码的构建，集成和验证，帮助交付团队完全接受CI。
* 提供容器扫描，静态应用程序安全测试（SAST），动态应用程序安全测试（DAST）和依赖项扫描，以提供安全的应用程序以及许可证合规性
* 帮助自动化并缩短发布和交付应用程序的时间

许可：GitLab 是一个商业工具和免费软件包。它提供了在 GitLab 或你的本地实例和/或公共云上托管 SaaS 的功能。

主页：<https://about.gitlab.com/>

## Buddy

Buddy 是一个 CI/CD 软件，它使用 GitHub，Bitbucket 和 GitLab 的代码构建，测试，部署网站和应用程序。它使用具有预安装语言和框架的 Docker 容器以及 DevOps 来监视和通知操作，并以此为基础进行构建。

Buddy主要特性:

* 易于将基于 Docker 的映像自定义为测试环境
* 智能变更检测，最新的缓存，并行性和全面的优化
* 创建，定制和重用构建和测试环境
* 普通和加密，固定和可设置范围：工作空间，项目，管道，操作
* 与 Elastic，MariaDB，Memcached，Mongo，PostgreSQL，RabbitMQ，Redis，Selenium Chrome 和 Firefox 关联的服务
* 实时监控进度和日志，无限历史记录
* 使用模板进行工作流管理，以克隆，导出和导入管道
* 一流的Git支持和集成

许可：Buddy 是免费的商业工具。

主页：<https://buddy.works/>

## Travis CI

Travis CI 是用于构建和测试项目的CI服务。Travis CI 自动检测新提交并推送到 GitHub 存储库的提交。每次提交新代码后，Travis CI 都会构建项目并相应地运行测试。

该工具支持许多构建配置和语言，例如 Node，PHP，Python，Java，Perl 等。

Travis 主要特性:

* 快速设置
* GitHub项目监控的实时构建视图
* 拉取请求支持
* 部署到多个云服务
* 预装的数据库服务
* 通过构建时自动部署
* 为每个版本清理虚拟机
* 支持 macOS，Linux 和 iOS
* 支持多种语言，例如 Android，C，C＃，C ++，Java，JavaScript（带有Node.js），Perl，PHP，Python，R，Ruby 等。

许可：Travis CI 是一项托管的 CI/CD 服务。私人项目可以在 travis-ci.com 上进行收费测试。可以在 travis-ci.org 上免费应用开源项目。

主页：<https://travis-ci.com>

## Codeship

Codeship 是一个托管平台，可多次支持早期和自动发布软件。通过优化测试和发布流程，它可以帮助软件公司更快地开发更好的产品。

Codeship 主要特性:

* 与所选的任何工具，服务和云环境集成
* 易于使用。提供快速而全面的开发人员支持。
* 借助CodeShip的交钥匙环境和简单的UI，使构建和部署工作更快
* 选择AWS实例大小，CPU和内存的选项
* 通过通知中心为组织和团队成员设置团队和权限
* 无缝的第三方集成，智能通知管理和项目仪表板，可提供有关项目及其运行状况的高级概述。

许可：每月最多免费使用100个版本，无限版本从$49/月开始。你可以为更大的实例大小购买更多的并发构建或更多的并行管道。

主页： <https://codeship.com/>

## GoCD

GoCD 来自 ThoughtWorks，是一个开放源代码工具，用于构建和发布支持 CI/CD 上的现代基础结构的软件。

* 轻松配置相关性以实现快速反馈和按需部署
* 促进可信构件：每个管道实例都锚定到特定的变更集
* 提供对端到端工作流程的控制，一目了然地跟踪从提交到部署的更改
* 容易看到上游和下游
* 随时部署任何版本
* 允许将任何已知的良好版本的应用程序部署到你喜欢的任何位置
* 通过比较内部版本功能获得用于任何部署的简单物料清单
* 通过 GoCD 模板系统重用管道配置，使配置保持整洁
* 已经有许多插件

许可：免费和开源

主页：<https://www.gocd.org/>

## Wercker

对于正在使用或正在考虑基于 Docker 启动新项目的开发人员，Wercker 可能是一个合适的选择。Wercker 支持组织及其开发团队使用 CI/CD，微服务和 Docker。

2017 年 4 月 17 日，甲骨文宣布已签署最终协议收购 Wercker。

Wercker 主要特性:

* Git 集成，包括 GitHub，Bitbucket，GitLab 和版本控制
* 使用 Wercker CLI 在本地复制 SaaS 环境，这有助于在部署之前调试和测试管道
* 支持 Wercker 的 Docker 集成以构建最少的容器并使尺寸可管理
* Walterbot – Wercker 中的聊天机器人 – 允许你与通知交互以更新构建状态
* 环境变量有助于使敏感信息远离存储库
* Wercker 利用关键安全功能（包括源代码保护）来关闭测试日志，受保护的环境变量以及用户和项目的可自定义权限

许可：甲骨文在收购后未提供 Wercker 的价格信息。

主页：<https://app.wercker.com>

## Semaphore

Semaphore 是一项托管的 CI/CD 服务，用于测试和部署软件项目。 Semaphore 通过基于拉取请求的开发过程来建立 CI/CD 标准。

Semaphore 主要特性:

* 与 GitHub 集成
* 自动执行任何连续交付流程
* 在最快的 CI/CD 平台上运行
* 自动缩放你的项目，以便你仅需支付使用费用
* 本机 Docker 支持。测试和部署基于 Docker 的应用程序
* 提供 Booster –一种功能，用于通过自动并行化Ruby项目的构建来减少测试套件的运行时间

许可：灵活。使用传统的CI服务，你会受到计划容量的限制。同时，Semaphore 2.0 将根据你团队的实际需求进行扩展，因此你无需使用该工具就不必付费

主页：<https://semaphoreci.com/>

## Nevercode

Nevercode 支持移动应用程序的 CI/CD。它有助于更​​快地构建，测试和发布本机和跨平台应用程序。

Nevercode 主要特性:

* 自动配置和设置
* 测试自动化：单元和UI测试，代码分析，真实设备测试，测试并行化
* 自动发布：iTunes Connect，Google Play，Crashlytics，T​​estFairy，HockeyApp
* 你的构建和测试状态的详细概述

许可：灵活。针对不同需求进行持续集成的不同计划。你可以从标准计划中选择，也可以请求根据自己的需求量身定制的计划。

主页：<https://nevercode.io/>

## Spinnaker

Spinnaker 是一个多云连续交付平台，支持在不同的云提供商之间发布和部署软件更改，包括 AWS EC2，Kubernetes，Google Compute Engine，Google Kubernetes Engine，Google App Engine 等。

Spinnaker主要特性:

* 创建部署管道，以运行集成和系统测试，旋转服务器组和降低服务器组以及监视部署。通过 Git 事件，Jenkins，Travis CI，Docker，cron 或其他 Spinnaker 管道触发管道
* 创建和部署不可变映像，以实现更快的部署，更轻松的回滚以及消除难以调试的配置漂移问题
* 使用它们的指标进行金丝雀分析，将你的发行版与诸如 Datadog，Prometheus，Stackdriver 或 SignalFx 的监视服务相关联
* 使用Halyard – Spinnaker的CLI管理工具安装，配置和更新你的 Spinnaker 实例
* 设置电子邮件，Slack，HipChat 或 SMS 的事件通知（通过 Twilio）

许可：开源

主页：<https://www.spinnaker.io/>

## Buildbot

Buildbot 是一个基于 Python 的 CI 框架，可自动执行编译和测试周期以验证代码更改，然后在每次更改后自动重建并测试树。因此，可以快速查明构建问题。

Buildbot 主要特性:

* 自动化构建系统，应用程序部署以及复杂软件发布过程的管理
* 支持跨多个平台的分布式并行执行，与版本控制系统的灵活集成，广泛的状态报告
* 在各种从属平台上运行构建
* 任意构建过程并使用 C 和 Python 处理项目
* 最低主机要求：Python 和 Twisted
* 注意：Buildbot 将停止支持 Python 2.7，并需要迁移到 Python 3。

许可：开源

主页：<https://buildbot.net/>

> [英文原文](https://www.katalon.com/resources-center/blog/ci-cd-tools/)
