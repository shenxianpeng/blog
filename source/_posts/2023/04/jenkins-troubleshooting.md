---
title: Jenkins agent service can not start automatically on Windows even the Startup type is Automatic
tags:
  - Pipeline
  - Troubleshooting
categories:
  - Jenkins
author: shenxianpeng
date: 2023-04-11 03:49:13
---

## Issue

My Windows build machine is regular reboot after Windows updates, but my Jenkins agent service on this Windows can not
start automatically even I have set the startup type to Automatic.

![](jenkins-troubleshooting/service-general.png)

## Solution

After some research, select "Allow service to interact with desktop" with service properties on Log On tab can fix this problem.

In service properties -> Log On -> Select "Local System account" and select the checkbox for "Allow service to interact with desktop"
![](jenkins-troubleshooting/service-log-on.png)

Reference is [HERE](https://stackoverflow.com/questions/41210060/even-after-installing-jenkins-as-a-windows-service-i-have-to-start-it-through-c).

## Semi-automatic setup of Jenkins Agent on Windows

By the way, if you want to set a jenkins agent as service on Windows more easier, you can use this [project](https://github.com/shenxianpeng/win-jenkins-agent) to semi-automatic setup.

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
