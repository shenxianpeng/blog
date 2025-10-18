---
title: Resolving Git Large Repository Download Failures on AIX by Removing File Resource Limits
summary: Resolving Git large repository download failures on AIX due to file size limits by modifying ulimit settings.
tags:
  - Git
  - AIX
  - ulimit
date: 2021-06-17
author: shenxianpeng
---

Recently, when downloading code from Bitbucket using AIX 7.1, I encountered this error:


`fatal: write error: A file cannot be larger than the value set by ulimit.`

```bash
$ git clone -b dev https://<username>:<password>@git.company.com/scm/vmcc/opensrc.git --depth 1
Cloning into 'opensrc'...
remote: Counting objects: 2390, done.
remote: Compressing objects: 100% (1546/1546), done.
fatal: write error: A file cannot be larger than the value set by ulimit.
fatal: index-pack failed
```

On AIX 7.3, I encountered this error:

`fatal: fetch-pack: invalid index-pack output`

```bash
$ git clone -b dev https://<username>:<password>@git.company.com/scm/vmcc/opensrc.git --depth 1
Cloning into 'opensrc'...
remote: Counting objects: 2390, done.
remote: Compressing objects: 100% (1546/1546), done.
fatal: write error: File too large68), 1012.13 MiB | 15.38 MiB/s
fatal: fetch-pack: invalid index-pack output
```

This is because the files in this repository are too large, exceeding the AIX limit on user file resource usage.

This can be checked using `ulimit -a`. More information about the `ulimit` command can be found at [ulimit Command](https://www.ibm.com/docs/en/aix/7.1?topic=u-ulimit-command)

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

We can see that `file` has an upper limit of 2097151. Changing this to `unlimited` should solve the problem.

The `limits` file `/etc/security/limits` is accessible by the root user (ordinary users do not have access permissions).

```bash
# The following is part of the content of this file

default:
        fsize = 2097151
        core = 2097151
        cpu = -1
        data = -1
        rss = 65536
        stack = 65536
        nofiles = 2000
```

Changing `fsize = 2097151` to `fsize = -1` removes the file size limit. After making this change, **log in again** for the changes to take effect.

Executing `ulimit -a` again shows that the change has taken effect.

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

Now `file(blocks)` is `unlimited`. Let's try `git clone` again.

```bash
git clone -b dev https://<username>:<password>@git.company.com/scm/vmcc/opensrc.git --depth 1
Cloning into 'opensrc'...
remote: Counting objects: 2390, done.
remote: Compressing objects: 100% (1546/1546), done.
remote: Total 2390 (delta 763), reused 2369 (delta 763)
Receiving objects: 100% (2390/2390), 3.80 GiB | 3.92 MiB/s, done.
Resolving deltas: 100% (763/763), done.
Checking out files: 100% (3065/3065), done.
```

Success!