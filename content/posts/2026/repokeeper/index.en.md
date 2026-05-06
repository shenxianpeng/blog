---
title: RepoKeeper—I Made an Active Maintenance Assistant for Open Source Repositories
summary: |
  RepoKeeper is not a code completion tool, but a GitHub assistant for open-source maintenance workflows: it can create fix PRs based on Issues, patrol dependencies and CI, monitor community feedback, and organize discussions worth following up on into Issues.
tags:
  - RepoKeeper
  - AI
  - Open Source
authors:
  - shenxianpeng
date: 2026-05-05
---

It's been almost a week since I last updated an article for the May Day holiday. Although I didn't update, I still brought my computer with me during the vacation—because I've been working on a new project: [RepoKeeper](https://github.com/shenxianpeng/repokeeper).

Its positioning is very specific: **helping open-source maintainers handle daily chores in their repositories.**

The motivation behind this project is actually very simple. After the explosion of AI agents, the number of open-source repositories I maintain quickly grew from a dozen to over thirty. cpp-linter has 9, commit-check added 3, conventional-branch 2, devops-maturity added 2, mkdocs-ng started from scratch and added 5, plus nearly 10 more from my personal projects. Before, I could look after each repository individually, but now, even with AI helping to write code, the number I can attend to each day is very limited, let alone investigating user feedback or developing new requirements.

What I need is not just a tool that helps write code—I need an assistant that can truly **patrol my repositories on my behalf, helping me discover problems and opportunities.** Copilot is indeed good for writing code, but it's expensive, and having it regularly analyze community feedback and automatically create issues requires setting up additional workflows, which isn't very cost-effective in terms of token usage.

RepoKeeper was built for this purpose: it doesn't just write code, but also includes patrolling and community feedback radar capabilities, and you can choose your own model—for example, DeepSeek is much cheaper than Copilot, making it perfectly suitable for handling daily maintenance tasks.

---

## What Exactly Can It Do?

RepoKeeper currently mainly does three types of things:

1.  Automatically implement changes based on Issues and create PRs;
2.  Regularly patrol repository health status—whether dependencies are outdated, why CI failed, which Issues have been left open for too long;
3.  Monitor community feedback and organize discussions worth following up on into GitHub Issues.

These three things correspond to RepoKeeper's three modules: Implementation Agent, Daily Patrol, and Community Radar. Behind them, a shared `repokeeper.yml` configuration file describes your maintenance style and preferences.

---

## 1. From Issue to PR

This is RepoKeeper's most direct capability.

When an Issue is clearly described, you can label it with `agent-todo`, or comment `@repokeeper go` under the Issue, which will trigger the repository's GitHub Actions workflow. After the Agent starts, it will perform these steps:

1.  Read the Issue's title, body, and recent comments;
2.  Collect relevant source files in the repository as context;
3.  Call the LLM to generate a modification plan;
4.  Modify code or documentation according to the plan, writing to files;
5.  Run verification commands (linter, tests, etc.);
6.  If verification passes, push a `repokeeper/...` branch;
7.  Create a Pull Request and leave a comment under the original Issue.

This process sounds similar to what Copilot does: both involve having an LLM write code for you. But there are a few key differences:

-   **You can use cheaper models.** For example, DeepSeek costs only a fraction of GPT-4o, making it especially suitable for these "patching and fixing" tasks. Copilot is also raising its prices in June, so save where you can.
-   **Its positioning is more geared towards "automated maintenance workflows" rather than "code completion".** In the future, I plan to integrate more models, support GitLab, Bitbucket, and even local CLI triggers.

---

## 2. Daily Repository Patrol

The second module is called Daily Patrol. It acts more like "periodically scanning your repository for you", listing areas that need attention, or even fixing them directly.

**Are dependencies outdated?** Patrol scans dependency files in the project, currently covering:

-   Python: `requirements.txt`, `pyproject.toml`, `Pipfile`
-   Node.js: `package.json`, `yarn.lock`
-   Go: `go.mod`
-   Rust: `Cargo.toml`
-   Ruby: `Gemfile`
-   PHP: `composer.json`
-   Maven: `pom.xml`
-   Gradle: `build.gradle`, `build.gradle.kts`

It organizes outdated dependencies by severity and can directly create a dependency upgrade PR. Unlike Dependabot, Patrol doesn't just tell you "this dependency is outdated" in a table; it attempts to analyze the potential risks posed by outdated dependencies and provides repair suggestions. However, to be honest, the automatic secure rewriting of lock files is still under development; currently, it mainly reports candidates and creates PR suggestions.

