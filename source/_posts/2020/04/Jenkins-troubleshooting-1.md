---
title: 三种方法解决 Jenkins 声明式流水线 Exception Method code too large !
tags:
  - Pipeline
  - Troubleshooting
categories:
  - Jenkins
date: 2020-04-20 21:33:09
author: shenxianpeng
---

这是我第二次在使用 Jenkins 声明式流水线的时候遇到了这个问题，第一次遇到这个问题的时候是在一个 Pipeline 里大概写到 600 多行时候遇到如下错误

```java
org.codehaus.groovy.control.MultipleCompilationErrorsException: startup failed:
General error during class generation: Method code too large!

java.lang.RuntimeException: Method code too large!
	at groovyjarjarasm.asm.MethodWriter.a(Unknown Source)
	[...]
```

<!-- more -->

当时我也使用了 Jenkins Shared Libraries，但那时候的代码组织的并不是很好，有不少步骤还没来得及单独抽离出来作为单独的方法。为了解决这个问题，经过一番重构，我将原来的 600 多行的 Pipeline 变成了现在的 300 多行，很不巧，随着继续添加功能，最近又遇到了这个问题。

出现这个问题的原因是 Jenkins 将整个声明性管道放入单个方法中，并且在一定大小下，JVM 因 java.lang .RuntimeException 失败：方法代码太大！看来我还是有什么方法超过了 64k。

Jenkins JIRA 上已经有了该问题的单子，但目前为止还是尚未解决。针对这个问题目前有三种方案，但他们都有各自的利弊。

## 方法1：将步骤放到管道外的方法中

自2017年中以来，你可以在管道的末尾声明一个方法，然后在声明性管道中调用它即可。 这样，我们可以达到与共享库相同的效果，但是避免了维护开销。

```pipeline
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                whateverFunction()
            }
        }
    }
}

void whateverFunction() {
    sh 'ls /'
}
```

| 优点 | 缺点 |
|---|---|
| 没有额外的维护费用 | 这个解决方案不知道会不会一直有效 |
| 所有的功能都反映在Jenkinsfile中 | 有的方法在多个Jenkinsfile里用到时，这种方法还是会写很多重复的代码 |

## 方法2：从声明式迁移到脚本式管道

最后，我们可以迁移到脚本化的管道。有了它，我们就有了所有的自由。但是也就会失去我们最初决定使用声明式管道的原因。有了专用的DSL，就很容易理解管道是如何工作的

| 优点 | 缺点 |
|---|---|
| 完全没有限制 | 需要比较大的重构 |
|  | 更容易出错 |
|  | 可能需要更多的代码来实现相同的功能 |

## 方法3：使用 Shared Libraries

我当前使用的就是 Jenkins Shared Libraries，有一个共享库来执行一些复杂的步骤。共享库目前看来使用的非常广泛，尤其是在维护一些比较大型的、复杂的项目里用的很多。

最终我的解决办法是进一步缩减 Pipeline 里的代码，这里我也用到 方法1 的解决方案，将一些步骤提到 Pipeline {} 括号的外面，尤其是那些重复调用的​步骤。​

| 优点 | 缺点 |
|---|---|
| 减少了大量重复的代码 | 任何一个修改都会影响到所有的引用，要测试好了再将变更放到引用分支里 |
| 可以分块使用 | 不熟悉的话很难理解一个步骤到底是做什么的 |  
| 生成的Jenkinsfile将易于阅读 |  |  

## 结论

方法1：对于单一的 Repository 的集成，可以快速实现，大多数人上手会很快。
方法2：脚本化提供了很少的限制，适合熟悉 Java，Groovy 的高级用户和有更复杂需求的人使用。
方法3：对于企业级项目，拥有很多 Repositories，需要进行大量集成，并且想了解共享库，推荐使用此方法。
