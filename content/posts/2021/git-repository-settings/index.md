---
title: 建议在 Bitbucket/GitHub 中启用的仓库设置
summary: |
  列出 Bitbucket 和 GitHub 仓库推荐启用的设置，包括禁止强制推送、分支保护、标签管理、合并检查以及提交信息规范等。
tags:
  - Bitbucket
  - Git
date: 2021-01-12
authors:
  - shenxianpeng
---

我管理团队的 Git 仓库已经超过两年，日常主要使用 Bitbucket，这里以 Bitbucket 为例，介绍一些推荐开启的设置。

---

## 1. 禁止强制推送（Reject Force Push）

这是我最推荐的设置。  
如果不禁止，当有人执行 `git push -f` 且本地代码比远程旧时，就可能**导致提交丢失**。  
一旦发生这种情况，只能手动恢复，非常麻烦。我身边听说过三次类似事故。  
**建议尽快启用 “Reject Force Push” 钩子。**

---

## 2. 防止重要分支被删除（Branch Prevent Deletion）

对于非常重要的分支，建议开启**防止分支被删除**功能，避免因误操作丢失关键分支。

---

## 3. 为每次 Hotfix/GA 发布打标签

每次 Hotfix 或 GA 版本发布后，建议立即**创建标签**（tag），方便后续追溯版本。

---

## 4. 合并检查（Merge Check）

使用 Pull Request 是团队良好的协作流程之一。  
为了避免有人直接合并代码而未经过审核，我们启用了**最低 1 次审批**的限制。  
这样，任何想要合并到主分支的分支都必须添加**其他人**作为 Reviewer，并且 Reviewer 必须点击 “Approve”，否则 “Merge” 按钮不可用。

---

## 5. 提交信息检查（Yet Another Commit Checker）

[Yet Another Commit Checker (YACC)](https://mohamicorp.atlassian.net/wiki/spaces/DOC/pages/1442119700/Yet+Another+Commit+Checker+YACC+for+Bitbucket) 是非常强大的插件，可以帮助规范提交信息和分支命名。  

我写过一篇中文文章介绍如何使用它来落地提交规范，有兴趣可以阅读：[提交信息规范实践](https://shenxianpeng.github.io/2020/09/commit-messages-specification/)

---

✅ **总结**  
- 开启这些设置，可以有效防止误操作、提升代码质量、保障协作流程。  
- GitHub 上也有类似功能，例如 Branch Protection Rules、Required Reviews、Tagging 等，可根据实际情况启用。
