---
title: Git 常见设置指北
tags:
  - Guidelines
  - Git
categories:
  - DevOps
date: 2021-05-14 00:19:15
author: shenxianpeng
---

在使用 Git 提交代码之前，建议做以下这些设置。

叫指南有点夸张，因为它在有些情况下下不适用，比如你已经有了 `.gitattributes` 或 `.editorconfig` 等文件，那么有些设置就不用做了。

因此暂且叫他指北吧，它通常情况下还是很有用的。

废话不多说，看看都需要哪些设置吧。

## 1. 配置 name 和 email

```bash
# 注意，你需要将下面示例中我的 name 和 email 换成你自己的
$ git config --global user.name "shenxianpeng"
$ git config --global user.email "xianpeng.shen@gmail.com"

```

对于，我还推荐你设置头像，这样方便同事间的快速识别。

当你不设置头像的时候，只有把鼠标放到头像上才知道 Pull Request 的 Reviewers 是谁（来自于Bitubkcet）。

![](git-guidelines/avatar.png)

## 2. 设置 core.autocrlf=false

为了防止 CRLF(windows) 和 LF(UNIX/Linux/Mac) 的转换问题。为了避免在使用 Git 提交代码时出现历史被掩盖的问题，强烈建议每个使用 Git 的人执行以下命令

```bash
$ git config --global core.autocrlf false
# 检查并查看是否输出 "core.autocrlf=false"，这意味着命令设置成功。
$ git config --list
```

如果你的项目底下已经有了 `.gitattributes` 或 `.editorconfig` 文件，通常这些文件里面都有放置 CRLF 和 LF 的转换问题的设置项。

这时候你就不必特意执行命令 `git config --global core.autocrlf false`

## 3. 编写有规范的提交

我在之前的文章里分享过关于如何设置提交信息规范，请参看[《Git提交信息和分支创建规范》](https://shenxianpeng.github.io/2020/09/commit-messages-specification/)。

## 4. 提交历史的压缩

比如你修改一个 bug，假设你通过 3 次提交到你的个人分支才把它改好。这时候你提 Pull Request 就会显示有三个提交。

如果提交历史不进行压缩，这个 PR 被合并到主分支后，以后别人看到你这个 bug 的修复就是去这三个 commits 里去一一查看，进行对比，才能知道到底修改了什么。

压缩提交历史就是将三次提交压缩成一次提交。

可以通过 git rebase 命令进行 commit 的压缩，比如将最近三次提交压缩成一次可以执行

```bash
git rebase -i HEAD~3
```

## 5. 删除已经 merge 的分支

有些 SCM，比如 Bitbucket 不支持默认勾选 `Delete source branch after merging`，这个问题终于在 Bitbucket 7.3 版本修复了。详见 [BSERV-9254](https://jira.atlassian.com/browse/BSERV-9254) 和 [BSERV-3272](https://jira.atlassian.com/browse/BSERV-3272) （2013年创建的）。

注意在合并代码时勾选删除源分支这一选项，否则会造成大量的开发分支留在 Git 仓库下。

---

如果还需要哪些设置这里没有提到的，欢迎补充。
