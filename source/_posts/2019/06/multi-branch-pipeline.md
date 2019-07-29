---
title: Multibranch pipeline
date: 2019-06-25 22:15:42
tags:
- Jenkins
- pipeline
- multi-branch
categories: 
- Jenkins
---

## Problems

Like database product, it runs on multi-platform, but for software enginner they may only works on one platform, how they could identify their code works on all platform? manually build the various platforms? NO!

## Solution

Most people would know we can use Jenkins pipeline, they may create multi Jenkins job for different stuation.

How to do it in an elegant way, I would want to share how to use multibranch pipeline to achieve.

1. When create a pull request, auto parallel start simple build.
2. Reviewers can decide whether to merge base on build results.
3. After code merged, auto start full build.

## Benefits

What are the benefits:

1. One Jenkins job and one pipeline can manage multi branches.
2. Do not need to compile platforms to verify, save huge time and machines.
3. Stop looking for other people's mistakes, no one can break the build.
4. Builds can be generated quickly for QA testing

## Jenkinsfile example

In case of reduce simple build time and let PR creater and reviewer know the builds status as soon as possbile, you may need to do something different here, like below, used when condition and branch variable to check it is a develop branch or pull request branch.

```bash
when {
    branch 'PR-*'
}

when {
    branch 'develop'
}
```

The entire code pipeline looks like this:

```bash
// This Jenkinsfile is an explame for multibranch pipeline

pipeline {
    agent none
    stages {
        stage("All platform builds") {
            parallel {
                stage("Windows build") {
                    agent {
                        node {
                            label 'windows-vm01'
                            customWorkspace 'C:\\agent\\workspace\\blog'
                        }
                    }
                    stages {
                        stage("PR build") {
                            when {
                                branch 'PR-*'
                            }
                            steps {
                                checkout scm
                                dir('src\\build') {
                                    bat label: '', script: 'build.bat PR'
                                }
                            }
                        }
                        stage("Release build") {
                            when {
                                branch 'develop'
                            }
                            steps {
                                cleanWs()
                                checkout scm
                                dir('src\\build') {
                                    bat label: '', script: 'build.bat release'
                                }
                            }
                        }
                        stage("Deploy") {
                            echo "====if you have more stage, can add stage like this==="
                        }
                    }
                }
                stage("Linux build") {
                    agent {
                        node {
                            label 'linux-vm01'
                            customWorkspace '/agent/workspace/blog'
                        }
                    }
                    stages {
                        stage("PR build") {
                            when {
                                branch 'PR-*'
                            }
                            steps {
                                checkout scm
                                dir('src/build') {
                                    bat label: '', script: 'build.sh PR'
                                }
                            }
                        }
                        stage("Release build") {
                            when {
                                branch 'develop'
                            }
                            steps {
                                cleanWs()
                                checkout scm
                                dir('src/build') {
                                    bat label: '', script: 'build.sh release'
                                }
                            }
                        }
                    }
                }
                stage("AIX build"){
                    steps{
                        echo "====same as windows/Linux example, can write the code here you need ===="
                    }
                }
            }
        }
    }
}
```
