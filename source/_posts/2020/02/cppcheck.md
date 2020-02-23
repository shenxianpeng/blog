---
title: 一个静态 C/C++ 代码分析工具 Cppcheck 和 Jenkins 集成
tags:
  - Jenkins
  - cppcheck
categories:
  - DevOps
date: 2020-02-16 21:14:12
author: shenxianpeng
---

最近我想完成 C/C++ 的静态代码扫描的集成，但是只要是 C/C++ 代码所涉及的工具很多都是收费的，比如首选的 SonarQube，Community 版本不支持 C/C++ 代码扫描，本着给公司省钱的目的，我尝试其他工具来替代。

本文记录我调查 cppcheck 和使用的经验，如果您也相关的需求，提供一点参考。

## 安装 Cppcheck

Linux 安装

```bash
sudo yum install cppcheck.x86_64
```

其他平台安装请参考 cppcheck [官网](http://cppcheck.sourceforge.net/)

如果你在 Linux 无法通过命令一键安装，也可通过下载源代码构建 cppcheck。以下是从代码手动构建一个 cppcheck 可执行文件的步骤

```bash
cd opt && mkdir cppcheck && cd cppcheck
# 下载代码
wget https://github.com/danmar/cppcheck/archive/1.90.tar.gz
# 解压
tar -xvf 1.90.tar.gz
# make build
cd cppcheck-1.90
mkdir build
cd build
cmake ..
cmake --build .
# link
sudo ln -s /opt/cppcheck/cppcheck-1.90/cppcheck /usr/bin/cppcheck
# 检查是否安装成功
which cppcheck
/usr/bin/cppcheck
cppcheck --version
Cppcheck 1.90
```

## 使用 cppcheck 静态代码扫描

```bash
# 在 Linux 使用 cppcheck 的 cppcheck-htmlreport 需要先安装 python-pygments
sudo yum install python-pygments
# 开始进行静态代码扫描
cppcheck src/uv src/u2 --xml 2> cppcheck.xml
```

有关 `cppcheck` 的差数说明请参看 [Cppcheck 官方文档](http://cppcheck.sourceforge.net/manual.pdf)

## Cppcheck 与 Jenkins 集成

下载 Cppcheck Jenkins [插件](https://plugins.jenkins.io/cppcheck/)，通过 Pipeline Syntax 生成了此代码 `publishCppcheck pattern: 'cppcheck.xml'`

但是在读取 xml 文件进行报告展示时，我遇到了两个问题：

问题1：分析 cppcheck.xml 我在有的 Linux 机器上成功，有的机器上会失败，我怀疑是我的 JDK 版本不同所致。Jenkins JIRA 我也找到了次问题 [JENKINS-60077](https://issues.jenkins-ci.org/browse/JENKINS-60077) 但目前还没有人来解决。

我之所以没有继续尝试去解决问题1，最主要的原因是它有一个对我来说是更致命的缺陷，那就是下面说的问题2。

```bash
# 问题2：查看代码文件时会出错
Can't read file: Can't access the file: file:/disk1/agent/workspace/cppcheck-ud113/src/u2/dummy/udt_err_printf.c
```

问题2： 无法通过 Cppcheck Results 报告直接查看代码，这样就算扫描出来了问题还需要去 git 或是本地的 IDE 上去查看具体的问题，大大降低效率。

并且官方也相应的 Ticket 记录了该问题 [JENKINS-42613](https://issues.jenkins-ci.org/browse/JENKINS-42613) 和 [JENKINS-54209](https://issues.jenkins-ci.org/browse/JENKINS-54209)，JENKINS-4261 代码等待 merge，不过还是暂时没有解决。

后来我发现 [Warnings Next Generation](https://plugins.jenkins.io/warnings-ng/) 将取代整个 Jenkins 静态分析套件，包含了这些插件 Android Lint, CheckStyle, Dry, FindBugs, PMD, Warnings, Static Analysis Utilities, Static Analysis Collector，最终我用 Warnings Next Generation 插件解决了报告展示的问题。

通过 Pipeline Syntax 生成了此代码 `recordIssues(tools: [codeAnalysis(pattern: 'cppcheck.xml')])`

更多有关 Warnings Next Generation 插件的使用，请参看[文档](https://github.com/jenkinsci/warnings-ng-plugin/blob/master/doc/Documentation.md)

### 最终 Pipeline 代码如下

```bash
pipeline{
  agent {
    node {
      label 'cppcheck'
      customWorkspace "/agent/workspace/cppcheck"
    }
  }

  parameters {
    string(name: 'Branch', defaultValue: 'develop', description: 'Which branch do you want to do cppcheck?')
  }

  options {
    timestamps ()
    buildDiscarder(logRotator(numToKeepStr:'50'))
  }

  stage("Checkout"){
    steps{
      checkout([$class: 'GitSCM', branches: [[name: '*/${Branch}']],
      browser: [$class: 'BitbucketWeb', repoUrl: 'https://git.yourcompany.com/projects/repos/cppcheck-example/browse'],
      doGenerateSubmoduleConfigurations: false, extensions: [
      [$class: 'LocalBranch', localBranch: '**'], [$class: 'CheckoutOption', timeout: 30], [$class: 'CloneOption', depth: 1, noTags: false, reference: '', shallow: true,   timeout: 30]], submoduleCfg: [],
      userRemoteConfigs: [[credentialsId: 'd1cbab74-823d-41aa-abb7', url: 'https://git.yourcompany.com/scm/cppcheck-example.git']]])
    }
  }
  stage("Cppcheck"){
    steps{
      script {
        sh 'cppcheck src/uv src/u2 --xml 2> cppcheck.xml'
      }
    }
  }
  stage('Publish results'){
    steps {
      // publishCppcheck pattern: 'cppcheck.xml'
      recordIssues(tools: [cppCheck(pattern: 'cppcheck.xml')])
    }
  }
}
```
