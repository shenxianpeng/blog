```
title: Developers Are Getting More Tired, Thus Backstage Emerged
summary: |
tags:
  - Backstage
authors:
  - shenxianpeng
date: 2025-12-14
---

### Developers Are Getting More Tired, Thus Backstage Emerged

In the past two years, I've discussed a common sentiment with many DevOps and platform engineers:

> **Systems are becoming more cloud-native, but developers are increasingly "not focused on development."**

A very real scenario:

* Want to modify an old service
* First ask: **Whose is this?**
* Then ask: **Where is it deployed?**
* Is CI using Jenkins or GitHub Actions?
* Is monitoring on Datadog or Prometheus?
* What about documentation? Confluence? Wiki? Or has it long been unmaintained?

Ultimately, you'll find:

> Writing code only accounts for 30%, while the remaining 70% is spent "searching for information."

Consequently, the concept of an **Internal Developer Portal** started to gain traction.
And one of the most representative among them is **Backstage**.

---

### What Exactly Is Backstage?

One-sentence version:

> **Backstage is not CI, not Kubernetes, nor a new DevOps tool; it's an "entry point that connects your existing tools."**

It originated from Spotify.
At that time, Spotify engineers faced pain points almost identical to what we encounter today:

* Many services
* Many teams
* Many tools
* People come and go, knowledge relies entirely on "tribal memory"

Backstage's original intention was very simple:

> **To give all software assets a "comprehensive record."**

Who is responsible, where it runs, what it depends on, where the documentation is – all visible at a glance.

Later, Spotify open-sourced it and donated it to the CNCF, and it has now become the de facto standard in the IDP (Internal Developer Portal) domain.

---

### Why DevOps Will Eventually Evolve Towards Platform Engineering?

Many teams initially say:

> We're already doing DevOps, why do we need Platform Engineering?

But the reality is:

* DevOps emphasizes **"you build it, you run it"**
* Platform Engineering focuses on **"I'll help you simplify the act of running it"**

Once system complexity increases, expecting **every developer to understand Kubernetes, CI, security, and monitoring** is actually an efficiency disaster.

The goal of Platform Engineering is not to control developers, but to:

* **Reduce cognitive load**
* **Provide "default-correct" paths**

And Backstage is precisely the vehicle for implementing this philosophy.

---

### Backstage's 3 Core Capabilities

If you only remember three points, remember these.

#### Software Catalog

This is the soul of Backstage.

You can think of it as:

> **The enterprise's "software asset search engine"**

Each service places a `catalog-info.yaml` in its repository:

* Whose service this is
* Which system it belongs to
* Which APIs it uses
* Which databases / cloud resources it depends on

Backstage then transforms this information into a **visual relationship network**.

The effects are very apparent:

* Newcomers find services without asking people
* When issues arise, quickly identify the scope of impact
* "Who is responsible for this thing" is no longer a mystery

---

#### Software Templates (Scaffolder / Golden Path)

This is the capability I **personally most recommend implementing first**.

In reality, creating a new service often goes like this:

* Request a repository
* Configure CI
* Connect monitoring
* Integrate security scanning
* Then add a bunch of "standardized requirements"

Backstage's templates do one thing:

> **Turn the "correct approach" into a one-click operation.**

Developers only need to fill in a few fields:

* Project name
* Language
* Whether a database is needed

The rest:

* Repository creation
* CI configuration
* Catalog registration
All completed automatically.

This not only improves efficiency, but more importantly:

> **Platform teams can finally turn "standards" into code, instead of documentation.**

---

#### TechDocs (Documentation as Code)

This point is a huge plus for someone like me who has long distrusted Wikis.

TechDocs enforces one principle:

> **Documentation and code are kept together, managed with Markdown.**

There's only one benefit, but it's crucial:

* Documentation will no longer become long-term outdated

In Backstage, when you click into a service:

* Code
* Responsible person
* Documentation
All complete a closed loop on a single page.

---

### But Honestly: Backstage Is Not Easy

If you've only heard success stories, then I need to pour some cold water on that.

#### It's Not "Install and Use"

Backstage is more like a **framework** than a product.

The reality is often:

* Requires writing React / TypeScript
* Requires developing plugins
* Requires maintaining metadata quality

Many companies underestimate this, and the result is:

> Backstage went live, but no one used it.

#### If Metadata Is Inaccurate, Trust Will Instantly Collapse

Just one instance of:

* The found responsible person has left the company
* The documentation is wrong

Developers will revert to old ways:
**Slack + direct messages + word-of-mouth**

---

### So, Should You Choose Backstage Or Not?

My own judgment is:

* **Small teams (<50 people)**
👉 Not recommended to build yourself, costs are too high

* **Medium to large engineering organizations**
👉 If you have a platform team, Backstage is worth serious evaluation

* **Want to see results quickly**
👉 You can directly look at hosted solutions like Port / Cortex / Roadie

The tool isn't the focus, the **philosophy is**.

---

### What's Truly Important Is Not Backstage Itself

Finally, a remark that might seem a bit "anti-tool theory."

The core of Backstage's success is not React, not plugins, but the three things behind it:

1. **Clear ownership**
2. **Standardization first**
3. **Treat the platform as a product**

If you're just looking to "implement another tool," then Backstage will likely fail.
But if you truly want to:

> **Let developers spend their time writing code, not searching for information**

Then whether you use Backstage or not, you'll eventually arrive at this path.
```