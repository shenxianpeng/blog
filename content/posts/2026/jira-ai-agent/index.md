---
title: 我在 Jira 里搭了一个 AI Agent：一个 Jira 版 Copilot 的实现思路
summary: |
  不少朋友问怎么在 Jira 里做一个类似 GitHub Copilot 的 AI Agent。本文结合我在 Jira 里实际开发的一个类似应用，分享从账号准备、Jira Automation 触发、Webhook 对接，到 Skills 能力体系搭建的完整思路。核心是利用现有服务，低成本快速实现。
tags:
  - AI
  - Jira
  - DevOps
authors:
  - shenxianpeng
date: 2026-05-12
---

大家好，我是沈工。

最近发现很多人问同一个问题：怎么在 Jira 里搞一个类似 GitHub Copilot 那样的 AI Agent？

坦白说，这个话题我本来没打算写——觉得原理不算复杂，懂的人看看文档应该就能上手。但后来被反复问到类似的问题，才觉得可能确实有不少朋友对这块还不太熟悉。

今天刚好结合自己在 Jira 里做过的一个类似应用，分享一下整体的实现思路。

核心原则就一条：**尽可能利用现有的服务，不要从零造轮子**。

下面我按流程一步步说。

### 第一步：准备一个 Bot 账号

首先，你得有一个专门的 Bot。在公司 IT 允许的情况下，建一个名字简单好记的账号，比如就叫 `copilot` 或者 `ai-bot`。

这个账号的作用是什么？它是一个“触发器”。用户在 Jira 的评论区 @ 这个账号时，后续的自动化流程就会被激活。所以名字要尽量简短、输入方便——你肯定不会希望同事每次都要 @ 一个又长又难拼的用户名。

这一步没什么技术含量，但它是整个流程的起点。

### 第二步：设置 Jira Automation

账号准备好之后，下一步是在 Jira 里配置 Automation。Jira 本身自带了 Automation 功能（Jira Automation），不需要额外安装插件。

具体逻辑很简单：

- 监控 Issue 的评论区
- 当检测到有用户 @ 了你指定的那个 User（比如 `copilot`）时，立即触发一个 Webhook

Jira Automation 的规则配置是可视化操作，不需要写代码。你只需要设置触发条件（Comment contains `@copilot`），然后添加一个“Send webhook”动作，指向你后端服务的地址。

这里的关键在于：**Automation 只负责检测和转发，不做任何业务逻辑**。它就像一个门铃——有人按了，信号传出去就行。

### 第三步：用 Webhook 触发后端 Application

Webhook 发出之后，需要一个接收方。我选择的是 Jenkins 的 Jenkins Generic Webhook Trigger Plugin。

为什么用 Jenkins？因为大部分团队本来就有 Jenkins 在跑 CI/CD，它是现成的基础设施，不需要额外部署新的服务。

配置方式：

- 在 Jenkins 里创建一个 Pipeline Job，配置 Generic Webhook 来接收 Jira Automation 发来的请求
- Webhook 被触发后，Pipeline 启动你的后端 Application

> 这里需要注意的是，Webhook 入口要做好安全控制，比如 token、来源限制、参数校验等，避免任何人都能随意触发 Jenkins Job。

这个 Application 就是你要开发的核心部分。我自己的实现是基于 GitHub Copilot 的 SDK 做的，但原理是通用的——你可以选择任何你熟悉的 AI 平台或 SDK，只要能通过 API 或 CLI 调用大语言模型即可。

### 第四步：构建 Skills 能力体系

这是整个设计中最重要的一环：**你的 Application 不应该是一个“大杂烩”式的脚本，而应该通过 Skills 来组织 AI 的能力**。

我的做法是建一个专门的 Git 仓库，结构大致如下：

```
ai-agent/
├── app/          # Application 主逻辑
└── skills/       # 各类技能定义
    ├── fix-bug/
    │   └── SKILL.md
    ├── draft-release-note/
    │   └── SKILL.md
    ├── analyze-root-cause/
    │   └── SKILL.md
    └── write-tests/
        └── SKILL.md
```

- `app/` 目录：管理 Application 的整体逻辑，包括接收 Webhook 请求、解析用户意图、调度 Skill、返回结果等。
- `skills/` 目录：每个 Skill 是一个以技能名命名的子目录，目录内有一个 `SKILL.md` 文件（大写），用自然语言描述这个技能要做什么、输入什么、输出什么。比如 `draft-release-note/SKILL.md` 可能包含：“根据最近的 commit 记录和 Jira Issue 列表，生成一份发布日志草稿，格式为 Markdown。”

这样设计的好处很明显：

1. **能力解耦**：增加新技能只需要在 `skills/` 目录下新增一个子目录和 `SKILL.md` 文件，不需要改动 Application 核心代码。
2. **版本可控**：Skills 文件在 Git 仓库中管理，有完整的变更历史和审核机制。
3. **易于协作**：团队里的任何人都可以提交新的 Skill 或改进现有 Skill，不依赖开发者单独排期。

每次 Application 启动时，会去 `skills/` 目录扫描当前有哪些能力可用，然后根据用户输入决定调用哪个 Skill。

### 第五步：实际运行效果

当这套系统跑起来之后，用户的操作体验是这样的：

1. 在任意 Jira Issue 的评论区 @ 你设置的那个 User，同时输入需求。比如 `@copilot 帮我生成这个版本的发布日志`
2. Jira Automation 检测到 @ 事件，向 Webhook 发送请求
3. Jenkins 接收到请求，启动 Application
4. Application 解析用户意图，匹配到对应的 Skill（比如 `draft-release-note`）
5. AI 按照 Skill 的定义执行任务，完成后将结果写回 Jira 评论

对用户来说，体验就是在评论区 @ 一下，然后在 Jira 里等它回评论，非常自然。

在我的场景里，目前比较适合处理的任务包括：撰写发布日志、分析构建失败原因、生成 Root Cause 分析草稿、根据上下文生成测试代码建议，或者在具备代码仓库权限的前提下做一些简单的修改。

然后你就可以不断的去优化这套系统，主要是 Skill，让它的输入越来越稳定和可靠。

### 小结

以上就是这套系统的大致实现思路。具体代码和技术细节我就不展开了，因为每家公司的技术栈、权限体系和内部流程都不一样，很难直接照搬。

但只要理解了这五个步骤背后的工作流，就完全可以在 AI 的辅助下，结合自己公司的实际情况，把类似的系统搭建起来。

本质上，这并不是一个特别神秘的东西。它更像是在公司内部创建了一个运行在 Jira 上、具备 AI 能力的机器人，或者说是一个“数字同事”。

以前你在 Jira 上 @ 某个同事，请他写发布日志、测试、改 bug；现在，你也可以 @ 这个新的数字同事，让它帮你完成这些工作。

这也是我觉得 AI 在企业内部真正有价值的地方：把那些原本需要反复沟通的工作，变得更自动、更顺畅。

希望这篇分享能给你一些启发。如果你也在做类似的尝试，欢迎在评论区一起交流。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
