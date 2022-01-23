---
title: 什么是 Go ？Go 有哪些优势，Go 的现状，以及初学者如何选择和学习
tags:
  - Go
  - CLI
categories:
  - Go
date: 2022-01-18 22:01:31
author: shenxianpeng
---

## Go 还是 Golang

问你一个问题：Google 的这门开源编程语言是叫 Golang 还是 Go？还是两个都行？给你三秒钟想一下 ...

Google 说：它叫 Go。之所以有人称它为 Golang 是由于之前的 Go 语言官网是 golang.org（因为 go.org 已经被别人用了），因此有人将 Golang 和 Go 混用了。

现在输入 golang.org 会直接跳转到 go.dev 这个网址，这也算是彻底个自己家孩儿正个名。

## Go 语言有那些优势

官网是这样介绍 Go 语言的：

* Go 适合大规模快速构建，可靠、高效的软件
* Go 是 Google 在背后支持的一门开源编程语言
* 易于学习和入门
* 内置并发和强大的标准库
* 不断发展的合作伙伴、社区和工具生态系统

今天，Go 被用于各种应用程序：

* Go 在基于云或服务器端的应用程序中很受欢迎
* 云基础设施方面。当今最流行的基础设施工具是用 Go 编写的，例如 Kubernetes、Docker 和 Prometheus
* 许多命令行工具都是用 Go 编写的
* DevOps 和 Web 可靠性自动化也常常用 Go 来写
* Go 也被用于人工智能和数据科学领域
* 微控制器编程、机器人技术和游戏中使用也会使用 Go

这也就是为什么 Go 越来越流行。

正是因为这些优势以及在工作上的需要写一个 CLI，我就入门 Go 语言了。

## Go 语言的排名

Go 语言在国内热度可谓是非常高了，我们来看看 Go 语言目前最新的排名怎么样。

<!-- more -->

![Go语言排名](get-started-with-go/tiobe-index-go.png)

这是 TIOBE 2022 年一月排名前 20 编程语言，可以看到 Go 语言位于这个排行榜的第 13 位，相比于去年上升了一位。

对比排在榜单前五的 Python，C，Java，C++，C#，你觉得 Go 能否追上它们呢？

从我身边非云厂商的公司和同事来看，目前大多数都是 C/C++，Java，C#，Python 的开发人员，所以这个排名我认为还是挺符合预期的。

## 初学者应该是学习 Python 还是 Go ？

Python 已有 30 多年的历史，但它的受欢迎程度仍在继续增长。Python 是一门出色的面向对象语言，你也可以使用函数式编程风格来编写代码。在所有编程语言中，你可能找不到一种比 Python 被更多非程序员使用的语言。

* 它的灵活性是 Python 如此受欢迎的原因之一
* 它经常用于编写脚本，Web 开发、数据科学、以及面向孩子们教授编程、制作动画等等。

那么 Go 与 Python 相比如何呢？

* Python 和 Go 都具有简单的语法
* Python 和 Go 对于初学者来说都很容易上手，且相对容易学习（Python 相对更容易）
* Python 往往在数据科学领域占据主导地位；Go 非常适合系统编程
* 程序的执行速度 Go 比 Python 快多了
* 作为高级语言，Python 拥有更广泛的库和围绕它建立的社区
* Go 是处理大型并发应用程序的理想选择、支持并发，同时运行多个程序/任务的能力。Python 没有。

今天 Python 和 Go 都是目前最流行和最方便使用的两种编程语言。对于初学者应该是学习 Python 还是 Go ？

* 如果你是零基础，建议先学习 Python。相比于 Go，Python 还是更容易学习。
* 如果你是测试工程师，想学习一门编程语言，建议学习 Python。因此绝大多数的自动化测试岗位要求是掌握 Python。
* 如果你是软件开发、DevOps 工程师，最好两门都要会。"小孩子才做选择，大人全都要。"

## 如何学习 Go 语言

* 看文档或视频，最最重要的是要动手！！

  我最早是在 2010~2020 期间看过 Go 语言的视频教程，但由于没怎么动手写过，一直处在“知道”阶段。

  对于新手学习任何一门编程语言，看教程大概只能学会 30%，想要真正的学会必须亲自上手实践，否则一定会是：“一看就会，一写就废”。

* 确定要一个方向，立刻开始 Coding。

  我的方向就是写一个 CLI 工具。尽管 Go 语言内置的 Flag 这个 package 可以用来编写 CLI 命令，我也看了很多使用 Go 开发的 CLI 项目后，注意到这些项目都没有使用内置的 Flag 包，而是绝大多数使用了 [spf13/cobra](https://github.com/spf13/cobra) 或 [urfave/cli](https://github.com/urfave/cli)。

  * 这是使用 cobra 的项目[列表](https://github.com/spf13/cobra/blob/master/projects_using_cobra.md)，其中包括了著名的项目比如 Kubernetes, Hugo, Docker，Github CLI 等都使用的 cobra。
  * 至于 urfave/cli，我看到 Jfrog CLI 在使用它，其他正在使用 urfave/cli 的知名项目我并没有看到像 cobra 那样的列表。

  对于我这样的初学者，最重要的是马上开始，因此在选择的框架的时候不需要花费太多时间，cobra 有那么多优秀的项目背书，跟着用就行，最重要的是尽快动手。在编码的过程中，选择同样使用该框架的顶级项目做参考，这能帮助我们通过阅读别人的代码也让我们自己写出更优秀的代码。千万不要去 Ctrl + C 然后 Ctrl + V。

* 最后，再分享几个在开发 CLI 时一切其他的优秀项目。比如：

  * github.com/AlecAivazis/survey/v2 - 支持终端上构建交互式和可访问提示的库
  * github.com/enescakir/emoji - 表情符号库，支持在终端输出表情符号
  * github.com/mgutz/ansi - 可以创建 ANSI 彩色字符串

---

以上就是我的一点分享，希望对你有所帮助。
