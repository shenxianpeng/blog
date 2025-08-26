---
title: A Look at the Services and Tools Used by Top Open Source Organizations
summary: This article introduces the services and tools used by the renowned Apache Software Foundation. This might help broaden your horizons and provide references when choosing tools.
tags:
  - Apache
  - Infrastructure
author: shenxianpeng
date: 2024-01-21
---

This article introduces the services and tools used by the renowned Apache Software Foundation. This might help broaden your horizons and provide references when choosing tools. If you are a DevOps, SRE, or Infra engineer, the content of this article will help you better showcase the services your team provides and gain insight into how Apache Infra organizes and manages its operations.

## Who is Apache?

If you are unfamiliar with Apache, here is a brief introduction.

Apache is an abbreviation for the Apache Software Foundation (ASF). The ASF is a non-profit organization dedicated to supporting and developing open-source software projects. The Apache Software Foundation provides legal, financial, and infrastructure support to help developers collaborate in creating and maintaining open-source software. One of the most well-known projects of the Apache Software Foundation is the Apache HTTP Server, also known as the Apache Web Server. In addition, the ASF also hosts many other popular open-source projects, such as ECharts, Superset, Dubbo, Spark, Kafka, and so on.

## Services and Tools

The Apache Infra team maintains various tools for PMCs (Project Management Committees), project committers, and the Apache Board of Directors. Some of these tools are only available to individuals with specific responsibilities or roles. Other tools, such as monitoring tools that display the status of various parts of the Apache infrastructure, are open to everyone.

