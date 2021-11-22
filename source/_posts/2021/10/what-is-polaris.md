---
title: Polaris - 静态代码分析
tags:
  - Polaris
  - Static
  - Coverity
  - Security
categories:
  - Polaris
date: 2021-10-24 21:33:53
author: shenxianpeng
---

> 这可能是中文网里介绍Polaris最详细的文章了

## 什么是 Polaris？

**Polaris** - 托管静态应用程序软件测试(SAST)工具的 SaaS 平台，它是用于分类和修复漏洞并运行报告的 Web 站点。
**SAST** - 一种对源代码分析或构建过程中去寻找安全漏洞的工具，是一种在软件开发的生命周期(SDLC)中确保安全的重要步骤。
**Coverity** - Coverity 是 Synopsys 公司提供的原始静态应用软件测试 (SAST) 工具。Polaris 是 Coverity 的 SaaS 版本。
**Synopsys** - 是开发 Polaris 和其他软件扫描工具的公司，比如 BlackDuck 也是他们的产品。

## Polaris 支持哪些语言？

```text
C/C++
C#
Java
JavaScript
TypeScript
PHP
Python
Fortran
Swift
...and more
```

## Polaris SaaS 平台

通常如果你的组织引入了 Polaris 的 SaaS 服务，你将会有如下网址可供访问 URL: https://organization.polaris.synopsys.com

然后登录，你就可以给自己的 Git Repository 创建对应的项目了。

> 建议：创建的项目名称与 Git Repository 的名称一致。

## Polaris 如何进行漏洞扫描？

### Polaris 安装

在进行 Polaris 扫描之前，你需要先下载并安装 polaris。

如果你的 Polaris server URL 为：`POLARIS_SERVER_URL=https://organization.polaris.synopsys.com`

下载连接为：`$POLARIS_SERVER_URL/api/tools/polaris_cli-linux64.zip`

然后将下载到本地的 `polaris_cli-linux64.zip` 进行解压，将其 bin 目录添加到 PATH 中。

### Polaris YAML 文件配置

在进行扫描之前，你需要为你的项目创建 YAML 文件。默认配置文件名为 `polaris.yml`，位于项目根目录。如果你希望指定不同的配置文件名，你可以在 `polaris` 命令中使用 `-c` 选项。

在项目根目录运行 `polaris setup` 以生成通用的 `polaris.yml` 文件。

运行 `polaris configure` 以确认你的文件在语法上是正确的并且 `polaris` 没有任何问题。

#### Capture - 捕获

YAML 配置文件可以包含三种类型的 Capture：

* Build(构建) - 运行构建命令，然后分析结果
* Filesystem(文件系统) - 对于解释型语言，提供项目类型和要分析的扩展列表
* Buildless - 对于一些可以使用依赖管理器的语言，比如 maven

| Languages  | Build Options  |
|---|---|
| C, C++, ObjectiveC, Objective C++,Go, Scala, Swift  | 使用 Build 捕获
| PHP, Python, Ruby  | 使用 Buildless 或 Filesystem 捕获 |
| C#, Visual Basic. | 如果想获得更准确的结果使用 Build 捕获；如果寻求简单使用 Buildless 捕获 |
| Java | 如果想获得更准确的结果使用 Build 捕获；如果寻求简单使用 Buildless 捕获  |
| JavaScript,TypeScript | 使用 Filesystem 捕获；如果寻求简单使用 Buildless 捕获

#### Analyze - 分析

如果你正在扫描 C/C++ 代码，则应包括此分析部分以充分利用 Polaris 的扫描功能：

```yml
analyze:
  mode: central
  coverity:
    cov-analyze: ["--security","--concurrency"]
```

#### Polaris YAML 示例文件

<!-- more -->

示例1：一个C/C++ 项目

```yml
version: "1"
project:
  name: test-cplus-demo
  branch: ${scm.git.branch}
  revision:
    name: ${scm.git.commit}
    date: ${scm.git.commit.date}
capture:
  build:
    cleanCommands:
    - shell: [make, -f, GNUmakefile, clean]
    buildCommands:
    - shell: [make, -f, GNUmakefile]
analyze:
  mode: central
install:
  coverity:
    version: default
serverUrl: https://organization.polaris.synopsys.com
```

示例2：一个 Java 项目

```yml
version: "1"
project:
  name: test-java-demo
  branch: ${scm.git.branch}
  revision:
    name: ${scm.git.commit}
    date: ${scm.git.commit.date}
capture:
  build:
    cleanCommands:
    - shell: [gradle, -b, build.gradle, --no-daemon, clean]
    buildCommands:
    - shell: [gradle, -b, build.gradle, --no-daemon, shadowJar]
  fileSystem:
    ears:
      extensions: [ear]
      files:
      - directory: ${project.projectDir}
    java:
      files:
      - directory: ${project.projectDir}
    javascript:
      files:
      - directory: client-vscode
      - excludeRegex: node_modules|bower_components|vendor
    python:
      files:
      - directory: ${project.projectDir}
    wars:
      extensions: [war]
      files:
      - directory: ${project.projectDir}
analyze:
  mode: central
install:
  coverity:
    version: default
serverUrl: https://organization.polaris.synopsys.com
```

示例3：一个 CSharp 项目

```yml
version: "1"
project:
  name: test-ssharp-demo
  branch: ${scm.git.branch}
  revision:
    name: ${scm.git.commit}
    date: ${scm.git.commit.date}
capture:
  build:
    buildCommands:
    # 如果构建过程很复杂，你可以写一个脚本，然后调用它
    - shell: ['script\polaris.bat']
    # 跳过一些你不想扫描的文件
    skipFiles:
    - "*.java"
    - "*.text"
    - "*.js"
analyze:
  mode: central
install:
  coverity:
    version: default
serverUrl: https://organization.polaris.synopsys.com
```

更多关于如何编写 `polaris.yml` 就不一一罗列了，详细请参考 Polaris 的官方文档：https://sig-docs.synopsys.com/polaris/topics/c_conf-overview.html

### 执行分析

可以使用如下命令进行 Polaris 分析：

```bash
polaris -c polaris.yml analyze -w --coverity-ignore-capture-failure
```

`--coverity-ignore-capture-failure` - 忽略 Coverity 捕获失败。运行 `polaris help analyze` 可以查看更多分析命令的介绍。

### Polaris 分析结果

如果 Polaris 分析成功，将会在控制台看到一条成功信息如下：

```bash
[INFO] [1zb99xsu] Coverity job completed successfully!

[INFO] [1zb99xsu] Coverity - analyze phase took 4m 36.526s.
Analysis Completed.
Coverity analysis
{
 "JobId": "mlkik4esb961p0dtq8i6m7pm14",
 "Status": "Success"
}
Job issue summary
{
 "IssuesBySeverity": {
  "Critical": 0,
  "High": 250,
  "Medium": 359,
  "Low": 81
 },
 "Total": 690,
 "NewIssues": 0,
 "ClosedIssues": 0,
 "SummaryUrl": "https://organization.polaris.synopsys.com/projects/bb079756-194e-4645-9121-5131493a0c93/branches/d567c376-4d5d-4941-8733-aa27bb2f5f5b"
}
```

这里显示了一共发现了多少 690 个漏洞，以及每种不同严重程度各占多少个。具体的漏洞信息需要登录到 Polaris SaaS 平台进行查看。

点击 `SummaryUrl` 中的链接将会直接跳转到该项目的 Polaris 扫描结果。

![Summary](what-is-polaris/summary.png)

![Issues](what-is-polaris/issues.png)
