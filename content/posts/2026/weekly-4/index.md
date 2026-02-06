---
title: 攻城狮周刊（第 4 期）：AI 编程助手市场竞争加剧
summary: 这里记录每周值得分享的 DevOps 与 AI 技术内容，周五发布。本杂志开源，欢迎投稿。
tags: 
  - Weekly
translate: false
authors: 
  - shenxianpeng
date: 2026-02-05
---

这里记录每周值得分享的 DevOps 与 AI 技术内容，周五发布。

本杂志[开源](https://github.com/shenxianpeng/blog)。合作请[邮件联系](mailto:xianpeng.shen@gmail.com)（xianpeng.shen@gmail.com）。

## 本周封面

![封面图](featured.webp)

GitHub 在 2026 年 2 月 4 日宣布，Copilot Pro+ 和 Enterprise 订阅用户可以在平台上使用 Anthropic Claude 和 OpenAI Codex，打破单一 AI 模型限制。

## AI 编程助手进入多模型时代

本周，GitHub 宣布在 [Agent HQ](https://github.blog/news-insights/company-news/welcome-home-agents/) 平台支持 Anthropic Claude 和 OpenAI Codex，标志着 AI 编程助手市场从单一供应商走向多模型竞争格局。

数据显示，GitHub Copilot 目前拥有超过 150 万付费用户，每天生成数十亿行代码建议。Anthropic 的 Claude 在代码生成准确率测试中达到 87%，而 OpenAI Codex 在复杂重构任务中表现优异。这次开放意味着开发者可以根据任务特性选择不同模型：Claude 擅长代码理解和文档生成，Codex 在算法实现和性能优化方面更强。

市场层面，多模型竞争推动了功能快速迭代。目前 GitHub Copilot Pro 定价为每月 10 美元，Copilot Pro+ 为每月 39 美元。各家公司都在通过差异化定价策略和功能组合争夺市场份额。业界预测，2026 年 AI 辅助编程市场规模将达到 45 亿美元，较 2025 年增长 80%。

技术趋势上，多模型架构正在成为主流。除了 GitHub，JetBrains、Cursor 等 IDE 也在集成多个 AI 后端。开源社区推出的 OpenCode 项目，试图建立统一的 AI 编程助手接口标准，让开发者可以无缝切换不同模型。

安全问题也引发关注。本周，安全研究人员在 ClawHub（一个 AI 技能市场）中发现恶意插件，可以在用户不知情的情况下执行系统命令。这暴露了 AI 助手权限管理的漏洞，促使行业重新审视沙盒隔离和权限控制机制。

## 行业动态

1、[**GitHub 开放 Claude 和 Codex 支持，打破 AI 编程助手单一模型限制**](https://github.blog/news-insights/company-news/pick-your-agent-use-claude-and-codex-on-agent-hq/)

![GitHub Agent HQ](news-1.png)

GitHub 在 2 月 4 日宣布，Copilot Pro+ 和 Enterprise 用户可以在 GitHub 和 VS Code 中使用 Anthropic Claude 和 OpenAI Codex。这是继去年 10 月支持 GPT-4 后，GitHub 首次引入竞争对手的模型。用户可以在设置中切换模型，根据任务选择最适合的 AI 助手。GitHub 表示，多模型支持将在未来几周内向所有付费用户开放。

2、[**Substack 确认数据泄露，影响用户邮箱和电话号码**](https://techcrunch.com/2026/02/05/substack-confirms-data-breach-affecting-email-addresses-and-phone-numbers/)

![数据泄露](news-2.png)

写作平台 Substack 在 2 月 5 日确认遭遇数据泄露，黑客窃取了部分用户的电子邮件地址和电话号码。公司表示，密码和支付信息未受影响，已通知受影响用户并重置安全措施。同日，政府技术服务商 Conduent 也披露数据泄露事件扩大，影响人数从最初的数十万增至数百万，涉及社保号、医疗记录等敏感信息。

3、[**OpenCode 开源 AI 编程助手，对标 Claude Code 和 Copilot**](https://www.infoq.com/news/2026/02/opencode-coding-agent/)

![OpenCode](news-3.png)

开源 AI 编程助手 OpenCode，支持多种大语言模型后端，可自行部署。项目在 GitHub 上已获得 95k Stars，承诺完全开源、无数据上传。OpenCode 提供代码补全、重构、测试生成等功能，但性能和稳定性仍待验证。开源社区对此反响积极，认为这是对抗商业 AI 工具垄断的重要尝试。

4、[**Vercel 推出 Skills.sh，建立 AI Agent 命令开放生态**](https://www.infoq.com/news/2026/02/vercel-agent-skills/)

![Vercel Skills](news-4.png)

Vercel 在 1 月 20 日发布 Skills.sh 平台，允许开发者创建、分享和复用 AI Agent 命令。这是继 OpenAI GPTs 和 Anthropic Claude Skills 后，第三个主要的 AI 能力扩展平台。Skills.sh 提供开放市场，任何人都可以发布技能包。但 2 月 2 日，安全公司 [1Password 披露](https://1password.com/blog/from-magic-to-malware-how-openclaws-agent-skills-become-an-attack-surface)，ClawHub 平台上排名第一的技能包含恶意代码，引发对开放市场安全性的担忧。

5、[**ElevenLabs 完成 5 亿美元融资，估值 110 亿美元**](https://techcrunch.com/2026/02/05/elevenlabs-ceo-voice-is-the-next-interface-for-ai/)

![ElevenLabs](news-5.png)

AI 语音公司 ElevenLabs 在 2 月 5 日宣布完成 5 亿美元融资，由 Sequoia Capital 领投，估值达到 110 亿美元。CEO 表示，语音将成为 AI 的下一个主流交互界面。公司在多语言语音合成和实时翻译领域取得突破，支持 32 种语言，每月处理超过 10 亿次语音请求。市场分析认为，语音 AI 市场规模将在 2027 年超过 300 亿美元。

## 深度阅读

1、[**如何最大化 GitHub Copilot 的 Agent 能力**](https://github.blog/ai-and-ml/github-copilot/how-to-maximize-github-copilots-agentic-capabilities/)

![Copilot Agent](blog-1.png)

GitHub 工程团队分享了如何在实际项目中架构和扩展 Copilot 的应用。文章介绍了从简单代码补全到复杂多步骤任务自动化的演进路径，包括提示词模板设计、上下文管理系统、自定义工具集成等技术细节。核心观点包括：Copilot 的价值在于理解意图并自动化工作流，上下文窗口管理是关键瓶颈，自定义工具可以访问企业内部系统。文章基于 GitHub 内部使用经验，提供了大量实践案例和代码示例。

2、[**与代码助手协作：骨架架构方法**](https://www.infoq.com/articles/skeleton-architecture/)

![骨架架构](blog-2.jpg)

InfoQ 文章提出了"骨架架构"（Skeleton Architecture）概念，即先用 AI 生成项目整体结构和接口定义，再由人工填充核心逻辑。文章认为，这种方法结合了 AI 的快速搭建能力和人类的深度思考能力，特别适合快速原型开发和遗留系统重构。作者通过三个实际案例展示了骨架架构的应用：电商系统重构、微服务拆分、API 网关设计。数据显示，使用骨架架构可以将项目初始化时间缩短 60%，代码一致性提高 40%。

3、[**为什么大多数机器学习项目无法投入生产**](https://www.infoq.com/articles/why-ml-projects-fail-production/)

这篇深度文章剖析了 ML 项目失败的根本原因。研究显示，80% 的 ML 项目在 POC（概念验证）阶段后就停滞，主要原因包括：数据质量问题、模型漂移、部署复杂度、监控缺失、组织问题等。文章特别指出，数据管道的稳定性比模型精度更重要，ML 系统需要持续监控和再训练，复杂度是传统软件的 10 倍。作者基于对 200+ 个 ML 项目的调研，提出了 MLOps 成熟度模型和最佳实践建议。

## 效率工具

1、**[sqldef](https://sqldef.github.io/)**

![sqldef](tool-1.png)

sqldef 是支持 MySQL、PostgreSQL 和 SQLite 的幂等 Schema 管理工具。它采用声明式设计，用户只需定义目标 Schema，工具会自动生成并执行所需的 DDL 语句。支持干运行模式、与 Git 工作流集成、CI/CD 自动化。项目在 GitHub 获得 2.7k Stars，用 Go 语言开发，支持 Docker 部署。适合微服务架构的 Schema 版本管理和本地开发环境快速搭建。

2、**[Graft](https://github.com/ms-henglu/graft)**

Graft 是一个把 Overlay（叠加）模式带进 Terraform 的 CLI 工具。它允许你在不 fork、不修改源码的前提下，对第三方 Terraform module 做“补丁式”改造。你可以覆盖模块里写死的值、注入新的资源或输出，甚至删除不符合公司规范的资源。上游模块依然保持官方版本，升级时只需要改版本号，补丁会自动重新应用。可以把 Graft 理解为 Terraform 世界里的 Kustomize。Go 语言实现，GitHub Stars 30+。

3、**[Nanobot](https://github.com/hkuds/nanobot)**

![Nanobot](tool-3.png)

Nanobot 是超轻量 AI Agent 框架，代码库仅数百行，定位为 OpenClaw 的简化替代。提供基础的对话管理、工具调用和上下文处理功能，但放弃了高级特性。核心代码少于 500 行，无外部依赖，启动速度快，资源占用低。支持 OpenAI、Anthropic、本地模型等主流 LLM API。适合嵌入式 Agent、资源受限环境、快速原型开发、学习 Agent 内部原理。Python 实现，GitHub Stars 9.4k。

## 开源项目

1、**[Frappe HR](https://github.com/frappe/hrms)**

![hrms](open-1.png)

Frappe HR 是一个 完全开源的 HR 和薪资管理系统（HRMS），基于 Frappe 框架构建，适用于各种规模的组织。它集成了员工生命周期管理、请假与考勤、绩效考核、报销与预支、薪资与税务等超过十几个核心模块，覆盖从员工入职到离职的完整流程。

2、**[Daggr](https://github.com/gradio-app/daggr)**

![Daggr](open-2.png)

Daggr 是用于构建可检查、可调试的 AI 工作流 Python 库。提供 DAG（有向无环图）式任务编排，每个节点的输入输出都可追踪。支持可视化调试、增量执行、与主流 ML 框架集成（LangChain、HuggingFace）。特别适合复杂 AI Agent 和数据处理流程。

3. **[NotepadNext](https://github.com/dail8859/NotepadNext)**

![NotepadNext](open-3.png)

NotepadNext 是一个由个人开发的跨平台开源文本/代码编辑器，用 C++ 和 Qt 重写 Notepad++，支持 Windows、macOS 和 Linux 等系统，是 Notepad++ 的跨平台实现。


## 学习资源

1、[InfoQ 2025 年技术趋势报告合集](https://www.infoq.com/minibooks/2025-infoq-trends-reports-emag/)

InfoQ 发布了 2025 年全系列技术趋势报告，涵盖 Java、云计算与 DevOps、AI/ML、架构设计、文化与方法论五大领域。每份报告分析技术成熟度曲线、采用建议和未来走向。报告基于真实项目经验，由领域专家撰写。主要发现包括：平台工程从新兴进入主流采用阶段，生成式 AI 从试验转向生产，事件驱动架构和 CQRS 进入主流，远程协作成为常态，工程师体验（DevEx）受到重视。总页数超过 150 页，免费下载。

## 精彩摘要

1、"我从未感到作为程序员如此落后。这个职业正在被大幅重构，程序员贡献的代码越来越稀疏。我有种感觉，如果我能恰当地串联起过去一年所出现的工具，我可以强大 10 倍，而未能获得这种提升明显是一个技能问题。"
—— Andrej Karpathy，OpenAI 联合创始人

2、"上个月是我作为工程师的第一个月，完全没有打开 IDE。Opus 4.5 写了大约 200 个 PR，每一行代码都是它写的。软件工程正在发生根本性变化，即使对于像我们这样的早期采用者和从业者来说，最困难的部分是持续重新调整我们的期望。"
—— Boris Cherny，Claude Code 创建者

3、"软件生产的成本正在趋向于零。"
—— Malte Ubl，Vercel CTO

## 行业观点

1、AI 不会终结工程职业，它正在对它们进行分类。
—— Morson Jobs 报告

这个观点准确概括了当前趋势。Morson Jobs 的研究显示，能够有效利用 AI 工具的工程师薪资溢价达到 30%，而仅依靠传统编码技能的工程师需求下降了 15%。报告指出，2026 年最重要的技能是提示工程、系统架构、产品思维，而不是单纯的代码编写能力。

（完）
