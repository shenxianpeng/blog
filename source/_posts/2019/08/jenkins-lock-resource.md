---
title: "通过 Jenkins lock resource 来实现准备开发和测试环境"
description: "对于大型产品项目，准备不同的开发和测试环境十分重要"
author: shenxianpeng
poster: "./jenkins-multi-branch-pipeline/cover.jped"
date: 2019-08-10
tags:
- Jenkins
- Pipeline
categories: 
- Jenkins
keywords:
- Jenkins
- lock resource
---

## 业务场景

日常工作中需要切换到不同的版本进行开发和验证问题，但是由于虚拟机有限，并不能保证每个开发和测试都有所以平台的虚拟机并且安装了不同的版本，因此准备各种各样的开发和测试环境会花费很长时间。

## 需求分析

对于这样的需求，首先想到的是 Docker，其次只能从 Source Code Build（由于其他原因 Artifactory 暂时还不能使用）

* 先说 Docker，由于我们所支持的平台繁多，包括 Linux, AIX, Windows, Solris, HP-UX, 因此 Docker 不能满足这样的需求。

* 但是使用 Jenkins 需要解决主要问题 Jenkins build 完成后的环境，如果这个环境有人正在使用，那么这台虚拟机的资源应该被锁住，不允许 Jenkins 再去调用这台正在使用的 node，以保证环境在使用过程中不被破坏。

这里我是通过 Jenkins Lock Resource 来实现的。

## 演示 Demo

1. 设置 Lockable Resources
    * Jenkins -> configuration -> Lockable Resources Manager -> Add Lockable Resource
    ![我设置了两个 Resources ](jenkins-lock-resource\config-lock-resource.png)
    这里的 Labels 是你的 node 的 Label，在 Jenkins -> Nodes 设置

2. 查看 Lockable Resources 资源池

    ![显示我有两个资源可用 ](jenkins-lock-resource\lock-resource-pool.png)

3. 测试上锁
    * 这里我配置的是参数化类型的 Job，可以选择不同平台，不同仓库进行构建
    ![ Build With Parameters ](jenkins-lock-resource\build-with-parameters.png) build-with-parameters
    * 运行第一个 Job
    ![ 第一个 Job 已经运行 ](jenkins-lock-resource\build-with-parameters-1.png)
    * 查看当前可用资源数量, Free resources = 1，看到已经被 #47 这个 Job 所使用
    ![当前可用资源数为1](jenkins-lock-resource\lock-resource-pool-1.png)
    * 运行第二个 Job
    ![ 第二个 Job 已经运行 ](jenkins-lock-resource\build-with-parameters-2.png)
    * 查看当前可用资源数量，Free resources = 0，看到已经被 #48 这个 Job 所使用
    ![当前可用资源数为0](jenkins-lock-resource\lock-resource-pool-2.png)
    * 看关键是这一步，如果继续运行第三个 Job，是否可以被执行
    ![ 第三个 Job 已经运行 ](jenkins-lock-resource\build-with-parameters-3.png)
    * 可以看到这个任务没有开始执行，看下 log 是否真的没有被执行。通过日志发现，当前正在等待可用的资源
    ![ 第三个 Job log ](jenkins-lock-resource\build-with-parameters-3-log.png)

4. 测试释放锁
    * 现在释放一个资源，看下第三个 Job 是否能拿到资源，并且执行
    ![ 释放 Job 1 锁 ](jenkins-lock-resource\unlock-job-1.png)
    * 可以看到 第三个 Job 已经运行成功了
    ![ 第三个 Job 运行 ](jenkins-lock-resource\unlock-job-1-after.png)

## Jenkins pipeline 代码

整个 pipeline 最重要的部分就是上锁和释放，这里通过 lock 和 input message 来实现的。只要不点击 Yes，当前 Job 就会一直处于没有完成的状态，那么的它的锁会一直生效中。直到点击 Yes， Job 结束，锁也就释放了。具体可以参考下面的 Jenkinsfile。

```bash
pipeline {
    agent {
        node {
            label 'PreDevENV'
        }
    }
    options {
        lock(label: 'PreDevENV', quantity: 1)
    }

    parameters {
        choice(
            name: 'platform',
            choices: ['Linux', 'AIX', 'Windows', 'Solris', 'HP-UX'],
            description: 'Required: which platform do you want to build')
        choice(
            name: 'repository',
            choices: ['repo-0.1', 'repo-1.1', 'repo-2.1', 'repo-3.1', 'repo-4.1'],
            description: 'Required: which repository do you want to build')
        string(
            name: 'branch',
            defaultValue: '',
            description: 'Required: which branch do you want to build')
    }

    stages {
        stage('git clone'){
            steps {
                echo "git clone source"
            }
        }
        stage('start build'){
            steps {
                echo "start build"
            }
        }
        stage('install build'){
            steps{
                echo "installing"
            }
        }
        stage('unlock your resource'){
            steps {
                input message: "do you have finished?"
                echo "Yes, I have finished"
            }
        }
    }
}
```

## 总结

使用 Jenkins 从 source code 来编译安装需要花费一定的时间，远不如 Docker 来的快，也不如从 Artifactory 上取 build 进行安装更快。
