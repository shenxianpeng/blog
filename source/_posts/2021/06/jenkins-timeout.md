---
title: How to make Jenkins job fail after timeout? (Resolved)
tags:
  - Jenkins
categories:
  - Jenkins
date: 2021-06-24 11:00:45
author: shenxianpeng
---

I've run into some situations when the build fails, perhaps because some processes don't finish, and even setting a timeout doesn't make the Jenkins job fail.

So, to fix this problem, I used `try` .. `catch` and `error` to make my Jenkins job failed, hopes this also helps you.

<!-- more -->
Please see the following example:

```java
pipeline {
    agent none
    stages {
        stage('Hello') {
            steps {
                script {
                    try {
                        timeout(time: 1, unit: 'SECONDS') {
                            echo "timeout step"
                            sleep 2
                        }
                    } catch(err) {
                        // timeout reached
                        println err
                        echo 'Time out reached.'
                        error 'build timeout failed'
                    }
                }
            }
        }
    }
}
```

Here is the output log

```log
00:00:01.326  [Pipeline] Start of Pipeline
00:00:01.475  [Pipeline] stage
00:00:01.478  [Pipeline] { (Hello)
00:00:01.516  [Pipeline] script
00:00:01.521  [Pipeline] {
00:00:01.534  [Pipeline] timeout
00:00:01.534  Timeout set to expire in 1 sec
00:00:01.537  [Pipeline] {
00:00:01.547  [Pipeline] echo
00:00:01.548  timeout step
00:00:01.555  [Pipeline] sleep
00:00:01.558  Sleeping for 2 sec
00:00:02.535  Cancelling nested steps due to timeout
00:00:02.546  [Pipeline] }
00:00:02.610  [Pipeline] // timeout
00:00:02.619  [Pipeline] echo
00:00:02.621  org.jenkinsci.plugins.workflow.steps.FlowInterruptedException
00:00:02.625  [Pipeline] echo
00:00:02.627  Time out reached.
00:00:02.630  [Pipeline] error
00:00:02.638  [Pipeline] }
00:00:02.656  [Pipeline] // script
00:00:02.668  [Pipeline] }
00:00:02.681  [Pipeline] // stage
00:00:02.696  [Pipeline] End of Pipeline
00:00:02.709  ERROR: build timeout failed
00:00:02.710  Finished: FAILURE
```
