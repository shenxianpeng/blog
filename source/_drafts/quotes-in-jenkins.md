---
title: 在 Jenkins pipeline step 的 Shell 使用 """ and ''' 有什么不同？
tags:
  - Jenkins
  - Shell
categories:
  - Jenkins
date: 2021-11-16 15:51:42
author: shenxianpeng
---

在 Jenkins pipeline 中 使用 sh """ """ 和 sh ''' ''' 到底有什么不同？

这个困扰了我很久，终于准备花点时间彻底搞清楚。

问题：

Don'\''t use this script outside of SCL scriptlets!

重现

参考：

https://docs.cloudbees.com/docs/admin-resources/latest/automating-with-jenkinsfile/string-interpolation
https://gerg.dev/2021/03/adventures-with-escaping-quotes-in-jenkins-pipelines/
https://www.jenkins.io/doc/book/pipeline/getting-started/#snippet-generator
https://unix.stackexchange.com/questions/347332/what-characters-need-to-be-escaped-in-files-without-quotes
https://earthly.dev/blog/understanding-bash/
https://gist.github.com/Faheetah/e11bd0315c34ed32e681616e41279ef4

http://docs.groovy-lang.org/latest/html/documentation/index.html#all-strings

问题2：如何在 Shell 里使用 Jenkins parameter 的值呢？

/agent/workspace/test@tmp/durable-9b078cd7/script.sh: line 14: ${params.REPO_KEY}: bad substitution

参考答案：https://stackoverflow.com/questions/37219348/jenkins-pipeline-sh-bad-substitution-error


问题3：

```bash
/agent/workspace/polaris@tmp:/agent/workspace/polaris@tmp:rw,z -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** -e ******** den-artifactory.rocketsoftware.com:6568/u2bld:polaris cat
```

问题4：

process apparently never started in /agent/workspace/polaris@2@tmp/durable-f5b6b737
00:05:13.688  (running Jenkins temporarily with -Dorg.jenkinsci.plugins.durabletask.BourneShellScript.LAUNCH_DIAGNOSTICS=true might make the problem clearer)

https://support.cloudbees.com/hc/en-us/articles/360029374071-Build-fails-with-process-apparently-never-started-error

这个对我来说不好用。
