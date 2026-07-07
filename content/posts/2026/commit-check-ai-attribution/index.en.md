---
title: Which Code in Your Repository is AI-Written—Now There's a Tool to Govern It
summary: |
  AI tools like Claude Code by default embed signatures in commits, something many people don't even notice. Commit Check v2.11.0 introduces AI Attribution Governance, allowing a single line of configuration to reject commits with AI signatures at the CI level. This article also discusses the boundaries of this feature and other pain points Commit Check has solved in the past six months.
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

Hi, I'm Xianpeng.

First, I'd like you to do a small experiment: open your team's repository and run this command—

```bash
git log --grep="Co-authored-by: Claude"
```

If someone in your team is using Claude Code, the results might surprise you.

Because Claude Code by default embeds signatures like `Co-authored-by: Claude` in commits. Tools like Copilot, Cursor, and Devin also have their own ways of marking. Without realizing it, a bunch of AI signatures have already crept into the commit history.

Some teams don't care, while others explicitly don't want these to appear in their commit history—especially enterprises with compliance requirements for code origin, and open-source projects that don't want to be overwhelmed by AI commits.

The community has actually been debating this issue. The Python community has specifically discussed it on [discuss.python.org](https://discuss.python.org/t/should-claude-codes-usage-be-described-in-the-code-docs-somewhere/107969), the Linux Kernel simply standardized the `Assisted-by:` format, and VS Code also has an [issue](https://github.com/microsoft/vscode/issues/313962) discussing whether to replace `Co-authored-by` with it.

Everyone is discussing "how to annotate," but I found a gap: **no tool can truly enforce this policy at the CI level.** Discussions remain discussions without practical implementation.

Commit Check's original purpose is commit checking, so who better to do this? Thus came the recently released v2.11.0—AI Attribution Governance.

## A Single Line of Configuration

```toml
[commit]
ai_attribution = "forbid"
```

Adding this line will directly reject any commit whose message contains a known AI tool signature. The default value is `ignore`, so it won't affect existing users.

Currently, the built-in signature library covers mainstream tools like Claude Code, Copilot, Codex, Gemini, Cursor, Devin, Aider, Windsurf, etc. It also recognizes the Kernel-style `Assisted-by: <tool>:<model>`, and can even identify model names like `claude-sonnet-4` or `gpt-4-turbo` directly appearing in the commit message.

## But There's a Catch: Some People Are Actually Named Claude

My biggest concern when developing this feature was false positives. Claude, Devin—these are normal English names. We can't have a colleague named Devin getting their commit rejected, can we?

Therefore, for such patterns, Commit Check doesn't simply match names, but **anchors to the known noreply email addresses of AI tools**. A real co-author like `Co-authored-by: Jane Doe <jane@example.com>` will never be mistakenly flagged.

If you want to try it, CLI, environment variables, TOML configuration, and Python API are all supported, with usage identical to other checks. For detailed implementation, see [commit-check/commit-check#456](https://github.com/commit-check/commit-check/pull/456). Feedback is welcome.

## A Reality Check: This Feature Can't Prevent Deliberate Cheating

One thing must be made clear: `ai_attribution = "forbid"` checks for signatures in commit messages. **It governs default behavior but cannot prevent those who deliberately try to circumvent it.**

For example, a developer can simply tell the AI, "Don't add any AI-related signatures when committing," or have the AI only modify the code, then commit manually themselves—in such cases, the commit message will be clean, and Commit Check naturally won't detect anything. Whether code is AI-written cannot be 100% determined solely by looking at the commit message.

So, what's the point of this feature then?

It's the same kind of thing as commit message conventions or branch naming conventions—**these checks have never prevented those who deliberately cause trouble (adding `--no-verify` bypasses everything), but they do prevent "unclear rules" and "casual, unintentional commits."**

In practical scenarios, the vast majority of AI signatures are not added by developers intentionally, but are the default behavior of the tools. If a team doesn't have a clear policy, the commit history will be unknowingly polluted. With mandatory checks at the CI level, at least two things are achieved:

*   First, it **makes the team's policy explicit**—the statement "we do not accept AI signatures" transforms from a verbal agreement into a rule that will reject commits;
*   Second, it **blocks all unintentional mistakes**. As for the deliberately hidden parts, that's a matter of engineering culture and code review, not something a lint tool should promise.

Clarity on the tool's boundaries prevents disappointment in its use.

## Also, Let's Talk About Other Things Added in the Past Six Months

It's been over half a year since I last wrote about Commit Check. I'll go through a few features released during this period, categorized by "what problem they solve," to see if any resonate with you.

**A colleague's force push wiped out your commits.** This is probably one of the most frustrating incidents in Git collaboration. Now Commit Check provides the `check-no-force-push` pre-push hook. Its principle is to use `git merge-base --is-ancestor` to determine if the remote commit is an ancestor of the local commit—new branches and fast-forward pushes are allowed, only genuine force pushes are blocked. Once installed, even quick-fingered colleagues trying to `push -f` won't be able to.

```yaml
repos:
  - repo: https://github.com/commit-check/commit-check
    rev: v2.11.0
    hooks:
      - id: check-no-force-push
        stages: [pre-push]
```

**Branches created with Claude Code fail branch name checks.** Conventional Branch v1.1.0 added AI agent branch prefixes, and Commit Check has followed suit: branch names like `claude/fix-bug-123`, `copilot/xxx` now pass by default without needing configuration changes.

**Dependabot's commits are always getting stuck by rules.** Configure `ignore_authors` to add bots like `dependabot[bot]`, `renovate[bot]`, and their commits will skip checks. This is also useful in AI-assisted workflows.

```toml
[commit]
ignore_authors = ["dependabot[bot]", "renovate[bot]", "coderabbitai[bot]"]
```

**Dozens of repositories, each requiring a copy of the configuration.** Now `inherit_from` is supported, allowing a central configuration in the organization, with each repository referencing it with a single line, and local overrides where needed. If you want to unify commit conventions across your team, this feature is for you.

```toml
inherit_from = "github:my-org/.github:cchk.toml"

[commit]
subject_max_length = 72  # Local override
```

**Annoyed by the ASCII banner taking up too much space in CI logs.** Add `--compact`, and each failed check will only output a single `[FAIL]` line. This was one of the most requested small features from users, and after the change, CI logs are much cleaner.

Additionally, there's the return of custom regex `message_pattern` (highly requested), and author information checks now prioritize reading `git config` (previously, incorrect `user.name` could slip through). I won't go into detail for each; if you're interested, you can check the Release Notes.

## Concluding Remarks

Commit Check started development in 2022, and initially, it was truly just a "tool for checking commit messages."

Looking back now, it's managing more and more: commit messages, branch naming, author identity, signatures, merge baselines, force pushes, and now AI attribution—basically covering the entire process of compliance checks for code submission. In terms of usage, CLI, pre-commit hook, Python API, and GitHub Action are all available, so you can integrate it however you like.

Behind all these checks is the same principle: **policy as code**. The rules themselves are code, stored in the repository, versioned, reviewed, and discussed alongside the actual code. A team's commit conventions are no longer verbal agreements, but executable rules.

Honestly, these weren't planned all at once. It's been four years of user feedback and changes in use cases that have driven Commit Check to evolve to where it is today.

If your team is also struggling with commit conventions or the question of "whether to govern AI commits," you can try it:

```bash
pip install commit-check
```

📍 Project address: **github.com/commit-check/commit-check**

📄 More details: https://commit-check.github.io/commit-check/

If you find it useful, please Star it, and feel free to open an Issue to tell me what other pain points your team would like to govern.

---

Please credit the author and source when reprinting articles from this site. Do not use for any commercial purposes. Welcome to follow the official account '沈显鹏' (Shen Xianpeng).