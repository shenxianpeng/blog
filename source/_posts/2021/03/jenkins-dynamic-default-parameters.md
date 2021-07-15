---
title: Different branches have different default parameters in Jenkins
tags:
  - Jenkins
categories:
  - Jenkins
date: 2021-03-24 10:50:53
author: shenxianpeng
---

## Problem

When you use Jenkins multibranch pipeline, you may want to have different default parameters settings for defferent branches build.

For example:

For develop/hotfix/release branches, except regular build, you also want to do some code analyzes, like code scanning, etc.
For other branches, like feature/bugfix or Pull Request that you just want to do a regular build.

So you need to have dynamic parameter settings for your multibranch pipeline job.

## Solution

So for these cases, how to deal with Jenkins multibranch pipeline. Here are some code snippet that is works well in my Jenkinsfile.

```bash
	def polarisValue = false
	def blackduckValue = false

	if (env.BRANCH_NAME.startsWith("develop") || env.BRANCH_NAME.startsWith("hotfix")
  || env.BRANCH_NAME.startsWith("release")) {
		polarisValue = true
		blackduckValue = true
	}

  pipeline {
    agent { node { label 'gradle' } }

    parameters {
        booleanParam defaultValue: polarisValue, name: 'Polaris',  description: 'Uncheck to disable Polaris'
        booleanParam defaultValue: blackduckValue, name: 'BlackDuck', description: 'Uncheck to disable BD scan'
    }

    stages {
      // ...
    }
  }

```
