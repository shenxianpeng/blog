---
title: GitHub AI 名词全解析：Copilot、Agents、Models 到 MCP，到底谁是谁？
summary: 本文通过基于事实的解释和比喻，详细解读了 GitHub 上的 AI 相关概念及其层级关系，帮助读者理清 Models、Agents、Spaces、Spark 等术语的含义和作用。
tags:
  - AI
  - GitHub
authors:
  - shenxianpeng
date: 2025-12-26
---

先说明一点：我自己也不是 AI 专家，以下内容都是通过查阅官方文档再结合实际使用经验总结出来的认知。希望能帮大家少走一些弯路，看清 GitHub AI 的整体布局和各自作用。

最近一年，GitHub 上的 AI 的词越来越多：

> **Models、Agents、Spaces、Spark、Instructions、Agent Skills、MCP……**
> 名字很像，但很多人一看就混了。

很多人会问：

> Copilot 是啥？
> Agents 和 Models 有啥区别？
> Spark 是不是低代码工具？
> Skills 又是啥？
> MCP 到底在干什么？

今天我用一个大家熟悉、**基于事实解释＋比喻**的方式，帮你把这些东西搞清楚。

---

## 一、核心概念先明确

我们先从 GitHub 官方文档开始说起。

### 什么是 **GitHub Models**

官方说：

> GitHub Models 提供一个模型目录、提示管理和评估工具，让你直接在 GitHub 内进行模型比较、提示调优、性能评估和集成工作。它旨在降低企业级 AI 采用门槛，并与 GitHub 工作流程紧密结合。([GitHub Docs][1])

换句话说：

**Models 是“模型资源库 + 调试评估工具集”，不是具体的 AI 产品。**
它帮助你在 GitHub 内：

* 搜索不同大模型
* 调试和比较 prompt 输出
* 评估哪个模型更适合自己的任务

所以 **GitHub Models 不是 Copilot、也不是一个 Agent**，它是一个“AI 模型的实验/集成平台”。

---

## 二、我们举个比喻：AI 不是单一工具，而像一家 AI 化的软件公司

为了更好理解接下来的名词，我们用一个比喻：

> **把这些 AI 概念比作一家正在全面 AI 化的软件公司内部的组织结构和工具。**

---

## 三、一个个慢慢解释

### 1️⃣ Copilot：坐在你 IDE 旁边的“AI 助手”

这个不用多介绍：

* 它给你 **代码补全**
* 能理解上下文
* 能在 IDE 里边写边建议

官方这几年也在变：

* 加入了多模型支持（Anthropic Claude、Google Gemini、OpenAI 各模型等）([The Verge][2])
* 引入了更强的 Agent 模式（可以执行命令）([Wikipedia][3])

所以 Copilot 本质上还是：

> **一个为人类开发者服务的实时代码助手（IDE 旁的 AI）**

---

### 2️⃣ Agents：能被派活的“AI 员工”

这里的 **Agent** 不能简单理解为“Copilot 的某个模式”。它有一层更强的语义：

GitHub 的新闻报道里（Agent HQ）介绍：

> GitHub 未来会让开发者从不同模型和服务中创建和管理多个 AI 代理，统一调度、执行任务甚至并行运行，然后选择最合适的结果。([The Verge][4])

所以，**Agent ≠ Copilot 基本补全**，它更接近：

> **一个能被指派任务、执行具体工作（完成任务）的 AI 助手。**

比如：

* 自动创建 PR
* 批量处理文件
* 跑测试
* 自动回复 Issues

你告诉它“去干活”，它去执行，甚至可以组成任务队列。

这个概念也出现在社区工具中，很多人会用 Agent 去做自动 PR、监听 pipeline 等。这个模式比 Copilot 传统补全更“自动化”。

---

### 3️⃣ GitHub Spaces：AI 和上下文的“专用办公区”

这个是很多人最混的一个：

**官方文档明确：**

> Spaces 提供一个你可以访问的“空间”，把你想给 AI 的上下文放在一起。
> 当你在 IDE 中使用 Copilot 时，这些上下文会在背后被加载。([GitHub Docs][5])

很多人误以为 Spaces 是 Repo 的一种，但它不是。

它更像是：

> **一个专门准备好上下文、数据、说明文档的“协作空间”，让 AI 能更好理解你想做什么。**

比方说：

你在做一个新功能，把需求文档、设计稿、相关 Markdown 放到一个 Space 里，AI 拥有这个完整上下文，它自然就更能准确地响应。

**所以 Spaces = 上下文 + 知识汇聚点，而不是模型或 Agent 本身。**

---

### 4️⃣ GitHub Spark：快速做原型的“企划沙盒”

GitHub Spark 是 GitHub 新近推出的产品（目前处于预览阶段）：

根据社区消息：

> Spark 让 Copilot Pro+ 用户通过自然语言生成 **全栈应用**，直接从想法到部署，自动处理代码、配置、权限等，并支持代码中和后续扩展。([Reddit][6])

换句话说：

> **Spark 是一个把“想法 → 工作产品”自动实现的平台。**
> 它打包了多种模型、工作流、部署机制，让你写一句需求就能看到效果。

这比传统的 Copilot 补全或者 Agent 执行更进一步 —— 它是一个 **一体化快速原型车间**。

---

