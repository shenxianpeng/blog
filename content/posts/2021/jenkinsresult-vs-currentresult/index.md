---
title: Jenkins 中 `result` 与 `currentResult` 的区别
summary: |
  本文解释了 Jenkins Pipeline 中 `result` 与 `currentResult` 的区别，并通过 Declarative Pipeline 与 Scripted Pipeline 示例展示它们在不同阶段的表现。
tags:
  - Jenkins
date: 2021-01-14
authors:
  - shenxianpeng
---

> 这是一篇记录 `result` 与 `currentResult` 区别的笔记。

---

## 1. Declarative Pipeline 示例

以下是来自 [JENKINS-46325](https://issues.jenkins.io/browse/JENKINS-46325) 的测试代码：

```groovy
pipeline {
    agent any
    stages {
        stage ('Init') {
            steps {
                echo "Init result: ${currentBuild.result}"
                echo "Init currentResult: ${currentBuild.currentResult}"
            }
            post {
                always {
                    echo "Post-Init result: ${currentBuild.result}"
                    echo "Post-Init currentResult: ${currentBuild.currentResult}"
                }
            }
        }
        stage ('Build') {
            steps {
                echo "During Build result: ${currentBuild.result}"
                echo "During Build currentResult: ${currentBuild.currentResult}"
                sh 'exit 1'
            }
            post {
                always {
                    echo "Post-Build result: ${currentBuild.result}"
                    echo "Post-Build currentResult: ${currentBuild.currentResult}"
                }
            }
        }
    }
    post {
        always {
            echo "Pipeline result: ${currentBuild.result}"
            echo "Pipeline currentResult: ${currentBuild.currentResult}"
        }
    }
}
```

运行结果（部分）：

```
Init result: null
Init currentResult: SUCCESS
Post-Init result: null
Post-Init currentResult: SUCCESS
During Build result: null
During Build currentResult: SUCCESS
+ exit 1
Post-Build result: FAILURE
Post-Build currentResult: FAILURE
Pipeline result: FAILURE
Pipeline currentResult: FAILURE
Finished: FAILURE
```

**结论：**

* `currentResult` 在流水线运行中会反映**当前阶段的执行结果**（初始为 `SUCCESS`，阶段失败时更新为 `FAILURE`）。
* `result` 在 Declarative Pipeline 中为 `null`，直到流水线执行结束或阶段显式设置时才有值。

---

## 2. Scripted Pipeline 示例

以下是来自 [CloudBees 支持文档](https://support.cloudbees.com/hc/en-us/articles/218554077-How-to-set-current-build-result-in-Pipeline-) 的例子。

### 失败情况

```groovy
node {
    try {
        sh "exit 1"
        currentBuild.result = 'SUCCESS'
    } catch (Exception err) {
        currentBuild.result = 'FAILURE'
    }
    echo "RESULT: ${currentBuild.result}"
}
```

输出：

```
+ exit 1
RESULT: FAILURE
Finished: FAILURE
```

### 成功情况

```groovy
node {
    try {
        echo "I'm not going to fail"
        currentBuild.result = 'SUCCESS'
    } catch (Exception err) {
        currentBuild.result = 'FAILURE'
    }
    echo "RESULT: ${currentBuild.result}"
}
```

输出：

```
I'm not going to fail
RESULT: SUCCESS
Finished: SUCCESS
```

---

## 3. 总结

| 属性              | 类型          | 何时更新                           | 典型用途             |
| --------------- | ----------- | ------------------------------ | ---------------- |
| `currentResult` | 只读（String）  | 始终反映当前构建或阶段的实时状态，默认 `SUCCESS`  | 判断当前流水线/阶段执行是否失败 |
| `result`        | 可读写（String） | 默认 `null`，可在脚本中显式设置，或构建结束后自动赋值 | 手动控制或覆盖最终构建结果    |

简单来说：

* **`currentResult`** = “当前状态”
* **`result`** = “最终结果（可手动覆盖）”
