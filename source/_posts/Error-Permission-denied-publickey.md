---
title: 'Error: Permission denied (publickey)'
date: 2018-05-06 16:15:18
tags: Git
---

困恼了几天的 Error: Permission denied (publickey) 错误终于解决了。
[参看这个文档](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/)

由于我用的是macOS Sierra 10.13.3，[文档这里](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/#adding-your-ssh-key-to-the-ssh-agent)写着如果是macOS Sierra 10.12.2 及以后的版本需要在
~/.ssh目录下创建一个config文件
congfig 文件的具体配置如下：
```
Host *
 AddKeysToAgent yes
 UseKeychain yes
 IdentityFile ~/.ssh/id_rsa
```
配置了这个文件之后，再次尝试
```
git clone git@github.com:shenxianpeng/blog.git
```
可以download代码了:)
