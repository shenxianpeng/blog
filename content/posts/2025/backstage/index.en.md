```
title: Developers Are Getting More Tired—So Backstage Emerged
summary: |
tags:
  - Backstage
authors:
  - shenxianpeng
date: 2025-12-14
---

In the past two years, I've discussed a common sentiment with many DevOps and platform engineers:

> **Systems are becoming increasingly cloud-native, but developers are becoming 'less focused on development.'**

A very real scenario:

*   Want to modify an old service
*   First, ask: **Whose is this?**
*   Then, ask: **Where is it deployed?**
*   Does CI use Jenkins or GitHub Actions?
*   Is monitoring on Datadog or Prometheus?
*   What about documentation? Confluence? Wiki? Or has no one maintained it for ages?

Eventually, you'll find:

> Coding only accounts for 30%, while the remaining 70% is spent 'searching for information.'

The problem is often not that there aren't enough tools, but that—
**Every developer is forced to understand too many things outside their scope of responsibility.**

Consequently, the concept of an **Internal Developer Portal (IDP)** started gaining traction.
And one of the most representative of these is **Backstage**.

---

## What Exactly Is Backstage?

One-sentence version:

> **Backstage is not CI, not Kubernetes, nor a new DevOps tool; rather, it's a 'unified entry point that connects your existing tools.'**

It originated from Spotify.
The pain points Spotify engineers encountered back then are almost identical to ours today:

*   Many services
*   Many teams
*   Many tools
*   People come and go, knowledge relies entirely on 'tribal memory'

Backstage's original intention was actually very simple:

> **To give all software assets an 'official record.'**

Who is responsible, where it runs, what it depends on, and where the documentation is – all visible at a glance.

Later, Spotify open-sourced it and donated it to the CNCF. Today, Backstage has become **one of the most representative open-source implementations in the IDP space**, and is often considered a de-facto standard.

---

## Why DevOps Will Inevitably Evolve into Platform Engineering?

Many teams initially say:

> We're already doing DevOps, why do we need platform engineering?

But the reality is:

*   DevOps emphasizes **'you build it, you run it'**
*   Platform engineering focuses on **'I'll help you make building and running simpler'**

As system complexity increases, expecting **every developer to master Kubernetes, CI, security, and monitoring** is actually an efficiency disaster.

The goal of platform engineering is not to control developers, but to:

*   **Reduce cognitive load**
*   **Provide 'default-correct' paths (Golden Paths)**

And Backstage perfectly serves as a crucial vehicle for this philosophy at an engineering level.

---

## The 3 Core Capabilities of Backstage

If you only remember three points, remember these three.

### Software Catalog

This is the soul of Backstage.

You can understand it as:

> **An 'enterprise internal software asset search engine.'**

Each service places a `catalog-info.yaml` in its repository to describe:

*   Whose service it is
*   Which system it belongs to
*   Which APIs it exposes
*   Which databases or cloud resources it depends on

Backstage organizes this information into a **visual software relationship network**.

The effect is very intuitive:

*   Newcomers find services without having to ask people
*   When problems arise, the scope of impact can be quickly assessed
*   'Who is responsible for this thing' is no longer a mystery

Of course, it's worth noting:
Backstage doesn't solve the problem of 'no one wanting to be responsible'; it merely **exposes whether responsibilities are clear or not**.

---

### Software Templates (Scaffolder / Golden Path)

This is the capability I personally **most recommend prioritizing for implementation**.

In reality, creating a new service often goes like this:

*   Request a repository
*   Configure CI
*   Integrate monitoring
*   Integrate security scanning
*   Then add a bunch of 'compliance requirements'

Backstage's templates do something very critical:

> **They turn 'the correct approach' directly into a one-click operation.**

Developers only need to fill in a few fields:

*   Project name
*   Tech stack
*   Whether a database is needed

The rest of the tasks, such as:

*   Repository creation
*   CI configuration
*   Catalog registration

Are all completed automatically.

This is not just an efficiency issue; more importantly:

> **Platform teams can finally turn 'specifications' into code, instead of leaving them in documentation.**

---

### TechDocs (Docs-as-Code)

This point is a huge plus for someone like me who has long been skeptical of Wikis.

TechDocs advocates for a very important principle:

> **Documentation and code are kept together, managed with Markdown.**

There's only one benefit, but it's crucial:

*   Documentation is less likely to become outdated long-term

In Backstage, when you click into a service:

*   Code
*   Responsible party
*   Documentation

Can form a complete closed loop on a single page.

---

## But Honestly: Backstage Is Not Easy

If you've only heard success stories, here's a splash of cold water.

### It's Not 'Install-and-Use'

Backstage is more like a **platform framework** than an out-of-the-box product.

The reality is usually:

*   You need to write React / TypeScript
*   You need to develop or customize plugins
*   You need to continuously maintain Catalog metadata

Many companies underestimate this, and the result is often:

> Backstage is live, but developers aren't buying into it.

---

### Once Metadata Is Inaccurate, Trust Collapses Instantly

Even if it happens just once:

*   The responsible person found has already left
*   The documentation is clearly outdated or incorrect

Developers will quickly revert to old ways:

> Slack + private messages + word of mouth

And the problem with the Catalog isn't usually that it 'breaks overnight,' but rather that it **slowly becomes inaccurate when no one is responsible for it**.

---

## So, Should You Choose Backstage Or Not?

My personal judgment is:

*   **Small teams (<50 people)** 👉 Self-building is not recommended; the cost is too high.

*   **Medium to large engineering organizations** 👉 If you have a platform team, Backstage is very much worth serious evaluation.

*   **Want to see results faster** 👉 You can directly look into managed solutions like Port, Cortex, Roadie.

The tool itself isn't the key; **the IDP philosophy is**.

---

## What's Truly Important Isn't Backstage Itself

Finally, let me say something that might sound a bit 'anti-tool.'

The core of Backstage's success has never been React, nor its plugin ecosystem, but three things:

1.  **Is ownership clear?**
2.  **Is standardization prioritized?**
3.  **Is the platform operated as a product?**

If you're just looking to 'adopt another tool,' Backstage is likely to fail.
But if what you truly want to do is:

> **Allow developers to spend their time writing code, not searching for information**

Then, whether you use Backstage or not, you will eventually reach this path.
```