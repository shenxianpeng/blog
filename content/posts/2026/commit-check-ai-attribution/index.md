---
title: Commit Check 新功能：AI 归属治理与近期亮点功能回顾
summary: |
  Commit Check 在最新版本中引入了 AI 归属治理功能——通过配置 ai_attribution = "forbid"，可以拒绝包含已知 AI 工具签名的提交。
  这篇博客也一并回顾了从 v2.5.0 到 v2.10.0 之间的多个重要更新，包括分支规范增强、强制推送保护、输出控制等。
tags:
  - Commit-Check
  - DevOps
  - AI
authors:
  - shenxianpeng
date: 2026-07-06
series: ["Commit Check"]
series_order: 4
---

大家好，我是沈工。

距离上次写 Commit Check 的更新已经过去大半年了。这段时间 Commit Check 发布了不少版本，今天趁着一个我觉得特别重要的新功能刚刚合入，写篇博客聊聊。

## 先说最重要的：AI 归属治理

刚刚发布的 v2.11.0 发布的核心功能——**AI 归属治理（AI Attribution Governance）**。

这个功能解决什么问题呢？

随着 Claude Code、GitHub Copilot、Cursor、Windsurf、Devin 等 AI 编程工具的普及，开源社区面临一个新问题：**如何知道一个提交是由人类还是 AI 写的？**

