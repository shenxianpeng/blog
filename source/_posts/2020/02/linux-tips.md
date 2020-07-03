---
title: 最有用的 Linux 命令行技巧
tags:
  - Linux
categories:
  - LinuxUnix
date: 2020-02-05 22:34:27
author: shenxianpeng
---

## ls 命令

列出当前目录的文件和文件夹。参数:

`-l` 列出时显示详细信息

`-a` 显示所有文件，包括隐藏的和不隐藏的

<!-- more -->

可以组合使用，像这样

```bash
ls -la
```

## cp 命令

将源文件复制到目标。参数：

`-i` 交互模式意味着等待确认，如果目标上有文件将被覆盖。

`-r` 递归复制，意味着包含子目录（如果有的话）。

```bash
cp –ir source_dir target_dir
```

## /tmp 空间不够怎么办

在 /etc/fstab 文件里增加一行

```bash
sudo vi /etc/fstab
# 添加如下一行
tmpfs                   /tmp                    tmpfs   defaults,size=4G          0 0
```

重启之后，`df -h` 查看，/tmp 目录已经就变成 4G 了。

More, Refer to these links

* https://likegeeks.com/main-linux-commands-easy-guide/
* https://dzone.com/articles/most-useful-linux-command-line-tricks
