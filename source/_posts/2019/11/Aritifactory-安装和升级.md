---
title: Aritifactory 安装和升级
tags:
  - Aritifactory
categories:
  - Aritifactory
date: 2019-11-10 17:52:58
author: shenxianpeng
---

## 介绍

如果您还不了解 Aritifactory，请参看 [中文官网](https://www.jfrogchina.com/) 以及 [English Website](https://jfrog.com/artifactory/)

## 安装 Aritifactory 到 Linux

1. 从官网下载 Open Source [Artifactory](https://jfrog.com/open-source/#artifactory)，点击 Download RPM 下载
2. 将下载好的 jfrog-artifactory-oss-6.14.0.rpm 上传到你的 Linux 上

```bash
# 在根目录创建一个文件，你也可以在任何目录创建文件夹
sudo mkdir /artifactory
cd /artifactory
# 将下载好的 jfrog-artifactory-oss-6.15.0.rpm 上传到你的 Linux 上
$ ls
jfrog-artifactory-oss-6.14.0.rpm
# 安装 artifactory
sudo rpm -ivh jfrog-artifactory-oss-6.14.0.rpm
```

## Artifactory 服务启动和关闭

```bash
# 启动服务
sudo systemctl start artifactory.service
# 停止服务
sudo systemctl stop artifactory.service
# 查看服务状态
sudo systemctl status artifactory.service
```

## 访问 Artifactory

* artifactory 默认端口是8040，安装成功后访问：`http://hostname:8040`

## Artifactory 升级

1. 从官网下载最新的 [Artifactory](https://jfrog.com/open-source/#artifactory)

2. 将下载好的 jfrog-artifactory-oss-6.15.0.rpm（目前最新）上传到你的 Linux 上

```bash
cd /artifactory
ls
jfrog-artifactory-oss-6.14.0.rpm  jfrog-artifactory-oss-6.15.0.rpm
# 停止服务
sudo systemctl stop artifactory.service
# 进行升级
sudo rpm -U jfrog-artifactory-oss-6.15.0.rpm
# 输出日志，显示升级成功
warning: jfrog-artifactory-oss-6.15.0.rpm: Header V4 DSA/SHA1 Signature, key ID d7639232: NOKEY
Checking if ARTIFACTORY_HOME exists
Removing tomcat work directory
Removing Artifactory's exploded WAR directory
Initializing artifactory service with systemctl...

************ SUCCESS ****************
The upgrade of Artifactory has completed successfully.

Start Artifactory with:
> systemctl start artifactory.service

Check Artifactory status with:
> systemctl status artifactory.service

NOTE: Updating the ownership of files and directories. This may take several minutes. Do not stop the installation/upgrade process.
```

## 更多资料

* [JFrog 在线视频](https://www.jfrogchina.com/resources/upcoming-webinars/)
* [与 Jenkins 流水线一起工作](https://www.jfrog.com/confluence/display/RTF/Working+With+Pipeline+Jobs+in+Jenkins)
