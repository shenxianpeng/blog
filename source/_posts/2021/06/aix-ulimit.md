---
title: 通过解除文件资源限制：解决在 AIX 使用 Git 下载大容量仓库失败问题
tags:
  - Git
  - AIX
categories:
  - Troubleshooting
date: 2021-06-17 13:52:44
author: shenxianpeng
---

最近使用 AIX 7.1 从 Bitucket 下载代码的时候遇到了这个错误 `fatal: write error: A file cannot be larger than the value set by ulimit.`

```bash
$ git clone -b dev https://<username>:<password>@git.company.com/scm/vmcc/opensrc.git --depth 1
Cloning into 'opensrc'...
remote: Counting objects: 2390, done.
remote: Compressing objects: 100% (1546/1546), done.
fatal: write error: A file cannot be larger than the value set by ulimit.
fatal: index-pack failed
```

这是由于这个仓库里的文件太大，超过了 AIX 对于用户文件资源使用的上限。通过 `ulimit -a` 可以来查看。更多关于 `ulimit` 命令的使用 [ulimit Command](https://www.ibm.com/docs/en/aix/7.1?topic=u-ulimit-command)

```bash
$ ulimit -a
time(seconds)        unlimited
file(blocks)         2097151
data(kbytes)         unlimited
stack(kbytes)        32768
memory(kbytes)       32768
coredump(blocks)     2097151
nofiles(descriptors) 2000
threads(per process) unlimited
processes(per user)  unlimited
```

可以看到 file 有一个上限值 2097151。如果将它也改成 unlimited 应该就好了。

通过 root 用户可以访问到 limits 文件 `/etc/security/limits`(普通用户没权限访问)。

```bash
# 以下是这个文件里的部分内容

default:
        fsize = 2097151
        core = 2097151
        cpu = -1
        data = -1
        rss = 65536
        stack = 65536
        nofiles = 2000
```
将上述的值 fsize = 2097151 改成 fsize = -1 就将解除了文件块大小的限制了。修改完成后，重新登录，再次执行 `ulimit -a`

```bash
$ ulimit -a
time(seconds)        unlimited
file(blocks)         unlimited
data(kbytes)         unlimited
stack(kbytes)        32768
memory(kbytes)       32768
coredump(blocks)     2097151
nofiles(descriptors) 2000
threads(per process) unlimited
processes(per user)  unlimited
```
此时 file(blocks) 已经变成 unlimited 了。再次尝试 git clone

```bash
$ git clone -b dev https://<username>:<password>@git.company.com/scm/vmcc/opensrc.git --depth 1
Cloning into 'opensrc'...
remote: Counting objects: 2390, done.
remote: Compressing objects: 100% (1546/1546), done.
remote: Total 2390 (delta 763), reused 2369 (delta 763)
Receiving objects: 100% (2390/2390), 3.80 GiB | 3.92 MiB/s, done.
Resolving deltas: 100% (763/763), done.
Checking out files: 100% (3065/3065), done.
```

这次就成功了！




