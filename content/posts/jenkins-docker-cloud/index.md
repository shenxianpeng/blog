---
title: 如何使用 Jenkins Docker Cloud
summary: |
  本文介绍如何使用 Jenkins Docker Cloud 来构建和部署应用，包括配置 Docker 主机以及创建自定义 Docker 镜像。
tags:
  - Cloud
  - Docker
author: shenxianpeng
date: 2025-01-25
---

最近我在进行 Jenkins 实例迁移，这次我选择使用 **Jenkins Docker Cloud**，而不是在 Jenkinsfile 中直接使用 `docker { ... }`。

## Jenkins Docker Cloud 插件

首先，你需要安装 Jenkins Docker Cloud 插件：  
https://plugins.jenkins.io/docker-plugin/

Jenkins Docker Cloud 是一个允许 Jenkins 使用 Docker 容器作为构建节点的插件。

所以，你需要配置一个启用 **Remote API** 的 Docker 主机，如下所示。

---

### 启用 Docker Remote API

Jenkins Controller 通过 REST API 连接到 Docker 主机。  
启用 Docker 主机的远程 API，请按照以下步骤操作：

**Step 1**：启动一个虚拟机并安装 Docker。你可以根据所使用的 Linux 发行版，参考官方文档进行安装。确保 Docker 服务已启动并正常运行。

**Step 2**：登录服务器，打开 Docker 服务文件 `/lib/systemd/system/docker.service`，找到 `ExecStart` 这一行，并替换为：

```bash
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:4243 -H unix:///var/run/docker.sock
````

**Step 3**：重新加载并重启 Docker 服务：

```bash
systemctl daemon-reload
service docker restart
```

**Step 4**：执行以下命令验证 API 是否可用（将 `myhostname` 替换为主机名或 IP 地址）：

```bash
curl http://localhost:4243/version
curl http://myhostname:4243/version
```

---

### 创建自定义 Docker 镜像

我在使用自定义 Docker 镜像时，选择了 [launch via JNLP](https://plugins.jenkins.io/docker-plugin/#plugin-content-launch-via-jnlp)。

如果你的镜像基于 [jenkins/inbound-agent](https://hub.docker.com/r/jenkins/inbound-agent)，可以参考以下 Dockerfile：

```Dockerfile
FROM jenkins/inbound-agent
RUN apt-get update && apt-get install XXX
COPY your-favorite-tool-here

ENTRYPOINT ["/usr/local/bin/jenkins-agent"]
```

---

### 在 Jenkinsfile 中使用

当 Docker Cloud 配置完成后，你就可以在 Jenkinsfile 中像普通 agent 一样使用它，例如：

```groovy
// Jenkinsfile (Declarative Pipeline)
pipeline {
    agent {
        node {
            "docker"
        }
    }
}
```

这种方式和直接使用 `docker { ... }` 是不同的。
例如直接在 Jenkinsfile 中使用 `docker { ... }`：

```groovy
// Jenkinsfile (Declarative Pipeline)
pipeline {
    agent {
        docker { image 'node:22.13.1-alpine3.21' }
    }
    stages {
        stage('Test') {
            steps {
                sh 'node --eval "console.log(process.platform,process.env.CI)"'
            }
        }
    }
}
```

更多关于在 Pipeline 中使用 Docker 的内容，请参考：
[https://www.jenkins.io/doc/book/pipeline/docker/](https://www.jenkins.io/doc/book/pipeline/docker/)

---

如有疑问，欢迎留言交流。

---

转载本文请注明作者与出处，禁止商业用途。欢迎关注公众号「DevOps攻城狮」。