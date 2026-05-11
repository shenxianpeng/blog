---
title: DeepSeek V4—Bringing Down the Cost of Using Coding Agents
summary: |
  Codex auto-renewed this month. I wasn't really planning to continue my subscription, but this renewal made me re-evaluate the actual experience of Codex, DeepSeek V4 series, and Copilot. For me, the core difference in AI programming tools is no longer just model capability, but rather which one can help me write code more stably, cheaply, and continuously.
tags:
  - AI
  - DeepSeek
  - Codex
  - Coding Agent
authors:
  - shenxianpeng
date: 2026-05-10
---

Hello everyone, I'm Shen Gong.

Codex renewed again this month.

I didn't renew it actively; I forgot to cancel the subscription. When I saw the debit notification, my first reaction was:

**This money wasn't well spent.**

I wasn't really planning to continue subscribing to Codex. GitHub Copilot isn't available for subscription on my end right now either, so my original thought was to either try subscribing to Claude or just not subscribe to anything for now.

> A side note here: I don't recommend annual subscriptions. Code Agents are updated daily; using different ones allows you to experience the differences.

But since the money was already spent, I continued using it for a while.

After using it, I became even more certain of one thing:

**Codex is great, but it's no longer the indispensable tool for my daily coding.**

## Codex is Good, But Not Irreplaceable

There have been many articles about Codex recently.

Tutorials, reviews, comparisons, best practices—you can basically find one every few days. Many people are saying how powerful and good it is, even better than Claude Code.

I don't deny Codex's capabilities.

Its interactive experience and task execution capabilities are good. But from my own use cases, Pi + DeepSeek V4 series is what's truly strong to the point of being irreplaceable.

I usually use AI for these tasks:

- Maintaining open-source projects
- Refactoring code
- Adding tests
- Solving Bugs
- Modifying CI/CD configurations
- Writing documentation and READMEs
- Understanding an unfamiliar project

Most of these tasks are now completed using Pi + DeepSeek V4 series.

Overall, DeepSeek gives me the feeling that:

**It's abundant, satisfying, and good enough to use.**

I used to think that the difference in AI programming tools mainly lay in model capabilities.

Now, I rather think that model capability is just the foundation. What truly affects daily use are cost, quotas, speed, and toolchain adaptation.

## The Cost Difference is Obvious

Let's talk about DeepSeek first.

I started using DeepSeek quite frequently since late April. So far, I've topped up a few times, 10 RMB each time, totaling about 40 RMB.

My experience can be summed up in one sentence:

**It's simply inexhaustible.**

Especially models like DeepSeek V4 Flash, which are designed for high-frequency use. Not only is it cheap, but it's also already smooth enough for many daily coding tasks.

Now, looking at Codex.

Since it's already renewed this month, it would be a waste not to use it, so I intentionally look for some projects to give tasks to Codex.

But the problem is also obvious: if I focus on one project, the quota easily runs out after an hour or two. My weekly limit is already used up, and I have to wait another day to use it.

If I want a higher quota, I have to consider the more expensive Pro tier. For me personally, that's not very cost-effective.

## What I Care More About Now is Continuous Availability

Once a Coding Agent enters the workflow, it's not as simple as just asking a few questions occasionally.

It continuously reads code, writes code, runs tests, modifies documentation, analyzes errors, and understands context.

All of these consume tokens.

If a tool is very powerful, but every time you use it, you have to think about 'saving it,' then its value in actual work will be discounted.

Conversely, if a model is cheaper and good enough, I'm more willing to put it into my daily workflow.

This is how I feel using DeepSeek now.

Think of a point, let it analyze directly.

Need to modify code, let it do it directly.

Not satisfied with the result, keep asking.

This kind of usage experience without psychological burden is very important for Coding Agents.

## Why Did ds4 Suddenly Become Popular?

Recently, there's been a very popular project on GitHub called ds4.

It's a local inference engine for DeepSeek V4 Flash created by Redis author antirez, also known as Salvatore Sanfilippo. The project quickly became popular, and now has over 6k stars on GitHub.

