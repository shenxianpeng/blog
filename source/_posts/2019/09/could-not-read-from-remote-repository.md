---
title: 解决 Could not read from remote repository 问题
tags:
  - Git
  - Troubleshooting
categories:
  - Git
date: 2019-09-01 22:22:32
author: shenxianpeng
---

最近我在运行 Jenkins Job 时候突然发现 git clone 代码的时候突然报了这个错误：

```bash
$ git clone ssh://git@git.companyname.com:7999/mvcc/opensrc.git
Cloning into 'opensrc'...
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

这个错误只在我刚开始使用 git 的时候遇到过，那时候我还不知道如何使用 ssh 的方式来 clone 代码。怎么会出现这个错误呢？我也没改过什么，非常不理解。

## 常见解决方案

<!-- more -->

Google 了没有找到我遇到的这个问题，绝大多数都是应为没有生成 ssh-key，然后将 pub key 添加到 Github 或是其他 Web git 管理平台，对于这个问题是这样解决的，以 GitHub 为例

首先，生成 SSH key

```bash
# 记得替换成你自己的邮箱账号
ssh-keygen -t rsa -C xianpeng.shen@gmail.com
```

其次，拷贝 SSH pub key 到你使用的 git web 平台，比如 Github 等等。

```bash
cd %userprofile%/.ssh
# 打开 id_rsa.pub 并拷贝内容
notepad id_rsa.pub
```

最后，打开 <https://github.com/settings/ssh/new> 把你复制的内容贴进去保存即可。

## 通过 SSH 连接测试排查

对于我遇到的问题，这种解决方式是无效的，因为同样的账号在别的虚拟机上并不存在这个问题，因此我在这个 HP-UX 虚拟机上用了另外一个账号生成 ssh-key, git clone 代码没有问题，那我知道了就是这两个账号的之间存在差异。

首先，我查看了这两个账号的 .gitconfig 文件，确实有差异，当我将好用的账号的 .gitconfig 内容复制到不好用的账号的 .gitconfig 文件时，并不好用。

其次，我发现执行 git clone 的时候在当前目录下生成了一个 core 文件，说明已经 coredump 了，但是这个 core 直接打开大部分都是乱码，错误信息很难准确定位。

最后，我发现有一个命令是可以用来测试 SSH 连接的
对于 Github 是这个命令

```bash
ssh -T git@github.com
```

我当前使用和出问题的是 Bitbucket，它的 SSH 连接测试命令是：

```bash
ssh -vvv git\@bitbucket.org
```

我先用好 git clone 好用的账号，测试结果如下，这里我省略一些其他返回信息。

```bash
$ ssh -vvv git\@bitbucket.org
OpenSSH_6.2p1+sftpfilecontrol-v1.3-hpn13v12, OpenSSL 0.9.8y 5 Feb 2013      # OpenSSH 版本不同
HP-UX Secure Shell-A.06.20.006, HP-UX Secure Shell version                  # 原来是调用路径不同
debug1: Reading configuration data /opt/ssh/etc/ssh_config
debug3: RNG is ready, skipping seeding
debug2: ssh_connect: needpriv 0
debug1: Connecting to bitbucket.org [18.205.93.1] port 22.
debug1: Connection established.

... ...

debug2: we did not send a packet, disable method
debug1: No more authentication methods to try.
Permission denied (publickey).
```

我再用 git clone 不好用的账号进行测试，结果返回如下：

```bash
$ ssh -vvv git\@bitbucket.org
OpenSSH_8.0p1, OpenSSL 1.0.2s  28 May 2019                                  # OpenSSH 版本不同
debug1: Reading configuration data /usr/local/etc/ssh_config                # 原来是调用路径不同
debug2: resolving "bitbucket.org" port 22
debug2: ssh_connect_direct
debug1: Connecting to bitbucket.org [180.205.93.10] port 22.
debug1: Connection established.
Memory fault(coredump)
$
```

明显看到他们使用了不同版本的 OpenSSH，说明他们的环境变量有所不同。我之前查看过环境变量，但由于变量很多，不能一下判断那个变量可能会有影响。

## 最终解决方案

回到 git clone 失败的那个账号下面的 .profile 文件查看，这里确实添加了一个 /usr/bin 的环境变量，导致这个账号在执行 git clone 时候用了另外版本的 OpenSSH，我用的是 HP-UX，它对于包之前的依赖以及版本要求都非常高，把这个环境变量去掉之后，保存，重新登录到虚拟机，执行 git clone 恢复正常。
