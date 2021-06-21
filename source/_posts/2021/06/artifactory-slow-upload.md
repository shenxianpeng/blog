---
title: 关于 Artifactory 上传制品变得非常缓慢，偶尔失败的问题分享
tags:
  - Artifactory
categories:
  - Troubleshooting
date: 2021-06-16 23:44:59
author: shenxianpeng
---

最近在我使用 Artifactory Enterprise 遇到了上传制品非常缓慢的问题，在经过与 IT，Artifactory 管理员一起合作终于解决这个问题，在此分享一下这个问题的解决过程。

如果你也遇到类似或许有所帮助。

## 问题描述

最近发现通过 Jenkins 往 Artifactory 里上传制品的时候偶尔出现上传非常缓慢的情况，尤其是当一个 Jenkins stage 里有多次上传，往往会在第二次上传的时候出现传输速度极为缓慢（KB/s ）。

## 问题排查和解决

我的构建环境和 Jenkins 都没有任何改动，所有的构建任务都出现了上传缓慢的情况，为了排除可能是使用 Artifactory plugin 的导致原因，通过 curl 命令来进行上传测试，也同样上传速度经常很慢。

那么问题就在 Artifactory 上面。

1. 是 Artifactory 最近升级了？
2. 还是 Artifactory 最近修改了什么设置？
3. 也许是 Artifactory 服务器的问题？

在跟 Artifactory 管理员进行了沟通之后，排除了以上 1，2 的可能。为了彻底排除是 Artifactory 的问题，通过 scp 进行拷贝的时候同样也出现了传输速度非常慢的情况，这问题就出现在网络上了。

这样需要 IT 来帮助排查网络问题了，最终 IT 建议更换网卡进行尝试（因为他们之前有遇到类似的情况），但这种情况会有短暂的网络中断，不过最终还是得到了管理者的同意。

幸运的是在更换网卡之后，Jenkins 往 Artifactory 传输制品的速度恢复了正常。

## 总结

处理次事件的一点点小小的总结：

由于这个问题涉及到几个团队，为了能够快速推进，此时明确说明问题，推测要有理有据，以及该问题导致了什么样的严重后果（比如影响发布）才能让相关人重视起来，否则大家都等着，没人回来解决问题。

当 Artifactory 管理推荐使用其他数据中心 instance，建议他们先尝试更换网卡；如果问题没有得到解决，在同一个数据中心创建另外一台服务器。如果问题还在，此时再考虑迁移到其他数据中心instance。这大大减少了作为用户去试错所带来的额外工作量。