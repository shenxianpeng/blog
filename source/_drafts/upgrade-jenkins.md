---
title: Jenkins 升级指南
tags:
  - DevOps
  - Jenkins
categories:
  - Jenkins
date: 2021-02-01 12:57:32
author: shenxianpeng
---

在谈到为什么要升级 Jenkins 之前，我们需要先了解 Jenkins 的两个版本线：分别是稳定版和定期版（每周）。

稳定版：也叫长期支持(Long-Term Support，简写LTS) 是每 12 周从定期发布流中选择的。他们会每4周发布一个稳定的版本，其中包括bug和安全修复的备份。了解更多…

定期版：

```log
[2021-01-30 23:53:40] [windows-agents] Connecting to devbw01.dev.software.com
Checking if Java exists
java -version returned 11.0.2.
[2021-01-30 23:53:47] [windows-agents] Copying jenkins-agent.xml
[2021-01-30 23:53:48] [windows-agents] Copying agent.jar
[2021-01-30 23:53:48] [windows-agents] Starting the service
ERROR: Unexpected error in launching an agent. This is probably a bug in Jenkins
org.jinterop.dcom.common.JIException: Unknown Failure
	at org.jvnet.hudson.wmi.Win32Service$Implementation.start(Win32Service.java:149)
Caused: java.lang.reflect.InvocationTargetException
	at sun.reflect.GeneratedMethodAccessor219.invoke(Unknown Source)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.kohsuke.jinterop.JInteropInvocationHandler.invoke(JInteropInvocationHandler.java:140)
Also:   java.lang.Throwable: launched here
```

Change `jenkins-agent.exe.config` file. remove or comment out this line `<supportedRuntime version="v2.0.50727" />`

> also do this for `jenkins-slave.exe.config` in case it exists.

then your config file will be like this

```xml
<configuration>
  <runtime>
    <!-- see http://support.microsoft.com/kb/936707 -->
    <generatePublisherEvidence enabled="false"/>
  </runtime>
  <startup>
    <!-- this can be hosted either on .NET 2.0 or 4.0 -->
    <!-- <supportedRuntime version="v2.0.50727" /> -->
    <supportedRuntime version="v4.0" />
  </startup>
</configuration>
```

Back to works

```log
[2021-01-31 00:05:01] [windows-agents] Connecting to devbw01.dev.software.com
Checking if Java exists
java -version returned 11.0.2.
[2021-01-31 00:05:02] [windows-agents] Copying jenkins-agent.xml
[2021-01-31 00:05:02] [windows-agents] Copying agent.jar
[2021-01-31 00:05:02] [windows-agents] Starting the service
[2021-01-31 00:05:02] [windows-agents] Waiting for the service to become ready
[2021-01-31 00:05:13] [windows-agents] Connecting to port 64,271
<===[JENKINS REMOTING CAPACITY]===>Remoting version: 4.5
This is a Windows agent
Agent successfully connected and online
Scheduled overwrite of jenkins-slave.exe on the next service startup
```
