---
title: From Praising to Bashing—My Attitude Shift Towards GitHub Copilot
summary: |
  Recently, my attitude towards GitHub Copilot has undergone a significant change: from "praising" to "bashing." After comparing it with Claude Code, I've found that Copilot has clear deficiencies in cross-repository support and "senior engineer" awareness, to the point where I'm no longer willing to discuss problems with it.
tags:
  - AI
  - GitHub Copilot
  - Claude Code
authors:
  - shenxianpeng
date: 2026-07-20
---

Recently, my attitude towards GitHub Copilot has undergone a significant change: from "praising" to "bashing." ([Previous article praising Copilot](/posts/2025/copilot/))

This shift happened in the past few days because my Claude Code subscription expired, and I planned to resubscribe and returned to GitHub Copilot, which I hadn't used for a long time. It must be stated that my dissatisfaction with it is limited to my specific work scenarios, but perhaps it also represents a common pain point for many.

Compared to Claude Code, GitHub Copilot's shortcomings are mainly reflected in the following two aspects:

## Lack of Multi-Repository Association and Cloud/Mobile Support

Most of my usage scenarios involve using it directly on my phone without turning on my computer. When starting a Session, Claude Code allows me to add all associated repositories (especially when you're working on projects within a GitHub Organization, where project interdependencies can sometimes be very tight).

Claude Code analyzes different projects and can modify code and submit Pull Requests across repositories, which is extremely convenient.

Currently, GitHub Copilot does not seem to possess such cross-repository processing capabilities. While you might achieve similar functionalities locally, it doesn't appear to support them in mobile or cloud environments, which is a crucial missing feature.

## Lack of "Senior Engineer" Awareness

Claude Code is more like a senior engineer; in communication, you don't need to be exhaustive, and it just has the "sense" to do things beautifully.

For example, when you ask it to modify code, it will submit a PR for you based on your previous actions, monitor CI success, and automatically perform the next follow-up steps after merging. The entire process is very smooth.

In contrast, GitHub Copilot's logic is sometimes incredibly unintelligent. Once it opened a PR for me, I was dissatisfied with the changes and closed it. When I proceeded with the next modification, it surprisingly continued to make changes based on the history of the previous branch I had closed, directly reintroducing the changes I had rejected into the next PR.

While such issues can be resolved by adding instructions in the Prompt (e.g., requiring it to always check out from the main branch), this is precisely the difference between a "senior engineer" and a "junior engineer":

- **Senior Engineer:** Understands the intent without you needing to provide too many details.
- **Junior Engineer:** You must instruct them step-by-step on what to do and what not to do under certain circumstances.

After using Claude Code, I find that having to painstakingly teach an AI these basic logics is incredibly exhausting. So, my current advice is: if you can use Claude Code, definitely use it over other tools.

## Model Limitations

Finally, regarding the models, GitHub Copilot does not include some of the latest versions from OpenAI and Anthropic (such as Fable, Opus 4.8, Sonnet 4.8, etc.), at least not in the Pro plan. This is also quite a regret.

This has led me to no longer want to discuss problems with it, because the results of discussions with it are often inappropriate or unusable, feeling like a waste of time.

I'll let it help me with some other tasks with the remaining tokens; after all, it still has some value in certain aspects.

---

Please cite the author and source when reprinting articles from this site. Do not use for any commercial purposes. Welcome to follow the official account "沈显鹏".