---
title: 规则只写在 AGENTS.md 里，AI 照样违反：31 个热门项目一个月的提交
summary: |
  31 个热门开源项目在 AGENTS.md 或贡献指南里写了"提交里不要给 AI 署名"。一个月后，只写在文档里的 25 个项目中，有 20 个的主干上出现了违反这条规则的提交，一共 389 个；把规则写成 CI 检查的 4 个项目，一个都没有。这篇讲怎么查的，以及我为什么觉得 Everything as Code 在 AI 时代更重要了。
tags:
  - AI
  - DevOps
  - Commit-Check
authors:
  - shenxianpeng
date: 2026-11-14
---

11 月 7 日，JUnit 合并了 [#6254](https://github.com/junit-team/junit-framework/pull/6254)。这个 PR 在 [CONTRIBUTING.md](https://github.com/junit-team/junit-framework/blob/main/CONTRIBUTING.md) 里加了一节 "AI Usage"，同时加了一个 workflow。

同一份 AI 政策，被拆成了两种写法。"在 PR 描述里说明用了多少 AI"写在 CONTRIBUTING.md 里，靠维护者 review 的时候去看。"提交信息里不许有 AI 署名"写成了 [workflow](https://github.com/junit-team/junit-framework/blob/main/.github/workflows/_forbid-ai-attribution.yml)，每个 PR 都会自动检查：

```yaml
- uses: commit-check/commit-check-action@d68e05baf9511853193e2749f8a64bf2a221619a # v2.22.0
  env:
    CCHK_AI_ATTRIBUTION: forbid
  with:
    message-ai-attribution: true
    branch: false
```

先交代一下：[commit-check](https://github.com/commit-check/commit-check) 是我维护的项目，JUnit 用的就是它。所以看到这个 PR 我挺高兴。也正因为是自己的工具，下面的数据我只摆事实，结论你可以自己判断。

这些年我在工作里一直推 Everything as Code：构建、发布、环境、团队规范，能写成代码的都写成代码。以前的理由是可重复、可评审、可审计。现在我觉得还要加一条：写代码的越来越多是 AI，规则只写在文档里，AI 会读，但不一定照做。

这句话说起来容易，我想用数据验证一下。

## 怎么查的

- **样本**：2026 年 11 月 14 日，取 GitHub 上 star 数最多、最近一个月有推送的 1000 个仓库（不含 fork 和归档仓库，最少的也有 2.9 万 star）。
- **找规则**：下载每个仓库默认分支上的 `AGENTS.md`、`CLAUDE.md`、`.github/copilot-instructions.md` 和 `CONTRIBUTING.md`，找出明确写了"提交里不要给 AI 署名"的项目，比如"不要加 `Co-Authored-By: Claude`"。
- **确认规则当时就在**：回到 10 月 15 日那天的代码，确认这条规则那时候已经写进仓库了。
- **数违反**：统计 10 月 15 日到 11 月 14 日这 30 天里，主干上有多少提交仍然带着 AI 署名。只认最明确的几种：`Co-authored-by` 里是 Claude（`noreply@anthropic.com`）、Cursor（`cursoragent@cursor.com`）或 Copilot 的 noreply 邮箱，以及 Claude Code 的 "Generated with Claude Code" 页脚。
- **看有没有检查**：用 GitHub 代码搜索找这些项目里有没有在 CI 或 git hook 里检查这条规则的脚本，再逐个打开确认。

## 结果

1000 个仓库里，**507 个**有给 AI 读的规则文件（`AGENTS.md`、`CLAUDE.md` 或 `copilot-instructions.md`）。在大项目里，给 AI 写说明书已经是常规操作了。

其中 **31 个**在 10 月 15 日之前就写明了"提交里不要给 AI 署名"。30 天后：

| 规则写在哪 | 项目数 | 出现违反的项目 | 违反的提交 |
|---|---:|---:|---:|
| 只写在文档里 | 25 | 20 | 389 |
| 本地 git hook | 2 | 1 | 1 |
| CI 检查 | 4 | 0 | 0 |

只写在文档里的 25 个项目，有 20 个在一个月里被违反了，平均每个项目接近 20 个提交。违反最多的几个：

| 项目 | 规则原文（节选） | 30 天内违反的提交 |
|---|---|---:|
| [BerriAI/litellm](https://github.com/BerriAI/litellm/blob/main/AGENTS.md) | Do not add `Co-Authored-By: Claude` or any Claude attribution to commit messages. | 73 |
| [tldraw/tldraw](https://github.com/tldraw/tldraw/blob/main/AGENTS.md) | Do not include AI attribution in commits, PR descriptions, issues, docs… | 46 |
| [reactive-resume](https://github.com/reactive-resume/reactive-resume/blob/main/AGENTS.md) | Never add AI attribution, co-author trailers naming AI tools… | 41 |
| [HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading/blob/main/CONTRIBUTING.md) | Do NOT add `Co-Authored-By:` trailers or AI-assistant attribution lines… | 38 |
| [vercel/next.js](https://github.com/vercel/next.js/blob/canary/AGENTS.md) | Do NOT add "Generated with Claude Code" or co-author footers to commits or PRs | 34 |
| [webpack/webpack](https://github.com/webpack/webpack/blob/main/AGENTS.md) | no `Co-authored-by` trailers | 33 |
| [elastic/elasticsearch](https://github.com/elastic/elasticsearch/blob/main/AGENTS.md) | Do not add "Co-Authored-By" or any AI attribution trailers to commit messages, by any means… | 23 |

举一个 next.js 的例子，11 月 6 日合进主干的 [#101225](https://github.com/vercel/next.js/pull/101225)，提交信息最后一行是：

```text
Co-authored-by: Claude Code (kimi-k3) <noreply@anthropic.com>
```

而它的 `AGENTS.md` 里写着 "Do NOT add … co-author footers to commits or PRs"。

另一头，把规则写成 CI 检查的 4 个项目，这 30 天里一个违反都没有。它们的做法都很朴素：

- [moby/moby](https://github.com/moby/moby/blob/master/.github/scripts/check-agent-coauthors.js)：一个 JavaScript 脚本，PR 里任何一个提交用 `Co-authored-by` 给 AI 署名就失败。
- [nautilus_trader](https://github.com/nautechsystems/nautilus_trader/blob/develop/scripts/ci/check_commit_message.py)：一个 Python 脚本，用正则匹配 `Co-authored-by` 里的 anthropic、claude、codex、copilot、cursor 等名字。
- [floci](https://github.com/floci-io/floci/blob/main/.github/workflows/pr-hygiene.yml)：一个 workflow，注释里直接引用了 CONTRIBUTING.md 和 AGENTS.md 里的那句规则。
- [VoiceStudio](https://github.com/debpalash/VoiceStudio/blob/main/.github/scripts/agent_identities.py)：一份 AI agent 身份列表，CLA 检查和提交身份检查共用。

两个用本地 git hook 的项目，[FlClash](https://github.com/chen08209/FlClash/blob/main/tool/hooks/commit_msg.sh) 是 0，[OmniRoute](https://github.com/cheaper-inference/OmniRoute/blob/main/.husky/commit-msg) 漏了 1 个。本地 hook 要每个人自己装，装没装、有没有跳过，仓库管不到。

31 个项目每一个的结果在 [ai-attribution-rules-2026-11-14.csv](ai-attribution-rules-2026-11-14.csv) 里。

## 为什么写了还会违反

我没有逐个去查这 389 个提交是怎么进来的，所以下面只说我能确定的事。

AI 编码工具大多默认会往提交里加署名。我在 [7 月那篇文章](/zh-cn/posts/2026/commit-check-ai-attribution/) 里写过，Claude Code 默认会加 `Co-authored-by: Claude`，Copilot、Cursor、Devin 也各有各的标记。`AGENTS.md` 让它别加，相当于让它在每次提交时都记得违背自己的默认设置。

人这一侧也一样。维护者 review 代码时看的是 diff，很少会盯着提交信息的最后一行。规则只写在文档里，就要靠每一次 review 都想起来去检查。

[cozystack](https://github.com/cozystack/cozystack/blob/main/hack/check-commit-trailers.sh) 在他们的检查脚本开头写了一句话，我很认同：

> All three are review blockers decided by the text alone, which is exactly the kind of thing a human should not be spending a review round on.

只看文本就能判断对错的规则，就不该占用人的 review。他们在把规则写成脚本之前，先拿它跑了一遍主干上当时全部的 6062 个提交，1300 个不合格。

## 规则有两层

回头看这些数据，我觉得给 AI 的规则其实有两层。

第一层是让 AI 知道规则，也就是 `AGENTS.md` 这类文件。1000 个项目里已经有一半做了，这一层的价值很明显：没有它，AI 连规则是什么都不知道。

第二层是让 AI 违反不了，也就是写成在提交或 CI 里执行的检查。31 个项目里只有 4 个做到了 CI 这一步，这 4 个一个月里都是零违反。只写在文档里的 25 个项目中也有 5 个是零，样本不大，原因我说不清。

这也是我理解的 Everything as Code 在 AI 时代多出来的那条理由：**写成文档的规则，AI 会读到；写成检查的规则，AI 才绕不过去。**

AI 署名只是最容易测的一条规则。提交信息格式、分支命名、哪些目录不能改、哪些依赖不能加，只要能只看文本或 diff 就判断对错，都可以这样处理。

## 局限

1. **只测了一条规则。** AI 署名最容易被机器判断，其他规则的情况未必一样。
2. **违反数是下限。** 我只认了三种邮箱和一种页脚，其他工具的署名写法没算进去。
3. **"有没有检查"可能漏判。** GitHub 代码搜索不是完整的，可能有项目有检查但我没搜到。不过只写在文档里的 25 个项目里，20 个确实出现了违反，有没有检查都没拦住。
4. **规则冲突。** 有的项目在不同文件里写法不完全一致，比如 Homebrew 的 CONTRIBUTING.md 允许和人类作者一起给 AI 署名，AGENTS.md 却要求 agent 不要加。我按"至少一个文件明确禁止"来算。
5. **样本偏大项目。** 1000 个仓库最少也有 2.9 万 star，不代表一般项目。

## 今天能做的一件事

翻一下你们团队的 `AGENTS.md`、贡献指南或者 wiki，找一条"只看文本就能判断对错"的规则，把它写成检查，放进 CI。

如果这条规则正好是 AI 署名，commit-check 一行配置就能做；不想引入依赖的话，像 moby 那样自己写一个一百多行的脚本也完全可以。只要它在每次提交时都会跑就行。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
