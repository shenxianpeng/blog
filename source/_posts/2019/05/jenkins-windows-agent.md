---
title: Jenkins Windows agent configuration
date: 2019-05-12 18:39:59
tags:
- Jenkins
categories:
- Jenkins
author: shenxianpeng
---

## Prepare Java runtime

### 1. [Download Java](https://www.java.com/en/download/)

#### 2. Configure Java Windows path

```bash
JAVA_HOME=C:\Program Files\Java\jdk1.8.0_201
CLASSPATH=.;%JAVA_HOME%\lib;%JAVA_HOME%\jre\lib
```

## Create Node

### 1. Jenkins home page->Manage Node->New Node, such as window-build-machine

#### 2. List windows agent settings

| Items | Settings |
|---|---|
| Name | window-build-machine |
| Description | used for windows build |
| of executors | 1 |
| Remote root directory | C:\agent |
| Labels | windows, build |
| Usage | Use this node as much as possible  |
| Launch method| Let Jenkins control this Windows slave as a Windows service |
| Administrator user name | .\Administrator |
| Password | mypassword |
| Host | 192.168.1.111 |
| Run service as | Use Administrator account given above |
| Availability | Keep this agent online as much as paossible |

#### 3. Save then Connect

```bash
[2019-05-11 01:32:50] [windows-slaves] Connecting to 192.168.1.111
Checking if Java exists
java -version returned 1.8.0.
[2019-05-11 01:32:50] [windows-slaves] Copying jenkins-slave.xml
[2019-05-11 01:32:50] [windows-slaves] Copying slave.jar
[2019-05-11 01:32:50] [windows-slaves] Starting the service
[2019-05-11 01:32:50] [windows-slaves] Waiting for the service to become ready
[2019-05-11 01:32:55] [windows-slaves] Connecting to port 52,347
<===[JENKINS REMOTING CAPACITY]===>Remoting version: 3.29
This is a Windows agent
Agent successfully connected and online
```

## Troubleshooting

The following issues I met and how I fixed them.

### 1. ERROR: Message not found for errorCode: 0xC00000AC

You need need to install JDK, and config JAVA environment variable.

### 2. How to fix add windows node as Windows service error

Ref to [JENKINS-16418](https://issues.jenkins-ci.org/browse/JENKINS-16418).

### 3. org.jinterop.dcom.common.JIException: Message not found for errorCode: 0x00000005

Fixed permission for the following registry keys

1. HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Wow6432Node\CLSID{72C24DD5-D70A-438B-8A42-98424B88AFB8}
2. HKEY_CLASSES_ROOT\CLSID{76A64158-CB41-11D1-8B02-00600806D9B6}

Steps to fix it

* Open 'regedit' (as Administrator), Find (Ctrl+F) the registry key: "{72C24DD5-D70A-438B-8A42-98424B88AFB8}" in HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Wow6432Node\CLSID
* Right click and select 'Permissions', Change owner to administrators group (Advanced...).
* Change permissions for administrators group. Grant Full Control。
* Change owner back to TrustedInstaller (user is "NT Service\TrustedInstaller" on local machine)

Repeat the above steps to fix permission for HKEY_CLASSES_ROOT\CLSID{76A64158-CB41-11D1-8B02-00600806D9B6}

Finally, Restart Remote Registry Service (Administrative Tools / Services).

### 4. ERROR: Unexpected error in launching an agent

This is probably a bug in Jenkins.

1. Login remote machine and open Services find `jenkinsslave-C__agent`
2. Set startup type: Automatic
3. Log On: select This account, type correct account and password
4. start jenkinsslave-C__agent

### 5. Caused by: org.jinterop.dcom.common.JIRuntimeException: Message not found for errorCode: 0x800703FA

Slave under domain account, If your slave is running under a domain account and you get an error code 0x800703FA, change a group policy:

1. open the group policy editor (gpedit.msc)
2. go to Computer Configuration->Administrative Templates->System-> UserProfiles, "Do not forcefully unload the user registry at user logoff"
3. Change the setting from "Not Configured" to "Enabled", which disables the new User Profile Service feature ('DisableForceUnload' is the value added to the registry)

### 6. ERROR: Message not found for errorCode: 0xC0000001 Caused by: jcifs.smb.SmbException: Failed to connect: 0.0.0.0<00>/10.xxx.xxx.xxx

Need to enable SMB1

1. Search in the start menu for ‘Turn Windows features on or off’ and open it.
2. Find 'SMB1.0/CIFS File Sharing Support' in the list of optional features that appears, and select the checkbox next to it.
3. Click OK and Windows will add the selected feature.

You’ll be asked to restart your computer as part of this process.

### 6. more connect jenkins agent problem on windows

Please refer to this link https://github.com/jenkinsci/windows-slaves-plugin/blob/master/docs/troubleshooting.adoc
