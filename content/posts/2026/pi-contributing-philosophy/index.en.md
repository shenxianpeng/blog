---
title: pi Project's Counter-Intuitive Design—From AGENTS.md to 'Close Your PR First'
summary: |
    After reading Mario Zechner's "I've sold out" and browsing through AGENTS.md and CONTRIBUTING.md in the pi repository, I found that this project deviates significantly from common open-source collaboration practices in many aspects. New contributors' issues and PRs are closed by default, no reviews on weekends, and don't submit PRs if you don't understand the code. It seems tough, but behind it is a serious attempt to address a problem: in the AI era, how can open-source projects avoid being bogged down by low-quality contributions?
tags:
  - AI
  - Open Source
  - pi
authors:
  - shenxianpeng
date: 2026-04-26
---

Last weekend, I wrote an article titled [Using pi + DeepSeek as a Codex backup solution](/posts/2026/pi-deepseek/).

After finishing it, I took the opportunity to look through other content related to the pi project. It turns out that the truly interesting aspect isn't just the tool itself, but the collaboration method behind it.

Especially its AGENTS.md and CONTRIBUTING.md. After reading them, I was a bit surprised.

Many of the project's rules are almost the opposite of what we usually understand about open-source communities.

*   New contributors' issues and PRs are closed by default.
*   Issues submitted on weekends are not processed.
*   If you don't understand the code you submitted, the PR will be closed directly.

These rules seem rigid, but when viewed in conjunction with Mario Zechner's recent article, it becomes clear that it's not simply "unwelcoming to contributors," but rather a serious consideration of one thing:

**In the AI era, how can open-source projects be sustainably maintained?**

## Starting with Mario's Blog Post

