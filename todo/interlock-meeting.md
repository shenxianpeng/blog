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

Artifactory 是 DevOps 工具链里一个非常重要的工具，使用它来管理我们的构建制品会带来以下这些优势：

* 很好的与 CI 工具进行集成
* 软件包的元数据，记录软件交付的元数据，如 Build 结果，自动化测试结果，以及未来我们把漏洞扫描结果也加上。
* 支持多语言制品仓库的存储，比如 Maven，Npm，Docker 等，减少多工具的维护成本，统一制品来源。

为了更好的实现 CI/CD 流水线，在设计和实施与 Aritifactory 集成我们也做了一些列统一化的工作。

## 统一分支命名规则

> Branch naming rules wiki: https://wiki.rocketsoftware.com/display/ML/Branch+naming+rules

通过定义分支命名规则，可以更好的帮助我们来实施 CI/CD，并且更加有助于在 Artifactory 有清晰的目录结构，以便任何人都可以很容易的找到他想要的分支所对应的构建地址。

另外，通过 Bitbucket 的 Hook 来进一步将分支命名规范的真正的落地，让不符合规范的分支无法推送到我们的产品仓库中。

> Commit and Branch Specifications wiki https://wiki.rocketsoftware.com/display/ML/Commit+and+Branch+Specifications

## 定义 Artifactory 目录结构

> Artifactory Directory Struture wiki https://wiki.rocketsoftware.com/display/ML/Artifactory+Directory+Structure

基于前面定义的分支命名规则，Artifactory 的目录结构就因此定义如图。通过合理目录结构，不但有助于管理，并且方便用户很快找到你想要的 Build。

> 当然了你也可以通过搜索 commit hash 来找到你想要找的 Build https://wiki.rocketsoftware.com/display/ML/Artifactory+User+Guide#ArtifactoryUserGuide-Searchbuildthoughcommithash

可以看到这里一共有四个仓库，他们是按照成熟度来划分的，他们分别是 `DEV`, `INT`, `STAGE`, `RELEASE`。

`DEV` open access for developers

`INT` used by CI builds

`STAGE` pre-production testing

`RELEASE` released components or product images

### Artifactory Permissions Matrix

| Repo Maturity | Product Members | Service Accounts | IT |
|---|---|---|---|
| dev (sandbox)	 | Write | Write | Admin |
| int | Read | Write | Admin |
| stage	 | Read | Write | Admin |
| release	 | Read | Write | Admin |

### 一个 Release 过程中 build 的运转流程

当一个 build 从 Jenkins 里被创建出来的时候，它首先会被放入 `INT` 仓库中，根据它所在分支的名称将它放入到不同的目录下。比如它的分支是 `hotfix/11.3.2.HF1` 分支，那么第一构建成功完成后，它会被放入 `mvas-generic-int-den/uv113/hotfix/11.3.2.HF1/1/` 这个目录下。

如果它时可测的（构建成功、Smoke Test通过等），会将它 promote 到成熟度更高的 `STAGE` 仓库下面，除了仓库名称换了（从 `mvas-generic-int-den` 变成 `mvas-generic-stage-den`）其目录结构不便，它会是 `mvas-generic-stage-den/uv113/hotfix/11.3.2.HF1/1/`

通常情况下，这个 release 发布出去前可能经过几次构建，最终加入我们在第五次构建的时候，这个 build 通过了所有的测试，可以准备发布了。这时候我会将它从 `STAGE` 仓库下将它 promote 到 `RELEASE` 仓库，它的目录是 `mvas-generic-release-den/uv113//hotfix/11.3.2.HF1/5/`。然后进行打包。

打包完成后的 zip files 会发布到 both RBC sites，同时图上的这个目录结果将会把它保存到 Artifactory. `mvas-generic-release-den/RBC/UNV/v11.3.2.7001.HF1/` 目录下。这也是 Backup Strategy 的部分内容。

其他的所有在 `INT` 和 `STAGE` 仓库下面所有有关 `hotfix/11.3.2.HF1` 构建将会被全部删除。最终只保留 `mvas-generic-release-den/uv113//hotfix/11.3.2.HF1/5/` 和 `mvas-generic-release-den/RBC/UNV/v11.3.2.7001.HF1/` 的构建。

TODO: 需要修改diagram里 RBC 的图例。

> Artifactory Work Process https://wiki.rocketsoftware.com/display/ML/Artifactory+Work+Process


# Backup Strategy

> U2 Infra Backup Strategy https://wiki.rocketsoftware.com/display/ML/U2+Infra+Backup+Strategy

我们有一些基础设施是自己搭建的，因此需要自己维护并备份。根据重要等级来划分，我将他们分为 level 1 和 level 2.

## Level 1 Infrastructure

* den-mvfile01.u2lab.rs.com
* Bamboo
* Jenkins

另外还有一些服务是公司提供了，但由于不满足我们的安全策略，因此也需要备份

* RBC
* Denver Artifactory

## Level 2 Infrastructure








