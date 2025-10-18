---
title: 在 Jenkins 中为不同分支设置不同的默认参数
summary: |
  本文介绍如何在 Jenkins 多分支流水线中，根据构建分支动态设置不同的默认参数，从而实现分支差异化配置。
tags:
  - Jenkins
date: 2021-03-24
authors:
  - shenxianpeng
---

## 问题背景

在使用 Jenkins **多分支流水线**（Multibranch Pipeline）时，有时需要针对不同分支设置不同的默认参数。

例如：

- **develop / hotfix / release 分支**  
  除了常规构建外，还需要进行代码扫描等额外分析（如安全扫描、质量检测）。
- **feature / bugfix 分支**或 Pull Request  
  只需要进行常规构建，不执行额外扫描。

因此，我们希望参数能够根据分支自动设置默认值。

---

## 解决方案

在 Jenkinsfile 中，可以通过 `env.BRANCH_NAME` 判断当前构建分支，并设置默认参数值。

示例代码：

```groovy
def polarisValue = false
def blackduckValue = false

if (env.BRANCH_NAME.startsWith("develop") || 
    env.BRANCH_NAME.startsWith("hotfix")  || 
    env.BRANCH_NAME.startsWith("release")) {
    polarisValue = true
    blackduckValue = true
}

pipeline {
    agent { node { label 'gradle' } }

    parameters {
        booleanParam defaultValue: polarisValue, name: 'Polaris',  description: '取消勾选可禁用 Polaris 扫描'
        booleanParam defaultValue: blackduckValue, name: 'BlackDuck', description: '取消勾选可禁用 BlackDuck 扫描'
    }

    stages {
        // 构建、测试、扫描等步骤
    }
}
```

---

✅ **优点**

* 不需要为每个分支单独维护一套 Jenkinsfile。
* 参数可灵活控制，方便扩展更多分支规则。
* 支持在多分支流水线中实现“按需扫描”，节省构建时间。

这样配置后，Jenkins 在不同分支构建时会自动使用对应的参数默认值，避免人工干预。
