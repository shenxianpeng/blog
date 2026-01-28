---
title: 新功能介绍：Explain Error Plugin 两项增强
summary: |
    在大家的反馈和贡献下，最近 Explain Error Plugin 新增了两个非常实用的功能：支持指定语言输出解释内容和支持在 Pipeline 中获取返回值以供编程使用。
tags:
  - Jenkins
  - AI
authors:
  - shenxianpeng
date: 2026-01-28
---

在大家的反馈和贡献下，最近 **Explain Error Plugin** 新增了两个非常实用的功能：

1. **支持指定语言输出解释内容**
2. **支持在 Pipeline 中获取返回值以供编程使用**

这次更新让插件在多语言支持和自动化使用场景下更加强大和友好。([GitHub][1])

---

## 一、支持指定语言输出解释内容（PR #76）

### 背景与功能

原先插件生成的错误解释内容默认是英文的，对于非英文读者来说体验不够友好。
通过 PR #76，我们为 `explainError()` **增加了一个可选的 `language` 参数**，允许用户指定希望获得错误解释的语言。([GitHub][1])

这意味着你可以让 AI 用中文、日语或其他语言来解释 Jenkins 构建失败的日志，从而更贴合团队的语言习惯（比如中文开发团队直接用中文解释）。

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

也可以用在不同语言：

```groovy
explainError(language: '日本語')
```

插件会自动将这个语言信息传给 AI 提示，让 AI 用指定语言生成错误解释内容。([GitHub][1])

---

## 二、支持返回值以便在 Pipeline 中编程使用（PR #77）

### 背景与功能

在某些场景下，我们希望 **不仅看到错误解释内容出现在 Jenkins UI 中，还能在 Pipeline 脚本里拿到这段内容进行进一步处理**（比如发送通知、发邮件、推送到聊天工具等）。

PR #77 添加了这项增强：现在 `explainError()` 步骤 **可以返回一个字符串结果**，方便将解释内容保存到变量并在 Pipeline 中使用。([GitHub][2])

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

通过这种方式，你不仅在侧边栏看到 AI 解释，还能进一步集成进你自己的流程。([GitHub][2])

---

## 小结

| 功能       | 说明                                        |
| -------- | ----------------------------------------- |
| 🌐 多语言支持 | 通过 `language:` 参数让 AI 解释内容以指定语言返回（中文、日语等） |
| 🔁 返回值支持 | 解释内容可以作为 Pipeline 步骤返回值用于自动化处理            |

这两个增强让 Explain Error Plugin **更加灵活、国际化且适用于更复杂的 CI/CD 流程**。如果你希望让错误解释更贴合你的团队语言或自动化集成通知系统，这次更新会大大提升体验！([GitHub][1])

赶快更新到最新版本，试试这些新功能吧！如果有任何建议或反馈，欢迎在 GitHub 上提出。Happy CI/CD! 🚀

---

[1]: https://github.com/jenkinsci/explain-error-plugin/pull/76 
[2]: https://github.com/jenkinsci/explain-error-plugin/pull/77