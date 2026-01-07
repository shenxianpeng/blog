---
title: JaCoCo 实现原理 (JaCoCo Implementation Design)
summary: 介绍 JaCoCo 的实现设计，包括覆盖率分析机制、Java 版本要求、字节码操纵、内存使用等方面的内容。
tags:
  - JaCoCo
  - Coverage
  - DevOps
translate: false
date: 2020-11-17
aliases:
  - /2020/11/jacoco/
authors:
  - shenxianpeng
---

想要对 Java 项目进行代码覆盖率的测试，很容易就找到 JaCoCo 这个开源代码覆盖率分析工具是众多工具中最后欢迎的哪一个。

本篇仅仅是在学习 JaCoCo 时对其实现设计文档 https://www.jacoco.org/trunk/doc/implementation.html 的粗略翻译。

## 实现设计(Implementation Design)

这是实现设计决策的一个无序列表，每个主题都试图遵循这样的结构:

* 问题陈述
* 建议的解决方案
* 选择和讨论

### 覆盖率分析机制(Coverage Analysis Mechanism)

> 覆盖率信息必须在运行时收集。为此，JaCoCo 创建原始类定义的插装版本，插装过程发生在加载类期间使用一个叫做 Java agents 动态地完成。

有几种收集覆盖率信息的不同方法。每种方法都有不同的实现技术。下面的图表给出了 JaCoCo 使用的技术的概述:

![实现](implementation.png)

字节码插装非常快，可以用纯 Java 实现，并且可以与每个 Java VM 一起工作。可以将带有 Java 代理钩子的动态插装添加到 JVM 中，而无需对目标应用程序进行任何修改。

Java 代理钩子至少需要 1.5 个 JVMs。用调试信息(行号)编译的类文件允许突出显示源代码。不幸的是，一些 Java 语言结构被编译成字节代码，从而产生意外的突出显示结果，特别是在使用隐式生成的代码时（如缺省构造函数或 finally 语句的控制结构）。



### 覆盖 Agent 隔离(Coverage Agent Isolation)

> Java 代理由应用程序类装入器装入，因此代理的类与应用程序类生活在相同的名称空间中，这可能会导致冲突，特别是与第三方库 ASM。因此，JoCoCo 构建将所有代理类移动到一个唯一的包中。

JaCoCo 构建将包含在 `jacocoagent.jar` 中的所有类重命名为具有 `org.jacoco.agent.rt_<randomid>` 前缀，包括所需的 ASM 库类。标识符是从一个随机数创建的，由于代理不提供任何 API，因此没有人会受到此重命名的影响，这个技巧还允许使用 JaCoCo 验证 JaCoCo 测试。

### 最低的Java版本(Minimal Java Version)

> JaCoCo 需要 Java 1.5 及以上版本。

Java 1.5 VMs 提供了用于动态插装的 Java 代理机制。使用 Java 1.5 语言级别进行编码和测试比使用旧版本更有效、更少出错——而且更有趣。JaCoCo 仍然允许运行针对这些编译的 Java 代码。

### 字节码操纵(Byte Code Manipulation)

> 插装需要修改和生成 Java 字节码的机制。JaCoCo 在内部使用 ASM 库来实现这个目的。

实现 Java 字节码规范将是一项广泛且容易出错的任务。因此，应该使用现有的库。ASM库是轻量级的，易于使用，在内存和 CPU 使用方面非常高效，它被积极地维护并包含为一个巨大的回归测试套件，它的简化 BSD 许可证得到了 Eclipse 基金会的批准，可以与 EPL 产品一起使用。

### Java类的身份(Java Class Identity)

> 在运行时加载的每个类都需要一个唯一的标识来关联覆盖率数据，JaCoCo 通过原始类定义的 CRC64 哈希代码创建这样的标识。

在多类加载器环境中，类的纯名称不能明确地标识类。例如，OSGi 允许在相同的虚拟机中加载相同类的不同版本。在复杂的部署场景中，测试目标的实际版本可能与当前开发版本不同。代码覆盖率报告应该保证所呈现的数字是从有效的测试目标中提取出来的。类定义的散列代码允许区分类和类的版本。CRC64 哈希计算简单而快速，结果得到一个小的64位标识符。

类加载器可能加载相同的类定义，这将导致 Java 运行时系统产生不同的类。对于覆盖率分析来说，这种区别应该是不相关的。类定义可能会被其他基于插装的技术(例如 AspectJ)改变。在这种情况下，哈希码将改变，标识将丢失。另一方面，基于被改变的类的代码覆盖率分析将会产生意想不到的结果。CRC64 代码可能会产生所谓的冲突，即为两个不同的类创建相同的哈希代码。尽管 CRC64 在密码学上并不强，而且很容易计算碰撞示例，但对于常规类文件，碰撞概率非常低。

