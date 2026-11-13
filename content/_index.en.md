---
title: "Keep software shipping."
heroRole: "DevOps and release engineer since 2009 · Vilnius, Lithuania"
heroLead: "Open-source tools that keep software shipping, whether a person or an AI agent wrote the code, even after upstream moves on."
heroButtons:
  - label: "See the projects"
    url: "/portfolio/"
  - label: "Read the blog"
    url: "/posts/"
    style: "outline"
heroAlso:
  label: "From commit to release, and long after"
  stages:
    - stage: "commit"
      note: "One policy for commit messages, branch names and AI attribution."
      links:
        - label: "commit-check"
          url: "https://commit-check.com/"
        - label: "Conventional Branch"
          url: "https://conventionalbranch.org/"
    - stage: "review"
      note: "clang-format and clang-tidy on every pull request."
      links:
        - label: "cpp-linter"
          url: "https://cpp-linter.github.io/"
    - stage: "build"
      note: "AI diagnosis of failed Jenkins builds, and Java 8 build hosts on a current Jenkins."
      links:
        - label: "explain-error"
          url: "https://github.com/jenkinsci/explain-error-plugin"
        - label: "Agent8"
          url: "https://keelinfra.io/jenkins/"
    - stage: "release"
      note: "SBOM, signed provenance and alerts for exploited vulnerabilities, as the EU Cyber Resilience Act asks."
      links:
        - label: "release-ledger"
          url: "https://keelinfra.io/cra/"
    - stage: "support"
      note: "Security fixes for the last Jenkins LTS on Java 17, and MkDocs 1.x, maintained."
      links:
        - label: "Jenkins Extended Security"
          url: "https://github.com/keelinfra/jenkins-extended-security"
        - label: "MkDocs NG"
          url: "https://mkdocs-ng.org/"
proof:
  stats:
    - value: "750,000+"
      label: "downloads of the clang-tools static binaries"
    - value: "1,000+"
      label: "GitHub repositories depend on cpp-linter"
    - value: "55,000+"
      label: "PyPI downloads of commit-check a month"
  usersLabel: "cpp-linter is used by projects from"
  users: ["AWS", "Apache", "Samsung", "Qualcomm", "Bloomberg", "LLNL", "Nextcloud"]
flagship:
  label: "cpp-linter"
  title: "Lint every pull request."
  text: "clang-format and clang-tidy on each PR, as a GitHub Action, a pre-commit hook and a Python package. Fixes arrive as review suggestions you can commit in one click. The clang tools come from static binaries for every LLVM version."
  links:
    - label: "Documentation"
      url: "https://cpp-linter.github.io/"
    - label: "GitHub"
      url: "https://github.com/cpp-linter"
  demo: "cpp-linter"
  demoLabel: "Animated demo of cpp-linter on a GitHub pull request: the check fails, cpp-linter posts a clang-format suggestion, the suggestion is committed, and the check passes."
products:
  title: "Infrastructure you own."
  text: "Jenkins agents for build hosts stuck on Java 8, Atlassian apps that run inside your own tenant, and Mac backups to your own storage."
  items:
    - name: "keelinfra"
      label: "Free · Open source · Support plans"
      text: "Agent8 keeps build hosts stuck on Java 8, such as AIX, Solaris and HP-UX, connected to a current Jenkins as ordinary agents."
      url: "https://keelinfra.io/jenkins/"
      preview: "agent8"
      style: "card"
      tone: "dark"
    - name: "keelapps"
      label: "Atlassian Marketplace"
      text: "Twelve apps for Jira and Confluence Cloud: permission audits, recurring tasks, scheduled reports, page approvals, and bulk page and attachment tools."
      url: "https://keelapps.app"
      preview: "accesslens"
      style: "card"
      tone: "mint"
    - name: "Keelhaven"
      label: "Free · Open source · macOS 14+"
      text: "Mac backup to storage you own. A native menu bar app over restic; files are encrypted before they leave your Mac."
      url: "https://keelhaven.app"
      preview: "keelhaven"
      style: "card"
  moreLabel: "Learn more"
writing:
  title: "Writing."
  text: "Since 2017, in Chinese and English."
sponsor:
  text: "If one of these tools saves you time, sponsoring keeps it maintained."
  label: "Sponsor on GitHub"
  url: "https://github.com/sponsors/shenxianpeng"
---
