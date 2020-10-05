---
title: 关于 Artifactory 以及基础设施备份策略
tags:
  - Infrastructure
  - Artifactory
  - Backup
categories:
  - DevOps
date: 2020-09-25 17:26:03
author: shenxianpeng
---

# Agenda

* Artifactory
* Backup Strategy
* Commit Stardard 
* Ohter CICD work

# Artifactory

在上次的 Inter lock meeting 上我分享了关于 Jenkins 的三个最佳实践。然后留下了两个主题：一个是关于 Artifactory，另一个是关于 Infrastructure 的管理的备份。

Artifactory 不但是 DevOps 工具链里一个非常重要的工具，也是 Rocket 统一工具链规划中的工具之一。使用它来管理我们的构建制品会带来以下这些优势：

* 它能很好的与 CI 工具进行集成
* 支持记录软件包元数据，比如 Build 结果，自动化测试结果，以及未来我们把漏洞扫描结果都可以在这个构建里添加上。
* 支持多语言制品仓库的存储，比如 Maven，Npm，Docker 等，减少使用多工具带来的维护成本，统一制品来源。

为了更好的实现 CI/CD 流水线，在设计和实施与 Aritifactory 集成做了如下一些列统一化的工作。

## 首先，设计 Artifactory 工作流程

从这个图上可以看到这里一共有四个仓库，他们是基于对于 Artifactory 的使用调研，以及官方的推荐。这四个仓库是按照成熟度来划分的，他们名字中的不同部分分别是 `DEV`, `INT`, `STAGE`, `RELEASE`。

All developers can R/W to Dev but can only read from Int, Stage, and Release. retention policies haven't been finalized, it's not yet fully supported by IT

`DEV` open access for developers。它是用来提供给开发者来使用的，他们可以将一些 libs, 3rdParty 等二进制文件上传到这里，所有 Product Members 都有读写权限。

对于 `INT`, `STAGE`, `RELEASE` 三个仓库 Product Members 只有读权限，Service Accounts 有读写权限，Admin 拥有所有的权限。

`INT` used by CI builds。这个仓库是用来存放 CI 工具完成自动化后的构建，是放置 build 的地方。

`STAGE` pre-production testing。这里我们是用来存放待测试的构建，因此QA或是Support拿取可以测试的构建，都应从这里获取。

`RELEASE` released components or product images。这里是存放可以准备发布或是已经发布的构建。比如 RBC 上的构架也会存放在这里。

因此我们 Aritafactory 的 CI/CD 工作流程是这样的。

* Jenkins 的 Nightly 或是 Pull Request build 如果构建成功，产生出来的 Artifacts 会首先放到 `INT` 仓库中。
* 通过 Smoke Test 或人为确认可测的构建会通过自动和手动的方式，将构建从 `INT` Promote 到 `STAGE` 仓库。QA/Support 通常的测试构建应该从 `STAGE` 获取。
* 一旦构建通过所有的测试，达到可以发布的状态，则将构建从 `STAGE` Promote 到 `RELEASE` 仓库。
* 准备打包的构建从 `RELEASE` 仓库下载，完成打包后
   * Post to Both RBC sites. 
   * 再传回 `RELEASE` 仓库留作备份。

Any questions about this work process? 

## 其次，定义 Artifactory 目录结构

### 统一分支命名规则

为了更好的定义 Artifactory 的目录结构，同时只有有了预期的目录结构，才能更容易使 Jenkins CI/CD 工具以及 rsmate 的设计都清晰明了。这里是我们的分支命名规则。

> Branch naming rules wiki: https://wiki.rocketsoftware.com/display/ML/Branch+naming+rules

在这个规则里最重要的原则就是创建分支时需要指定分支类型，比如 `bugfix` `feature` `hotifx` `release` `diag`。这样当分支很多的时候可以很容易找到 hotfix 分支，快速知道一个分支的是做什么的

这里不但定于了命名规则，并且通过 Bitbucket 的 Hook 来进一步将分支命名规范的真正的落地，让不符合规范的分支无法推送到我们的产品仓库中。

> Commit and Branch Specifications wiki https://wiki.rocketsoftware.com/display/ML/Commit+and+Branch+Specifications

###  Artifactory 目录结构以及 build 如何流转

> Artifactory Directory Structure wiki https://wiki.rocketsoftware.com/display/ML/Artifactory+Directory+Structure

TODO: 插入结构图

通过定义分支命名规则，清晰的 Artifactory 目录结构，有助于任何人都可以很容易的找到他想要的分支所对应的构建地址。

> 当然了你也可以通过搜索 commit hash 来找到你想要找的 Build https://wiki.rocketsoftware.com/display/ML/Artifactory+User+Guide#ArtifactoryUserGuide-Searchbuildthoughcommithash

当一个 build 从 Jenkins 里被创建出来的时候，它首先会被放入 `INT` 仓库中，根据它所在分支的名称将它放入到不同的目录下，每个 `/` 将会产生一个目录。

比如它的分支是 `hotfix/11.3.2.HF1` 分支，那么第一构建成功完成后，它会被放入 `mvas-generic-int-den/uv113/hotfix/11.3.2.HF1/1/` 这个目录下。

