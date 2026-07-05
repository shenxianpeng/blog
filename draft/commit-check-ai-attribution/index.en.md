---
title: "Commit Check: AI Attribution Governance and Recent Highlights"
summary: |
  Commit Check v2.11.0 introduces AI attribution governance — a single config toggle that
  rejects commits containing known AI tool signatures. This post also recaps important
  updates from v2.5.0 through v2.10.0, including AI agent branch prefixes, force push
  protection, output controls, and more.
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

Hi everyone, I'm Shen Gong.

It's been over half a year since the last Commit Check update post. Quite a few versions have shipped in that time, and today I'm writing to highlight what I think is the most important feature yet — plus a recap of everything else that's happened since v2.5.0.

## The Big One: AI Attribution Governance

Coming in v2.11.0 — **AI Attribution Governance**.

What problem does this solve?

As AI coding tools like Claude Code, GitHub Copilot, Cursor, Windsurf, and Devin become mainstream, the open-source community faces a new question: **how do we know whether a commit was written by a human or AI?**

The Python community [discussed this](https://discuss.python.org/t/should-claude-codes-usage-be-described-in-the-code-docs-somewhere/107969) at length. The Linux kernel standardized on the `Assisted-by:` trailer format. VS Code has an open [issue](https://github.com/microsoft/vscode/issues/313962) debating whether to replace `Co-authored-by` with `Assisted-by` for AI agents.

But until now, **no tool enforced these policies at the CI level.**

Commit Check fills that gap.

### Configuration

A single binary switch — simple and backward compatible:

```toml
[commit]
ai_attribution = "forbid"  # "ignore" is the default
```

Once set to `forbid`, Commit Check scans commit messages for known AI tool signatures and rejects any match.

### Detected AI Tools

The built-in signature database recognizes:

| Tool | Patterns matched |
|------|-----------------|
| Claude Code | `Co-authored-by: Claude`, `Assisted-by: Claude:<model>`, `🤖 Generated with Claude`, `Claude-Session:`, `Claude-Workflow:` |
| GitHub Copilot | `Co-authored-by: Copilot` |
| OpenAI Codex | `Co-authored-by: Codex` |
| Gemini | `Co-authored-by: Gemini` |
| Cursor | `Co-authored-by: Cursor` |
| Devin | `Co-authored-by: Devin` |
| Aider | `Co-authored-by: Aider`, `Co-authored-by: ... (aider)` |
| Windsurf | `Co-authored-by: Windsurf` |
| Tabby | `Co-authored-by: Tabby` |
| Generic AI | `Assisted-by: <tool>:<model>` (kernel style), model names (`claude-sonnet-4`, `gpt-4-turbo`) |

### False Positive Prevention

A practical concern: people named Claude or Devin exist. The implementation anchors Claude/Devin/Copilot patterns to known noreply email addresses, so human co-authors like `Co-authored-by: Jane Doe <jane@example.com>` are never flagged.

### Multiple Integration Options

Like all Commit Check features, AI attribution works across all interfaces:

```bash
# CLI
commit-check --ai-attribution=forbid

# Environment variable
export CCHK_AI_ATTRIBUTION=forbid

# TOML config
[commit]
ai_attribution = "forbid"

# Python API
from commit_check.api import validate_message
result = validate_message(message, ai_attribution="forbid")
```

See the full PR at [commit-check/commit-check#456](https://github.com/commit-check/commit-check/pull/456). Feedback welcome!

---

## Recent Highlights (v2.5.0 — v2.10.0)

Since the last update post, Commit Check has shipped a number of notable features. Here's a recap.

### v2.9.0 — AI Agent Branch Prefixes

The Conventional Branch v1.1.0 spec introduced AI agent branch prefixes: `ai/`, `claude/`, `codex/`, `copilot/`, and `cursor/`.

In v2.9.0, these were added to `DEFAULT_BRANCH_TYPES` — branches like `claude/fix-bug-123` pass validation out of the box.

### v2.7.0 — Force Push Protection

A frequently requested feature: Commit Check now detects and blocks `git push --force` / `git push -f` via a `pre-push` hook.

It uses `git merge-base --is-ancestor` to inspect the ancestry relationship. New branch pushes and fast-forwards pass normally; only true force pushes are blocked.

```toml
[push]
allow_force_push = false  # default: true
```

Use it as a pre-commit hook:

```yaml
repos:
  - repo: https://github.com/commit-check/commit-check
    rev: v2.7.0
    hooks:
      - id: check-no-force-push
        stages: [pre-push]
```

### v2.6.0 — Output Controls

Two new CLI flags for quieter CI logs:

- `--no-banner`: Suppress the ASCII art failure banner, keep detailed messages
- `--compact`: Print one `[FAIL]` line per failing check, implies `--no-banner`

### v2.5.0 — Multiple Practical Improvements

**Co-author bypass in `ignore_authors`**

When a co-author matches the ignore list, all commit checks are skipped — useful for AI-assisted workflows:

```toml
[commit]
ignore_authors = ["dependabot[bot]", "renovate[bot]", "coderabbitai[bot]", "copilot[bot]"]
```

**Organization-level config inheritance (`inherit_from`)**

Share a centralized base config across all repositories:

```toml
inherit_from = "github:my-org/.github:cchk.toml"

[commit]
subject_max_length = 72  # local override
```

**Git config author validation fix**

Now checks `git config user.name / user.email` first — the identity for the *next* commit — instead of only the last commit's author.

### v2.8.0 — Custom Regex & Python 3.9 Drop

Two significant changes:

**Custom regex support** via `message_pattern`:

```toml
[commit]
message_pattern = "^(feat|fix|docs|chore|test)\\(.*\\):.*$"
```

**Python 3.9 support dropped**, enabling use of newer Python features.

---

## Housekeeping

Beyond features, there were several maintenance improvements:

- **Legacy YAML config code removed** (v2.10.1): Cleaned out the YAML compatibility layer from the v2.0 migration.
- **OpenSSF Scorecard added** (v2.10.2): Check out the Scorecard badge in the repo.
- **Bug fixes**: WIP commit detection case-insensitivity fix, special character support in Conventional Commit descriptions (v2.10.1).
- **CI/CD improvements**: Migrated PyPI publishing to `pypa/gh-action-pypi-publish`.

---

## Closing Thoughts

When I started Commit Check, I never imagined it would grow into what it is today.

From commit messages and branch names, to author validation and sign-off checks, to merge-base verification and force push protection — and now AI attribution governance — it has evolved into a comprehensive compliance framework for the entire commit workflow.

All driven by user feedback and community needs.

If you haven't tried it yet, now is the perfect time:

```bash
pip install commit-check
```

📍 **Project**: github.com/commit-check/commit-check

📄 **Docs**: https://commit-check.github.io/commit-check/

---

Please attribute the author when redistributing. For commercial use, please contact the author. Follow my WeChat public account 「沈显鹏」for updates.
