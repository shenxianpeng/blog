---
title: 为什么我的 Jenkins Controller 越来越慢？可能犯了这些错误...
tags:
  - Jenkins
  - pipeline
categories:
  - Jenkins
author: shenxianpeng
date: 2023-02-06 21:52:12
---

就像标题所说的，为什么我的 Jenkins Controller 越来越慢，可能是因为没有遵循 Jenkins pipeline 编写的一些最佳实践。

所以主要介绍 Jenkins pipeline 的一些最佳实践，目的是为了向 pipeline 作者和维护者展示一些他们过去可能并没有意识到的“反模式”。

我会尽量列出所有可能的 Pipeline 最佳实践，并提供一些实践中常见的具体示例。

## 一般问题

### 确保在 pipeline 中使用 Groovy 代码作为粘帖剂

使用 Groovy 代码连接一组操作而不是作为 pipeline 的主要功能。

换句话说，与其依赖 pipeline 功能（Groovy 或 pipeline 步骤）来推动构建过程向前发展，不如使用单个步骤（例如 `sh`）来完成构建的多个部分。

pipeline 随着其复杂性的增加（Groovy 代码量、使用的步骤数等），需要 controller 上的更多资源（CPU、内存、存储）。将 Pipeline 视为完成构建的工具，而不是构建的核心。

示例：使用单个 Maven 构建步骤通过其构建/测试/部署过程来驱动构建。

### 在 Jenkins pipeline 中运行 shell 脚本

在 Jenkins Pipeline 中使用 shell 脚本可以通过将多个步骤合并到一个阶段来帮助简化构建。shell 脚本还允许用户添加或更新命令，而无需单独修改每个步骤或阶段。

Jenkins Pipeline 中使用 shell 脚本及其提供的好处：

<!-- more -->

### 避免 pipeline 中的复杂 Groovy 代码

对于 pipeline，Groovy 代码始终在 controller 上执行，这意味着使用 controller 资源（内存和 CPU）。

因此，减少 Pipeline 执行的 Groovy 代码量至关重要（这包括在 Pipeline 中导入的类上调用的任何方法）。以下是要避免使用的最常见 Groovy 方法示例：

1. `JsonSlurper`：此函数（以及其他一些类似函数，如 `XmlSlurper` 或 `readFile`）可用于从磁盘上的文件中读取数据，将该文件中的数据解析为 `JSON` 对象，然后使用 `JsonSlurper().parseText(readFile("$LOCAL_FILE"))`。该命令两次将本地文件加载到 controller 的内存中，如果文件很大或命令执行频繁，将需要大量内存。

    解决方案：不使用 `JsonSlurper`，而是使用 shell 步骤并返回标准输出。这个 shell 看起来像这样：`def JsonReturn = sh label: '', returnStdout: true, script: 'echo "$LOCAL_FILE"| jq "$PARSING_QUERY"'`。这将使用代理资源来读取文件，`$PARSING_QUERY` 将帮助将文件解析成更小的尺寸。

2. `HttpRequest`：此命令经常用于从外部源获取数据并将其存储在变量中。这种做法并不理想，因为不仅该请求直接来自 controller （如果 controller 没有加载证书，这可能会为 HTTPS 请求之类的事情提供错误的结果），而且对该请求的响应被存储了两次。

    解决方案：使用 shell 步骤执行来自代理的 HTTP 请求，例如使用 curl 或 wget 等工具，视情况而定。如果结果必须在 Pipeline 的后面，尽量在 agent 端过滤结果，这样只有最少的需要的信息必须传回 Jenkins controller。

### 减少类似 pipeline 步骤的重复

尽可能多地将 pipeline 步骤组合成单个步骤，以减少 pipeline 执行引擎本身造成的开销。

例如，如果你连续运行三个 shell 步骤，则每个步骤都必须启动和停止，需要创建和清理 agent 和 controller 上的连接和资源。

但是，如果将所有命令放入单个 shell 步骤，则只需启动和停止一个步骤。

示例：与其创建一系列 `echo` 或 `sh` 步骤，不如将它们组合成一个步骤或脚本。

### 避免调用 `Jenkins.getInstance`

在 Pipeline 或共享库中使用 Jenkins.instance 或其访问器方法表示该 Pipeline/共享库中的代码滥用。

从非沙盒共享库使用 Jenkins API 意味着共享库既是共享库又是一种 Jenkins 插件。

从 pipeline 与 Jenkins API 交互时需要非常小心，以避免严重的安全和性能问题。如果你必须在你的构建中使用 Jenkins API，推荐的方法是在 Java 中创建一个最小的插件，它在你想要使用 Pipeline 的 Step API 访问的 Jenkins API 周围实现一个安全的包装器。

直接从沙盒 Jenkinsfile 使用 Jenkins API 意味着你可能不得不将允许沙盒保护的方法列入白名单，任何可以修改 pipeline 的人都可以绕过它，这是一个重大的安全风险。列入白名单的方法以系统用户身份运行，具有整体管理员权限，这可能导致开发人员拥有比预期更高的权限。

解决方案：最好的解决方案是解决正在进行的调用，但如果必须完成这些调用，那么最好实施一个能够收集所需数据的 Jenkins 插件。

### 清理旧的 Jenkins 构建

作为 Jenkins 管理员，删除旧的或不需要的构建可以使 Jenkins controller 高效运行。

