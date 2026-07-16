---
title: Conventional Branch 1.1.0 发布，正式支持 AI Coding Agent 分支前缀
summary: |
  Conventional Branch 规范迎来首次重大更新。1.1.0 版本新增了 AI coding agent 分支前缀支持（ai/、copilot/、cursor/、claude/、codex/），同时提供了 machine-readable 的 spec.json 和 agent 注册表，让规范不仅面向人，也面向工具。
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

Conventional Branch 自发布以来，一直维持在 1.0.0 版本。最近我们发布了 1.1.0 版本，主要的变化就是对于 AI 的支持，以适应新的编程时代的变化。

这篇文章就来聊聊这次更新的背景和具体内容。

## 为什么需要 AI 分支前缀

大家都知道，很多 Code Agent 在写代码时，默认创建的 branch 都是根据自己的供应商来命名的。

比如 GitHub Copilot 创建的 branch 就是 `copilot/`，Claude 创建的 branch 就是 `claude/`。

这已经是一个行业的默认规则了。因此在 1.1.0 中，我们新增了以下 AI agent 前缀：

```
copilot/      — GitHub Copilot 生成
cursor/       — Cursor 生成
claude/       — Claude 生成
codex/        — OpenAI Codex 生成
ai/           — 通用 AI 生成分支
```

> 其中 `ai/` 是一个通用前缀，用于那些不属于特定供应商、但仍然是由 AI 生成的 branch。

## 如果你常用的 Agent 没有在列表中

目前仅仅是在文档里列出了这几个前缀。我们还提供了一个**可注册的 agent 前缀 registry**。

如果你正在使用的 AI coding agent 没有在列表中，可以通过提交 PR 的方式将其添加到 `data/agents.yaml` 中。

PR 一经合并就会同步到官方网站的表格中，帮助更多开发者识别和使用这些 AI 分支前缀。

## spec.json：让规范可以被代码读取

除了 AI 前缀，这次更新的另一个重点是 `spec.json`。

以前，如果你想通过代码去验证一个 branch 是否符合 Conventional Branch 规范，你需要自己去解析文档、提取 ABNF 语法、手写正则表达式。这个过程既容易出错，也难以保持一致。

现在，我们在 [conventionalbranch.org/spec.json](https://conventionalbranch.org/spec.json) 提供了一份 machine-readable 的规范文件，包含了以下内容：

- 所有支持的 type（类型）及其 alias（别名）
- 分支命名规则
- ABNF 语法定义
- 可直接用于验证的 regex

这意味着你可以直接用代码去读取这份 spec，然后用其中的 regex 来验证你的分支命名是否正确。

举个例子，如果你在 CI 中想要检查当前分支是否符合规范，不需要再重复维护一套正则规则了：

```bash
# 从 spec.json 中提取 regex，然后做验证
REGEX=$(curl -s https://conventionalbranch.org/spec.json | jq -r '.grammar.regex')
if [[ ! "$BRANCH_NAME" =~ $REGEX ]]; then
  echo "分支名不符合 Conventional Branch 规范"
  exit 1
fi
```

## 版本切换和网站更新

随着 1.1.0 的发布，规范文档网站也做了相应的更新。现在你可以在网站上看到版本切换器，在 1.0.0 和 1.1.0 之间切换，来查看不同版本的差异。

## 一点感想

从 1.0.0 发布到现在，Conventional Branch 已经走过了两年之久。

最初发布的时候，Git 分支规范还是一个相对小众的话题。后来随着 Conventional Commits 的普及，越来越多的团队开始重视代码提交和分支的规范化管理。

而现在，随着 AI coding agent 的广泛使用，"如何让规范适应 AI 时代" 成了一个需要认真对待的问题。

在我看来，Conventional Branch 1.1.0 的意义不在于增加了几个新前缀，而在于**规范从只面向人，开始面向工具了**。

`spec.json` 让机器可以读取和理解规范，`data/agents.yaml` 让新的 agent 前缀可以动态注册。这些变化让规范不再是一份静止的文档，而是一个可以被集成到工具链中的活的标准。

如果你还不知道 Conventional Branch，可以去 [conventionalbranch.org](https://conventionalbranch.org) 看看。

如果觉得它能给你们团队的分支策略带来更好的开发体验，也欢迎大家使用或转发推荐。

感谢大家一直以来对 Conventional Branch 的关注，我们下一篇再见～

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