Python 社区在 [discuss.python.org](https://discuss.python.org/t/should-claude-codes-usage-be-described-in-the-code-docs-somewhere/107969) 上专门讨论过这个问题，Linux Kernel 标准化了 `Assisted-by:` 格式，VS Code 也有相关的 [issue](https://github.com/microsoft/vscode/issues/313962) 讨论是否用 `Assisted-by` 替代 `Co-authored-by` 来标注 AI 贡献者。

但问题是，目前似乎没有一款工具能在 CI 层面自动执行这种策略。

Commit Check 本身就是做 commit 检查的，很适合来做这个事情。

### 配置方式

非常简单，只需一行配置:

```toml
[commit]
ai_attribution = "forbid"  # "ignore" 为默认值，表示不检查
```

设置为 `forbid` 后，Commit Check 会检查提交消息中是否包含已知 AI 工具的特征签名。如果检测到，提交将被拒绝。

> **注意**：此功能仅在提交消息中检测 AI 工具签名，不会影响其他类型的提交检查。

### 支持检测的 AI 工具

目前内置的签名库可以识别以下工具：

| 工具 | 匹配模式 |
|------|----------|
| Claude Code | `Co-authored-by: Claude`、`Assisted-by: Claude:<model>`、`🤖 Generated with Claude`、`Claude-Session:`、`Claude-Workflow:` |
| GitHub Copilot | `Co-authored-by: Copilot` |
| OpenAI Codex | `Co-authored-by: Codex` |
| Gemini | `Co-authored-by: Gemini` |
| Cursor | `Co-authored-by: Cursor` |
| Devin | `Co-authored-by: Devin` |
| Aider | `Co-authored-by: Aider`、`Co-authored-by: ... (aider)` |
| Windsurf | `Co-authored-by: Windsurf` |
| Tabby | `Co-authored-by: Tabby` |
| 通用 AI | `Assisted-by: <tool>:<model>` (Kernel 风格)、模型名称 (`claude-sonnet-4`、`gpt-4-turbo`) |

### 误报防护

实际使用中，有的外国人的名字就叫 Claude 或 Devin，如果不做区分就会出现误报。

Commit Check 的方案是：针对 Claude、Devin、Copilot 等模式，**锚定到已知的 noreply 邮箱地址**，不会匹配到人类的 co-author。普通用户如 `Co-authored-by: Jane Doe <jane@example.com>` 永远不会被标记。

### 多种集成方式

和所有 Commit Check 功能一样，AI 归属治理支持：

```bash
# CLI 方式
commit-check --ai-attribution=forbid

# 环境变量
export CCHK_AI_ATTRIBUTION=forbid

# TOML 配置
[commit]
ai_attribution = "forbid"

# Python API
from commit_check.api import validate_message
result = validate_message(message, ai_attribution="forbid")
```

详细的 PR 见 [commit-check/commit-check#456](https://github.com/commit-check/commit-check/pull/456)，欢迎 review 和反馈。

---

## 这段时间发布的亮点回顾

自 v2.5.0 以来，Commit Check 着实还发布了不少实用的功能，这里一并回顾一下。

### v2.9.0 — AI Agent 分支前缀默认支持

[Conventional Branch](https://www.conventionalbranch.org) v1.1.0 规范中新增了 AI agent 相关的分支前缀：`ai/`、`claude/`、`codex/`、`copilot/`、`cursor/`。

在 v2.9.0 中，这些前缀被直接加入到默认分支类型中，开箱即用，无需额外配置。

如果你用 Claude Code 或 Copilot 创建分支，分支名如 `claude/fix-bug-123` 现在默认就能通过检查。

### v2.8.0 — 自定义正则与 Python 3.9 告别

v2.8.0 有两个重要变化：

一是把用户呼声很高的自定义正则功能加了回来，通过 `message_pattern` 配置选项支持：

```toml
[commit]
message_pattern = "^(feat|fix|docs|chore|test)\\(.*\\):.*$"
```

二是正式放弃了对 Python 3.9 的支持，让项目可以使用更新的 Python 特性。

### v2.7.0 — 强制推送保护

这是一个很多团队呼声很高的功能。

Commit Check 现在可以通过 `pre-push` hook 检测强制推送 (`git push --force` / `git push -f`)，并在检测到时阻止推送。

原理是通过 `git merge-base --is-ancestor` 检查远程提交是否是本地提交的祖先。新分支推送、快进推送正常通过，只有真正的强制推送才会被拦截。

```toml
[push]
allow_force_push = false  # 默认 true，设为 false 后阻止强制推送
```

这个功能作为 `pre-commit` 的 `pre-push` hook 使用：

```yaml
repos:
  - repo: https://github.com/commit-check/commit-check
    rev: v2.7.0
    hooks:
      - id: check-no-force-push
        stages: [pre-push]
```

### v2.6.0 — 输出控制

很多用户在 CI 日志中觉得提交检查的 banner 太长了。v2.6.0 新增了两个 CLI 标志：

- `--no-banner`：去掉 ASCII 艺术 banner，保留详细错误信息
- `--compact`：每个失败检查只输出一行 `[FAIL]`，同时隐含 `--no-banner`

在 CI 日志或 pre-commit 输出中非常实用。

### v2.5.0 — 多个实用更新

这是 v2 系列中最重要的一个功能版本，包含三个重要更新：

**Co-author 绕过支持**

当 commit 的 co-author 匹配 `ignore_authors` 列表时，该提交可以跳过所有检查。特别适合 AI 辅助工作流：

```toml
[commit]
ignore_authors = ["dependabot[bot]", "renovate[bot]", "coderabbitai[bot]", "copilot[bot]"]
```

**组织级配置继承（inherit_from）**

团队现在可以共享一个中心化的基础配置：

```toml
# 每个仓库只需引用组织配置
inherit_from = "github:my-org/.github:cchk.toml"

[commit]
subject_max_length = 72  # 局部覆盖
```

支持 GitHub raw 文件、本地路径、HTTPS URL 多种来源。

**Git Config 作者验证修复**

之前只检查最新提交的作者信息，现在优先检查 `git config user.name / user.email`——也就是**下一次提交**会使用的身份。解决了开发者配置了错误的 user.name 但仍然能通过检查的问题。

---

## 结语

Commit Check 自 2022 年诞生至今，我最大的感受是 —— 它已经不仅仅是一个"检查 commit message 的工具"了。

它已经从原来的基本检查包括提交消息、分支命名、作者信息、签名验证，到后面的合并基线检查、强制推送保护，再到现在的 AI 归属治理，已逐渐成为一个覆盖代码提交全流程的合规检查框架。

这也是我最初没有想到的——用户的反馈和社区的需求，推动着它一步步走到今天。

如果你还没有用过 Commit Check，可以通过 pip 安装：

```bash
pip install commit-check
```

📍 项目地址：**github.com/commit-check/commit-check**

📄 更多详情：https://commit-check.github.io/commit-check/

最后欢迎大家在 GitHub 上 Star、提出问题和贡献代码。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
