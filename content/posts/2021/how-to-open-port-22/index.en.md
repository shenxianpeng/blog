---
title: How to open port 22 and make it listening on Windows
summary: |
  This article explains how to open port 22 on Windows and ensure it is listening, which is necessary for SSH connections. It includes steps to install OpenSSH and configure the firewall.
tags:
  - OpenSSH
  - Windows
date: 2021-01-12
authors:
  - shenxianpeng
---

Recently our Bamboo server has an error when connecting to the Windows build system.

Some errors like: Can not connect to the host XXXX 22 port.

I log into the build machine find port 22 with the below command

```bash
netstat -aon|findstr "22"
```

but not found port 22 is inbound.


## Inbound port 22

There's a lot of articles will tell you how to open ports on Windows. see this one

https://www.windowscentral.com/how-open-port-windows-firewall

## But still not works for me

My problem is when I inbound port 22, execute the above command still can't see the port 22 is listening.

So I install the [Win32-OpenSSH](https://github.com/PowerShell/Win32-OpenSSH), this will lanch two services, then port 22 is listening.

Here are the wiki page about download and installation https://github.com/PowerShell/Win32-OpenSSH/wiki/Install-Win32-OpenSSH
