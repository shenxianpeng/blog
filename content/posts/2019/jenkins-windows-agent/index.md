---
title: Jenkins Windows Agent 配置
summary: |
  本文提供 Jenkins Windows Agent 的详细配置步骤，包括 Java 运行时准备、节点创建以及常见问题的排查方法。
date: 2019-05-12
tags:
  - Jenkins
  - Jenkins
authors:
  - shenxianpeng
---

## 准备 Java 运行时

### 1. [下载 Java](https://www.java.com/en/download/)

---

### 2. 配置 Windows 系统环境变量

```bash
JAVA_HOME=C:\Program Files\Java\jdk1.8.0_201
CLASSPATH=.;%JAVA_HOME%\lib;%JAVA_HOME%\jre\lib
```

---

## 创建节点

### 1. 在 Jenkins 首页进入

**Manage Node → New Node**，例如创建 `window-build-machine`

---

### 2. Windows Agent 设置示例

| 项目                      | 配置                                 |
| ----------------------- | ---------------------------------- |
| Name                    | window-build-machine               |
| Description             | 用于 Windows 构建                      |
| # of executors          | 1                                  |
| Remote root directory   | C:\agent                           |
| Labels                  | windows, build                     |
| Usage                   | 尽可能多地使用此节点                         |
| Launch method           | 让 Jenkins 以 Windows 服务的方式控制此 Agent |
| Administrator user name | .\Administrator                    |
| Password                | mypassword                         |
| Host                    | 192.168.1.111                      |
| Run service as          | 使用上述 Administrator 账户              |
| Availability            | 尽可能保持此 Agent 在线                    |

---

### 3. 保存并连接

```bash
[windows-slaves] Connecting to 192.168.1.111
Checking if Java exists
java -version returned 1.8.0.
[windows-slaves] Copying jenkins-slave.xml
[windows-slaves] Copying slave.jar
[windows-slaves] Starting the service
[windows-slaves] Waiting for the service to become ready
<===[JENKINS REMOTING CAPACITY]===>Remoting version: 3.29
This is a Windows agent
Agent successfully connected and online
```

---

## 常见问题排查

### 1. `ERROR: Message not found for errorCode: 0xC00000AC`

需要安装 JDK，并配置 JAVA 环境变量。

---

### 2. 添加 Windows 节点作为服务时报错

参考 [JENKINS-16418](https://issues.jenkins-ci.org/browse/JENKINS-16418)。

---

### 3. `org.jinterop.dcom.common.JIException: Message not found for errorCode: 0x00000005`

修复以下注册表项权限：

1. `HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Wow6432Node\CLSID{72C24DD5-D70A-438B-8A42-98424B88AFB8}`
2. `HKEY_CLASSES_ROOT\CLSID{76A64158-CB41-11D1-8B02-00600806D9B6}`

步骤：

* 打开 `regedit`（以管理员身份），找到对应注册表项
* 修改所有者为 **Administrators** 组，并赋予 **完全控制** 权限
* 将所有者改回 **NT Service\TrustedInstaller**
* 重启 **Remote Registry Service**

---

### 4. `ERROR: Unexpected error in launching an agent`

1. 登录远程机器，在服务中找到 `jenkinsslave-C__agent`
2. 启动类型设为 **Automatic**
3. **Log On** 选择 **This account** 并输入正确账号密码
4. 启动服务

---

### 5. `errorCode: 0x800703FA`

Agent 使用域账号运行时，在组策略中：

* 打开 `gpedit.msc`
* **计算机配置 → 管理模板 → 系统 → 用户配置文件**
* 启用 **Do not forcefully unload the user registry at user logoff**

---

### 6. `errorCode: 0xC0000001 ... Failed to connect`

需要启用 SMB1：

1. 打开 **启用或关闭 Windows 功能**
2. 勾选 **SMB 1.0/CIFS File Sharing Support**
3. 确认并重启

---

### 7. `.NET Framework 2.0 or later is required`

升级 .NET Framework，参考 [这篇文章](https://shenxianpeng.github.io/2020/07/jenkins-windows-agent-connect-problem/)。

---

### 8. 更多 Windows Agent 连接问题

参考：[https://github.com/jenkinsci/windows-slaves-plugin/blob/master/docs/troubleshooting.adoc](https://github.com/jenkinsci/windows-slaves-plugin/blob/master/docs/troubleshooting.adoc)
