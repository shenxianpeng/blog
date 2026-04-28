---
title: Counter-intuitive Designs in the pi project — From AGENTS.md to "Just Close Your PR First"
summary: |
    After reading Mario Zechner's "I've sold out" and then reviewing AGENTS.md and CONTRIBUTING.md in the pi repository, I found that this project differs from common open-source collaboration methods in many ways. New contributors' issues and PRs are closed by default, no reviews on weekends, and don't submit PRs if you don't understand the code. It seems tough, but behind it is a serious attempt to address a problem: how open-source projects can avoid being bogged down by low-quality contributions in the AI era.
tags:
  - AI
  - Open Source
  - pi
authors:
  - shenxianpeng
date: 2026-04-26
---

This weekend, I wrote an article titled [Using pi + DeepSeek as a Codex Backup Solution](/posts/2026/pi-deepseek/).

After writing it, I casually browsed other content of the pi project and found that the truly interesting part is not just the tool itself, but the set of collaboration methods behind it.

Especially its AGENTS.md and CONTRIBUTING.md caught me by surprise after reading them.

Many rules of this project are almost the opposite of how we usually understand open-source communities.

*   New contributors' issues and PRs are closed by default.
*   Issues submitted on weekends are not processed.
*   If you don't understand the code you submitted, the PR will be closed directly.

These rules seem tough, but when viewed in conjunction with Mario Zechner's recent article, it becomes clear that it's not simply "not welcoming contributors," but rather a serious consideration of one thing:

**How can open-source projects be sustainably maintained in the AI era?**

## Starting with Mario's Blog Post

