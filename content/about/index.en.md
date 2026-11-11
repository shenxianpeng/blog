---
title: "About"
date: 2022-06-13T20:55:37+01:00
draft: false

showDate : false
showDateOnlyInArticle : false
showDateUpdated : false
showHeadingAnchors : false
showPagination : false
showRelatedContent : false
showReadingTime : false
showTableOfContents : false
showTaxonomies : false
showWordCount : false
showSummary : false
sharingLinks : false
showEdit: false
showViews: false
showLikes: false
showAuthor: true
layoutBackgroundHeaderSpace: false
---

DevOps and release engineer, based in Vilnius, Lithuania. I build open-source tools that keep software shipping, even after upstream moves on.

I have worked on the build, test and release side of software since 2009. AI has made writing code cheap. What comes after the code is as expensive as ever: knowing who, or which agent, made a change, building it on the hosts you actually have, showing where a release came from, and patching it for years. From December 2027 the EU Cyber Resilience Act turns part of that into a legal duty: a manufacturer selling software in the EU has to declare a support period and ship security updates until it ends. The projects below are for that stretch.

## From commit to release, and long after

{{< pipeline >}}

- **commit.** [commit-check](https://github.com/commit-check/commit-check): one policy for commit messages, branch names and AI attribution, in CI or as a pre-commit hook. [Conventional Branch](https://conventionalbranch.org): a branch naming specification.
- **review.** [cpp-linter](https://github.com/cpp-linter): clang-format and clang-tidy on every pull request. More than 1,000 repositories on GitHub depend on it, including projects from AWS, Apache, Samsung, Qualcomm and Bloomberg.
- **build.** [explain-error-plugin](https://github.com/jenkinsci/explain-error-plugin) and [jenkinsfilelint](https://github.com/jenkinsci/jenkinsfilelint), in the jenkinsci organization: AI diagnosis of build failures, and Jenkinsfile validation without a Jenkins server. [Agent8](https://github.com/keelinfra/agent8) keeps Java 8 build hosts such as AIX, Solaris and HP-UX on a current Jenkins.
- **release.** [release-ledger](https://github.com/keelinfra/release-ledger), my newest project: runs when you publish a release, attaches an SBOM and signed build provenance, and watches every supported version for actively exploited vulnerabilities, which the EU Cyber Resilience Act requires you to report within 24 hours. The [static binaries](https://github.com/cpp-linter/clang-tools-static-binaries) of clang-format and clang-tidy that I publish for each LLVM version have been downloaded more than 750,000 times.
- **support.** [Extended Security for Jenkins 2.541.x](https://github.com/keelinfra/jenkins-extended-security): Jenkins 2.541.3, the last LTS that runs on Java 17, with the core security fixes released after it. [MkDocs NG](https://mkdocs-ng.org): MkDocs 1.x, maintained, so existing sites and their plugins keep building. 1.x is supported until the end of 2028.

## Products

Both are for the team that keeps a company's development tools running.

- [keelinfra](https://keelinfra.io): for CI that cannot move to what upstream supports yet. Agent8, Extended Security for Jenkins and the rest are free and open source, tested in public, with paid support if you want someone to stand behind them.
- [keelapps](https://keelapps.app): admin tools for Jira and Confluence Cloud.

On the side I also build [Keelhaven](https://keelhaven.app), a free Mac app that backs up to storage you own.

More on each of them on the [Projects](/portfolio/) page.

## Community

Member of the Jenkins GitHub organization. Top 3 in Lithuania for public contributions on [committers.top](https://committers.top/lithuania_public). EuroPython 2025 proposal reviewer. Anthropic Open Source Developer Program, 2026. Writing here since 2017; the Chinese posts also go out on WeChat (沈显鹏).

## Support

This blog has never carried ads. If the writing or the tools helped, you can sponsor me on [GitHub Sponsors](https://github.com/sponsors/shenxianpeng), support the work via [Thanks.dev](https://thanks.dev/u/gh/shenxianpeng), or [buy me a coffee](https://buymeacoffee.com/shenxianpeng).

## Contact

A problem with one of the tools, or just want to talk: [xianpeng.shen@gmail.com](mailto:xianpeng.shen@gmail.com), or find me on [GitHub](https://github.com/shenxianpeng) and [X](https://x.com/xianpengshen). The rest of my career is on the [résumé](/resume/).
