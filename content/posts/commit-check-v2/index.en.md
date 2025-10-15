---
title: Commit Check v2.0.0 Released—TOML Config Support, Simplified CLI & Hooks, Rebuilt Validation Engine!
summary: After a month of intermittent development and testing, I have finally completed this major update. This is the biggest update Commit Check has received since its inception.
tags:
  - Commit-Check
  - DevOps
author: shenxianpeng
date: 2025-10-13
---

During every Code Review, do your colleagues' commit messages always vary widely?

"fix", "temp change", "update"... these make people shake their heads.

Developers know how important a clean and clear commit history is.

It not only records code changes but also the team's "thought process".

This is precisely the original intention of [Commit Check](https://github.com/commit-check)—to help you and your team maintain consistency and standardization in commit messages and branch naming.

Its goal is simple: **ensure every code commit follows a consistent standard.**

Since 2022, I have been maintaining this open-source project—Commit Check.

Over three years, it has grown from a small tool into an influential DevOps tool in the community, with many teams integrating it into their CI/CD pipelines.

As my understanding of such tools deepened, I realized Commit Check could be even better.

So, after a month of intermittent development and testing, I finally completed this major update.

This is also the biggest version upgrade Commit Check has seen since its inception. 🎉

## What's New in Commit Check v2.0.0?

This update primarily includes three major highlights:

*   TOML Configuration File Support
*   Simplified CLI & Hooks
*   Rebuilt Validation Engine

In a nutshell: **simpler, faster, and easier to use.**

## Why Switch to TOML?

Previously, Commit Check used `.commit-check.yml` as its configuration file.

While highly customizable for users, it brought maintenance complexity, a less intuitive configuration experience, wasn't modern enough, and was prone to errors due to indentation and formatting.

Thus, the decision was made—**to fully switch to TOML**.

TOML's syntax is more intuitive and better suited for **declarative configuration**.

Let's take a look at the before-and-after comparison of the configuration files:

### Old YAML Configuration File

```yaml
# .commit-check.yml
checks:
- check: message
    regex: '^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test){1}(\([\w\-\.]+\))?(!)?: ([\w ])+([\s\S]*)|(Merge).*|(fixup!.*)'
    error: "The commit message should be structured as follows:\n\n
    <type>[optional scope]: <description>\n
    [optional body]\n
    [optional footer(s)]\n\n
    More details please refer to https://www.conventionalcommits.org"
    suggest: please check your commit message whether matches above regex

- check: branch
    regex: ^(bugfix|feature|release|hotfix|task|chore)\/.+|(master)|(main)|(HEAD)|(PR-.+)
    error: "Branches must begin with these types: bugfix/ feature/ release/ hotfix/ task/ chore/"
    suggest: run command `git checkout -b type/branch_name`
```

### New TOML Configuration File

```toml
# commit-check.toml or cchk.toml
[commit]
conventional_commits = true
allow_commit_types = ["feat", "fix", "docs", "style", "refactor", "test", "chore", "ci"]

[branch]
conventional_branch = true
allow_branch_types = ["feature", "bugfix", "hotfix", "release", "chore", "feat", "fix"]
```

Isn't that instantly much cleaner?

No nesting, no indentation pitfalls, easy to understand at a glance.

TOML's structure is naturally suitable for this "rule-declarative" configuration method, allowing direct readability of configuration content.

## Other Updates and Improvements

Other updates primarily revolve around the migration of configuration files, simplification of CLI and Hooks, and the rebuilding of the validation engine.

Besides code updates, I also rewrote the entire [Commit Check documentation](https://commit-check.github.io/commit-check/) system and the [official website](https://commit-check.github.io).

Now you can find complete example configurations and FAQs directly on the official website:

[What's New in v2.0.0](https://commit-check.github.io/commit-check/what-is-new.html)

## Conclusion

If you haven't used Commit Check yet, I highly recommend you try it now, and feel free to share it with your developer friends.

It helps you and your team easily adopt [Conventional Commits](https://www.conventionalcommits.org) and [Conventional Branch](https://conventional-branch.github.io), and through automated checks, makes code commits more standardized, clean, and traceable.

📍 Project Address: **github.com/commit-check/commit-check**

📄 More Details: https://commit-check.github.io/commit-check/

---

When reprinting articles from this site, please credit the author and source, and do not use them for any commercial purposes. Feel free to follow the official account "DevOps攻城狮".