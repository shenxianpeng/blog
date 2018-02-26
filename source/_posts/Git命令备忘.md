---
title: Git命令备忘
date: 2018-02-26 20:46:44
tags: Git
---

有些git命令总是记不住，在我这台Ubuntu使用web版OneNote不方便，那就把他们记到Blog里吧，需要的时候翻看一下。

1. git remote
```
$ git remote -v                 //查看当前位置的远程代码库
$ git remote remove origin      //取消远程仓库
$ git remote add orgin git@github.com:shenxianpeng/nightwatch.git       //关联新的仓库
```

2. git log
```
// 得到某一时段提交日志
$ git log --after='2017-12-04' --before='2017-12-08' --author=xshen --pretty=oneline --abbrev-commit
```

3. git tag
```
$ git tag -a v1.6.700 -m 'Release v1.6.700' 

// 给前面的提交补上tag
$ git log --pretty=oneline
$ git tag -a v1.6.700 -m 'Release v1.6.700' e454ad98862

// push tag
git push origin --tag
```

4. 设置npm install代理
```
npm config set proxy=http://10.17.201.60:8080       //设置代理
npm config set proxy null                           //取消代理
```

5. cnpm
```
$ npm install -g cnpm --registry=https://registry.npm.taobao.org
$ cnpm install [name]
$ cnpm sync connect
$ cnpm info connect
```

