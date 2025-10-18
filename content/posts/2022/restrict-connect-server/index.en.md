---
title: Restrict others from login your important Linux machine
summary: |
  This article explains how to restrict access to a critical Linux machine by modifying the `/etc/security/access.conf` file, allowing only specific users to log in.
tags:
  - Linux
authors:
  - shenxianpeng
date: 2022-09-16
---

If you have a critical machine like your team's CI server that runs on Linux, so you don't want every members in your group to access it.

Modifying this setting `/etc/security/access.conf` on Linux can do it.

## How to setup

I commented out the access settings for TEAM A, and add some user accounts can access.

```bash
#+ : (SRV_WW_TEAM_A_CompAdmin) : ALL
+ : shenx, map, xiar : ALL
```



**Be careful not to restrict everyone including yourself.**

It would be best to allow several people can also access it to prevent any issues to log in with your account or you leave the organization.

## Let's test

Then when I try to use another account not in the list to access this machine and the connection shows closed.

```bash
$ ssh test@devciserver.organization.com
test@devciserver.organization.com's password:
Connection closed by 10.84.17.119 port 22
```

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
