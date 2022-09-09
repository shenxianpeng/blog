---
title: Jenkins troubleshooting summary
author: shenxianpeng
date: 2019-08-16
tags:
- Jenkins
- Troubleshooting
categories:
- Jenkins
---

## ERROR: Error cloning remote repo 'origin' timeout=10

Recently, my Jenkins build failed when execute `git clone` with following this error message: ERROR: Error cloning remote repo 'origin'.

1. first I suspect it is the network reason, maybe because clone from Bitbucket need took up a lot bandwidth during `git clone` and causing this disconnection. but when I try to git clone on the agent, it works well.
2. Then I noticed the there is `timeout=10` in the Jenkins console log, I suddenly remembered that I deleted a very large folder a few days ago from git repo, and this may cause the repo more bigger, so it may take more time do a complete clone and it exceeds the Jenkins default clone timeout `10`.

Googling and finally I found this issue JENKINS-47660 which is the same problem as mine.

<!-- more -->

## Solution

Finally I found the the property of Advanced clone behaviors in Git clone in Jenkins, an checked Shallow clone then set Shallow clone depth equals to 1. (This setting is equivalent to --depth 1), and I changed timeout from 10 minutes to 15 minutes.

![Advanced clone behaviours](jenkins-troubleshooting/advanced-clone-behaviour.png)

## Full Log below

```log
using credential d1cbab74-823d-41aa-abb7
 Wiping out workspace first.
 Cloning the remote Git repository
 Cloning with configured refspecs honoured and without tags
 Cloning repository https://git.company.com/scm/db/blog.git
  > C:\Program Files\Git\bin\git.exe init C:\agent\workspace\develop # timeout=10
 Fetching upstream changes from https://git.company.com/scm/db/blog.git
  > C:\Program Files\Git\bin\git.exe --version # timeout=10
 using GIT_ASKPASS to set credentials blwmv
  > C:\Program Files\Git\bin\git.exe fetch --no-tags --progress https://git.company.com/scm/db/blog.git +refs/heads/develop:refs/remotes/origin/develop
 ERROR: Error cloning remote repo 'origin'
 hudson.plugins.git.GitException: Command "C:\Program Files\Git\bin\git.exe fetch --no-tags --progress https://git.company.com/scm/db/blog.git +refs/heads/develop:refs/remotes/origin/develop" returned status code 130:
 stdout:
 stderr: remote: Counting objects: 1
remote: Counting objects: 242690, done.
 remote: Compressing objects:   0% (1/75028)
remote: Compressing objects:   1% (751/75028)
remote: Compressing objects:   2% (1501/75028)
remote: Compressing objects:   3% (2251/75028)
remote: Compressing objects:   4% (3002/75028)
remote: Compressing objects:   5% (3752/75028)
... ...
remote: Compressing objects: 100% (75028/75028), done.
 Receiving objects:   0% (1/242690)
Receiving objects:   1% (2427/242690)
Receiving objects:   1% (4762/242690), 972.00 KiB | 949.00 KiB/s
Receiving objects:   2% (4854/242690), 972.00 KiB | 949.00 KiB/s
Receiving objects:   3% (7281/242690), 1.38 MiB | 919.00 KiB/s
Receiving objects:   3% (8998/242690), 1.82 MiB | 645.00 KiB/s
Receiving objects:   4% (9708/242690), 1.82 MiB | 645.00 KiB/s
Receiving objects:   4% (9778/242690), 1.82 MiB | 645.00 KiB/s
Receiving objects:   5% (12135/242690), 1.82 MiB | 645.00 KiB/s
... ...
Receiving objects:  86% (209321/242690), 1.01 GiB | 2.08 MiB/s
 	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl.launchCommandIn(CliGitAPIImpl.java:2042)
 	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl.launchCommandWithCredentials(CliGitAPIImpl.java:1761)
 	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl.access$400(CliGitAPIImpl.java:72)
 	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl$1.execute(CliGitAPIImpl.java:442)
 	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl$2.execute(CliGitAPIImpl.java:655)
 	at org.jenkinsci.plugins.gitclient.RemoteGitImpl$CommandInvocationHandler$1.call(RemoteGitImpl.java:153)
 	at org.jenkinsci.plugins.gitclient.RemoteGitImpl$CommandInvocationHandler$1.call(RemoteGitImpl.java:146)
 	at hudson.remoting.UserRequest.perform(UserRequest.java:212)
 	at hudson.remoting.UserRequest.perform(UserRequest.java:54)
 	at hudson.remoting.Request$2.run(Request.java:369)
 	at hudson.remoting.InterceptingExecutorService$1.call(InterceptingExecutorService.java:72)
 	at java.util.concurrent.FutureTask.run(Unknown Source)
 	at java.util.concurrent.ThreadPoolExecutor.runWorker(Unknown Source)
 	at java.util.concurrent.ThreadPoolExecutor$Worker.run(Unknown Source)
 	at java.lang.Thread.run(Unknown Source)
 	Suppressed: hudson.remoting.Channel$CallSiteStackTrace: Remote call to dendevu2uvbw01
 		at hudson.remoting.Channel.attachCallSiteStackTrace(Channel.java:1743)
 		at hudson.remoting.UserRequest$ExceptionResponse.retrieve(UserRequest.java:357)
 		at hudson.remoting.Channel.call(Channel.java:957)
 		at org.jenkinsci.plugins.gitclient.RemoteGitImpl$CommandInvocationHandler.execute(RemoteGitImpl.java:146)
 		at sun.reflect.GeneratedMethodAccessor1074.invoke(Unknown Source)
 		at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
 		at java.lang.reflect.Method.invoke(Method.java:498)
 		at org.jenkinsci.plugins.gitclient.RemoteGitImpl$CommandInvocationHandler.invoke(RemoteGitImpl.java:132)
 		at com.sun.proxy.$Proxy124.execute(Unknown Source)
 		at hudson.plugins.git.GitSCM.retrieveChanges(GitSCM.java:1152)
 		at hudson.plugins.git.GitSCM.checkout(GitSCM.java:1192)
 		at org.jenkinsci.plugins.workflow.steps.scm.SCMStep.checkout(SCMStep.java:124)
 		at org.jenkinsci.plugins.workflow.steps.scm.SCMStep$StepExecutionImpl.run(SCMStep.java:93)
 		at org.jenkinsci.plugins.workflow.steps.scm.SCMStep$StepExecutionImpl.run(SCMStep.java:80)
 		at org.jenkinsci.plugins.workflow.steps.SynchronousNonBlockingStepExecution.lambda$start$0(SynchronousNonBlockingStepExecution.java:47)
 		at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
 		at java.util.concurrent.FutureTask.run(FutureTask.java:266)
 		at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
 		at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
 		at java.lang.Thread.run(Thread.java:748)
 [Pipeline] }
 [Pipeline] // ws
 [Pipeline] }
 [Pipeline] // node
 [Pipeline] }
 [Pipeline] // stage
 [Pipeline] }
 Failed in branch Windows build
```

## java.io.IOException: error=24, Too many open files

I'm using a centos VM as Jenkins server, recently I have this problem "java.io.IOException: error=24, Too many open files", and run any Jenkins job will be failure.

1. Run `ulimit -n` the default value on my machine is `1024`.
2. Run `ulimit -n 4096` to increase this value to `4096` solved my problem

> https://stackoverflow.com/questions/46065008/too-many-open-files-error-cant-open-jenkins-after-installing-many-plugins
