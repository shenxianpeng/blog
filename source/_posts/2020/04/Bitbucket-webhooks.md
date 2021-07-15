---
title: Bitbucket Webhooks Configuration
tags:
  - Bitbucket
  - Webhook
categories:
  - Jenkins
date: 2020-04-24 17:40:21
author: shenxianpeng
---

## Background

I have set several multi-branch pipeline and it can support Bitbucket Pull Request build. So, when developer create a Pull Request on Bitbucket, Jenkins can auto-trigger PR build. but this jenkins-plugin may not very stable, it had not work two times and I actually don't know why it does that. But I know the use Git webhook is a direct and hard approach could solve this problem. After my test, the answer is yes. it works as expect.

<!-- more -->

## Principle

By setting Webhook events, you can listen for git push, create Pull requests and other events, and automatically trigger Jenkins scan when these events occur, so that Jenkins can get the latest branch (or Pull Request) created (or deleted), and automatically build Jenkins Job.

![Scan Multibranch Pipeline](Bitbucket-webhooks/scan-multibranch.png)

## Setting.

* Webhook name: test-multibranch
* Webhook URL: http://localhost:8080/multibranch-webhook-trigger/invoke?token=test-multibranch
* Test connection: 200(green), it passed.
* Events:
  * Repository: N/A
  * Pull Request: Opened, Merged, Declined, Deleted.
* Active: enable

Here is setting screenshots.

![Bitbucket webhooks setting](Bitbucket-webhooks/webhook-setting.png)

![Jenkins multi-branch pipeline setting](Bitbucket-webhooks/jenkins-setting.png)

At first, I also enable Modified event, but I found when there is new merged commits into our develop branch(this is our PR target branch), the holding Pull Request will be triggered and merge develop branch back to source branch then re-build.

Then I notice the Modified description: A pull request's description, title, or target branch is changed.

This is a nice feature to make sure the source code integrate with target branch and build passed, but  this is too frequent for our product builds, because our product pull request build on some Unix platform need almost 3 hours, if has 5 Pull Requests waiting to review, when new commits into develop branch, these 5 PR need to rebuild again, this takes up all the build machines, resulting in those that need to be built not getting the resources.

After enable above Pull Request event and have these functions.

* when open a new Pull Request on Bitbucket, auto create Pull Request branch and build in Jenkins.
* when merge the Pull Request Bitbucket, auto delete Pull Request branch in Jenkins.
* when decline the Pull Request Bitbucket, auto delete Pull Request branch in Jenkins.
* when delete the Pull Request Bitbucket, auto delete Pull Request branch in Jenkins.

For other specific branches build my Jenkins job support manually build and timing trigger, so this event settings currently good to me.

If there is new settings need to add, I will keep update this article in the future.
