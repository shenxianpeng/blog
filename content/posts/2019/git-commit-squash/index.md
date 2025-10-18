---
title: Git 提交合并（Squash）
summary: |
  介绍如何将多个 Git 提交合并为一个提交，包括本地和已推送到远程的情况，分别使用交互式 rebase 和在 Bitbucket 中的合并策略。
tags:
  - Squash
  - Git
date: 2019-08-20
authors:
  - shenxianpeng
---

## 本地提交尚未推送到远程

如果要将本地的多个提交合并为一个，可以按以下流程操作。

这里有一个 [3 分钟短视频](https://www.youtube.com/watch?v=V5KrD7CmO4o) 讲解了 `git rebase -i` 的用法。

1. 查看本地仓库的日志：
   ```bash
   git log --oneline
``

![list your logs in oneline](example-01.png)

2. 假设要合并最近的 3 个提交（`add6152`、`3650100`、`396a652`）：

   ```bash
   git rebase -i HEAD~3
   ```

   ![list last three commits](example-02.png)

3. 将需要合并到前一个提交的记录改为 `s` 或 `squash`：
   ![combine three commits to one](example-03.png)

4. 保存退出（`ESC` → `:wq!`）。

5. 在提交信息编辑界面中，注释掉不需要保留的提交信息：
   ![comment out some commits message you don't need](example-04.png)
   ![comment out some commits message you don't need](example-05.png)

6. 查看日志，确认已合并为一个提交：
   ![comment out some commits message you don't need](example-06.png)

---

## 提交已推送到远程

如果提交已推送到远程，建议新建分支进行 squash 以避免影响已有分支历史。

1. 查看日志：
   ![list your logs in oneline](example-07.png)

2. 新建分支：

   ```bash
   git checkout -b bugfix/UNV-1234-for-squash
   ```

3. 合并最近 2 个提交：

   ```bash
   git rebase -i HEAD~2
   ```

   ![select a commit you want to squash](example-08.png)

4. 修改提交信息，例如：

   ```
   UNV-1234 combine all commit to one commit
   ```

   ![comment out commit message you don't want to display](example-09.png)

5. 推送新分支到远程：

   ```bash
   git push -u origin bugfix/UNV-1234-for-squash
   ```
