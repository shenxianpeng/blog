---
title: 解决在 AIX 上 Git Clone 失败的两个问题
summary: 本文记录了在 AIX 上使用 Jenkins 进行 Git Clone 时遇到的两个问题及其解决方法，包括依赖库加载失败和 SSH 认证失败。
tags:
  - Git
  - AIX
  - Jenkins
date: 2021-06-20
authors:
  - shenxianpeng
---

## 前言

本篇记录两个在做 Jenkins 与 AIX 做持续集成得时候遇到的 Git clone 代码失败的问题，并已解决，分享出来或许能有所帮助。

1. Dependent module /usr/lib/libldap.a(libldap-2.4.so.2) could not be loaded.
2. 通过 SSH 进行 git clone 出现 Authentication failed


## 问题1：Dependent module /usr/lib/libldap.a(libldap-2.4.so.2) could not be loaded

Jenkins 通过 **HTTPS** 来 checkout 代码的时候，出现了如下错误：

```bash
[2021-06-20T14:50:25.166Z] ERROR: Error cloning remote repo 'origin'
[2021-06-20T14:50:25.166Z] hudson.plugins.git.GitException: Command "git fetch --tags --force --progress --depth=1 -- https://git.company.com/scm/vas/db.git +refs/heads/*:refs/remotes/origin/*" returned status code 128:
[2021-06-20T14:50:25.166Z] stdout:
[2021-06-20T14:50:25.166Z] stderr: exec(): 0509-036 Cannot load program /opt/freeware/libexec64/git-core/git-remote-https because of the following errors:
[2021-06-20T14:50:25.166Z] 	0509-150   Dependent module /usr/lib/libldap.a(libldap-2.4.so.2) could not be loaded.
[2021-06-20T14:50:25.166Z] 	0509-153   File /usr/lib/libldap.a is not an archive or
[2021-06-20T14:50:25.166Z] 		   the file could not be read properly.
[2021-06-20T14:50:25.166Z] 	0509-026 System error: Cannot run a file that does not have a valid format.
[2021-06-20T14:50:25.166Z]
[2021-06-20T14:50:25.166Z] 	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl.launchCommandIn(CliGitAPIImpl.java:2450)
[2021-06-20T14:50:25.166Z] 	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl.launchCommandWithCredentials(CliGitAPIImpl.java:2051)
[2021-06-20T14:50:25.166Z] 	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl.access$500(CliGitAPIImpl.java:84)
[2021-06-20T14:50:25.167Z] 	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl$1.execute(CliGitAPIImpl.java:573)
[2021-06-20T14:50:25.167Z] 	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl$2.execute(CliGitAPIImpl.java:802)
[2021-06-20T14:50:25.167Z] 	at org.jenkinsci.plugins.gitclient.RemoteGitImpl$CommandInvocationHandler$GitCommandMasterToSlaveCallable.call(RemoteGitImpl.java:161)
[2021-06-20T14:50:25.167Z] 	at org.jenkinsci.plugins.gitclient.RemoteGitImpl$CommandInvocationHandler$GitCommandMasterToSlaveCallable.call(RemoteGitImpl.java:154)
..........................
[2021-06-20T14:50:25.167Z] 	Suppressed: hudson.remoting.Channel$CallSiteStackTrace: Remote call to aix-devasbld-01
[2021-06-20T14:50:25.167Z] 		at hudson.remoting.Channel.attachCallSiteStackTrace(Channel.java:1800)
..........................
[2021-06-20T14:50:25.168Z] 		at java.lang.Thread.run(Thread.java:748)
[2021-06-20T15:21:20.525Z] Cloning repository https://git.company.com/scm/vas/db.git
```

但是直接在虚拟机上通过命令 `git clone https://git.company.com/scm/vas/db.git` ，可以成功下载，没有出现任何问题。

* 如果将 `LIBPATH` 设置为 `LIBPATH=/usr/lib` 就能重现上面的错误，这说明通过 Jenkins 下载代码的时候它是去 `/usr/lib/` 下面找 `libldap.a`
* 如果将变量 `LIBPATH` 设置为空 `export LIBPATH=` 或 `unset LIBPATH`，执行 `git clone https://...` 就正常了。

> 尝试在 Jenkins 启动 agent 的时候修改 `LIBPATH` 变量设置为空，但都不能解决这个问题，不明白为什么不行！？

那就看看 `/usr/lib/libldap.a` 是什么问题了。

```bash
# ldd 的时候发现这个静态库有问题
$ ldd /usr/lib/libldap.a
/usr/lib/libldap.a needs:
         /opt/IBM/ldap/V6.4/lib/libibmldapdbg.a
         /usr/lib/threads/libc.a(shr.o)
Cannot find libpthreads.a(shr_xpg5.o)
         /opt/IBM/ldap/V6.4/lib/libidsldapiconv.a
Cannot find libpthreads.a(shr_xpg5.o)
Cannot find libc_r.a(shr.o)
         /unix
         /usr/lib/libcrypt.a(shr.o)
Cannot find libpthreads.a(shr_xpg5.o)
Cannot find libc_r.a(shr.o)

# 可以看到它链接到是 IBM LDAP
$ ls -l /usr/lib/libldap.a
lrwxrwxrwx    1 root     system           35 Jun 10 2020  /usr/lib/libldap.a -> /opt/IBM/ldap/V6.4/lib/libidsldap.a

# 再看看同样的 libldap.a 在 /opt/freeware/lib/ 是没问题的
$ ldd /opt/freeware/lib/libldap.a
ldd: /opt/freeware/lib/libldap.a: File is an archive.

$ ls -l /opt/freeware/lib/libldap.a
lrwxrwxrwx    1 root     system           13 May 27 2020  /opt/freeware/lib/libldap.a -> libldap-2.4.a
```

