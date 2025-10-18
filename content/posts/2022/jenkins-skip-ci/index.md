---
title: 如何在 Jenkins 多分支流水线中实现 [skip ci]
summary: |
  本文介绍如何在 Jenkins 多分支流水线中实现 [skip ci] 功能，根据提交信息跳过构建。
tags:
  - CI
  - Jenkins
authors:
  - shenxianpeng
date: 2022-10-09
---

在 Jenkins 多分支流水线中实现 `[skip ci]` 或 `[ci skip]` 时，现有插件似乎已不可用。

* [JENKINS-35509](https://issues.jenkins.io/browse/JENKINS-35509)  
* [JENKINS-34130](https://issues.jenkins.io/browse/JENKINS-34130)  

> 建议：如果可能，尽量不要依赖 Jenkins 插件。

于是，我决定自己实现一个 `[skip ci]` 功能。

---

## 在 Jenkins Shared Library 中创建函数

如果你和我一样使用 Jenkins Shared Library，可以在 `src/org/cicd/utils.groovy` 中创建一个 `SkipCI` 函数，这样其他任务也可以复用。

```groovy
// src/org/cicd/utils.groovy
def SkipCI(number = "all"){
  def statusCodeList = []

  String[] keyWords = ['ci skip', 'skip ci'] // 可根据需要添加更多关键词
  keyWords.each { keyWord ->
    def statusCode = null
    if (number == "all") {
      statusCode = sh script: "git log --oneline --all | grep \'${keyWord}\'", returnStatus: true
    } else {
      statusCode = sh script: "git log --oneline -n ${number} | grep \'${keyWord}\'", returnStatus: true
    }
    statusCodeList.add(statusCode)
  }

  return statusCodeList.contains(0)
}
````

---

## 在其他任务中调用

```groovy
// 以下为示例代码，并非完整可运行的版本
import org.cicd.utils

def call(){

  pipeline {
    agent {
      node {
        label 'linux'
      }
    }

    parameters {
      booleanParam defaultValue: true, name: 'Build', summary: '取消勾选以跳过构建。'
    }

    def utils = new org.cicd.utils()

    stage("Checkout") {
      checkout scm

      // 仅检查最新一次提交信息
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

---

## 总结

通过这种方式，你可以在不依赖插件的情况下，在 Jenkins 多分支流水线中灵活地实现 `[skip ci]` 功能。
如果有任何问题或建议，欢迎留言交流。

---

转载本文请注明作者与出处，禁止商业用途。欢迎关注公众号「DevOps攻城狮」。
