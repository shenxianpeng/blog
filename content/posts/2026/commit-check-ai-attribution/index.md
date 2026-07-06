---
title: 你的仓库里，哪些代码是 AI 写的？现在有工具能管住了
summary: |
  Claude Code 等 AI 工具默认会往提交里塞签名，很多人根本没注意到。Commit Check v2.11.0 引入 AI 归属治理，一行配置即可在 CI 层面拒绝带 AI 签名的提交。本文也聊聊这个功能的边界，以及这半年 Commit Check 解决的其他几个痛点。
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

先请你做个小实验：打开团队的仓库，跑一下这条命令——

```bash
git log --grep="Co-authored-by: Claude"
```

如果你们团队有人在用 Claude Code，结果可能会让你有点惊讶。

因为 Claude Code 默认就会往提交里塞 `Co-authored-by: Claude` 这样的签名，Copilot、Cursor、Devin 这些工具也各有各的标记方式。提交历史里已经不知不觉混进了一堆 AI 签名。

有的团队无所谓，有的团队明确不希望这些出现在提交历史里——尤其是对代码来源有合规要求的企业，以及不想被 AI 提交淹没的开源项目。

这个问题社区其实已经吵起来了。Python 社区在 [discuss.python.org](https://discuss.python.org/t/should-claude-codes-usage-be-described-in-the-code-docs-somewhere/107969) 上专门讨论过，Linux Kernel 干脆标准化了 `Assisted-by:` 格式，VS Code 也有 [issue](https://github.com/microsoft/vscode/issues/313962) 在讨论要不要用它替代 `Co-authored-by`。

大家都在讨论"该怎么标注"，但我发现一个空白：**没有工具能在 CI 层面把这个策略真正执行起来。** 讨论归讨论，落不了地。

Commit Check 本来就是干 commit 检查这行的，这事它不做谁做？于是就有了刚发布的 v2.11.0——AI 归属治理（AI Attribution Governance）。

## 一行配置的事

```toml
[commit]
ai_attribution = "forbid"
```

加上这行，凡是提交消息里带有已知 AI 工具签名的提交，直接拒绝。默认值是 `ignore`，不影响老用户。

目前内置的签名库覆盖了 Claude Code、Copilot、Codex、Gemini、Cursor、Devin、Aider、Windsurf 等主流工具，也认 Kernel 风格的 `Assisted-by: <tool>:<model>`，甚至提交消息里直接出现 `claude-sonnet-4`、`gpt-4-turbo` 这种模型名也能识别。

## 但有个坑：真有人就叫 Claude

做这个功能时我最担心的是误报。Claude、Devin 这些都是正常的英文人名，总不能同事就叫 Devin，一提交就被拒吧。

所以对这类模式，Commit Check 不是单纯匹配名字，而是**锚定到 AI 工具已知的 noreply 邮箱**。`Co-authored-by: Jane Doe <jane@example.com>` 这种真人 co-author 永远不会被误伤。

想试的话，CLI、环境变量、TOML 配置、Python API 都支持，用法和其他检查项完全一致。详细实现见 [commit-check/commit-check#456](https://github.com/commit-check/commit-check/pull/456)，欢迎来拍砖。

## 先泼盆冷水：这个功能防不了刻意作弊

必须说清楚一点：`ai_attribution = "forbid"` 检查的是提交消息里的签名，**它管得住默认行为，管不住存心绕过的人**。

比如开发者完全可以跟 AI 说一句"提交的时候不要加任何 AI 相关的签名"，或者让 AI 只改代码、自己手动提交——这样提交消息里干干净净，Commit Check 自然什么也查不出来。代码是不是 AI 写的，光看 commit message 是永远无法百分百判断的。

那这个功能还有什么意义？

它和 commit message 规范、分支命名规范是同一类东西——**这些检查从来防不住存心捣乱的人（`--no-verify` 一加全绕过了），防的是"没人说清楚规则"和"顺手就那么提了"**。

实际场景里，绝大多数 AI 签名不是开发者主动加的，而是工具的默认行为。团队如果没有明确策略，提交历史就会不知不觉被污染。有了 CI 层面的强制检查，至少做到两件事：

* 一是**把团队的策略显式化**——"我们不接受 AI 签名"这句话从口头约定变成了一条会拒绝提交的规则；
* 二是**拦住所有无心之失**。至于刻意隐瞒的那部分，那是工程文化和 code review 的事，不是一个 lint 工具该许诺的。

工具的边界说清楚，用起来才不会失望。

## 顺便聊聊这半年加的其他东西

距离上次写 Commit Check 已经大半年了，这期间发的几个功能，我按"解决什么问题"给大家过一遍，看看有没有戳中你的。

**同事一个 force push，把你的提交推没了。** 这可能是 Git 协作里最气人的事故之一。现在 Commit Check 提供了 `check-no-force-push` 这个 pre-push hook，原理是用 `git merge-base --is-ancestor` 判断远程提交是不是本地提交的祖先——新分支和快进推送正常放行，只拦真正的强制推送。装上之后，手快的同事想 `push -f` 也推不出去。

```yaml
repos:
  - repo: https://github.com/commit-check/commit-check
    rev: v2.11.0
    hooks:
      - id: check-no-force-push
        stages: [pre-push]
```

**用 Claude Code 建的分支过不了分支名检查。** Conventional Branch v1.1.0 新增了 AI agent 分支前缀，Commit Check 也跟进了：`claude/fix-bug-123`、`copilot/xxx` 这类分支名现在默认就能通过，不用改配置。

**dependabot 的提交老是被规则卡住。** 配一下 `ignore_authors`，把 `dependabot[bot]`、`renovate[bot]` 这些机器人加进去，它们的提交就跳过检查。AI 辅助工作流里同样好用。

```toml
[commit]
ignore_authors = ["dependabot[bot]", "renovate[bot]", "coderabbitai[bot]"]
```

**几十个仓库，每个都要拷一份配置。** 现在支持 `inherit_from`，组织里放一份中心配置，每个仓库一行引用，需要的地方再局部覆盖。想在团队里统一提交规范的，这个功能就是为你准备的。

```toml
inherit_from = "github:my-org/.github:cchk.toml"

[commit]
subject_max_length = 72  # 局部覆盖
```

**嫌 CI 日志里那个 ASCII banner 太占地方。** 加 `--compact`，每个失败检查只输出一行 `[FAIL]`。这是用户反馈最多的小需求之一，改完之后 CI 日志清爽多了。

另外还有自定义正则 `message_pattern` 的回归（呼声很高）、作者信息检查改为优先读 `git config`（之前配错 user.name 居然能混过去）等等，就不一一展开了，感兴趣的可以去 Release Notes 里翻。

## 写在最后

Commit Check 是 2022 年开始写的，最初真的就只是个"检查 commit message 的工具"。

现在回头看，它管的事已经越来越多：提交消息、分支命名、作者身份、签名、合并基线、强制推送，再到现在的 AI 归属——基本覆盖了代码提交这个环节的全流程合规检查。使用方式上，CLI、pre-commit hook、Python API、GitHub Action 也都齐了，想怎么接入都行。

这些检查背后其实是同一个原则：**policy as code**。规则本身就是代码，放在仓库里，和代码一起被版本化、被审查、被讨论。团队的提交规范不再是口头约定，而是一条条可以被执行的规则。

说实话这些不是一次性规划出来的，是四年来用户的反馈和使用场景的变化，推着 Commit Check 一点点演进到今天。

如果你的团队也在为提交规范、或者"AI 提交要不要管"的问题头疼，可以试试：

```bash
pip install commit-check
```

📍 项目地址：**github.com/commit-check/commit-check**

📄 更多详情：https://commit-check.github.io/commit-check/

觉得有用的话，欢迎 Star，也欢迎提 Issue 告诉我你的团队还有什么想治理的痛点。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
