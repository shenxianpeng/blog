---
title: What Optimizations I Made During the Jenkins Upgrade
summary: This article discusses the optimizations made during the Jenkins upgrade, including using Docker Compose for deployment, refactoring the Jenkins Shared Library, introducing Windows Docker Containers, and more to enhance the efficiency and security of the CI/CD process.
tags:
  - Jenkins
  - DevOps
date: 2024-10-25
authors:
  - shenxianpeng
---

## Background

Recently, I’ve been working on migrating and upgrading Jenkins. The main motivation is the vulnerability [CVE-2024-23897](https://nvd.nist.gov/vuln/detail/CVE-2024-23897).

> Jenkins 2.441 and earlier, LTS 2.426.2 and earlier does not disable a feature of its CLI command parser that replaces an '@' character followed by a file path in an argument with the file's contents, allowing unauthenticated attackers to read arbitrary files on the Jenkins controller file system.

To address this, Jenkins needs to be upgraded to at least version 2.442 or LTS 2.426.3 or above. This was also an opportunity to rework parts of the setup that weren’t initially optimized.


## Pre-Upgrade Jenkins

Before the upgrade, we were using Jenkins 2.346.3, the last version supporting Java 8. Because older operating systems don’t support Java 17, this blocked us from upgrading Jenkins.

That said, our initial setup was already well-structured:

* We followed the Infrastructure as Code principle, deploying Jenkins through Docker Compose.
* We adhered to the Configuration as Code principle, managing all Jenkins Pipelines with a Jenkins Shared Library.
* We used Jenkins Multibranch Pipeline to build and test projects.

However, there were some limitations, such as:

* The Jenkins server didn’t have a fixed domain name like jenkinsci.organization.com, but instead had a format like `http://234.345.999:8080`. Whenever the IP or hostname changed, Webhook configurations for this Jenkins instance had to be updated manually in the Git repository.
* We hadn’t adopted Docker Cloud. While many tasks used Docker for builds, we weren’t utilizing Docker JNLP agents to create dynamic agents for builds that would automatically be destroyed upon completion.
* The naming and code structure of the Jenkins Shared Library needed refactoring, as it was initially created for a single team, which limited repository naming.
* We hadn’t yet used Windows Docker Containers.
* Some Jenkins plugins were likely outdated or unused but still present.
* Jenkins and its plugins weren’t regularly updated due to the Jenkins Agent version restrictions.

## Post-Upgrade Jenkins

Building on prior best practices, we made the following improvements:

* Continued following the Infrastructure as Code principle, and using Nginx as a reverse proxy, we deployed Jenkins with Docker Compose to ensure a stable domain name.
* Continued to follow the Configuration as Code principle.
* Continued using Jenkins Multibranch Pipeline for building and testing projects.
* Where possible, implemented Docker Cloud for builds.
* Renamed the Jenkins Shared Library to `pipeline-library` (aligning with Jenkins' naming conventions) and refactored many Jenkinsfiles and Groovy files.
* Introduced Windows Docker Containers to build Windows components.
* Utilized the Jenkins Configuration as Code plugin and scheduled regular configuration backups.
* Installed only necessary Jenkins plugins and exported the current plugin list using the `plugin` command.
* Attempted to automate plugin backups before upgrading, enabling quick rollback if the upgrade fails.

## Summary

I hope these efforts enable Infrastructure maintenance and Pipeline development to be managed through GitOps.

Through continuous exploration, experimentation, and application of best practices, I aim to establish CI/CD as a healthy, sustainable, self-improving DevOps system.
