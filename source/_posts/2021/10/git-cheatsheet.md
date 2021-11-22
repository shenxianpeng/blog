---
title: Git 常用命令备忘录
tags:
  - Git
  - Cheatsheet
categories:
  - Git
date: 2021-10-23 19:40:06
author: shenxianpeng
---

不管是对于 Git 的初学者还是经常使用 Git 的码农们，在日常工作中难免会有遇到有的命令一时想不起来。不妨将下面总结的一些 Git 常用命令及技巧收藏或打印出来，以备需要的时候可以很快找到。

## `git config`

```bash
# 检查 git 配置
git config -l

# 设置你的 git 提交 username 和 email
# 例如：对于公司里项目
git config --global user.name "Your Name"
git config --global user.email "your_email@organization.com"

# 例如：对于个人的 GitHub 项目
git config user.name "Your Name"
git config user.email "your_emailn@gmail.com"

# 使用 HTTP/HTTPS 避免每次输入密码
git config --global credential.helper cache
```

## `git init`

```bash
# 初始化一个仓库
git init
```

## `git add`

```bash
# 将文件添加到暂存区
git add file_name

# 将所有文件添加到暂存区
git add .

# 仅将某些文件添加到暂存区, 例如:仅添加所有以 'test*' 开头的文件
git add test*
```

## `git status`

```bash
# 检查仓库状态
git status
```

## `git commit`

```bash
# 提交更改
git commit

# 提交带有消息的更改
git commit -m "This is a commit message"
```

## `git log`

```bash
# 查看提交历史
git log

# 查看提交历史和显示相应的修改
git log -p

# 显示提交历史统计
git log --stat

# 显示特定的提交
git show commit_id

# 以图形方式显示当前分支的提交信息
git log --graph --oneline

# 以图形方式显示所有分支的提交信息
git log --graph --oneline --all

# 获取远程仓库的当前提交日志
git log origin/master
```

## `git diff`

```bash
# 在使用 diff 提交之前所做的更改
git diff
git diff some_file.js
git diff --staged
```

## `git rm`

```bash
# 删除跟踪文件
git rm file_name
```

## `git mv`

```bash
# 重命名文件
git mv old_file_name new_file_name
```

## `git checkout`

```bash
# 切换分支
git checkout branch_name

# 还原未暂存的更改
git checkout file_name
```

## `git reset`

```bash
# 还原暂存区的更改
git reset HEAD file_name
git reset HEAD -p
```

## `git commit --amend`

```bash
# 修改最近的提交信息
git commit --amend

# 修改最近的提交信息为：New commit message
git commit --amend -m "New commit message"
```

## `git revert`

```bash
# 回滚最后一次提交
git revert HEAD

# 回滚指定一次提交
git revert commit_id
```

## `git branch`

```bash
# 创建分支
git branch branch_name

# 创建分支并切到该分支
git checkout -b branch_name

# 显示当前分支
git branch

# 显示所有分支
git branch -a

# 检查当前正在跟踪的远程分支
git branch -r

# 删除分支
git branch -d branch_name
```

## `git merge`

```bash
# 将 branch_name 合并到当分支
git merge branch_name

# 中止合并
git merge --abort
```

## `git pull`

```bash
# 从远程仓库拉取更改
git pull
```

## `git fetch`

```bash
# 获取远程仓库更改
git fetch
```

## `git push`

```bash
# 推送更改到远程仓库
git push

# 推送一个新分支到远程仓库
git push -u origin branch_name

# 删除远程仓库分支
git push --delete origin branch_name
```

## `git remote`

```bash
# 添加远程仓库
git add remote https://repository_name.com

# 查看远程仓库
git remote -v

# 查看远程仓库的更多信息
git remote show origin
```

## Git技巧和窍门

### 清理已合并分支

清理已经合并的本地分支

```bash
git branch --merged master | grep -v "master" | xargs -n 1 git branch -d
```

### `.gitignore`

指明 Git 应该忽略的故意不跟踪的文件的文件，比如 `.gitignore` 如下

```bash
# 忽略 .vscode 目录
.vscode/

# 忽略 build 目录
build/

# 忽略文件
output.log
```

### `.gitattributes`

关于 `.gitattributes` 请参考

* https://www.git-scm.com/docs/gitattributes
* https://docs.github.com/en/get-started/getting-started-with-git/configuring-git-to-handle-line-endings
