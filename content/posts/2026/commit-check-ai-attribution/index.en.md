---
title: Commit Check New Features—AI Attribution Governance and Recent Highlights Review
summary: |
  Commit Check introduces AI Attribution Governance in its latest version—by configuring ai_attribution = "forbid", it can reject commits containing signatures of known AI tools.
  This blog post also reviews multiple important updates from v2.5.0 to v2.10.0, including branch specification enhancements, force push protection, and output control.
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

Hello everyone, I'm Engineer Shen.

It's been more than half a year since I last wrote about Commit Check updates. During this time, Commit Check has released many versions. Today, with a new feature that I consider particularly important just merged, I'm writing a blog post to discuss it.

## First, the Most Important: AI Attribution Governance

The core feature of the newly released v2.11.0 is **AI Attribution Governance**.

What problem does this feature solve?

With the popularization of AI programming tools like Claude Code, GitHub Copilot, Cursor, Windsurf, and Devin, the open-source community faces a new problem: **How to know if a commit was written by a human or an AI?**

The Python community has specifically discussed this issue on [discuss.python.org](https://discuss.python.org/t/should-claude-codes-usage-be-described-in-the-code-docs-somewhere/107969), and the Linux Kernel has standardized the `Assisted-by:` format. VS Code also has a related [issue](https://github.com/microsoft/vscode/issues/313962) discussing whether to use `Assisted-by` instead of `Co-authored-by` to tag AI contributors.

However, the problem is that currently, there seems to be no tool that can automatically enforce such a policy at the CI level.

Commit Check itself is designed for commit inspection, making it very suitable for this task.

### Configuration Method

It's very simple, just one line of configuration:

```toml
[commit]
ai_attribution = "forbid"  # "ignore" is the default, meaning no check
```

When set to `forbid`, Commit Check will check if the commit message contains characteristic signatures of known AI tools. If detected, the commit will be rejected.

> **Note**: This feature only detects AI tool signatures in commit messages and does not affect other types of commit checks.

### Supported AI Tools for Detection

The currently built-in signature library can identify the following tools:

| Tool | Matching Pattern |
|------|------------------|
| Claude Code | `Co-authored-by: Claude`、`Assisted-by: Claude:<model>`、`🤖 Generated with Claude`、`Claude-Session:`、`Claude-Workflow:` |
| GitHub Copilot | `Co-authored-by: Copilot` |
| OpenAI Codex | `Co-authored-by: Codex` |
| Gemini | `Co-authored-by: Gemini` |
| Cursor | `Co-authored-by: Cursor` |
| Devin | `Co-authored-by: Devin` |
| Aider | `Co-authored-by: Aider`、`Co-authored-by: ... (aider)` |
| Windsurf | `Co-authored-by: Windsurf` |
| Tabby | `Co-authored-by: Tabby` |
| General AI | `Assisted-by: <tool>:<model>` (Kernel style)、Model names (`claude-sonnet-4`、`gpt-4-turbo`) |

### False Positive Prevention

In actual use, some foreigners are named Claude or Devin. If no distinction is made, false positives may occur.

Commit Check's solution is: for patterns like Claude, Devin, Copilot, etc., **anchor to known noreply email addresses**, which will not match human co-authors. Regular users like `Co-authored-by: Jane Doe <jane@example.com>` will never be flagged.

### Multiple Integration Methods

Like all Commit Check features, AI Attribution Governance supports:

```bash
# CLI method
commit-check --ai-attribution=forbid

# Environment variable
export CCHK_AI_ATTRIBUTION=forbid

# TOML configuration
[commit]
ai_attribution = "forbid"

# Python API
from commit_check.api import validate_message
result = validate_message(message, ai_attribution="forbid")
```

See the detailed PR at [commit-check/commit-check#456](https://github.com/commit-check/commit-check/pull/456). Welcome reviews and feedback.

---

## Review of Highlights Released During This Period

Since v2.5.0, Commit Check has indeed released many practical features. Here's a quick review.

### v2.9.0 — Default Support for AI Agent Branch Prefixes

The [Conventional Branch](https://www.conventionalbranch.org) v1.1.0 specification added AI agent-related branch prefixes: `ai/`, `claude/`, `codex/`, `copilot/`, `cursor/`.

In v2.9.0, these prefixes are directly added to the default branch types, making them available out-of-the-box without additional configuration.

If you create a branch using Claude Code or Copilot, branch names like `claude/fix-bug-123` will now pass the check by default.

### v2.8.0 — Custom Regex and Bidding Farewell to Python 3.9

v2.8.0 has two important changes:

First, it brought back the highly requested custom regex feature, supported by the `message_pattern` configuration option:

```toml
[commit]
message_pattern = "^(feat|fix|docs|chore|test)\\(.*\\):.*$"
```

Second, it officially dropped support for Python 3.9, allowing the project to use newer Python features.

### v2.7.0 — Force Push Protection

This is a highly requested feature by many teams.

Commit Check can now detect force pushes (`git push --force` / `git push -f`) via the `pre-push` hook and block them when detected.

The principle is to check if the remote commit is an ancestor of the local commit using `git merge-base --is-ancestor`. New branch pushes and fast-forward pushes pass normally; only actual force pushes are intercepted.

```toml
[push]
allow_force_push = false  # Default is true; set to false to block force pushes
```

This feature is used as a `pre-push` hook for `pre-commit`:

```yaml
repos:
  - repo: https://github.com/commit-check/commit-check
    rev: v2.7.0
    hooks:
      - id: check-no-force-push
        stages: [pre-push]
```

### v2.6.0 — Output Control

Many users found the commit check banner too long in CI logs. v2.6.0 added two CLI flags:

- `--no-banner`: Removes the ASCII art banner, retaining detailed error messages.
- `--compact`: Outputs only one `[FAIL]` line for each failed check, and implicitly includes `--no-banner`.

This is very practical in CI logs or pre-commit output.

### v2.5.0 — Multiple Practical Updates

This was the most important feature version in the v2 series, containing three significant updates:

**Co-author Bypass Support**

When a commit's co-author matches the `ignore_authors` list, that commit can skip all checks. This is especially suitable for AI-assisted workflows:

```toml
[commit]
ignore_authors = ["dependabot[bot]", "renovate[bot]", "coderabbitai[bot]", "copilot[bot]"]
```

**Organization-level Configuration Inheritance (inherit_from)**

Teams can now share a centralized base configuration:

```toml
# Each repository only needs to reference the organization configuration
inherit_from = "github:my-org/.github:cchk.toml"

[commit]
subject_max_length = 72  # Local override
```

Supports GitHub raw files, local paths, and HTTPS URLs as sources.

**Git Config Author Validation Fix**

Previously, only the author information of the latest commit was checked. Now, `git config user.name / user.email` is prioritized—that is, the identity that will be used for the **next commit**. This solves the problem where developers configured incorrect user.name but could still pass checks.

---

## Conclusion

Since Commit Check was born in 2022, my biggest feeling is that it is no longer just "a tool to check commit messages."

It has evolved from basic checks including commit messages, branch naming, author information, and signature verification, to later merge baseline checks, force push protection, and now AI attribution governance. It has gradually become a compliance check framework covering the entire code submission process.

This was something I didn't initially foresee—user feedback and community needs have pushed it step by step to where it is today.

If you haven't used Commit Check yet, you can install it via pip:

```bash
pip install commit-check
```

📍 Project Address: **github.com/commit-check/commit-check**

📄 More Details: https://commit-check.github.io/commit-check/

Finally, everyone is welcome to Star, ask questions, and contribute code on GitHub.

---

Please cite the author and source when reprinting articles from this site. Do not use for any commercial purposes. Welcome to follow the official account "沈显鹏" (Shen Xianpeng).