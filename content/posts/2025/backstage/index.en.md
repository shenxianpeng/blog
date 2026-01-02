```
title: Developers Are Getting Tired—Enter Backstage
summary: As systems become more cloud-native, developers increasingly spend less time coding and more time searching for information across disparate tools. This post explores the rise of Internal Developer Portals and how Backstage, originating from Spotify, addresses this challenge by centralizing software assets, standardizing creation processes, and integrating documentation, embodying the shift towards Platform Engineering.
tags:
  - Backstage
authors:
  - shenxianpeng
date: 2025-12-14
---

### Developers Are Getting Tired—Enter Backstage

In the past two years, I've discussed a common sentiment with many DevOps and platform engineers:

> **As systems become increasingly cloud-native, developers are becoming "less focused on development."**

A very real scenario:

* You want to modify an old service
* First, you ask: **Whose is this?**
* Then, you ask: **Where is it deployed?**
* Does it use Jenkins or GitHub Actions for CI?
* Is monitoring on Datadog or Prometheus?
* What about the documentation? Confluence? Wiki? Or has no one maintained it for ages?

In the end, you'll find:

> Writing code only accounts for 30%, while the remaining 70% is spent "finding information."

Thus, the concept of an **Internal Developer Portal** began to gain traction.
And one of its most representative examples is **Backstage**.

---

### What Exactly Is Backstage?

The one-sentence version:

> **Backstage is not CI, not Kubernetes, nor a new DevOps tool; rather, it's an "entry point that stitches your existing tools together."**

It originated from Spotify.
The pain points Spotify engineers faced back then are almost identical to what we encounter today:

* Many services
* Many teams
* Many tools
* People come and go, knowledge relies entirely on "tribal memory"

Backstage's initial goal was very simple:

> **To give all software assets a "household registration book" (a central record).**

Who is responsible, where it runs, what it depends on, where the documentation is—all visible at a glance.

Later, Spotify open-sourced it and donated it to the CNCF, and it has now become the de facto standard in the IDP (Internal Developer Portal) domain.

---

### Why DevOps Inevitably Leads to Platform Engineering?

Many teams initially say:

> We're already doing DevOps, why do we need Platform Engineering?

But the reality is:

* DevOps emphasizes **"you build it, you run it"**
* Platform Engineering focuses on **"I'll help you make running things simpler"**

When system complexity increases, expecting **every developer to understand Kubernetes, CI, security, and monitoring** is actually an efficiency disaster.

The goal of Platform Engineering is not to control developers, but to:

* **Reduce cognitive load**
* **Provide "default correct" paths**

And Backstage is precisely the vehicle for implementing this philosophy.

---

### Backstage's 3 Core Capabilities

If you only remember three points, remember these three.

#### Software Catalog

This is the soul of Backstage.

You can think of it as:

> **An "internal software asset search engine" for your enterprise.**

Each service places a `catalog-info.yaml` file in its repository:

* Whose service it is
* Which system it belongs to
* Which APIs it uses
* Which databases / cloud resources it depends on

Backstage then transforms this information into a **visual relationship network**.

The effects are very clear:

* New hires find services without having to ask people
* When issues arise, the scope of impact can be quickly identified
* "Who is responsible for this thing?" is no longer a mystery

---

#### Software Templates (Scaffolder / Golden Path)

This is the capability I personally **most recommend prioritizing for implementation**.

In reality, creating a new service often looks like this:

* Request a repository
* Configure CI
* Integrate monitoring
* Integrate security scanning
* Then add a bunch of "spec requirements"

Backstage's templates do one thing:

> **They turn "the correct way" into a one-click operation.**

Developers only need to fill in a few fields:

* Project name
* Language
* Whether a database is needed

The rest:

* Repository creation
* CI configuration
* Catalog registration
  All automatically completed.

This not only improves efficiency, but more importantly:

> **The platform team can finally turn "standards" into code, rather than just documentation.**

---

#### TechDocs (Docs as Code)

This point is a huge bonus for someone like me who has long distrusted Wikis.

TechDocs enforces one principle:

> **Documentation and code are kept together, managed with Markdown.**

There's only one benefit, but it's crucial:

* Documentation will no longer become stale long-term

In Backstage, when you click into a service:

* Code
* Owner
* Documentation
  All complete a closed loop on a single page.

---

### But Honestly: Backstage Isn't Easy

If you've only heard success stories, I need to temper your expectations.

#### It's Not "Install and Use"

Backstage is more like a **framework** than a product.

The real situation is often:

* You'll need to write React / TypeScript
* You'll need to develop plugins
* You'll need to maintain metadata quality

Many companies underestimate this, and as a result:

> Backstage was launched, but no one used it.

#### If Metadata Is Inaccurate, Trust Collapses Instantly

If it happens even once:

* The owner found has left the company
* The documentation is wrong

Developers will revert to the old ways:
**Slack + DMs + word-of-mouth**

---

### So, Should You Choose Backstage?

My own judgment is:

* **Small teams (<50 people)**
  👉 Not recommended for self-hosting, the cost is too high

* **Medium to large engineering organizations**
  👉 If you have a platform team, Backstage is worth serious evaluation

* **Want to see results quickly**
  👉 You can directly look at hosted solutions like Port / Cortex / Roadie

The tool isn't the point; the **philosophy is**.

---

### What's Truly Important Isn't Backstage

Finally, a somewhat "anti-tool" statement.

The core of Backstage's success isn't React, isn't plugins, but rather the three things behind it:

1.  **Clear ownership**
2.  **Standardization first**
3.  **Treating the platform as a product**

If you're just looking to "add another tool," Backstage will likely fail.
But if you truly want to:

> **Let developers spend their time writing code, not searching for information**

Then whether you use Backstage or not, you'll eventually arrive at this path.
```