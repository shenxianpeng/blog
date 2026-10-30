---
title: "关于"
date: 2022-06-13T20:55:37+01:00
draft: false

showDate : false
showDateOnlyInArticle : false
showDateUpdated : false
showHeadingAnchors : false
showPagination : false
showRelatedContent : false
showReadingTime : false
showTableOfContents : false
showTaxonomies : false
showWordCount : false
showSummary : false
sharingLinks : false
showEdit: false
showViews: false
showLikes: false
showAuthor: true
layoutBackgroundHeaderSpace: false
---

开源维护者，也做产品，生活在立陶宛维尔纽斯。这里的东西都围绕一件事：软件怎么构建、测试、发布。

## 开源

- [cpp-linter](https://github.com/cpp-linter)：每个 PR 上跑 clang-format 和 clang-tidy。GitHub 上有 1000 多个仓库依赖它，包括 Apache、Samsung、Qualcomm、Bloomberg 的项目。所用的工具来自我维护的[静态二进制](https://github.com/cpp-linter/clang-tools-static-binaries)，每个 LLVM 版本一个发布，累计下载超过 75 万次。
- [commit-check](https://github.com/commit-check/commit-check)：一份策略统一校验提交信息、分支名和 AI 署名，CI 里或 pre-commit 里都能跑。
- [Conventional Branch](https://conventionalbranch.org)：分支命名规范。
- jenkinsci 组织下的 [explain-error-plugin](https://github.com/jenkinsci/explain-error-plugin) 和 [jenkinsfilelint](https://github.com/jenkinsci/jenkinsfilelint)：用 AI 解释构建失败，以及不用 Jenkins 服务器也能校验 Jenkinsfile。
- [release-ledger](https://github.com/keelinfra/release-ledger)，我最新的项目：发布 release 时自动附上 SBOM 和签名的构建溯源，并持续检查仍在支持期内的版本有没有被在野利用的漏洞。欧盟《网络弹性法案》要求这类漏洞在 24 小时内上报。

## 产品

- [keelinfra](https://keelinfra.io)：[Agent8](https://github.com/keelinfra/agent8)，让只有 Java 8 的构建机（AIX、Solaris、HP-UX）继续接入新版 Jenkins。
- [keelapps](https://keelapps.app)：Jira 与 Confluence Cloud 的管理工具。
- [Keelhaven](https://keelhaven.app)：把 Mac 备份到你自己的存储，免费。

每一个的细节都在[作品](/zh-cn/portfolio/)页。

## 社区

Jenkins GitHub 组织成员，按公开贡献在 [committers.top](https://committers.top/lithuania_public) 立陶宛榜上排前三，EuroPython 2025 议题评审，2026 年入选 Anthropic Open Source Developer Program。博客从 2017 年写到现在，中文版同步发在公众号「沈显鹏」。

## 支持我

博客一直没有广告。工具帮到了你的话，可以在 [GitHub Sponsors](https://github.com/sponsors/shenxianpeng) 说声谢谢。

## 联系我

工具用起来有问题，或者想聊聊：[xianpeng.shen@gmail.com](mailto:xianpeng.shen@gmail.com)，或在 [GitHub](https://github.com/shenxianpeng)、[X](https://x.com/xianpengshen) 上找我。2009 年入行，构建、测试、发布这一段的活都干过，细节在[简历](/zh-cn/resume/)。
