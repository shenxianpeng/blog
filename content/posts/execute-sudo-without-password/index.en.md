---
title: Execute sudo without password—A Jenkins Pipeline Solution
summary: This article describes how to execute sudo commands in a Jenkins Pipeline without entering a password, providing specific implementation methods and sample code.
date: 2019-07-16
tags:
- Jenkins
- Pipeline
- Shell
- OS
author: shenxianpeng
---

When using the Jenkins pipeline, root privileges are sometimes needed on Linux systems.  I wanted to solve this using Jenkins pipeline syntax, but only found this method: [SSH Pipeline Steps](https://jenkins.io/doc/pipeline/steps/ssh-steps/)



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

The example requires many parameters, many of which I've already set in the Pipeline's environment. Setting them again here seems inelegant.  Furthermore,  due to a lack of sufficient examples and the notoriously painful debugging of Jenkinsfiles, I didn't try this approach.

Solving the problem via Linux configuration

```bash
// open a shell console and type
$ sudo visudo

// type your user name
jenkins ALL=(ALL) NOPASSWD: ALL
```

However, even with this configuration, executing a shell script through Jenkins still resulted in this error:

```shell
sudo: no tty present and no askpass program specified
```

Finally, I solved the problem using the following script:

```shell
// Jenkinsfile

environment {
    JENKINS = credentials("d1cbab74-823d-41aa-abb7-85848595")
}

sh 'sudo -S <<< "$JENKINS_PSW" sh test.sh'
```

If you have a better way, please leave a comment. Thank you.