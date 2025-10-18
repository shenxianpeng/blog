---
title: How to implement [skip ci] for Jenkins multi-branch pipeline
summary: |
  This article explains how to implement [skip ci] functionality in Jenkins multi-branch pipelines, allowing you to skip builds based on commit messages.
tags:
  - CI
  - Jenkins
author: shenxianpeng
date: 2022-10-09
---

When I want to implement [skip ci] or [ci skip] for Jenkins multi-branch pipeline, the existing plugin seems broken.

* [JENKINS-35509](https://issues.jenkins.io/browse/JENKINS-35509)

* [JENKINS-34130](https://issues.jenkins.io/browse/JENKINS-34130)

> My advice: try not to use the Jenkins plugin if possible.

Good, it's time to implement [skip ci] myself.

If you like me used Jenkins shared library, you can create a function like `SkipCI` from `src/org/cicd/utils.groovy`, then other jobs can reused this function.

```groovy
// src/org/cicd/utils.groovy
def SkipCI(number = "all"){
  def statusCodeList = []

  String[] keyWords = ['ci skip', 'skip ci'] // add more keywords if need.
  keyWords.each { keyWord ->
    def statusCode = null
    if (number == "all") {
      statusCode = sh script: "git log --oneline --all | grep \'${keyWord}\'", returnStatus: true
    } else {
      statusCode = sh script: "git log --oneline -n ${number} | grep \'${keyWord}\'", returnStatus: true
    }
    statusCodeList.add(statusCode)
  }

  if (statusCodeList.contains(0)) {
    return true
  } else {
    return false
  }
}
```

Then I can call this function from other jobs.

```groovy
// The following is not the complete code, it is just sample code and may not be run successfully.

import org.cicd.utils

def call(){

  pipeline {
    agent {
      node {
        label 'linux'
      }
    }

    parameters {
      booleanParam defaultValue: true, name: 'Build', summary: 'Uncheck to skip build.'
    }

    def utils = new org.cicd.utils()

    stage("Checkout") {
      checkout scm

      // just check the latest commit message.
      SkipCI = utils.SkipCI('1')
    }

    stage("Build"){
      when {
        beforeAgent true
        expression { return params.Build && !SkipCI }
      }

      steps {
        script {
          sh "make build"
        }
      }
    }
  }
}

```

Please let me know if any questions or suggestions.

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
