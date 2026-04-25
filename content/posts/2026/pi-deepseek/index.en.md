---
title: Twenty-Four Cents to Write an Article—My Experience Replacing Codex with Pi + DeepSeek
summary: |
    Codex's $22 monthly subscription fee and usage limits prompted me to seek alternatives. After a failed attempt with OpenCode, I turned to the Pi + DeepSeek combination—the results were surprisingly good, costing only 0.24 RMB to write an entire blog post.
tags:
  - AI
  - Codex
  - DeepSeek
authors:
  - shenxianpeng
date: 2026-04-25
---

Let me start with the conclusion: **Pi + DeepSeek is the most cost-effective AI coding alternative I've found so far.**

Twenty-four cents, for a complete blog post.

---

## Why an Alternative is Needed

I use Claude Code, Codex, and Copilot simultaneously. Together, they cost tens of dollars a month, which isn't cheap, but acceptable.

The real problem is **usage limits**.

It's not a hard stop-when-used-up limit—it's a soft limit where it feels like it's "conserving" usage. The experience during peak hours noticeably degrades; I've paid, but I'm not getting the full service.

I don't want to spend hundreds of dollars to increase my limits. What I need is a reliable, affordable alternative that can step in anytime.

---

## Tried OpenCode, Couldn't Get It Running

The first one I tried was OpenCode. It's been highly discussed recently.

But it wouldn't even open on my Mac. I couldn't get past the interface. Later, I tried configuring it with the DeepSeek API, but the process wasn't smooth, and after a lot of fiddling, I gave up.

That's when I remembered Pi.

---

## What is Pi

[Pi][1] is a terminal AI coding agent, developed by [@badlogic][1]. It's open source, comes with an API Key, and doesn't lock you into any specific model.

Pi only provides a terminal interface; all interactions happen on the command line. This perfectly suits someone like me who loves command-line tools.

DeepSeek-V4 was recently released, and its price is roughly one-tenth of GPT-5.5's—it's a perfect fit to integrate with Pi and test its capabilities.

---

## Hands-on: Letting It Write an Article

Coincidentally, I recently added many new features to the Explain Error Plugin and needed to write an article to share them.

I didn't give it any detailed prompts. Just one sentence:

> "Explain Error has recently released some new features. I haven't shared the features developed since my last article, so please help me organize these new features and write an article."

Then I left it alone.

It did a few things on its own: it pulled closed issues from GitHub, grouped 11 updates into four dimensions—"Major Features / Usage Management / New Providers / Bug Fixes"—extracted the technical details and configuration methods for each feature, and even reproduced my blog's usual table format and footnote style.

Throughout the entire process, I didn't intervene with a single word.

Final cost: **¥0.24**.

---

## What Makes It Valuable

First, **transparent costs**. How much each call costs is crystal clear. No discovering a blown-up bill at the end of the month.

Second, **no soft limits**. Direct API connections don't care about quotas; you pay for what you use, with no throttling.

Third, **model freedom**. DeepSeek for code, Qwen for analyzing long Chinese texts—switch to whichever you want. Codex only offers its own models.

Fourth, **open source**. Pi is at [badlogic/pi-mono][1], with an active community, supporting TypeScript extensions and Pi Packages—you can even package and share your own Skills.

---

## Imperfections

It needs to be clear.

Configuration isn't out-of-the-box—you need to apply for a DeepSeek API Key and recharge it yourself. It's not difficult, but it's an extra step.

Pi is a terminal tool, not a graphical IDE. People accustomed to mouse operations might find it uncomfortable for the first few days. It follows an "agent" approach, reading and writing to code repositories from the terminal, rather than providing line-by-line completion as you type code.

So I haven't given up on Codex. It's still my primary tool—I've already paid for it. When limits are tight or I need to run batch tasks (writing articles, refactoring, generating tests), I switch to Pi + DeepSeek.

This isn't a replacement; it's a complement.

---

Twenty-four cents for an article is just the beginning. When the marginal cost of AI calls drops to this level, many things that were "just ideas" suddenly become worth trying.

If you're also anxious about usage limits, why not take ten minutes to set up Pi + DeepSeek or Qwen?

[1]: https://pi.dev