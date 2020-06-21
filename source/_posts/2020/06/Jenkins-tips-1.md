---
title: Jenkins Tips 001：如何忽略 Shell 步骤中的故障？
tags:
  - Tips
  - Jenkins
categories:
  - Jenkins
date: 2020-06-21 21:42:17
author: shenxianpeng
---

![](Jenkins-tips-1/jenkins-tips.png)

## 问题

* 不希望 Shell 脚本因失败而中止
* 想一直运行 Shell 脚本并报告失败

## 解决

<!-- more -->

### 方法一

运行 Shell 时，你可以通过使用内置的 `+e` 选项来控制执行你的脚本错误。这可以禁用“非 0 退出”的默认行为

执行的时候如果出现了返回值为非零将会继续执行下面的脚本 

```bash
$ set +e
$ ls no-exit-file
$ whoami
```
![Jenkins Console Output](Jenkins-tips-1/1.png)

执行的时候如果出现了返回值为非零，整个脚本就会立即退出

```bash
$ set -e
$ ls no-exit-file
$ whoami
```
![Jenkins Console Output](Jenkins-tips-1/2.png)

### 方法二

还有一种方式，如果不想停止失败的另一种方法是添加 `|| true` 到你的命令结尾

```bash
# 做可能会失败，但并不关注失败的命令时
$ ls no-exit-file || true
```

![Jenkins Console Output](Jenkins-tips-1/3.png)

如果要在失败时执行某些操作则添加 `|| <doSomethingOnFailure>` 

```bash
# 做可能会失败的事情，并关注失败的命令
# 如果存在错误，则会创建变量 error 并将其设置为 true
$ ls no-exit-file || error=true

# 然后去判断 error 变量的值。如果为真，则退出 Shell
$ if [ $error ]
$ then 
$    exit -1
$ fi
```
![Jenkins Console Output](Jenkins-tips-1/4.png)

