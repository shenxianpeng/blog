---
title: Explain Error Plugin 新增两大企业级功能：自定义上下文与文件夹级配置
summary: |
    Explain Error Plugin 迎来两个重要更新：支持自定义上下文信息和文件夹级别的 AI 提供商配置。这两个功能让插件在企业环境中的使用更加灵活和强大。
tags:
  - Jenkins
  - AI
authors:
  - shenxianpeng
date: 2026-02-13
---

最近 Explain Error Plugin 又迎来了两个重要的功能更新，这两个功能都是基于用户的实际使用反馈而开发的，能够让插件在企业环境中更加灵活和强大。

这两个新功能分别是：

1. **自定义上下文支持 (Custom Context)** - 让 AI 更懂你的业务场景
2. **文件夹级别的 AI 提供商配置** - 不同团队使用不同的 AI 服务



## 一、自定义上下文支持

### 为什么需要这个功能？

在使用 AI 解释构建错误时，我们经常会遇到这样的问题：**AI 虽然能识别错误，但不了解你的具体业务场景和环境信息**。

比如：
- 你的项目使用了特定的构建环境或工具链
- 你希望 AI 根据公司的最佳实践来提供解决方案
- 你需要 AI 考虑特定的约束条件（如不能升级某个依赖版本）

通过 [PR #83][1]，插件现在支持在全局配置和 Pipeline 步骤级别添加**自定义上下文信息**，这些信息会被传递给 AI，帮助生成更准确、更符合实际情况的错误解释。

### 如何使用自定义上下文

#### 1. 全局配置

在 Jenkins 系统配置中，你可以设置全局的自定义上下文：

1. 进入 **Manage Jenkins** → **Configure System**
2. 找到 **Explain Error Plugin** 配置区域
3. 在 **Custom Context** 字段中输入你的上下文信息

例如：
```
我们的项目运行在 Ubuntu 20.04 环境中，使用 Docker 进行构建。
我们不能升级到最新版本的 Node.js，必须使用 14.x 版本。
请优先考虑使用公司内部的镜像仓库来解决依赖问题。
```

#### 2. Pipeline 步骤级别覆盖

你也可以在具体的 Pipeline 中覆盖全局配置：

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
                def explanation = explainError(
                    customContext: '这是一个前端项目，使用 pnpm 作为包管理器。请不要建议使用 npm。'
                )
                echo explanation
            }
        }
    }
}
```

### 实际效果对比

**不使用自定义上下文时：**

```
Summary: The build failed because the `make` command was not found.

Resolution Steps:
- Install make using: apt-get install make
- Ensure make is in your PATH
```

**使用自定义上下文后：**

```
Summary: The build failed because the `make` command was not found. 
Given that your project runs in a Docker environment, this issue is likely 
related to your base image.

Resolution Steps:
- Update your Dockerfile to include: RUN apt-get update && apt-get install -y make
- Use a base image that already includes build tools, such as our internal 
  ubuntu-buildenv:20.04 image from the company registry
- Ensure your CI pipeline is using the correct Docker image version
```

可以看到，加入上下文信息后，AI 的回答更加贴合实际情况，提供的解决方案也更具针对性。

---

## 二、文件夹级别的 AI 提供商配置

### 企业场景中的实际需求

在大型企业环境中，不同的团队可能有不同的需求：

- **A 团队**使用公司统一采购的 Azure OpenAI 服务
- **B 团队**由于预算原因，使用开源的本地部署 LLM
- **C 团队**在进行敏感项目，需要使用完全隔离的私有 AI 服务
- **测试环境**可能不需要启用 AI 解释功能，以节省成本

之前的版本只支持**全局配置**，这意味着所有项目必须使用同一个 AI 提供商，这在企业环境中显然不够灵活。

### 文件夹级配置的优势

通过 [PR #88][2]，插件引入了 **Folder-Level Configuration** 功能，现在可以：

- ✅ 在 Jenkins 文件夹级别单独配置 AI 提供商
- ✅ 不同团队/项目使用不同的 AI 服务
- ✅ 支持配置继承，子文件夹自动继承父文件夹的配置
- ✅ 可以在文件夹级别完全禁用 AI 解释功能
- ✅ 未配置时自动回退到全局配置

### 如何配置文件夹级别的设置

#### 1. 创建或配置文件夹

在 Jenkins 中，进入你的文件夹（Folder）配置页面：

1. 点击文件夹名称
2. 点击 **Configure**
3. 找到 **Explain Error Configuration** 区域

#### 2. 配置选项

你会看到以下配置选项：

**Enable Error Explanation（启用错误解释）**
- 勾选此项以在此文件夹中启用 AI 错误解释
- 取消勾选则完全禁用此文件夹下所有项目的 AI 解释功能

**AI Provider（AI 提供商）**
- 可以选择与全局不同的 AI 提供商
- 支持 OpenAI、Azure OpenAI、Google Gemini 等主流服务
- 填写对应的 API Key 和配置信息

#### 3. 配置优先级

配置的优先级如下：

```
文件夹配置 > 父文件夹配置 > 全局配置
```

这意味着：
1. 如果当前文件夹有配置，使用当前配置
2. 如果当前文件夹没配置，查找父文件夹的配置
3. 如果整个文件夹链都没配置，使用全局配置

### 实际使用场景

#### 场景 1：不同团队使用不同 AI 服务

```
Jenkins Root（使用 OpenAI - 全局配置）
├── Team-A-Folder（继承全局配置，使用 OpenAI）
├── Team-B-Folder（配置使用 Google Gemini）
└── Team-C-Folder（配置为禁用 AI 解释）
```

#### 场景 2：生产与测试环境分离

```
Jenkins Root（全局配置 OpenAI）
├── Production（继承全局配置）
│   ├── App1-Pipeline
│   └── App2-Pipeline
└── Testing（禁用 AI 解释以节省成本）
    ├── Test-Pipeline-1
    └── Test-Pipeline-2
```

---

## 小结

| 功能 | 解决的问题 | 使用场景 |
|------|------------|----------|
| **自定义上下文** | AI 不了解你的具体业务场景 | 提供项目环境信息、约束条件、最佳实践等 |
| **文件夹级配置** | 全局配置无法满足不同团队的需求 | 不同团队使用不同 AI 服务，或按环境隔离 |

这两个功能的加入，让 [Explain Error Plugin][3] 在企业级应用场景中更加实用：

- **自定义上下文**让 AI 的解释更准确，更符合你的实际情况
- **文件夹级配置**让不同团队可以灵活地使用不同的 AI 服务，满足各种业务需求

如果你在使用过程中有任何建议或遇到问题，欢迎在 [GitHub][4] 上提 Issue 或 PR。

Happy CI/CD! 🚀

---

[1]: https://github.com/jenkinsci/explain-error-plugin/pull/83
[2]: https://github.com/jenkinsci/explain-error-plugin/pull/88
[3]: https://plugins.jenkins.io/explain-error/
[4]: https://github.com/jenkinsci/explain-error-plugin
