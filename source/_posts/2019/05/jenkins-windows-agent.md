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

| No. | Problem  | how to fix |
|---|---|---|
|1 | ERROR: Message not found for errorCode: 0xC00000AC  | need to install JDK, and config JAVA environment variable|
|2 | how to fix add windows node as Windows service error | [JENKINS-16418](https://issues.jenkins-ci.org/browse/JENKINS-16418) |
|3 | org.jinterop.dcom.common.JIException: Message not found for errorCode: 0x00000005 | HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Wow6432Node\CLSID {72C24DD5-D70A-438B-8A42-98424B88AFB8} <br> HKEY_CLASSES_ROOT\CLSID{76A64158-CB41-11D1-8B02-00600806D9B6} <br>Launch 'regedit' (as Administrator) <br>Find (Ctrl+F) the following registry key: "{72C24DD5-D70A-438B-8A42-98424B88AFB8}" in HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Wow6432Node\CLSID\ <br>Right click and select 'Permissions', Change owner to administrators group (Advanced...). <br>Change permissions for administrators group. Grant Full Control <br>Change owner back to TrustedInstaller (user is "NT Service\TrustedInstaller" on local machine)<br>Repeat the steps above for HKEY_CLASSES_ROOT\CLSID {76A64158-CB41-11D1-8B02-00600806D9B6} <br>Restart Remote Registry Service (Administrative Tools / Services) |
|4 | ERROR: Unexpected error in launching an agent. This is probably a bug in Jenkins| Login remote machine and open Services find jenkinsslave-C__agent <br>Set startup type: Automatic <br>Log On: select This account, type correct account and password <br>start jenkinsslave-C__agent |
|5 | Caused by: org.jinterop.dcom.common.JIRuntimeException: Message not found for errorCode: 0x800703FA | Slave under domain account <br>If your slave is running under a domain account and you get an error code 0x800703FA, change a group policy: <br>open the group policy editor (gpedit.msc) <br>go to Computer Configuration->Administrative Templates->System-> UserProfiles, "Do not forcefully unload the user registry at user logoff" <br>Change the setting from "Not Configured" to "Enabled", which disables the new User Profile Service feature ('DisableForceUnload' is the value added to the registry) |
|6 | more connect jenkins agent problem on windows ... | please refer to this link https://github.com/jenkinsci/windows-slaves-plugin/blob/master/docs/troubleshooting.adoc |
|7 | ERROR: Message not found for errorCode: 0xC0000001 Caused by: jcifs.smb.SmbException: Failed to connect: 0.0.0.0<00>/10.xxx.xxx.xxx | need to enable SMB1 <br>Search in the start menu for ‘Turn Windows features on or off’ and open it. <br>Search for ‘SMB1.0/CIFS File Sharing Support’ in the list of optional features that appears, and select the checkbox next to it. <br>Click OK and Windows will add the selected feature. You’ll be asked to restart your computer as part of this process |
