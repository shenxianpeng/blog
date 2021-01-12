---
title: git sparse-checkout enable and disable
tags:
  - Git
categories:
  - Git
date: 2021-01-11 15:03:45
author: shenxianpeng
---

This post just a note to myself and it works on my environment. it has not been widely tested.

## Enable git sparse-checkout

Just in my case, I cloned a git repo exists problems on the Windows platform with some folder, in order to work on the Windows platform we get a work around solution as following:

Case 1: when you not already cloned a repository

```bash
$ mkdir git-src
$ cd git-src
$ git init
$ git config core.sparseCheckout true
$ echo "/assets/" >> .git/info/sparse-checkout
$ git remote add origin git@github.com:shenxianpeng/shenxianpeng.git
$ git fetch
$ git checkout master
```

```bash
Case 2: when you already cloned a repository
$ cd git-src
$ git config core.sparseCheckout true
$ echo "/assets/" >> .git/info/sparse-checkout
$ rm -rf <other-file/folder-you-dont-need>
$ git checkout
```

## Disable git sparse-checkout

```bash
$ git config core.sparseCheckout false
$ git read-tree --empty
$ git reset --hard
```