### 5️⃣ GitHub Instructions / Repository Custom Instructions（官方功能）

这是 GitHub Docs 里出现的一个功能：

你可以在 Repo 里写 **Custom Instructions** 来指导 Copilot 和 Agents：

> 告诉它：
>
> * 你的代码规范
> * 输出风格
> * 业务约束
> * 特定任务要求

换句话说：

> **Instructions = 给 AI 写的“行为规范/指南”**
> 让它回答时更贴合项目需求。

这和 Copilot 的“prompt”不同，它更像一套长期有效的项目习惯指南。

---

### 6️⃣ Agent Skills / Claude Skills：可被调用的能力模块

这里有两个概念：

* GitHub Agent Skills（官方）
* Claude Skills（Anthropic 社区体系）

官方说明：

> Agent Skills 是一组放在 `.github/skills` 的指令、脚本、资源，它们在需要时由 Copilot 载入以提升任务表现。([GitHub Docs][7])

而社区里的 Claude Skills 也是：

> 一套可以扩展 Claude 模型能力的“技能集合”，可以让它做特定任务（比如数据分析、表格处理、自动脚本）。([GitHub][8])

这意味着：

* Skills 本质上是“告诉 AI 去做好某类任务的详细指令 + 例子”
* 它有结构化定义（`SKILL.md` + 元数据）
* 不同于随机 prompt，它是一套可复用的模块

用比喻说：

> **Skills = 模块化的“职业技能包”，AI 在执行任务时可以调用它们。**

---

### 7️⃣ MCP（Model Context Protocol）：AI 世界的“标准接口协议”

最后这个概念，是很多人提到却最不清晰的一个。

官方文档和社区解释都说：

> MCP 是一种协议标准，允许 AI 助手与外部服务、安全连接和访问数据等进行统一交互。([GitHub Docs][9])

社区里也有很多人基于它做了 MCP server，让各种模型和工具通过 JSON 配置与 GitHub 进行交互，比如克隆仓库、提交 PR 等。([playbooks][10])

所以本质上：

> **MCP 不是模型、不是 Agent；
> 它是“让模型/Agent 能获取外部上下文、执行外部任务的通用协议”。**

可以看成：

* 就像 HTTP 是浏览器访问网页的标准协议
* MCP 是 AI Agent 访问工具和数据的标准协议

官方文档里有相关说明，但它并不是某个产品组件，而是一个**规范层协议**。

---

## 四、记住它们的关系（比喻版）

为了让大家一眼记住，下面是我的图景比喻：

| 概念            | 比喻           | 核心作用            |
| ------------- | ------------ | --------------- |
| Copilot       | 你的 AI 编程助手   | 实时代码建议          |
| GitHub Models | 模型资源库 + 调试平台 | 管理、评估多种模型       |
| Agents        | 能“干活”的 AI    | 自动执行具体任务        |
| Spaces        | AI 的协作工位     | 提供上下文环境         |
| Spark         | 原型快速实现室      | 让想法快速变成可运行成果    |
| Instructions  | AI 的行为指南     | 长期规范项目表现        |
| Skills        | 可复用技能包       | 模块化增强 AI 任务执行能力 |
| MCP           | AI 的标准协议接口   | 让 AI 能访问外部资源和数据 |

---

## 五、总结与行动建议

这些概念看起来很多，但从本质上：

1. **Models + MCP 是基础设施**
2. **Agents + Skills + Instructions 是生产力工具**
3. **Spaces + Spark 是工作空间/产品层**

理解了分层，你就可以：

* 先用 Copilot 补全/生成代码
* 尝试 Agents 自动化任务
* 在 Spark 做快速原型
* 用 Instructions 和 Skills 规范和增强 AI 行为

GitHub AI 发展很快，概念在演化。理解了这些层次，你就不会轻易混淆，也能更合理地引入 AI 到自己的开发流程。

[1]: https://docs.github.com/en/github-models/about-github-models "About GitHub Models - GitHub Docs"
[2]: https://www.theverge.com/2024/10/29/24282544/github-copilot-multi-model-anthropic-google-open-ai-github-spark-announcement "GitHub Copilot will support models from Anthropic, Google, and OpenAI"
[3]: https://en.wikipedia.org/wiki/GitHub_Copilot "GitHub Copilot"
[4]: https://www.theverge.com/news/808032/github-ai-agent-hq-coding-openai-anthropic "GitHub is launching a hub for multiple AI coding agents"
[5]: https://docs.github.com/en/copilot/how-tos/provide-context/use-copilot-spaces/use-copilot-spaces "Using GitHub Copilot Spaces - GitHub Docs"
[6]: https://www.reddit.com//r/AIGuild/comments/1m7xgg0 "GitHub Spark Ignites One‑Click AI App Building for Copilot Users"
[7]: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills "About Agent Skills - GitHub Docs"
[8]: https://github.com/anthropics/skills "GitHub - anthropics/skills: Public repository for Skills"
[9]: https://docs.github.com/zh/copilot/how-tos/agents/copilot-coding-agent/extending-copilot-coding-agent-with-mcp "使用模型上下文协议 (MCP) 扩展 Copilot 编码助手 - GitHub 文档"
[10]: https://playbooks.com/mcp/parassolanki-github "GitHub MCP server for AI agents"

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
