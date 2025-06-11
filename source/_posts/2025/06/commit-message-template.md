---
title: 提升代码可追溯性：一招把 PR 描述写入 Git commit
tags:
  - Git
  - Bitbucket
categories:
  - Git
author: shenxianpeng
date: 2025-06-12 12:32:00
---

## 背景

最近和同事讨论了一个看似简单但很重要的问题：

**我们如何确保 PR 中有价值的信息不会随着时间和工具的更替而丢失？**

虽然我们日常使用 Bitbucket 来协作开发，但未来也许会迁移到 GitHub、GitLab 等平台。**这些托管平台可能会变，但 Git 本身作为代码历史的记录核心，很可能还会长期存在。**

问题也就来了：

> PR 页面里描述的变更背景、解决思路和关键讨论，如果只保存在 PR 工具里，就很可能在平台迁移后“消失”。而这些信息，本应是 commit message 的一部分。

## 我们讨论过的一些方案：

1. **在 `git commit -m` 时手动记录问题的解决方式** —— 但容易被忽略或写得不完整。
2. **模仿 pip 项目使用 `NEWS` 文件** 来记录每次变更 —— 虽然能保留信息，但这种方式更适合用于生成 release note，而不是记录修改的动机或原因。
3. **强制要求成员把内容写在 Jira ticket 中** —— 工具间割裂，不利于在代码上下文中快速理解历史。

最终我们决定：**使用 Bitbucket 的 Commit Message Templates 功能，把 PR 的描述直接写入 Git commit 中。**

<!--more-->

## Bitbucket 的 Commit Message Templates 功能

Bitbucket 支持在合并 PR 时自动生成 commit message，并允许通过模板插入有用的信息。文档地址如下：
🔗 [Pull request merge strategies - Bitbucket Server](https://confluence.atlassian.com/bitbucketserver0819/pull-request-merge-strategies-1416826109.html)


> 我看到了 GitLab 也有类似的功能，但 GitHub 似乎没有。
>
> GitLab commit templates: https://docs.gitlab.com/user/project/merge_requests/commit_templates/

你可以在模板中使用以下变量：

| 变量名                             | 说明          |
| --------------------------------- | ------------- |
| `title`                           | PR 标题       |
| `id`                              | PR ID         |
| `description`                     | PR 描述       |
| `approvers`                       | 当前已批准的审阅人 |
| `fromRefName` / `toRefName`       | 源 / 目标分支名称  |
| `fromProjectKey` / `toProjectKey` | 源 / 目标项目      |
| `fromRepoSlug` / `toRepoSlug`     | 源 / 目标仓库      |
| `crossRepoPullRequestRepo`        | 跨仓库 PR 的源仓库信息 |

## 我们是怎么用的？

在 Bitbucket 的仓库设置中，你可以配置 PR 的合并提交模板，找到设置：

Repository settings -> Merge strategies -> Commit message template

配置后，当你在 PR 页面合并时，Bitbucket 会自动把 PR 的标题、描述、相关 ID 等内容写入最终的 merge commit message 中。

这样，不管将来团队是否继续使用 Bitbucket，**PR 的关键信息都将永远保存在 Git 历史中**。

下面是实际效果：

📥 配置模板界面：
![Bitbucket 模板配置界面](commit-message-template/bb-template.png)

📤 最终生成的 Git commit message：
![最终合并 commit 的样子](commit-message-template/bb-result.png)

## 总结

这项改动虽然小，却帮助我们从流程上保护了代码变更的上下文。它让 PR 不再是“临时信息容器”，而是自然地成为 Git 历史的一部分。

如果你也在使用 Bitbucket，不妨试试这个功能。

让 Git commit message，不只是代码提交，更是决策和演进的记录。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
