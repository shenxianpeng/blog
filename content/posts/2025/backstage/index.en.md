```yaml
title: Backstage (Developer Portal)—What It Is, What It Solves, and What It Doesn't Solve
summary: What is Backstage? Why has it become so important in the platform engineering domain? Sharing some insights and judgments on Backstage.
tags:
  - Backstage
authors:
  - shenxianpeng
date: 2025-12-14
---

Recently, I've been pondering a question:
**Can we use `Kubernetes` to provide cloud-based development environments similar to `Codespaces`, `Gitpod`, or `Code Server` for development teams?**

Technically, this isn't new:

* `Kubernetes` handles resource isolation and lifecycle.
* Containers solve environment consistency.
* Cloud-based development can theoretically be out-of-the-box, ephemeral, and instantly available.

However, a more practical problem quickly emerged:

> **What should "manage" these development environments?**

Who can create them?
Which project does the created environment belong to?
How can it be associated with code repositories, `CI`, permissions, and documentation?
Where should developers access it from, instead of having to remember yet another URL?

In a discussion with a friend, he mentioned `Backstage`.
The name wasn't unfamiliar to me, but I had never really taken the time to delve into it.

So, I decided to systematically research `Backstage`. I soon discovered:

> What it solves is not a `Kubernetes` problem, but rather **the problem of how developers "find their way in" complex systems.**

It was from that moment on that I gradually understood why `Backstage` has become so important in the domain of Platform Engineering.

The following article compiles some of my insights and judgments based on these thoughts.

---

## What is Backstage?

A one-sentence version:

> **`Backstage` is not `CI`, not `Kubernetes`, nor a new `DevOps` tool; instead, it's a "unified portal that connects your existing tools."**

It originated from `Spotify`.
The pain points `Spotify` engineers encountered back then are almost identical to ours today:

* Many services
* Many teams
* Many tools
* People come and go, knowledge relies entirely on "tribal memory"

`Backstage`'s original intention was actually very simple:

> **To provide a "household registration book" for all software assets.**

Who is responsible, where it runs, what it depends on, where the documentation is—all visible at a glance.

Later, `Spotify` open-sourced it and donated it to `CNCF`. Today, `Backstage` has become **one of the most representative open-source implementations in the `IDP` (Internal Developer Platform) domain**, and is often considered a de facto reference standard.

---

## Why Platform Engineering?

Many teams initially say:

> We're already doing `DevOps`, why do we need Platform Engineering?

But the reality is:

* `DevOps` emphasizes **"you build it, you run it"**
* Platform Engineering focuses on **"I'll help you simplify the act of building and running it"**

When system complexity increases, expecting **every developer to be proficient in `Kubernetes`, `CI`, security, and monitoring** is actually an efficiency disaster.

The goal of Platform Engineering is not to control developers, but to:

* **Reduce cognitive load**
* **Provide a "default correct" path (Golden Path)**

And `Backstage` happens to be an important vehicle for this philosophy at the engineering level.

---

## Backstage's 3 Most Core Capabilities

If you only remember three points, remember these three.

### Software Catalog

This is `Backstage`'s soul.

You can understand it as:

> **An internal "software asset search engine" for the enterprise.**

Each service places a `catalog-info.yaml` file in its repository to describe:

* Whose service this is
* Which system it belongs to
* Which `API`s it exposes
* Which databases or cloud resources it depends on

`Backstage` organizes this information into a **visualized software relationship network**.

The effect is very intuitive:

* Newcomers no longer rely on asking people to find services
* When problems arise, the scope of impact can be quickly assessed
* "Who is responsible for this thing" is no longer a mystery

Of course, it needs to be clarified:
`Backstage` cannot solve the problem of "no one wants to take responsibility"; it merely **exposes whether responsibility is clear or not.**

---

### Software Templates (Scaffolder / Golden Path)

This is the capability I personally **most recommend prioritizing for implementation**.

In reality, creating a new service often goes like this:

* Requesting a repository
* Configuring `CI`
* Integrating monitoring
* Integrating security scanning
* Adding a bunch of "compliance requirements"

`Backstage`'s templates do something very critical:

> **They turn the "correct posture" directly into a one-click operation.**

Developers only need to fill in a few fields:

* Project name
* Tech stack
* Whether a database is needed

The remaining tasks, such as:

* Repository creation
* `CI` configuration
* Catalog registration

Are all automatically completed.

This is not just an efficiency issue; more importantly:

> **The platform team can finally turn "specifications" into code, instead of leaving them in documentation.**

---

### TechDocs (Docs as Code)

This point is a huge plus for someone like me who has long been skeptical of `Wiki`s.

`TechDocs` advocates a very important principle:

> **Documentation and code are kept together and managed with `Markdown`.**

There's only one benefit, but it's critical:

* Documentation is less likely to become outdated long-term

In `Backstage`, clicking into a service shows:

* Code
* Owner
* Documentation

Forming a complete closed loop on a single page.

---

## What Problems Can't Backstage Solve?

If you've only heard success stories, here's a dose of cold water.

### It's Not "Install and Use"

`Backstage` is more like a **platform framework** than an out-of-the-box product.

The reality usually is:

* You need to write `React` / `TypeScript`
* You need to develop or customize plugins
* You need to continuously maintain Catalog metadata

Many companies underestimate this, and the result is often:

> `Backstage` went live, but developers didn't buy in.

---

### Once Metadata is Inaccurate, Trust Collapses Instantly

As soon as it happens even once:

* The found owner has already left
* The documentation is clearly outdated or incorrect

Developers will quickly revert to the old ways:

> `Slack` + private messages + word-of-mouth

And the problem with the Catalog is often not that it "breaks in a day," but rather that it **slowly loses accuracy when no one is responsible for it.**

---

## Who is Backstage Suitable For?

My personal judgment is:

* **Small teams**
  👉 Self-building is not recommended; the cost is quite high.

* **Medium to large engineering organizations**
  👉 If you have a platform team, `Backstage` is definitely worth a serious evaluation.

* **Those hoping for quicker results**
  👉 You can directly look into hosted solutions like `Port`, `Cortex`, `Roadie`.

The tool itself isn't the focus; **the `IDP` philosophy is.**

---

## Summary

Finally, a somewhat "anti-tool" statement.

The core of `Backstage`'s success has never been `React`, nor its plugin ecosystem, but rather three things:

1. **Whether ownership is clear**
2. **Whether standardization is prioritized**
3. **Whether the platform is operated as a product**

If you're just looking to "add another tool," `Backstage` is likely to fail.
But if what you truly want to do is:

> **Let developers spend their time coding, rather than searching for information**

Then whether you use `Backstage` or not, you will eventually walk this path.
```