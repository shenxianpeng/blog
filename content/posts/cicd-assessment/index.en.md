---
title: How to Evaluate CI/CD Maturity within an Organization
summary: This article introduces how to use the Jenkins generic-webhook-trigger plugin to obtain real-time event information from Bitbucket repositories, such as Pull Request IDs.
tags:
  - CI
  - CD
  - Badge
date: 2021-12-07
author: shenxianpeng
---

## Problem

Within an organization, different teams may use different dimensions to evaluate the maturity of their CI/CD pipelines. This makes it difficult to measure the CI/CD performance of each team.

How can we quickly assess which projects follow best practices? How can we more easily build high-quality and secure software?  The organization needs to establish best practices, collaboratively discussed by team members, to help teams establish clear directions for improvement.


## How to Evaluate

Here, I refer to the open-source project [CII Best Practices Badge program](https://github.com/coreinfrastructure/best-practices-badge), an initiative of the Linux Foundation (LF). It provides a set of best practices for Free/Libre/Open Source Software (FLOSS) projects. Projects that adhere to these best practice standards can self-certify to obtain a Core Infrastructure Initiative (CII) badge.  This is free of charge; your project can use a web application (BadgeApp) to demonstrate and detail its compliance with these standards.

These best practice standards can be used to:

* Encourage projects to follow best practices.
* Help new projects identify best practices to follow.
* Help users understand which projects follow best practices (allowing users to preferentially select such projects).

Best practices include five standards: Basic, Change Control, Reporting, Quality, Security, and Analysis.

![cii](cii.png)

For more detailed breakdown of the standards, please refer to the [CII Chinese documentation](https://hardenedlinux.github.io/2016/08/04/best-practices-criteria-for-floss-part1.html) or the [CII English documentation](https://github.com/coreinfrastructure/best-practices-badge/blob/main/doc/criteria.md).

Many well-known projects, such as [Kubernetes](https://bestpractices.coreinfrastructure.org/en/projects/569) and [Node.js](https://bestpractices.coreinfrastructure.org/en/projects/29), are using this best practices badge program.

![badge-owners](badge-owners.png)

If your project is on GitHub or you can follow the above badge program, you can use it to evaluate your project's best practices and display the badge results on your project's README.

![badge-result](badge-result.png)

## Customizing Best Practice Standards

If the above project doesn't meet your evaluation requirements, based on my experience, the following "best practice standards" and corresponding maturity badges are provided for reference.

### Calculation Rules

1. Each best practice standard has a score; generally, common standards are 10 points, and important standards are 20 points.
2. Best practice standards with 🔰 indicate "must-have".
3. Best practice standards with 👍 indicate "should-have".
4. The range in which the sum of the best practice standard scores for each project falls determines the corresponding badge.

### Badge Score Mapping Table

| Badge  | Score | Description |
|----  | --  | -- |
| 🚩WIP | < 100 | Less than 100 points receives a 🚩Work In Progress badge |
| ✔️PASSING | = 100 | Equal to 100 points receives a ✔️PASSING badge |
| 🥈SILVER | > 100 && <= 150 | Greater than 100, less than or equal to 150 points receives a 🥈Silver badge |
| 🥇GOLD | > 150 | Greater than or equal to 150 points receives a 🥇Gold badge |

Note: This score range is adjustable.

### Best Practice Standards and Scores

| Category      | Best Practice Standard        | Score | Description |
|----      | ----------------- | -----| ----------- |
|**Basic**  | 🔰**Build any branch** | **20** | Jenkins: Supports building any branch |
|          | 🔰**Build any PR**  | **20** | Jenkins: Supports building any Pull Request before merging |
|          | 🔰Upload artifacts        | 10 | Jenkins: Upload build artifacts to the artifact repository |
|          | 👍Containerized build      | 10  | Recommend using containerization technology to implement the Pipeline |
| **Quality** | 🔰**Automated testing**   | **20** | Jenkins: Supports triggering smoke/unit/regression tests |
|          | 👍Performance testing        | 10 | Jenkins: Supports triggering performance tests |
|          | 👍Code coverage collection  | 10 | Jenkins: Supports obtaining code coverage |
| **Security** | 🔰Vulnerability scanning        | 10  |  Jenkins: Supports triggering vulnerability scans |
|          | 🔰License scanning    | 10 | Jenkins: Supports triggering license scans |
| **Analysis**  | 👍Code Lint     | 10  | Jenkins: Supports code format checking for PRs |
|          | 👍Static code analysis    | 10  | Jenkins: Supports static code analysis for PRs |
|          | 👍Dynamic code analysis    | 10  | Jenkins: Supports dynamic code analysis for PRs |
| **Reporting** | 🔰Email or Slack notifications | 10 | Supports notifications via Email or Slack |

Note: Jenkins is used as an example.

## Final Results

| No | Repository Name | Implemented Best Practice Standards | Badge |
|---| --------------- | --------- | ---- |
| 1 | project-a       | 🔰**Build any branch**</br>🔰**Build any PR**</br>🔰Upload artifacts</br>🔰**Automated testing**</br>🔰Email or Slack notifications | 🚩WIP |
| 2 | project-b       | 🔰**Build any branch**</br>🔰**Build any PR**</br>🔰Upload artifacts</br>🔰**Automated testing**</br>🔰Vulnerability scanning</br>🔰License scanning</br>🔰Email or Slack notifications | ✔️PASSING |
| 3 | project-c       | 🔰**Build any branch**</br>🔰**Build any PR**</br>🔰Upload artifacts</br>👍Containerized build</br>🔰**Automated testing**</br>🔰Vulnerability scanning</br>🔰License scanning</br>🔰Email or Slack notifications | 🥈SILVER |
| 4 | project-d       | 🔰**Build any branch**</br>🔰**Build any PR**</br>🔰Upload artifacts</br>👍Containerized build</br>🔰**Automated testing**</br>👍Performance testing</br>👍Code coverage collection</br>🔰Vulnerability scanning</br>🔰License scanning</br>👍Code Lint</br>👍Static code analysis</br>👍Dynamic code analysis</br>🔰Email or Slack notifications | 🥇GOLD |

## Q&A

Q: Why use badges instead of scores?\
A: Using badges better helps teams strive for goals rather than scores.

Q: What other benefits are there to establishing best practice standards?\
A: Easier technical sharing among teams, easier building of high-quality and secure software, and maintaining consistent high standards across teams.