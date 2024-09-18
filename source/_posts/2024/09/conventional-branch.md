---
title: 约定试分支规范正式发布 Conventional Branch Specification Released!
tags:
  - Git
categories:
  - DevOps
date: 2024-09-18 00:00:00
author: shenxianpeng
---

好消息！《约定式分支规范》开源项目正式上线！诚邀广大开发者共同参与，为项目贡献力量。更多详情请访问：https://conventional-branch.github.io

## 什么是约定试分支规范

约定试分支规范是指 Git 分支的结构化和标准化命名约定，旨在使分支更具可读性和可操作性。我们建议了一些你可能想要使用的分支前缀，但你也可以指定自己的命名约定。一致的命名约定使按类型识别分支变得更加容易。


## 规范

分支规范通过 `feature/`、`bugfix/`、`hotfix/`、`release/` 和 `chore/` 来描述，其结构应如下：

---

```
<type>/<description>
```

* **main**：主要开发分支（例如，`main`、`master` 或 `develop`）
* **feature/**：用于新功能（例如，`feature/add-login-page`）
* **bugfix/**：用于错误修复（例如，`bugfix/fix-header-bug`）
* **hotfix/**：用于紧急修复（例如，`hotfix/security-patch`）
* **release/**：用于准备发布的分支（例如，`release/v1.2.0`）
* **chore/**：用于依赖项更新等非代码任务（例如，`chore/update-dependencies`）

---

## 要点

1. **以目的为导向的分支名称**：每个分支名称都清楚地表明了其目的，使所有开发人员都可以轻松了解分支的用途。
2. **与CI/CD集成**：通过使用一致的分支名称，它可以帮助自动化系统（如持续集成/持续部署管道）根据分支类型触发特定操作（例如，从发布分支自动部署）。
3. **团队协作**：通过明确分支目的、减少误解并使团队成员更容易在任务之间切换而不会产生混淆，它鼓励团队内部的协作。

### 好处

* **清晰的沟通**：分支名称本身就提供了对其用途的清晰理解，而无需深入研究代码。
* **自动化友好**：轻松挂接到自动化流程（例如，针对功能、发布等的不同工作流程）。
* **可扩展性**：在许多开发人员同时处理不同任务的大型团队中效果很好。

总之，约定试分支命名旨在改善 Git 工作流程中的项目组织、沟通和自动化。

## 常见问题

**可以使用哪些工具自动识别团队成员是否不符合此规范？**

以使用 [commit-check](https://github.com/commit-check/commit-check) 检查分支规范或 [commit-check-action](https://github.com/commit-check/commit-check-action) 如果你的代码托管在 GitHub 上。

## 最后

非常感谢约定式提交规范的启发，在此基础上我们很高兴推出这个开源项目——约定式分支规范。

目前，项目仅提供英文版本，我们计划在未来增加更多语言版本，欢迎各位开发者踊跃参与！如果你对项目有任何建议或想贡献力量，欢迎在 [issues](https://github.com/conventional-branch/conventional-branch/issues) 页面提出。

感谢大家的关注！最后，欢迎Star和分享。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
