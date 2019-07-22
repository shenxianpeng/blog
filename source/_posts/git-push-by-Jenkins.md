---
title: 通过Jenkins来提交修改的代码(git push by Jenkins)
date: 2019-07-22 21:54:42
tags: [Jenkins, git]
categories: DevOps
---

在持续集成中，你可能需要通过Jenkins来修改代码，并且将修改后的代码提交到Git仓库里。怎么做呢？最方便的做法还是Jenkins提供对应的插件，但是很遗憾我没找到合适的。另外我也觉得通过脚本的方式来实现会更加稳定，不用担心Jenkins以及插件升级带来潜在不好用的可能。

以下pipeline片段供参考使用：
```
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
```
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

在最后一个阶段提交代码时，sheel脚本不能使用单引号 ''，要使用三引号才行''' '''。我在这里花了很多时间，一直找不到问题所在，因为我在上面的shell脚本使用的时候用单引号 '' 可以正常git clone代码，但在提交代码时不行，最后我Jenkins的Pipeline Syntax生成的脚本，提交代码成功。

