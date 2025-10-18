---
title: How to use Jenkins Docker Cloud
summary: |
  This article explains how to use Jenkins Docker Cloud for building and deploying applications, including setting up a Docker host and creating custom Docker images.
tags:
  - Cloud
  - Docker
authors:
  - shenxianpeng
date: 2025-01-25
---

Recently, I am working on Jenkins instance migration, this time I started to use Jenkins Docker Cloud insead of use `docker { ... }` in Jenkinsfile.

## Jenkins cloud plugin

First you need to install Jenkins Docker Cloud plugin https://plugins.jenkins.io/docker-plugin/

Jenkins Docker Cloud is a plugin that allows Jenkins to use Docker containers as build agents.

So you need to config a Docker Host with remote API as follows.



### Enable Docker Remote API

Jenkins controller connects to the docker host using REST APIs. To enable the remote API for docker host, please follow the steps below.

Step 1: Spin up a VM, and install docker on it. You can follow the official documentation for installing docker. based on the Linux distribution you use. Make sure the docker service is up and running.

Step 2: Log in to the server and open the docker service file `/lib/systemd/system/docker.service`. Search for `ExecStart` and replace that line with the following.

```bash
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:4243 -H unix:///var/run/docker.sock
```

Step 3: Reload and restart docker service.

```bash
systemctl daemon-reload
service docker restart
```

Step 4: Validate API by executing the following curl commands. Replace myhostname with your hostname or IP.

```bash
curl http://localhost:4243/version
curl http://myhostname:4243/version
```

### Create custom docker image

For me, I use [launch via JNLP](https://plugins.jenkins.io/docker-plugin/#plugin-content-launch-via-jnlp) for my custom docker image.

For example, you docker image is based on [jenkins/inbound-agent](https://hub.docker.com/r/jenkins/inbound-agent), you can use the following Dockerfile to create your custom image.

```Dockerfile
FROM jenkins/inbound-agent
RUN apt-get update && apt-get install XXX
COPY your-favorite-tool-here

ENTRYPOINT ["/usr/local/bin/jenkins-agent"]
```

### How to use in Jenkinsfile

Once you have configed Docker Cloud, you can use it in Jenkinsfile like a normal agent.

For example:

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

Which is does not like if you use `docker { ... }` directly.

For example of using `docker { ... }`:

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

Here is more details about using Docker with pipeline: https://www.jenkins.io/doc/book/pipeline/docker/

Feel free to comment if you have any questions.

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
