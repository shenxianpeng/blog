---
title: "Open-source guardrails for software delivery."
heroCaption: "Xianpeng Shen · Engineer. Builder. Maintainer."
heroLead: "Linting, commit standards, and CI/CD automation — maintained in the open, and running in the CI of more than 1000 public repositories."
heroButtons:
  - label: "Read the blog"
    url: "/posts/"
  - label: "See the projects"
    url: "/portfolio/"
    style: "outline"
---

I'm Xianpeng Shen, in Vilnius, Lithuania. I work on how software gets built, tested and shipped: CI/CD, build and release, infrastructure, and the tools around them. I maintain [cpp-linter](https://github.com/cpp-linter), and I build two products: [keelinfra](https://keelinfra.io) (self-hosted Keycloak for production) and [keelapps](https://keelapps.app) (admin tools for Jira and Confluence). If my tools save you time, [sponsoring the work](https://github.com/sponsors/shenxianpeng) keeps them maintained.

## What I build

{{< feature-grid columns="2" align="left" >}}
{{< feature icon="check" title="cpp-linter" url="https://github.com/cpp-linter" label="Open source" >}}
clang-format and clang-tidy on every pull request, as a GitHub Action, a pre-commit hook, and a Python package. In the CI of Apache, Samsung, Qualcomm, Bloomberg, LLNL, and Nextcloud.
{{< /feature >}}
{{< feature icon="lock" title="keelinfra" url="https://keelinfra.io" label="Product" >}}
Self-hosted Keycloak you can run in production: HA, backups with point-in-time recovery, monitoring, and upgrade paths re-tested nightly in public CI.
{{< /feature >}}
{{< feature icon="list-check" title="keelapps" url="https://keelapps.app" label="Product" >}}
Admin tools for Jira and Confluence Cloud: permission audits, recurring tasks, scheduled reports, page approvals. Built on Atlassian Forge, so each app runs inside your own tenant.
{{< /feature >}}
{{< feature icon="apple" title="Keelhaven" url="https://keelhaven.app" label="Free app" >}}
Mac backup to storage you own. A native menu bar app over restic; files are encrypted on your Mac before they leave it. Free and open source.
{{< /feature >}}
{{< /feature-grid >}}
