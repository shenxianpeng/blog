---
title: Explain Error Plugin 又更新了：来自用户反馈的两个实用新功能
summary: |
    最近收到一些用户反馈，我也第一时间对 Explain Error Plugin 做了增强，新增了两个非常实用的功能：支持指定语言输出解释内容和支持在 Pipeline 中获取返回值 AI 的返回值。
tags:
  - Jenkins
  - AI
authors:
  - shenxianpeng
date: 2026-01-28
---

最近收到一些用户反馈，我也第一时间对 Explain Error Plugin 做了增强，新增了两个非常实用的功能：

1. **支持指定语言输出解释内容**
2. **支持在 Pipeline 中获取返回值 AI 的返回值**

这次更新让插件在多语言支持和自动化使用场景下变得更加灵活和友好。

## 一、支持指定语言输出解释内容

### 背景与功能

在之前的版本中，插件生成的错误解释内容默认是英文的，对于非英文使用者来说并不算友好。

通过 [PR #76][1]，我为 `explainError()` **增加了一个可选的 `language` 参数**，允许用户指定希望获得错误解释的语言。

这意味着你可以让 AI 使用中文、日语或其他语言来解释 Jenkins 构建失败的日志，从而更好地服务于不同语言背景的团队成员。

### 如何使用

你可以在 Jenkins Pipeline 中这样使用：

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'make build'  // 模拟构建过程
            }
        }
    }
    post {
        failure {
            // 指定语言为中文
            explainError(language: '中文')
        }
    }
}
```

通过上述配置，当构建失败时，插件会将语言参数一并传递给 AI，从而以指定语言生成错误解释内容。

---

## 二、支持返回值以便在 Pipeline 中编程使用

### 背景与功能

在一些使用场景中，用户不仅希望在 Jenkins UI 中看到错误解释内容，还希望 **能在 Pipeline 脚本中获取这段内容，进行进一步的自动化处理**，例如发送通知、发邮件或推送到聊天工具。

通过 [PR #77][2] 插件新增了返回值支持：现在 `explainError()` 步骤 **可以返回一个字符串结果**，步骤 **可以直接返回一个字符串结果**，方便在 Pipeline 中保存并使用。

### 如何使用返回值

示例 Pipeline：

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'make build'
            }
        }
    }
    post {
        failure {
            script {
                // 获取解释内容
                def explanation = explainError(language: '中文')
                echo "AI 解释结果：${explanation}"

                // 你可以在这里做更多自动化处理
                // 例如发送到 Slack 或邮件
            }
        }
    }
}
```

通过这种方式，你不仅可以在 Jenkins 页面中看到 AI 生成的解释内容，还能将其无缝集成到自己的 CI/CD 流程中。

---

## 小结

| 功能       | 说明                                        |
| -------- | ----------------------------------------- |
| 🌐 多语言支持 | 通过 `language:` 参数让 AI 解释内容以指定语言返回（中文、日语等） |
| 🔁 返回值支持 | 解释内容可以作为 Pipeline 步骤返回值用于自动化处理            |

这两个新功能让 [Explain Error Plugin][3] **在国际化和自动化方面都更加实用，也更贴近真实的 CI/CD 使用场景。**。

欢迎更新到最新版本体验这些新功能。如果你有任何建议或反馈，也非常欢迎在 [GitHub][4] 上提出。Happy CI/CD! 🚀

---

[1]: https://github.com/jenkinsci/explain-error-plugin/pull/76 
[2]: https://github.com/jenkinsci/explain-error-plugin/pull/77
[3]: https://plugins.jenkins.io/explain-error/
[4]: https://github.com/jenkinsci/explain-error-plugin
