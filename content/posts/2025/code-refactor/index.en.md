---
title: CI/CD—Not a One-Time Project, but a Continuously Evolving System
summary: |
  In DevOps, CI/CD pipelines require continuous maintenance and refactoring. This article explores why CI/CD is not a one-time construction project, but a system that requires long-term investment and continuous evolution.
tags:
  - CI/CD
  - DevOps
authors:
  - shenxianpeng
date: 2025-06-02
---

This article stems from a WeChat Moments post I saw from a former colleague.

<img src="image.png" alt="同事的朋友圈" width="400" height="300" />

I feel like he's **blatantly praising me** :)
(Sorry, had to brag a little~)

But honestly, for the past few years in the CI/CD field, I've been consistently doing two things:

* Keeping up with the latest industry practices;
* Selecting and implementing parts suitable for our business, or writing articles to share.

However, I've noticed a common misconception:

**Many people think that once CI/CD is done, it's done—a set-and-forget solution.**

This is not the case.



## Rome Wasn't Built in a Day, Neither Was CI/CD

Whether it's the CI/CD pipeline, or the underlying programs, tools, libraries, and platforms, they all belong to the infrastructure. A significant characteristic of infrastructure is:

> **It requires long-term investment and continuous maintenance.**

Otherwise, no matter how well you build it now, after a few years, it will become a bloated, uncontrolled "technical debt wasteland" due to lack of maintenance. Eventually, you'll have to start over.

A few examples will make this clear:


## Risks Quickly Emerge Without Maintenance

### 1. Security Risks:

  If you haven't paid attention to [CVE-2024-23897](https://nvd.nist.gov/vuln/detail/CVE-2024-23897), you might not know that your Jenkins has an arbitrary file reading vulnerability, risking intrusion by attackers.

### 2. Missing Functionality and Compatibility Issues:

  Not checking Jenkins' update logs might cause you to miss critical fixes or new features;
  Not updating the CI/CD toolchain might suddenly cause your code to fail compilation or tests.

### 3. Technical Debt Accumulation and Increased Maintenance Costs:

  Without introducing new practices and tools, the pipeline will become increasingly complex and difficult to maintain, leading to a worse development experience.


## Now Let's Look at the Python Project Side

### 1. Still Using `setup.py`?

  Then you might have missed the unified build ecosystem brought by `pyproject.toml` introduced by PEP 518.

### 2. Still Using `pip install` to Install CLI Tools?

  Then you might not know how `pipx` and `uvx` can manage tool dependencies more conveniently and efficiently.

### 3. Unfamiliar with PEPs, Package Structure, and Release Specifications?

  This easily leads to writing non-standard, hard-to-maintain, and non-reusable code.

These issues, seemingly minor on the surface, hide behind them maintenance costs, team collaboration efficiency, and the sustainability of the project's future development.

**Therefore, refactoring is a daily task in software engineering.**

Many times, this work is not obvious, and is even easily considered "doing too much," "fiddling around," or "wasting time."

But in reality, **precisely these "hidden tasks" are the true foundation of software engineering.**

> Without refactoring, the system will only become more bloated;
> Without continuous evolution, CI/CD will eventually become a mess;
> Without continuous learning and exploration, you will drift further and further from best practices.

So, I hope this article can give you some inspiration:

> CI/CD is not a one-time construction project, but a continuously evolving, constantly refactored, and growing DevOps system.

If you are also doing this "invisible work," don't be discouraged. You are laying the foundation for the long-term sustainability of the entire system.

Have you encountered any related pitfalls?  Welcome to share your story in the comments.

---

Please indicate the author and source when reprinting this article, and do not use it for any commercial purposes. Welcome to follow the WeChat official account "DevOps攻城狮"