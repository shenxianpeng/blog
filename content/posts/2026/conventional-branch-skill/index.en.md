---
title: Conventional Branch Official Skill Is Here—Install with One Command
summary: |
  A user opened an issue hoping Conventional Branch could provide an official Agent Skill, which I thought was a very reasonable request. I implemented it the same day, and now it can be downloaded and used with a single `npx skills add` command. Coincidentally, the project also surpassed 100 Stars this week, so I'll talk about that too.
tags:
  - Conventional Branch
  - Skills
  - Coding Agent
  - Open Source
authors:
  - shenxianpeng
date: 2026-05-17
---

Conventional Branch now has an official Skill.

This all started with an [Issue](https://github.com/conventional-branch/conventional-branch/issues/119) opened by [@ruzickap] on GitHub:

> I'm looking for an official agent skill that will help my agent properly create the Conventional Branch when needed.

His request was: he hopes for an official Agent Skill that allows an AI coding agent to name branches according to Conventional Branch rules when creating them.

I had actually considered this idea before.

Back when the concept of Skills first emerged, I thought about which of the many projects I maintain should provide a set of rules for agents to use.

I didn't do it at the time, and later forgot about the idea.

This time someone brought up the request, and I thought it was really great, not too late at all.

I wrote and submitted this Skill on the same day (PR [#120](https://github.com/conventional-branch/conventional-branch/pull/120)).

## Install with One Command

Now, you just need to execute one command:

```bash
npx skills add conventional-branch/conventional-branch --skill conventional-branch
```

You can choose which agent to install it under, whether it's project-scoped or global-scoped, during the execution of the command.

After installation, when a coding agent needs to create a branch, it can refer to this set of rules: what prefix to use, how to write the description, which names are valid, and which names might be blocked by `commit-check`.

For users, the biggest benefit is: no need to repeatedly remind the agent every time.

Previously, you might have had to repeatedly say:

> Please use the Conventional Branch specification.
> Branch names should use `kebab-case`.
> Do not use capital letters.
> Do not use underscores.
> `feature` branches should use `feature/xxx`.

Now these rules can be directly placed into the Skill, allowing the agent to read them itself at the appropriate time.

## What This Skill Includes

This Skill is written according to the [Conventional Branch specification](https://conventional-branch.github.io) and primarily covers the following types of rules.

First, branch naming format.

Conventional Branch uses:

```
type/description
```

Currently supported types include:

*   `feature`
*   `bugfix`
*   `hotfix`
*   `release`
*   `chore`

`description` uses lowercase letters and `kebab-case`, for example:

```
feature/add-login-page
bugfix/fix-user-cache
chore/update-ci-config
```

Second, common error checks.

The Skill explicitly states which branch names do not conform to the specification, for example:

```
feature/AddLoginPage
feature/add_login_page
feature/add--login-page
bugfix/fix user cache
```

These issues are common when creating branches manually, and equally likely to occur when agents create branches.

With the Skill, agents have the opportunity to refer to these rules before generating branch names, avoiding the creation of names that are clearly non-compliant.

Third, base branch detection.

The trunk branch might be different for different repositories.

Some projects use `main`, some still use `master`, and some teams use `develop`.

Therefore, the Skill also specifies that before creating a new branch, the existing base branch of the current repository should be detected first, rather than assuming all projects use `main` by default.

Fourth, relationship with Conventional Commits.

Conventional Branch and Conventional Commits can be used together.
For example:

```
feature/add-login-page  -> feat: add login page
bugfix/fix-user-cache   -> fix: fix user cache
chore/update-ci-config  -> chore: update ci config
```

Branch names are responsible for expressing "what type of work this is", while commit messages are responsible for expressing "what was done in this commit".

Together, the entire Git workflow becomes easier for people and tools to understand.

Fifth, synergy with `commit-check`.

The Skill addresses the context issue when agents create branches.
However, whether to enforce the specification ultimately, it's still recommended to rely on tools for fallback.

This is also why I mentioned [`commit-check`](https://github.com/commit-check/commit-check) in the Skill.

If an agent occasionally generates a non-compliant branch name, `commit-check` can still block non-compliant branches locally, in CI, or within team workflows.

In other words: the Skill is responsible for helping the agent do it right as much as possible, and `commit-check` is responsible for providing a fallback in the process.

They work together for a more complete solution.

## Why I Think This Is Worth Doing

AI coding agents are becoming increasingly common. Fewer and fewer people will go to your `Contributing guide` to read instructions written for human contributors.

Even if you explicitly state in your documentation to create branches according to the Conventional Branch specification, AI might still create branches in various forms like:

```
My_New_Feature
feature/newFeature
fix-login-bug
```

This makes CI rules difficult to write, and automated processes like release notes, changelogs, and issue linking also become harder to maintain.

Previously, specifications were primarily written in documentation, relying on people to read, remember, and execute them.

Now with agents, specifications should also be able to become context that agents can read.

This is the value of the Skill. It doesn't replace documentation, nor does it replace validation tools, but rather moves the "specification" forward to the entry point of the agent's work.

Before the agent starts working, it can know: how this repository expects branches to be named.

## How to Participate

If you are not yet familiar with Conventional Branch, you can start here:

-   [Specification Document](https://conventional-branch.github.io)
-   [GitHub Repository](https://github.com/conventional-branch/conventional-branch)
-   [`commit-check` Validation Tool](https://github.com/commit-check/commit-check)

If you have already installed and used this Skill, you are also welcome to provide feedback on your real-world experience.

Feel free to leave a comment under [Issue #119](https://github.com/conventional-branch/conventional-branch/issues/119), or open a new Issue directly.

---

Please cite the author and source when reprinting articles from this site. Do not use for any commercial purposes. Welcome to follow the official account '沈显鹏'.