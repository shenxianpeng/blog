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

发布工程师，生活在立陶宛维尔纽斯。我做开源工具，帮团队把软件稳稳发出去，上游不管了也一样。

2009 年入行，我一直在做构建、测试和发布。AI 让写代码变便宜了，代码写完之后的事一样没便宜：这次改动是谁、或者哪个 agent 提交的，在你手上那些机器上还能不能构建，发出去的版本说不说得清来历，往后几年出了漏洞谁来补。从 2027 年 12 月起，欧盟《网络弹性法案》把其中一部分写成了法律义务：在欧盟卖软件的厂商要声明支持期，并在支持期内持续提供安全更新。下面这些项目做的就是这一段。

## 从提交到发布，再到发布之后

{{< pipeline >}}

- **commit**　[commit-check](https://github.com/commit-check/commit-check)：一份策略统一校验提交信息、分支名和 AI 署名，CI 里或 pre-commit 里都能跑。[Conventional Branch](https://conventionalbranch.org)：分支命名规范。
- **review**　[cpp-linter](https://github.com/cpp-linter)：每个 PR 上跑 clang-format 和 clang-tidy。GitHub 上有 1000 多个仓库依赖它，包括 AWS、Apache、Samsung、Qualcomm、Bloomberg 的项目。
- **build**　jenkinsci 组织下的 [explain-error-plugin](https://github.com/jenkinsci/explain-error-plugin) 和 [jenkinsfilelint](https://github.com/jenkinsci/jenkinsfilelint)：用 AI 解释构建失败，以及不用 Jenkins 服务器也能校验 Jenkinsfile。[Agent8](https://github.com/keelinfra/agent8) 让只有 Java 8 的构建机（AIX、Solaris、HP-UX）继续接入新版 Jenkins。
- **release**　[release-ledger](https://github.com/keelinfra/release-ledger)，我最新的项目：发布 release 时自动附上 SBOM 和签名的构建溯源，并持续检查仍在支持期内的版本有没有被在野利用的漏洞。欧盟《网络弹性法案》要求这类漏洞在 24 小时内上报。我给每个 LLVM 版本发布的 clang-format、clang-tidy [静态二进制](https://github.com/cpp-linter/clang-tools-static-binaries)，累计下载超过 75 万次。
- **support**　[Extended Security for Jenkins 2.541.x](https://github.com/keelinfra/jenkins-extended-security)：Jenkins 2.541.3 是最后一个能跑在 Java 17 上的 LTS，这个项目把之后发布的核心安全修复补回去。[MkDocs NG](https://mkdocs-ng.org)：持续维护的 MkDocs 1.x，已有站点和插件照常构建，1.x 支持到 2028 年底。

## 产品

两个产品面向同一群人：在公司里维护研发工具的团队。

- [keelinfra](https://keelinfra.io)：给暂时跟不上上游的 CI 用。Agent8、Extended Security for Jenkins 等都免费开源，测试过程公开，需要有人兜底时可以买支持。
- [keelapps](https://keelapps.app)：Jira 与 Confluence Cloud 的管理工具。

业余还做了 [Keelhaven](https://keelhaven.app)，一个免费的 Mac 备份应用，把数据备份到你自己的存储。

每一个的细节都在[作品](/zh-cn/portfolio/)页。

## 社区

Jenkins GitHub 组织成员，按公开贡献在 [committers.top](https://committers.top/lithuania_public) 立陶宛榜上排前三，EuroPython 2025 议题评审，2026 年入选 Anthropic Open Source Developer Program。博客从 2017 年写到现在，中文版同步发在公众号「沈显鹏」。

## 支持我

博客一直没有广告。文章或工具帮到了你的话，可以在 [GitHub Sponsors](https://github.com/sponsors/shenxianpeng) 赞助，通过 [Thanks.dev](https://thanks.dev/u/gh/shenxianpeng) 支持，或[请我喝杯咖啡](https://buymeacoffee.com/shenxianpeng)。

## 联系我

工具用起来有问题，或者想聊聊：[xianpeng.shen@gmail.com](mailto:xianpeng.shen@gmail.com)，或在 [GitHub](https://github.com/shenxianpeng)、[X](https://x.com/xianpengshen) 上找我。完整的工作经历在[简历](/zh-cn/resume/)。
