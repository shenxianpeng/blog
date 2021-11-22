---
title: 使用 JMeter 做性能测试
tags:
  - Performance
  - JMeter
  - Jenkins
categories:
  - Automation
date: 2020-05-23 15:43:16
author: shenxianpeng
---

## 什么是性能测试

性能测试是一种软件测试，它可以确保应用程序在工作负载下运行良好。性能测试的目标不是发现缺陷，而是消除性能瓶颈。

### 性能测试的属性包括

* 速度 —— 它决定应用程序是否快速响应
* 可伸缩性 —— 它决定了软件应用程序能够处理的最大用户负载
* 稳定性 —— 它决定应用程序在变化负载下是否稳定

### 性能测试的类型

* 负载测试 —— 它检查应用程序在预期的用户负载下的执行能力。目的是在软件应用程序上线之前确定性能瓶颈
* 压力测试 —— 涉及在极端工作负载下测试应用程序，以查看其如何处理高流量或数据处理。目的是确定应用程序的断点
* 耐用性测试 —— 这样做是为了确保软件可以长时间处理预期的负载
* 峰值测试 —— 可以测试软件对用户产生的突然突然的峰值负载的反应
* 体积测试–在“体积测试”下，没有。的。数据被填充到数据库中，并且监视整个软件系统的行为。目的是检查在不同数据库容量下软件应用程序的性能
* 可伸缩性测试 —— 可伸缩性测试的目的是确定软件应用程序进行扩展以支持用户负载增加的有效性。它有助于计划软件系统的容量增加。

## Apache JMeter

性能测试工具也很多，比如 LoadNinja, WebLOAD, LoadUI Pro, LoadRunner 等等。今天介绍的这款是我觉得用过且觉得很好用的 Apache JMeter。

他是一块开源软件，一个 100% 纯 Java 应用程序，旨在加载测试功能行为和衡量性能。它最初是为测试 Web 应用程序而设计的，但此后已扩展到其他测试功能。

### JMeter 能做什么

Apache JMeter 可用于测试静态和动态资源，Web 动态应用程序的性能。
它可用于模拟服务器，服务器组，网络或对象上的重负载，以测试其强度或分析不同负载类型下的整体性能。

JMeter 的功能包括：

* 能够加载和性能测试许多不同的应用程序/服务器/协议类型

  * Web - HTTP, HTTPS (Java, NodeJS, PHP, ASP.NET, …)
  * SOAP / REST Webservices
  * FTP
  * Database via JDBC
  * LDAP
  * Message-oriented middleware (MOM) via JMS
  * Mail - SMTP(S), POP3(S) and IMAP(S)
  * Native commands or shell scripts
  * TCP
  * Java Objects

* 功能齐全的Test IDE，允许快速记录测试计划（来自浏览器或本机应用程序），构建和调试

* CLI 模式（命令行模式（以前称为Non GUI）/无头模式）可从任何 Java 兼容的操作系统（Linux，Windows，Mac OSX等）加载测试

* 完整且随时可以呈现的动态 HTML 报告

* 通过从大多数流行的响应格式，HTML，JSON，XML 或任何文本格式中提取数据的能力，轻松实现关联

* 完整的多线程框架允许通过多个线程进行并发采样，并通过单独的线程组同时对不同的函数进行采样

* 缓存和脱机分析/重放测试结果

* 高度可扩展的核心

  * 可插拔采样器允许无限的测试功能
  * 可脚本化的采样器（与 Groovy 和 BeanShel l等 JSR223 兼容的语言）
  * 可以使用可插入计时器选择几个负载统计信息
  * 数据分析和可视化插件可实现出色的可扩展性和个性化
  * 函数可用于为测试提供动态输入或提供数据处理
  * 通过针对 Maven，Gradle 和 Jenkins 的第三方开源库轻松进行持续集成

### Apache JMeter HTTP(S) 测试脚本记录器

对于 JMeter 的新手来说，创建测试计划的一种简单方法是使用 Recorder 。

#### 基本介绍

1. 运行 Jmeter。去到 `JMETER_HOME/bin` 目录下，在 Windows 执行 `jmeterw.bat` 这个 batch 文件，在 Linux/Unix 上执行 `jmeter.sh` 这个 shell 文件。
2. 选择菜单栏选择 `Templates…`

  ![](apache-jmeter/Select-Templates-Icon.png)
