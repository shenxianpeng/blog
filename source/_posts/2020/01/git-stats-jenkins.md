---
title: 通过 Jenkins 定期自动给老板提供 Git 仓库的多维度代码分析报告
tags:
  - Stats
  - Git
categories:
  - Jenkins
date: 2020-01-21 22:06:53
author: shenxianpeng
---

上一篇（GitStats - Git 历史统计信息工具），我已经给老板提供了他想看的所有仓库的 Git 提交历史分析报告了，并且把报告都部署到了一台虚拟机的 tomcat 上了，老板可以通过网址访问直接查看每个仓库的分析报告了，看看谁的贡献大，谁活跃，谁偷懒了，谁周末写代码了（这里不鼓励 996）。

最近老板提需求了。

_老板：你弄个这个网址的数据咋不更新呢？报告上咋没见你们提交代码呢？_  
_小开：老板儿，您看到这些一个个仓库的数据都是小开我人肉手动生成的，要不您给我点时间，我来做个自动化任务吧。_

我这么积极主动，不是我奉承老板，我心里也知道老板如果觉得 Git Stats 这个工具好用，肯定希望看到的分析报告是最新的。既然老板先提了，那我就别磨蹭了，赶紧干吧。

不过用啥实现呢？肯定是 Jenkins 了。一来我已经在 Jenkins 上做了很多的自动化任务了，轻车熟路；二来使用同一套系统不但可以减少繁多的系统入口，降低学习成本，也提高 Jenkins 服务器的利用率。

设身处地的考虑了下老板的使用需求，他肯定不希望自己去 Jenkins 服务器上去运行 Job 来生成这个Git 仓库的多维度代码分析报告，那么，如果我是老板，我希望：

1. 这个 Jenkins 任务要定期执行，不需要太频繁，一周更新一次就行；
2. 另外还要支持对单独仓库的单独执行，一旦老板要立即马上查看某个仓库的的分析报告呢。

最后实现的效果如下：

## 手动执行

老板可以勾选他最关心的代码仓库进行更新

## 每周末定时执行

老板在周一上班就能看到最新的分析数据了，可以看到这个任务 Started by timer

## 最终的 Jenkinsfile 是这样的

```bash
pipeline{
  agent{
    node {
      label 'main-slave'
      customWorkspace "/workspace/gitstats"
    }
  }

  environment {
    USER_CRE = credentials("d1cbab74-823d-41aa-abb7")
    webapproot = "/workspace/apache-tomcat-7.0.99/webapps/gitstats"
  }

  parameters {
    booleanParam(defaultValue: true, name: 'repo1', description: 'uncheck to disable [repo1]')
    booleanParam(defaultValue: true, name: 'repo2', description: 'uncheck to disable [repo2]')
  }

  triggers {
    cron '0 3 * * 7'    # 每周日早上进行定时运行，因此此时机器是空闲的。
  }

  options {
    buildDiscarder(logRotator(numToKeepStr:'10'))
  }

  stages{
    stage("Checkout gitstats"){
      steps{
        # 准备存放 html 报告目录
        sh "mkdir -p html"
        # 下载 gitstats 代码
        sh "rm -rf gitstats && git clone https://github.com/hoxu/gitstats.git"
      }
    }
    stage("Under statistics") {
      parallel {
        stage("reop1") {
          when {
            expression { return params.repo1 }  # 判断是否勾选了
          }
          steps {
            # 下载要进行分析的仓库 repo1
            sh 'git clone -b master https://$USER_CRE_USR:"$USER_CRE_PSW"@git.software.com/scm/repo1.git'
            # 进行仓库 repo1 的历史记录分析
            sh "cd gitstats && ./gitstats ../repo1 ../html/repo1"
          }
          post {
            success {
              # 如果分析成功，则将分析结果放到 apache-tomcat-7.0.99/webapps/gitstats 目录下
              sh 'rm -rf ${webapproot}/repo1 && mv html/repo1 ${webapproot}'
              # 然后删掉 repo1 的代码和 html 报告，以免不及时清理造成磁盘空间的过度占用
              sh "rm -rf repo1"
              sh "rm -rf html/repo1"
            }
          }
        }
      }
      stage("repo2") {
          when {
            expression { return params.repo2 }
          }
          steps {
            sh 'git clone -b master https://$USER_CRE_USR:"$USER_CRE_PSW"@git.software.com/scm/repo2.git'
            sh "cd gitstats && ./gitstats ../repo2 ../html/repo2"
          }
          post {
            success {
              sh 'rm -rf ${webapproot}/repo2 && mv html/repo2 ${webapproot}'
              sh "rm -rf repo2"
              sh "rm -rf html/repo2"
            }
          }
        }
      }
    }
  }
  post{
    always{
      # 总是给执行者分送邮件通知，不论是否成功都会对工作空间进行清理
      script {
        def email = load "vars/email.groovy"
        email.build(currentBuild.result, '')
      }
      cleanWs()
    }
  }
}
```

## 最后

如果你是测试、DevOps或是从事研发效能方面的工作，那么利用好开源工具，比如 Jenkins 和 Git Stats 就可以快速帮助老板或是你自己提供一个 Git 仓库的多维度代码分析报告，有助于更加了解产品的代码情况。
