---
title: Conventional Branch Now Has Its Own Domain—conventionalbranch.org
summary: |
  The Conventional Branch project website has officially migrated from conventional-branch.github.io to conventionalbranch.org. From last year's user suggestion to this year's final implementation, let's talk about the hesitations, pitfalls, and reflections behind the domain migration.
tags:
  - Conventional Branch
  - Open Source
authors:
  - shenxianpeng
date: 2026-05-31
---


Conventional Branch finally has its own independent domain.

Starting today, you can access the official Conventional Branch website via **[conventionalbranch.org](https://conventionalbranch.org)**. All project documentation (specifications, installation guides, FAQs, etc.) has been migrated to the new domain.

The old domain `conventional-branch.github.io` will still redirect, but the official address has switched to conventionalbranch.org.

## Why This Change Was Made

The starting point for this was actually a suggestion from a user last year.

At the time, he commented on a GitHub issue, saying that Conventional Branch, as an independent project with clear specifications, felt less formal using a GitHub Pages subdomain, and suggested I consider registering an independent domain.

Honestly, I was quite hesitant then.

Conventional Branch is a purely open-source project with no commercial revenue. Registering a domain and renewing it annually means I'd have to bear these costs myself. It wasn't that I didn't want to do it; I just wondered if it was "necessary."

But I kept the user's suggestion in mind. After some thought, I decided to register a domain first.

## A Less-Than-Satisfactory Start

Subsequently, I actually purchased a domain: **conventionalbranches.org**.

Why "branches" instead of "branch"?

I was in a hurry when I bought it, and at the time, I just thought, "The project is called Conventional Branch, and branches are 'branches,' so using the plural seems reasonable."

But the more I thought about it after purchasing, the more I felt it was wrong—the project name is **Conventional Branch**, singular. `conventionalbranches.org` doesn't roll off the tongue and doesn't fully match the project name.

So, after buying that domain, it just sat there, unused.

## This Year's Turning Point

Things have changed this year.

Firstly, both the user base and usage of Conventional Branch are growing.

The project website's monthly traffic is already quite significant, and the GitHub repository's stars are steadily increasing. More and more teams are using the Conventional Branch specification to manage branch naming in their daily development.

Secondly, I've added a lot of new features to the project this year.

For example, the [official Agent Skill](https://github.com/conventional-branch/conventional-branch/blob/main/skills/conventional-branch/SKILL.md) launched last month allows AI coding agents to create branches according to Conventional Branch rules. You can install this Skill using `npx skills add conventional-branch/conventional-branch --skill conventional-branch`, enabling AI to automatically follow the specification when creating branches.

Additionally, I've also submitted this Skill to GitHub's official [awesome-copilot](https://github.com/github/awesome-copilot) project.

You can directly install this Skill using `gh skills install github/awesome-copilot conventional-branch`, allowing Copilot to automatically follow the Conventional Branch specification when creating branches.

Furthermore, the Conventional Branch ecosystem is expanding. In addition to the core specification itself, the accompanying [commit-check](https://github.com/commit-check/commit-check) tool is continuously being iterated upon, helping developers more easily check if Git Metadata conforms to the specification.

Considering these changes, I felt it was time to give Conventional Branch a formal domain. While there's nothing functionally wrong with using a GitHub Pages domain, having an independent domain makes a project with a complete ecosystem and clear specifications appear more formal and reliable.

So this time, I purchased the domain: **conventionalbranch.org**.

## What Was Done for the Migration

The domain migration itself wasn't overly complex; primarily, a few things were done:

*   **DNS and Hosting Configuration.** Pointed conventionalbranch.org to GitHub Pages and enabled HTTPS.
*   **Old Domain Redirection.** conventional-branch.github.io retains redirection, so users accessing the old domain will be automatically redirected to the new one. Existing bookmarks, documentation links, and references in READMEs will not break.
*   **Website Verification (Verify).** Completed GitHub's domain verification to ensure the new domain is correctly recognized and used on GitHub Pages.
*   **Documentation Update.** All instances referencing the old domain in the project repository, such as READMEs, internal document links, and Skill configurations, have been updated to the new domain.

Throughout the entire process, there was no noticeable impact on users; the accessed content remains the same, only the URL in the address bar has changed.

## In Conclusion

From a user's suggestion last year, to buying the wrong domain, and finally purchasing the correct one and completing the migration last weekend, this matter dragged on for quite some time.

However, for an open-source project, some things shouldn't be rushed.

Buying a domain when the user base is insufficient might just be for self-gratification; but when the user base, ecosystem, and project maturity all reach an appropriate point, then doing it becomes a natural progression.

Thanks to the user who made the suggestion last year, and thanks to all developers who use Conventional Branch.

If you'd like to support Conventional Branch, you can do so in the following ways:

*   Follow / Star the project on GitHub: [github.com/conventional-branch](https://github.com/conventional-branch)
*   Share and recommend Conventional Branch on social media
*   Participate in project discussions and contributions, submit issues or pull requests
*   Support me in continuing to maintain and develop Conventional Branch and other open-source projects via donations or [GitHub Sponsors](https://github.com/sponsors/shenxianpeng)

If you want to learn more, you can visit:

*   Official Website: [conventionalbranch.org](https://conventionalbranch.org)
*   GitHub: [github.com/conventional-branch/conventional-branch](https://github.com/conventional-branch/conventional-branch)
*   Accompanying Tool: [commit-check/scommit-check](https://github.com/commit-check/commit-check)

Thanks for your attention, see you next time~

---

Please cite the author and source when reproducing articles from this site. Do not use for any commercial purposes. Feel free to follow the official account "沈显鹏".