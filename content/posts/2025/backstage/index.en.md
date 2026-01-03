```
title: Developers Are Getting Tired, So Backstage Emerged
summary: |
  In the past two years, I've discussed a common feeling with many DevOps and platform engineers:

  > **Systems are becoming more cloud-native, but developers are becoming "less focused on development."**

  A very real scenario:

  * Want to modify an old service
  * First ask: **Whose is this?**
  * Then ask: **Where is it deployed?**
  * Does CI use Jenkins or GitHub Actions?
  * Is monitoring in Datadog or Prometheus?
  * What about documentation? Confluence? Wiki? Or has no one maintained it for ages?

  Eventually, you'll find:

  > Writing code only accounts for 30%, the remaining 70% is spent "finding information."

  Consequently, the concept of an **Internal Developer Portal** started gaining traction.
  And one of the most representative among them is **Backstage**.
tags:
  - Backstage
authors:
  - shenxianpeng
date: 2025-12-14
---

### Developers Are Getting Tired, So Backstage Emerged

In the past two years, I've discussed a common feeling with many DevOps and platform engineers:

> **Systems are becoming more cloud-native, but developers are becoming "less focused on development."**

A very real scenario:

* Want to modify an old service
* First ask: **Whose is this?**
* Then ask: **Where is it deployed?**
* Does CI use Jenkins or GitHub Actions?
* Is monitoring in Datadog or Prometheus?
* What about documentation? Confluence? Wiki? Or has no one maintained it for ages?

Eventually, you'll find:

> Writing code only accounts for 30%, the remaining 70% is spent "finding information."

Consequently, the concept of an **Internal Developer Portal** started gaining traction.
And one of the most representative among them is **Backstage**.

---

### What Exactly Is Backstage?

One-sentence version:

> **Backstage is not CI, not Kubernetes, nor a new DevOps tool; it's an "entry point that stitches your existing tools together."**

It originated from Spotify.
The pain points Spotify engineers faced back then are almost identical to what we encounter today:

* Many services
* Many teams
* Many tools
* People come and go, knowledge relies entirely on "tribal memory"

Backstage's initial intention was very simple:

> **To give all software assets a "registry."**

Who is responsible, where it runs, what it depends on, where the documentation is—all visible at a glance.

Later, Spotify open-sourced it and donated it to the CNCF; it has now become the de facto standard in the IDP (Internal Developer Portal) domain.

---

### Why DevOps Inevitably Leads to Platform Engineering

Many teams initially say:

> We're already doing DevOps, why do we need platform engineering?

But the reality is:

* DevOps emphasizes **"you build it, you run it"**
* Platform engineering focuses on **"I help you simplify the act of running it"**

When system complexity increases, expecting **every developer to understand Kubernetes, CI, security, and monitoring** is actually an efficiency disaster.

The goal of platform engineering is not to control developers, but to:

* **Reduce cognitive load**
* **Provide "default-correct" paths**

And Backstage happens to be the vehicle for implementing this philosophy.

---

### Backstage's 3 Core Capabilities

If you only remember three points, remember these.

#### Software Catalog

This is the soul of Backstage.

You can think of it as:

> **An "enterprise internal software asset search engine"**

Each service places a `catalog-info.yaml` in its repository:

* Whose service this is
* Which system it belongs to
* Which APIs it uses
* Which databases / cloud resources it depends on

Backstage then transforms this information into a **visualized relationship network**.

The effects are very clear:

* Newcomers can find services without having to ask around
* When issues arise, quickly pinpoint the scope of impact
* "Who is responsible for this thing" is no longer a mystery

---

#### Software Templates (Scaffolder / Golden Path)

This is the capability I personally **most recommend implementing first**.

In reality, creating a new service often goes like this:

* Apply for a repository
* Configure CI
* Hook up monitoring
* Integrate security scanning
* Then add a bunch of "compliance requirements"

Backstage's templates do one thing:

> **Turn the "correct way" into a one-click operation.**

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

> **Platform teams can finally turn "specifications" into code, rather than documentation.**

---

#### TechDocs (Docs-as-Code)

This point is a huge plus for someone like me who has long distrusted Wikis.

TechDocs enforces one principle:

> **Documentation and code are kept together, managed with Markdown.**

There's only one benefit, but it's crucial:

* Documentation will no longer become outdated for long periods

In Backstage, when you click into a service:

* Code
* Owners
* Documentation
All complete a closed loop on a single page.

---

### But To Be Honest: Backstage Is Not Easy

If you've only heard success stories, then I need to temper your expectations.

#### It's Not "Install and Use"

Backstage is more like a **framework** than a product.

The reality is often:

* You need to write React / TypeScript
* You need to develop plugins
* You need to maintain metadata quality

Many companies underestimate this, and the result is:

> Backstage is live, but no one uses it.

#### If Metadata Is Inaccurate, Trust Will Instantly Collapse

As soon as it happens once:

* The owner found has left the company
* The documentation is wrong

Developers will revert to the old ways:
**Slack + direct messages + word-of-mouth**

---

### So, Should You Choose Backstage Or Not?

My own judgment is:

* **Small teams (<50 people)**
  👉 Not recommended for self-hosting, the cost is too high

* **Medium to large engineering organizations**
  👉 If you have a platform team, Backstage is worth serious evaluation

* **Want to see results quickly**
  👉 You can directly look into managed solutions like Port / Cortex / Roadie

The tool isn't the key; the **philosophy is**.

---

### What's Truly Important Isn't Backstage

Finally, a statement that might be a bit "anti-tool theory."

The core of Backstage's success isn't React, isn't plugins, but the three things behind it:

1.  **Clear ownership**
2.  **Standardization first**
3.  **Treat the platform as a product**

If you just want to "add another tool," then Backstage is likely to fail.
But if you truly want to:

> **Let developers spend their time writing code, not searching for information**

Then whether you use Backstage or not, you'll eventually arrive at this path.
```