**Why did CI fail?** Patrol reads recent failed GitHub Actions run records, retrieves actual job and step information, uses AI to diagnose the cause, and provides repair suggestions. If it determines that the issue can be fixed automatically—for example, an action version is too old, a path is misconfigured, or an environment variable is not set—it will read the failed workflow file, generate a fix, and directly create a CI fix PR. Many CI failures aren't complex problems but small pitfalls; Patrol providing a reviewable fix first is much easier than you tracing it through logs bit by bit.

**Which Issues have been left open for too long?** Daily Patrol also identifies Issues that haven't been updated for a long time, with a default threshold of 90 days. It will provide a summary and suggested actions—close, ping, continue pushing, or ignore.

Finally, Patrol generates a health score (0-100) and a Markdown summary, suitable for inclusion in GitHub Actions summaries, Issues, or notifications.

---

## 3. Monitor Community Feedback, Automatically Organize into Issues

The third module is Community Radar.

It can scan GitHub Issues and Discussions for keywords you care about, such as `bug`, `crash`, `security`, `performance`. After matching content, Radar uses AI to determine whether it's a bug report, a feature request, a general question, or just noise.

If `auto_create_issue` is enabled, it will automatically create new GitHub Issues for feedback worth following up on.

A few design details worth mentioning:

-   New Issues will link back to the original discussion, preserving the source;
-   Automatically tag with `repokeeper-radar` for easy filtering;
-   If the same source is scanned again, it won't create a duplicate Issue, but instead append an activity comment to the existing Issue;
-   Can notify you via Email, Telegram, or WeChat.

This solves an often-overlooked pain point in open-source maintenance: users sometimes don't come to your repository to create Issues, but rather discuss problems within their own projects. Radar's role is to turn these scattered "signals worth addressing" into actionable GitHub Issues that can be queued, assigned, and processed.

---

## 4. Document Your Maintenance Habits with a Configuration File

RepoKeeper doesn't work the same way for every repository. You can document your project preferences using `repokeeper.yml`:

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

This configuration determines how RepoKeeper reads the project, how it verifies changes, which issues to skip, the maximum number of files a PR can modify, and where notifications are sent.

---

## How to Get Started?

The minimal integration is simple.

Install:

```bash
pip install repokeeper
```

Initialize a minimal configuration (only Implementation Agent workflow):

```bash
repokeeper init --minimal
```

Or generate workflows for all three modules at once:

```bash
repokeeper init --all-workflows
```

Before pushing, you can also use the `doctor` command to check the environment:

```bash
repokeeper doctor --repo owner/repo
```

It checks common issues such as whether the profile configuration is valid, if workflow trigger conditions and permissions are complete, if GitHub tokens and LLM API keys are configured, and if the repository name is correct.

After confirmation, configure the model key in GitHub Actions Secrets, for example, `DEEPSEEK_API_KEY`, and it's ready to use.

Complete resources:

*   GitHub: <https://github.com/shenxianpeng/repokeeper>
*   Documentation: <https://shenxianpeng.github.io/repokeeper/>
*   PyPI: <https://pypi.org/project/repokeeper/>

---

## Security Boundaries

The most common question asked about such tools is: Will it make arbitrary changes to my repository?

RepoKeeper's default design is: **create PRs, do not automatically merge.**

The default workflow requires these permissions:

```yaml
permissions:
  contents: write
  issues: write
  pull-requests: write
```

These permissions are only used to push branches, comment on Issues, and create PRs. The final decision to merge still rests with you.

In addition, there are several default security measures:

-   Branches generated by the Agent consistently start with `repokeeper/`;
-   The maximum number of files modified per PR can be limited via `pr.max_files_per_pr`;
-   If verification commands (linter, tests) fail, no PR will be created;
-   The `.github/workflows/` directory is hardcoded and protected, preventing the Agent from modifying its own workflow to escalate privileges;
-   You can use `skip_keywords` to have the Agent automatically skip Issues involving security, architecture, or breaking changes.

The goal of this design is clear: to maximize the effectiveness of the AI assistant while minimizing potential risks.

---

## Current Status

RepoKeeper's current latest version is `v0.7.0`, released on May 5, 2026.

The project is written in Python, supports Python 3.10 to 3.14, and is open-source under the MIT License. In terms of models, it supports DeepSeek (`deepseek-chat` / `deepseek-reasoner`), OpenAI compatible APIs (including GPT-4o), and Anthropic Claude. Each LLM call estimates token cost, and you can also customize the billing price for different models via environment variables.

If you maintain open-source projects, especially those with a certain volume of community feedback or if you want to regularly patrol repository health, you might want to give RepoKeeper a try.

Project address:

https://github.com/shenxianpeng/repokeeper