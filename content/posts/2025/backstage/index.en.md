```
title: Developers Are Getting Tired, So Backstage Emerged
summary: |
  Over the past two years, I've discussed a common sentiment with many DevOps and platform engineers: as systems become increasingly cloud-native, developers are becoming "less focused on development."
tags:
  - Backstage
authors:
  - shenxianpeng
date: 2025-12-14
---

### Developers Are Getting Tired, So Backstage Emerged

Over the past two years, I've discussed a common sentiment with many DevOps and platform engineers:

> **As systems become increasingly cloud-native, developers are becoming "less focused on development."**

A very real scenario:

* Want to modify an old service
* First ask: **Whose is this?**
* Then ask: **Where is it deployed?**
* Is CI using Jenkins or GitHub Actions?
* Is monitoring in Datadog or Prometheus?
* And the documentation? Confluence? Wiki? Or has no one maintained it for ages?

Finally, you'll find:

> Writing code only accounts for 30%, the remaining 70% is spent "finding information."

Thus, the concept of an **Internal Developer Portal (IDP)** began to gain traction.
And one of the most representative among them is **Backstage**.

---

### What Exactly Is Backstage?

One-sentence version:

> **Backstage is not CI, not Kubernetes, nor a new DevOps tool, but rather an "entry point that strings together your existing tools."**

It originated from Spotify.
The pain points Spotify engineers faced back then are almost identical to what we encounter today:

* Many services
* Many teams
* Many tools
* People come and go, knowledge relies entirely on "tribal memory"

Backstage's original intention was very simple:

> **To give every software asset a "household registration book."**

Who is responsible, where it runs, what it depends on, where the documentation is—all visible at a glance.

Later, Spotify open-sourced it and donated it to the CNCF, and it has now become the de facto standard in the IDP (Internal Developer Portal) domain.

---

### Why DevOps Inevitably Leads to Platform Engineering?

Many teams initially say:

> We're already doing DevOps, why do we need Platform Engineering?

But the reality is:

* DevOps emphasizes **"you build it, you run it"**
* Platform Engineering focuses on **"I'll help you make running things simpler"**

As system complexity increases, expecting **every developer to understand Kubernetes, CI, security, and monitoring** is actually an efficiency disaster.

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

> **An "internal software asset search engine" for enterprises**

Each service places a `catalog-info.yaml` in its repository:

* Whose service this is
* Which system it belongs to
* Which APIs it uses
* Which databases / cloud resources it depends on

Backstage then transforms this information into a **visualized relationship network**.

The effects are very clear:

* Newcomers find services without asking around
* When issues arise, the scope of impact can be quickly identified
* "Who is responsible for this thing" is no longer a mystery

---

#### Software Templates (Scaffolder / Golden Path)

This is the capability I personally **most recommend prioritizing for implementation**.

In reality, creating a new service often looks like this:

* Request a repository
* Configure CI
* Integrate monitoring
* Integrate security scanning
* Then add a bunch of "standard requirements"

Backstage's templates do one thing:

> **Turn the "correct posture" into a one-click operation.**

Developers only need to fill in a few fields:

* Project name
* Language
* Whether a database is required

The rest:

* Repository creation
* CI configuration
* Catalog registration
  All completed automatically.

This not only improves efficiency, but more importantly:

> **Platform teams can finally turn "standards" into code, rather than documentation.**

---

#### TechDocs (Docs-as-Code)

This point is a huge plus for someone like me who has long distrusted Wikis.

TechDocs enforces one principle:

> **Documentation is stored alongside code and managed with Markdown.**

There's only one benefit, but it's crucial:

* Documentation will no longer become perpetually outdated

In Backstage, when you click into a service:

* Code
* Responsible person
* Documentation
  All are closed-loop on a single page.

---

### But Honestly: Backstage Isn't Easy

If you've only heard success stories, then I need to pour some cold water on that.

#### It's Not "Install and Use"

Backstage is more like a **framework** than a product.

The reality is often:

* You need to write React / TypeScript
* You need to develop plugins
* You need to maintain metadata quality

Many companies underestimate this, and as a result:

> Backstage goes live, but no one uses it.

#### If Metadata Is Inaccurate, Trust Collapses Instantly

If it happens even once:

* The found responsible person has left the company
* The documentation is incorrect

Developers will revert to the old ways:
**Slack + private chats + word-of-mouth**

---

### So, Should You Choose Backstage?

My own judgment is:

* **Small teams (<50 people)**
  👉 Self-building is not recommended; the cost is too high

* **Medium to large engineering organizations**
  👉 If you have a platform team, Backstage is worth serious evaluation

* **Want to see results quickly**
  👉 You can directly look at hosted solutions like Port / Cortex / Roadie

The tool isn't the focus; the **philosophy is**.

---

### What's Truly Important Is Not Backstage Itself

Finally, a somewhat "anti-tool" statement.

The core of Backstage's success isn't React, isn't plugins, but rather the three things behind it:

1. **Clear ownership**
2. **Standardization first**
3. **Treat the platform as a product**

If you're just looking to "add another tool," Backstage will likely fail.
But if you truly want to:

> **Let developers spend their time writing code, not searching for information**

Then whether you use Backstage or not, you will eventually walk this path.
```