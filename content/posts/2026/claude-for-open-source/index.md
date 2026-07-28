---
title: 申请通过了，Anthropic 免费送了我 6 个月 Claude Max
summary: |
    申请 Anthropic 开源开发者计划通过了，拿到了 6 个月 Claude Max 20x 的免费使用权。聊聊申请条件、为什么能通过，以及这些年维护开源项目的一些感受。
tags:
  - Open Source
  - Claude
  - AI
authors:
  - shenxianpeng
translate: false
date: 2026-07-28
---

前几天申请的 **Anthropic 开源开发者计划（Claude for Open Source）**，今天终于收到了通过邮件。

看到邮件的时候，还是挺开心的。

这次获得的是 **6 个月 Claude Max 20x** 的免费使用权。

如果自己订阅的话，官方价格是 **200 美元/月**，6 个月下来大约价值 1200 美元。对于经常写代码、维护开源项目的人来说，这份支持还是挺有诚意的。

首先也感谢 Anthropic 推出这样的计划，去支持那些持续为开源社区做贡献的开发者。

毕竟，大多数开源维护者都不是全职做开源，而是在工作之余利用自己的时间，一点一点把项目维护起来。

---

## 谁可以申请？

如果你也是开源项目维护者，其实也可以去试试看。

官方列出的申请条件主要包括：（以下是我简单整理后的版本）

* **维护者和库作者**：你维护的软件包被大量项目依赖，例如有 500 个以上依赖仓库、100 个以上依赖软件包，或者在 npm、PyPI、crates.io、RubyGems 等平台月下载量达到 200,000 次以上。
* **核心贡献者**：你是知名基金会或语言项目的维护者，例如 CPython、Rust、Node.js、Apache、CNCF、Kubernetes、Linux 内核等项目贡献者。
* **活跃贡献者**：过去 12 个月向非自己拥有的仓库提交过 100 个以上合并请求。
* **社区建设者**：过去 12 个月，你维护的项目有至少 20 位不同的外部贡献者提交过合并请求。
* **关键基础设施维护者**：维护的项目 OpenSSF 关键性评分达到 0.4 或以上。

