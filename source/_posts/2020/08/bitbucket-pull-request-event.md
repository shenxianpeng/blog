---
title: bitbucket-pull-request-event
tags:
  - Bitbucket
  - Jenkins
  - webhook
  - generic
categories:
  - DevOps
date: 2020-08-07 16:53:03
author: shenxianpeng
---

This post about how to trigger Jenkins pipeline Job (not multi-branch pipeline job) when a Pull Request created on Bitbucket.

there are these key ponits I would like to mentions

1. Create a Jenkins job, exmaple called `tigger-demo`

2. Install generic-webhook-trigger-plugin on Jenkins

3. Configue the Jenkins job and enable Generic Webhook Trigger 

    * Post content parameters 
      * set Variable is pr_id, Expression is $.pullRequest.id, selected `JSONPath`
        > Reference generic-webhook-trigger-plugin[bitbucket-server-pull-request.feature](https://github.com/jenkinsci/generic-webhook-trigger-plugin/blob/master/src/test/resources/org/jenkinsci/plugins/gwt/bdd/bitbucket-server/bitbucket-server-pull-request.feature)
    
    * Token
      * test-demo

4. Setting Bitbucket hook. create **Webhooks** or **Post Wehooks**

    * URL: http://JENKINS_URL/generic-webhook-trigger//invoke?token=test-demo

    * choose events you want in Bitbucket

5. then create Jenkins pipeline just used `${pr_id}` you will get the pull request id just created and your Jenkins job will be triggered.


