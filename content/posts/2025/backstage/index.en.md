```
title: Developers Are Getting More and More Tired—So Backstage Emerged
summary: |
tags:
  - Backstage
authors:
  - shenxianpeng
date: 2025-12-14
---

### Developers Are Getting More and More Tired—So Backstage Emerged

In the past two years, I've discussed a common feeling with many `DevOps` and Platform Engineers:

> **Systems are becoming increasingly `cloud-native`, but developers are becoming less and less "focused on development."**

A very real scenario:

* Want to modify an old service
* First ask: **Whose is this?**
* Then ask: **Where is it deployed?**
* Does `CI` use `Jenkins` or `GitHub Actions`?
* Is monitoring on `Datadog` or `Prometheus`?
* What about documentation? `Confluence`? `Wiki`? Or has no one maintained it for ages?

Ultimately, you'll find:

> Writing code only accounts for 30%, with the remaining 70% spent on "finding information."

Consequently, the concept of an **Internal Developer Portal (`IDP`)** started to gain traction.
And one of the most representative of these is **Backstage**.

---

### What Exactly Is Backstage?

One-sentence version:

> **Backstage is not `CI`, not `Kubernetes`, nor is it a new `DevOps` tool; rather, it's an "entry point that stitches your existing tools together."**

It originated from `Spotify`.
The pain points `Spotify` engineers faced back then are almost identical to what we encounter today:

* Many services
* Many teams
* Many tools
* People come and go, knowledge relies entirely on "tribal memory"

Backstage's initial intention was very simple:

> **To give all software assets a "household registration book."**

Who is responsible, where it runs, what it depends on, and where the documentation is – all visible at a glance.

Later, `Spotify` open-sourced it and donated it to `CNCF`, and it has now become the de facto standard in the `IDP` (`Internal Developer Portal`) domain.

---

### Why `DevOps` Inevitably Leads to Platform Engineering in the Long Run

Many teams initially say:

> We are already doing `DevOps`, why do we still need Platform Engineering?

But the reality is:

* `DevOps` emphasizes **"you build it, you run it"**
* Platform Engineering focuses on **"I'll help you make running things simpler"**

Once system complexity increases, expecting **every developer to understand `Kubernetes`, `CI`, security, and monitoring** is actually an efficiency disaster.

The goal of Platform Engineering is not to control developers, but to:

* **Reduce cognitive load**
* **Provide "default-correct" paths**

And `Backstage` happens to be the implementation vehicle for this philosophy.

---

### Backstage's 3 Most Core Capabilities

If you only remember three points, remember these three.

#### Software Catalog

This is the soul of `Backstage`.

You can think of it as:

> **An enterprise-internal "software asset search engine"**

Each service places a `catalog-info.yaml` in its repository:

* Whose service is this
* Which system it belongs to
* Which `API`s it uses
* Which databases / cloud resources it depends on

Then `Backstage` transforms this information into a **visualized relationship network**.

The effect is very clear:

* Newcomers find services without relying on asking people
* When problems arise, quickly locate the scope of impact
* "Who is responsible for this thing" is no longer a mystery

---

#### Software Templates (`Scaffolder` / `Golden Path`)

This is the capability I personally **most recommend prioritizing for implementation**.

In reality, creating a new service often looks like this:

* Apply for a repository
* Configure `CI`
* Integrate monitoring
* Integrate security scanning
* And then add a bunch of "standard requirements"

`Backstage`'s templates do one thing:

> **Turn "the correct posture" into a one-click operation.**

Developers only need to fill in a few fields:

* Project name
* Language
* Whether a database is needed

The rest:

* Repository creation
* `CI` configuration
* Catalog registration
  All completed automatically.

This not only improves efficiency, but more importantly:

> **Platform teams can finally turn "standards" into code, not documentation.**

---

#### `TechDocs` (Documentation as Code)

This point is a huge plus for someone like me who has long been skeptical of `Wiki`s.

`TechDocs` enforces one principle:

> **Documentation and code are kept together, managed with `Markdown`.**

There's only one benefit, but it's crucial:

* Documentation will no longer become long-term outdated

In `Backstage`, when you click into a service:

* Code
* Owner
* Documentation
  All form a closed loop on a single page.

---

### But Honestly: Backstage Is Not Easy

If you've only heard success stories, then I need to pour some cold water on that.

#### It's Not "Install and Use"

`Backstage` is more like a **framework** than a product.

The reality is often:

* Requires writing `React` / `TypeScript`
* Requires developing plugins
* Requires maintaining metadata quality

Many companies underestimate this, and as a result:

> `Backstage` was launched, but no one used it.

#### Once Metadata Is Inaccurate, Trust Will Instantly Collapse

Even if it only happens once:

* The owner found has left the company
* The documentation is incorrect

Developers will revert to old habits:
**`Slack` + private chats + word-of-mouth**

---

### So, Should You Choose Backstage Or Not?

My own judgment is:

* **Small teams (<50 people)**
  👉 Not recommended for self-hosting, costs are too high

* **Medium-to-large engineering organizations**
  👉 If you have a platform team, `Backstage` is worth serious evaluation

* **Want to see quick results**
  👉 You can directly look at managed solutions like `Port` / `Cortex` / `Roadie`

The tool isn't the point; the **philosophy is**.

---

### What's Truly Important Isn't Actually Backstage

Finally, a somewhat "anti-tool" statement.

The core of `Backstage`'s success is not `React`, not plugins, but the three things behind it:

1.  **Clear ownership**
2.  **Standardization first**
3.  **Treat the platform as a product**

If you're just looking to "add another tool," then `Backstage` will likely fail.
But if you truly want to:

> **Let developers spend their time writing code, not finding information**

Then whether you use `Backstage` or not, you'll eventually arrive at this path.
```