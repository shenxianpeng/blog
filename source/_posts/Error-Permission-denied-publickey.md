---
title: 'Error: Permission denied (publickey)'
date: 2018-05-06 16:15:18
tags: Git
---

如果你想在一台电脑上配置github和bitbucket，如何配置多个SSH git key？
输入以下命令生成SSH Key，注意在生成过程中最好输入新的名字，比如id_rsa_github和id_rsa_bitbucket
```
$ ssh-keygen -t rsa -C "your_email@youremail.com"
```
然后将生成的SSH key文件内容复制到对应网址的个人用户设置中即可。但是明明按照官方教程做的但是在git clone的时候还是遇到以下问题：
Error: Permission denied (publickey)
困恼了几天的错误终于解决了。

[参看这个文档](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/)

由于我用的是macOS Sierra 10.13.3，[文档这里](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/#adding-your-ssh-key-to-the-ssh-agent)写着如果是macOS Sierra 10.12.2 及以后的版本需要在
~/.ssh目录下创建一个config文件
congfig 文件的具体配置如下：
```
Host *
 AddKeysToAgent yes
 UseKeychain yes
 IdentityFile ~/.ssh/id_rsa_github

Host *
 AddKeysToAgent yes
 UseKeychain yes
 IdentityFile ~/.ssh/id_rsa_bitbucket
```
配置了这个文件之后，再次尝试
```
git clone git@github.com:shenxianpeng/blog.git
```
可以download代码了，两个SSH git都好用了 : )
