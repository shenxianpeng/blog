---
title: RepoKeeper：我给开源仓库做了一个会干活的维护助手
summary: |
  RepoKeeper 不是代码补全工具，而是一个面向开源维护流程的 GitHub 助手：它可以根据 Issue 创建修复 PR，巡检依赖和 CI，监控社区反馈，并把值得跟进的讨论整理成Issue。
tags:
  - RepoKeeper
  - AI
  - Open Source
authors:
  - shenxianpeng
date: 2026-05-05
---

五一假期有快一周没更新文章了。虽然没有更新，但休假期间我还是把电脑带上了——因为我一直在做一个新项目：[RepoKeeper](https://github.com/shenxianpeng/repokeeper)。

它的定位很具体：**帮开源维护者处理仓库里的日常杂活。**

我做这个项目的动机其实很简单。在 AI agent 爆发之后，我维护的开源仓库从十几个迅速涨到了三十多个。cpp-linter 有 9 个，commit-check 新增 3 个，conventional-branch 2 个，devops-maturity 新增 2 个，mkdocs-ng 从零起步新增 5 个，加上我个人的一些项目也陆续增长了近 10 个。以前我还能逐个仓库照看，现在即使有 AI 帮着写代码，每天能照顾到的数量也非常有限，更别说去调查用户反馈、发展新需求了。

我需要的不只是一个能帮忙写代码的工具——我需要一个真正能**代替我巡视仓库、帮我发现问题和机会**的助手。Copilot 写代码确实不错，但它贵，而且让它定期分析社区反馈、自动创建 issue 这类事情，需要额外搭建 workflow，继续烧 token 也不太划算。

RepoKeeper 就是为这个目的做的：它不只是写代码，还加上了巡检和社区反馈的雷达能力，并且你可以自选模型——比如 DeepSeek 比 Copilot 便宜太多，用它来处理日常维护工作再合适不过了。

---

## 它到底能做什么？

RepoKeeper 现在主要做三类事：

1. 根据 Issue 自动实现改动，并创建 PR；
2. 定期巡检仓库健康状态——依赖是否过期、CI 为什么挂了、哪些 Issue 放太久了；
3. 监控社区反馈，把值得跟进的讨论整理成 GitHub Issue。

这三件事对应 RepoKeeper 的三个模块：Implementation Agent、Daily Patrol、Community Radar。它们背后共享一份 `repokeeper.yml` 配置文件，用来描述你的维护风格和偏好。

---

## 1. 从 Issue 到 PR

这是 RepoKeeper 最直接的能力。

当某个 Issue 描述清楚了，你给它打上 `agent-todo` 标签，或者在 Issue 下评论 `@repokeeper go`，仓库的 GitHub Actions workflow 就会被触发。Agent 启动后会做这几步：

1. 读取 Issue 的标题、正文和最近评论；
2. 收集仓库里相关的源文件作为上下文；
3. 调用 LLM 生成修改计划；
4. 按计划修改代码或文档，写入文件；
5. 运行验证命令（linter、测试等）；
6. 如果验证通过，推送一个 `repokeeper/...` 分支；
7. 创建 Pull Request，并在原 Issue 下留言。

这个流程听起来和 Copilot 做的差不多：都是让 LLM 帮你写代码。但有几个关键区别：

- **你可以用更便宜的模型。** 比如 DeepSeek，价格仅为 GPT-4o 的几十分之一，尤其适合这类"修修补补"的任务。Copilot 六月份还要涨价，能省则省。
- **它的定位更偏"自动化维护流程"，而不是"代码补全"。** 未来我打算让它接入更多模型，支持 GitLab、Bitbucket，甚至本地 CLI 触发。

---

## 2. 每天巡检仓库

第二个模块叫 Daily Patrol。它做的事更像"定时帮你把仓库扫一遍"，把需要留意的地方列出来，甚至直接修。

**依赖是否过期。** Patrol 会扫描项目中的依赖文件，目前覆盖：

- Python：`requirements.txt`、`pyproject.toml`、`Pipfile`
- Node.js：`package.json`、`yarn.lock`
- Go：`go.mod`
- Rust：`Cargo.toml`
- Ruby：`Gemfile`
- PHP：`composer.json`
- Maven：`pom.xml`
- Gradle：`build.gradle`、`build.gradle.kts`

它会按严重程度整理过期的依赖，并可以直接创建一个依赖升级的 PR。和 Dependabot 不同的是，Patrol 不只是在表格里告诉你"这个依赖过期了"，而是尝试分析过期依赖可能带来的风险，并给出修复建议。不过要坦诚地说，自动安全改写 lock file 这块还在完善中，目前主要做的是报告候选项和创建 PR 建议。

**CI 为什么失败。** Patrol 会读取最近失败的 GitHub Actions 运行记录，拿到真实的 job 和 step 信息，用 AI 来诊断原因并给出修复建议。如果判断这个问题可以自动修——比如 action 版本太旧、路径配错了、某个环境变量没设——它会读取失败的 workflow 文件，生成修复，直接创建一个 CI 修复 PR。很多 CI 红叉不是复杂问题，而是这些小坑，Patrol 先给一版可 review 的修复，比你从日志里一点点排查要省心。

**哪些 Issue 放太久了。** Daily Patrol 也会找出长期没有更新的 Issue，默认阈值是 90 天。它会给出摘要和建议动作——关闭、ping 一下、继续推进，或者忽略。

最后，Patrol 会生成一个健康分数（0-100）和一份 Markdown 摘要，适合放到 GitHub Actions summary、Issue 或通知里。

---

## 3. 监控社区反馈，自动整理成 Issue

第三个模块是 Community Radar。

它可以扫描 GitHub Issues 和 Discussions，查找你关心的关键词，比如 `bug`、`crash`、`security`、`performance`。匹配到内容后，Radar 会用 AI 判断这是 bug 报告、feature request、普通问题，还是纯噪音。

如果开启了 `auto_create_issue`，它会为值得跟进的反馈自动创建新的 GitHub Issue。

几个设计细节值得提一下：

- 新 Issue 会链接回原始讨论，保留来源；
- 自动打上 `repokeeper-radar` 标签，方便筛选；
- 如果下一次扫描到同一个来源，不会重复创建 Issue，而是在已有 Issue 下追加一条活动评论；
- 可以通过 Email、Telegram 或 WeChat 通知你。

这解决了一个容易被忽视的开源维护痛点：用户有时候不会跑到你的仓库提 Issue，而是在他们自己的项目里讨论问题。Radar 的作用，就是把散落各处的"值得处理的信号"变成一个个可以排队、可以分配、可以处理的 GitHub Issue。

---

## 4. 用配置文件写下你的维护习惯

RepoKeeper 不是每个仓库都按同一种方式工作。你可以用 `repokeeper.yml` 写下项目偏好：

```yaml
maintainer: shenxianpeng

style:
  testing: pytest
  linting: true

agent:
  model: deepseek-chat
  max_context_files: 40
  skip_keywords:
    - "needs design"
    - "breaking change"
    - "security audit"
  verify_commands:
    - ruff check .
    - pytest tests

pr:
  max_files_per_pr: 10
  min_tests: true
  review_required: true

radar:
  enabled: true
  keywords:
    - bug
    - crash
    - performance
  auto_create_issue: true
```

这份配置决定了 RepoKeeper 怎么读项目、怎么验证改动、哪些问题跳过、PR 最多能改多少文件、通知发到哪里。

---

## 怎么接入？

最小接入方式很简单。

安装：

```bash
pip install repokeeper
```

初始化一个最小配置（仅 Implementation Agent workflow）：

```bash
repokeeper init --minimal
```

或者一次性生成全部三个模块的 workflow：

```bash
repokeeper init --all-workflows
```

推送前，还可以用 `doctor` 命令检查一遍环境：

```bash
repokeeper doctor --repo owner/repo
```

它会检查 profile 配置是否合法、workflow 触发条件和权限是否齐全、GitHub token 和 LLM API key 是否配好、仓库名称是否正确等常见问题。

确认无误后，在 GitHub Actions Secrets 里配置模型 key，比如 `DEEPSEEK_API_KEY`，就可以用了。

完整资料：

* GitHub：<https://github.com/shenxianpeng/repokeeper>
* 文档：<https://shenxianpeng.github.io/repokeeper/>
* PyPI：<https://pypi.org/project/repokeeper/>

---

## 安全边界

这类工具最容易被问到的问题是：它会不会乱改我的仓库？

RepoKeeper 的默认设计是：**创建 PR，不自动合并。**

默认 workflow 需要的权限是：

```yaml
permissions:
  contents: write
  issues: write
  pull-requests: write
```

这些权限只用来推送分支、评论 Issue、创建 PR。最终是否合并，仍然由你决定。

除此之外，还有几道默认的安全防线：

- Agent 生成的分支统一以 `repokeeper/` 开头；
- 单次 PR 最多修改的文件数可以通过 `pr.max_files_per_pr` 限制；
- 验证命令（linter、测试）不过不会创建 PR；
- `.github/workflows/` 目录被硬编码保护，Agent 无法修改自己的 workflow 扩权；
- 可以通过 `skip_keywords` 让 Agent 自动跳过涉及安全、架构、破坏性变更的 Issue。

这套设计的目标很明确：在发挥 AI 助手作用的同时，最大程度降低它可能带来的风险。

---

## 当前状态

RepoKeeper 当前最新版本是 `v0.7.0`，发布于 2026 年 5 月 5 日。

项目用 Python 编写，支持 Python 3.10 到 3.14，MIT License 开源。模型方面支持 DeepSeek（`deepseek-chat` / `deepseek-reasoner`）、OpenAI 兼容接口（包括 GPT-4o），以及 Anthropic Claude。每次 LLM 调用都会估算 token 成本，你也可以通过环境变量自定义不同模型的计费价格。

如果你维护开源项目，尤其是有一定社区反馈量、或者想定期巡检仓库健康状况的，不妨试试 RepoKeeper。

项目地址：

https://github.com/shenxianpeng/repokeeper
