---
title: Git Guidelines
tags:
  - Guidelines
  - Git
categories:
  - DevOps
date: 2021-05-14 00:19:15
author: shenxianpeng
---

Everyone use Git should know these Git guidelines below.

1. Configure name and email

```bash
# Note that you need to replace your name and email
$ git config --global user.name "shenxianpeng"
$ git config --global user.email "xianpeng.shen@gmail.com"

# also recommended set your avatar if you can
```

2. Set core.autocrlf=false

To prevent CRLF(windows) and LF(UNIX/Linux/Mac) convert issues. to avoid history shelter problem when you committed code using Git, I strongly recommend that everyone using Git execute the following command

```bash
$ git config --global core.autocrlf false
# Check and see if output "core.autocrlf=false", which means the command setting success.
$ git config --list
```

3. Write conventional commits

Please read my this article: 

4. Git Commits Squash

Please be sure to read this wiki page Git Commits Squash


5. Delete merged branch

Please check Delete source branch after merging button before clicking Merge button

Please CHECK and DELETE your merged feature branches. (Do not delete hotfix/release/diag related important branches by mistake)
