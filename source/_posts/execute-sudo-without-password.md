---
title: execute sudo without password
date: 2019-07-16 21:07:39
tags: [Jenkins, pipeline, Shell]
categories: Shell
---

在使用Jenkins pipeline的时候，在Linux需要用root来执行，我想通过Jenkins pipeline的语法来解决，但是只找到这种方式，如下：
1. [SSH Pipeline Steps](https://jenkins.io/doc/pipeline/steps/ssh-steps/)

    ```
    def remote = [:]
    remote.name = 'test'
    remote.host = 'test.domain.com'
    remote.user = 'root'
    remote.password = 'password'
    remote.allowAnyHosts = true
    stage('Remote SSH') {
        sshCommand remote: remote, command: "ls -lrt"
        sshCommand remote: remote, command: "for i in {1..5}; do echo -n \"Loop \$i \"; date ; sleep 1; done"
    }
    ```
    * command
        * Type: String
    * dryRun (optional)
        * Type: boolean
    * failOnError (optional)
        * Type: boolean
    * remote (optional)
        * Nested Choice of Objects
    * sudo (optional)
        * Type: boolean

    从example来看需要提供的参数比较多，很多参数我已经在Pipeline的environment已经设置过了，这里再设置就显得不够优美，且限于没有足够的example，你知道的Jenkinsfile调试非常痛苦和麻烦，我就没通过这种方式来尝试解决。

2. 通过Linux设置来解决
    ```
    // open a shell console and type
    $ sudo visudo

    // type your user name
    jenkins ALL=(ALL) NOPASSWD: ALL
    ```
    但即使这样设置，通过Jenkins执行shell脚本的时候还是出现如下问题
    ```
    sudo: no tty present and no askpass program specified
    ```
    最后通过如下脚本解决了我的问题

    ```
    // Jenkinsfile

    environment {
        JENKINS = credentials("d1cbab74-823d-41aa-abb7-85848595")
    }

    sh 'sudo -S <<< "$JENKINS_PSW" sh test.sh'
    ```

如果你有更好的方式，欢迎留言评论，谢谢。