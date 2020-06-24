---
title: 《Jenkins Tips 002》 处理 Shell 返回的字符串成字符数组
tags:
  - Tips
  - Jenkins
categories:
  - Jenkins
date: 2020-06-22 14:37:29
author: shenxianpeng
---

> Jenkins Tips —— 每期用简短的图文描述一个 Jenkins 小技巧。

![](Jenkins-tips-2/jenkins-tips.png)

## 问题

想要把 Linux 上不同的文本数据通过 Jenkins 发送邮件给不同的人。

## 思路

想通过 Shell 先对数据进行处理，然后返回到 Jenkins pipeline 里，但只能得到 Shell 返回的字符串，因此需要在 Jenkinsfile 里把字符串处理成数组，然后通过一个 for 循环对数组中的值进行处理。

以下是要处理的文本数据：

```bash
# Example
$ ls
fail-list-user1.txt  fail-list-user2.txt  fail-list-user3.txt
```
要将以上文件通过 Jenkins 分别进行处理，得到用户 user1，user2，user3 然后发送邮件。

## 解决

<!-- more -->

### 字符串截取

通过 Shell 表达式只过滤出 user1 user2 user3

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
$ ls
fail-list-user1.txt  fail-list-user2.txt  fail-list-user3.txt
$ l=$(ls -a fail-list-*) && for f in $l; do f=${f#fail-list-}; f=${f%.txt}; echo $f ; done;
user1
user2
user3
```

### 处理字符串为数组

以下在 Jenkinsfile 使用 groovy 将 Shell 返回的字符串处理成字符数组。

```groovy
// Jenkinsfile 
// 忽略 stage, steps 等其他无关步骤
...

scripts {
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
}
```

最终完成了通过 Groovy 将 Shell 返回的字符串处理成字符数组，实现上述例子中对不同人进行邮件通知的需求。

希望以上例子对你做其他类似需求的时候有所启示和帮助。
