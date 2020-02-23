---
title: HP-UX 安装工具以及一些使用总结
tags:
  - UNIX
  - HP-UX
categories:
  - UNIX
date: 2020-02-05 10:28:37
author: shenxianpeng
---


## 安装 Java8

安装包下载链接是 https://h20392.www2.hpe.com/portal/swdepot/displayProductInfo.do?productNumber=JDKJRE8018

需要先注册，然后登陆后才能下载，我下载的是 `Itanium_JDK_8.0.18_June_2019_Z7550-96733_java8_18018_ia.depot`

在线安装文档 https://support.hpe.com/hpesc/public/docDisplay?docId=emr_na-c04481894

```bash
swinstall -s /tmp/Itanium_JDK_8.0.18_June_2019_Z7550-96733_java8_18018_ia.depot

# if swinstall not found
/usr/sbin/swinstall -s /tmp/Itanium_JDK_8.0.18_June_2019_Z7550-96733_java8_18018_ia.depot
```

安装成功后，会在根目录 opt 下多了一个 java8 目录，检查下 java 版本：

```bash
bash-5.0$ pwd
/opt/java8
bash-5.0$ cd bin
bash-5.0$ java -version
java version "1.8.0.18-hp-ux"
Java(TM) SE Runtime Environment (build 1.8.0.18-hp-ux-b1)
Java HotSpot(TM) Server VM (build 25.18-b1, mixed mode)
```

创建软连接

```bash
sudo ln -s /opt/java8/bin/java /bin/java
```

## 安装 gzip 和 gunzip

```bash
# 安装 gzip
/usr/bin/sudo /usr/local/bin/depothelper gzip
```

如果你机器上已经有 zip 和 gunzip 了，只需要软连接一下即可，防止出现命令找不到的问题

```bash
/usr/bin/sudo ln -s /usr/contrib/bin/gzip /usr/bin/gzip
/usr/bin/sudo ln -s /usr/contrib/bin/gunzip /usr/bin/gunzip
```