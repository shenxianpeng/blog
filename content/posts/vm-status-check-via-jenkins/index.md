---
title: 这也能用Jenkins？快速实现一个定期批量登录远程虚拟机并支持添加新的主机名称的Job
summary: 本文介绍了如何使用 Jenkins 实现定期批量登录远程虚拟机，并支持用户添加新的主机名称，提供了完整的实现代码和步骤。
tags:
  - Shell
  - Jenkins
translate: false
date: 2020-06-13
author: shenxianpeng
---

## 背景

实现定期批量登录远程虚拟机然后进行一些指定的操作，还支持用户添加新的 hostname。



## 需求分解

通过一个简单的 shell 脚本可实现定期进行 ssh 登录操作，但如何实现的更优雅一些就需要花点时间了，比如：

1. 定期自动执行
2. 输出比较直观的登录测试结果
3. 支持用户添加新的虚拟机 hostname 到检查列表中
4. 执行完成后，通知用户等等

希望在不引入其他 Web 页面的情况下通过现有的工具 Jenkins 使用 Shell 脚本如何实现呢？

1. 写一个脚本去循环一个 list 里所有的 hostname，经考虑这个 list 最好是一个 file，这样方便后续处理。
2. 这样当用户通过执行 Jenkins job 传入新的 hostname 时，使用新的 hostname 到 file 里进行 grep，查看是否已存在。
3. 如果 grep 到，不添加；如果没有 grep 到，将这个 hostname 添加到 file 里。
4. 将修改后的 file 添加到 git 仓库里，这样下次 Jenkins 的定时任务就会执行最近添加的 hostname 了。

## 实现重点

1. 使用 `expect`。在使用 ssh 连接远程虚拟机的时候需要实现与远程连接时实现交互，例如：可以期待屏幕上的输出，然后进而进行相应的输入。在使用 `expect` 之前需要先安装，以 Redhat 的安装命令为例： `sudo yum install expect` 来进行安装。

    > 更多有关 `expect` 使用的可以参看这个连接：http://xstarcd.github.io/wiki/shell/expect.html

2. 使用了 Shell 数组。使用 Shell 读取文件数据，进行登录操作，将操作失败的记录到一个数组里，然后打印出来。

3. 在通过 Jenkins 提交新的 hostname 到 Git 仓库时，origin 的 URL 需要是 `https://${USERNAME}:${PASSWORD}@git.company.com/scm/vmm.git` 或 `git@company.com:scm/vmm.git`（需要提前在执行机器上生成了 id_rsa.pub）

> 代码已经上传 GitHub 请参看 https://github.com/shenxianpeng/vmm.git

## 最终效果

### 开始执行，提供输入新的 hostname

![Bulid with parameters](pipeline-start.png)

### 执行完成，将执行结果归档以便查看

![VM 检查结果](pipeline-result.png)

### 打开归档结果如下

```bash
#####################################################
######### VM login check via SSH results ############
#####################################################
#                                                   #
# Compelted (success) 14/16 (total) login vm check. #
#                                                   #
# Below 2 host(s) login faied, need to check.       #
#                                                   #
      abc.company.com
      xyz.company.com
#                                                   #
#####################################################
```

## 最后

现在技术的更新非常快，尤其作为 DevOps 工程师，各种工具层出不穷，想要每一样工具都掌握几乎是不可能的。

只会工具不了解其背后的原理，等到新工具出现替换掉旧的工具，其实这些年是没有进步的。

只有认真的把在工作中遇到的每个问题背后来龙去脉去搞懂，才能地基打的稳，这样不论工具怎么变，学习起来都会很快。

掌握操作系统，Shell，以及一门擅长的编程语言之后再去学习那些工具，要不永远都是漂浮在空中。
