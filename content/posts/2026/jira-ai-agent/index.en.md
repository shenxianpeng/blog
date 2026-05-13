---
title: "Building an AI Agent Inside Jira: A Jira Copilot Implementation Guide"
summary: |
  Many people have asked how to build a GitHub Copilot-like AI Agent inside Jira. This post shares my hands-on experience building one — covering account setup, Jira Automation triggers, webhook integration, and a Skills-based capability system. The core philosophy: leverage existing infrastructure to get it running fast and cheap.
tags:
  - AI
  - Jira
  - DevOps
authors:
  - shenxianpeng
date: 2026-05-12
---

Lately I've been getting the same question over and over: how do you build an AI Agent inside Jira, something like GitHub Copilot but for Jira?

I wasn't planning to write about this — the concept didn't seem particularly complex, and I figured anyone with the relevant background could piece it together from the docs. But after being asked enough times, I realized a lot of people genuinely aren't familiar with this area.

I happened to build a similar application inside Jira recently, so here's the full implementation approach.

The guiding principle is simple: **use existing services wherever possible. Don't build from scratch.**

Let me walk through it step by step.

### Step 1: Create a Bot Account

First, you need a dedicated bot. If your company's IT policy allows it, create an account with a short, easy-to-remember name — something like `copilot` or `ai-bot`.

What does this account do? It acts as a "trigger." When a user @-mentions this account in a Jira comment, the automation pipeline kicks in. That's why the name should be short and easy to type — you don't want your colleagues typing `@very-long-hard-to-spell-username-2026` every time they need something.

This step isn't technically exciting, but it's where the whole flow begins.

### Step 2: Set Up Jira Automation

Once the bot account is ready, the next step is configuring Jira Automation. Jira ships with built-in Automation features — no plugins required.

The logic is straightforward:

- Monitor the issue comment section
- When someone @-mentions your target user (e.g., `copilot`), immediately fire a webhook

Jira Automation rules are configured visually, no code involved. You set the trigger condition (Comment contains `@copilot`), then add a "Send webhook" action pointing to your backend service.

The key here: **Automation only handles detection and forwarding. It does zero business logic.** Think of it as a doorbell — someone presses it, the signal goes out, that's it.

### Step 3: Use a Webhook to Trigger the Backend Application

Once the webhook fires, something needs to receive it. I used Jenkins with the Jenkins Generic Webhook Trigger Plugin.

Why Jenkins? Because most teams already have Jenkins running CI/CD. It's existing infrastructure — no need to deploy a new service from scratch.

The setup:

- Create a Pipeline Job in Jenkins, configure the Generic Webhook to receive requests from Jira Automation
- When the webhook is triggered, the Pipeline launches your backend Application

> One thing to get right: the webhook endpoint needs proper security — tokens, source restrictions, parameter validation. You don't want anyone on the internet triggering your Jenkins jobs.

This Application is the core piece you'll build. My own implementation is based on the GitHub Copilot SDK, but the principle is universal — you can use whatever AI platform or SDK you're comfortable with, as long as it can call an LLM via API or CLI.

### Step 4: Build a Skills Architecture

This is the most important design decision in the whole system: **your Application should not be a monolithic "do-everything" script. Instead, organize AI capabilities through Skills.**

My approach is to maintain a dedicated Git repository, structured roughly like this:

```
ai-agent/
├── app/          # Core application logic
└── skills/       # Skill definitions
    ├── fix-bug/
    │   └── SKILL.md
    ├── draft-release-note/
    │   └── SKILL.md
    ├── analyze-root-cause/
    │   └── SKILL.md
    └── write-tests/
        └── SKILL.md
```

- `app/` directory: manages the overall application logic — receiving webhook requests, parsing user intent, dispatching Skills, returning results.
- `skills/` directory: each Skill is a subdirectory named after the skill, containing a `SKILL.md` file (capitalized). This file describes, in natural language, what the skill does, what it takes as input, and what it produces as output. For example, `draft-release-note/SKILL.md` might contain: "Based on recent commit records and Jira issue lists, generate a draft release note in Markdown format."

The benefits of this design are clear:

1. **Decoupled capabilities**: adding a new skill just means creating a new subdirectory and `SKILL.md` file under `skills/` — no changes to core Application code.
2. **Version-controlled**: Skills files live in a Git repository with full change history and review mechanisms.
3. **Easy collaboration**: anyone on the team can submit a new Skill or improve an existing one, without waiting for a developer's schedule.

Each time the Application starts up, it scans the `skills/` directory to see what capabilities are available, then decides which Skill to invoke based on user input.

### Step 5: The Actual User Experience

Once this system is running, the user experience looks like this:

1. In any Jira issue's comment section, @-mention your configured user and describe what you need. For example: `@copilot generate the release notes for this version`
2. Jira Automation detects the @-mention event and sends a webhook request
3. Jenkins receives the request and starts the Application
4. The Application parses user intent and matches it to the appropriate Skill (e.g., `draft-release-note`)
5. The AI executes the task according to the Skill definition, then writes the result back as a Jira comment