On April 8th, Mario Zechner, the author of pi, published a blog post: [I've sold out][1].

The title is a bit self-depdeprecating, but the content is very sincere.

In the article, he recounted his open-source journey, which began in 2009. First, there was [libGDX][2], a cross-platform game development framework that was once a popular game engine on Android, used by Ingress and Slay the Spire.

Later, he participated in a startup called RoboVM, which built a JVM to iOS AOT compiler. Then, RoboVM was acquired by Xamarin, Xamarin was acquired by Microsoft, and Microsoft eventually shut down RoboVM.

As the "OSS guy" at the time, Mario had to write that "sorry, no longer open-source" announcement. The outcome, as one can imagine, was that he was heavily criticized on social media and via email.

The problem was, this decision was not within his control.

This experience gave him a very clear understanding of the relationship between VCs, startups, and open source. To put it more bluntly, he had been educated by reality.

So when pi suddenly exploded in popularity due to [OpenClaw][3], attracting more and more VCs, large companies, and potential investors, he wasn't facing a simple "to monetize or not to monetize" question. Instead, it was a problem he had already encountered before:

If an open-source project suddenly gains commercial value, what should happen next?

His final choice was not to start his own company, but to join [Earendil][4].

The reason was simple: he has a four-year-old child. He wants to accompany his child as they grow up.

If he were to become a CEO himself, the next steps would be finding co-founders, finding PMF, building a team, establishing company culture, dealing with various people and money issues, and then slowly stopping writing code, becoming a "manager" he dislikes.

By joining Earendil, he can continue to write code and maintain pi, while also having a team to help him handle commercialization.

Mario also stated in his article: the core code of pi will continue to be under the MIT license, allowing forking, usage, and building products upon it. If one day the direction is wrong, the fork button is still there.

Because he personally witnessed the libGDX community fork MobiVM after RoboVM was closed source, he knows that this can indeed happen.

## Armin Ronacher's Involvement

Another key reason Mario joined Earendil was Armin Ronacher.

If you've written Python Web, you've likely seen the ID @mitsuhiko. He is the creator of [Flask][5] and also wrote Jinja2, Click, Werkzeug, and other very important projects in the Python ecosystem. At the same time, he is a co-founder of [Sentry][6] and has practical experience with "how to commercialize open-source projects."

Armin also wrote an article welcoming Mario to Earendil: [Mario and Earendil][7].

His evaluation of pi: pi doesn't attract people by being the loudest or fastest, but rather it shows that the author cares about software quality, design sense, extensibility, and long-term maintenance.

Many current AI coding tools give the impression of: release first, occupy the niche, build up the buzz. As for whether the design is unified, the code is clean, or if it can be maintained long-term, these often get pushed to the back.

pi feels different.

It's not the best at promotion, but the more you look into the repository, the more you can feel the author's demand for engineering details.

Mario and Armin have known each other for over a decade. They first debated on Reddit's r/austria subreddit, later met in person, and gradually became friends. After the explosion of AI coding tools in 2025, Steinberger, Mario, and Armin often communicated, experimented, and reviewed each other's blog posts, later being playfully dubbed the "Vienna Coding Agent School."

This background is also quite important.

Many business collaborations appear to happen suddenly, but often, they are the result of long-term trust. Especially for open-source projects, once ownership, trademarks, agreements, and future roadmaps are involved, a mere contract is not enough.

You have to trust that the people you work with won't mess things up.

## AGENTS.md: An Onboarding Manual for AI Agents

The pi repository contains an [AGENTS.md][8] file.

I initially just casually clicked on it, but then discovered it was written with incredible detail.

It specifies the rules that AI agents must follow when participating in pi development, including:

-   Replies should be concise, no emojis, no fluff
-   Do not use `any` type casually
-   Do not use inline `import`
-   Do not delete or downgrade code to bypass type errors
-   Run `npm run check` after modifying code
-   Do not delete seemingly "useless" code without understanding it
-   Which files to modify and tests to add when introducing a new LLM Provider
-   When multiple agents work in parallel, do not use `git add -A`
-   Do not use `git stash`
-   Do not use `git reset --hard`
-   How the release process should be followed

These rules seem very detailed, even a bit verbose, but if you've actually used coding agents, you'll know they are very necessary.

Current agents don't lack the ability to write a lot of code; they lack the ability to write high-quality code.

Some rules cannot be temporarily supplemented by prompts, as this can easily lead to omissions. The value of AGENTS.md lies here: it compiles the project's engineering habits into a fixed context.

This provides AI agents with an "operation manual."

If your project has also started extensively using AI coding tools, you might seriously consider pi's approach and write an AGENTS.md for your own project.

You don't need to start by writing something overly complex. Just listing the few most common pitfalls can already reduce a lot of ineffective modifications and token waste.

## CONTRIBUTING.md: Close Your PR First

If AGENTS.md is written for machines, [CONTRIBUTING.md][9] is written for humans—direct in its wording, without ceremony.

**1. Don't submit if you don't understand.** Using AI to write code is fine, but if you can't explain what your PR does and how it interacts with the system, it will be closed directly. The time you save with AI should not become a cost for maintainers to cover for you.

**2. Newcomers are closed by default.** All new contributors' issues and PRs are automatically closed. Want to "be promoted"? It's based on trust markers replied by a maintainer in the issue—not a GitHub label, but the comment content: reply `lgtmi`, and future issues will no longer be automatically closed; reply `lgtm`, and both issues and PRs will no longer be automatically closed. Maintainers browse closed issues daily, picking out valuable ones to reopen and mark. pi is not rejecting new contributors; it's asking you to first prove your submission is worth reviewing—agents are making the cost of creating issues/PRs increasingly low, so the bar becomes increasingly important.

**3. No processing on weekends.** Issues submitted from Friday to Sunday are automatically closed and do not enter the Monday review queue. If urgent, go to Discord. The explanation in the FAQ is straightforward: *"Maintainers need uninterrupted time away from the issue tracker."*

**4. Two rule violations lead to a ban.** If you disregard CONTRIBUTING.md twice, or use an agent to spam the issue tracker, you will be permanently banned from the Pi project.

## The Logic Behind These Rules

On the surface, pi's rules make it seem unwelcoming to contributors and community participation.

But by continuing to read the CONTRIBUTING.md FAQ, one can see the real problem it aims to solve.

The number of issues pi receives already exceeds what maintainers can seriously review in real-time. Many issues do not meet quality requirements or comply with CONTRIBUTING.md. Even more troublesome, some content is directly dumped into the repository by agents without much thought.

This is a problem that many projects will find increasingly difficult to deal with.

AI lowers the cost of writing code and issues but does not automatically improve submission quality.

In fact, much of the time, it makes low-quality content appear more like high-quality content. The format is complete, the tone is polite, and the text is fluent, but the problem might be wrong, redundant, irreproducible, or require maintainers to spend a lot of time verifying.

This is dangerous for open-source maintainers.

Because every seemingly "okay" issue might hide a cost.

*   You have to read it.
*   You have to judge it.
*   You have to reproduce it.
*   You have to reply.
*   You have to explain why it's not accepted.

These are all maintenance costs. Therefore, pi's auto-closing mechanism is essentially creating a buffer for maintainers.

Not everything immediately enters the formal review process; instead, it's initially blocked, and then maintainers pick out truly worthwhile content at their own pace.

This is connected to Mario's life choices mentioned in his blog post.

He doesn't want to live the kind of life where his child cries, saying "daddy isn't here." Many people on the Earendil team also have children, and the company culture emphasizes this.

This explains why pi's rules place such a strong emphasis on boundaries.

It's not simply to control contributors, nor to appear aloof, but to protect two things:

*   The maintainers' quality of life.
*   The project's code quality.

If these two cannot be preserved, an open-source project, no matter how lively it appears on the surface, can easily lead to burnout.

## What Value Does This Have for Your Project?

pi's approach may not suit all projects.

If a project is small and has few contributors, this barrier might be self-indulgent.

However, if your project has already started to be affected by AI-generated issues, AI-generated PRs, and low-quality automated submissions, then pi's approach is indeed worth considering.

But regardless of project size, here are some directly applicable points:

1.  **Write an AGENTS.md**

    If your project has started using AI coding agents, don't just rely on temporary prompts.

    Write down the project rules.

    For example, how tests are run, which commands should not be run, what the code style is, which directories should not be modified casually, and what must be checked before submitting.

    Putting this content into AGENTS.md is more stable than re-explaining it every time.

2.  **Specify quality requirements**

    Don't just write "high-quality contributions are welcome."

    Clearly state what kind of issues will be processed and what kind will be closed.

    For example:

    -   Must use an issue template
    -   Must describe what the problem is
    -   Must explain why it's important
    -   Bugs must provide reproduction steps
    -   Large features should be discussed first, don't submit a PR directly

    The more specific the rules, the lower the explanation cost for maintainers.

3.  **Protect maintainer time**

    Open-source maintenance is not customer service.

    Not all time should be response time.

    You can clearly state: only seek maintainer review after self-testing passes; low-quality issues are not guaranteed a reply.

    This might sound a bit cold, but it's much better than prolonged exhaustion leading to no desire to maintain the project.

4.  **Establish a trust mechanism**

    pi's issues and PRs for new contributors are closed by default, but can be unlocked after a maintainer's reply. Then, that person's ID will be recorded, and subsequent submissions will no longer be automatically closed.

## Finally

After reviewing pi's rules, my biggest takeaway is:

**For popular open-source projects, the scarce resource may no longer be contributors, but maintainers' time.**

Especially after the rise of AI Agents, the quantity of contributions might increase, but the quality may not improve proportionally.

At this point, what a project truly needs to protect might not be "welcoming more people to contribute," but rather "welcoming more valuable contributions."

pi's rules seem counter-intuitive, but they at least honestly confront this problem.

*   It doesn't pretend all contributions are good contributions.
*   Nor does it pretend maintainers' time is infinite.

Open-source projects in the AI era may need more such thinking and design to truly maintain sustainable maintenance and high-quality development.

[1]: https://mariozechner.at/posts/2026-04-08-ive-sold-out/
[2]: https://libgdx.com
[3]: https://openclaw.ai
[4]: https://earendil.com
[5]: https://flask.palletsprojects.com/
[6]: https://sentry.io
[7]: https://lucumr.pocoo.org/2026/4/8/mario-and-earendil/
[8]: https://github.com/badlogic/pi-mono/blob/main/AGENTS.md
[9]: https://github.com/badlogic/pi-mono/blob/main/CONTRIBUTING.md