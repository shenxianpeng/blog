---
title: 初识 JFrog Artifactory
tags:
  - Artifactory
  - JFrog
categories:
  - JFrog
date: 2019-11-10 17:52:58
author: shenxianpeng
---

## 什么是 Artifactory

Artifactory 是 JFrog 的一个产品，用作二进制存储库管理器。二进制存储库可以将所有这些二进制统一托管，从而使团队的管理更加高效和简单。

就跟你用 Git 一样，Git 是用来管理代码的，Artifactory 是用来管理二进制文件的，通常是指 jar, war, pypi, DLL, EXE 等 build 文件。

我觉得使用 Artifactory 的最大优势是创造了更好的持续集成环境，有助于其他持续集成任务去 Artifactory 里调用，再部署到不同的测试或开发环境，这对于实施 DevOps 至关重要。

<!-- more -->

如果想了解更多有关 Artifactory，请参看 [中文官网](https://www.jfrogchina.com/) 以及 [English Website](https://jfrog.com/artifactory/)。

## 安装 Artifactory

1. 从官网下载 Open Source [Artifactory](https://jfrog.com/open-source/#artifactory)，这里演示的是安装到 Linux，所以点击 Download RPM 下载
2. 将下载好的 jfrog-artifactory-oss-6.14.0.rpm 上传到 Linux 上

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

# 在使用上面的命令启动服务的时候遇到如下错误：
# Job for artifactory.service failed because a configured resource limit was exceeded. See "systemctl status artifactory.service" and "journalctl -xe" for details.
# 详情：https://www.jfrog.com/jira/browse/RTFACT-19988
# 可尝试如下命令启动
cd /opt/jfrog/artifactory/app/bin && ./artifactory.sh start &

# 停止服务
sudo systemctl stop artifactory.service
# 查看服务状态
sudo systemctl status artifactory.service
```

## 访问 Artifactory

Artifactory 默认端口是8040，安装成功后访问：`http://hostname:8040` 即可登录（默认用户名 admin 密码 password）
![Artifactory 首页](Artifactory-install-and-upgrade/homepage.png)

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

## Artifactory 卸载

1. 停止 Artifactory 服务

```bash
systemctl stop artifactory.service
```

2. 使用 root 用户执行 RPM uninstall 命令

```bash
# remove OSS version
yum erase jfrog-artifactory-oss
# remove PRO version, etc.
yum erase jfrog-artifactory-pro
```

更多关于 JFrog 产品的卸载，请看：https://www.jfrog.com/confluence/display/JFROG/Uninstalling+JFrog+Products

## 安装 JFrog CLI

```bash
# ON MAC
brew install jfrog-cli-go
# WITH CURL
curl -fL https://getcli.jfrog.io | sh
# WITH NPM
npm install -g jfrog-cli-go
# WITH DOCKER
docker run docker.bintray.io/jfrog/jfrog-cli-go:latest jfrog -v
```

CLI for JFrog Aritifactory

[如何在 Artifactory 上使用 JFrog CLI](https://www.jfrog.com/confluence/display/CLI/CLI+for+JFrog+Artifactory)
