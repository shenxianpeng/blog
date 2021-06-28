---
title: Branch Naming Convention
tags:
  - Naming
  - Branch
categories:
  - DevOps
date: 2021-05-13 23:52:01
author: shenxianpeng
---

## Why need branching naming convention

To better manage the branches on Git(I sued Bitbucket), integration with CI tool, Artifactory, and automation will be more simple and clear.

For example, good unified partition naming can help the team easily find and integrate without special processing. Therefore, you should unify the partition naming rules for all repositories.

## Branches naming convention

### main branch naming 

In general, the main's branch names most like `master` or `main`.

### Development branch naming

I would name my development branch just called `develop`.

### Bugfix and feature branches naming

For Bitbucket, it has default types of branches for use, like `bugfix/`, `feature/`.
So my `bugfix`, `feature` combine with the Jira key together, such as `bugfix/ABC-1234` or `feature/ABC-2345`.

### Hotfix and release branches naming

For hotfix and release, my naming convention always like `release/1.1.0`, `hotfix/1.1.0.HF1`.

### Other branches

Maybe your Jira task ticket you don't want to make it in `bugfix` or `feature`, you can name it to start with `task`, so the branch name is `task/ABC-3456`.

If you have to provide diagnostic build to custom, you can name your branch `diag/ABC-5678`.

## Summary

Anyway, having a unified branch naming convention is very important for implement CI/CD and your whole team.

> Related Reading: [Git Branch Strategy](https://shenxianpeng.github.io/2019/07/git-branching-strategy/) (Chinese)
