---
title: Docker 常用命令
summary: |
  一个 Docker 常用命令小纸条，记录一些常用的 Docker 命令和操作，方便日常使用和参考。
tags:
  - Docker
  - DevOps
translate: false
date: 2019-12-02
aliases:
  - /2019/12/docker-commands/
authors:
  - shenxianpeng
---

> Docker 常用命令小纸条

## Docker start|stop|restart

```bash
# 查看 Docker 版本
docker -v # or docker --version
# 重启 docker
sudo systemctl restart docker.service
# 停止 docker
sudo systemctl stop docker.service
# 启动 docker
sudo systemctl start docker.service
```



## Docker run

我们通过 docker 的两个参数 -i -t，让 docker 运行的容器实现"对话"的能力：

```bash
docker run -i -t ubuntu:15.10 /bin/bash
```

## Login Artifactory

注意：Open Source 版本 Artifactory 不支持 Docker，需要下载 [JFrog Container Registry](https://jfrog.com/container-registry/) 或是 Artifactory 企业版。

```bash
docker login -u <USER_NAME> -p <USER_PASSWORD> devasvm.dev.org.com:<REPOSITORY_PORT>
```

```bash
-sh-4.2$ sudo docker login devasvm.dev.org.com:8040
Username: admin
Password:
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
```

把 Docker image 推送到远程仓库

```bash
// docker tag SOURCE_IMAGE[:TAG] devasvm.dev.org.com:8040/docker-local/IMAGE[:TAG]
-sh-4.2$ sudo docker tag ubuntu:15.10 devasvm.dev.org.com:8040/docker-local/ubuntu:15.10

// docker push devasvm.dev.org.com:8040/docker-local/IMAGE[:TAG]
-sh-4.2$ sudo docker push devasvm.dev.org.com:8040/docker-local/ubuntu:15.10
The push refers to repository [devasvm.dev.org.com:8040/docker-local/ubuntu]
98d59071f692: Pushed
af288f00b8a7: Pushed
4b955941a4d0: Pushed
f121afdbbd5d: Pushed
15.10: digest: sha256:a3f5e428c0cfbfd55cffb32d30b1d78fedb8a9faaf08efdd9c5208c94dc66614 size: 1150
```

## TODO

更多 Docker 常用命令记录到这里。
