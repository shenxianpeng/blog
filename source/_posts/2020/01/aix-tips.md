---
title: aix-tips
tags:
  - UNIX
  - AIX
categories:
  - UNIX
date: 2020-01-09 09:55:26
author: shenxianpeng
---

## 在 AIX 上无法解压超一个大约 600 MB 文件

```bash
bash-4.3$ ls
data_cdrom_debug_AIX_05949fb.tar.Z
bash-4.3$ gzip -d data_cdrom_debug_AIX_05949fb.tar.Z
gzip: data_cdrom_debug_AIX_05949fb.tar: File too large
bash-4.3$ sudo vi /etc/security/limits

default:
        fsize = -1 # 修改为 -1
        core = 2097151
        cpu = -1
        data = -1
        rss = 65536
        stack = 65536
        nofiles = 2000

# 需要重启
bash-4.3$ sudo reboot

Rebooting . . .

```

修改之后，重启，再解压就没有问题了。
