---
title: Jenkins Linux agent configuration
date: 2019-05-12 19:49:20
tags:
- Jenkins
categories:
- Jenkins
author: shenxianpeng
---

## Prepare Java runtime

### Check if had installed java

```bash
$ java -version
openjdk version "1.8.0_65"
OpenJDK Runtime Environment (build 1.8.0_65-b17)
OpenJDK 64-Bit Server VM (build 25.65-b01, mixed mode)
```

#### if not Here is an [article](https://www.javahelps.com/2015/03/install-oracle-jdk-in-ubuntu.html) telling you how to install it

## Create Node

### 1. Jenkins home page->Manage Node->New Node, such as window-build-machine

#### 2. List Linux agent settings

| Items | Settings |
|---|---|
| Name | Linux-build-machine |
| Description | used for Linux build |
| of executors | 1 |
| Remote root directory | /home/agent |
| Labels | Linux, build |
| Usage | Use this node as much as possible  |
| Launch method| Launch agent agents via SSH |
| Host | 192.168.1.112 |
| Credentials | username/password|
| Host Key Verification Strategy | Manually trusted key Verification Strategy |
| Availability | Keep this agent online as much as paossible |

#### 3. How to set credentials

| credentials | configuration |
|---|---|
| Domain | Global credentials (unrestricted) |
| Kind | Username with password |
| Scope | Global(Jenkins, nodes, items, all child items, etc) |
| Username | root |
| Password | mypassword |
| Description | Linux agent username & password |

#### 4. Save then Connect

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

## Troubleshooting

| Problem  | how to fix |
|---|---|
| [04/22/19 23:15:07] [SSH] WARNING: No entry currently exists in the Known Hosts file for this host. Connections will be denied until this new host and its associated key is added to the Known Hosts file. | ssh-keyscan HOSTNAME >> known_hosts |
| /var/lib/jenkins/.ssh/known_hosts [SSH] No Known Hosts file was found at /var/lib/jenkins/.ssh/known_hosts. | changing the Host key verification strategy in LAUNCH METHOD from "Known Hosts file verification strategy" to "Manually trusted key verification strategy" |
