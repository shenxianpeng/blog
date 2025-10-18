---
title: Jenkinsfile example - 实现交互、clone 多个仓库以及 git push
summary: |
  这个 Jenkinsfile 示例展示了如何在 Jenkins Pipeline 中实现交互式输入、克隆多个 Git 仓库，并在构建完成后将代码推送到远程仓库。
date: 2019-07-07
tags:
  - Jenkins
  - Pipeline
translate: false
authors:
  - shenxianpeng
---

这个pipeline里包含了如下几个技术：

* 如何使用其他机器，agent
* 如何使用环境变量，environment
* 如何在build前通过参数化输入，parameters
* 如何使用交互，input
* 如何同时clone多个repos
* 如何进行条件判断，anyOf



```bash
pipeline {
    agent {
        node {
            label 'windows-agent'
        }
    }

    environment {
        MY_CRE = credentials("2aee7e0c-a728-4d9c-b25b-ad5451a12d")
    }

    parameters {
        // Jenkins parameter
        choice(
            name: 'REPO',
            choices: ['repo1', 'repo2', 'repo3', 'repo4'],
            summary: 'Required: pick a repo you want to build')
        string(
            name: 'BRANCH',
            defaultValue: '',
            summary: 'Required: chose a branch you want to checkout')
        string(
            name: 'BUILD_NO',
            defaultValue: '',
            summary: 'Required: input build number')
        string(
            name: 'JIRA_NO',
            defaultValue: '',
            summary: 'Optional: input jira ticket number for commit message')
    }

    stages {
        stage("Are you sure?"){
            steps{
                // make sure you want to start this build
                input message: "${REPO}/${BRANCH}:${BUILD_NO}, are you sure?"
                echo "I'm sure!"
            }
        }
        stage('Git clone repos') {
            steps {
                // git clone one repo source code
                checkout([
                    $class: 'GitSCM', branches: [[name: 'refs/heads/${BRANCH}']], browser: [$class: 'GitHub', repoUrl: 'https://github.com/${REPO}'], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'CleanBeforeCheckout'], [$class: 'LocalBranch', localBranch: '**'], [$class: 'RelativeTargetDirectory', relativeTargetDir: '../${REPO}']], submoduleCfg: [], userRemoteConfigs: [[credentialsId: '2aee7e0c-a728-4d9c-b25b', url: 'https://github.com/${REPO}.git']]])

                // git clone another repo source code
                checkout([
                    $class: 'GitSCM', branches: [[name: 'refs/heads/${BRANCH}']], browser: [$class: 'GitHub', repoUrl: 'https://github.com/${REPO}'], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'CleanBeforeCheckout'], [$class: 'LocalBranch', localBranch: '**'], [$class: 'RelativeTargetDirectory', relativeTargetDir: '../${REPO}']], submoduleCfg: [], userRemoteConfigs: [[credentialsId: '2aee7e0c-a728-4d9c-b25b', url: 'https://github.com/${REPO}.git']]])
            }
        }
        stage('Build repo1 and repo2') {
            when {
                // if REPO=repo1 or REPO=repo2, execute build_repo12.sh
                anyOf {
                    environment name: 'REPO', value: 'repo1'
                    environment name: 'REPO', value: 'repo2'
                }
            }
            steps {
                sh label: '', script: '${REPO}/build_repo12.sh ${REPO} ${BUILD_NO} ${JIRA_NO}'
            }
        }
        stage('Build repo3 and repo4') {
            when {
                // if REPO=repo3 or REPO=repo4, execute build_repo34.sh
                anyOf {
                    environment name: 'REPO', value: 'repo3'
                    environment name: 'REPO', value: 'repo4'
                }
            }
            steps {
                sh label: '', script: '${REPO}/build_repo34.sh ${REPO} ${BUILD_NO} ${JIRA_NO}'
            }
        }

        stage('Git push to remote repo') {
            steps {
                // commit code to remote repo
                sshagent(['2aee7e0c-a728-4d9c-b25b']) {
                    sh "git push https://%MY_CRE_USR%:%MY_CRE_PSW%@github.com/${REPO}.git"
                }
            }
        }
    }
}
```