具体条件可以查看 [Anthropic 官方页面](https://claude.com/contact-sales/claude-for-oss)。

如果你也是开源维护者，后面几个条件相对来说更容易达到。如果觉得自己符合要求，可以去申请试试。

另外，我从申请条款里还发现几条有用的信息，一并分享给你：

**名额有限，先到先得**

项目总共只有 **10,000 个名额**，采用滚动审核机制，满员即止。所以如果你符合条件，建议尽早申请，不要拖延。

**还有一条「生态系统影响」通道**

如果你不符合前面那些量化指标（500 依赖、20 万月下载等），别急着放弃。还有一个 **Ecosystem Impact Track（生态系统影响通道）**：只要你维护的项目是广泛使用的底层依赖、基础工具或基础设施库，可以通过书面说明的方式申请，由 Anthropic 综合评估。这对很多非头部但很重要的项目维护者来说，是额外的机会。

**基础资格要求也需要注意**

此外还有一些基础门槛：必须是**自然人**（不能以公司身份申请）、年满 18 岁、GitHub 账号需 **至少 2 年**且状态良好、申请前 **90 天内有公开贡献活动**、项目使用 **OSI 批准的开源许可证**（MIT、Apache 2.0、GPL 等）。

**申请时需要提交什么？**

流程也比较简单：用 GitHub 登录，填写邮箱，简述你的使用计划，再写一段 **不超过 500 字的说明**解释为什么符合条件就行。

对了，虽然这 6 个月基础订阅免费，但**超额使用 Claude Max 20x 的额度**会产生费用，使用时稍加留意。

**关于激活时间的一个提醒**

如果你和我一样是通过 **iOS（App Store）订阅**的 Claude Pro，需要等到当前订阅周期结束后才能激活。因为 iOS 走的是苹果内购，Anthropic 侧无法暂停你的订阅。

但如果你是 **Web 订阅**的用户，操作就灵活多了：激活后现有订阅会自动暂停，等 6 个月免费期结束后再恢复，无需手动处理。

无论哪种方式，激活链接的有效期都是 **90 天**，过期作废。所以收到邮件后，记得在这个时间内完成激活。

---

## 我怎么申请成功？

这次我是使用自己维护的 **cpp-linter** 项目进行申请的。

这个项目已经维护了 4 年多。

从最开始的个人项目，到后来逐渐有人使用、提交 Issue、贡献 PR，再发展成现在的组织项目。

虽然 Star 数量不算特别多，但项目已经被大量开源项目使用，依赖数量也达到数千规模，其中包括微软、Apache 等知名开源项目。

除此之外，我还提交了自己的 GitHub 主页，介绍了其他开源贡献情况。

可能这些因素也帮助申请更容易通过。

---

## 开源其实就是「用爱发电」

很多人都说，开源就是「用爱发电」，这句话其实没有错。

维护一个开源项目，需要持续投入时间：

写代码、修 Bug、Review PR、回复 Issue、更新文档……

很多时候，一个周末可能就在处理社区反馈中度过了。

这些投入，其实远远超过任何一份福利能够补偿的。

但是，偶尔收到来自社区或者公司的认可时，还是会觉得挺开心。

它不能让你因此发财，也不足以覆盖这些年的投入。

但它会让你感觉，自己的努力确实被一些人看到了。

这就挺好的。

---

## OpenAI 那边还在等待消息

除了 Anthropic，其实我更早申请的是 OpenAI 面向开源开发者的免费计划，同样也是 6 个月。

不过截至目前还没有收到任何回复。

可能希望不大了（笑）。

---

## 最后，也顺便推荐一下我的开源项目

这次能够申请成功，主要还是因为这些年一直在维护自己的开源项目。

如果你平时也从事 CI/CD、代码质量、DevOps 工作流相关工作，下面这些项目或许能帮到你：

* [cpp-linter](https://github.com/cpp-linter/cpp-linter)：C/C++ 代码格式化和静态检查工具，提供 GitHub Action、Python 包以及 Jenkins Plugin。
* [commit-check](https://github.com/commit-check/commit-check)：自动检查 Git 提交信息、分支命名、提交用户名和邮箱、force push 等各种提交规范。
* [conventional-branch](https://github.com/conventional-branch/conventional-branch)：关于 Git 分支命名规范的工具，帮助团队统一分支管理方式。
* [devops-maturity](https://github.com/devops-maturity/devops-maturity)：DevOps 成熟度评估工具，帮助组织和团队评估 DevOps 实践成熟度。
* [open-delivery-spec](https://github.com/open-delivery-spec/open-delivery-spec)：开源交付规范，提供 CLI 工具和 GitHub Action，帮助团队在 AI 驱动开发时代实现更高效、更安全的软件交付。
* [gitstats](https://github.com/shenxianpeng/gitstats)：生成 Git 仓库统计报告，帮助团队了解代码贡献、提交历史以及项目演进情况。

除了维护自己的项目，我也持续参与一些开源社区贡献。

目前我是 PyPA（Python Packaging Authority） 的志愿者，参与 Python 官方生态相关工作；同时也是 Jenkins 社区的 Committer，创建并维护了 [explain-error-plugin](https://github.com/jenkinsci/explain-error-plugin) 和 [jenkinsfilelint](https://github.com/jenkinsci/jenkinsfilelint) 等项目。

这些项目并不一定适合所有人，但如果你刚好在解决类似的问题，欢迎去 GitHub 看看。

如果它们曾经帮到你，欢迎点一个 Star，或者分享给身边可能需要的人。

对于开源维护者来说，一个 Star、一条 Issue、一份 PR，甚至一句「这个项目帮到我了」，都是继续坚持下去的动力。