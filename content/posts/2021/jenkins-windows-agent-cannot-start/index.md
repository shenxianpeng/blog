---
title: Jenkins 升级后 Windows Agent 无法启动的解决方法
summary: |
  本文介绍 Jenkins 升级后 Windows Agent 无法启动的问题，以及通过更新 Windows Slaves 插件和修改配置文件来解决的步骤。
tags:
  - Jenkins
date: 2021-02-11
aliases:
  - /2021/02/jenkins-windows-agent-cannot-start/
authors:
  - shenxianpeng
---

## 问题描述

在将团队的 Jenkins 从 **2.235.1** 升级到 **2.263.3** 后，发现 **Windows Agent 无法启动**，日志报错如下：

```log
[windows-agents] Installing the Jenkins agent service
ERROR: Unexpected error in launching an agent. This is probably a bug in Jenkins
java.lang.NullPointerException
    at hudson.os.windows.ManagedWindowsServiceLauncher.launch(ManagedWindowsServiceLauncher.java:298)
```

该问题已在 Jenkins Jira 上有反馈：

* [JENKINS-63198](https://issues.jenkins.io/browse/JENKINS-63198)
* [Windows Support Updates](https://www.jenkins.io/blog/2020/07/23/windows-support-updates/)

---

## 解决步骤

### 1. 更新 Windows Slaves 插件

将 [windows-slaves-plugin](https://github.com/jenkinsci/windows-slaves-plugin) 升级到 **1.7** 版本（支持 Jenkins 2.248+）。

更新后，如果仍出现如下错误：

```log
ERROR: Unexpected error in launching an agent. This is probably a bug in Jenkins
org.jinterop.dcom.common.JIException: Unknown Failure
    at org.jvnet.hudson.wmi.Win32Service$Implementation.start(Win32Service.java:149)
```

请继续执行下一步。

---

### 2. 修改 `jenkins-agent.exe.config`

找到 Jenkins agent 安装目录下的 `jenkins-agent.exe.config` 文件，注释或删除以下行：

```xml
<!-- <supportedRuntime version="v2.0.50727" /> -->
```

确保配置如下：

```xml
<configuration>
  <runtime>
    <generatePublisherEvidence enabled="false"/>
  </runtime>
  <startup>
    <supportedRuntime version="v4.0" />
  </startup>
</configuration>
```

> 如果存在 `jenkins-slave.exe.config` 文件，也需同样修改。

---

### 3. 检查 .NET Framework 版本

如果启动时提示：

```
.NET Framework 2.0 or later is required on this computer to run a Jenkins agent as a Windows service
```

则需要升级本机的 **.NET Framework**。
可参考：[更新 .NET Framework](https://shenxianpeng.github.io/2020/07/jenkins-windows-agent-connect-problem/)

---

## 总结

通过 **更新插件** + **修改配置文件** + **升级 .NET Framework**，即可解决 Jenkins 升级后 Windows Agent 无法启动的问题。
