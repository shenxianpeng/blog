---
title: "Keep software shipping."
heroRole: "DevOps and release engineer since 2009 · Vilnius"
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
      note: "Commit message, branch name and AI-attribution policy"
      links:
        - label: "commit-check"
          url: "https://commit-check.com/"
        - label: "Conventional Branch"
          url: "https://conventionalbranch.org/"
    - stage: "review"
      note: "clang-format and clang-tidy on every pull request"
      links:
        - label: "cpp-linter"
          url: "https://cpp-linter.github.io/"
          tag: "flagship"
    - stage: "build"
      note: "AI diagnosis of Jenkins failures; Java 8 hosts on a current Jenkins"
      links:
        - label: "explain-error"
          url: "https://github.com/jenkinsci/explain-error-plugin"
        - label: "Agent8"
          url: "https://keelinfra.io/jenkins/"
    - stage: "release"
      note: "SBOM, signed provenance, exploited-CVE watch for the EU CRA"
      links:
        - label: "release-ledger"
          url: "https://keelinfra.io/cra/"
    - stage: "support"
      note: "Security fixes for the last Jenkins LTS on Java 17; MkDocs 1.x, maintained"
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
    - value: "Jenkins org"
      label: "member, two projects under jenkinsci"
    - value: "Top 3"
      label: "in Lithuania for public contributions"
  usersLabel: "cpp-linter is used by projects from"
  users: ["AWS", "Apache", "Samsung", "Qualcomm", "Bloomberg", "LLNL", "Nextcloud"]
flagship:
  label: "cpp-linter"
  title: "Lint every pull request."
  text: "clang-format and clang-tidy on each PR, as a GitHub Action, a pre-commit hook and a Python package. Fixes arrive as review suggestions you can commit in one click."
  chips: ["thread comment", "PR review suggestions", "step summary", "auto-fix"]
  chipActive: "PR review suggestions"
  links:
    - label: "Documentation"
      url: "https://cpp-linter.github.io/"
    - label: "GitHub"
      url: "https://github.com/cpp-linter"
  demo: "cpp-linter-review"
  demoLabel: "cpp-linter on a GitHub pull request: a clang-format suggestion from github-actions on src/demo.hpp that puts a constructor's initialiser list on separate lines, with a Commit suggestion button under it, and the cpp-linter check passing."
features:
  - label: "commit-check"
    title: "Commit policy as code."
    text: "Commit messages, branch names, authors, sign-offs, tags, files and AI attribution, checked from one config file. In CI, as a pre-commit hook, or by an AI agent reading its JSON output."
    chips: ["GitHub Action", "pre-commit hook", "--format json", "AI attribution"]
    chipActive: "--format json"
    links:
      - label: "commit-check.com"
        url: "https://commit-check.com/"
      - label: "GitHub"
        url: "https://github.com/commit-check/commit-check"
    demo: "commit-check"
    demoLabel: "A terminal: the commit message \"Fix: add streaming support\" is piped to commit-check with --format json. The failing entry of the output's checks array has rule CC001, status fail, and the suggestion to use \"fix: add streaming support\"."
    flip: true
products:
  title: "Infrastructure you own."
  text: "Jenkins agents for Java 8 build hosts, and Mac backups to your own storage."
  also: "Also: [keelapps](https://keelapps.app), admin apps for Jira and Confluence Cloud, on the Atlassian Marketplace."
  items:
    - name: "keelinfra"
      label: "Free · Open source · Support plans"
      text: "Agent8 keeps AIX, Solaris and HP-UX build hosts on a current Jenkins as ordinary agents."
      url: "https://keelinfra.io/jenkins/"
      preview: "agent8"
      style: "card"
      tone: "dark"
    - name: "Keelhaven"
      label: "Free · Open source · macOS 14+"
      text: "Mac backup to storage you own. A menu bar app over restic; files are encrypted before they leave your Mac."
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
