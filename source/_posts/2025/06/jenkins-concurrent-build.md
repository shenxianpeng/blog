---
title: How to Change abortPrevious Value in Jenkins?
tags:
  - Jenkins
  - DevOps
categories:
  - DevOps
author: shenxianpeng
date: 2025-06-04 23:41:00
---

## Background

In our Jenkins pipeline, we use the following configuration to manage resource consumption, especially for builds that typically take more than 30 minutes to complete:

```groovy
disableConcurrentBuilds abortPrevious: true
```

This setting prevents concurrent builds on the same branch or pull request. When a new build is triggered while a previous one is still running, the older build is automatically aborted.

This helps conserve resources and avoids redundant builds when developers push multiple updates shortly after opening a pull request.

## The problem

But the problem is:

> Sometimes, during merges, an ongoing build gets aborted midway or near completion because a new build was triggered for the same branch.
> They requested that if a build is already running, new builds triggered on the same branch should wait in the queue instead of aborting the current build.

<!-- more -->

### Before the changes:

Let's take a picture bellow of the release/x.x.x branch.

![What's the difference?](jenkins-concurrent-build/image.png)

* Job #104 was aborted because a new merge was triggered on the release/x.x.x branch.
* Job #105 was also aborted for the same reason, due to another new merge on the release/x.x.x branch.

### After the changes:

* Job #106 will continue running without being canceled, even if a new merge occurs.
* Job #107 will wait in the queue until Job #106 finishes before starting.

## Initial Thoughts

Initially, I believed that `disableConcurrentBuilds` was a global setting that applied uniformly across all branches and pull requests.

After researching via ChatGPT and Google, I found that selectively applying this setting per branch is not straightforward and requires adding complexity to the existing pipeline.

## The Solution

But there is a simple solution? Yes!

I implemented and tested conditional logic that:

* Retains `abortPrevious: true` for pull request builds,
* Disables it for specific branches such as `devel` and `release`.

Here the code snap about how to implement it.

```groovy
// vars/build.groovy
def call() {
    def isAboutPrevious = true

    if (env.BRANCH_NAME == 'devel' || env.BRANCH_NAME.startsWith('release/')) {
        isAboutPrevious = false // disable abortPrevious for devel and release branches.
    }

    pipeline {
        options {
            disableConcurrentBuilds abortPrevious: isAboutPrevious
        }
        stages{
            // ....
        }
    }
}
```

### The Result

The changes passed testing and have been merged into our shared pipeline library.

Now, for the `devel` and `release` branches in multi-branch pipeline:

* Jenkins **no longer aborts running builds** when new builds are triggered.
* Instead, it **queues subsequent builds**, improving stability and predictability for our QA workflows.

---

Please credit the author and source when reposting this article. Commercial use is not permitted. You're welcome to subscribe to my blog via RSS.
