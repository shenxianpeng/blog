---
title: I Built an AI Agent in Jira—A Realization Idea for a Jira-based Copilot
summary: |
  Many friends have asked how to build an AI Agent in Jira similar to GitHub Copilot. This article shares a complete implementation idea, from account preparation, Jira Automation triggers, Webhook integration, to building a Skills capability system, based on a similar application I actually developed in Jira. The core is to leverage existing services for low-cost, rapid implementation.
tags:
  - AI
  - Jira
  - DevOps
authors:
  - shenxianpeng
date: 2026-05-12
---

Hello everyone, I'm Shen Gong.

Recently, I've noticed many people asking the same question: how to create an AI Agent in Jira similar to GitHub Copilot?

To be honest, I hadn't planned to write about this topic—I thought the principles weren't that complex, and anyone who understood it could probably get started by reading the documentation. But after being asked similar questions repeatedly, I realized that many friends might indeed be unfamiliar with this area.

Today, I'll combine this with a similar application I developed in Jira to share the overall implementation idea.

The core principle is simple: **Leverage existing services as much as possible, don't reinvent the wheel.**

Below, I'll explain it step by step.

### Step One: Prepare a Bot Account

First, you need a dedicated Bot. With IT's permission, create an account with a simple, easy-to-remember name, such as `copilot` or `ai-bot`.

What is the purpose of this account? It acts as a "trigger." When a user @mentions this account in Jira's comment section, the subsequent automation process will be activated. So, the name should be as short and easy to type as possible—you certainly don't want colleagues to have to @ a long, hard-to-spell username every time.

This step involves no technical complexity, but it is the starting point of the entire process.

### Step Two: Set up Jira Automation

Once the account is ready, the next step is to configure Automation in Jira. Jira comes with a built-in Automation feature (Jira Automation), so no additional plugins are needed.

The specific logic is simple:

- Monitor the Issue's comment section.
- When a user @mentions your specified User (e.g., `copilot`), immediately trigger a Webhook.

Jira Automation rule configuration is visual, no code is required. You just need to set the trigger condition (Comment contains `@copilot`) and then add a "Send webhook" action, pointing to your backend service's address.

The key here is: **Automation is only responsible for detection and forwarding, not for any business logic.** It's like a doorbell—when someone rings it, the signal is sent out.

### Step Three: Use Webhook to Trigger Backend Application

After the Webhook is sent, a receiver is needed. I chose Jenkins's Jenkins Generic Webhook Trigger Plugin.

Why Jenkins? Because most teams already have Jenkins running for CI/CD; it's existing infrastructure, eliminating the need to deploy new services.

Configuration method:

- Create a Pipeline Job in Jenkins, configure Generic Webhook to receive requests from Jira Automation.
- When the Webhook is triggered, the Pipeline starts your backend Application.

> It's important to note here that the Webhook entry point should have robust security controls, such as tokens, source restrictions, parameter validation, etc., to prevent anyone from arbitrarily triggering Jenkins Jobs.

This Application is the core part you need to develop. My own implementation is based on the GitHub Copilot SDK, but the principle is universal—you can choose any AI platform or SDK you are familiar with, as long as it can call large language models via API or CLI.

### Step Four: Build the Skills Capability System

This is the most important part of the entire design: **Your Application should not be a "mishmash" script, but should organize AI's capabilities through Skills.**

My approach is to create a dedicated Git repository with a structure roughly like this:

```
ai-agent/
├── app/          # Application main logic
└── skills/       # Various skill definitions
    ├── fix-bug/
    │   └── SKILL.md
    ├── draft-release-note/
    │   └── SKILL.md
    ├── analyze-root-cause/
    │   └── SKILL.md
    └── write-tests/
        └── SKILL.md
```

- `app/` directory: Manages the overall logic of the Application, including receiving Webhook requests, parsing user intent, dispatching Skills, returning results, etc.
- `skills/` directory: Each Skill is a subdirectory named after the skill, containing a `SKILL.md` file (uppercase) that describes in natural language what the skill does, what its input is, and what its output is. For example, `draft-release-note/SKILL.md` might contain: "Generate a draft release log based on recent commit records and Jira Issue lists, formatted as Markdown."

The advantages of this design are obvious:

1.  **Capability Decoupling**: Adding new skills only requires adding a new subdirectory and `SKILL.md` file in the `skills/` directory, without modifying the Application's core code.
2.  **Version Control**: Skill files are managed in a Git repository, with complete change history and review mechanisms.
3.  **Easy Collaboration**: Anyone on the team can submit new Skills or improve existing ones, without relying on developers to schedule separately.

Each time the Application starts, it scans the `skills/` directory to see what capabilities are available, and then decides which Skill to call based on user input.

### Step Five: Actual Running Effect

When this system is up and running, the user experience is as follows:

1.  In the comment section of any Jira Issue, @mention the User you set up, and simultaneously enter your request. For example, `@copilot Help me generate the release notes for this version.`
2.  Jira Automation detects the @event and sends a request to the Webhook.
3.  Jenkins receives the request and starts the Application.
4.  The Application parses user intent and matches it to the corresponding Skill (e.g., `draft-release-note`).
5.  The AI executes the task according to the Skill's definition, and after completion, writes the result back to the Jira comment.

For the user, the experience is simply @mentioning in the comments and then waiting for a reply in Jira, which is very natural.

In my scenario, tasks currently well-suited for this system include: writing release notes, analyzing build failure causes, generating Root Cause Analysis drafts, suggesting test code based on context, or making simple modifications given code repository permissions.

You can then continuously optimize this system, primarily the Skills, to make its input increasingly stable and reliable.

### Summary

The above is a general idea of how this system is implemented. I won't go into specific code and technical details, as each company's technology stack, permission system, and internal processes are different, making direct replication difficult.

However, by understanding the workflow behind these five steps, you can absolutely build a similar system with the help of AI, tailored to your company's specific situation.

Essentially, this is not something particularly mysterious. It's more like creating an AI-powered robot, or a "digital colleague," that operates within Jira for your company.

Previously, you would @mention a colleague in Jira to ask them to write release notes, test, or fix a bug; now, you can also @mention this new digital colleague and have it help you complete these tasks.

This is where I believe AI truly adds value within enterprises: it makes tasks that previously required repeated communication more automated and smoother.

I hope this sharing provides some inspiration. If you are also making similar attempts, feel free to share your thoughts and experiences in the comments section.

---

Please cite the author and source when reprinting articles from this site. Do not use for any commercial purposes. Welcome to follow the official account '沈显鹏'.