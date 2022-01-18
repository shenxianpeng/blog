---
title: 我终于开始使用 Go 语言来开发了
tags:
  - Go
  - CLI
categories:
  - Go
date: 2022-01-18 22:01:31
author: shenxianpeng
---

我作为 Go 语言的初学者来分享一下我对学习 Go 语言的一些心得和体会，请轻拍。

## 为什么要使用 Go 语言

随着越来越多的云原生的重量级应用，比如 Kubernetes，Prometheus，Docker，Contained 等等都是用 Go 语言来开发的。

作为这些工具的使用者，掌握 Go 语言能够帮助我在今后更好的学习这些产品，理解它们背后的工作原理，甚至是参与到这些产品的社区建设中。

另外就是最近我有一个工作就是需要写一个 CLI 工具，使用 Go 语言开发 CLI 有天然的优势（后面我会提到），因此我决定一定要好好学习 Go 了。

## Go 语言的排名

Go 语言在国内可谓是知名度非常高了，经常和 Java，Python 一起被提及。那我们看看目前 Go 语言是怎样的排名？

![Go语言排名](get-started-with-go/tiobe-index-go.png)

这是知名的编程语言排名网站 TIOBE 2022 一月的前 20 名数据，我们看到 Go 语言位于这个排行榜的第 13 位，相比于去年上升了一位。

相比于排在榜单前五的 Python，C，Java，C++，C# 应该还有不少的时间要走。

从我所在的公司和身边的同事所使用的编程语言来看，大多数人都是 C/C++，Java 和 C# 的开发人员，因此 Go 语言的这个排名我认为还是比较合理的。

## Go 语言有那些优势

* 构建后的可执行文件不需要依赖，可以随处运行
* Go 的上手比较容易（比Python难一些）
* Go 在上手后开发效率很高；
* Go 开发的软件性能好，并发效率高
* Go 语言有内置 go fmt，go test，go build，go install 等功能
* 越来越多的 CLI 工具都是使用 Go 来开发的，比如 GitHub CLI，Jfrog CLI 等等。

## 如何学习 Go 语言

我最早是在 2010~2020 期间看过 Go 语言的视频教程，中文英文的都看过，但由于没怎么动手写过，我那时还处在“知道”阶段。

这里我想强调的是学习编程语言，看多少教程不是那么重要，最最重要的是立刻动手尝试！！！否则一定会是：“一看就会，一写就废”。这对于学些任何一门技术都是通用的道理。

## 选择一个 Go CLI 框架

Go 语言内置的 Flag 这个 package 可以用来编写 CLI 命令，我也看了很多使用 Go 开发的 CLI 项目后，注意到这些项目都没有使用内置的 Flag 包，而是绝大多数使用了 [spf13/cobra](https://github.com/spf13/cobra) 或 [urfave/cli](https://github.com/urfave/cli)。

这是使用 cobra 的项目[列表](https://github.com/spf13/cobra/blob/master/projects_using_cobra.md)，其中包括了著名的项目比如 Kubernetes, Hugo, Github CLI 等都使用的 cobra。

至于 urfave/cli，我看到 Jfrog CLI 在使用它，其他正在使用 urfave/cli 的知名项目我并没有看到像 cobra 那样的列表。

因此基于少数服从多数的原则，我就迅速选择了 cobra 开始开发了。

目前我认为这个框架还是非常优秀的，通过参考其他 CLI 的项目，我也学到了很多其他的优秀的轮子。比如：

* github.com/AlecAivazis/survey/v2 - 支持终端上构建交互式和可访问提示的库
* github.com/enescakir/emoji - 表情符号库，支持在终端输出表情符号
* github.com/mgutz/ansi - 可以创建 ANSI 彩色字符串

另外我觉得学习 CLI 的开发最好找一个你很熟悉的项目，如果你熟悉 GitHub 的使用，那 [GitHub CLI]( https://github.com/cli/cli) 项目就很推荐用来学习。看看优秀的项目是怎么写的，有助于我们将来也能写出优秀的代码。

## 最后

以上就是我的一点点作为初学者的分享，希望对你有所帮助。
