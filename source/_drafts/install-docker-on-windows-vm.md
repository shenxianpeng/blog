---
title: Install Docker Desktop on Windows Virtual machine
tags:
  - Windows
  - Desktop
categories:
  - Docker
author: shenxianpeng
date: 2022-02-26 14:41:18
---

I need to install Docker Desktop on Windows VM. but I have many problems as following.

For examples:

Error1: Hyper-V cannot be installed: the processor does not have required virtualization capabilities.

Error2: System.InvalidOperationException:
Failed to deploy distro docker-desktop to C:\Users\xshen\AppData\Local\Docker\wsl\distro: exit code: -1
 stdout: Copyright (c) Microsoft Corporation. All rights reserved.

So, please follow the following steps you will install Docker Desktop on your Windows VM successully

* Uninstall Docker and WSL 2 kernel
* Go to the Control Panel -> Programs -> Turn Windows features on or off
* Uncheck the following: Containers, Hyper-V, Windows Subsystem for Linux
* Restart the system
* Install Docker without the WSL2 enabled/checked in the first screen
* Go to the Control Panel -> Programs -> Turn Windows features on or off
* Turn on/check the Windows Subsystem for Linux
* Restart the system.
* Do not install the WSL2 Kernel when reinstalling Docker.

I was not able to launch the Ubuntu WSL initially (got the same error messages in the first post), I then ran "wsl --update" and was able to launch the Ubuntu WSL and got Docker started running again.

```powershell
Enable-WindowsOptionalFeature -Online -FeatureName $("VirtualMachinePlatform", "Microsoft-Windows-Subsystem-Linux")
```

Refrence links:

* Failed to deploy distro docker-desktop https://github.com/docker/for-win/issues/8204
* System.InvalidOperationException: Failed to deploy distro docker-desktop https://github.com/docker/for-win/issues/7208
* How to enable Hyper-V https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v

---

![ ](https://github.com/shenxianpeng/shenxianpeng.github.io/blob/master/about/index/qrcode.jpg?raw=true)

关注公众号「DevOps攻城狮」

（转载本站文章请注明作者和出处，请勿用于任何商业用途）
