---
title: 看看顶级的开源组织都在用哪些服务和工具
summary: 本篇介绍的是大名鼎鼎的开源软件基金会 Apache 所使用的服务(Services)和工具(Tools)，这或许能帮助你打开视野，在选择工具的时候提供参考。
tags:
  - Apache
  - Infrastructure
authors:
  - shenxianpeng
translate: false
date: 2024-01-21
---

本篇介绍的是大名鼎鼎的开源软件基金会 Apache 所使用的服务(Services)和工具(Tools)，这或许能帮助你打开视野，在选择工具的时候提供参考。如果你是一名 DevOps、SRE 或是 Infra 工程师，通过本篇文章内容结果帮助你更好的展示团队所提供的服务有哪些，以及窥探到 Apache Infra 是怎样组织和管理他们的。

## Apache 是谁

如果你不太了解 Apache，下面是关于 Apache 的简要介绍。

Apache 是一个开源软件基金会（Apache Software Foundation，简称 ASF）的缩写。ASF 是一个非营利性的组织，致力于支持和发展开源软件项目。Apache 软件基金会通过提供法律、财务和基础设施支持，帮助开发者共同合作创建和维护开源软件。其中，Apache 软件基金会最为著名的项目之一是 Apache HTTP 服务器，也称为 Apache Web 服务器。此外，ASF 还托管了许多其他流行的开源项目，像 ECharts，Superset，Dubbo，Spark，Kafka 等等。

## 服务与工具

Apache Infra 团队维护着供 PMC（项目管理委员会）、项目提交者和 Apache 董事会使用的各种工具。这些工具中的部分工具只提供给有特定职责或角色的人员使用。其他工具，如显示 Apache 基础设施各部分状态的监控工具，则向所有人开放。

