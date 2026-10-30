---
title: "Open-source guardrails for software delivery."
heroLead: "The checks that run between a commit and a release, whether a person or an AI agent wrote the code. I have worked on the build, test and release side of software since 2009."
heroButtons:
  - label: "See the projects"
    url: "/portfolio/"
  - label: "Read the blog"
    url: "/posts/"
    style: "outline"
heroAlso:
  label: "From commit to release: "
  stages:
    - stage: "commit"
      links:
        - label: "commit-check"
          url: "https://commit-check.com/"
        - label: "Conventional Branch"
          url: "https://conventionalbranch.org/"
    - stage: "review"
      links:
        - label: "cpp-linter"
          url: "https://cpp-linter.github.io/"
    - stage: "build"
      links:
        - label: "explain-error"
          url: "https://github.com/jenkinsci/explain-error-plugin"
        - label: "Agent8"
          url: "https://keelinfra.io/jenkins/"
    - stage: "release"
      links:
        - label: "release-ledger"
          url: "https://keelinfra.io/cra/"
flagship:
  label: "cpp-linter"
  title: "Lint every pull request."
  text: "clang-format and clang-tidy on each PR, as a GitHub Action, a pre-commit hook and a Python package. Fixes arrive as review suggestions you can commit in one click. The clang tools come from static binaries for every LLVM version, downloaded more than 750,000 times."
  links:
    - label: "Documentation"
      url: "https://cpp-linter.github.io/"
    - label: "GitHub"
      url: "https://github.com/cpp-linter"
  demo: "cpp-linter"
  demoLabel: "Animated demo of cpp-linter on a GitHub pull request: the check fails, cpp-linter posts a clang-format suggestion, the suggestion is committed, and the check passes."
  usersLabel: "Used by projects from"
  users: ["Apache", "Samsung", "Qualcomm", "Bloomberg", "LLNL", "Nextcloud"]
products:
  title: "Infrastructure you own."
  text: "Jenkins agents for build hosts stuck on Java 8, Atlassian apps that run inside your own tenant, and Mac backups to your own storage."
  items:
    - name: "keelinfra"
      label: "Free · Open source · MIT"
      text: "Agent8 keeps build hosts stuck on Java 8, such as AIX, Solaris and HP-UX, connected to a current Jenkins as ordinary agents. One install script, and releases named after the Jenkins version they were tested with."
      url: "https://keelinfra.io/jenkins/"
      demo: "agent8"
      demoLabel: "Animated demo of Agent8: on an AIX build host, install.sh checks the host's Java 8, finds the release for the controller's remoting version, verifies the jars and swaps them in; then the Nodes page of Jenkins 2.580.1 shows the AIX, Solaris, HP-UX and CentOS 6 hosts coming online on Java 8, and a build on the AIX host finishes."
      style: "wide"
      tone: "dark"
    - name: "keelapps"
      label: "Atlassian Marketplace"
      text: "Twelve apps for Jira and Confluence Cloud: permission audits, recurring tasks, scheduled reports, page approvals, and bulk page and attachment tools."
      url: "https://keelapps.app"
      demo: "accesslens"
      demoLabel: "Animated demo of AccessLens for Jira: a reverse lookup shows the three projects the contractors group can reach, then an access review confirms two, flags the project anonymous users can browse for remediation, and is signed off."
      style: "wide"
      tone: "mint"
      flip: true
    - name: "Keelhaven"
      label: "Free · Open source · macOS 14+"
      text: "Mac backup to storage you own. A native menu bar app over restic; files are encrypted before they leave your Mac."
      url: "https://keelhaven.app"
      demo: "keelhaven"
      demoLabel: "Animated demo of the Keelhaven menu bar app running a backup: a plan named Documents is backed up to an external drive, with a progress bar and then a Backup complete notification."
      style: "wide"
  moreLabel: "Learn more"
writing:
  title: "Writing."
  text: "Since 2017, in Chinese and English."
---
