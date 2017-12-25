---
title: Ubuntu下安装Hexo
date: 2017-12-25 23:34:50
tags: ubuntu
---

执行如下命令：
``` bash
$ npm install                                   #Install dependencies
$ npm install hexo-deployer-git --save          #Install deploy
```
出现这个错误：-bash: hexo: command not found
***

执行如下命令：
``` bash
$ sudo npm install-g hexo
```
出现这个错误：/usr/bin/env: node: No such file or directory
***

执行这个命令，最终解决。
``` bash
$ sudo ln -s /usr/bin/nodejs /usr/bin/node
```
