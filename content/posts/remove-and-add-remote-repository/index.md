---
title: Git remove and add remote repository
summary: 本文介绍了如何在 Git 中移除和添加远程仓库，帮助开发者管理代码仓库的远程连接。
date: 2018-02-06
tags:
  - Git
author: shenxianpeng
---

如果是通过 https 方式来 pull 和 push 代码，每次都要输入烦人的账号和密码
可以通过切成成 ssh 方式：

```bash
# 取消远程仓库
git remote remove origin


# 关联远程仓库
git remote add origin git@github.com:shenxianpeng/blog.git
```
