---
title: Exploring Agentic DevOps—GitHub Agentic Workflow and Practical Observations of Continuous AI
summary: |
  Recently, I came across a related but more advanced concept—Agentic DevOps. After spending time reading Microsoft Azure's introductions, GitHub's latest documentation, and some open-source practices, I compiled these notes. The goal is to document the learning process and provide a reference for peers. The following content is based on public information and my understanding, without any exaggerated predictions.
tags:
  - Agentic DevOps
  - DevOps
authors:
  - shenxianpeng
date: 2026-02-17
---

Previously, I shared the [basic concepts of AIOps](../aiops/index.md) and some implementation scenarios on my public account, mainly focusing on operations monitoring, anomaly detection, and automated response. Recently, I encountered the concept of Agentic DevOps and the related practices of Continuous AI proposed by GitHub Next, which I believe are worth organizing and sharing with everyone.

Most of this content is currently still in the early exploration phase. I myself have only made some simple attempts based on public documentation and examples and have not yet conducted large-scale production environment verification.

This article is based solely on public information and limited testing, aiming to clarify the core principles, tool forms, and current boundaries, while avoiding over-interpretation.

### Core Meaning of Agentic DevOps

Agentic DevOps can be understood as the next evolutionary stage of DevOps: introducing AI agents with certain autonomous capabilities, allowing them to collaborate with developers and other agents, covering various stages of the software lifecycle.

Specifically:
- **Planning and Coding Phase**: Agents can handle repetitive tasks such as code reviews, generating tests, fixing simple bugs, and updating documentation.
- **Delivery and Operations Phase**: Integrated with CI/CD pipelines, they can automatically analyze failure causes, suggest fixes, and even monitor and respond to certain events in production environments.

In statements from Microsoft and GitHub, it's emphasized that agents are "developers' teammates," not replacements. The core idea is to free humans from trivial tasks, allowing them to focus on higher-value decisions.

Compared to traditional AIOps, Agentic DevOps has a broader scope, no longer limited to the operations layer, but spanning the entire chain from requirements to production. Technically, it usually relies on the reasoning capabilities of large language models (LLMs), combined with tool calling mechanisms and multi-agent collaboration frameworks.

### GitHub's Agentic Workflow and Continuous AI

GitHub Next refers to this type of automation as Continuous AI, analogous to the "continuous" concept in CI/CD: AI is not just a one-time assistant but runs continuously in the background within the repository, handling tasks that require judgment.

**Agentic Workflow** is the specific form for implementing Continuous AI (currently a technical preview/research prototype):
- **Writing Method**: Instead of writing complex YAML, you use Markdown files in the `.github/workflows/` directory to describe intentions. For example, writing a natural language statement: "Generate a repository health report daily, summarizing recent issues and PR changes, and suggesting improvements."
- **Execution Mechanism**: Compiled into standard GitHub Actions workflows via the `gh aw` CLI tool and executed by supported coding agents (GitHub Copilot, Claude Code, OpenAI Codex, etc.).
- **Triggering and Running**: Supports event triggers like schedule, push, issue, and runs in a sandbox environment within GitHub Actions.
- **Security Boundaries**: Read-only permissions by default; write operations (e.g., creating PRs, commenting) must use predefined safe outputs; tool calls are whitelisted; all logs are visible and auditable; PRs are not automatically merged, always retaining a human review step.

This is the official introduction to Agentic Workflow.

![](gh-aw.png)

Practical examples of what can be done include:
- Continuous triage: Automatically label and summarize new issues.
- Continuous documentation updates: Synchronize README or API documentation based on code changes.
- Continuous quality checks: Analyze test coverage and suggest new tests.
- Daily repository status report: Summarize activities and provide actionable items.

These workflows can run in parallel with existing CI/CD pipelines, serving as a supplement rather than a replacement.

Here is an [official GitHub example repository](https://github.com/githubnext/agentics) showcasing many Agentic Workflow use cases, which you can refer to.

### Current Stage and Implementation Boundaries

Based on public information (as of February 2026):
- Most implementations are still in technical preview or research prototype stages.
- GitHub Agentic Workflow requires installing a CLI extension and configuring an agent token. In terms of cost, each run consumes the corresponding model's call quota (e.g., Copilot's premium requests).
- Applicable scenarios are mainly repetitive tasks that "require judgment but can be clearly described." For purely deterministic operations (e.g., builds, unit tests), traditional Actions are still recommended.
- The boundaries are clear: currently, agents do not possess full autonomous decision-making capabilities, and their output must undergo human review; they are not suitable for highly security-sensitive operations; effectiveness depends on prompt engineering and the quality of the repository context.

I tested a simple daily report workflow in my personal repository, and it largely produced summaries as expected.

### Why It's Worth Paying Attention To

Learning these concepts isn't about immediately replacing existing processes, but rather about staying aware of tool evolution. In practical work, we can:
- Experiment with Agentic Workflow at low cost in personal or small team repositories to gain experience.
- Consider which parts of existing DevOps pipelines are suitable for introducing agents (e.g., documentation maintenance, initial triage).
- Pay attention to subsequent updates from vendors like Microsoft Azure, GitHub, and open-source community agentics example repositories.

Ultimately, technology always serves people. Agentic DevOps and Continuous AI merely offer new possibilities, and the effectiveness of their implementation depends on specific scenarios, team size, and governance capabilities.

Everyone is welcome to share their attempts or observations in the comments section. I will also continue to track the progress of these tools and share new practices as they emerge.
---