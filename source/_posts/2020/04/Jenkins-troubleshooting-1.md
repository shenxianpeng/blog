---
title: Jenkins Declarative Pipeline throws Method Code Too Large Exception
tags:
  - Pipeline
  - Troubleshooting
categories:
  - Jenkins
date: 2020-04-20 21:33:09
author: shenxianpeng
---

这是我第二次在使用 Jenkins 声明式流水线的时候遇到了这个问题，那时候是一个 Pipeline 里大概写到 600 多行时候遇到的。

```java
org.codehaus.groovy.control.MultipleCompilationErrorsException: startup failed:
General error during class generation: Method code too large!

java.lang.RuntimeException: Method code too large!
	at groovyjarjarasm.asm.MethodWriter.a(Unknown Source)
	[...]
```

当时我也使用了 Jenkins Shared Libraries，但那时候的代码组织的并不是很好，很不少步骤可以单独抽离出来作为单独的方法。经过一番重构，我将原来的 600 多行的 Pipeline 变成了现在的 300 多行，很不巧，今天又遇到了这个问题。

出现这个问题的原因是 Jenkins 将整个声明性管道放入单个方法中，并且在一定大小下，JVM 因 java.lang .RuntimeException 失败：方法代码太大！看来我还是有什么方法超过了 64k。

Jenkins JIRA 上已经有了该问题的单子，但目前为止还是尚未解决。

针对这个问题目前有三种方案，但他们都有各自的利弊。

## 使用 Shared Libraries

我已经有一个共享库来执行一些复杂的步骤，例如将 Sonarqube 分析的结果放入 Bitbucket 中的匹配请求请求中，但是这种方法存在一个主要问题。

顾名思义，共享库应该共享，并且由于它们需要存放在单独的存储库中，因此你需要花费大量的精力来维护适用于你自己项目的强耦合功能。 因此，由于额外的维护工作，我通常不喜欢以当前格式使用它们。

同样，这种方法不会无休止地扩展，因为你仍然可以达到每个阶段都是单线的观点，并且无法进一步缩短它们。

| 优点 | 缺点 |
|---|---|
| 不需要进行重大重构 | 很难维护，因为几乎每个更改都需要触及共享库 |
| 可以分块使用 | 很难理解一个步骤到底是做什么的 |  
| 生成的Jenkinsfile将易于阅读 | 仍然有限，特别是在有很多步骤的管道中 |  

## 将步骤放到管道外的方法中

该解决方案目前是一个未记录的黑客 https://stackoverflow.com/questions/47628248/how-to-create-methods-in-jenkins-declarative-pipeline/47631522#47631522。 自2017年中以来，您只需在管道的末尾声明一个方法，然后在声明性管道中调用它即可。 这样，我们可以达到与共享库相同的效果，但是避免了维护开销。

| 优点 | 缺点 |
|---|---|
| 没有额外的维护费用 |在某种程度上，这个解决方案可能不再有效 |
| 所有的功能都反映在Jenkinsfile中 | 仍然有限，特别是在有很多步骤的管道中 |

## 迁移到脚本管道

最后，我们可以迁移到脚本化的管道。有了它，我们就有了所有的自由。但是我们也会失去我们最初决定使用声明性管道的原因。有了专用的DSL，就很容易理解管道是如何工作的

| 优点 | 缺点 |
|---|---|
| 完全没有限制 | 需要比较大的重构 |
|  | 更容易出错 |
|  | 可能需要更多的代码来实现相同的功能 |

## 结论

由于在开发完全不同的功能时发生了异常，因此我决定暂时在文件末尾使用变通办法和其他方法。 但是可以肯定的是我们需要一个长期的解决方案。 因此，除非找到其他解决方案，否则我们将致力于迁移到脚本化管道。 但是这样做，我们需要确保为管道实施适当的生命周期，以避免陷入维护困境。