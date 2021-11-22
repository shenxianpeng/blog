---
title: Annual work summary from 2019.03 - 2020.07
tags:
  - Summary
  - Work
categories:
  - MyNotes
date: 2020-07-29 13:52:04
author: shenxianpeng
---

Summarize what did I do from 2019.03 to 2020.07 when I became a Build Release/DevOps engineer.

## Build automation

* Support all server windows platform build manual to auto.
* Support clients build from manual to auto.
* Switch Linux/Unix build from Bamboo to Jenkins.
* Support all platforms branches/Pull Request build.
* Provide auto-build as self-service for a developer, no need to involve build engineer, they could build themselves.

## Integration

* Integration with Jenkins

  * Self-service installation.
  * Blackduck, Polaris integration.
  * Git stats, analyze Bitbucket data with Elastic stack.
  * Monitor legacy build machines status.
  * Product escrow, sync xdemo, provide NFS and SYNC mvopensrc, update Bitbucket Jenkins build status, etc.

* Integration with JFrog Ariifactory

  * Establish deploy strategy and directory structure organization.
  * Handle artifacts(build, etc) with different maturity.

## Infrastructure management

* Manage Jenkins for setting, update and backup.
* Ariifactory artifacts cleanup, retention, backup.
* Git branches/hooks management.
* VMs tracking, management build machines.