* [为顶级项目（TLP）提供的服务](#为顶级项目tlp提供的服务)
    * [网站](#网站)
    * [电子邮件](#电子邮件)
    * [ASF 自助服务平台](#asf-自助服务平台)
    * [ASF 账户管理](#asf-账户管理)
    * [支持 LDAP 的服务](#支持-ldap-的服务)
* [项目孵化服务](#孵化项目podlings服务)
* [ASF 项目工具](#asf-项目工具)
    * [版本控制](#版本控制)
    * [问题跟踪和功能请求](#问题跟踪和功能请求)
    * [将版本库与 Jira 票据集成](#将你的版本库与-jira-票据集成)
    * [源码库发布者/订阅者服务](#源码库发布者订阅者服务)
    * [构建服务](#构建服务)
    * [产品命名](#产品命名)
    * [代码签名](#代码签名)
    * [代码质量](#代码质量)
    * [代码分发](#代码分发)
    * [虚拟服务器](#虚拟服务器)
    * [在线投票](#在线投票)
* [其他工具](#其他工具)
    * [DNS](#dns)
    * [URL 短缩器](#url-短缩器)
    * [共享片段](#分享代码片段)
    * [机器列表](#机器列表)
    * [奇思妙想](#)

## 为顶级项目（TLP）提供的服务

### 网站

* www.apache.org 这是 Apache 的主要网站。
* [Apache 项目网站检查器](https://whimsy.apache.org/site/) 会定期检查所有为顶级项目（TLP）提供的网站，并报告它们是否符合 Apache 的 TLP 网站政策。

这里只列出了几个挺有意思的连接，比如项目网址检查器，它会检查顶级项目是否有 License, Donate, Sponsors, Privacy 等正确的连接。

### 电子邮件

* 所有新建电子邮件列表的申请都应通过[自助服务系统](https://selfserve.apache.org/mailinglist-new.html)进行。
* 电子邮件服务器 - QMail/QSMTPD



### ASF自助服务平台

* Infra 的目标之一是让 ASF 成员、PMC 和提交者有能力完成他们需要做的大部分工作，而无需向 Infra 求助。例如，[自助服务平台](https://selfserve.apache.org/)提供了许多方便的工具，拥有 Apache 电子邮件地址的人（基本上是项目提交者、PMC 成员和 ASF 成员）可以使用这些工具：

    * 创建 Jira 或 Confluence 项目、Git 仓库或电子邮件列表（PMC 主席和 Infra 成员）。
    * 编辑你的 ASF 身份或更新你的 ASF 密码。如果要更新密码，则需要访问与 Apache 帐户相关联的电子邮件帐户。重置密钥的有效期只有 15 分钟，因此请务必在收到密钥后立即使用。
    * 同步 Git 仓库。
    * 使用 OTP 计算器为 OTP 或 S/Key 一次性密码系统生成一次性密码（一般用于 PMC 成员）。
    * 将 Confluence Wiki 空间存档并设置为只读。

不属于 ASF 社区但希望提交有关 ASF 项目产品的 Jira 票据的人员可使用该平台[申请 Jira 账户](https://infra.apache.org/jira-guidelines.html#who)。

### ASF账户管理

如果你想更新账户详情或丢失了账户访问权限，[ASF 账户管理](https://infra.apache.org/account-mgmt.html)可为你提供指导。

### 支持LDAP的服务

Infra 支持许多 [LDAP 的 ASF 服务](https://cwiki.apache.org/confluence/display/INFRA/LDAP+enabled+services+at+the+ASF)。你可以使用 LDAP 凭据登录这些服务。

### 孵化项目服务

Infra 支持孵化项目。

* [Infra 孵化器介绍](https://infra.apache.org/infra-incubator.html)，展示了建立孵化项目的步骤。
* [项目或产品名称选择指南](https://apache.org/foundation/marks/pmcs.html#naming)

### ASF项目工具

Infra 支持一系列工具和服务，以帮助项目开发和支持其应用程序及其社区，包括

* 每个项目都可以在 [Confluence 维基](https://infra.apache.org/cwiki.html)上使用专用空间。
    * 如何管理项目维基空间的用户权限。
    * 如何授予用户编辑维基空间的权限。
* Reporter 提供有关项目的活动统计和其他信息，并提供编辑工具，帮助你撰写和提交项目的季度董事会报告。
* 你可以创建并运行项目博客。
* 你可以建立一个 Slack 频道，用于团队实时讨论。一旦你建立了 Slack 频道，Infra 就可以建立 Slack-Jira 桥接，这样你就可以在频道中收到新的或更新的 Jira 票据通知。
* 团队可以使用 ASFBot 通过 Internet Relay Chat (IRC) 进行并记录会议。不过，你必须按照 Apache 投票流程，在相应的项目电子邮件列表中对决策进行正式投票。
* [本地化工具](https://infra.apache.org/localization.html)。
* Apache [发布审核工具 (RAT)](https://creadur.apache.org/rat/) 可帮助你确认所提议的产品发布符合 ASF 的所有要求。
* ASF [OAuth](https://oauth.apache.org/api.html) 系统为希望使用身份验证的服务提供了一个协调中心，而不会对存储敏感用户数据造成安全影响。许多 Apache 服务使用它来验证请求访问的用户是否是项目中的提交者，以及是否拥有对相关系统的合法访问权限。了解更多有关 Apache OAuth 的信息。

### 版本控制

Apache 提供并由 Infra 维护代码库，Apache 项目可使用这些代码库来保证项目代码的安全、团队成员的可访问性以及版本控制。

* 关于使用 【Git 的信息](https://infra.apache.org/git-primer.html)
    * [SVN 代码库的只读 Git 镜像](https://infra.apache.org/git.html)
    * [可写的 Git 代码库](https://infra.apache.org/project-repo-policy.html)
    * [Apache 与 GitHub](https://infra.apache.org/apache-github.html)
    * [GitHub 仓库的访问角色](https://infra.apache.org/github-roles.html)

* 关于使用 [Subversion 的信息](https://infra.apache.org/svn-basics.html)
    * [Subversion (SVN) 版本库](https://svn.apache.org/repos/asf/)
    * [ViewVC（SVN 主版本库的浏览器界面）](https://svn.apache.org/viewvc/)

### 问题跟踪和功能请求

ASF 支持以下用于跟踪问题和功能请求的选项：
    * [Jira](https://issues.apache.org/jira)
    * [GitHub 问题跟踪功能](https://guides.github.com/features/issues/)

由于历史原因，一些项目使用 [Bugzilla](https://bz.apache.org/bugzilla/)。我们将继续支持 Bugzilla，但不会为尚未使用它的项目设置。

[Apache Allura](https://allura.apache.org/) 是另一个问题跟踪选项。如果你觉得它可以满足你的项目需求，请通过 users@allura.apache.org 邮件列表直接咨询 Allura 项目。

请参阅 issues.apache.org，查看各项目使用的问题列表。

以下是为你的项目[申请 bug 和问题跟踪器的方法](https://infra.apache.org/request-bug-tracker.html)。

以下是[撰写优秀错误报告的指南](https://infra.apache.org/bug-writing-guide.html)。

### 将你的版本库与Jira票据集成

Infra 可以为你的项目[激活 Subversion 和 Git 与 Jira 票据的集成](https://infra.apache.org/svngit2jira.html)。

### 源码库发布者/订阅者服务

* SvnPubSub
* [PyPubSub](https://infra.apache.org/pypubsub.html)

### 构建服务

Apache 支持并模拟持续集成和持续部署（或 CI/CD）。ASF 构建和支持的服务页面提供了有关 ASF 提供和/或支持的 CI 服务的信息和链接。

其他可考虑的工具:

* [Travis CI](https://travis-ci.org/)
* [Appveyor](https://www.appveyor.com/)

### 产品命名

请参阅[产品名称选择指南](https://apache.org/foundation/marks/pmcs.html#naming)

### 代码签名

* 数字证书源码库发布者/订阅者服务

    * 请求[访问 Digicert 代码签名服务](https://infra.apache.org/digicert-access.html)
    * [使用 Digicert](https://infra.apache.org/digicert-use.html)
* 通过[苹果应用程序商店发布](https://cwiki.apache.org/confluence/display/INFRA/Distribution+via+the+Apple+App+Store)
* 关于[代码签名和发布](https://cwiki.apache.org/confluence/display/INFRA/Code+Signing+and+Publishing)的更多信息

### 代码质量

[SonarCloud](https://sonarcloud.io/) 是一款代码质量和安全工具，开源项目可免费使用。它允许对代码质量进行持续检查，因此你的项目可以通过对代码进行静态分析来执行自动审查，以检测 20 多种编程语言中的错误、代码气味和安全漏洞。

你可以[检查许多 Apache 项目软件源的状态](https://sonarcloud.io/organizations/apache/projects)。

有关在 ASF 项目中使用 SonarCloud 的指导，请点击[此处](https://cwiki.apache.org/confluence/display/INFRA/SonarCloud+for+ASF+projects)。

### 代码分发

使用 ASF [Nexus Repository Manager](https://repository.apache.org/#welcome) 浏览和审查 ASF 项目的代码发布。

#### 发布

* [当前发布](https://www.apache.org/dyn/closer.lua)
* [历史发布存档](https://archive.apache.org/)
* [Rsync 分发镜像](https://infra.apache.org/how-to-mirror.html)
* [Nexus](https://repository.apache.org/)

### 虚拟服务器

Infra 可为项目提供 Ubuntu 虚拟机。

* [虚拟机策略](https://infra.apache.org/vm-policy.html)
* [申请虚拟机的流程](https://infra.apache.org/vm-for-project.html)

### 使用nightlies.a.o

nightlies.a.o 如其名称所示，是一种 "短期 "存储解决方案。请参阅 [nightlies 使用政策](https://infra.apache.org/nightlies.html)。

### 在线投票

项目可使用 [Apache STeVe](https://steve.apache.org/) 投票系统实例（不使用时离线）。工具名称指的是作为投票选项之一的单一可转移投票系统。为 Infra 开立 Jira 票单，以便为你的项目使用 STeVe 做好准备。

## 其他工具

### DNS

Infra 管理在 Namecheap 注册的 ASF DNS。

### URL短缩器

[URL 短缩器](https://s.apache.org/)

### 分享代码片段

[Paste](https://paste.apache.org/) 是一项服务，ASF 成员可以发布代码片段或类似的文件摘要，以说明代码问题或供重复使用，通常是与其他项目成员共享。你可以以纯文本形式发布内容，也可以以多种编码和格式发布内容。

### 机器列表

[主机密钥和指纹](https://infra.apache.org/machines.html)

### 奇思妙想

[Apache Whimsy](https://whimsy.apache.org/) 自称为 "以易于使用的方式提供有关 ASF 和我们项目的组织信息，并帮助 ASF 实现企业流程自动化，使我们众多的志愿者能够更轻松地处理幕后工作"。

Whimsy 有许多对项目管理委员会和个人提交者有用的工具，例如提交者搜索。

## 总结

以上就是 Apache 开源软件基金会用到的一些服务和工具，总体的感觉就是写的很全面，并且每个连接都对应着完整的文档，这也是这种开源协作方式最重要的地方：通读文档。另外这种组织方式对于想参与的人来说很清晰，值得学习。

* 另外我们看到了一些常见的服务和工具，像是 Jira，Confluence，Slack，Git，GitHub，SonarCloud，Digicert，Nexus。
* 也看到了不太常见的工具，像在 CI 工具上的选择是 Travis CI 和 Appveyor。
* 还有一些有意思的工具，像是 URL缩短器，代码片段分享，奇思妙想等工具，从访问的网址来看它们是部署在内部。
* 由于历史原因，还有项目还在使用 Bugzilla 和 SVN 等工具。

以上 Apache 所使用的服务和工具，借用理财中风险评估等级划分是属于**稳健型**，而非一味的追求“新”、“开源”和“免费”。

> 为了文章的可读性，本文做了部分修改和删减。原文在[这里](https://infra.apache.org/services.html)。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
