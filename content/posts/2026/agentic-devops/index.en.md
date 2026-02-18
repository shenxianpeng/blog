---
title: Exploring Agentic DevOps—GitHub Agentic Workflow and Practical Observations of Continuous AI
summary: |
  Recently, I encountered a related but more advanced concept—Agentic DevOps. After spending time reading Microsoft Azure's introductions, GitHub's latest documentation, and some open-source practices, I compiled these notes. The purpose is to document my learning process and provide reference for colleagues. The following content is based on publicly available information and my understanding, without any exaggerated predictions.
tags:
  - Agentic DevOps
  - DevOps
authors:
  - shenxianpeng
date: 2026-02-17
---

Agentic DevOps was introduced by Microsoft at the Azure Build conference in 2025. Recently, with GitHub's release of [GitHub Agentic Workflow](https://github.github.com/gh-aw/) and the concept of [Continuous AI](https://githubnext.com/projects/continuous-ai), Agentic DevOps has resurfaced.

![](azure-build.webp)

Previously, I shared the [basic concepts of AIOps](../aiops/index.md) and some practical application scenarios on my public account, mainly focusing on operations monitoring, anomaly detection, and automated responses. Combining the concept of Agentic DevOps with the Continuous AI practices proposed by GitHub Next, I felt it was worth organizing and sharing with everyone.

Most of this content is still in the early exploration phase. I myself have only made some simple attempts based on public documentation and examples, and have not yet conducted large-scale production environment validation.

This article is based solely on public information and limited testing, aiming to clarify the core principles, tool forms, and current boundaries, while avoiding over-interpretation.

### Core Meaning of Agentic DevOps

Agentic DevOps can be understood as the next evolutionary stage of DevOps: introducing AI agents with a degree of autonomy, allowing them to collaborate with developers and other agents, covering various stages of the software lifecycle.

Specifically:
- **Planning and Coding Stages**: Agents can handle repetitive tasks such as code reviews, test generation, simple bug fixes, and documentation updates.
- **Delivery and Operations Stages**: Combined with CI/CD pipelines, they can automatically analyze failure causes, suggest fixes, and even monitor and respond to some events in production environments.

In statements from Microsoft and GitHub, agents are emphasized as "developers' teammates," not replacements. The core idea is to free humans from琐碎事务 and allow them to focus on higher-value decisions.

Compared to traditional AIOps, Agentic DevOps has a broader scope, no longer limited to the operations layer, but spanning the entire chain from requirements to production. Technical implementation typically relies on the inferential capabilities of Large Language Models (LLMs), combined with tool calling mechanisms and multi-agent collaboration frameworks.

### GitHub's Agentic Workflow and Continuous AI

GitHub Next refers to this type of automation as Continuous AI, analogizing the "continuous" concept in CI/CD: AI is not just a one-time assist, but runs continuously in the background within the repository, handling tasks that require judgment.

**Agentic Workflow** is the specific form of implementing Continuous AI (currently in technical preview/research prototype):
- **Writing Method**: Instead of writing complex YAML, Markdown files are used in the `.github/workflows/` directory to describe intent. For example, writing a natural language statement like: "Generate a repository health report daily, summarizing recent issues and PR changes, and suggesting improvements."
- **Execution Mechanism**: Compiled into standard GitHub Actions workflows via the `gh aw` CLI tool, and executed by supported coding agents (GitHub Copilot, Claude Code, OpenAI Codex, etc.).
- **Triggering and Running**: Supports triggers such as schedule, push, and issue events, running in the GitHub Actions sandbox environment.
- **Security Boundaries**: Default read-only permissions; write operations (e.g., creating PRs, comments) must be performed via predefined safe outputs; tool calls have a whitelist; all logs are visible and auditable; PRs are never automatically merged, always retaining a human review step.

This is the official introduction to Agentic Workflow.

![](gh-aw.png)

Examples of what can actually be done include:
- Continuous triage: Automatic labeling and summarizing of new issues.
- Continuous documentation updates: Synchronizing READMEs or API documentation based on code changes.
- Continuous quality checks: Analyzing test coverage and suggesting new tests.
- Daily repository status reports: Summarizing activity and providing actionable items.

These workflows can run in parallel with existing CI/CD pipelines, serving as a supplement rather than a replacement.

Here is an [official GitHub example repository](https://github.com/githubnext/agentics) showcasing many Agentic Workflow use cases for reference.

### Current Stage and Implementation Boundaries

Based on publicly available information (as of February 2026):
- Most implementations are still in technical preview or research prototype stages.
- GitHub Agentic Workflow requires installing a CLI extension and configuring an agent token. In terms of cost, each run consumes the corresponding model's call quota (e.g., Copilot's premium requests).
- Applicable scenarios are mainly repetitive tasks that "require judgment but can be clearly described." Purely deterministic operations (e.g., builds, unit tests) are still recommended for traditional Actions.
- The boundaries are very clear: currently, agents do not possess full autonomous decision-making capabilities, and output results must undergo human review; they are not suitable for highly security-sensitive operations; effectiveness depends on prompt engineering and the quality of the repository context.

I tested a simple daily report workflow in my personal repository, and it generally produced summaries as expected.

### Why It's Worth Paying Attention

Learning these concepts is not about immediately replacing existing processes, but about staying aware of tool evolution. In practical work, we can:
- Low-cost experimentation with Agentic Workflow in personal or small team repositories to gain experience.
- Consider which parts of existing DevOps pipelines are suitable for introducing agents (e.g., documentation maintenance, initial triage).
- Follow subsequent updates from vendors like Microsoft Azure and GitHub, as well as open-source community agentics example repositories.

Ultimately, technology always serves people. Agentic DevOps and Continuous AI merely offer new possibilities, and the implementation effect depends on the specific scenario, team size, and governance capabilities.

Feel free to share your attempts or observations in the comments section. I will also continue to track the progress of these tools and will share new practices when available.