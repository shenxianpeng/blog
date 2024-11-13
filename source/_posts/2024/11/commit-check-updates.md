---
title: Commit Check 的最新更新 —— 新增检查 pull request 是否已经 rebase(WIP)
tags:
  - commit-check
  - DevOps
categories:
  - DevOps
draft: true
date: 2024-11-13 00:00:00
author: shenxianpeng
---

## 背景

最新有用户提出来（issue [191](https://github.com/commit-check/commit-check/issues/191)）是否可以让 `commit-check` 支持对于对分支进行是否已经 rebase 检查，跟其他检查一样，可以支持开启或是关闭。

哼哼，感觉这是一个不错的建议。因此经过一周过的晚上下班的陪娃间隙的时间的努力，现在正式宣布在最新的 commit-check 以及 commit-check-action 中都已经支持了一个新的选项叫做 `merge-base`。


对了如果你还不知道什么是 commit-check，这里我要隆重的介绍以下：

Commit Check 是一个免费且强大的工具，用于强制执行提交元数据标准，包括提交消息、分支命名、提交者姓名/邮箱以及提交签名，变基。它的错误信息和建议命令都可以完全自定义，确保团队之间的一致性。

作为 [GitHub Enterprise 元数据限制](https://docs.github.com/en/enterprise-server@3.11/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#metadata-restrictions)和 Bitbucket 付费插件 [Yet Another Commit Checker](https://marketplace.atlassian.com/apps/1211854/yet-another-commit-checker?tab=overview&hosting=datacenter) 的替代方案，Commit Check 通过集成 DevOps 原则和基础设施即代码（IaC）脱颖而出。

那么如何使用 commit-check 呢？有以下几种方式。

## 配置

### 使用默认配置

如果你没有设置 `.commit-check.yml`，Commit Check 将使用默认配置。提交消息将遵循 Conventional Commits 规则，分支命名遵循 Conventional Branch 规则。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
