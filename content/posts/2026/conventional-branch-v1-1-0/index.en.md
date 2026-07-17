---
title: Conventional Branch 1.1.0 Released—Official Support for AI Coding Agent Branch Prefixes
summary: |
  The Conventional Branch specification receives its first major update. Version 1.1.0 adds support for AI Coding Agent branch prefixes (ai/, copilot/, cursor/, claude/, codex/), and provides a machine-readable spec.json and agent registry, making the specification useful not only for humans but also for tools.
tags:
  - Conventional Branch
  - Git
  - AI
  - Coding Agent
authors:
  - shenxianpeng
date: 2026-07-16
series: ["Conventional Branch"]
series_order: 3
---

As more and more AI Coding Agents begin to automatically create Git branches, a new question arises: **What specification should these branches follow?**

Conventional Branch has remained at version 1.0.0 since its release, but the newly released 1.1.0 primarily extends around the AI Coding Agent scenario to adapt to new development methods.

This article will discuss the background of this update and the several important changes brought by 1.1.0.

## Why AI Branch Prefixes Are Needed

More and more developers are now using AI Coding Agents, and many tools automatically create branches.

For example, GitHub Copilot defaults to creating `copilot/` branches, and Claude defaults to creating `claude/` branches.

These naming conventions have gradually become a de facto standard. Therefore, Conventional Branch 1.1.0 chooses to embrace this trend rather than redefine it.

This version adds the following AI Agent branch prefixes:

```text
copilot/      — GitHub Copilot
cursor/       — Cursor
claude/       — Claude
codex/        — OpenAI Codex
ai/           — Generic AI branch
```

Among these, `ai/` is a generic prefix for branches that are created by AI but do not belong to a specific vendor.

## If Your Commonly Used Agent Is Not Listed

Currently, the specification only includes a few common AI Agent prefixes, but we also provide a registrable **Agent Registry**.

If the AI Coding Agent you are using is not included in the list, you can add it by submitting a PR to `data/agents.yaml`.

After the PR is merged, the official website will automatically synchronize and update the corresponding Agent list. This way, new AI Agents can quickly join the entire ecosystem without waiting for a new version of the specification to be released.

## spec.json—Making the Specification Readable by Code

For tool developers, `spec.json` is likely the most important update.

In the past, if you wanted to validate a branch against Conventional Branch using code, you would have to parse the documentation yourself, extract the ABNF syntax, and maintain a set of regular expressions.

Now, we provide a machine-readable `spec.json`, which includes:

- All supported types and their aliases
- Branch naming rules
- ABNF grammar definition
- Regular expressions (regex) directly usable for validation

This means that whether it's CI, Git Hooks, or IDE plugins, they can directly read this specification without having to repeatedly maintain their own rules.

For example, in CI, you can directly read the regular expression provided in `spec.json` for validation:

```bash
REGEX=$(curl -s https://conventionalbranch.org/spec.json | jq -r '.grammar.regex')

if [[ ! "$BRANCH_NAME" =~ $REGEX ]]; then
  echo "Branch name does not conform to Conventional Branch specification"
  exit 1
fi
```

Of course, in production environments, `spec.json` is usually cached rather than redownloaded every time CI runs.

## Website Synchronously Supports Version Switching

With the release of 1.1.0, the official website has also synchronously added a version switching feature.

You can now freely switch between 1.0.0 and 1.1.0 on the website to compare specification changes between different versions.

## A Few Thoughts

Two years have passed since the release of 1.0.0, and Conventional Branch has come a long way.

When it was first released, Git branch specifications were a relatively niche topic. Later, with the popularization of Conventional Commits, more and more teams began to pay attention to standardizing code commits and branch management.

Today, AI Coding Agents are gradually becoming involved in daily development workflows, and Git branches are increasingly being automatically created by AI.

In my opinion, the biggest change in Conventional Branch 1.1.0 is not the addition of a few AI prefixes, but rather that the specification truly begins to cater to tools.

`spec.json` allows machines to read and understand the specification, and `data/agents.yaml` allows new Agents to continuously join the ecosystem. This means that Conventional Branch is no longer just a document for developers to read, but an open standard that can be directly integrated into toolchains.

In the future, collaboration partners will no longer be just developers, but also an increasing number of AI Agents. Specifications also need to evolve with development methods.

If you are not yet familiar with Conventional Branch, please visit https://conventionalbranch.org.

If you believe it can improve your team's Git branch management, feel free to try it out and share it with more developers.
