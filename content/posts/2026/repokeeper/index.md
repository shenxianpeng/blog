---
title: RepoKeeper 十天一百次提交之后，它已经能自己开发自己了
summary: |
  过去十天，我给 RepoKeeper 提交了一百多次代码，从一个概念验证跑到了 v1.2.0。它现在有六个模块，两个后端，支持 DeepSeek/OpenAI/Claude，还能用自己来开发自己——这篇文章讲讲它到底进化成了什么。
tags:
  - RepoKeeper
  - AI
  - Open Source
authors:
  - shenxianpeng
date: 2026-05-10
---

大家好，我是沈工。

五一之后我安静了一周多 —— 不是因为没东西可写，而是因为在写代码，写到没时间写文章。

那个让我停不下来的项目，就是 [RepoKeeper](https://github.com/shenxianpeng/repokeeper)。

目前已经迭代到了 v1.2.0，中间提交了一百多次。模块从最初的三个扩展到了六个，从「能用」变成了「能用自己来开发自己」。

这篇文章，就跟大家聊聊 RepoKeeper 现在到底长什么样，以及它为什么值得你试试看。

## 为什么要做 RepoKeeper

它的定位很具体：**帮开源维护者处理仓库里的日常杂活。**

我做这个项目的动机其实很简单。在 AI agent 爆发之后，我维护的开源仓库从十几个迅速涨到了三十多个。cpp-linter 有 9 个，commit-check 新增 3 个，conventional-branch 2 个，devops-maturity 新增 2 个，mkdocs-ng 从零起步新增 5 个，加上我个人的一些项目也陆续增长了近 10 个。

现在即使有 AI 帮着写代码，每天能照顾到的数量也非常有限，更别说去调查用户反馈、发展新需求了。

我需要的不只是一个能帮忙写代码的工具——还需要一个真正能**代替我巡视仓库、帮我发现问题和机会**的助手。

Copilot 写代码确实不错，但它贵，另外让它定期分析社区反馈、自动创建 issue 这类事情，需要额外搭建 workflow，继续烧 token 也不太划算。

RepoKeeper 就是为这个目的做的：它不只是写代码，还加上了巡检和社区反馈的雷达能力，并且你可以自选模型——比如 DeepSeek 比 Copilot 便宜太多，用它来处理日常维护工作再合适不过了。

---

## 它跟 Copilot、CodeRabbit 有什么区别？

这是个绕不开的问题。市面上已经有 GitHub Copilot 写代码，有 CodeRabbit 和 PR-Agent 做代码审查。为什么还要一个 RepoKeeper？

我的回答是：**Copilot 陪你写代码，CodeRabbit 帮你审 PR，RepoKeeper 替你管仓库。** 这三件事不是竞争关系。

具体看看：

| | Copilot Code Review | CodeRabbit | PR-Agent (Qodo) | **RepoKeeper** |
|---|---|---|---|---|
| Issue → PR | ❌ | ❌ | ❌ | ✅ 两种后端 |
| 对话式 PR 修复 | ❌ | ❌ | ❌ | ✅ 推到同一分支 |
| 代码审查 | ✅ 仅 PR | ✅ 逐行 | ✅ /review | ✅ 逐行 + 严重程度 |
| PR 描述生成 | ❌ | ✅ | ✅ /describe | ✅ /describe |
| 自动打标签 | ❌ | ✅ | ✅ | ✅ 15 类别 + diff 感知 |
| 依赖扫描 | ❌ | ❌ | ❌ | ✅ 8 个生态 |
| CI 诊断 + 修复 | ❌ | ❌ | ❌ | ✅ 自动修复 PR |
| 社区监控 | ❌ | ❌ | ❌ | ✅ Radar（Issue + Discussion） |
| 定时巡检 | ❌ | ❌ | ❌ | ✅ 每日 Patrol |
| 多模型 | 仅 GitHub 模型 | 多种 | 多种 | DeepSeek / OpenAI / Claude |
| 后端选择 | 单一 | 单一 | 单一 | Native + Pi agent loop |
| 成本 | 需订阅 | 公共仓库免费 | 公共仓库免费 | **免费（用自己的 key）** |
| 自部署 | ❌ | ❌ | ✅ | ✅ 5 个 composite action |

RepoKeeper 做的事情比它们都宽。Copilot 在编辑器里帮你写代码，CodeRabbit 在 PR 里点评代码，这些都很重要——但它们不管 Issue 怎么变成 PR，不管 CI 为什么天天挂，不管社区在 Discussions 里提了什么问题。

这些恰好是开源维护者每天花最多时间的事情，也是 RepoKeeper 的定位。

---

## 已经能自己开发自己了

这可能是整个项目最让我兴奋的地方：**RepoKeeper 现在已经到了「鸡生蛋、蛋生鸡」的状态。** 我可以用它来给 RepoKeeper 自己提 PR、修 bug、打标签、做代码审查。

具体来说，RepoKeeper 仓库里已经跑着五条 workflow：

1. **Agent** —— 打 `agent-todo` 标签或评论 `/repokeeper go`，它自己写代码、自己验证、自己提 PR。
2. **Radar** —— 监控社区反馈，扫描 Issues 和 Discussions 里的关键词，AI 分类后自动创建 Issue。
3. **Patrol** —— 每天早上八点巡检依赖、CI 状态、过期 Issue，生成健康分数。
4. **Labeler** —— 新 Issue 和新 PR 自动分类打标签。
5. **Review** —— PR 提交后自动做逐行代码审查，新 commit 推送后自动重新审。

一个开源项目，自己的 workflow 里跑着自己的 action 来维护自己——这件事本身是对 RepoKeeper 稳定性最好的证明。

---

## 六个模块分别干什么

RepoKeeper 现在有六个模块，每个都可以独立启用或关闭。

### 1. Implementation Agent（从 Issue 到 PR）

这是最核心的能力。有两种后端可以选：

- **Native 后端**：单次 LLM 调用，生成结构化 JSON 计划，执行修改，验证通过后提 PR。一次不到一分钱，适合简单、单文件的改动。
- **Pi 后端**：基于 [pi](https://github.com/earendil-works/pi) 的自主 agent loop。它会自己读文件、改代码、跑测试、看结果、反复迭代，直到任务完成。适合多文件重构、跨模块改动。一次几分钱到几毛钱。

两种后端共享同一套工作流：读取 Issue → 收集代码上下文 → 生成修改计划 → 执行 → 跑 lint 和测试 → 验证通过 → 推送分支 → 创建 PR。

Agent 还内置了几道安全防线：
- 不会改 `.github/workflows/` 目录（防止扩权）
- 单次最多改文件数可配置（默认 15 个）
- 验证命令不过就不会创建 PR
- 命中 `skip_keywords` 的 Issue 自动跳过

### 2. PR Fix Mode（对话式修复）

这是最近加的一个能力，解决一个很实际的问题：Agent 提的 PR 不够好，怎么办？

以前你得关掉 PR、修改 Issue 描述、重新跑一遍。现在只需要在 PR 下面评论 `/repokeeper go`，把反馈写清楚，Agent 就会读取整个 PR 的 diff 和评论历史，在同一个分支上继续改。

你可以反复来——每一轮它都带着之前的对话历史，不会重蹈覆辙。

### 3. Code Review Agent（逐行审查）

这个模块做的不只是在 PR 下留一条评论。

它会：
- 读取 PR 的完整 diff
- 对照你的 Maintainer Profile 检查代码风格、技术栈偏好、测试覆盖
- **在具体代码行上留下 inline comment**，标注严重程度（🔴 Critical / 🟠 Major / 🟡 Minor / ⚪ Nit）
- 带有 suggestion block，可以一键应用
- 新 commit 推送后自动 dismiss 旧 review、重新审

另外还支持 `/repokeeper describe`，从 diff 自动生成结构化的 PR 描述（Summary / Changes / Testing / Screenshots）。

### 4. Auto-Labeler（自动打标签）

标签看起来是个小事，但仓库里 Issue 和 PR 多了之后，分类就变成了体力活。

Labeler 的特别之处在于：
- 它会先读你仓库里已经有的标签，匹配命名习惯和颜色风格
- 只在没有合适标签时才创建新标签
- 对 PR 做 **diff 感知的分类**：一个改了两个 `.py` 文件和一个 `ci.yml` 的 PR，会优先归为 feature 而不是 CI
- 支持 15 个类别：bug、feature、question、documentation、performance、security、dependencies、duplicate、wontfix、good first issue、help wanted、refactoring、testing、ci_cd、noise

### 5. Daily Patrol（每日巡检）

每天早上八点（可配），Patrol 会把仓库扫一遍：

**依赖是否过期。** 覆盖 8 个生态：pip、npm、Go、Cargo、Bundler、Composer、Maven、Gradle。不只是列出过期依赖，还会分析风险并给出修复建议。

**CI 为什么失败。** 读 GitHub Actions 的真实运行记录，拿到 job 和 step 的日志，用 AI 诊断原因。如果判断可以自动修（action 版本太旧、路径配错、环境变量缺失），它会读取 workflow 文件，直接创建一个 CI 修复 PR。

**哪些 Issue 放太久了。** 默认阈值 90 天，给出建议动作。

最后输出一个 0-100 的健康分数和 Markdown 摘要。

### 6. Community Radar（社区雷达）

扫描 GitHub Issues 和 Discussions 里的关键词（`bug`、`crash`、`security`、`performance` 等），AI 判断是不是值得处理的信号。

如果开启了 `auto_create_issue`，它会：
- 自动创建 Issue，链接回原始讨论
- 打上 `repokeeper-radar` 标签
- 下次扫描到同一来源时不会重复创建，而是在已有 Issue 下追加评论
- 支持 Email、Telegram、WeChat 通知

---

## 一份配置管所有

六个模块共享一份 `repokeeper.yml`：

```yaml
maintainer: shenxianpeng

style:
  code_style: |
    Follow existing code style exactly.
    Use type hints in Python.
  testing: pytest
  linting: true

agent:
  model: deepseek-chat
  backend: pi          # native 或 pi
  skip_keywords:
    - "needs design"
    - "breaking change"
  verify_commands:
    - ruff check .
    - pytest tests

pr:
  max_files_per_pr: 15
  min_tests: true
  review_required: true

radar:
  enabled: true
  keywords: [bug, crash, security, performance]
  auto_create_issue: false

patrol:
  enabled: true
  schedule: "0 8 * * 1-5"
  auto_upgrade_deps: true
  ci_auto_fix: true

labeler:
  enabled: true
  mode: add

review:
  incremental: true
  describe_on_open: true
```

写一次，所有模块都按你的偏好来。

---

## 接入：一分钟就能跑起来

最小接入只需要两步。

**1. 复制 workflow 文件到你的仓库：**

```bash
pip install repokeeper
repokeeper init --all-workflows   # 所有 5 个模块
# 或者
repokeeper init --minimal         # 只要 Agent 模块
```

**2. 推送前检查一遍：**

```bash
repokeeper doctor --repo yourname/yourrepo
```

`doctor` 会检查 profile 配置、workflow 触发条件和权限、GitHub token、LLM key、仓库名称等所有常见问题。确认无误后，在 GitHub Actions Secrets 里配好 `DEEPSEEK_API_KEY`，push workflow 就行了。

或者，直接把下面的 prompt 丢给任何 AI coding agent：

> Add RepoKeeper to this repository. Create `.github/workflows/repokeeper.yml` that uses the `shenxianpeng/repokeeper/agent@v1` composite action — trigger on issue comments (`/repokeeper go`) and labels (`agent-todo`). Pass `DEEPSEEK_API_KEY` as the `llm_api_key` input. Then tell me to add a `DEEPSEEK_API_KEY` secret in GitHub Actions settings.

---

## 成本和安全性

**成本方面**，用 DeepSeek 的话，一次 Agent 实现不到一分钱到几毛钱（取决于用 Native 还是 Pi），一次 Patrol 巡检大约几分钱，一次 Review 大约几分钱。跟你付给 Copilot 的订阅费比起来，基本可以忽略。

**安全方面**，RepoKeeper 的默认设计是：创建 PR，不自动合并。需要的权限只有 `contents: write`、`issues: write`、`pull-requests: write`。Agent 生成的分支统一以 `repokeeper/` 开头，`.github/workflows/` 目录被硬编码保护，验证命令不过不会创建 PR。

最终是否合并，仍然由你决定。

---

## 最后

RepoKeeper 现在离我理想中的「开源维护助手」越来越近了。

它可以监控社区、巡检仓库、写代码、审代码、打标签、修 CI——而且成本极低。最让我满意的是，它已经在用它自己的能力来维护自己了。每次我在 RepoKeeper 仓库里打一个 `agent-todo` 标签，看着它自己读代码、自己写改动、自己跑测试、自己提 PR，那种感觉确实不太一样。

如果你也在维护开源项目，尤其是仓库多了之后开始顾不过来，不妨试试 RepoKeeper。

- GitHub：https://github.com/shenxianpeng/repokeeper
- 文档：https://shenxianpeng.github.io/repokeeper/
- PyPI：https://pypi.org/project/repokeeper/

遇到问题去 GitHub 提 Issue，或者直接让 RepoKeeper 自己修。

老司机们，我们下期见～

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