* [Services for Top-Level Projects (TLPs)](#services-for-top-level-projects-tlps)
    * [Website](#website)
    * [Email](#email)
    * [ASF Self-Service Platform](#asf-self-service-platform)
    * [ASF Account Management](#asf-account-management)
    * [LDAP-enabled Services](#ldap-enabled-services)
* [Incubation Projects (Podlings) Services](#incubation-projects-podlings-services)
* [ASF Project Tools](#asf-project-tools)
    * [Version Control](#version-control)
    * [Issue Tracking and Feature Requests](#issue-tracking-and-feature-requests)
    * [Integrating your Repository with Jira Tickets](#integrating-your-repository-with-jira-tickets)
    * [Source Repository Publisher/Subscriber Service](#source-repository-publisher-subscriber-service)
    * [Build Services](#build-services)
    * [Product Naming](#product-naming)
    * [Code Signing](#code-signing)
    * [Code Quality](#code-quality)
    * [Code Distribution](#code-distribution)
    * [Virtual Machines](#virtual-machines)
    * [Online Voting](#online-voting)
* [Other Tools](#other-tools)
    * [DNS](#dns)
    * [URL Shortener](#url-shortener)
    * [Share Code Snippets](#share-code-snippets)
    * [Machine List](#machine-list)
    * [Whimsy](#whimsy)

## Services for Top-Level Projects (TLPs)

### Website

* www.apache.org This is the main Apache website.
* [Apache Project Website Checker](https://whimsy.apache.org/site/) regularly checks all websites for Top-Level Projects (TLPs) and reports whether they comply with Apache's TLP website policies.

Only a few interesting links are listed here, such as the project website checker, which checks whether top-level projects have the correct links for License, Donate, Sponsors, Privacy, etc.

### Email

* All new email list requests should be submitted through the [self-service system](https://selfserve.apache.org/mailinglist-new.html).
* Email Server - QMail/QSMTPD



### ASF Self-Service Platform

* One of Infra's goals is to empower ASF members, PMCs, and committers to accomplish most of the tasks they need to do without having to reach out to Infra. For example, the [self-service platform](https://selfserve.apache.org/) provides many convenient tools that people with an Apache email address (basically project committers, PMC members, and ASF members) can use to:

    * Create Jira or Confluence projects, Git repositories, or email lists (PMC chairs and Infra members).
    * Edit your ASF identity or update your ASF password. To update your password, you will need access to the email account associated with your Apache account. Reset keys are only valid for 15 minutes, so be sure to use them immediately after receiving them.
    * Sync Git repositories.
    * Generate one-time passwords for the OTP or S/Key one-time password system using an OTP calculator (generally for PMC members).
    * Archive and set Confluence Wiki spaces to read-only.

Individuals who are not part of the ASF community but wish to submit Jira tickets regarding ASF project products can use the platform to [apply for a Jira account](https://infra.apache.org/jira-guidelines.html#who).

### ASF Account Management

If you want to update your account details or have lost account access, [ASF Account Management](https://infra.apache.org/account-mgmt.html) can provide guidance.

### LDAP-enabled Services

Infra supports many [ASF services enabled by LDAP](https://cwiki.apache.org/confluence/display/INFRA/LDAP+enabled+services+at+the+ASF). You can use your LDAP credentials to log in to these services.

### Incubation Projects Services

Infra supports incubation projects.

* [Infra Incubator Introduction](https://infra.apache.org/infra-incubator.html), showing the steps to establish an incubation project.
* [Project or Product Naming Guidelines](https://apache.org/foundation/marks/pmcs.html#naming)

### ASF Project Tools

Infra supports a range of tools and services to assist project development and support their applications and communities, including

* Each project can use a dedicated space on the [Confluence Wiki](https://infra.apache.org/cwiki.html).
    * How to manage user permissions for project Wiki spaces.
    * How to grant users permission to edit Wiki spaces.
* Reporter provides activity statistics and other information about the project and provides editing tools to help you write and submit your project's quarterly board report.
* You can create and run a project blog.
* You can establish a Slack channel for real-time team discussions. Once you establish a Slack channel, Infra can set up Slack-Jira bridging so you can receive notifications of new or updated Jira tickets in the channel.
* Teams can use ASFBot to conduct and record meetings via Internet Relay Chat (IRC). However, you must follow the Apache voting process and formally vote on decisions in the appropriate project email list.
* [Localization tools](https://infra.apache.org/localization.html).
* Apache [Release Audit Tool (RAT)](https://creadur.apache.org/rat/) helps you confirm that the proposed product release meets all ASF requirements.
* ASF [OAuth](https://oauth.apache.org/api.html) system provides a central point for services that want to use authentication without compromising the security of storing sensitive user data. Many Apache services use it to verify that the user requesting access is a committer in the project and has legitimate access to the relevant systems. Learn more about Apache OAuth.

### Version Control

Apache provides and Infra maintains code repositories that Apache projects can use to ensure the security of project code, accessibility for team members, and version control.

* Information on using 【Git】(https://infra.apache.org/git-primer.html)
    * [Read-only Git mirrors of SVN repositories](https://infra.apache.org/git.html)
    * [Writable Git repositories](https://infra.apache.org/project-repo-policy.html)
    * [Apache and GitHub](https://infra.apache.org/apache-github.html)
    * [Access roles for GitHub repositories](https://infra.apache.org/github-roles.html)

* Information on using [Subversion](https://infra.apache.org/svn-basics.html)
    * [Subversion (SVN) repositories](https://svn.apache.org/repos/asf/)
    * [ViewVC (browser interface for the main Subversion repository)](https://svn.apache.org/viewvc/)

### Issue Tracking and Feature Requests

The ASF supports the following options for tracking issues and feature requests:
    * [Jira](https://issues.apache.org/jira)
    * [GitHub issue tracker](https://guides.github.com/features/issues/)

Due to historical reasons, some projects use [Bugzilla](https://bz.apache.org/bugzilla/). We will continue to support Bugzilla but will not set it up for projects that are not already using it.

[Apache Allura](https://allura.apache.org/) is another issue tracking option. If you feel it meets your project needs, please consult the Allura project directly via the users@allura.apache.org mailing list.

See issues.apache.org to see which issue trackers are used by each project.

Here's how to [request a bug and issue tracker for your project](https://infra.apache.org/request-bug-tracker.html).

Here are [guidelines for writing good bug reports](https://infra.apache.org/bug-writing-guide.html).

### Integrating your Repository with Jira Tickets

Infra can [activate Subversion and Git integration with Jira tickets for your project](https://infra.apache.org/svngit2jira.html).

### Source Repository Publisher/Subscriber Service

* SvnPubSub
* [PyPubSub](https://infra.apache.org/pypubsub.html)

### Build Services

Apache supports and emulates Continuous Integration and Continuous Delivery (or CI/CD). The ASF Build and Supported Services page provides information and links to CI services provided and/or supported by the ASF.

Other tools to consider:

* [Travis CI](https://travis-ci.org/)
* [Appveyor](https://www.appveyor.com/)

### Product Naming

See the [Product Naming Guidelines](https://apache.org/foundation/marks/pmcs.html#naming)

### Code Signing

* Digital Certificate Source Repository Publisher/Subscriber Service

    * Request [access to the Digicert code signing service](https://infra.apache.org/digicert-access.html)
    * [Using Digicert](https://infra.apache.org/digicert-use.html)
* [Distribution via the Apple App Store](https://cwiki.apache.org/confluence/display/INFRA/Distribution+via+the+Apple+App+Store)
* More information on [Code Signing and Publishing](https://cwiki.apache.org/confluence/display/INFRA/Code+Signing+and+Publishing)

### Code Quality

[SonarCloud](https://sonarcloud.io/) is a code quality and security tool that is free to use for open-source projects. It allows for continuous code quality checks, so your project can perform automated reviews by statically analyzing your code to detect bugs, code smells, and security vulnerabilities in over 20 programming languages.

You can [check the status of many Apache project software sources](https://sonarcloud.io/organizations/apache/projects).

For guidance on using SonarCloud in ASF projects, click [here](https://cwiki.apache.org/confluence/display/INFRA/SonarCloud+for+ASF+projects).

### Code Distribution

Use the ASF [Nexus Repository Manager](https://repository.apache.org/#welcome) to browse and review code releases for ASF projects.

#### Releases

* [Current Releases](https://www.apache.org/dyn/closer.lua)
* [Historical Release Archives](https://archive.apache.org/)
* [Rsync distribution mirrors](https://infra.apache.org/how-to-mirror.html)
* [Nexus](https://repository.apache.org/)

### Virtual Machines

Infra can provide Ubuntu virtual machines for projects.

* [Virtual Machine Policy](https://infra.apache.org/vm-policy.html)
* [Process for requesting VMs](https://infra.apache.org/vm-for-project.html)

### Using nightlies.a.o

nightlies.a.o, as the name suggests, is a "short-term" storage solution. See the [nightlies usage policy](https://infra.apache.org/nightlies.html).

### Online Voting

Projects can use an instance of the [Apache STeVe](https://steve.apache.org/) voting system (offline when not in use). The tool name refers to the Single Transferable Vote system as one of the voting options. Open a Jira ticket with Infra to prepare STeVe for use in your project.

## Other Tools

### DNS

Infra manages the ASF DNS registered with Namecheap.

### URL Shortener

[URL Shortener](https://s.apache.org/)

### Share Code Snippets

[Paste](https://paste.apache.org/) is a service where ASF members can post code snippets or similar file excerpts to illustrate code issues or for reuse, typically sharing with other project members. You can post content as plain text or in various encodings and formats.

### Machine List

[Host Keys and Fingerprints](https://infra.apache.org/machines.html)

### Whimsy

[Apache Whimsy](https://whimsy.apache.org/) describes itself as "providing organizational information about the ASF and our projects in an easy-to-use manner, and helping the ASF automate business processes to make it easier for our many volunteers to handle the behind-the-scenes work."

Whimsy has many useful tools for Project Management Committees and individual committers, such as a committer search.

## Summary

These are some of the services and tools used by the Apache Software Foundation. The overall feeling is that it's very comprehensive, and each link corresponds to a complete document, which is the most important aspect of this open-source collaboration approach: reading the documentation thoroughly.  This organizational approach is also very clear for those who want to participate, and is worth learning from.

* We see some common services and tools, such as Jira, Confluence, Slack, Git, GitHub, SonarCloud, Digicert, Nexus.
* We also see less common tools, such as the choice of CI tools being Travis CI and Appveyor.
* There are also some interesting tools, such as a URL shortener, code snippet sharing, and Whimsy, which appear to be deployed internally based on their URLs.
* Due to historical reasons, some projects are still using tools like Bugzilla and SVN.

The services and tools used by Apache, borrowing from the risk assessment levels in finance, are considered **conservative**, rather than blindly pursuing what is "new," "open-source," and "free."

> For readability, this article has been modified and abridged. The original article is located [here](https://infra.apache.org/services.html).

---

Please indicate the author and source when reprinting this article, and do not use it for any commercial purposes. Welcome to follow the WeChat public account "DevOps攻城狮".