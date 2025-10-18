---
title: How to Set Up NFS Sharing and Mount on Different Platforms—Windows/Linux/Unix
summary: This article introduces the steps and commands for setting up NFS sharing and mounting it on different platforms (Windows/Linux/Unix).
tags:
  - NFS
  - Shell
  - Jenkins
date: 2019-09-10
authors:
  - shenxianpeng
---

For example, I have a shared repository for code that's very large (over 20G).  Each product build requires this repository's code (copying third-party libraries from it). If everyone needs to `git clone` this third-party repository, the network overhead is very large, `git clone` takes a long time, and it occupies a lot of physical space.

This can be solved by using NFS sharing.

Additionally, I want this code repository to update automatically. This introduces Jenkins. It checks for code commits to this large repository and automatically executes `git pull` to update the latest code to the shared server.


What is NFS? NFS (Network File System) is a type of file system supported by FreeBSD that allows computers on a network to share resources. In NFS applications, local NFS clients can transparently read and write files located on a remote NFS server, just like accessing local files.  On Windows, this is commonly known as a share.

## Setting Up NFS

```bash
# For example, on Linux, the shared server's IP is 192.168.1.1
sudo vi /etc/exports

# The following is the configuration of my exports file
# Assume the internal network IP range is 192.168.1.1 ~ 192.168.1.250
# ro means read-only
# all_squash means regardless of the user using NFS, their identity will be limited to a specified ordinary user identity (nfsnobody)
/agent/workspace/opensrc 192.168.1.*(ro,all_squash)
/agent/workspace/opensrc dev-team-a*.com(ro,all_squash)
/agent/workspace/opensrc dev-team-b*.com(ro,all_squash)
/agent/workspace/opensrc dev-ci*(ro,all_squash)
```

## NFS Operations

### Starting the NFS Service

To start the NFS service, you need to start both the `portmap` and `nfs` services.  `portmap` must be started before `nfs`.

```bash
service portmap start
service nfs start
# Check portmap status
service portmap status
```

### Checking Service Status

```bash
service nfs status
```

### Stopping the Service

```bash
service nfs stop
```

### Exporting Configuration

After changing the `/etc/exports` configuration file, you don't need to restart the NFS service; use `exportfs` directly.

```bash
sudo exportfs -rv
```

## Mounting on Different Platforms

### Windows

```bash
# Install the NFS Client (Services for NFS)
# Step 1: Open Programs and Features
# Step 2: Click Turn Windows features on or off
# Step 3: Find and check option Services for NFS
# Step 4: Once installed, click Close and exit back to the desktop. refer to https://graspingtech.com/mount-nfs-share-windows-10/
$ mount -o anon 192.168.1.1:/agent/workspace/opensrc Z:
```

### Linux/Unix

```bash
# Linux
sudo mount -t nfs 192.168.1.1:/agent/workspace/opensrc /agent/workspace/opensrc

# AIX
sudo nfso -o nfs_use_reserved_ports=1     # should only first time mount need to run this command
sudo mount -F nfs 192.168.1.1:/agent/workspace/opensrc /agent/workspace/opensrc

# HP-UX
sudo mount -F nfs 192.168.1.1:/agent/workspace/opensrc /agent/workspace/opensrc

# Solaris-SPARC
# If you can't execute mount directly from the command line
sudo /usr/sbin/mount -F nfs 192.168.1.1:/agent/workspace/opensrc /agent/workspace/opensrc
```