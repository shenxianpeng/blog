---
title: 通过 NFS 和 Jenkins 来共享和同步第三方库代码
tags:
  - NFS
  - Linux
  - Jenkins
categories:
  - Shell
date: 2019-09-10 22:38:47
author: shenxianpeng
---

最近遇到这样一个需求，我们有一个共享仓库的代码所在用的空间非常大（超过 20 G），在每个产品构建时候都需要用到这个仓库的代码（从里面 copy 第三方库），如果每个人都要 git clone 这个第三方仓库，一是网络开销非常大，二是 git clone 时间长，三是占用大量的物理空间。

这里通过 NFS 和 Jenkins 来解决。

什么是 NFS？NFS（Network File System）即网络文件系统，是 FreeBSD 支持的文件系统中的一种，它允许网络中的计算机之间共享资源。在 NFS 的应用中，本地 NFS 的客户端应用可以透明地读写位于远端 NFS 服务器上的文件，就像访问本地文件一样，Windows 上俗称共享。

Jenkins 不必多说，用它主要是来监测如果这个容量巨大的仓库有代码提交就自动执行 git pull 操作，更新最近的代码到共享服务器上。

## 设置 NFS 及 启动命令

```bash
# 例如在 Linux 上, 共享服务器的 ip 是 192.168.1.1
sudo vi /etc/exports

# 以下是我的 exports 文件的配置
# 假设内网 ip 是这样的区间 192.168.1.1 ~ 192.168.1.250
# ro 表示只读
# all_squash 表示不管使用 NFS 的用户是谁，他的身份都会被限定成为一个指定的普通用户身份(nfsnobody)
/agent/workspace/opensrc 192.168.1.*(ro,all_squash)

# 启动 NFS 服务，需要启动portmap和nfs两个服务，并且portmap一定要先于nfs启动;
service portmap start
service nfs start
# 查看 portmap 状态
service portmap status
# 查看 NFS 状态
service nfs status
# 停止 NFS 服务
service nfs stop

# 当改变/etc/exports配置文件后，不用重启 NFS 服务直接用这个 exportfs 即可
sudo exportfs -rv
```

## 挂载到不同 UNIX 平台

```bash
# Linux
sudo mount -t nfs 192.168.1.1:/agent/workspace/opensrc /agent/workspace/opensrc

# AIX
sudo nfso -o nfs_use_reserved_ports=1     # should only first time mount need to run this command
sudo mount -F nfs 192.168.1.1:/agent/workspace/opensrc /agent/workspace/opensrc

# HP-UX
sudo mount -F nfs 192.168.1.1:/agent/workspace/opensrc /agent/workspace/opensrc

# Solaris-SPARC
# 如果你不能直接在命令行执行 mount
sudo /usr/sbin/mount -F nfs 192.168.1.1:/agent/workspace/opensrc /agent/workspace/opensrc
```
