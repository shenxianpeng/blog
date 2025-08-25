---
title: Most Useful Linux Command-Line Tricks
summary: This article introduces some of the most useful Linux command-line tricks to improve development and operation efficiency.
tags:
  - Linux
date: 2020-02-05
author: shenxianpeng
---

## ls Command

Lists files and folders in the current directory. Parameters:

`-l` Lists details when listing.

`-a` Shows all files, including hidden and unhidden ones.



They can be combined, like this:

```bash
ls -la
```

## cp Command

Copies the source file to the target. Parameters:

`-i` Interactive mode means waiting for confirmation if the target file will be overwritten.

`-r` Recursive copy, meaning including subdirectories (if any).

```bash
cp –ir source_dir target_dir
```

## What to Do When /tmp Space is Insufficient

Add a line in the `/etc/fstab` file:

```bash
sudo vi /etc/fstab
# Add the following line
tmpfs                   /tmp                    tmpfs   defaults,size=4G          0 0
```

After restarting, check with `df -h`. The `/tmp` directory will have become 4G.

More, Refer to these links

* https://likegeeks.com/main-linux-commands-easy-guide/
* https://dzone.com/articles/most-useful-linux-command-line-tricks