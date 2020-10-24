---
title: 企业版 Artifactory 的实践分享
tags:
  - Artifactory
  - JFrog
categories:
  - DevOps
date: 2020-10-4 20:43:46
author: shenxianpeng
---

本篇介绍使用企业版 Artifactory 有哪些优势。以及如何使用、工作流（包括，仓库命名，目录结构，Jenkins关键）、仓库权限、保留策略的实践分享。

## 什么是Artifactory

一句话概括：Artifactory 是一个存放制品（Artifacts）的工具。目前，Artifactory 是一个非常流行，非常强大的 DevOps 工具链中非常重要的工具。

## Artifactory有哪些优势

可能你的团队已经有了存放构建的工具了，比如 FTP，但为什么还了解 Artifactory。这就要说说它到底有有哪些优势。

> 以下优势都是针对 JFrog Aritifacvtory 企业版来介绍的。开源版，即 OSS 版本不具备以下丰富的功能。

### 它是一个通用管理仓库

JFrog Artifactory 完全支持所有主要包格式的存储库管理器。它不但可以管理二进制文件，也可以对市面上几乎所有语言的包的依赖进行管理，如下图所示。

![主要的包格式](what-is-artifactory/support-package-formats.png)

因此，使用 Artifactory 能够将所有的二进制文件和包存储在一个地方。

<!-- more -->

### 很好的与 CI 工具进行集成

它支持所有主流 CI 工具（如下图所示），并在部署期间捕获详尽的构建环境信息，以实现可完全复制的构建。

![](what-is-artifactory/ci-tools.png)

另外通过提供的丰富的 REST API，因此GUI页面上的任何操作都可以通过代码以编程方式完成，方便做持续集成。


### 提供强大的搜索功能

如果你的构建是存储在 FTP 上，如果你想从大量的制品中找到你要找的那一个，如果你还不知道它的名字，那么真的很难快速找到。

Artifactory 提供了强大的搜索功能，你可以通过带有正则表达的名字进行搜索，还可以通过文件的 checksum，以及通过属性（Properties）等进行快速搜索。

#### 通过名字搜索

你想找某一个提交点的构建制品，假设那个提交点的 commit hash 是 `a422912`，那么你就可以直接输入 `*a422912*` 快速的从众多的制品中返回对应的构建，例如 Demo_Linux_bin_a422912.zip

![](what-is-artifactory/search-by-name.png)

#### 通过属性搜索

比如要找属性 release.status 为 released 的所有构建那么就可以这样搜索。

![](what-is-artifactory/search-by-property.png)

#### 通过 checksum 搜索

如果只知道一个文件的 `checksum`，也可以进行搜索。例如通过 `sha1sum` 计算出文件的 `checksum`

```
$ sha1sum test.zip
ad62c72fb097fc4aa7723e1fc72b08a6ebcacfd1 *test.zip
```

![](what-is-artifactory/search-by-checksum.png)

### 管理制品的生命周期

通过定义不同成熟度存储库，然后使用 Artifactory Promote 功能可以将制品移动到不同的成熟度存储库，以及通过元数据属性，可以很好的管理和维护制品的生命周期。


除了这些优点之外，Artifactory 还有更多的特点，但我不会在这次会议上一一介绍。

> 更多可以浏览 JFrog Artifactory 的官方介绍 https://jfrog.com/artifactory/features/

接下来我通过一个 Demo 来介绍 Artifactory 应该怎么使用，以及其中有哪些最佳实践与你分享。


## Artifactory首页介绍

![Artifactory Home](what-is-artifactory/artifactory-home.png)

### 页面上部

你可以看到 Artifactory 已经服务了超过5000件的制品。然后可以看到Artifactory 企业版的当前版本号，以及最新版本。

### 页面中部，从左到右

1. 你可以看到搜索功能，它使搜索制品变得很容易。然后是一些有用的信息，包括用户手册、视频、REST API 文档等。

2. Set Me Up 在中间，使用它可以选择和筛选你想要关注的存储库，单击特定的存储库将弹出关于如何使用它的详细说明。

3. 最右边是显示的是最近部署的构建和最多下载量的制品（最多被下载时95次）

### 页面底部

在底部是一些与 Artifactory 集成的相关工具和技术用户文档。

## 实践和工作流

### 设置关注的仓库

在首页的 Set Me Up 里你也看到了我们有很多仓库（Repository），然后对你想关注的仓库。 添加喜欢，然后点击喜欢按钮就可以只列出你关注的 Artifact Repository。

