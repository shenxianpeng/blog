---
title: "30,000 Merges a Day on One Side, Back to Hand-Coding on the Other"
summary: |
  A company on V2EX banned AI coding after AI-written code caused a production incident, while Anthropic's daily merged changes grew from 2,500 to over 30,000. The difference isn't the AI, it's the checkpoints. My call: within a year most software companies will be turned upside down, and the people who remain are the ones trusted to sign off.
tags:
  - AI
  - DevOps
  - Thoughts
authors:
  - shenxianpeng
date: 2026-11-22
---

This week a thread on V2EX, a Chinese developer forum, was titled ["My company banned AI coding outright, and overnight we're back to hand-coding the old-fashioned way"](https://www.v2ex.com/t/1258200).

The poster said a colleague's AI-written code passed review, went to production, broke, and users complained in droves.

The boss was furious and banned using AI to generate code directly. It can be used to analyze problems and propose solutions, nothing more. His words: I'd rather be slow than have things break.

Over two hundred replies, and a lively fight.

Two things came to mind when I read it.

First, maybe the model wasn't smart enough, wrote something broken, and the people reviewing it didn't catch it either.

Second, flip it around: going back to writing code by hand can break things just the same. If review doesn't catch the problem, it slips through no matter who wrote the code.

One of the most-liked replies put it more bluntly: AI produces code so fast that the old review and release process simply can't keep up.

I think that's the company's real problem. Writing a lot of code with AI isn't wrong. Having too few places to check it is.

AI-native companies have run into the same problem, at a much larger scale.

At Anthropic, as of May this year, [over 80% of the code merged into the main codebase was written by Claude](https://www.anthropic.com/institute/recursive-self-improvement). Company-wide daily merged changes went from about 2,500 in May to [more than 30,000 by September](https://www.anthropic.com/research/redesigning-source-control). They also say that if people can't review code as fast as Claude writes it, human review will become the bottleneck.

So every PR first goes through an automated Claude review. Looking back at past claude.ai incidents, they estimate this step would have caught about a third of the bugs.

One of their engineering posts says that very often, the engineers' role was to tell Claude "no."

OpenAI is much the same. Internally they run an ["agentic software factory"](https://newsletter.pragmaticengineer.com/p/openai-software-factory): writing code, writing tests, fixing CI, waiting on review, all done by Codex. High-risk changes still need a human after the AI has looked at them, and someone has to make the call before anything hits production.

A few days ago I saw a line on X: straight from Claude Code to production. Honestly, for the less critical things I build in my spare time, like my personal site and project websites, that's pretty much how I work. For the things that matter, I don't.

One merges 30,000 changes a day; the other goes back to hand-coding. The difference isn't the AI. It's the checkpoints.

Can that company keep writing code by hand forever? No way. Once efficiency goes up, it doesn't come back down. Make someone used to AI type every line again and they'll feel their life is being wasted.

With the checkpoints in place, people only need to stand at the two ends: say clearly what you want at the start, and decide whether it ships at the end. The long stretch in between goes to AI.

So here's my call: within a year, most software companies will be turned upside down. At the rate AI works now, at least two-thirds of the people aren't needed.

That long stretch in the middle used to be full of people. More people means more communication, and efficiency actually drops.

If a company still runs this process today: product managers write requirements, a Grooming meeting breaks them into stories, a Planning meeting schedules the sprint, developers write code, QA tests, a docs team writes docs, and finally ops releases it. To me, that's a whole era behind.

Why is all this still around? It's like the turnstiles installed in so many places. Once they're up, everyone swipes through every day and gets used to them. Removing one takes a very good reason, plus taking responsibility for removing it, and for anything that goes wrong afterwards. Keeping it requires no explanation at all.

By banning AI, that company on V2EX got another turnstile, when what it actually needed was a checkpoint. A turnstile stops everyone. A checkpoint stops things by risk.

Once all of this is torn down, who's still needed?

Junior people, I can say with certainty, are no longer needed. Junior work, and even mid-level work, AI already covers.

The ones who remain are the ones who can sign off: close to customers and know what's worth building; with judgment and taste to tell whether what AI wrote is heading the right way and whether the architecture makes sense; willing to say "this can ship" or "this can't," and to own that call.

What these people have in common I call qualification.

Last month Gregory Kurtzer, the creator of CentOS, used OpenAI's Codex to write [a new kernel called Ginux](https://itsfoss.com/news/ginux/) in 11 days. It now has over six hundred stars [on GitHub](https://github.com/gmkurtzer/ginux). Had someone nobody knows done the same thing, it probably wouldn't have drawn nearly as much attention.

The difference is that he was building CentOS over twenty years ago, then Rocky Linux, and companies have run them in production for years.

It's the same inside a company. When you say "this can go live," whether your colleagues and your manager believe you doesn't depend on how much code you had AI write today. It depends on whether the calls you made before ever went wrong.

The code takes 11 days. The qualification takes a whole career.

## References

- [V2EX, "My company banned AI coding outright, and overnight we're back to hand-coding the old-fashioned way" (in Chinese)](https://www.v2ex.com/t/1258200)
- [Anthropic, "When AI builds itself" (as of May 2026, over 80% of merged code written by Claude; human review becomes the bottleneck if people can't keep up; every change goes through automated Claude review, estimated in hindsight to catch about a third of the bugs behind past claude.ai incidents)](https://www.anthropic.com/institute/recursive-self-improvement)
- [Anthropic, "Redesigning source control at Anthropic" (2026-10-13; daily merged changes 2,500 → 30,000+; "very often, the role of the engineers was to tell Claude no")](https://www.anthropic.com/research/redesigning-source-control)
- [The Pragmatic Engineer, "Inside OpenAI's agentic software factory" (2026-09-15)](https://newsletter.pragmaticengineer.com/p/openai-software-factory)
- [It's FOSS, coverage of Ginux (2026-10-27)](https://itsfoss.com/news/ginux/)
- [Ginux repository](https://github.com/gmkurtzer/ginux)

---

Please credit the author and source when reprinting articles from this site. Do not use for any commercial purposes. Welcome to follow the official WeChat account 「沈显鹏」.