From the user's perspective, it's just @-mentioning someone and waiting for a reply in Jira — a completely natural interaction pattern.

In my setup, the tasks that work well include: drafting release notes, analyzing build failure causes, generating root cause analysis drafts, suggesting test code based on context, or (with appropriate repository access) making small code changes.

From there, you continuously refine the system — mostly the Skills — to make the outputs more stable and reliable over time.

### Step 6: Lessons Learned and Optimization

Getting the system running is step one. The real work is the continuous optimization that follows. Here are a few lessons I've picked up from hands-on experience.

**1. Run in containers, not VMs**

Your Application should run in containers (Docker / Kubernetes), not traditional VMs. Containers start fast, isolate resources well, scale horizontally, and — importantly — each trigger gets a clean execution environment. VMs can work, but image management, dependency conflicts, and operational overhead are an order of magnitude worse. For an AI Agent that gets triggered frequently and needs quick responses, containers are the clear winner.

**2. If a script can do it, don't use AI**

This is the most common mistake — throwing every task at the LLM. The reality is, many operations don't need AI at all. For example:

- Pulling issue lists from the Jira API, filtering fields, formatting output → plain script.
- Parsing webhook requests, extracting key fields, assembling prompts → preprocessing script.
- Writing AI results back as Jira comments → still a script.

Let AI handle only what it's best at: understanding and generating text. All other deterministic logic should be handled by scripts. This not only saves money (fewer tokens consumed) but also produces more stable, predictable results. A useful litmus test: **if you can express the logic clearly in under 50 lines of script, don't make an LLM guess at it.**

**3. Design Skills for reuse**

Skills aren't disposable. Design them with reuse in mind:

- **Right-size granularity.** A Skill does one thing, but that thing should be general enough — for example, `analyze-build-failure` should work across multiple projects, not be hardcoded to one repository.
- **Parameterize.** Use input parameters (project name, version number, date range) to adapt to different scenarios, rather than creating a separate Skill for each one.
- **Composable.** Complex tasks can be built by chaining multiple base Skills. A "weekly release report" might be composed of `collect-commits` + `draft-release-note`, instead of writing yet another Skill.

**4. Follow Skill authoring best practices**

The quality of `SKILL.md` directly determines the quality of AI output. Here are the key points I've learned:

- **Explicit input/output definitions.** Every Skill must clearly state what it receives (fields, format) and what it produces (text, structure). Don't write "analyze the problem"; write "Receive a Jira Issue Key, read its Description and the last 10 Comments, output a root cause analysis in Chinese, under 200 words."
- **Provide examples.** Include an input/output example in `SKILL.md`. The AI understands your expectations much more accurately with a concrete sample.
- **Define boundaries.** Explicitly tell the AI what NOT to do. For example: "Do not modify original code, only output suggestions", "Do not fabricate information not present in the issue." A Skill without boundaries gives the AI too much room to improvise, and the results are often unreliable.
- **Test iteratively.** Run the same set of test cases against a Skill repeatedly, comparing output quality after each edit to `SKILL.md`. This is essentially unit testing — except the subject under test is the AI's prompt.

**5. Log token consumption for optimization comparison**

This is easy to overlook but critically important: in your Application logs, **explicitly record the token count for every request** (input tokens, output tokens, total tokens).

Why? Because optimization needs a quantifiable metric. You tweak a prompt, restructure a Skill, switch models — how many tokens did those changes save? Without logging, you're judging by feel. With data, a glance at the logs tells you clearly: same task, token consumption dropped from 2000 to 1200 — optimization confirmed.

I recommend logging these fields:

- `timestamp`: request time
- `skill_name`: the matched Skill
- `model`: the model used
- `input_tokens` / `output_tokens` / `total_tokens`
- `latency_ms`: total time (network + inference)
- `user_input`: a summary of the original user input (for traceability)

Once this becomes a habit, every change can be validated quickly, and you'll never have to guess which direction to optimize.

### Wrap-Up

That's the high-level implementation approach, along with the pitfalls I've hit and the lessons learned along the way. I won't go into specific code or technical details — every company has different tech stacks, permission models, and internal processes, so directly copy-pasting wouldn't work anyway.

But once you understand the workflow behind these six steps, you can absolutely build a similar system with AI assistance, tailored to your own company's reality.

At its core, this isn't anything particularly mysterious. It's essentially creating an AI-capable robot — a "digital colleague" — that operates inside Jira.

Before, you'd @-mention a teammate in Jira and ask them to write release notes, run tests, or fix a bug. Now, you can @-mention this new digital colleague and have it handle those tasks.

And that, I think, is where AI creates real value inside organizations: making the work that used to require endless back-and-forth communication more automatic, more seamless.

Hope this gives you some ideas. If you're building something similar, I'd love to hear about it in the comments.

---

This work is licensed under CC BY-NC 4.0. Please attribute the author and source when sharing. No commercial use. Follow the official WeChat account 「沈显鹏」
