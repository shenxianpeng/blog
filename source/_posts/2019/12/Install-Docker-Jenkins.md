---
title: Install Docker Jenkins
tags:
  - Jenkins
  - Docker
categories:
  - Jenkins
date: 2019-12-01 15:17:39
author: shenxianpeng
---

## 安装 Jenkins Docker 版

在 CentOS 上安装 Docker 版 Jenkins，这里推荐用 Long-term Support (LTS) 版本，可以从 Jenkins 官网[下载](https://jenkins.io/download/)。

```bash
# 下载指定 lts 版本 2.130
sudo docker pull jenkins/jenkins:2.130
# 运行指定 docker Jenkins
sudo docker run -p 8080:8080 -p 50000:50000 jenkins/jenkins:2.130
# 如果想下载最新的 lts 版
sudo docker pull jenkins/jenkins:lts
# 运行最新的 lts 版 docker Jenkins
sudo docker run -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
```

### 访问 http://hostname:8080/ 即可访问

### 获取登录密码

```bash
# 列出来所有 image
sudo docker image list
# 进入容器
sudo docker exec -it 39bc7a8307d9 /bin/bash
# 或是
sudo docker ps
a6195912b579
sudo docker exec -it a6195912b579 /bin/bash
# 查看默认 admin 密码
jenkins@a6195912b579:/$ cat /var/jenkins_home/secrets/initialAdminPassword
5193d06c813d46d3b18babeda836363a
```

登录之后，可以修改 admin 密码，方便下次登录。

### 将宿主机目录映射到 Jenkins Docker 中

我想把搭建在宿主机上的 Jenkins 替换为 Docker Jenkins。我在宿主机上 /data/backup 目录下有我的 Jenkins 定期备份，想恢复到我的新创建的 Docker Jenkins 中。

* 首先需要将宿主机的 /data/backup 目录映射到 Jenkins Docker 的目录上
* 然后将备份的内容恢复到 Docker Jenkins，然后再做个镜像

```bash
sudo docker run -p 8080:8080 -p 50000:50000 --name mydata -v /data/backup:/home/backup jenkins/jenkins:2.130
# 映射成功，可以看到宿主机上的备份文件了
jenkins@c85db3f88115:/home/backup$ ls
FULL-2019-09-14_02-00  FULL-2019-09-28_02-00  FULL-2019-10-19_02-00  FULL-2019-11-02_02-00  FULL-2019-11-23_02-00
FULL-2019-09-21_02-00  FULL-2019-10-05_02-00  FULL-2019-10-26_02-00  FULL-2019-11-09_02-00  FULL-2019-11-30_02-00
```

在 Docker Jenkins 上下载 ThinBackup 这个插件
