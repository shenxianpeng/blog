---
title: Aritifactory 安装
tags:
  - Aritifactory
categories:
  - Aritifactory
date: 2019-11-10 17:52:58
author: shenxianpeng
---

## 介绍

如果您还不了解 Aritifactory，请参看 [中文官网](https://www.jfrogchina.com/) 以及 [English Website](https://jfrog.com/artifactory/)

## 安装到 Linux

```bash
# 这里安装的是 artifactory open source https://jfrog.com/open-source/#artifactory

# 在根目录创建一个文件，你也可以在任何目录创建文件夹
sudo mkdir /artifactory
cd /artifactory

# 下载安装文件，这是我当前用的下载链接，如果失效请到这里找最新下载链接 https://jfrog.com/open-source/#artifactory
wget https://akamai.bintray.com/d1/d1f325dfa559e719e3f4b7e70ad5b8c8ac34fcd83bb20e2a3eaebafadcc2bcb6?__gda__=exp=1572935113~hmac=4c3fa4def65ac39f279e2f9c66c669a1abaa991d08c5cd1c2bc8e1a4b52e39fb&response-content-disposition=attachment%3Bfilename%3D%22jfrog-artifactory-oss-6.14.0.rpm%22&response-content-type=application%2Foctet-stream&requestInfo=U2FsdGVkX1-fi3Llt13PyUudcmJCXrWwiucmtMEVB3bZjZWS1PsbNWow-t4u_1mgnvU8R2dKmLUN7gfhchB7MSRbUIkRL3eOdYg7IpSlg1rNah5FqvLt0qFI6vPeBgBLEzkeBGiLK7M02pK92QwhGCdfc5EM-62AaiMe839oJ_Q&response-X-Checksum-Sha1=0653ddf2de53894517ac5bd65b8596c95390075c&response-X-Checksum-Sha2=d1f325dfa559e719e3f4b7e70ad5b8c8ac34fcd83bb20e2a3eaebafadcc2bcb6
# 将下载后的文件重命名为一个有意义的名字
mv d1f325dfa559e719e3f4b7e70ad5b8c8ac34fcd83bb20e2a3eaebafadcc2bcb6\?__gda__\=exp\=1572935113~hmac\=4c3fa4def65ac39f279e2f9c66c669a1abaa991d08c5cd1c2bc8e1a4b52e39fb jfrog-artifactory-oss-6.14.0.rpm
# 安装 artifactory
sudo rpm -ivh jfrog-artifactory-oss-6.14.0.rpm
```

## Artifactory 服务的启动和关闭

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

## 更多

* [JFrog 在线视频](https://www.jfrogchina.com/resources/upcoming-webinars/)
* [与 Jenkins 流水线一起工作](https://www.jfrog.com/confluence/display/RTF/Working+With+Pipeline+Jobs+in+Jenkins)
