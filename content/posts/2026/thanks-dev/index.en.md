---
title: How to Claim the 'Lottery Ticket' of Open Source—Starting from thanks.dev's Operational Mechanism
summary: |
tags:
  - Donation
authors:
  - shenxianpeng
date: 2026-03-15
---

In the previous article, I wrote about receiving a [donation](thanks-canonical) from Canonical, and a reader asked: How did you get selected?

At first, I didn't fully understand it either. Later, after carefully studying thanks.dev's operational mechanism, I finally figured out the underlying logic of the whole thing—and what kind of projects are more likely to be funded by downstream vendors.

---

## How thanks.dev Distributes Funds

The core mechanism of thanks.dev is essentially an **automated dependency tree scanning + proportional distribution** system.

Once downstream vendors integrate, thanks.dev scans the dependencies of all their GitHub repositories, tracing down three levels. Then, donations are distributed based on the "frequency of being depended upon." The more repositories your project appears in, the higher the proportion of donations it receives.

The entire process is fully automated, requiring no manual selection—the algorithm makes the decisions for them.

This explains my situation: badgepy was used in one of Canonical's repositories, entered their dependency tree, and the money flowed automatically. It wasn't because the project was famous, but simply because it was "accidentally used."

---

## Who is Contributing Funds

Currently, the most active major donors on thanks.dev are:

**Sentry** is the platform's largest corporate donor to date, having cumulatively donated over $500,000 in recent years, covering more than 500 open-source projects. They have an internal rule: each engineer has an annual open-source donation budget of $2,000.

**Canonical** (the company behind Ubuntu) has pledged to donate $120,000 within 12 months in 2025, at $10,000 per month, currently covering over 350 GitHub projects—from linters to coverage tools, from the Pallets Project to Sindre Sorhus's personal projects, all are on the list.

**Codecov** ranks second, with cumulative donations of $86,000+.

However, if you do the math, these three largest contributors combined only amount to just over a million dollars. In Silicon Valley, this amount would barely cover the annual salaries of 2 to 3 senior architects.

So, after being distributed among thousands of projects, the amount each project receives is actually very limited. Compared to the time and effort put in by open-source maintainers, this money is completely disproportionate.

Nevertheless, having someone contribute money is far better than companies that use projects without giving anything back. (I won't name names here; everyone knows who they are.)

---

## What Kind of Projects are Easily Selected

This is the most crucial question.

thanks.dev's algorithm doesn't look at star counts or popularity; it only looks at one thing: **whether your project genuinely appears in the dependency tree of downstream vendors.**

This means that the projects most likely to receive funds are often those "unknown but indispensable" foundational tools:

- **Foundational libraries in language ecosystems**: For example, Python's coverage.py, TypeScript's ts-loader, which are used by almost every project and thus frequently appear in dependency trees.
- **Development toolchains**: Linters, formatters, test runners, CI-related tools, which engineers use daily and are highly likely to be found in large repositories.
- **Solutions for specific problems**: They don't need to be comprehensive, but they must solve a real, specific problem, and solve it well enough.

Conversely, application-type projects purely aimed at end-users, or projects not depended upon by any large codebases, are generally outside the algorithm's scope.

---

## A Prerequisite for Being Selected

One point that's easy to overlook: thanks.dev requires project maintainers to **actively register** in order to receive funds.

The algorithm might scan and find you, but if you haven't registered, the money won't flow through.

So, if you maintain an open-source project, even a small one, as long as it has the potential to appear in someone else's dependency tree, there's no harm in registering with thanks.dev—who knows, Sentry or Canonical might scan you one day.

---

## A Final Note

Tidelift's 2024 survey data shows: **Six out of ten open-source maintainers have never received a single penny for maintaining their projects.**

This is the reality of the open-source ecosystem. Most people sustain a project based on passion and spare time, but passion doesn't last forever, and projects can therefore stop updates, become abandoned, or disappear.

The value of mechanisms like thanks.dev isn't just about "giving maintainers some money"; it's more about trying to establish a way for funds to flow, allowing the open-source ecosystem to operate sustainably.

Its scale is still small, but the direction is correct.

To the large companies that truly benefit from open-source projects, you know what you should do. Don't be too greedy.