### 覆盖运行时依赖(Coverage Runtime Dependency)

> 插装代码通常依赖于负责收集和存储执行数据的覆盖运行时。JaCoCo 只在生成的插装代码中使用 JRE 类型。

在使用自己的类加载机制的框架中，使运行时库对所有插装类可用可能是一项痛苦或不可能完成的任务。自 Java 1.6 `java.lang.instrument.Instrumentation`。插装有一个扩展引导带加载器的API。因为我们的最低目标是 Java 1.5，所以 JaCoCo 只通过官方的 JRE API 类型来解耦插装类和覆盖运行时。插装的类通过 `Object.equals(Object)` 方法与运行时通信。插装类可以使用以下代码检索其探测数组实例。注意，只使用 JRE APIs:

```java
Object access = ...                          // Retrieve instance

Object[] args = new Object[3];
args[0] = Long.valueOf(8060044182221863588); // class id
args[1] = "com/example/MyClass";             // class name
args[2] = Integer.valueOf(24);               // probe count

access.equals(args);

boolean[] probes = (boolean[]) args[0];
```

最棘手的部分发生在第 1 行，上面的代码片段中没有显示必须获得通过 equals() 方法提供对覆盖运行时访问的对象实例。到目前为止，已经实施和测试了不同的方法:

* `SystemPropertiesRuntime`: 这种方法将对象实例存储在系统属性下。这个解决方案打破了系统属性必须只包含 `java.lang.String` 的约定。字符串值，因此会在依赖于此定义的应用程序(如Ant)中造成麻烦。
* `LoggerRuntime`: 这里我们使用共享的 `java.util.logging.Logger`。并通过日志参数数组而不是 equals() 方法进行通信。覆盖运行时注册一个自定义处理程序来接收参数数组。这种方法可能会破坏安装自己日志管理器的环境(例如Glassfish)。
* `ModifiedSystemClassRuntime`: 这种方法通过插装将公共静态字段添加到现有的 JRE 类中。与上面的其他方法不同，此方法仅适用于活动 Java 代理的环境。
* `InjectedClassRuntime`：这个方法使用 Java 9 中引入的 `java.lang.invoke.MethodHandles.Lookup.defineClass` 定义了一个新类。

从 0.8.3 版本开始，在 JRE 9 或更高版本上运行时，JaCoCo Java 代理实现使用 `InjectedClassRuntime` 在引导类装入器中定义新类，否则使用`ModifiedSystemClassRuntime` 向现有 JRE 类添加字段。从版本 0.8.0 开始，字段被添加到类 `java.lang.UnknownError` 中。version 0.5.0 - 0.7.9 向类 `java.util.UUID` 中添加了字段，与其他代理发生冲突的可能性较大。

### 内存使用(Memory Usage)

> 对于具有数千类或数十万行代码的大型项目，覆盖率分析应该是可能的。为了允许合理的内存使用，覆盖率分析是基于流模式和“深度优先”遍历的。

一个庞大的覆盖率报告的完整数据树太大了，无法适合合理的堆内存配置。因此，覆盖率分析和报告生成被实现为“深度优先”遍历。也就是说，在任何时间点，工作记忆中只需要保存以下数据:

* 当前正在处理的单个类。
* 这个类的所有父类(包、组)的汇总信息。

### Java元素标识符(Java Element Identifiers)

> Java 语言和 Java VM 对Java 元素使用不同的字符串表示格式。例如，Java 中的类型引用读起来像 `java.lang.Object`。对象，VM 引用的类型与 `Ljava/lang/Object` 相同。JaCoCo API 仅基于VM标识符。

直接使用 VM 标识符不会在运行时造成任何转换开销。有几种基于 Java VM 的编程语言可能使用不同的符号。因此，特定的转换应该只在用户界面级别发生，例如在报表生成期间。

### JaCoCo实现的模块化(Modularization of the JaCoCo implementation)

> JaCoCo 是在提供不同功能的几个模块中实现的。这些模块是作为带有适当清单文件的 OSGi 包提供的。但是它不依赖于 OSGi 本身。

使用 OSGi bundle 允许在开发时和运行时在 OSGi 容器中定义良好的依赖关系。由于对 OSGi 没有依赖关系，捆绑包也可以像普通的 JAR 文件一样使用。
