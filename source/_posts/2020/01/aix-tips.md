---
title: AIX 上安装工具以及一些使用总结
tags:
  - UNIX
  - AIX
categories:
  - LinuxUnix
date: 2020-01-09 09:55:26
author: shenxianpeng
---

记录在使用 AIX 时所遇到的问题和解决办法，以备以后遇到同样问题不要再因为这些再浪费时间，希望也能帮助到你。

<!-- more -->

## 在 AIX 上无法解压超一个大约 600 MB 文件

```bash
bash-4.3$ ls
data_cdrom_debug_AIX_05949fb.tar.Z
bash-4.3$ gzip -d data_cdrom_debug_AIX_05949fb.tar.Z
# 错误信息
gzip: data_cdrom_debug_AIX_05949fb.tar: File too large
# 解决办法
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

## 安装 Java Standard Edition on AIX

下载地址 https://developer.ibm.com/javasdk/support/aix-download-service/

1. download Java8_64.sdk.8.0.0.600.tar.gz Java8_64.jre.8.0.0.600.tar.gz
2. gzip -d Java8_64.sdk.8.0.0.600.tar.gz and Java8_64.jre.8.0.0.600.tar.gz
3. tar -xvf Java8_64.sdk.8.0.0.600.tar  and Java8_64.jre.8.0.0.600.tar
4. installp -agXYd .  Java8_64.jre Java8_64.sdk 2>&1 | tee installp.log

```bash
# install output
Installation Summary
--------------------
Name                        Level           Part        Event       Result
-------------------------------------------------------------------------------
Java8_64.sdk                8.0.0.600       USR         APPLY       SUCCESS
Java8_64.jre                8.0.0.600       USR         APPLY       SUCCESS
Java8_64.jre                8.0.0.600       ROOT        APPLY       SUCCESS
```

5. smitty install_all
6. Input: Type "./" in the field
7. Acceptance Install the Agreement, then start install.

Troubleshooting

```bash
bash-4.4# ./java -version
Error: Port Library failed to initialize: -70
Error: Could not create the Java Virtual Machine.
Error: A fatal exception has occurred. Program will exit.
```
