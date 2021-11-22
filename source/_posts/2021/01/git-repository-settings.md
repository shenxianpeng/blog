---
title: These settings in Bitbucket/GitHub recommends enable
tags:
  - Bitbucket
  - Git
categories:
  - DevOps
date: 2021-01-12 17:35:19
author: shenxianpeng
---

As I have management our team's git repositories for more than two years, and as my daily work using Bitbucket, so I'll take it as an example.

Here are some settings recommend you to enable.

1. Set Reject Force Push
2. Set Branch Prevent deletion
3. Set tags for each hotfix/GA releases
4. Merge Check -> Minimum approvals (1)
5. Yet Another Commit Checker

## Reject Force Push

This is the first setting I highly recommend you/your team to open it. if not, when someone using the `git push -f` command to the git repository, you may lost commits if his local code is old then remote repository.

you have to recover the lost commits manually, I have heard 3 times around me. so enable the hook: Reject Force Push ASAP!

## Set Branch Prevent deletion

If some branch is very important, you don't want to lost it, set Branch Prevent deletion ASAP!

## Set tags for each hotfix/GA releases

For each hotfix/GA release, highly recommend create tags after release.

## Merge Check

Pull Request is a very good workflow process for each team. in case of commits were merged directly without review, we enable Minimum approvals (1).

So, every branch wants to be merged to the main branch MUST add a reviewer (not allow yourself) and the review must click the Approve button otherwise the merge button is disabled.

## Yet Another Commit Checker

This is a very powerful feature. it helps to standardize commit messages and create a branch.

More details about this tool you can refer to [this introduction](https://mohamicorp.atlassian.net/wiki/spaces/DOC/pages/1442119700/Yet+Another+Commit+Checker+YACC+for+Bitbucket)

I have a Chinese article to describe how to use Yet Another Commit Checker implement. if you interest it, you can see the post [here](https://shenxianpeng.github.io/2020/09/commit-messages-specification/)
