```
title: Developers Are Getting More Tired—That's Why Backstage Exists
summary: |
  As systems become more complex, developers spend less time coding and more time searching for information. This post introduces Backstage as an Internal Developer Portal, explaining its core capabilities—Software Catalog, Scaffolder, and TechDocs—and discussing why DevOps naturally leads to platform engineering. It also offers a realistic perspective on Backstage's implementation challenges and advises on when to adopt it, emphasizing that the underlying philosophy of clear ownership and standardization is more crucial than the tool itself.
tags:
  - Backstage
authors:
  - shenxianpeng
date: 2025-12-14
---

### Developers Are Getting More Tired—That's Why Backstage Exists

Over the past two years, I've discussed a common feeling with many DevOps and platform engineers:

> **Systems are becoming increasingly cloud-native, but developers are increasingly "not focused on development."**

A very real scenario:

* Want to modify an old service
* First ask: **Whose is this?**
* Then ask: **Where is it deployed?**
* Is CI using Jenkins or GitHub Actions?
* Is monitoring in Datadog or Prometheus?
* What about the documentation? Confluence? Wiki? Or has no one maintained it for a long time?

Eventually, you'll find:

> Writing code only accounts for 30%, with the remaining 70% spent "searching for information."

Consequently, the concept of an **Internal Developer Portal** started to gain traction.
And one of the most representative among them is **Backstage**.

---

### What Exactly is Backstage?

One-sentence version:

> **Backstage is not CI, not Kubernetes, and not a new DevOps tool; rather, it's an "entry point that strings together your existing tools."**

It originated from Spotify.
The pain points for Spotify engineers back then were almost identical to what we face today:

* Many services
* Many teams
* Many tools
* People come and go, knowledge relies entirely on "tribal memory."

Backstage's original intention was very simple:

> **To give all software assets a "household registration book" (a central record).**

Who is responsible, where it runs, what it depends on, and where the documentation is – all visible at a glance.

Later, Spotify open-sourced it and donated it to the CNCF, and it has now become the de facto standard in the IDP (Internal Developer Portal) domain.

---

### Why DevOps Eventually Leads to Platform Engineering?

Many teams initially say:

> We already do DevOps, why do we need platform engineering?

But the reality is:

* DevOps emphasizes **"you build it, you run it."**
* Platform engineering focuses on **"I'll help you make running things simpler."**

Once system complexity increases, expecting **every developer to understand Kubernetes, CI, security, and monitoring** is actually an efficiency disaster.

The goal of platform engineering is not to control developers, but to:

* **Reduce cognitive load**
* **Provide "default-correct" paths**

And Backstage is precisely the vehicle for implementing this philosophy.

---

### Backstage's 3 Core Capabilities

If you only remember three points, remember these.

#### Software Catalog

This is the soul of Backstage.

You can think of it as:

> **An "internal software asset search engine" for the enterprise.**

Each service places a `catalog-info.yaml` in its repository:

* Whose service is this
* Which system it belongs to
* Which APIs it uses
* Which databases / cloud resources it depends on

Backstage then transforms this information into a **visualized relationship network**.

The effects are very clear:

* Newcomers find services without asking people
* When issues arise, quickly pinpoint the scope of impact
* "Who is responsible for this thing" is no longer a mystery

---

#### Software Templates (Scaffolder / Golden Path)

This is the capability I personally **most recommend prioritizing for implementation**.

In reality, creating a new service often looks like this:

* Requesting a repository
* Configuring CI
* Integrating monitoring
* Integrating security scanning
* And then adding a bunch of "compliance requirements"

Backstage templates do one thing:

> **They turn the "correct way" into a one-click operation.**

Developers only need to fill in a few fields:

* Project name
* Language
* Whether a database is needed

The rest:

* Repository creation
* CI configuration
* Catalog registration
  are all completed automatically.

This not only improves efficiency, but more importantly:

> **The platform team can finally turn "specifications" into code, rather than just documentation.**

---

#### TechDocs (Documentation as Code)

This point is a huge plus for someone like me who has long been skeptical of wikis.

TechDocs enforces one principle:

> **Documentation and code are kept together, managed with Markdown.**

There's only one benefit, but it's crucial:

* Documentation will no longer become outdated over time

In Backstage, when you click into a service:

* Code
* Owner
* Documentation
  Everything is brought to a closed loop on a single page.

---

### But Honestly: Backstage Is Not Easy

If you've only heard success stories, then I need to pour some cold water on that.

#### It's Not "Install and Use"

Backstage is more like a **framework** than a product.

The reality is often:

* You need to write React / TypeScript
* You need to develop plugins
* You need to maintain metadata quality

Many companies underestimate this point, and as a result:

> Backstage went live, but no one used it.

#### Once Metadata Is Inaccurate, Trust Collapses Instantly

If it happens even once that:

* The found owner has left the company
* The documentation is wrong

Developers will revert to old habits:
**Slack + private chats + word-of-mouth**

---

### So, Should You Choose Backstage?

My own judgment is:

* **Small teams (<50 people)**
  👉 Self-building is not recommended, as the cost is too high

* **Medium to large engineering organizations**
  👉 If you have a platform team, Backstage is worth serious evaluation

* **Want to see results quickly**
  👉 You can directly look at hosted solutions like Port / Cortex / Roadie

The tool is not the focus; **the philosophy is**.

---

### What's Truly Important Is Not Backstage

Finally, a somewhat "anti-tool" statement.

The core of Backstage's success is not React, not plugins, but the three things behind it:

1. **Clear ownership**
2. **Standardization first**
3. **Treat the platform as a product**

If you're just looking to "add another tool," Backstage is likely to fail.
But if you truly want to:

> **Let developers spend their time writing code, not searching for information**

Then, whether you use Backstage or not, you'll eventually walk this path.
```