---
title: 限制他人登录你的重要 Linux 服务器
summary: |
  本文介绍如何通过修改 `/etc/security/access.conf` 文件，限制只有特定用户可以登录关键的 Linux 服务器。
tags:
  - Linux
author: shenxianpeng
date: 2022-09-16
---

如果你有一台关键机器，例如团队的 CI 服务器，你可能不希望组内所有成员都能访问它。

在 Linux 中修改 `/etc/security/access.conf` 配置文件即可实现该限制。

---

## 配置方法

我将 **TEAM A** 的访问配置注释掉，并添加了允许访问的用户账号：

```bash
#+ : (SRV_WW_TEAM_A_CompAdmin) : ALL
+ : shenx, map, xiar : ALL
```

---

⚠ **注意不要把自己也锁在外面**

最好允许多个账号有权限登录，以防因账号问题或离开组织而无法访问服务器。

---

## 测试效果

当我使用不在名单中的账号尝试访问该机器时，连接会直接被关闭：

```bash
$ ssh test@devciserver.organization.com
test@devciserver.organization.com's password:
Connection closed by 10.84.17.119 port 22
```

---

转载本文请注明作者与出处，禁止商业用途。欢迎关注公众号「DevOps攻城狮」。
