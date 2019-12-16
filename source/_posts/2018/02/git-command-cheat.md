---
title: Git 命令备忘
date: 2018-02-26 20:46:44
tags: Git
categories: Git
---

有些git命令总是记不住，在我这台 Ubuntu 使用 web 版 OneNote 不方便，那就把他们记到 Blog 里吧，需要的时候翻看一下。

git remote

```bash
git remote -v                 # 查看当前位置的远程代码库
git remote remove origin      # 取消远程仓库
git remote add orgin git@github.com:shenxianpeng/nightwatch.git       # 关联新的仓库
```

git log

```bash
# 得到某一时段提交日志
git log --after='2017-12-04' --before='2017-12-08' --author=xshen --pretty=oneline --abbrev-commit
```

git tag

```bash
git tag -a v1.6.700 -m 'Release v1.6.700'

# 给前面的提交补上 tag
git log --pretty=oneline
git tag -a v1.6.700 -m 'Release v1.6.700' e454ad98862

git push tag
git push origin --tag
```

设置 npm install 代理

```bash
npm config set proxy=http://10.17.201.60:8080       # 设置代理
npm config set proxy null                           # 取消代理
```

设置 cnpm

```bash
npm install -g cnpm --registry=https://registry.npm.taobao.org
cnpm install [name]
cnpm sync connect
cnpm info connect
```
