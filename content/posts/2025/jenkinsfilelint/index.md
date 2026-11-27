---
title: 受够了 Jenkinsfile 提交后才报错？试试这个预检查工具！
summary: Jenkinsfile 本地检查神器，利用 API 校验，完美支持 pre-commit。
tags:
  - Jenkins
  - DevOps
translate: true
authors:
  - shenxianpeng
date: 2025-11-27
---

> 更新（2026 年 11 月）：jenkinsfilelint 已改名为 [jenkins-lint](https://github.com/jenkinsci/jenkins-lint)，安装命令和 pre-commit 配置都变了，见 [Migrating to 2.0](https://jenkinsci.github.io/jenkins-lint/migrating/)。

大家好!

今天想和大家分享一个我最近开发的开源小工具：**jenkinsfilelint**。

#### **为什么写这个工具？**

相信写过 Jenkins Pipeline 的同学都有过这样的痛苦经历：

1.  辛辛苦苦写好了 `Jenkinsfile`。
2.  提交代码，推送到仓库。
3.  盯着 Blue Ocean 或 Console 等待构建开始。
4.  **崩！** 几秒钟后构建失败，原因竟然是少了一个括号 `}` 或者关键字拼写错误。
5.  修改代码 -\> 再次提交 -\> 等待 -\> 祈祷...

为了解决这个问题，我在市面上找了一圈 Jenkinsfile 的检查工具。虽然有一些现成的方案，但我发现它们要么配置繁琐，要么**无法很好地集成到 `pre-commit` 工作流中**。

既然没有顺手的工具，那就自己造一个吧！于是就有了 **jenkinsfilelint**。

#### **它是什么？**

`jenkinsfilelint` 是一个基于 Python 开发的命令行工具，旨在帮助你在代码提交前验证 Jenkinsfile 的语法正确性。

它通过调用 Jenkins 原生的 API 接口来进行校验，因此能够保证检查结果与实际运行时的解析逻辑完全一致。

**项目地址：**

> [https://github.com/shenxianpeng/jenkinsfilelint](https://github.com/shenxianpeng/jenkinsfilelint)

#### **核心特性**

  * ✅ **基于 Jenkins API**：利用 Jenkins 官方的 `/pipeline-model-converter/validate` 接口，校验结果不仅准确，还能提示具体的错误行号。
  * 🚀 **完美支持 pre-commit**：这是我开发它的初衷。你可以把它轻松集成到项目的 git hooks 中，确保每次 commit 前自动检查。
  * 🛠 **配置灵活**：支持通过环境变量或命令行参数配置 Jenkins 地址和凭证。
  * 🔍 **智能过滤**：在使用 Jenkins Shared Library 时，仓库里可能包含纯 Groovy 的辅助类文件（不是 Pipeline 脚本）。工具支持通过 `--skip` 参数跳过这些文件，避免误报。

#### **如何使用？**

##### 1\. 安装

你可以直接使用 pip 安装：

```bash
pip install jenkinsfilelint
```

##### 2\. 集成到 pre-commit（强烈推荐）

在你的项目根目录下创建或修改 `.pre-commit-config.yaml` 文件，添加如下配置：

```yaml
repos:
  - repo: https://github.com/shenxianpeng/jenkinsfilelint
    rev: v1.2.0  # 建议使用最新版本 tag
    hooks:
      - id: jenkinsfilelint
```

然后安装钩子：

```bash
pre-commit install
```

##### 3\. 配置凭证

由于校验需要调用 Jenkins 的 API，你需要提供 Jenkins 的地址和访问凭证。

**⚠️ 安全提示**：强烈建议不要将账号密码硬编码在配置文件中！推荐使用环境变量的方式：

```bash
# Linux/macOS
export JENKINS_URL=https://your-jenkins-instance.com
export JENKINS_USER=your-username
export JENKINS_TOKEN=your-api-token
```

配置好之后，当你尝试执行 `git commit` 时，`jenkinsfilelint` 就会自动帮你检查变更中的 Jenkinsfile 了！

#### **命令行手动检查**

当然，你也可以在本地手动运行它来检查特定文件：

```bash
# 检查单个文件
jenkinsfilelint Jenkinsfile

# 检查多个文件
jenkinsfilelint Jenkinsfile Jenkinsfile.prod

# 跳过特定模式的文件（例如 src 目录下的 Groovy 文件）
jenkinsfilelint --skip '*/src/*.groovy' Jenkinsfile src/Utils.groovy
```

#### **写在最后**

这个项目目前已经发布在 PyPI 上，欢迎大家下载试用。

如果你也受够了 Jenkinsfile 的“提交后报错”，不妨试试 `jenkinsfilelint`。如果觉得好用，欢迎在 GitHub 上点个 **⭐️ Star** 支持一下！

如有任何问题或建议，欢迎提 Issue 或 PR。

**GitHub 传送门：**
[https://github.com/shenxianpeng/jenkinsfilelint](https://github.com/shenxianpeng/jenkinsfilelint)
