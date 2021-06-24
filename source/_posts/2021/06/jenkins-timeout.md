---
title: How to make Jenkins job fail after timeout? (Resolved)
tags:
  - timeout
  - Jenkins
categories:
  - Jenkins
date: 2021-06-24 11:00:45
author: shenxianpeng
---

When using Jenkins timeout like below, it can't make the Jenkins build failed.

```java
pipeline {
    agent none
    stages {
        stage('Hello') {
            steps {
                timeout(time: 1, unit: 'SECONDS') {
                    echo "timeout step"
                    sleep 2
                }
            }
        }
    }
}
```
So, If want to make the Job failed after it's timeout, you can use `try` .. `catch` and `error` to make your Jenkins job failed. like below.

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
                            sleep 1
                        }
                    } catch(err) {
                        // timeout reached or input false
                        println err
                        echo 'Time out reached or user aborted'
                        error 'build timeout failed'
                    }
                }
            }
        }
    }
}
```

Here is the output log

```
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
00:00:01.558  Sleeping for 1 sec
00:00:02.535  Cancelling nested steps due to timeout
00:00:02.546  [Pipeline] }
00:00:02.610  [Pipeline] // timeout
00:00:02.619  [Pipeline] echo
00:00:02.621  org.jenkinsci.plugins.workflow.steps.FlowInterruptedException
00:00:02.625  [Pipeline] echo
00:00:02.627  Time out reached or user aborted
00:00:02.630  [Pipeline] error
00:00:02.638  [Pipeline] }
00:00:02.656  [Pipeline] // script
00:00:02.668  [Pipeline] }
00:00:02.681  [Pipeline] // stage
00:00:02.696  [Pipeline] End of Pipeline
00:00:02.709  ERROR: build timeout failed
00:00:02.710  Finished: FAILURE
```
