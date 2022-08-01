---
title: 学历平平的IT从业者如何进阶
tags:
  - OpenSource
categories:
  - Others
author: shenxianpeng
date: 2022-08-01 15:37:08
---

本篇我想谈论一下关于《普通程序员如何进阶》的话题。

之前我看过一个短视频是 TDengine 的创始人 XXX 分享的 二本专业的毕业生如何与清华姚班的毕业生竞争的视频，那就是参与到一个开源项目中来，看完了我很受启发。

结合自己的一点点开源经历，我想谈谈自己的看法。

说来惭愧，我在 2013 年 12 月就注册了 GitHub，期间也在用 GitHub 写了一些测试脚手架，但实际真正的参与到开源中来还是在 2021 年 4 月我 Fork 了一个已经不维护的 GitHub Action 项目做修改并重新发布，然后在同年 8 月，被另外一个外国人也有同样需求的外国人看到了，整体做了重构，支持了更多的功能，这花掉了我很多的业余使时间，但好在与人交流并获得别人的使用让我一直很有收获，并一直维护到了现在。

这个项目叫 [cpp-linter-action](https://github.com/cpp-linter/cpp-linter-action) 是通过 GitHub Action 来对 C/C++ 代码通过 clang-format 和 clang-tidy 进行检查并将检查结果通过注释（annotations）和评论（comments）反馈给用户。

经过这一年的维护，慢慢地已经其他项目在使用了这个项目，其中最著名的有 Google 的 `flatbuffers` (18.4k Star) ，chocolate-doom (1.4k Star) 都使用了 `cpp-linter-action`。

为了更好的维护我把这个项目从我得 GitHub 个人账户移到了 `cpp-linter` 这个 Organization 下面。但与此同时在一段时间内我们失去了比较好的被依赖的增长势头，其中丢掉了 `flatbuffers` 项目的使用记录（这是一个很好的背书）。

为此还创建了项目还包括 `clang-tools`，`clang-tool-pip` 和 `cpp-linter-hooks`

* `clang-tools` 提供了从 `v6` 到最新的 `v14` 所有的 clang-format 和 clang-tidy docker 镜像
* `clang-tool-pip` 通过 `pip` 自动安装 clang-format 和 clang-tidy binaries
* `cpp-linter-hooks` 是一个提供 clang-format 和 clang-tidy 的 hooks，方便用户使用 pre-commit 时可以使用。

GitHub Action 的开发不是什么高科技，但也涉及很多个技术栈，包括 Docker，GitHub Action, clang-format, clang-tidy, Python, Mkdocs 这些。尤其是在与人交流的过程中也学到了很多（我们通常只是通过 issue 来交流）。

目前该项目已经基本稳定了，我也在寻求其他的项目想参与其中，这不但可以学到了很多技术，长远来看对自己的职业生涯是一个非常宝贵的经验。

这个过程中最为困难的还有锁定目标并一直坚持着。还记得 Apache Log4j 出现漏洞时，我注意到我的一个同事他已经是该项目的第一贡献者了，几年前我注意到他在贡献这个项目的时候还只是其中之一的贡献者。

在这种顶级项目中成为贡献者甚至是顶级贡献者是多么让人骄傲的一件事，同时对自己的职业生涯也是非常有帮助的。

希望大家都在做开源这件事情中有所收获。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
