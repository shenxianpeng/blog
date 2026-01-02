```
title: 开发者越来越累了，于是有了 Backstage
summary: |
  Developers are getting bogged down searching for information rather than coding. This post introduces Backstage, an Internal Developer Portal (IDP) from Spotify, as a solution. It highlights how Backstage aids platform engineering by providing a Software Catalog, Scaffolder for golden paths, and TechDocs for docs-as-code, all aimed at reducing cognitive load. The post also provides a realistic view, noting Backstage isn't plug-and-play and requires effort to maintain metadata quality. It concludes by emphasizing that the underlying principles—clear ownership, standardization, and treating the platform as a product—are more crucial than the tool itself for empowering developers.
tags:
  - Backstage
authors:
  - shenxianpeng
date: 2025-12-14
---

### Developers are Getting More and More Tired, So Backstage Emerged

Over the past two years, I've discussed a common feeling with many DevOps and platform engineers:

> **Systems are becoming more cloud-native, but developers are becoming "less focused on development".**

A very real scenario:

* Want to modify an old service
* First ask: **Whose is this?**
* Then ask: **Where is it deployed?**
* Does CI use Jenkins or GitHub Actions?
* Is monitoring on Datadog or Prometheus?
* What about documentation? Confluence? Wiki? Or has no one maintained it for ages?

Finally, you'll find:

> Writing code only accounts for 30%, while the remaining 70% is spent "searching for information".

Thus, the concept of an **Internal Developer Portal** started to gain traction.
And one of the most representative of these is **Backstage**.

---

### What Exactly is Backstage?

One-sentence version:

> **Backstage is not CI, not Kubernetes, nor a new DevOps tool; it's an "entry point that connects your existing tools".**

It originated from Spotify.
The pain points Spotify engineers faced back then are almost identical to what we encounter today:

* Many services
* Many teams
* Many tools
* People come and go, knowledge relies entirely on "tribal memory"

Backstage's initial intention was very simple:

> **To give all software assets a "household registration book".**

Who is responsible, where it runs, what it depends on, where the documentation is—all visible at a glance.

Later, Spotify open-sourced it and donated it to the CNCF, and it has now become the de facto standard in the IDP (Internal Developer Portal) domain.

---

### Why DevOps Will Inevitably Evolve Towards Platform Engineering?

Many teams initially say:

> We're already doing DevOps, why do we need platform engineering?

But the reality is:

* DevOps emphasizes **"you build it, you run it"**
* Platform engineering focuses on **"I'll help you simplify the running part"**

When system complexity increases, expecting **every developer to understand Kubernetes, CI, security, and monitoring** is actually an efficiency disaster.

The goal of platform engineering is not to control developers, but to:

* **Reduce cognitive load**
* **Provide "default-correct" paths**

And Backstage, precisely, is the embodiment of this philosophy.

---

### Backstage's 3 Core Capabilities

If you only remember three points, remember these three.

#### Software Catalog

This is the soul of Backstage.

You can understand it as:

> **An enterprise's internal "software asset search engine"**

Each service places a `catalog-info.yaml` in its repository:

* Whose service this is
* Which system it belongs to
* Which APIs it uses
* Which databases / cloud resources it depends on

Then Backstage transforms this information into a **visual relationship network**.

The effects are very clear:

* Newcomers find services without asking others
* When issues arise, quickly pinpoint the scope of impact
* "Who is responsible for this thing" is no longer a mystery

---

#### Software Templates (Scaffolder / Golden Path)

This is the capability I personally **most recommend implementing first**.

In reality, creating a new service often looks like this:

* Apply for a repository
* Configure CI
* Integrate monitoring
* Integrate security scanning
* And then add a bunch of "compliance requirements"

Backstage's templates do one thing:

> **Turn "the right way" into a one-click operation.**

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

> **Platform teams can finally turn "standards" into code, rather than documentation.**

---

#### TechDocs (Docs-as-Code)

This point is a huge plus for someone like me who has long distrusted Wikis.

TechDocs enforces one principle:

> **Documentation and code are kept together and managed with Markdown.**

There's only one benefit, but it's crucial:

* Documentation will no longer become stale for long periods

In Backstage, when you click into a service:

* Code
* Owner
* Documentation
  All complete a closed loop on a single page.

---

### But Honestly: Backstage Is Not Easy

If you've only heard success stories, I need to pour some cold water on that.

#### It's Not "Install and Use"

Backstage is more like a **framework**, not a product.

The reality is often:

* You need to write React / TypeScript
* You need to develop plugins
* You need to maintain metadata quality

Many companies underestimate this, and as a result:

> Backstage went live, but no one used it.

#### Once Metadata is Inaccurate, Trust Collapses Instantly

As soon as it happens once:

* The owner found has left the company
* The documentation is wrong

Developers will revert to old habits:
**Slack + private chats + word-of-mouth**

---

### So, Should You Choose Backstage?

My own judgment is:

*   **Small teams (<50 people)**
    👉 Not recommended for self-hosting, costs are too high

*   **Medium to large engineering organizations**
    👉 If you have a platform team, Backstage is worth serious evaluation

*   **Want to see quick results**
    👉 Can directly look at hosted solutions like Port / Cortex / Roadie

Tools are not the focus, **the philosophy is**.

---

### What's Truly Important Isn't Backstage

Finally, a somewhat "anti-tool" statement.

The core of Backstage's success isn't React, isn't plugins, but the three things behind it:

1.  **Clear ownership**
2.  **Standardization first**
3.  **Treat the platform as a product**

If you just want to "add another tool", Backstage will likely fail.
But if you truly want to:

> **Let developers spend their time writing code, not searching for information**

Then whether you use Backstage or not, you'll eventually walk this path.
```