---
title: DeepSeek V4—Bringing Down the Cost of Using Coding Agents
summary: |
  This month, Codex renewed automatically. I hadn't really planned on continuing the subscription, but this renewal made me re-evaluate the actual experience with Codex, the DeepSeek V4 series, and Copilot. For me, the core difference in AI programming tools is no longer just about model capabilities, but about which one can help me write code more stably, affordably, and continuously.
tags:
  - AI
  - DeepSeek
  - Codex
  - Coding Agent
authors:
  - shenxianpeng
date: 2026-05-11
---

This month, Codex accidentally renewed again.

I didn't actively renew it; I forgot to cancel the subscription. When I saw the debit notification, my first reaction was:

**This money isn't worth spending.**

Originally, I wasn't really planning to continue subscribing to Codex. GitHub Copilot isn't available for me to subscribe to right now either, so I was thinking of either trying Claude or simply not subscribing to anything for a while.

> A side note here: I don't recommend annual subscriptions. Code Agents are updated daily, and you need to switch between them to appreciate the differences.

But since the money was already spent, I continued using it for a while.

After using it, I became even more certain of one thing:

**Codex is decent, but it's no longer the indispensable tool for my daily coding.**

## Codex is Okay, but Not Irreplaceable

Recently, there have been many articles about Codex.

Tutorials, reviews, comparisons, best practices—you can basically find a new one every few days. Many people are saying how powerful and good it is, even better than Claude Code.

I don't deny Codex's capabilities.

Its interactive experience, desktop application, and task execution capabilities are all good. But from my personal usage scenarios, Pi + DeepSeek V4 series is so powerful that it's irreplaceable.

I mainly use AI for these tasks:

- Maintaining open-source projects
- Refactoring code
- Adding tests
- Fixing bugs
- Modifying CI/CD configurations
- Writing documentation and READMEs
- Understanding an unfamiliar project

Most of these tasks are now completed using the Pi + DeepSeek V4 series.

![DeepSeek性能对比](benchmark.png)

Overall, my experience with DeepSeek is that it feels like:

**It's abundant, satisfying, and good enough to use.**

Before, I used to think that the main difference in AI programming tools lay in model capabilities.

Now I feel that model capability is just the foundation. What truly impacts daily use are cost, quotas, speed, and toolchain adaptation.

## The Cost Difference is Obvious

Let's talk about DeepSeek first.

I started using DeepSeek quite frequently from late April. So far, I've topped up a few times, each time 10 RMB, totaling about 40 RMB.

![五月份花费](cost.png)

My personal experience can be summed up in one sentence:

**I can't even use it all up.**

Now, let's look at Codex.

Since it renewed this month, it would be a waste not to use it, so I intentionally look for projects for Codex to work on.

But the problem is also obvious: if I focus on one project, the quota can easily run out in about an hour. The weekly limit is already used up, and I have to wait another day to use it.

If I want a higher quota, I'd have to consider the more expensive Pro tier. For me personally, that's not very cost-effective.

## I'm More Concerned About Continuous Availability Now

Once a Coding Agent enters the workflow, it's not as simple as just asking a few questions occasionally.

It continuously reads code, writes code, runs tests, modifies documentation, analyzes errors, and understands context.

All of these consume tokens.

If a tool is very powerful but you always have to think "be frugal with it" every time you use it, then its value in actual work is diminished.

Conversely, if a model is cheaper and good enough, I'm more willing to integrate it into my daily workflow.

This is how I feel about using DeepSeek now.

If I have an idea, I let it analyze it directly.

If code needs changing, I let it do it directly.

If the results aren't satisfactory, I keep asking.

This kind of worry-free usage experience is very important for Coding Agents.

## Why Did ds4 Suddenly Become Popular?

Recently, there's a very popular project on GitHub called ds4.

It's a local inference engine for DeepSeek V4 Flash, created by Redis author antirez, also known as Salvatore Sanfilippo. The project quickly became popular, and now has over 6k stars on GitHub.

I think there are several reasons why this project became popular.

First, the author himself is very influential.

antirez is the author of Redis, and projects he creates naturally attract a lot of attention from developers.

Second, unlike ollama, ds4 focuses solely on the DeepSeek V4 Flash model.

This indicates that DeepSeek V4 Flash is no longer just an ordinary "cheap model". It has reached a point where influential system-level developers are willing to build dedicated inference engines around it.

Third, the direction of local inference is very attractive.

If such models can run more stably on local machines in the future, the API call cost for Coding Agents would significantly decrease. Although hardware, memory, electricity, and maintenance costs still exist, for many developers, this is already a very promising direction.

So the popularity of ds4 also indicates: **developers recognize high-cost-performance models like DeepSeek V4 Flash.**

## What about Copilot?

If GitHub Copilot becomes available for smooth subscription again in the future, I might still consider continuing to use it.

The reason is simple: Copilot's native integration with GitHub is excellent.

You open a repository, and Copilot can analyze issues, modify code, and submit PRs. This experience is currently hard for other tools to fully replace.

Copilot's advantage isn't just a strong model; it's that it's deeply integrated into the GitHub workflow.

This is very important for developers.

However, Copilot also has its own issues. Its billing and quota rules are changing. For those who frequently use AI programming tools, future costs and restrictions still need careful consideration.

That's why I've also been making my own attempt recently.

## RepoKeeper: My Own Attempt

This is also one of the reasons I recently created [RepoKeeper](https://github.com/shenxianpeng/repokeeper).

I hope it can become a more flexible entry point for GitHub Coding Agents.

Compared to Copilot, RepoKeeper's biggest advantage isn't being more native, but being more flexible.

For example:

1.  **Backend can be customized**

    Currently, it can connect to Pi, and later it can also connect to OpenCode, or other Agent backends.

2.  **Models can be chosen by yourself**

    You can use DeepSeek, or Qwen, Kimi, or other more cost-effective models.

3.  **Costs are more controllable**

    You don't necessarily have to be tied to the subscription and quotas of a single platform.

Of course, RepoKeeper is not as out-of-the-box ready as Copilot yet.

Copilot is a native GitHub product; it works immediately in any repository. RepoKeeper still requires configuring workflows, tokens, and backends first.

But these are all one-time tasks.

Once configured, it can become a more flexible AI programming entry point.

This is also the direction I want to continue exploring:

**AI Coding Agents don't necessarily have to be tied to a single platform.**

In the future, developers might need a more flexible way to connect different models, different agents, and different repository workflows.

## Finally

If you also use AI programming frequently, and model inference capabilities are strong at this stage, the most important questions have become:

**Who can let me keep using it?**

**Whose costs can I accept?**

**Who can stably integrate into my daily development workflow?**

From this perspective, the DeepSeek V4 series is well worth serious consideration.

It's powerful enough, cheap enough, and suitable enough for high-frequency use.

Especially for friends in China, if accessing Claude is inconvenient, subscribing to Codex is inconvenient, or you don't want to be stuck with various quota limitations, then you can definitely try a combination like this:

**A handy AI programming tool + DeepSeek V4 series models.**

> Of course, cost-effective models also seem good, such as Qwen, Kimi, GLM. I will try using them as the brain for my Coding Agent later.

My feeling is:

**Model capability is no longer the only barrier.**

What's truly important is whether you can integrate AI into your daily development workflow and use it consistently, stably, and affordably in the long term.

At least for me, the DeepSeek V4 series has achieved this.

So next month, I will most likely cancel Codex.

I'd rather put this money towards DeepSeek, Qwen, GLM, Kimi, and other models.