```
---
title: GitHub AI Terminology Explained—Copilot, Agents, Models to MCP, Who is Who?
summary: This article provides a detailed explanation of GitHub's AI-related concepts and their hierarchical relationships through fact-based explanations and analogies, helping readers clarify the meaning and function of terms like Models, Agents, Spaces, and Spark.
tags:
  - AI
  - GitHub
authors:
  - shenxianpeng
date: 2025-12-26
---

First, a disclaimer: I am not an AI expert myself. The following content is my understanding, summarized from official documentation and practical experience. I hope it helps everyone avoid detours and clearly understand GitHub AI's overall layout and individual functions.

In the past year, AI terms on GitHub have been proliferating:

> **Models、Agents、Spaces、Spark、Instructions、Agent Skills、MCP……**
> The names are similar, but many people get confused at first glance.

Many people ask:

> What is Copilot?
> What's the difference between Agents and Models?
> Is Spark a low-code tool?
> What are Skills?
> What exactly does MCP do?

Today, I'll help you clarify these concepts using a familiar approach of **fact-based explanations + analogies**.

---

## I. Clarify Core Concepts First

Let's start with GitHub's official documentation.

### What are **GitHub Models**

The official documentation states:

> GitHub Models provides a model catalog, prompt management, and evaluation tools, allowing you to compare models, fine-tune prompts, evaluate performance, and integrate models directly within GitHub. It aims to lower the barrier for enterprise-grade AI adoption and integrate seamlessly with GitHub workflows.([GitHub Docs][1])

In other words:

**Models are a "model resource library + debugging and evaluation toolset," not a specific AI product.**
It helps you within GitHub to:

*   Search for different large models
*   Debug and compare prompt outputs
*   Evaluate which model is more suitable for your task

Therefore, **GitHub Models is not Copilot, nor is it an Agent**; it is an "experimental/integration platform for AI models."

---

## II. Let's use an analogy: AI is not a single tool, but like an AI-powered software company

To better understand the following terms, let's use an analogy:

> **Let's liken these AI concepts to the internal organizational structure and tools of a software company undergoing full AI transformation.**

---

## III. Explaining Them One by One

### 1️⃣ Copilot: The "AI Assistant" sitting next to your IDE

This needs little introduction:

*   It provides you with **code completion**
*   Understands context
*   Can suggest as you write in the IDE

The official offering has also evolved over the years:

*   Added multi-model support (Anthropic Claude, Google Gemini, various OpenAI models, etc.) ([The Verge][2])
*   Introduced a stronger Agent mode (capable of executing commands) ([Wikipedia][3])

So Copilot fundamentally remains:

> **A real-time code assistant serving human developers (AI next to your IDE)**

---

### 2️⃣ Agents: "AI Employees" that can be assigned tasks

The **Agent** here cannot be simply understood as "a mode of Copilot." It carries a stronger semantic meaning:

GitHub news reports (Agent HQ) introduce:

> GitHub will allow developers in the future to create and manage multiple AI agents from different models and services, unifying scheduling, executing tasks, and even running them in parallel, then choosing the most suitable results. ([The Verge][4])

Thus, **Agent ≠ Copilot's basic completion**; it is closer to:

> **An AI assistant that can be assigned tasks and perform specific work (complete tasks).**

For example:

*   Automatically create PRs
*   Batch process files
*   Run tests
*   Automatically respond to Issues

You tell it "go do the work," it executes, and can even form a task queue.

This concept also appears in community tools, where many people use Agents for automatic PRs, monitoring pipelines, etc. This mode is more "automated" than Copilot's traditional completion.

---

### 3️⃣ GitHub Spaces: The "Dedicated Workspace" for AI and Context

This is one that many people find most confusing:

**Official documentation clarifies:**

> Spaces provide a "space" that you can access, where you put together the context you want to give to the AI. When you use Copilot in your IDE, this context is loaded in the background. ([GitHub Docs][5])

Many people mistakenly think Spaces are a type of Repo, but they are not.

It's more like:

> **A "collaboration space" specifically prepared with context, data, and documentation, allowing the AI to better understand what you want to do.**

For example:

If you're working on a new feature, putting requirements documents, design mockups, and relevant Markdown into a Space, the AI has this complete context and can naturally respond more accurately.

**So Spaces = Context + Knowledge Hub, not a model or Agent itself.**

---

### 4️⃣ GitHub Spark: The "Project Sandbox" for Rapid Prototyping

GitHub Spark is a newly launched GitHub product (currently in preview):

According to community messages:

> Spark allows Copilot Pro+ users to generate **full-stack applications** using natural language, going directly from idea to deployment, automatically handling code, configuration, permissions, etc., and supporting in-code and subsequent extensions. ([Reddit][6])

In other words:

> **Spark is a platform that automatically transforms "ideas → working products".**
> It packages various models, workflows, and deployment mechanisms, allowing you to see results just by writing a single requirement.

This goes a step further than traditional Copilot completion or Agent execution — it is an **all-in-one rapid prototyping workshop**.

---

### 5️⃣ GitHub Instructions / Repository Custom Instructions (Official Feature)

This is a feature appearing in GitHub Docs:

You can write **Custom Instructions** in your Repo to guide Copilot and Agents:

> Tell it:
>
> *   Your code standards
> *   Output style
> *   Business constraints
> *   Specific task requirements

In other words:

> **Instructions = "Behavioral Guidelines/Manual" written for AI**
> To make its responses more aligned with project requirements.

This differs from Copilot's "prompt"; it's more like a set of long-term effective project habit guidelines.

---

### 6️⃣ Agent Skills / Claude Skills: Callable Capability Modules

There are two concepts here:

*   GitHub Agent Skills (Official)
*   Claude Skills (Anthropic community ecosystem)

Official explanation:

> Agent Skills are a set of instructions, scripts, and resources placed in `.github/skills` that are loaded by Copilot when needed to improve task performance. ([GitHub Docs][7])

And Claude Skills in the community are also:

> A "skill set" that can extend the capabilities of the Claude model, allowing it to perform specific tasks (e.g., data analysis, table processing, automated scripting). ([GitHub][8])

This means:

*   Skills are essentially "detailed instructions + examples telling AI how to perform a certain type of task"
*   They have a structured definition (`SKILL.md` + metadata)
*   Unlike random prompts, they are a set of reusable modules

To use an analogy:

> **Skills = Modular "professional skill packs" that AI can call upon when executing tasks.**

---

### 7️⃣ MCP (Model Context Protocol): The "Standard Interface Protocol" of the AI World

This last concept is one that many mention but find least clear.

Official documentation and community explanations both state:

> MCP is a protocol standard that allows AI assistants to interact uniformly with external services, secure connections, and access data. ([GitHub Docs][9])

Many in the community have also built MCP servers based on it, allowing various models and tools to interact with GitHub via JSON configuration, such as cloning repositories and submitting PRs. ([playbooks][10])

So essentially:

> **MCP is not a model, nor is it an Agent;**
> **It is "a general protocol that allows models/Agents to acquire external context and execute external tasks."**

It can be seen as:

*   Just as HTTP is the standard protocol for browsers to access web pages
*   MCP is the standard protocol for AI Agents to access tools and data

There are related explanations in the official documentation, but it is not a specific product component; rather, it is a **standard-layer protocol**.

---

## IV. Remember Their Relationships (Analogy Version)

To help everyone remember at a glance, here is my pictorial analogy:

| Concept            | Analogy                       | Core Function                           |
| :----------------- | :---------------------------- | :-------------------------------------- |
| Copilot            | Your AI Coding Assistant      | Real-time code suggestions              |
| GitHub Models      | Model resource library + debugging platform | Manage, evaluate various models         |
| Agents             | AI that "gets work done"      | Automatically execute specific tasks    |
| Spaces             | AI's collaborative workstation | Provide context environment             |
| Spark              | Rapid prototyping room        | Quickly turn ideas into runnable results |
| Instructions       | AI's behavioral guidelines    | Long-term regulation of project performance |
| Skills             | Reusable skill pack           | Modularly enhance AI task execution capabilities |
| MCP                | AI's standard protocol interface | Enable AI to access external resources and data |

---

## V. Summary and Actionable Advice

These concepts may seem numerous, but essentially:

1.  **Models + MCP are infrastructure**
2.  **Agents + Skills + Instructions are productivity tools**
3.  **Spaces + Spark are workspace/product layers**

Understanding these layers, you can:

*   Start by using Copilot for code completion/generation
*   Experiment with Agents to automate tasks
*   Create rapid prototypes with Spark
*   Use Instructions and Skills to regulate and enhance AI behavior

GitHub AI is evolving rapidly, and concepts are developing. By understanding these layers, you won't easily get confused and can more reasonably integrate AI into your development workflow.

[1]: https://docs.github.com/en/github-models/about-github-models "About GitHub Models - GitHub Docs"
[2]: https://www.theverge.com/2024/10/29/24282544/github-copilot-multi-model-anthropic-google-open-ai-github-spark-announcement "GitHub Copilot will support models from Anthropic, Google, and OpenAI"
[3]: https://en.wikipedia.org/wiki/GitHub_Copilot "GitHub Copilot"
[4]: https://www.theverge.com/news/808032/github-ai-agent-hq-coding-openai-anthropic "GitHub is launching a hub for multiple AI coding agents"
[5]: https://docs.github.com/en/copilot/how-tos/provide-context/use-copilot-spaces/use-copilot-spaces "Using GitHub Copilot Spaces - GitHub Docs"
[6]: https://www.reddit.com//r/AIGuild/comments/1m7xgg0 "GitHub Spark Ignites One‑Click AI App Building for Copilot Users"
[7]: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills "About Agent Skills - GitHub Docs"
[8]: https://github.com/anthropics/skills "GitHub - anthropics/skills: Public repository for Skills"
[9]: https://docs.github.com/zh/copilot/how-tos/agents/copilot-coding-agent/extending-copilot-coding-agent-with-mcp "使用模型上下文协议 (MCP) 扩展 Copilot 编码助手 - GitHub 文档"
[10]: https://playbooks.com/mcp/parassolanki-github "GitHub MCP server for AI agents"

---

Please cite the author and source when reprinting articles from this site. Do not use for any commercial purposes. Welcome to follow the official account「DevOps攻城狮」
```