I think there are several reasons why this project became popular.

First, the author himself is very influential.

antirez is the author of Redis, and projects he creates naturally attract a lot of developer attention.

Second, unlike ollma, ds4 focuses only on the DeepSeek V4 Flash model.

This indicates that DeepSeek V4 Flash is no longer just an ordinary "cheap model." It has reached the point where influential system-level developers are willing to build dedicated inference engines around it.

Third, the direction of local inference is very attractive.

If such models can run more stably on local machines in the future, the API call costs for Coding Agents will significantly decrease. Although hardware, memory, electricity, and maintenance costs still exist, for many developers, this is already a very promising direction.

Therefore, the popularity of ds4 also shows that: **developers recognize high-performance-to-price ratio models like DeepSeek V4 Flash.**

## What About Copilot?

If GitHub Copilot can be smoothly subscribed to again in the future, I might still consider continuing to use it.

The reason is simple: Copilot's native GitHub integration is excellent.

You can open a repository and have Copilot analyze issues, modify code, and submit PRs. This experience is currently difficult for other tools to completely replace.

Copilot's advantage is not simply that the model is powerful, but that it's already integrated into the GitHub workflow.

For developers, this is very important.

But Copilot also has its own issues. Its billing and quota rules are also changing. For those who frequently use AI programming tools, subsequent costs and limitations still need careful consideration.

That's why I've also been making my own attempt recently.

## RepoKeeper: An Attempt of My Own

This is also one of the reasons why I've been working on [RepoKeeper](repokeeper) recently.

I hope it can become a more flexible GitHub Coding Agent entry point.

Compared to Copilot, RepoKeeper's biggest advantage is not being more native, but being more free.

For example:

1.  **Backend can be customized**

    Currently, it can connect to Pi, and later it can also connect to OpenCode, or other Agent backends.

2.  **Models can be self-selected**

    You can use DeepSeek, or Qwen, Kimi, or other more cost-effective models.

3.  **Costs are more controllable**

    No need to be tied to a specific platform's subscription and quotas.

Of course, RepoKeeper is not as out-of-the-box as Copilot yet.

Copilot is a native GitHub product; it works immediately upon entering any repository. RepoKeeper still requires configuring workflow, token, and backend first.

But these are one-time tasks.

Once configured, it can become a more free AI programming entry point.

This is also the direction I want to continue exploring:

**AI Coding Agents don't necessarily have to be tied to a single platform.**

In the future, developers may need a more flexible way to connect different models, different Agents, and different repository workflows.

## What I Really Want to Say

Writing this article is not to prove that Codex is bad.

Codex is a good tool.

Claude is also a good model.

Copilot still has strong product advantages.

But for someone like me who frequently uses AI programming tools, the most important questions have become:

**Who can let me keep using it?**

**Whose cost can I accept?**

**Who can stably integrate into my daily development workflow?**

From this perspective, the DeepSeek V4 series is very worth serious consideration.

It's strong enough, cheap enough, and suitable enough for high-frequency use.

Especially for friends in China, if accessing Claude is inconvenient, subscribing to Codex is inconvenient, or if you don't want to be stuck by various quota limits, then you can definitely try this combination:

**A handy AI programming tool + DeepSeek V4 series models.**

My feeling is:

**Model capability is no longer the only barrier.**

What's truly important is whether you can integrate AI into your daily development workflow and use it long-term, stably, and at a low cost.

At least for me, the DeepSeek V4 series has achieved this.

So next month, I will most likely cancel Codex.

I'd rather continue topping up DeepSeek with this money.

Veterans, see you next time~

[1]: https://github.com/antirez/ds4 "GitHub - antirez/ds4: DeepSeek 4 Flash local inference engine for Metal · GitHub"
[2]: https://api-docs.deepseek.com/news/news260424 "DeepSeek V4 Preview Release | DeepSeek API Docs"
[3]: https://developers.openai.com/codex/pricing "Pricing – Codex | OpenAI Developers"