## 问题1：解决办法

```bash
# 尝试替换
# 先将 libldap.a 重名为 libldap.a.old（不删除以防需要恢复）
$ sudo mv /usr/lib/libldap.a /usr/lib/libldap.a.old
# 重新链接
$ sudo ln -s /opt/freeware/lib/libldap.a /usr/lib/libldap.a
$ ls -l /usr/lib/libldap.a
lrwxrwxrwx    1 root     system           27 Oct 31 23:27 /usr/lib/libldap.a -> /opt/freeware/lib/libldap.a
```

重新链接完成后，重新连接 AIX agent，再次执行 Jenkins job 来 clone 代码，成功了！

## 问题2：通过 SSH 进行 git clone 出现 Authentication failed

由于 AIX 7.1-TL4-SP1 即将 End of Service Pack Support，因此需要升级。但是升级到 AIX 7.1-TL5-SP6 后无法通过 SSH 下载代码。

```bash
$ git clone ssh://git@git.company.com:7999/vas/db.git
Cloning into 'db'...
Authentication failed.
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

像这样的错误，在使用 Git SSH 方式来 clone 代码经常会遇到，通常都是没有设置 public key。只要执行 `ssh-keygen -t rsa -C your@email.com` 生成 `id_rsa` keys，然后将 `id_rsa.pub` 的值添加到 GitHub/Bitbucket/GitLab 的 public key 中一般就能解决。

但这次不一样，尽管已经设置了 public key，但错误依旧存在。奇快的是之前 AIX 7.1-TL4-SP1 是好用的，升级到 AIX 7.1-TL5-SP6 就不好用了呢？

使用命令 `ssh -vvv <git-url>` 来看看他们在请求 git 服务器时候 debug 信息。

```bash
# AIX 7.1-TL4-SP1
bash-4.3$ oslevel -s
7100-04-01-1543
bash-4.3$ ssh -vvv git.company.com
OpenSSH_6.0p1, OpenSSL 1.0.1e 11 Feb 2013
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: Failed dlopen: /usr/krb5/lib/libkrb5.a(libkrb5.a.so):   0509-022 Cannot load module /usr/krb5/lib/libkrb5.a(libkrb5.a.so).
        0509-026 System error: A file or directory in the path name does not exist.

debug1: Error loading Kerberos, disabling Kerberos auth.
.......
.......
ssh_exchange_identification: read: Connection reset by peer
```

```bash
# New machine AIX 7.1-TL5-SP6
$ oslevel -s
7100-05-06-2015
$ ssh -vvv git.company.com
OpenSSH_7.5p1, OpenSSL 1.0.2t  10 Sep 2019
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: Failed dlopen: /usr/krb5/lib/libkrb5.a(libkrb5.a.so):   0509-022 Cannot load module /usr/krb5/lib/libkrb5.a(libkrb5.a.so).
        0509-026 System error: A file or directory in the path name does not exist.

debug1: Error loading Kerberos, disabling Kerberos auth.
.......
.......
ssh_exchange_identification: read: Connection reset by peer
```

可以看到的差别是 OpenSSH 的版本不同，可能是因此导致的，根据这个推测很快就找到了类似的问题和答案（Stackoverflow [链接](https://stackoverflow.com/questions/54191112/bitbucket-ssh-clone-on-aix-7-1-fails))

## 问题2：解决办法

在 `~/.ssh/config` 文件里添加选项 `AllowPKCS12keystoreAutoOpen no`

但问题又来了，这个选项是 AIX 上的一个定制选项，在 Linux 上是没有的。

这会导致同一个域账户在 AIX 通过 SSH 可以 git clone 成功，但在 Linux 上 git clone 会失败。

```bash
# Linux 上不识别改选项
stderr: /home/****/.ssh/config: line 1: Bad configuration option: allowpkcs12keystoreautoopen
/home/****/.ssh/config: terminating, 1 bad configuration options
fatal: Could not read from remote repository.
```

1. 如果 `config` 文件可以支持条件选项就好了，即当为 AIX 是添加选项 `AllowPKCS12keystoreAutoOpen no`，其他系统则没有该选项。可惜 `config` 并不支持。
2. 如果能单独的设置当前 AIX 的 ssh config 文件就好了。尝试将 `/etc/ssh/ssh_config` 文件修改如下，重启服务，再次通过 SSH clone，成功~！

```bash
Host *
  AllowPKCS12keystoreAutoOpen no
#   ForwardAgent no
#   ForwardX11 no
#   RhostsRSAAuthentication no
#   RSAAuthentication yes
#   PasswordAuthentication yes
#   HostbasedAuthentication no
#   GSSAPIAuthentication no
#   GSSAPIDelegateCredentials no
#   GSSAPIKeyExchange no
#   GSSAPITrustDNS no
#   ....省略
```
