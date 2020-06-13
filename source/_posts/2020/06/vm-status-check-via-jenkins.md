---
title: 快速实现一个定期检查虚拟机状态并给用户提供新增查询的功能
tags:
  - Shell
  - Jenkins
categories:
  - DevOps
date: 2020-06-13 03:34:28
author: shenxianpeng
---

## 背景

为了解决一些重要但不常用的虚拟机在长时间不登陆会被系统认定为暂不使用，导致被关闭，当再次使用的时候需要请求管理员进行开启这种麻烦的操作。

需要一个脚本来实现定期进行登录，并执行简单的命令，从而让系统判定这些虚拟机是活跃的，从而达到不对它进行关闭操作。

## 需求分析

从背景来看，通过一个简单的 shell 脚本定期进行 ssh 登录操作就可以实现了，但如何实现的更优雅一些就需要花点时间了。

想象中的优雅：

1. 定期自动执行
2. 输出比较直观的登录测试结果
3. 支持用户添加新的虚拟机 hostname 到检查列表中
4. 执行完成后，通知用户等等。

希望在不引入其他 Web 页面的情况下通过现有的工具（Jenkins）使用 Shell 脚本和 Pipeline 去实现。

## 需求分解

1. 写一个脚本去循环一个 list 里所有的 hostname，经考虑这个 list 最好是一个 file，这样方便后续处理。
2. 这样当用户通过执行 Jenkins job 传入新的 hostname 时，用心的 hostname 到 file 里进行 grep
3. 如果 grep 到，不添加。如果没有 grep 到，把这个 hostname 添加到 file 里。
4. 将这个修改后的 file 添加到 git 仓库里，这样下次 Jenkins 的定时任务就会执行最近添加的 hostname 了。

## 代码实现

详细代码请参看 https://github.com/shenxianpeng/vmm.git

## 最终结果

### 开始执行，提供输入新的 hostname

![](vm-status-check-via-jenkins/pipeline-start.png)

### 执行完成，将执行结果归档以便查看

![](vm-status-check-via-jenkins/pipeline-result.png)

### 查看归档结果如下

```
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

