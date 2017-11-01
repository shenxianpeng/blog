---
title: Hello Git
date: 2017-07-08 16:26:15
tags: Git
---

Welcome to [git](https://git-scm.com) world! Here is sample demo post. Check [documentation](https://git-scm.com/docs) for more info.

## Quick Start

#### Getting a Git Repository

``` bash
$ git clone https://github.com/shenxianpeng/shenxianpeng.github.io.git
```

#### Git Status

``` bash
$ git-status - Show the working tree status
```

#### Git Add

``` bash
$ git-add - Add file contents to the index
```

#### Git Commit

``` bash
$ git-commit - Record changes to the repository
```

#### Git Push

``` bash
$ git-push - Update remote refs along with associated objects
```

#### Git Tag

``` bash
$ git tag -a v1.0.1 -m "Relase v1.0.1"  - create tag
$ git push origin -tags                 - push tag to remote repository
$ git tag -d v1.0.1                     - delete tag
$ git push origin :refs/tags/v1.0.1     - delete remote tag
$ git tag                               - view tag
```

#### Git Branch

``` bash
$ git branch deploy                     - create a branch named deploy
$ git checkout deploy                   - switch to deploy branch
```