当你不删除旧版本时，用于更新和相关版本的资源就会减少。可以在每个 pipeline 作业中使用 `buildDiscarder` 来保留特定历史构建数量。

## 使用共享库

### 不要覆盖内置的 pipeline 步骤

尽可能远离自定义/覆盖的 pipeline 步骤。覆盖内置 pipeline 步骤是使用共享库覆盖标准 pipeline API（如 `sh` 或 `timeout`）的过程。此过程很危险，因为 pipeline API 可能随时更改，导致自定义代码中断或给出与预期不同的结果。

当自定义代码因 Pipeline API 更改而中断时，故障排除很困难，因为即使自定义代码没有更改，在 API 更新后它也可能无法正常工作。

因此，即使自定义代码没有更改，也不意味着在 API 更新后它会保持不变。

最后，由于在整个 pipeline 中普遍使用这些步骤，如果某些内容编码不正确/效率低下，结果对 Jenkins 来说可能是灾难性的。

### 避免大型全局变量声明文件

拥有较大的变量声明文件可能需要大量内存而几乎没有任何好处，因为无论是否需要变量，都会为每个 pipeline 加载该文件。

**建议创建仅包含与当前执行相关的变量的小变量文件。**

### 避免非常大的共享库

在 Pipelines 中使用大型共享库需要在 Pipeline 启动之前检出一个非常大的文件，并为当前正在执行的每个作业加载相同的共享库，这会导致内存开销增加和执行时间变慢。

## 回答其他常见问题

### 处理 pipeline 中的并发

尽量不要跨多个 pipeline 执行或多个不同的 pipeline 共享工作区。这种做法可能会导致每个 pipeline 中的意外文件修改或工作区重命名。

理想情况下，共享卷/磁盘安装在单独的位置，文件从该位置复制到当前工作区，然后当构建完成时，如果有更新完成，文件可以被复制回来。

构建不同的容器，从头开始创建所需的资源（云类型代理非常适合此）。构建这些容器将确保构建过程每次都从头开始，并且很容易重复。如果构建容器不起作用，请禁用 pipeline 上的并发性或使用可锁定资源插件在运行时锁定工作区，以便其他构建在锁定时无法使用它。

警告：如果这些资源被任意锁定，则在运行时禁用并发或锁定工作区可能会导致 pipeline 在等待资源时被阻塞。

**另外，请注意，与为每个作业使用唯一资源相比，这两种方法获得构建结果的时间都比较慢。**

### 避免 `NotSerializableException`

Pipeline 代码经过 CPS 转换，以便 pipeline 能够在 Jenkins 重启后恢复。也就是说，当 pipeline 正在运行你的脚本时，你可以关闭 Jenkins 或失去与代理的连接。当它返回时，Jenkins 会记住它在做什么，并且你的 pipeline 脚本会恢复执行，就好像它从未被中断过一样。一种称为“连续传递样式 (CPS)”的执行技术在恢复 pipeline 中起着关键作用。但是，由于 CPS 转换，某些 Groovy 表达式无法正常工作。

在幕后，CPS 依赖于能够序列化 pipeline 的当前状态以及要执行的 pipeline 的其余部分。
这意味着在 pipeline 中使用不可序列化的对象将触发 `NotSerializableException` 在 pipeline 尝试保留其状态时抛出。

有关更多详细信息和一些可能有问题的示例，请参阅 [Pipeline CPS 方法不匹配](http://jenkins.io/redirect/pipeline-cps-method-mismatches)。

下面将介绍确保 pipeline 能够按预期运行的技术。

### 确保持久变量可序列化

在序列化期间，局部变量作为 pipeline 状态的一部分被捕获。这意味着在 pipeline 执行期间将不可序列化的对象存储在变量中将导致抛出 `NotSerializableException`。

### 不要将不可序列化的对象分配给变量

一种策略是利用不可序列化的对象始终“及时”推断它们的值，而不是计算它们的值并将该值存储在变量中。

### 使用 `@NonCPS`

如果有必要，你可以使用 `@NonCPS` 注释为特定方法禁用 CPS 转换，如果它经过 CPS 转换，该方法的主体将无法正确执行。请注意，这也意味着 Groovy 函数将不得不完全重新启动，因为它没有被转换。

> 异步 pipeline 步骤（例如 `sh` 和 `sleep`）始终是 CPS 转换的，并且不能在使用 `@NonCPS` 注释的方法内部使用。通常，你应该避免在使用 `@NonCPS` 注释的方法内部使用 pipeline 步骤。

### Pipeline 耐久性

值得注意的是，更改 pipeline 的持久性可能会导致 `NotSerializableException` 不会被抛出，否则它们会被抛出。这是因为通过 `PERFORMANCE_OPTIMIZED` 降低 pipeline 的持久性意味着 pipeline 当前状态的持久化频率大大降低。因此，pipeline 从不尝试序列化不可序列化的值，因此不会抛出异常。

> 此注释的存在是为了告知用户此行为的根本原因。不建议纯粹为了避免可串行化问题而将 pipeline 的持久性设置设置为性能优化。

* https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/
* https://www.cloudbees.com/blog/top-10-best-practices-jenkins-pipeline-plugin
* https://github.com/jenkinsci/pipeline-examples/blob/master/docs/BEST_PRACTICES.md
* https://devopscook.com/jenkinsfile-best-practices/

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
