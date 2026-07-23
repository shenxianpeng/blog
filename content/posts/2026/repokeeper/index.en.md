---
title: RepoKeeper After a hundred commits in ten days, it can now develop itself
summary: |
  Over the past ten days, I've made over a hundred commits to RepoKeeper, evolving it from a proof-of-concept to v1.2.0. It now boasts six modules, two backends, supports DeepSeek/OpenAI/Claude, and can even develop itself—this post will explain what it has evolved into.
tags:
  - RepoKeeper
  - AI
  - Open Source
authors:
  - shenxianpeng
date: 2026-05-10
---

After May Day, I've been quiet for over a week—not because I had nothing to write, but because I was coding so intensely that I had no time for articles.

The project that kept me going is [RepoKeeper](https://github.com/shenxianpeng/repokeeper).

It has now iterated to v1.2.0, with over a hundred commits in between. Modules have expanded from the initial three to six, transforming from "usable" to "capable of developing itself."

In this article, I'll talk about what RepoKeeper looks like now and why it's worth checking out.

## Why I Built RepoKeeper

Its positioning is very specific: **helping open-source maintainers handle daily chores in their repositories.**

My motivation for this project is actually quite simple. After the explosion of AI agents, the number of open-source repositories I maintained rapidly grew from a dozen to over thirty. cpp-linter has 9, commit-check added 3, conventional-branch 2, devops-maturity added 2, mkdocs-ng started from scratch and added 5, plus nearly 10 more from my personal projects.

Even with AI helping to write code, the number of repositories I can attend to daily is very limited, let alone investigating user feedback and developing new features.

What I need is not just a tool that helps write code—but a true assistant that can **replace me in patrolling repositories and helping me discover problems and opportunities.**

Copilot is good for writing code, but it's expensive. Furthermore, having it regularly analyze community feedback and automatically create issues requires setting up additional workflows, and continuing to burn tokens isn't very cost-effective.

RepoKeeper was built for this purpose: it not only writes code but also adds patrol and community feedback radar capabilities. You can choose your own model—for example, DeepSeek is much cheaper than Copilot, making it perfect for handling daily maintenance tasks.

---

## What's the Difference Between It, Copilot, and CodeRabbit?

This is an unavoidable question. There's already GitHub Copilot for writing code, and CodeRabbit and PR-Agent for code review. Why do we need another RepoKeeper?

My answer is: **Copilot accompanies you in writing code, CodeRabbit helps you review PRs, and RepoKeeper manages your repository.** These three are not in competition.

Let's take a closer look:

| | Copilot Code Review | CodeRabbit | PR-Agent (Qodo) | **RepoKeeper** |
|---|---|---|---|---|
| Issue → PR | ❌ | ❌ | ❌ | ✅ Two backends |
| Conversational PR fix | ❌ | ❌ | ❌ | ✅ Pushes to the same branch |
| Code Review | ✅ PR only | ✅ Line-by-line | ✅ /review | ✅ Line-by-line + severity |
| PR description generation | ❌ | ✅ | ✅ /describe | ✅ /describe |
| Automatic labeling | ❌ | ✅ | ✅ | ✅ 15 categories + diff-aware |
| Dependency scanning | ❌ | ❌ | ❌ | ✅ 8 ecosystems |
| CI diagnosis + fix | ❌ | ❌ | ❌ | ✅ Automatically fixes PR |
| Community monitoring | ❌ | ❌ | ❌ | ✅ Radar (Issue + Discussion) |
| Scheduled patrol | ❌ | ❌ | ❌ | ✅ Daily Patrol |
| Multi-model | GitHub model only | Multiple | Multiple | DeepSeek / OpenAI / Claude |
| Backend options | Single | Single | Single | Native + Pi agent loop |
| Cost | Subscription required | Free for public repos | Free for public repos | **Free (use your own key)** |
| Self-hosting | ❌ | ❌ | ✅ | ✅ 5 composite actions |

RepoKeeper does more than all of them. Copilot helps you write code in the editor, and CodeRabbit comments on code in PRs. These are all important—but they don't handle how an Issue becomes a PR, why CI keeps failing daily, or what questions the community raises in Discussions.

These are precisely the things open-source maintainers spend the most time on every day, and they are also RepoKeeper's focus.

---

## It Can Now Develop Itself

This is probably the most exciting aspect of the entire project: **RepoKeeper has reached a "chicken-and-egg" state.** I can use it to create PRs, fix bugs, apply labels, and perform code reviews for RepoKeeper itself.

Specifically, five workflows are already running in the RepoKeeper repository:

1. **Agent** — With an `agent-todo` label or a `/repokeeper go` comment, it writes code, verifies it, and submits a PR on its own.
2. **Radar** — Monitors community feedback, scans keywords in Issues and Discussions, and automatically creates an Issue after AI classification.
3. **Patrol** — Every day at 8 AM, it patrols dependencies, CI status, and overdue Issues, generating a health score.
4. **Labeler** — Automatically classifies and labels new Issues and PRs.
5. **Review** — Automatically performs line-by-line code review after PR submission, and re-reviews automatically after new commits are pushed.

An open-source project running its own actions within its own workflows to maintain itself—this itself is the best proof of RepoKeeper's stability.

---

## What Each of the Six Modules Does

RepoKeeper now has six modules, each of which can be enabled or disabled independently.

### 1. Implementation Agent (From Issue to PR)

This is the core capability. There are two backends to choose from:

- **Native Backend**: A single LLM call, generating a structured JSON plan, executing modifications, and submitting a PR upon successful verification. Costs less than a cent per run, suitable for simple, single-file changes.
- **Pi Backend**: An autonomous agent loop based on [pi](https://github.com/earendil-works/pi). It reads files, modifies code, runs tests, checks results, and iteratively refines until the task is complete. Suitable for multi-file refactoring and cross-module changes. Costs a few cents to tens of cents per run.

Both backends share the same workflow: Read Issue → Collect code context → Generate modification plan → Execute → Run lint and tests → Verify success → Push branch → Create PR.

The Agent also includes several security safeguards:
- Will not modify `.github/workflows/` directory (prevents privilege escalation)
- Configurable maximum number of files to change per run (default 15)
- Will not create a PR if verification commands fail
- Issues matching `skip_keywords` are automatically skipped

### 2. PR Fix Mode (Conversational Fixes)

This is a recently added capability that addresses a very practical problem: what to do if the PR proposed by the Agent isn't good enough?

Previously, you'd have to close the PR, modify the Issue description, and run it again. Now, simply comment `/repokeeper go` on the PR with clear feedback, and the Agent will read the entire PR's diff and comment history, continuing to make changes on the same branch.

You can do this repeatedly—each round it carries the previous conversation history, preventing it from repeating mistakes.

### 3. Code Review Agent (Line-by-Line Review)

This module does more than just leaving a single comment on a PR.

It will:
- Read the full PR diff
- Check code style, tech stack preferences, and test coverage against your Maintainer Profile
- **Leave inline comments on specific code lines**, indicating severity (🔴 Critical / 🟠 Major / 🟡 Minor / ⚪ Nit)
- Include suggestion blocks that can be applied with one click
- Automatically dismiss old reviews and re-review after new commits are pushed

It also supports `/repokeeper describe`, which automatically generates structured PR descriptions (Summary / Changes / Testing / Screenshots) from the diff.

### 4. Auto-Labeler (Automatic Labeling)

Labels might seem minor, but once a repository accumulates many Issues and PRs, classification becomes manual labor.

What makes the Labeler special is:
- It first reads existing labels in your repository to match naming conventions and color styles
- Only creates new labels when no suitable existing label is found
- Performs **diff-aware classification** for PRs: a PR that changes two `.py` files and one `ci.yml` will be prioritized as a feature rather than CI
- Supports 15 categories: bug, feature, question, documentation, performance, security, dependencies, duplicate, wontfix, good first issue, help wanted, refactoring, testing, ci_cd, noise

### 5. Daily Patrol (Daily Inspection)

Every day at 8 AM (configurable), Patrol scans the repository for:

**Outdated dependencies.** Covering 8 ecosystems: pip, npm, Go, Cargo, Bundler, Composer, Maven, Gradle. It doesn't just list outdated dependencies; it also analyzes risks and provides fix suggestions.

**Why CI failed.** It reads real GitHub Actions run logs, retrieves job and step logs, and uses AI to diagnose the cause. If it determines an automatic fix is possible (e.g., outdated action version, incorrect path, missing environment variable), it reads the workflow file and directly creates a CI fix PR.

**Which Issues have been open too long.** Default threshold is 90 days, providing suggested actions.

Finally, it outputs a health score from 0-100 and a Markdown summary.

### 6. Community Radar (Community Radar)

Scans GitHub Issues and Discussions for keywords (`bug`, `crash`, `security`, `performance`, etc.), and AI determines if they are signals worth addressing.

If `auto_create_issue` is enabled, it will:
- Automatically create an Issue, linking back to the original discussion
- Apply the `repokeeper-radar` label
- Will not create duplicates if scanning the same source again; instead, it will append comments to an existing Issue
- Supports Email, Telegram, WeChat notifications

---

## One Configuration to Rule Them All

All six modules share a single `repokeeper.yml` configuration:

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

Write once, and all modules will follow your preferences.

---

## Onboarding: Up and Running in One Minute

Minimum onboarding requires just two steps.

**1. Copy the workflow file to your repository:**

```bash
pip install repokeeper
repokeeper init --all-workflows   # All 5 models
# Or
repokeeper init --minimal         # Just Agent model
```

**2. Check before pushing:**

```bash
repokeeper doctor --repo yourname/yourrepo
```

`doctor` checks for all common issues like profile configuration, workflow trigger conditions and permissions, GitHub token, LLM key, repository name, etc. After confirming everything is correct, configure `DEEPSEEK_API_KEY` in GitHub Actions Secrets, then push the workflow.

Alternatively, just feed the following prompt to any AI coding agent:

```
Add RepoKeeper to this repository. Create `.github/workflows/repokeeper.yml` that uses the `shenxianpeng/repokeeper/agent@v1` composite action — trigger on issue comments (`/repokeeper go`) and labels (`agent-todo`). Pass `DEEPSEEK_API_KEY` as the `llm_api_key` input. Then tell me to add a `DEEPSEEK_API_KEY` secret in GitHub Actions settings.
```

---

## Cost and Security

**Cost-wise**, using DeepSeek, one Agent implementation costs less than a cent to tens of cents (depending on whether Native or Pi is used), one Patrol inspection costs about a few cents, and one Review costs about a few cents. Compared to the subscription fee you pay for Copilot, this is practically negligible.

**Security-wise**, RepoKeeper's default design is: create a PR, do not auto-merge. The only required permissions are `contents: write`, `issues: write`, `pull-requests: write`. Branches generated by the Agent are uniformly prefixed with `repokeeper/`, the `.github/workflows/` directory is hard-coded protected, and a PR will not be created if verification commands fail.

The final decision to merge is still yours.

---

## Finally

RepoKeeper is now getting closer to my ideal "open-source maintenance assistant."

It can monitor the community, patrol repositories, write code, review code, label issues, and fix CI—all at an extremely low cost. What satisfies me most is that it's already using its own capabilities to maintain itself. Every time I apply an `agent-todo` label in the RepoKeeper repository and watch it read code, write changes, run tests, and propose PRs on its own, that feeling is truly unique.

If you also maintain open-source projects, especially if you're starting to feel overwhelmed by the number of repositories, you might want to give RepoKeeper a try.

- GitHub：https://github.com/shenxianpeng/repokeeper
- 文档：https://shenxianpeng.github.io/repokeeper/
- PyPI：https://pypi.org/project/repokeeper/

If you encounter issues, open one on GitHub, or simply let RepoKeeper fix it itself.

See you next time, experienced developers!
