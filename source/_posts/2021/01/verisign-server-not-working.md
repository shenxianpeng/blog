---
title: 解决 InstallShield 默认时间戳服务器 http://timestamp.verisign.com/scripts/timstamp.dll 不可用
tags:
  - InstallShield
  - Build
categories:
  - DevOps
date: 2021-01-06 09:35:41
author: shenxianpeng
---

## 问题和解决办法

相信很多 Build Engineer 在编译Windows build 时候很多时候会用到 InstallShield ，这是一个收费的数字签名工具，最近（我注意到是在 2020.1.4 日）我的 InstallShield 签名出现错误

![](verisign-server-not-working/failed.png)

究其原因就是它默认的时间戳服务器，出现了无法访问的情况。

`Http://timestamp.verisign.com/scripts/timstamp.dll`

尝试去替换一个新的时间戳服务器后，例如：

`http://timestamp.globalsign.com/scripts/timstamp.dll`

InstallShield 签名恢复正常。

## 是否有影响

虽然能工作正常了，到底这个改变会不会影响到产品的发布？InstallShield 给出了替换默认时间戳网址的办法，并且没有提到有任何影响，因此不会对原有的签名有任何影响。

## 替换旧时间戳

具体如何替换，请参考官方的这篇文章 [Changing the Timestamp Server for Digital Signatures](https://docs.revenera.com/installshield25helplib/helplibrary/SettingsXML-Timestamp.htm)


最后：

如果你只有一两处在使用这个时间戳网址，并且需要发布版本，果断替换掉原来的时间戳网址，

如果你有一些列的构建机器和构建脚本都需要相应的修改，建议再等等看原有的时间戳服务器能否恢复正常。
