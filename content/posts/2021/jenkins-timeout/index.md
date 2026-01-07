---
title: Jenkins 作业超时后让构建失败的方法（已解决）
summary: |
  本文介绍如何在 Jenkins 流水线中正确处理超时场景，通过 `try` 和 `catch` 结合 `error` 确保超时后作业会失败。
tags:
  - Jenkins
date: 2021-06-24
aliases:
  - /2021/06/jenkins-timeout/
authors:
  - shenxianpeng
---

在一些情况下，即使设置了超时，Jenkins 作业依然不会因为超时自动失败，比如某些进程没有正常结束。

为了解决这个问题，可以在流水线中结合 `try` .. `catch` 与 `error`，在超时后显式让构建失败。

---

## 示例代码

```groovy
pipeline {
    agent none
    stages {
        stage('Hello') {
            steps {
                script {
                    try {
                        timeout(time: 1, unit: 'SECONDS') {
                            echo "timeout step"
                            sleep 2
                        }
                    } catch (err) {
                        // 捕获超时异常
                        println err
                        echo 'Time out reached.'
                        error 'build timeout failed'
                    }
                }
            }
        }
    }
}
```

---

## 日志输出

```log
[Pipeline] Start of Pipeline
[Pipeline] stage
[Pipeline] { (Hello)
[Pipeline] script
[Pipeline] {
[Pipeline] timeout
Timeout set to expire in 1 sec
[Pipeline] {
[Pipeline] echo
timeout step
[Pipeline] sleep
Sleeping for 2 sec
Cancelling nested steps due to timeout
[Pipeline] }
[Pipeline] // timeout
[Pipeline] echo
org.jenkinsci.plugins.workflow.steps.FlowInterruptedException
[Pipeline] echo
Time out reached.
[Pipeline] error
[Pipeline] }
[Pipeline] // script
[Pipeline] }
[Pipeline] // stage
[Pipeline] End of Pipeline
ERROR: build timeout failed
Finished: FAILURE
```

---

## 总结

* `timeout` 步骤会在超时后抛出 `FlowInterruptedException`
* 通过 `try`/`catch` 捕获异常后调用 `error`，可以强制让 Jenkins 构建标记为 **FAILURE**
* 这种方式适用于任何需要在超时后终止并失败的场景

---

转载请注明作者与出处，欢迎关注公众号「DevOps攻城狮」获取更多 Jenkins 实战技巧。
