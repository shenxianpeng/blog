---
title: Synchronize from Bitbucket to GitHub via Jenkins
tags:
  - GitHub
  - Bitbucket
  - Jenkins
categories:
  - Jenkins
date: 2020-05-05 16:54:09
author: shenxianpeng
---

### 背景

最近我们团队需要将一些示例和例子从内部的 Bitbucket 同步到 GitHub。我了解 GitHub 可以创建公共的或是私人的仓库，但我们需要保持以下两点

* 只分享我们想给客户分享的内容
* 不改变当前的工作流程，即继续使用 Bitbucket

<!-- more -->

因此我们需要在 GitHub 上创建相应的仓库，然后将内部 Bitbucket 仓库中对应的 master 分支定期的通过 CI job 同步到 BitHub 上去。

![](sync-from-bitbucket-to-github/sync-diagrom.png)

### 分支策略

首先，需要对 Bitbucket 进行分支权限设置

* master 分支只允许通过 Pull Request 来进行修改
* Pull Request 默认的 reviewer 至少需要一人，并且只有同意状态才允许合并

其次，为了方便产品、售后等人员使用，简化分支策略如下

1. 从 master 分支上创建 feature 或是 bugfix 分支（取决于你的修改目的）
2. 然后将你的更改提交到自己的 feature 或 bugfix 分支
3. 在你自己的分支通过测试后，提交 Pull Request 到 master 分支
4. 当 reviewer 同意状态，才能进行合并进入到 master 分支

![分支策略](sync-from-bitbucket-to-github/branch-strategy.png)

### Jenkins Pipeline

基于这样的工作不是特别的频繁，也为了方便维护 Jenkins Pipeline 的简单和易于维护，我没有在需要同步的每个仓库里添加 `Jenkinsfile` 或在 Bitbucket 里添加 `webhooks`。有以下几点好处：

* 只创建一个 Jenkins Job，用一个 `Jenkinsfile` 满足所有仓库的同步
* 减少了冗余的 `Jenkinsfile` 的代码，修改时只需更维护一个文件
* 不需要在每个仓库里添加一个 `Jenkinsfile`，更纯粹的展示示例，避免给非 IT 人员造成困扰

不足之处，不能通过 SCM 来触发构建，如果想通过 `webhooks` 来触发，有的公司需要申请权限来添加 `webhooks` 比较麻烦；另外可能无法区分从哪个仓库发来的请求，实现指定仓库的同步。

因此如果不是特别频繁的需要同步，提供手动或是定时同步即可。

```groovy
// 这个 Jenkinsfile 是用来将 Bitbucket 仓库的 master 分支同步到 GitHub 仓库的 master 分支
// This Jenkinsfile is used to synchronize Bitbucket repositories master branches to GitHub repositories master branches.

@Library('jenkins-shared-library@develop') _

def email = new org.cicd.email()

pipeline {

  agent {
    label "main-slave"
  }
  parameters {
    booleanParam(defaultValue: false, name: 'git-repo-win', description: 'Sync internal git-repo-win master branch with external git-repo-win on GitHub')
    booleanParam(defaultValue: true,  name: 'git-repo-lin', description: 'Sync internal git-repo-lin master branch with external git-repo-lin on GitHub')
    booleanParam(defaultValue: false, name: 'git-repo-aix', description: 'Sync internal git-repo-aix master branch with external git-repo-aix on GitHub')
    booleanParam(defaultValue: false, name: 'git-repo-sol', description: 'Sync internal git-repo-sol master branch with external git-repo-sol on GitHub')
  }
  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr:'50'))
  }
  stages {
    stage("Synchronous master branch"){
      steps{
        script {
          try {
            params.each { key, value ->
              def repoName = "$key"
              if ( value == true) {
                echo "Start synchronizing $key Bitbucket repository."
                sh """
                rm -rf ${repoName}
                return_status=0
                git clone -b master ssh://git@git.your-company.com:7999/~xshen/${repoName}.git
                cd ${repoName}
                git config user.name "Sync Bot"
                git config user.email "bot@your-company.com"
                git remote add github git@github.com:shenxianpeng/${repoName}.git
                git push -u github master
                return_status="\$?"
                if [ \$return_status -eq 0 ] ; then
                  echo "Synchronize ${repoName} from Bitbucket to GitHub success."
                  cd ..
                  rm -rf ${repoName}
                  exit 0
                else
                  echo "Synchronize ${repoName} from Bitbucket to GitHub failed."
                  exit 1
                fi"""
              } else {
                echo "${repoName} parameter value is $value, skip it."
              }
            }
            cleanWs()
          }
          catch (error) {
            echo "Some error occurs during synchronizing $key process."
          } finally {
            email.Send(currentBuild.currentResult, env.CHANGE_AUTHOR_EMAIL)
          }
        }
      }
    }
  }
}
```

以上的 `Jenkinsfile` 的主要关键点是这句 `params.each { key, value ->  }`，可以通过对构建时选择参数的进行判断，如果构建时参数已勾选，则会执行同步脚本；否则跳过同步脚本，循环到下一个参数进行判断，这样就实现了可以对指定仓库进行同步。

---

## Background

Recently our team need to share code from internal Bitbucket to external GitHub. I know GitHub can create private and public repository, but we have these points want to keep.

* only share the code what we want to share
* not change current work process, continue use Bitbucket.

So we have created corresponding repositories in the internal Bitbucket, and the master branches of these repositories will periodically synchronize with the master branches of corresponding repositories on GitHub via Jenkins job.

## Branch Strategy

Then the work process will be like

1. Create a feature or bugfix branch (it depends on the purpose of your modification).

2. Commit changes to your feature/bugfix branch.

3. Please pass your feature/bugfix branch test first then create a Pull Request from your branch to master branch, at least one reviewer is required by default.

4. After the reviewer approved, you or reviewer could merge the Pull Request, then the changes will be added to the master branch.

Timing trigger CI job will sync code from internal repositories master branch to GitHub master branch by default. also support manual trigger.

![Branch Strategy](sync-from-bitbucket-to-github/branch-strategy.png)

## Jenkins Job

Base on this work is not very frequency, so I want make the Jenkins job simple and easy to maintain, so I don't create every `Jenkinsfile` for every Bitbucket repositories.

Pros

* Only one `Jenkinsfile` for all Bitbucket repositories.
* Less duplicate code, less need to change when maintenance.
* Don't need to add `Jenkinsfile` into very Bitbucket repositories.

Cons

* Can not support SCM trigger, in my view this need add `Jenkinsfile` into repository.

The main part for this `Jenkinsfile` is below, use this function `params.each { key, value -> }` can by passing in parameters when start Jenkins build.