On April 8th, Mario Zechner, the author of pi, published a blog post: [I've sold out][1].

The title is a bit self-deprecating, but the content is very sincere.

In the article, he reviewed his experience with open source since 2009. First, there was [libGDX][2], a cross-platform game development framework that was once a popular game engine on Android, used by Ingress and Slay the Spire.

Later, he participated in a startup called RoboVM, which created an AOT compiler from JVM to iOS. RoboVM was later acquired by Xamarin, which was then acquired by Microsoft, and Microsoft eventually shut down RoboVM.

As the "OSS guy" at the time, Mario had to write that "sorry, no longer open source" announcement. The results, as imagined, were harsh criticism on social media and in emails.

The problem was that this decision was not within his control.

This experience gave him a very clear understanding of the relationship between VCs, startups, and open source. To put it more bluntly, he had been educated by reality.

So when pi became popular due to [OpenClaw][3] and attracted increasing attention from VCs, large companies, and potential investors, he wasn't facing a simple "should I monetize" question, but a problem he had already encountered:

What happens if an open-source project suddenly gains commercial value?

His final choice was not to start his own company but to join [Earendil][4].

The reason is simple: he has a four-year-old child. He wants to be there for his child as they grow up.

If he were to become CEO himself, the next steps would involve finding co-founders, finding PMF, building a team, establishing company culture, dealing with various people and money issues, and then slowly stopping writing code, becoming a "manager" he dislikes.

By joining Earendil, he can continue to write code and maintain pi, while also having a team to help him with commercialization.

Mario also stated in his article: pi's core code will remain under the MIT license, allowing it to be forked, used, and products to be built upon it. If one day the direction is wrong, the fork button is still there.

Because he witnessed the libGDX community fork MobiVM after RoboVM was closed source, he knows this really happens.

## Armin Ronacher's Involvement

Another key reason for Mario joining Earendil was Armin Ronacher.

If you've written Python Web code, you've likely seen this ID @mitsuhiko. He is the creator of [Flask][5], and also wrote Jinja2, Click, Werkzeug, and other very important projects in the Python ecosystem. At the same time, he is a co-founder of [Sentry][6] and has practical experience in "how open-source projects are commercialized."

Armin also wrote an article welcoming Mario to Earendil: [Mario and Earendil][7].

His evaluation of pi: pi doesn't attract people by being the loudest or fastest, but rather it shows that the author cares deeply about software quality, design sense, extensibility, and long-term maintenance.

Many AI coding tools today give the impression of: release first, claim the spot first, build momentum first. As for whether the design is unified, the code is clean, or if it can be maintained long-term, these are often pushed to the back.

pi feels different.

It may not be the most promotional project, but the deeper you look into the repository, the more you can feel the author's high standards for engineering details.

Mario and Armin have known each other for over a decade. They first debated on Reddit's r/austria subreddit, later met offline, and gradually became friends. After the boom of AI coding tools in 2025, Steinberger, Mario, and Armin frequently communicated, experimented, and reviewed each other's blog posts, later being jokingly referred to as the "Vienna Coding Agent School."

This background is also quite important.

Many commercial collaborations appear to happen suddenly, but often, they are the result of long-term trust. Especially for open-source projects, once ownership, trademarks, agreements, and future roadmaps are involved, a contract alone is not enough.

You need to trust that the people you work with won't mess things up.

## AGENTS.md: An Onboarding Manual for AI Agents

The pi repository contains an [AGENTS.md][8] file.

I initially just clicked into it out of curiosity and found it to be very detailed.

It specifies the rules that AI agents must follow when participating in pi development, including:

-   Replies should be concise, without emojis or unnecessary words.
-   Do not arbitrarily use the `any` type.
-   Do not use inline `import`.
-   Do not delete or downgrade code to bypass type errors.
-   Run `npm run check` after modifying code.
-   Do not delete seemingly "useless" code without understanding it.
-   Which files to modify and which tests to add when adding a new LLM Provider.
-   When multiple agents work in parallel, do not use `git add -A`.
-   Do not use `git stash`.
-   Do not use `git reset --hard`.
-   How the release process should be followed.

These rules seem very detailed, even a bit verbose, but if you've actually used a coding agent, you'll know they are very necessary.

Current agents do not lack the ability to write code; they lack the ability to write high-quality code.

Some rules cannot be temporarily supplemented by prompts, which can easily lead to omissions. The value of AGENTS.md lies here: it compiles the project's engineering habits into a fixed context.

This gives AI agents an "operation manual."

If your project has also started extensively using AI coding tools, you might seriously consider pi's approach and write an AGENTS.md for your own project.

You don't need to make it complicated from the start. Just by writing down the few most common pitfalls, you can already reduce many invalid modifications and token waste.

## CONTRIBUTING.md: Just Close Your PR First

If AGENTS.md is written for machines, [CONTRIBUTING.md][9] is written for humans—the wording is direct and no-nonsense.

**1. Don't submit if you don't understand.** Using AI to write code is fine, but if you can't explain what your PR does and how it interacts with the system, it will be closed directly. The time you save with AI should not become the cost of maintainers having to clean up after you.

**2. Newcomers closed by default.** All new contributors' issues and PRs are automatically closed. Want to "be promoted"? It depends on a trust marker replied by a maintainer in the issue—not a GitHub label, but in the comment content: reply `lgtmi`, and future issues will no longer be automatically closed; reply `lgtm`, and both issues and PRs will no longer be automatically closed. Maintainers will browse closed issues daily, picking out valuable ones to reopen and mark. pi is not rejecting new contributors; it's asking you to first prove that your submission is worth reviewing—agents make the cost of creating issues/PRs lower and lower, making the barrier to entry increasingly important.

**3. Not processed on weekends.** Issues submitted from Friday to Sunday are automatically closed and do not enter the Monday review queue. If urgent, go to Discord. The explanation in the FAQ is straightforward: *"Maintainers need uninterrupted time away from the issue tracker."*

**4. Two rule violations lead to a ban.** If you disregard CONTRIBUTING.md twice, or flood the issue tracker with agents, you will be permanently banned from the Pi project.

## The Logic Behind These Rules

On the surface, pi's rules might make it seem unwelcoming to contributors and community participation.

But by continuing to read CONTRIBUTING.md's FAQ, you can see the real problem it aims to solve.

The number of issues pi receives has already exceeded what maintainers can seriously review in real-time. Many issues do not meet quality requirements and do not adhere to CONTRIBUTING.md. More troublingly, some content is directly dumped into the repository by agents without much thought.

This is a growing headache for many projects today.

AI lowers the cost of writing code and issues, but it does not automatically increase the quality of submissions.

In fact, much of the time, it makes low-quality content appear more like high-quality content. The format is complete, the tone is polite, and the text flows smoothly, but the problem might be wrong, redundant, irreproducible, or require maintainers to spend a lot of time verifying.

This is dangerous for open-source maintainers.

Because every seemingly "decent" issue could be a hidden cost.

*   You have to read it.
*   You have to judge it.
*   You have to reproduce it.
*   You have to reply.
*   You have to explain why it's not accepted.

These are all maintenance costs. Therefore, pi's automatic closing mechanism essentially creates a buffer for maintainers.

Not everything immediately enters the formal review process; instead, it's initially blocked, and then maintainers pick out truly valuable content at their own pace.

This is connected to Mario's life choices discussed in his blog.

He doesn't want to live a life where his child cries, "daddy isn't here." Many people on the Earendil team also have children, and the company culture emphasizes this.

This explains why pi's rules place such a strong emphasis on boundaries.

It's not simply to control contributors or to appear aloof, but to protect two things:

*   The quality of life for maintainers.
*   The quality of the project's code.

If these two things cannot be protected, an open-source project, no matter how lively it seems on the surface, can easily lead to burnout.

## What Value Does It Have for Your Project?

pi's approach may not suit all projects.

If a project is small and has few contributors, this barrier would be self-indulgent.

However, if your project is already being affected by AI-generated issues, AI-generated PRs, and low-quality automated submissions, then pi's approach is indeed worth considering.

But regardless of project size, here are some directly applicable points:

1.  **Write an AGENTS.md**

    If your project has started using AI coding agents, don't just rely on temporary prompts.

    Write down the project rules.

    For example, how to run tests, which commands not to run, what the code style is, which directories should not be modified casually, and what must be checked before committing.

    Putting this content into AGENTS.md is more stable than re-explaining it every time.

2.  **Specify quality requirements**

    Don't just write "welcome high-quality contributions."

    Clearly state what kind of issues will be processed and what kind will be closed.

    For example:

    -   Must use an issue template.
    -   Must describe what the problem is.
    -   Must explain why it's important.
    -   Bugs must provide reproduction steps.
    -   Large features should be discussed first, don't jump directly to a PR.

    The more specific the rules, the lower the explanation cost for maintainers.

3.  **Protect maintainer time**

    Open-source maintenance is not customer service.

    Not all time should be response time.

    You can explicitly state: only seek maintainer review after self-testing passes; low-quality issues are not guaranteed a reply.

    This might sound a bit cold, but it's much better than long-term exhaustion leading to a desire to stop maintaining.

4.  **Establish a trust mechanism**

    pi closes new contributors' issues and PRs by default, but they can be unlocked after a maintainer's reply. Then that person's ID will be recorded, and subsequent submissions will no longer be automatically closed.

## Not Just Collaboration: pi's Tool Design Follows the Same Logic

Above, we discussed how pi treats contributors. But in fact, many designs within the pi tool itself follow the same logic: **remove all unnecessary abstractions and retain only what is truly useful.**

Mario elaborated on these design choices in another blog post, [What I learned building an an opinionated and minimal coding agent][10]. After reading it, you'll find they align with the ideas behind CONTRIBUTING.md.

### Minimal system prompt

pi's system prompt is less than 1000 tokens.

Compare this: Claude Code's system prompt has tens of thousands of tokens, and opencode is similar. pi only tells the agent four things: who you are, what tools you can use, how to use them, and where the documentation is.

This is exactly the style of CONTRIBUTING.md. No lengthy welcome messages, no polite phrases, just clear rules.

Mario's explanation is: state-of-the-art models are already well-trained with RL; they inherently understand what a coding agent is. There's no need for ten thousand tokens to explain it.

Benchmark results also prove this: pi + Claude Opus 4.5 ranks among the top-performing agents on Terminal-Bench 2.0, only behind Codex's native model. A tool with a system prompt under 1000 tokens performs comparably to those with tens of thousands of tokens.

### Only four tools

pi only gives the agent four tools by default: `read`, `write`, `edit`, `bash`.

There's no built-in web search, no Git operations, no to-do list, no plan mode.

This sounds like a lack of features, but Mario believes four tools are sufficient. Models know how to use bash and have been trained on tools similar to `read`, `write`, `edit`.

Moreover, he is very resistant to adding abstraction at the tool layer. For example:

-   **No built-in to-do**: To track tasks, put a `TODO.md` in the project, which the agent reads and writes itself. Use checkboxes to mark completion status. Simple, visible, controllable.
-   **No plan mode**: To plan, write a `PLAN.md`. Unlike planning that only exists within a session, files can be shared across sessions, committed to the repository, and humans can view and modify them at any time. Mario specifically emphasized one point: **for planning, he needs complete observability.** In Claude Code, plan mode spawns a sub-agent, and you can't see what it does. But in pi, everything the agent reads, every markdown it outputs, is right before your eyes.
-   **No MCP support**: An MCP server would stuff twenty or thirty tool descriptions into the context, and just the tool definitions could eat up 7–9% of the context window. Mario's approach is to write these functions as CLI tools + READMEs. The agent reads the READMEs and calls them with bash when needed. Tokens are consumed only when needed (what he calls progressive disclosure), rather than starting every session by deducting tens of thousands of tokens.
-   **No background bash**: Need to run a dev server or debug a process? Use tmux. The agent operates in tmux, and a human can attach to it at any time to observe or even co-debug. Compared to a background process management module whose internal state you can't see, tmux gives you complete observability.
-   **No sub-agent tool**: If an agent needs to spawn itself, it directly runs `pi --print` with bash. While not exactly a sub-agent, the output is fully visible. Mario's criticism of sub-agents is direct: "It's a black box within a black box." And he believes that many people use sub-agents for context gathering when their workflow is actually flawed—they should first gather context in an independent session, produce artifacts, and then start working in a new session with those artifacts.

Looking at these design choices together, there's a very clear thread:

**It's better to let the agent manipulate files and run commands in the simplest way possible than to add an opaque layer of abstraction in between.**

### How Does This Relate to CONTRIBUTING.md?

Returning to the topic of collaboration, pi's CONTRIBUTING.md does the same thing:

-   Uses a simple rule (closed by default) instead of a complex review process.
-   Uses a clear trust marker (`lgtmi` / `lgtm`) instead of vague "welcome contributions."
-   Uses a fixed FAQ instead of having to explain why your PR was closed every time.

Both sides follow the same idea: **remove the middle layer.**

In tool design, what's removed are unnecessary features and abstraction layers.

In collaboration rules, what's removed are unnecessary pleasantries and an openness that doesn't guarantee quality.

Mario repeatedly mentions a word in his blog: observability.

He wants to see everything the agent does. He doesn't want sub-agents operating in a black box, doesn't want background processes to be invisible, doesn't want plan mode to just give results without the process.

CONTRIBUTING.md can also be understood from this perspective:

It makes the maintainer's decision-making process visible to contributors. You were closed not because the maintainer was in a bad mood, but because the rules are structured that way. The FAQ clearly states the reasons. As long as you follow the rules, there's a path forward.

From tools to collaboration, the pi project has a very consistent aesthetic:

**Simple, direct, visible. Without adding things just to "look better."**

This is why I think its approach is worth a serious look. It's not a governance template for large open-source projects, but it's a very well-thought-out case study—about how an open-source project should design its interfaces with the outside world in the AI era.

## Finally

After reviewing pi's rules, my biggest takeaway is:

**The scarce resource in popular open-source projects may no longer be contributors, but maintainers' time.**

Especially after the explosion of AI Agents, the quantity of contributions might increase, but the quality may not improve proportionally.

At this point, what a project truly needs to protect might not be "welcoming more people to contribute," but "welcoming more valuable contributions."

pi's rules seem counter-intuitive, but they honestly face this problem.

*   It doesn't pretend all contributions are good contributions.
*   Nor does it pretend maintainers' time is infinite.

Open-source projects in the AI era might need more such thinking and design to truly maintain sustainable development and high quality.

[1]: https://mariozechner.at/posts/2026-04-08-ive-sold-out/
[2]: https://libgdx.com
[3]: https://openclaw.ai
[4]: https://earendil.com
[5]: https://flask.palletsprojects.com/
[6]: https://sentry.io
[7]: https://lucumr.pocoo.org/2026/4/8/mario-and-earendil/
[8]: https://github.com/badlogic/pi-mono/blob/main/AGENTS.md
[9]: https://github.com/badlogic/pi-mono/blob/main/CONTRIBUTING.md
[10]: https://mariozechner.at/posts/2025-11-30-pi-coding-agent/