![Artifacts](what-is-artifactory/artifactory-artifacts.png)

### Artifactory 仓库命名方法

在这个列表仓库中，你可以从这些仓库的名称中看到遵循了某些命名约定，这是 [JFrog Artifactory 推荐的官方命名](https://jfrog.com/whitepaper/best-practices-structuring-naming-artifactory-repositories/)方法，它是由四部分组成：

`<team>-<technology>-<maturity>-<locator>`
 
* 这里 team 我做了脱敏，我们叫它 team1。
* 然后是技术，这里有很多选项，比如 generic, Docker, Maven, NPM 等等，这里我们的产品是 C/C++ 编译出来的二进制文件，它属于 generic 类别
* 接下来是成熟度（maturity），一个仓库通常由四个级别的成熟度，从低到搞这里分别是 dev, int, stage 和 release。
* 最后是表明制品的位置在哪里。比如一个跨国公司，它为了保证上传/下载速度等因素，会在全球部署多个 Artifactory 站点。图上的 den 就是当前 Artifactory 所在位置的缩写。

### 从构建的生成到发布，了解它的工作流

dev 意味着 development（开发），该仓库对所有产品成员都具有读写权限，他们可以上传一些库或其他一些二进制文件。

int 表示 integration（集成）的意思，比如从 Jenkins 里成功构建的制品将首先放在这个存储库下。如果构建失败，它将不会被上传到 Artifactory。

#### 规范分支命名有利于Artifactory的目录清晰

例如，一个产品叫 ART，它的 Git 仓库也叫 ART，它下面有这样一个分支 `feature/ART-1234`

Jenkins Pipeline 里的环境变量设置如下：

```
environment {
  INT_REPO_PATH = "team1-generic-int-den/ART/${BRANCH_NAME}/${BUILD_NUMBER}/"
}
```

这个分支通过 Jenkins 第1构建成功后，它首先会被 `team1-generic-int-den` 仓库下的 `ART/feature/ART-1234/1/` 的目录下面，如果进行第2次构建，并成功，那么它的制品目录会是：

`team1-generic-int-den/ART/feature/ART-1234/2/` 依次类推。

为了更好的管理仓库下面的目录，这里我强力建议团队事先做好分支的命名规范，这样同一种类型的分支的所有构建都会出现在一个目录下面。

关于命名规范可参见这篇文章[程序员自我修养之Git提交信息和分支创建规范](https://shenxianpeng.github.io/2020/09/commit-messages-specification/)

对于 Pull Request Build 如果也想放到 Artifactory 上面，建议像下面这样设置：

```
environment {
  PR_INT_REPO_PATH = "team1-generic-int-den/ART/PRs/${BRANCH_NAME}/${BUILD_NUMBER}/"
}
```

这样所有的 Pull Request Build 构建成功后都会被放到 `PRs` 这个目录下，方便查找和管理。

#### 不同阶段添加不同的属性

如果以上的构建通过了一些质量关卡，比如通过了自动化测试以及 sonaqube 的扫描等等，可进入待人工测试状态，可以通过 Artifactory Promote 功能在，将构建从 int 仓库自动移动到 stage 仓库（需要在 Pipeline 写好这部分的动作代码）

然后测试工程师就可以到 stage 仓库下去获取构建，进行测试了。通过测试后，对制品添加相应的属性状态，比如在 Property 中添加 `manual.test.status=passed`。

之后发布流水线中去到 stage 仓库里去找这些状态为通过的构建进行发布。 

```
automated.test.status=passed
sonaqube.scan.status=passed
manual.test.status=passed
```

发布成功后，将构建从 stage 仓库 promote 到 release 仓库中，并添加属性 `release.status=released`，这样就完成了发布。

这个过程中，就像使用漏斗一样将构建通过层层帅选，从 int 仓库到 stage 仓库，最后到 release 仓库完成了发布。

## 仓库权限与保留策略

参考如下：

|仓库(maturity)|保留策略(Retention)|个人账户权限(Personal Account)|服务账户权限(Service Account)|管理员(Admin)|
|---|---|---|---|---|
| dev | 通常不清理  |  read/write | read/write  | all |
| int  | 一周或是几天  | read  | read/write   | all  |
| stage  | 永不清理  | read  |  read/write  | all  |
| release  | 永不清理  | read |  read/write  |  all |

