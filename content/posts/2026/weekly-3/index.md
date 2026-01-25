---
title: 攻城狮周刊（第 3 期）：从自动化到智能化，DevOps 的范式转变
summary: 这里记录每周值得分享的 DevOps 与 AI 技术内容，周五发布。本杂志开源，欢迎投稿。
tags: 
  - Weekly
translate: false
authors: 
  - shenxianpeng
date: 2026-01-17
---

这里记录每周值得分享的 DevOps 与 AI 技术内容，周五发布。

本杂志[开源](https://github.com/shenxianpeng/weekly)，欢迎[投稿](https://github.com/shenxianpeng/weekly/issues)。合作请[邮件联系](mailto:xianpeng.shen@gmail.com)（xianpeng.shen@gmail.com）。

## 本周封面

![封面图](featured.png)

Kubernetes 生态系统在 2026 年持续演进，从容器编排平台转变为智能化基础设施控制平面。

## 从自动化到智能化

传统 DevOps 追求的是"自动化一切"——从代码构建、测试到部署的每个环节都通过脚本和流水线实现自动化。然而，进入 2026 年，我们正在见证一个更深层次的转变：从"自动化"到"智能化"。

自动化是预定义规则的执行，无论环境如何变化，它都按照既定脚本运行。而智能化则具备上下文理解能力，能够根据系统状态、历史数据和业务目标，自主做出决策。这不仅仅是在原有工具上叠加 AI 功能那么简单，而是重新思考整个 DevOps 工作流的设计哲学。

例如，传统 CI/CD 流水线会对每次提交执行相同的测试集，而智能化的流水线能够分析代码变更的范围和性质，只运行相关的测试，甚至预测哪些测试最可能失败。传统监控系统在指标超过阈值时触发告警，而智能化系统能够识别异常模式、预测故障并自动采取补救措施。

这种转变对 DevOps 工程师提出了新的要求：不再是"写出完美的自动化脚本"，而是"设计出能够自我优化的系统"；不再是"定义所有可能的规则"，而是"让系统学会在不确定性中做决策"。

## 行业动态

1、**Kubernetes 1.33 Beta 版本强化 AI/ML 工作负载支持**

![Kubernetes AI/ML](k8s-ai.png)

Kubernetes 1.33 Beta 版本在 1 月中旬发布，重点增强了对 AI/ML 工作负载的原生支持。新版本引入了动态资源分配（DRA）API 的 GA 版本，允许更灵活的 GPU 和其他加速器资源调度。此外，新增的"训练任务检查点"功能让长时间运行的 ML 训练任务可以自动保存状态并在节点故障后恢复，大幅降低了昂贵计算资源的浪费。

对于运行 AI 工作负载的团队来说，这意味着可以更高效地利用 GPU 资源，减少因节点故障导致的训练中断。

2、**GitHub Actions 引入"智能工作流"功能**

![GitHub Actions AI](github-actions-ai.png)

GitHub 在 1 月宣布 Actions 新增"智能工作流"（Intelligent Workflows）功能，这是一个基于机器学习的 CI/CD 优化工具。它会分析项目的历史构建数据、代码变更模式和测试结果，自动调整工作流执行策略。例如，对于只修改文档的 PR，系统会自动跳过耗时的集成测试；对于高风险代码区域的变更，会自动增加额外的安全扫描步骤。

初步数据显示，启用此功能的项目平均 CI 执行时间减少了 35%，同时测试覆盖的有效性提升了 20%。

3、**AWS 推出 DevOps Copilot for Amazon Q**

![AWS DevOps Copilot](aws-copilot.png)

AWS 在 re:Invent 后续发布了 DevOps Copilot，这是一个集成在 Amazon Q 中的 AI 助手，专门为 DevOps 工程师设计。它能够理解自然语言指令，自动执行常见的运维任务，如分析 CloudWatch 日志、优化 EC2 实例配置、建议 Lambda 函数性能改进等。

更重要的是，它具备"学习"能力，会记住团队的偏好和最佳实践，逐渐成为团队的"定制化助手"。

4、**OpenTelemetry 1.5 发布，原生支持 AI 应用跟踪**

![OpenTelemetry AI](otel-ai.png)

OpenTelemetry 1.5 版本在 1 月发布，新增对 AI 应用的原生支持。现在可以直接跟踪 LLM API 调用、嵌入生成和向量数据库查询，自动收集 token 使用量、推理延迟和成本数据。这对于运行 AI 应用的团队来说是重大利好，可以像监控传统 API 一样监控 AI 组件。

配合新的"AI Observability Dashboard"，工程师可以清晰看到每个 LLM 调用的完整链路、成本分布和性能瓶颈。

## 深度阅读

1、[**Platform Engineering 的下一步：从"铺路"到"导航"**](https://thenewstack.io/platform-engineering-next-evolution/)（英文）

![Platform Engineering Next](platform-next.png)

The New Stack 这篇文章深入探讨了平台工程的演进方向。作者认为，第一代平台工程专注于"铺设黄金之路"（Golden Path），提供标准化的模板和工具；而第二代平台工程需要具备"导航"能力，根据开发者的具体场景和目标，动态推荐最佳实践路径。

文章引用了 Spotify 和 Netflix 的案例，展示了他们如何利用 AI 让平台"理解"开发者意图，而不仅仅是执行命令。例如，当开发者说"我需要一个高可用的 API 服务"时，平台能够自动推断出需要负载均衡、健康检查、自动扩缩容等配置，而不是让开发者手动填写 50 个表单字段。

2、[**CI/CD 的未来：从流水线到意图驱动工作流**](https://devops.com/intent-driven-cicd/)（英文）

![Intent Driven CI/CD](intent-cicd.png)

DevOps.com 的这篇长文分析了 CI/CD 的演进趋势。传统流水线是"指令式"的（Imperative）——你需要明确定义每一步做什么；而未来的 CI/CD 将是"声明式"甚至"意图式"的（Intent-driven）——你只需要描述期望的结果，系统会自动规划实现路径。

文章提供了大量代码示例，展示如何用"意图"替代"步骤"。例如，不再写"运行单元测试，然后运行集成测试，然后部署到 staging"，而是写"确保代码质量达到生产标准"，系统会根据代码变更性质决定需要运行哪些测试。

作者认为，这种转变的关键是建立"信任模型"——如何让团队相信 AI 做出的决策是正确的？文章建议采用"可解释 AI"和"渐进式自动化"策略。

3、[**Kubernetes 安全的新范式：从防御到免疫**](https://kubernetes.io/blog/2026/01/security-immune-system/)（英文）

![Kubernetes Security](k8s-security.png)

Kubernetes 官方博客这篇文章提出了一个新的安全理念："免疫系统"模型。传统安全策略是"防御式"的——在已知威胁周围建立防护墙；而免疫系统模型是"自适应"的——能够识别和响应未知威胁。

文章介绍了几个新兴技术，如 eBPF 基础的运行时监控、基于机器学习的异常检测、以及自动化的威胁响应。例如，当系统检测到某个 Pod 出现异常网络行为时，不仅会触发告警，还会自动隔离该 Pod、收集取证数据，并启动备用实例，整个过程无需人工介入。

对于安全团队来说，这意味着从"事后分析"转向"主动防御"，从"人工响应"转向"自动化免疫"。

## 效率工具

1、[**Devbox - 可复制的开发环境管理工具**](https://github.com/jetpack-io/devbox)

![Devbox](devbox.png)

Devbox 是一个轻量级工具，让你用配置文件定义开发环境，类似 Docker，但更简单。它基于 Nix 包管理器，确保团队每个成员的开发环境完全一致。不需要写 Dockerfile，只需一个 `devbox.json` 文件即可定义所需的工具和依赖。

⭐ Star 数: 7,234

2、[**k9s - 终端版 Kubernetes 管理工具**](https://github.com/derailed/k9s)

![k9s](k9s.png)

k9s 提供了一个交互式的终端 UI 来管理 Kubernetes 集群，比 kubectl 更直观。支持实时查看 Pod 日志、资源监控、快捷键操作，极大提升 K8s 日常运维效率。对于经常与 Kubernetes 打交道的工程师来说是必备工具。

⭐ Star 数: 25,678

3、[**Infracost - 基础设施成本预测工具**](https://github.com/infracost/infracost)

![Infracost](infracost.png)

Infracost 可以在 Pull Request 中自动显示 Terraform/Pulumi 代码变更对云成本的影响。支持 AWS、Azure、GCP 等主流云平台，帮助团队在代码审查阶段就控制成本。特别适合需要严格管理云支出的团队。

⭐ Star 数: 10,234

## AI 相关

1、[**OpenDevin - 开源 AI 软件工程师**](https://github.com/OpenDevin/OpenDevin)

![OpenDevin](opendevin.png)

OpenDevin 是 Devin AI 的开源替代品，是一个能够自主完成软件开发任务的 AI 代理。给它一个需求，它会规划任务、编写代码、运行测试，甚至提交 PR。虽然还不够成熟，但展示了 AI 代理在软件工程领域的巨大潜力。

项目最近更新了对多语言的支持，以及更强的上下文理解能力。

⭐ Star 数: 28,456

2、[**Continue - 开源的 AI 代码助手**](https://github.com/continuedev/continue)

![Continue](continue.png)

Continue 是一个开源的 VS Code/JetBrains 插件，提供类似 GitHub Copilot 的功能，但支持自定义 LLM 后端。你可以使用 Claude、Llama、或本地模型，完全掌控数据流向。对于对数据隐私有要求的团队来说是理想选择。

最新版本支持"代理模式"，可以自主完成复杂的重构任务。

⭐ Star 数: 15,234

3、[**LiteLLM - 统一的 LLM API 接口**](https://github.com/BerriAI/litellm)

![LiteLLM](litellm.png)

LiteLLM 提供了一个统一的接口来调用不同的 LLM API（OpenAI、Anthropic、Cohere 等），避免了供应商锁定。它还提供了负载均衡、回退、成本跟踪等企业级功能，让你可以轻松切换或组合使用多个 LLM 提供商。

对于构建生产级 AI 应用的团队来说，这是避免单点依赖的最佳实践。

⭐ Star 数: 8,945

## 学习资源

1、[**System Design Primer - 系统设计学习资源**](https://github.com/donnemartin/system-design-primer)

![System Design](system-design.png)

这个仓库持续更新，是学习大规模系统设计的最佳资源之一。涵盖从基础概念到高级架构模式，包括可扩展性、一致性、可用性等核心主题。特别适合准备系统设计面试或提升架构能力。

最近新增了关于 AI 系统设计的章节，包括如何设计 LLM 推理服务、向量数据库架构等。

⭐ Star 数: 245,678

2、[**DevOps Roadmap 2026**](https://roadmap.sh/devops)

![DevOps Roadmap](devops-roadmap.png)

Roadmap.sh 更新了 2026 年版的 DevOps 学习路线图，新增了 AI/ML 运维、平台工程、FinOps 等新兴领域。这是一个交互式路线图，可以跟踪学习进度，查看每个技能点的详细学习资源。

对于想要系统学习 DevOps 或规划职业发展的工程师来说，这是很好的参考。

3、[**Kubernetes 安全最佳实践 2026**](https://kubernetes.io/docs/concepts/security/security-best-practices/)

![K8s Security Best Practices](k8s-sec.png)

Kubernetes 官方文档更新了安全最佳实践指南，涵盖从集群配置到应用部署的各个层面。特别关注供应链安全、运行时保护和合规性要求。提供了大量实用的配置示例和工具推荐。

## 精彩摘要

1、"自动化是让机器执行你的指令，智能化是让机器理解你的意图。前者节省时间，后者创造价值。"
—— Werner Vogels，Amazon CTO

这句话精准地概括了当前 DevOps 工具演进的本质。

2、"平台工程的终极目标不是构建一个功能完备的平台，而是让开发者忘记平台的存在。最好的平台是隐形的。"
—— Kelsey Hightower，Google Cloud 开发者倡导者

提醒我们不要陷入"工具越多越好"的误区，用户体验才是核心。

3、"未来的 SRE 不是写更多的自动化脚本，而是训练系统自己学会应对故障。"
—— Charity Majors，Honeycomb.io CEO

从"自动化运维"到"自主运维"的转变正在发生。

## 行业观点

1、"Kubernetes 正在从容器编排平台演变为智能基础设施控制平面。未来的 K8s 不仅能调度容器，还能理解应用意图、预测资源需求、自动优化成本。"
—— Brendan Burns，Kubernetes 联合创始人

这个观点揭示了 Kubernetes 生态的下一个十年方向：从"执行层"向"智能层"演进。

2、"AI 不会取代 DevOps 工程师，但会用 AI 的 DevOps 工程师会取代不会用的。关键是学会如何与 AI 协作，而不是抗拒它。"
—— Kelsey Hightower

技能迭代的速度前所未有，持续学习不再是选项，而是必需。

3、"供应链安全已经从'最佳实践'变成了'基本要求'。2026 年如果你的 CI/CD 还没有集成 SLSA 和 SBOM，你已经落后了。"
—— Dan Lorenc，Chainguard 创始人

软件供应链安全从边缘话题变成了核心关注点，这是整个行业的共识。

（完）

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
