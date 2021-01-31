---
title: Jenkins upgrade issue "Windows agents won't start" workaround
tags:
  - Jenkins
categories:
  - Jenkins
date: 2021-02-11 16:09:06
author: shenxianpeng
---

Today, when I tried to upgrade my team's Jenkins server from Jenkins 2.235.1 to Jenkins 2.263.3, I met a problem that can not launch the Windows agent.

```
[2021-01-29 23:50:40] [windows-agents] Connecting to xxx.xxx.xxx.xxx
Checking if Java exists
java -version returned 11.0.2.
[2021-01-29 23:50:40] [windows-agents] Installing the Jenkins agent service
[2021-01-29 23:50:40] [windows-agents] Copying jenkins-agent.exe
ERROR: Unexpected error in launching an agent. This is probably a bug in Jenkins
Also: java.lang.Throwable: launched here
at hudson.slaves.SlaveComputer._connect(SlaveComputer.java:286)
at hudson.model.Computer.connect(Computer.java:435)
at hudson.slaves.SlaveComputer.doLaunchSlaveAgent(SlaveComputer.java:790)
...
...
at java.lang.Thread.run(Thread.java:748)
java.lang.NullPointerException
at hudson.os.windows.ManagedWindowsServiceLauncher.launch(ManagedWindowsServiceLauncher.java:298)
```

This issue had been raised in the Jenkins Jira project: [JENKINS-63198](https://issues.jenkins.io/browse/JENKINS-63198) and [JENKINS-63198](https://issues.jenkins.io/browse/JENKINS-63198)

There is also a Windows Support Updates guide [here](https://www.jenkins.io/blog/2020/07/23/windows-support-updates/) that mentioned this problem.

Finally, I fixed this problem by the following steps:

1. Update [windows-slaves-plugin](https://github.com/jenkinsci/windows-slaves-plugin) to the lastest version 1.7 (fixes for Jenkins 2.248+)

Then the error should be like this

```
[2021-01-30 23:53:40] [windows-agents] Connecting to xxx.xxx.xxx.xxx
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

2. Then change `jenkins-agent.exe.config` file. remove or comment out this line `<supportedRuntime version="v2.0.50727" />` as below

> also do this for `jenkins-slave.exe.config` in case it also exists.

```
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

3. Then try to Launch agent.

If it still does not work and has this error message ".NET Framework 2.0 or later is required on this computer to run a Jenkins agent as a Windows service", you need to upgrade your .NET Framework.

> Here is a [link](https://shenxianpeng.github.io/2020/07/jenkins-windows-agent-connect-problem/) for update .NET Framework.

Hopefully, this could help you to fix connect the issue of the Windows agent. Let me know in case of any questions.
