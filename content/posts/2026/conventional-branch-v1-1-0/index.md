---
title: Conventional Branch 1.1.0 发布，正式支持 AI Coding Agent 分支前缀
summary: |
  Conventional Branch 规范迎来首次重大更新。1.1.0 版本新增了 AI Coding Agent 分支前缀支持（ai/、copilot/、cursor/、claude/、codex/），同时提供了 machine-readable 的 spec.json 和 agent 注册表，让规范不仅面向人，也面向工具。
tags:
  - Conventional Branch
  - Git
  - AI
  - Coding Agent
authors:
  - shenxianpeng
date: 2026-07-16
series: ["Conventional Branch"]
series_order: 3
---

大家好，我是沈工。

当越来越多的 AI Coding Agent 开始自动创建 Git 分支（branch）时，一个新的问题也随之出现：**这些分支应该遵循什么规范？**

Conventional Branch 自发布以来一直维持在 1.0.0 版本，而最新发布的 1.1.0，则主要围绕 AI Coding Agent 场景进行了扩展，以适应新的开发方式。

这篇文章就来聊聊这次更新的背景，以及 1.1.0 带来的几个重要变化。

## 为什么需要 AI 分支前缀

现在越来越多的开发者已经开始使用 AI Coding Agent，而不少工具都会自动创建分支。

例如，GitHub Copilot 默认创建 `copilot/` 分支，Claude 默认创建 `claude/` 分支。

这些命名方式已经逐渐成为事实标准（de facto standard）。因此，Conventional Branch 1.1.0 选择拥抱这一趋势，而不是重新定义它。

本次版本新增了以下 AI Agent 分支前缀：

```text
copilot/      — GitHub Copilot
cursor/       — Cursor
claude/       — Claude
codex/        — OpenAI Codex
ai/           — 通用 AI 分支
```

其中，`ai/` 是一个通用前缀，用于那些不属于特定供应商、但仍然由 AI 创建的分支。

## 如果常用的 Agent 不在列表中

目前规范中仅内置了几个常见的 AI Agent 前缀，同时我们还提供了一个可注册的 **Agent Registry**。

如果正在使用的 AI Coding Agent 没有包含在列表中，可以通过提交 PR 的方式将其添加到 `data/agents.yaml`。

PR 合并后，官方网站会自动同步更新对应的 Agent 列表。这样新的 AI Agent 无需等待规范发布新版本，也能够快速加入整个生态。

## spec.json：让规范可以被代码读取

对于工具开发者来说，`spec.json` 可能是本次更新中最重要的内容。

过去，如果希望通过代码验证一个分支是否符合 Conventional Branch，需要自己解析文档、提取 ABNF 语法，并维护一套正则表达式。

现在，我们提供了一份机器可读（machine-readable）的 `spec.json`，其中包含：

- 所有支持的 type（类型）及其 alias（别名）
- 分支命名规则
- ABNF 语法定义
- 可直接用于验证的正则表达式（regex）

这意味着，无论是 CI、Git Hook，还是 IDE 插件，都可以直接读取这份规范，而无需重复维护自己的规则。

例如，在 CI 中可以直接读取 `spec.json` 中提供的正则表达式进行验证：

```bash
REGEX=$(curl -s https://conventionalbranch.org/spec.json | jq -r '.grammar.regex')

if [[ ! "$BRANCH_NAME" =~ $REGEX ]]; then
  echo "分支名不符合 Conventional Branch 规范"
  exit 1
fi
```

当然，在生产环境中通常会缓存 `spec.json`，而不是每次运行 CI 时重新下载。

## 网站同步支持版本切换

随着 1.1.0 的发布，官方网站也同步增加了版本切换功能。

现在可以在网站中自由切换 1.0.0 与 1.1.0，对比不同版本之间的规范变化。

## 一点感想

从 1.0.0 发布到现在，Conventional Branch 已经走过了两年。

最初发布时，Git 分支规范还是一个相对小众的话题。后来随着 Conventional Commits 的普及，越来越多的团队开始重视代码提交和分支管理的规范化。

而今天，AI Coding Agent 正逐渐参与到日常开发流程中，Git 分支也开始越来越多地由 AI 自动创建。

在我看来，Conventional Branch 1.1.0 最大的变化，并不是新增了几个 AI 前缀，而是规范开始真正面向工具。

`spec.json` 让机器能够读取和理解规范，`data/agents.yaml` 让新的 Agent 可以持续加入生态。这意味着，Conventional Branch 不再只是一份供开发者阅读的文档，而是一个可以直接集成到工具链中的开放标准。

未来，协作对象将不再只是开发者，还包括越来越多的 AI Agent。规范，也需要随着开发方式一起演进。

如果还不了解 Conventional Branch，欢迎访问 https://conventionalbranch.org。

如果觉得它能够改善团队的 Git 分支管理，也欢迎尝试使用，并分享给更多开发者。

感谢大家一直以来对 Conventional Branch 的关注，我们下一篇再见。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」。