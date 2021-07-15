---
title: Ubuntu 上使用 VPN
date: 2017-12-26 21:30:34
tags:
- Ubuntu
- VPN
categories:
- OS
---

如何在 Ubuntu 上连接 Cisco AnyConnect VPN

打开Terminal，执行：

```bash
sudo /sbin/modprobe tun
```

安装OpenConnect，执行:

```bash
sudo apt-get install openconnect
```

连接VPN，执行：

```bash
sudo openconnect yourvpn.example.com
```

将提示你输入用户名和密码，输入争取后，VPN连接成功。

原文 [请点击](http://ubuntuhandbook.org/index.php/2014/11/connect-cisco-anyconnect-vpn-ubuntu/) 。