> 其中 `uv113` 不但表示它的版本，也是他们的 Git 仓库的名字 `uvuddb-uv113` 的简写，为 `uv113`。依此类推，`ud82` `uv121` 所对应的 Git 仓库分别是 `uvuddb-ud82` 和 `uvuddb`。

如果它是可测的（构建成功、Smoke Test通过等），会将构建 promote 到成熟度更高的 `STAGE` 仓库下面，除了仓库名称换了（从 `mvas-generic-int-den` 变成 `mvas-generic-stage-den`）其目录结构不变，它会是 `mvas-generic-stage-den/uv113/hotfix/11.3.2.HF1/1/`

通常情况下，这个 release 发布出去前可能经过很多次构建，假如在第五次构建的时候，这个 build 通过了所有的测试，可以准备发布了。这时候我会将它从 `STAGE` 仓库下将它 promote 到 `RELEASE` 仓库，它的目录就变成了 `mvas-generic-release-den/uv113//hotfix/11.3.2.HF1/5/`。

然后进行打包。打包完成后的 zip files 会发布到 both RBC sites，同时也会将会把它保存到 Artifactory. `mvas-generic-release-den/RBC/UNV/v11.3.2.7001.HF1/` 目录下。这也是 Backup Strategy 的部分内容。

成功发布周，其他的所有在 `INT` 和 `STAGE` 仓库下面所有有关 `hotfix/11.3.2.HF1` 构建将会被全部删除。最终只保留 `mvas-generic-release-den/uv113//hotfix/11.3.2.HF1/5/` 和 `mvas-generic-release-den/RBC/UNV/v11.3.2.7001.HF1/` 的构建。

TODO: 需要修改diagram里 RBC 的图例。

> Artifactory Work Process https://wiki.rocketsoftware.com/display/ML/Artifactory+Work+Process

# Backup Strategy

> U2 Infra Backup Strategy https://wiki.rocketsoftware.com/display/ML/U2+Infra+Backup+Strategy

备份一些基础设施对于我们的产品也是非常重要的一部分。在 2020 年以前，Bill 是通过三个外置硬盘进行备份的，包括 RBC, mvfile01 和 Bamboo Server。但 2020 年以后，公司的安全策略发生了变化，任何人都不能继续使用外置硬盘了，尽管我们详细阐述了理由，但还是没有得到同意，因此我们的备份策略也相应的发生了变化。

对于我们需要备份的基础设施，根据重要性，将他们分为 level 1 和 level 2 两个级别。

## Level 1 Infrastructure 包括

* RBC
* Denver Artifactory。这是由于当前的 Denver Artifactory 还没有完全被 IT 接管。
* den-mvfile01.u2lab.rs.com
* MV Bamboo Server
* U2 Jenkins Server

这个级别的基础设施是是我们不能承受丢失的数据，因此我们根据现有的 IT 策略，以及我们的资源情况进行最大限度的备份。

例如 RBC 上存放的是我们几十年来交付给客户的构建，但由于 IT backup only keeps files which are in 1 year old，但我们需要保留所有的数据，因此我们还同时存在于在 SharPoint, Denver Artifactory, den-mvfile01.u2lab.rs.com，另外 2020 以前的数据还在一个外置硬盘里。

Denver Artifactory 是未来主要的放置构建以及备份的地方，但是由于目前它还没有完全被 IT 接管，它的备份策略还没有最终确定，因此目前我们还需要自己备份。这里的构建除了 RBC 上的以外（RBC 我们已经在上面做了妥善的备份）其他构建都是从 Jenkins 里 build 出来了，因此它只要 代码在，Jenkins 在，我们就可以构建出来任何我们想要的 build。因此，对于 Denver Artifactory 我们仅将其 `STAGE`, `RELEASE` 仓库下的所有构建同步到另外一个我们自建的 Arifactory 上进行备份。

对于 den-mvfile01.u2lab.rs.com 同样也存放了所有包括 MV U2, SB, wIntergrate 等其他团队的 Artifacts，包括 Builds, 和多年的 Releases 的构建，因此我们也需要尽可能的备份。目前是手动每一至两周将最新的 Artifacts 备份到一个容量为 500 GB 的虚拟机上。

接下来是 MV Bamboo Server，会进行每周一次的将 Bamboo 的自动备份上传到  Self-created Artifactory。

最后是 U2 Jenkins, 虽然我们的 Jenkins 使用 Configuration as code，但一旦这台服务器 crash 了，备份了 Jenkins 的工作目录能够更快速的恢复。因此也是每周进行定期备份，并将备份信息上传到 Denver Artifactory

## Level 2 Infrastructure

Build machines 

* U2 Windows/Linux/Unix build machines 
* UCC Windows build machines 

这个级别的基础设施通常都是 build machine。

So, for all build machines, we have created snapshots for each build machine. And if the product build environment upgrade will need to take another snapshot to capture the previous build environment.

For Linux/Unix build machines, except for the very odl products build machine, most of machines we have knowlage how to set up a new build environment.











