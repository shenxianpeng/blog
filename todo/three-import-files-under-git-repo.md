---
title: Git 仓库下三个重要的以 . 开头的文件
tags:
  - Git
categories:
  - Git
date: 2020-05-23 15:44:05
author: shenxianpeng
---

## .gitignore

在一个 Git 仓库下，你可以通过 `git add filename` 命令将你想要文件进行添加，然后通过 `git commit` 来提交到远程 Git 仓库。但是，总有一些文件是你不想提交到远程 Git 仓库，尤其是当你不小心执行了 `git add .` 命令时就会意外的将这些不想提交的文件提交远程 Git 仓库，这是 `.gitignore` 文件派上用场的地方，通过 `.gitignore` 文件可以告诉 Git 哪些文件应该被忽略，执行 `git status` 命令时不会出现你的工作区里。


### 什么类型的文件应该被忽略

* log 文件
* 带有 API keys/secrets, credentials或敏感信息的文件
* 无用的系统文件，例如 macOS 上的 `.DS_Store`
* 生成的文件，比如 `dist` 文件夹
* 比如用 IDE 打开项目时在根目录生成的 `.vscode` 等等






