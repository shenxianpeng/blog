---
title: 'Error: Permission denied (publickey)'
summary: 本文介绍了如何在配置多个 SSH Git Key 时解决 "Permission denied (publickey)" 错误，确保 GitHub 和 Bitbucket 的 SSH 连接正常工作。
date: 2018-05-06
tags:
- Git
translate: false
authors:
  - shenxianpeng
---

如果你想在一台电脑上配置 github 和 bitbucket，如何配置多个 SSH git key？
输入以下命令生成 SSH Key，注意在生成过程中最好输入新的名字，比如 id_rsa_github 和 id_rsa_bitbucket

```bash

ssh-keygen -t rsa -C "your_email@youremail.com"
```

然后将生成的 SSH key 文件内容复制到对应网址的个人用户设置中即可。但是明明按照官方教程做的但是在 git clone 的时候还是遇到以下问题：
Error: Permission denied (publickey)
困恼了几天的错误终于解决了。

[参看这个文档](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/)

由于我用的是macOS Sierra 10.13.3，[文档这里](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/#adding-your-ssh-key-to-the-ssh-agent)写着如果是macOS Sierra 10.12.2 及以后的版本需要在
~/.ssh 目录下创建一个 config 文件
congfig 文件的具体配置如下：

```bash
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

```bash
git clone git@github.com:shenxianpeng/blog.git
```

可以 download 代码了，两个 SSH git 都好用了 : )
