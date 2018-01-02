---
title: Ubuntu下使用VPN
date: 2017-12-26 21:30:34
tags: ubuntu
---

如何在Ubuntu上连接Cisco AnyConnect VPN

1. 打开Terminal，执行：
```
$ sudo /sbin/modprobe tun
```

2. 安装OpenConnect，执行:
```
$ sudo apt-get install openconnect
```

3.连接VPN，执行：
```
sudo openconnect yourvpn.example.com
```

将提示你输入用户名和密码，输入争取后，VPN连接成功。

原文[请点击](http://ubuntuhandbook.org/index.php/2014/11/connect-cisco-anyconnect-vpn-ubuntu/)