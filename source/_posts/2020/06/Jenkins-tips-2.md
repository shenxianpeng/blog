---
title: 《Jenkins Tips 002》 如何把 Shell 返回的数据处理为数组
tags:
  - Tips
  - Jenkins
categories:
  - Jenkins
date: 2020-06-22 14:37:29
author: shenxianpeng
---

> Jenkins Tips —— 每期用简短的图文描述一个 Jenkins 小技巧。

![](Jenkins-tips-1/jenkins-tips.png)

## 问题

需要对 Linux 上不同的数据文件通过 Jenkins 给不同的人发送邮件，需要将数据变成数组，然后通过循环把他们发给指定的用户。

```bash
# Example
$ ls
fail-list-user1.txt  fail-list-user2.txt  fail-list-user3.txt
```
假如要对以上文件分别进行分送邮件给用户 user1，user2，user3 如何处理呢？

初步的想法就是通过一些 Shell 表达式只 `list` 出 user1 user2 user3，将它返回给 Jenkins Pipeline。然后通过 groovy 语法对 Shell 传回的字符串进行 `split`，从而处理成数组。

## 解决

<!-- more -->

### Shell 截取字符串

对原文件的名字通过 Shell 进行处理。

```bash
# list 所有以 fail-list 开头的文件，并赋给一个数组 l
l=$(ls -a fail-list-*)

for f in $l; 
do 
  f=${f#fail-list-} # 使用#号截取左边字符
  f=${f%.txt}       # 使用%号截取右边字符
  echo $f           # 最终输出仅包含 user 的字符串
done
```

测试结果如下：

```bash
sxp@localhost MINGW64 /c/workspace/test (master)
$ ls
fail-list-user1.txt  fail-list-user2.txt  fail-list-user3.txt

sxp@localhost MINGW64 /c/workspace/test (master)
$ l=$(ls -a fail-list-*) && for f in $l; do f=${f#fail-list-}; f=${f%.txt}; echo $f ; done;
user1
user2
user3
```

### Groovy 处理 Shell 返回

```groovy
// 将 Shell 返回字符串赋给 owners 这个变量。注意在 $ 前面需要加上 \ 进行转义。
def owners = sh(script: "l=\$(ls -a fail-list-*) && for f in \$l; do f=\${f#fail-list-}; f=\${f%.txt}; echo \$f ; done;", returnStdout:true).trim()

// 查看 owners 数组是否为空，isEmpty() 是 groovy 内置方法。
if ( ! owners.isEmpty() ) {
  // 通过 .split() 对 owners string 进行分解，返回字符串数组。然后通过 .each() 对返回的字符串数组进行循环。
  owners.split().each { owner ->
    // 打印最终的用户返回
    println "owner is ${owner}"

    // 发送邮件，例子
    email.SendEx([
        'buildStatus'  : currentBuild.currentResult,
        'buildExecutor': "${owner}",
        'attachment'   : "fail-list-${owner}.txt"
    ])
  }
}
```

最终完成了通过 Groovy 将 Shell 返回的字符串，处理成字符数组，实现上述例子中需要对不同人进行邮件通知的需求。

希望以上的例子对你做类似需求的时候有所启示和帮助。
