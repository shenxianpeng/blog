---
title: 创建 NuGet Organization 的遇到的坑
summary: 本文记录了在创建 NuGet Organization 时遇到的问题和解决方法，特别是关于公司邮箱地址的使用。
tags:
  - NuGet
author: shenxianpeng
date: 2023-08-25
---

其实创建包管理平台账户没什么可说的，但最近准备在 https://www.nuget.org 上面发布产品前创建 Organization 的时候确遇到了问题。

## 事情是这样的

作为一名公司员工在首次打开 NuGet 网站 (www.nuget.org) 的时候，点击【Sign in】，映入眼帘的就是【Sign in with Microsoft】，点击，下一步、下一步，我就顺利的就用公司邮箱注册了我的第一个 NuGet 的账户。

此时我准备创建一个 Organization 的时候，输入自己的公司邮箱提示这个邮箱地址已经被使用了，What ？？？

OK。那我就填写同事的公司邮箱地址吧。

同事在收到邮件通知后也是一步步操作，先是打开 NuGet.org，点击【Sign in with Microsoft】，然后也是需要填写自己的账户名，结果完成这一系列的操作之后，再输入他的邮件地址去注册 Organization 的时候也同样提示这个邮箱已经被使用了？？？什么操作！！！醉了...


## 如何解决的

就在这千钧一发焦急得等待发布之际，我突然灵机一动，以死马当活马医的心态，将我注册的 NuGet 的个人账户绑定的公司邮箱修改为了自己的 Gmail 邮箱，然后此时再去创建 Organization 的时候输入的是自己的公司邮箱，创建 Organization 成功了！！

好了，谨以此记录一下在注册 NuGet 时候遇到的问题。不知道对你是否有用，如果真的有帮助到你，举手示意一下哦。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
