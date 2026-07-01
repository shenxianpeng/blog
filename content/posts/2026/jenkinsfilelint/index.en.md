---
title: Originally Just Wanted to Propose a Doc PR, Ended Up Moving the Project to the Official Jenkins Organization
summary: |
  I wrote a small tool to validate Jenkinsfiles, initially just wanting it to appear in Jenkins' official list of development tools. However, a Jenkins maintainer suggested: why not just transfer the project directly into the jenkinsci organization? This article records the complete process from PR to transfer to an official blog post, including an interesting pitfall encountered along the way.
tags:
  - Jenkins
  - Open Source
  - pre-commit
  - Pipeline
authors:
  - shenxianpeng
date: 2026-06-09
---

Recently, a personal project I maintain, [jenkinsfilelint](https://github.com/jenkinsci/jenkinsfilelint), officially moved from my GitHub account to the [jenkinsci](https://github.com/jenkinsci) official organization.

The entire process took about two weeks, and some of the issues encountered along the way were quite interesting. Today, I'm writing this article to talk about the process.

First, let me introduce the jenkinsfilelint tool.

Simply put, it's a [pre-commit](https://pre-commit.com/) hook that automatically sends your Jenkinsfile to your own Jenkins server for syntax validation when you `git commit`.

```bash
% git commit -m "Update Jenkinsfile"
jenkinsfilelint..........................................................Failed
- hook id: jenkinsfilelint
- exit code: 1

Errors encountered validating Jenkinsfile:
WorkflowScript: 17: Expected a step @ line 17, column 11.
             test
             ^
```

The underlying principle is that it calls Jenkins' built-in Pipeline Linter API:

```
$JENKINS_URL/pipeline-model-converter/validate
```

Similar to manually pasting your Jenkinsfile on the "Pipeline Syntax" page of your Jenkins server to test for syntax issues,

This project enhances that process, allowing you to discover syntax errors before you modify and commit your Jenkinsfile.

The project started development last November, and by May of this year, several versions had been released, and it's also installable from PyPI:

```bash
pip install jenkinsfilelint
```

I found it quite handy, so I thought, why not let more Jenkins users also benefit from this tool?

So, I opened a PR aiming to add it to the Jenkins official development tools list on the [Pipeline Development Tools](https://www.jenkins.io/doc/book/pipeline/development/) page.

On May 30th, I submitted a PR to the jenkins.io repository: [jenkins-infra/jenkins.io#9183](https://github.com/jenkins-infra/jenkins.io/pull/9183), to add jenkinsfilelint to the Development Tools page.

After the PR was submitted, Jenkins community maintainers [dduportal](https://github.com/dduportal) and [krisstern](https://github.com/krisstern) quickly provided feedback.

I understood their concerns: I was the sole maintainer of this project, so how was its quality? Could it be maintained long-term? Was it safe enough to directly recommend it in the official documentation?

But then dduportal proposed a suggestion I hadn't anticipated at all:

> thinking aloud, I am not sure about the exact process but what would you think about moving the project into jenkinsci?

He asked if I would like to move the project directly under the official Jenkins organization.

My first thought upon seeing this reply was: when can we transfer : )

This would give it more exposure than being under my personal account, and I would still be maintaining it, so why not?

Thinking back, a few reasons might have prompted his suggestion:

1. The official Jenkins ecosystem indeed lacked a pre-commit hook to validate Jenkinsfile syntax, and this tool filled that gap.
2. Perhaps I had already accumulated some credibility within the Jenkins community (due to maintaining the Explain Error Plugin).

In any case, I certainly wouldn't refuse this proposal, so I replied:

> I'd be honored to transfer jenkinsfilelint to the jenkinsci organization and continue maintaining it there.

After deciding to contribute this project to the official organization, the next step was figuring out how to transfer it.

I wanted to transfer it directly using GitHub's repository transfer feature, because if the official team were to fork + detach, the release history, issues, and PRs would all be lost, which isn't friendly for projects with existing release history.

However, I discovered I didn't have permission to directly transfer the repository to jenkinsci, even as a member of jenkinsci. It would throw an error directly.

> You don't have the permission to create public repositories on jenkinsci

So, what to do?

Later, someone from the Jenkins community replied, saying I could first transfer the project to the jenkinsci-transfer organization, and then a Jenkins administrator would transfer it from jenkinsci-transfer to jenkinsci.

The process is roughly as follows:

1. A Jenkins administrator first invites me to jenkinsci-transfer.
2. I transfer the repository from my personal account to jenkinsci-transfer.
3. A Jenkins administrator then transfers the repository from jenkinsci-transfer to jenkinsci.

Although this process adds an extra step, it might be the only viable way currently. Its benefits:

- **Solves the permission issue**: I don't need higher permissions in jenkinsci; I just need to be invited into jenkinsci-transfer, which has no repositories.
- **Solves the trust issue**: I couldn't transfer the repository to a stranger — jenkinsci-transfer is an officially recognized Jenkins organization, not someone's alt account. My repository won't be lost or hijacked after transfer.
- **Preserves full history**: Neither transfer will lose any data like commits, releases, issues, or PRs.

After the transfer, I was "kicked out" of jenkinsci-transfer, and the repository remained under jenkinsci.

If you ever need to contribute a project to a large open-source community in the future, this process might serve as a reference.

Alright, the project has moved under jenkinsci, but it hasn't appeared in the official Jenkins documentation yet, so the tool's exposure is still limited.

Thus, my first blog post on jenkins.io came about. [Introducing jenkinsfilelint: Catch Jenkinsfile Errors Before You Commit](https://www.jenkins.io/blog/2026/06/08/jenkinsfilelint-pre-commit/)

The content of this blog post primarily introduces what jenkinsfilelint is, why to use it, and how to use it.

I believe this experience brought me the following thoughts:

1. If you have projects that solve a specific problem, perhaps you can contribute them to or propose them to more influential communities. While not every community is as friendly as Jenkins or willing to accept your project, how will you know if you don't try? You won't know what the future holds if you don't try.

2. When AI emerged, for a long time I felt open source had no future, or I didn't want to do open source anymore. But recently, or rather, after that period passed, I returned to my original passion for open source, and I still enjoy doing open source, enjoying doing impactful things.

I believe open source is a long-term endeavor. You might not make any waves when you start, but results may slowly emerge a year or two later.

---

Finally

jenkinsfilelint is now at [github.com/jenkinsci/jenkinsfilelint](https://github.com/jenkinsci/jenkinsfilelint). The functionality is still the same, but its location has changed — from a personal side project to a member of the official Jenkins ecosystem.

If you're also using Jenkins Pipeline, consider adding it to your `.pre-commit-config.yaml`. You'll catch syntax errors before committing, which is much faster than pushing and waiting for CI to run.

Seasoned developers, see you next time~

---

Please credit the author and source when reprinting articles from this site. Do not use for any commercial purposes. Welcome to follow the official account '沈显鹏'.