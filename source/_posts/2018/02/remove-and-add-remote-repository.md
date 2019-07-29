---
title: Git remove and add remote repository
date: 2018-02-06 11:42:34
tags: Git
categories: Git
---

如果是通过https方式来pull和push代码，每次都要输入烦人的账号和密码
可以通过切成成ssh方式：

```bash
//取消远程仓库
$ git remote remove origin

//关联远程仓库
$ git remote add origin git@github.com:shenxianpeng/blog.git

```
