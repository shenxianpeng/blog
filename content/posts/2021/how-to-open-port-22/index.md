---
title: 在 Windows 上开启 22 端口并让其处于监听状态
summary: |
  本文介绍如何在 Windows 上开启 22 端口并确保其处于监听状态，以便支持 SSH 连接。内容包括安装 OpenSSH 以及防火墙配置步骤。
tags:
  - OpenSSH
  - Windows
date: 2021-01-12
author: shenxianpeng
---

最近我们的 Bamboo 服务器在连接 Windows 构建机时出现错误：

```
Can not connect to the host XXXX 22 port.
```

登录到构建机后，通过以下命令检查 22 端口：

```bash
netstat -aon | findstr "22"
```

结果并没有发现 22 端口在监听。

---

## 1. 开放入站 22 端口

网上有很多关于在 Windows 上开放端口的文章，例如：
[How to open a port in Windows Firewall](https://www.windowscentral.com/how-open-port-windows-firewall)

---

## 2. 仍然无法监听的原因

我在防火墙中开放了 22 端口，但执行上面的命令依然看不到 22 端口处于监听状态。

原因是：**系统中没有运行 SSH 服务**。

---

## 3. 解决方法：安装 Win32-OpenSSH

我通过安装 [Win32-OpenSSH](https://github.com/PowerShell/Win32-OpenSSH) 解决了问题。

安装完成后会启动两个服务（SSH Server 和 SSH Agent），此时端口 22 就会处于监听状态。

安装步骤可参考官方 Wiki：
[Install Win32-OpenSSH](https://github.com/PowerShell/Win32-OpenSSH/wiki/Install-Win32-OpenSSH)

---

✅ **总结**

* 防火墙开放端口只是第一步，还需要确保有进程在监听该端口。
* 对于 SSH，必须运行 `sshd` 服务才能让 22 端口真正处于监听状态。
