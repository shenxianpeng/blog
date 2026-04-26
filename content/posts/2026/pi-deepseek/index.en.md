---
title: Writing an Article for Twenty-Four Cents—My Experience Using Pi + DeepSeek as a Codex Backup Solution
summary: |
    Codex's $22 monthly subscription fee and usage limits prompted me to seek a cheaper, stable, and always-ready backup solution. After an unsuccessful attempt with OpenCode, I turned to the Pi + DeepSeek combination. The result was a bit unexpected: writing an entire blog post cost only 0.24 RMB.
tags:
  - AI
  - Codex
  - DeepSeek
authors:
  - shenxianpeng
date: 2026-04-25
---

Let me start with the conclusion: **Pi + DeepSeek is the most cost-effective AI coding backup solution I've found so far.**

For twenty-four cents, I wrote a complete blog post.

In the past, I might have dismissed this price as a gimmick. But after actually using it, my feeling is: when the marginal cost of AI calls is this low, many things we previously only 'thought about doing' can genuinely be handed over to AI.

## Why a Backup Solution is Needed

I'm currently using `Claude Code`, `Codex`, and `Copilot` simultaneously.

Adding up to tens of dollars each month, it's not cheap, but still acceptable. What really stresses me out isn't the subscription fee, but the **usage limits**.

Often, it's not that the tools are bad, but that I subconsciously 'conserve' them when using them. For example, writing articles, batch analyzing issues, generating tests, or refactoring code—these tasks are all well-suited for AI, but constantly worrying about limits can easily disrupt the workflow.

I don't want to spend hundreds more dollars to upgrade my quota for these scenarios.

So what I need is a backup solution:  
**Always ready, performs well, and most importantly, affordable.**

## First Attempt: OpenCode, But It Didn't Run

The first thing I tried was `OpenCode`.

However, it didn't run successfully on my Mac; I couldn't even get into the interface. Later, I tried configuring the `DeepSeek` API for it, which also failed.

At this point, `Pi` came to mind.

## What is Pi?

[Pi][1] is a minimalist terminal programming harness, developed by [@badlogic][2]. It's open source and not tied to any specific model.

You can think of it as an AI programming assistant framework running in your terminal:  
It doesn't provide a complex graphical interface, but instead interacts with models via the command line, allowing AI to read projects, analyze code, execute tasks, and generate content.

This suits me perfectly, as I naturally prefer command-line tools and am more accustomed to completing development work in the terminal.

Recently, `DeepSeek-V4` was released, priced at roughly one-tenth of `GPT-5.5`. Since `Pi` can freely integrate different models, I decided to connect `DeepSeek` to it and see how it performs.

## Hands-on: Letting It Write an Article

Coincidentally, I've added many new features to the Explain Error Plugin recently, but haven't had time to write an article summarizing them.

So I only gave `Pi` one sentence:

> Explain Error has recently released some new features. Since my last article, these new features haven't been shared. Please help me organize them and write an article.

Then I left it alone.

It did several things on its own:

1.  Pulled recently closed issues from GitHub;
2.  Organized 11 updates from them;
3.  Grouped them into four dimensions: "Major Features / Usage Management / New Providers / Bug Fixes";
4.  Extracted the corresponding technical details and configuration methods for each feature;
5.  Generated the article following the table format and footnote style commonly used in my blog.

Throughout the entire process, I didn't add any prompts midway, nor did I manually intervene to adjust the direction.

The final generated article, although still requiring some polishing from me, already had a structure, content completeness, and technical detail level very close to publishable.

Final cost: **¥0.24**.

## What's Good About Pi + DeepSeek

I believe it's best suited as a supplement to tools like `Codex` and `Claude Code`, rather than a complete replacement.

It has several main advantages.

First, **cost transparency**.

The cost of each API call is clearly visible every time. Unlike subscription-based tools, you won't suddenly find your quota running out mid-use, nor will you start worrying about the bill only at the end of the month.

Second, **no soft limits**.

The advantage of direct API connection is that you pay for what you use. As long as there's a balance in your account, you can continue running tasks without suddenly being blocked because your monthly quota is depleted.

Third, **model flexibility**.

You can choose different models based on the task.  
For writing code, you can use `DeepSeek`; for analyzing long Chinese texts, you can switch to `Qwen`; and for other tasks, you can connect different providers.

In contrast, `Codex` primarily revolves around OpenAI's own model ecosystem. It offers a more complete experience, but less freedom in choice.

Fourth, **open source**.

`Pi`'s code is at [badlogic/pi-mono][2]. It supports TypeScript extensions and `Pi Packages`, and you can even package and share your own Skills.

This is very important to me because it's not a completely closed product, but rather a tool that can be tinkered with, extended, and integrated into my workflow.

## Of Course, It's Not Without Its Hurdles

The biggest issue with `Pi + DeepSeek` is that it requires a bit of manual configuration.

You need to apply for an API Key, top up your balance, and then integrate the model. The whole process isn't difficult, but it's definitely an extra step compared to directly subscribing to `Codex` or `Claude Code`.

Additionally, `Pi` is a terminal tool, not a graphical IDE.  
If you're already accustomed to the more complete product experience of `Cursor`, `Copilot Chat`, or `Codex`, you might find it a bit 'rudimentary' at first.

But for me, this isn't an issue. Because what I need isn't a full IDE, but a backup tool that can help me continue running tasks when my quota is tight.

## My Usage Positioning

I haven't given up on `Codex` because of this.

`Codex` remains one of my primary tools, after all, I've already paid for it, and its overall experience, context handling, and product completeness are still very strong.

However, when `Codex`'s quota is tight, or when I need to run some batch tasks, such as:

- Organizing GitHub issues;
- Generating article drafts;
- Analyzing changelogs;
- Batch generating tests;
- Performing low-risk refactoring;

`Pi + DeepSeek` is very well-suited to step in.

It's not meant to replace `Codex`, but rather to take over tasks that are 'valuable, but not worth consuming premium quota' for.

## Final Thoughts

For twenty-four cents, I wrote a pretty good article.

This experience didn't make me think 'AI is cheap again,' but rather: **When AI call costs are low enough, our perception of task value changes.**

Previously, you might have thought that organizing a batch of issues, writing a first draft, or analyzing historical records could be done by a free AI Chat, then copied over, and wasn't worth specifically handing over to an AI Code Agent to run.

But if it only costs a few cents per task, these things suddenly become worthwhile.

Therefore, `Pi + DeepSeek` is a very practical backup solution for me.

If you're already using `Codex`, `Claude Code`, or `Copilot`, but frequently get stuck due to quota limits, you might try `Pi + DeepSeek` or `Pi + Qwen`.

Spend ten minutes setting it up, and you might gain an affordable, stable, and always-ready AI programming assistant.

[1]: https://pi.dev
[2]: https://github.com/badlogic/pi-mono