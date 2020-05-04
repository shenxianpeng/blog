---
title: 通过 Jenkins 来提交修改的代码 git push by Jenkins
date: 2019-07-22 21:54:42
tags: 
- Jenkins
- Git
- Pipeline
categories: 
- Jenkins
author: shenxianpeng
---

在持续集成中，你可能需要通过 Jenkins 来修改代码，并且将修改后的代码提交到Git仓库里。怎么做呢？最方便的做法还是 Jenkins 提供对应的插件，但是很遗憾我没找到合适的。另外我也觉得通过脚本的方式来实现会更加稳定，不用担心 Jenkins 以及插件升级带来潜在不好用的可能。

以下 pipeline 片段供参考使用：

```bash
// This pipeline is used for bumping build number

pipeline {

    environment {
        MYGIT = credentials("d1cbab74-823d-41aa-abb7")
    }
    stages {

        stage('Git clone repo') {
            steps {
                sh 'git clone -b develop --depth 1 https://$MYGIT_USR:"$MYGIT_PSW"@github.com/shenxianpeng/blog.git'
            }
        }

        stage('Change code stage'){
            steps {
                sh ''
            }
        }

        stage('Git push to remote repo') {
            steps {
                sh label: '', script: '''
                cd blog
                git add .
                git commit -m "Bld # 1001"
                git push https://$MYGIT_USR:"$MYGIT_PSW"@github.com/shenxianpeng/blog.git --all'''
            }
        }
    }

}
```

这里面我所遇到最大的坑，我之前脚本是这样写的：

```bash
stage('Git push to remote') {

    // not works script

    steps {
        sh 'cd blog'
        sh 'git add .'
        sh 'git commit -m "${JIRA_NO} Bld # ${BUILD_NO}"'
        sh 'git push https://$MYGIT_USR:"$MYGIT_PSW"@github.com/shenxianpeng/blog.git --all'
    }
}
```

在最后一个阶段提交代码时，shell 脚本不能使用单引号 ''，要使用三引号才行''' '''。我在这里花了很多时间，一直找不到问题所在，因为我在上面的shell脚本使用的时候用单引号 '' 可以正常 git clone 代码，但在提交代码时不行，最后我 Jenkins 的 Pipeline Syntax 生成的脚本，提交代码成功。
