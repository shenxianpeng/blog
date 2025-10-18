---
title: Jenkins Linux Agent 配置
summary: |
  本文提供了 Jenkins Linux Agent 的逐步配置指南，包括 Java 运行时的准备、节点创建以及常见问题的排查方法。
date: 2019-05-12
tags:
  - Jenkins
  - Jenkins
authors:
  - shenxianpeng
---

## 准备 Java 运行时

### 检查是否已安装 Java

```bash
$ java -version
openjdk version "1.8.0_65"
OpenJDK Runtime Environment (build 1.8.0_65-b17)
OpenJDK 64-Bit Server VM (build 25.65-b01, mixed mode)
```

#### 如果未安装，可参考 [这篇文章](https://www.javahelps.com/2015/03/install-oracle-jdk-in-ubuntu.html) 进行安装

---

## 创建节点

### 1. 在 Jenkins 首页进入

**Manage Node → New Node**，例如创建 `window-build-machine`

---

### 2. Linux Agent 设置示例

| 项目                             | 配置                                         |
| ------------------------------ | ------------------------------------------ |
| Name                           | Linux-build-machine                        |
| Description                    | 用于 Linux 构建                                |
| # of executors                 | 1                                          |
| Remote root directory          | /home/agent                                |
| Labels                         | Linux, build                               |
| Usage                          | 尽可能多地使用此节点                                 |
| Launch method                  | 通过 SSH 启动 Agent                            |
| Host                           | 192.168.1.112                              |
| Credentials                    | username/password                          |
| Host Key Verification Strategy | Manually trusted key Verification Strategy |
| Availability                   | 尽可能保持此 Agent 在线                            |

---

### 3. 凭据配置

| 凭据项         | 配置                                |
| ----------- | --------------------------------- |
| Domain      | Global credentials (unrestricted) |
| Kind        | Username with password            |
| Scope       | Global (Jenkins、nodes、items 及其子项) |
| Username    | root                              |
| Password    | mypassword                        |
| Description | Linux agent 用户名和密码                |

---

### 4. 保存并连接

示例日志：

```log
Remoting version: 3.29
This is a Unix agent
Evacuated stdout
Agent successfully connected and online
SSHLauncher{host='192.168.1.112', port=22, credentialsId='d1cbab74-823d-41aa-abb7-8584859503d0', jvmOptions='', javaPath='/usr/bin/java',
prefixStartSlaveCmd='', suffixStartSlaveCmd='', launchTimeoutSeconds=210, maxNumRetries=10, retryWaitTime=15,
sshHostKeyVerificationStrategy=hudson.plugins.sshslaves.verifiers.ManuallyTrustedKeyVerificationStrategy, tcpNoDelay=true, trackCredentials=true}
[05/11/19 01:33:37] [SSH] Opening SSH connection to 192.168.1.112:22.
[05/11/19 01:33:37] [SSH] SSH host key matches key seen previously for this host. Connection will be allowed.
[05/11/19 01:33:37] [SSH] Authentication successful.
[05/11/19 01:33:37] [SSH] The remote user's environment is:
```

---

## 常见问题排查

| 问题                                                                                  | 解决方法                                                                                                                                             |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `[SSH] WARNING: No entry currently exists in the Known Hosts file for this host...` | 执行 `ssh-keyscan HOSTNAME >> known_hosts`                                                                                                         |
| `/var/lib/jenkins/.ssh/known_hosts [SSH] No Known Hosts file was found...`          | 在 **Launch method** 中将 Host key verification strategy 从 "Known Hosts file verification strategy" 改为 "Manually trusted key verification strategy" |
