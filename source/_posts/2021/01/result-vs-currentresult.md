---
title: What's the difference between result and currentResult in Jenkins?
tags:
  - Jenkins
categories:
  - Jenkins
date: 2021-01-14 10:48:18
author: shenxianpeng
---

> This is just a note to myself about Jenkins result or currentResult

## Declarative Pipeline

Here is a test code from this ticket [JENKINS-46325](https://issues.jenkins.io/browse/JENKINS-46325)

```bash
pipeline {
    agent any
    stages {
        stage ('Init') {
            steps {
                echo "Init result: ${currentBuild.result}"
                echo "Init currentResult: ${currentBuild.currentResult}"
            }
            post {
                always {
                    echo "Post-Init result: ${currentBuild.result}"
                    echo "Post-Init currentResult: ${currentBuild.currentResult}"
                }
            }
        }
        stage ('Build') {
            steps {
                echo "During Build result: ${currentBuild.result}"
                echo "During Build currentResult: ${currentBuild.currentResult}"
                sh 'exit 1'
            }
            post {
                always {
                    echo "Post-Build result: ${currentBuild.result}"
                    echo "Post-Build currentResult: ${currentBuild.currentResult}"
                }
            }
        }
    }
    post {
        always {
            echo "Pipeline result: ${currentBuild.result}"
            echo "Pipeline currentResult: ${currentBuild.currentResult}"
        }
    }
}
```

Output

```bash
Init result: null
Init currentResult: SUCCESS
Post-Init result: null
Post-Init currentResult: SUCCESS
During Build result: null
During Build currentResult: SUCCESS
[test-pipeline] Running shell script
+ exit 1
Post-Build result: FAILURE
Post-Build currentResult: FAILURE
Pipeline result: FAILURE
Pipeline currentResult: FAILURE
ERROR: script returned exit code 1
Finished: FAILURE
```

## Scripted Pipeline

Here is a test code from [cloudbees support case](https://support.cloudbees.com/hc/en-us/articles/218554077-How-to-set-current-build-result-in-Pipeline-)

Example that forces a failure then prints result:

```bash
node {
    try {
        // do something that fails
        sh "exit 1"
        currentBuild.result = 'SUCCESS'
    } catch (Exception err) {
        currentBuild.result = 'FAILURE'
    }
    echo "RESULT: ${currentBuild.result}"
}
```

Output:

```bash
Started by user anonymous
[Pipeline] Allocate node : Start
Running on master in /tmp/example/workspace/test
[Pipeline] node {
[Pipeline] sh
[test] Running shell script
+ exit 1
[Pipeline] echo
RESULT: FAILURE
[Pipeline] } //node
[Pipeline] Allocate node : End
[Pipeline] End of Pipeline
Finished: FAILURE
```

Example that doesn’t fail then prints result:

```bash
node {
    try {
        // do something that doesn't fail
        echo "Im not going to fail"
        currentBuild.result = 'SUCCESS'
    } catch (Exception err) {
        currentBuild.result = 'FAILURE'
    }
    echo "RESULT: ${currentBuild.result}"
}
```


Output:

```bash
Started by user anonymous
[Pipeline] Allocate node : Start
Running on master in /tmp/example/workspace/test
[Pipeline] node {
[Pipeline] echo
Im not going to fail
[Pipeline] echo
RESULT: SUCCESS
[Pipeline] } //node
[Pipeline] Allocate node : End
[Pipeline] End of Pipeline
Finished: SUCCESS
```