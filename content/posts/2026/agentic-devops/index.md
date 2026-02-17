---
title: Agentic DevOps 初探：GitHub Agentic Workflow 与 Continuous AI 的实践观察
summary: | 
  最近又接触到一个相关但更进一步的概念——Agentic DevOps。花时间阅读了微软 Azure 相关介绍、GitHub 的最新文档以及部分开源实践后，我整理了这篇笔记。目的是记录学习过程，也供同行参考。以下内容基于公开资料和我的理解，不涉及任何夸大预测。
tags:
  - Agentic DevOps
  - DevOps
authors:
  - shenxianpeng
date: 2026-02-17
---

之前在公众号分享过 [AIOps 的基本概念](../aiops/index.md)和部分落地场景，主要是围绕运维监控、异常检测和自动化响应等方向。最近接触到 Agentic DevOps 这个概念，以及 GitHub Next 提出的 Continuous AI 相关实践，觉得值得整理出来和大家交流。

这些内容目前大多仍处于早期探索阶段。我自己也只是基于公开文档和示例做过一些简单尝试，还没有进行大规模生产环境验证。

本文仅基于公开信息和有限测试，尽量讲清核心原理、工具形态以及当前边界，避免过度解读。

### Agentic DevOps 的核心含义

Agentic DevOps 可以理解为 DevOps 的下一阶段演进：引入具备一定自主能力的 AI agents，让它们与开发者、以及其他 agents 协作，覆盖软件生命周期的各个环节。

具体来说：
- **规划与编码阶段**：agents 可以处理代码审查、生成测试、修复简单 bug、更新文档等重复性工作。
- **交付与运维阶段**：结合 CI/CD 流水线，自动分析失败原因、建议修复，甚至在生产环境中监控并响应部分事件。

Microsoft 和 GitHub 的表述中，强调 agents 是“开发者的队友”，而非替代者。核心是把人类从琐碎事务中解放出来，聚焦更高价值的决策。

与传统 AIOps 相比，Agentic DevOps 的范围更广，不再局限于运维层，而是贯穿从需求到生产的全链路。技术实现上通常依赖大型语言模型（LLM）的推理能力，结合工具调用（tool calling）机制以及多代理协作框架。

### GitHub 的 Agentic Workflow 与 Continuous AI

GitHub Next 把这类自动化称为 Continuous AI，类比 CI/CD 中“持续”的理念：AI 不只是单次辅助，而是持续、后台运行在仓库中，处理需要判断力的任务。

**Agentic Workflow** 是实现 Continuous AI 的具体形式（目前为技术预览/研究原型）：
- **编写方式**：不再编写复杂的 YAML，而是使用 Markdown 文件，在 `.github/workflows/` 目录下描述意图。比如写一段自然语言：“每天生成仓库健康报告，总结最近 issue、PR 变化，并提出改进建议。”
- **执行机制**：通过 `gh aw` CLI 工具编译成标准 GitHub Actions 工作流，由支持的 coding agent（GitHub Copilot、Claude Code、OpenAI Codex 等）执行。
- **触发与运行**：支持 schedule、push、issue 等事件触发，运行在 GitHub Actions 的沙箱环境中。
- **安全边界**：默认只读权限；写操作（如创建 PR、评论）必须通过预定义的 safe outputs；工具调用有白名单；所有日志可见、可审计；不会自动合并 PR，始终保留人工审查环节。

这是官方关于 Agentic Workflow 的介绍。

![](gh-aw.png)

实际能做的例子包括：
- 持续 triage：自动标签、摘要新 issue。
- 持续文档更新：根据代码变更同步 README 或 API 文档。
- 持续质量检查：分析测试覆盖率、提出新增测试建议。
- 每日仓库状态报告：汇总活动并给出可行动项。

这些工作流可以与现有 CI/CD 流水线并行运行，作为补充，而非替代。

这里有一个 [GitHub 官方示例仓库](https://github.com/githubnext/agentics)，展示了很多 Agentic Workflow 的用例，可以参考。

### 当前阶段与落地边界

从公开信息看（截至 2026 年 2 月）：
- 大部分实现仍处于技术预览或研究原型阶段。
- GitHub Agentic Workflow 需要安装 CLI 扩展，配置 agent token，成本方面每次运行会消耗对应模型的调用额度（例如 Copilot 的 premium 请求）。
- 适用场景主要是“需要判断但可描述清楚”的重复任务。纯确定性操作（如构建、单元测试）仍推荐传统 Actions。
- 边界很清晰：目前 agents 目前不具备完全自主决策能力，输出结果必须经过人工审核；不适合高安全敏感操作；效果依赖提示工程和仓库上下文质量。

我在个人仓库里测试过一个简单的每日报告 workflow，基本能按预期输出总结。

### 为什么值得关注

学习这些概念，不是为了立刻替换现有流程，而是保持对工具演进的感知。在实际工作中，我们可以：
- 在个人或小团队仓库里低成本尝试 Agentic Workflow，积累经验。
- 思考现有 DevOps 流水线中哪些环节适合引入 agents（例如文档维护、初步 triage）。
- 关注 Microsoft Azure、GitHub 等厂商的后续更新，以及开源社区的 agentics 示例仓库。

最终，技术始终服务于人。Agentic DevOps 和 Continuous AI 只是提供了新的可能性，落地效果取决于具体场景、团队规模和治理能力。

欢迎大家在评论区分享自己的尝试或观察。我也会继续跟踪这些工具的进展，有新实践再和大家交流。