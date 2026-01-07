---
title: 在 Jenkins pipeline 中执行 sudo 的时候不需要输入密码
summary: 本文介绍了如何在 Jenkins Pipeline 中执行 sudo 命令而无需输入密码，提供了具体的实现方法和示例代码。
date: 2019-07-16
aliases:
  - /2019/07/execute-sudo-without-password/
tags:
- Jenkins
- Pipeline
- Shell
- OS
translate: false
authors:
  - shenxianpeng
---

在使用 Jenkins pipeline 的时候，在 Linux 需要用 root 来执行，我想通过 Jenkins pipeline 的语法来解决，但是只找到这种方式：[SSH Pipeline Steps](https://jenkins.io/doc/pipeline/steps/ssh-steps/)



```bash
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
```

从 example 来看需要提供的参数比较多，很多参数我已经在 Pipeline 的 environment 已经设置过了，这里再设置就显得不够优美，且限于没有足够的 example，你知道的 Jenkinsfile 调试非常痛苦和麻烦，我就没通过这种方式来尝试解决。

通过 Linux 设置来解决

```bash
// open a shell console and type
$ sudo visudo

// type your user name
jenkins ALL=(ALL) NOPASSWD: ALL
```

但即使这样设置，通过 Jenkins 执行 shell 脚本的时候还是出现如下问题

```shell
sudo: no tty present and no askpass program specified
```

最后通过如下脚本解决了我的问题

```shell
// Jenkinsfile

environment {
    JENKINS = credentials("d1cbab74-823d-41aa-abb7-85848595")
}

sh 'sudo -S <<< "$JENKINS_PSW" sh test.sh'
```

如果你有更好的方式，欢迎留言评论，谢谢。
