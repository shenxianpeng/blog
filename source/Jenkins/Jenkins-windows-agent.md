---
title: How to config Jenkins windows agent
date: 2019-05-12 18:39:59
tags: Jenkins
---

# Prepare Java runtime
1. download Java https://www.java.com/en/download/
2. configure Java Windows path
    ```
    JAVA_HOME=C:\Program Files\Java\jdk1.8.0_201
    CLASSPATH=.;%JAVA_HOME%\lib;%JAVA_HOME%\jre\lib
    ```



# Create Node
1. Jenkins home page->Manage Node->New Node, such as window-build-machine
2. List windows agent settings
    | Items  | Settings |   
    |:-:|:-:|---|---|---|
    | Name  |window-build-machine |   
    | Description  | used for windows build | 
    | of executors | 1  |  
    | Remote root directory | C:\agent |  
    | Labels | windows, build |  
    | Usage | 1  |  
    | Launch method	| Let Jenkins control this Windows slave as a Windows service |  
    | Administrator user name | .\Administrator |  
    | Password | *********** |  
    | Host | 192.168.1.111 |
    | Run service as | Use Administrator account given above |
    | Availability | Keep this agent online as much as paossible |
3. Save then Connect
    ```
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

# Troubleshooting
| Problem  | how to fix |   
|---|---|
| ERROR: Message not found for errorCode: 0xC00000AC  |need to install JDK, and config JAVA environment variable|   
| how to fix add windows node as Windows service error | https://issues.jenkins-ci.org/browse/JENKINS-16418 | 
| org.jinterop.dcom.common.JIException: Message not found for errorCode: 0x00000005 | HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Wow6432Node\CLSID {72C24DD5-D70A-438B-8A42-98424B88AFB8}, HKEY_CLASSES_ROOT\CLSID{76A64158-CB41-11D1-8B02-00600806D9B6} Launch 'regedit' (as Administrator), Find (Ctrl+F) the following registry key: "{72C24DD5-D70A-438B-8A42-98424B88AFB8}" in HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Wow6432Node\CLSID\, Right click and select 'Permissions', Change owner to administrators group (Advanced...). Change permissions for administrators group. Grant Full Control, Change owner back to TrustedInstaller (user is "NT Service\TrustedInstaller" on local machine), Repeat the steps above for HKEY_CLASSES_ROOT\CLSID {76A64158-CB41-11D1-8B02-00600806D9B6}, Restart Remote Registry Service (Administrative Tools / Services) |  
| ERROR: Unexpected error in launching an agent. This is probably a bug in Jenkins| Login remote machine and open Services, find jenkinsslave-C__agent, Set startup type: Automatic, Log On: select This account, type correct account and password, start jenkinsslave-C__agent |  
| Caused by: org.jinterop.dcom.common.JIRuntimeException: Message not found for errorCode: 0x800703FA | Slave under domain account, If your slave is running under a domain account and you get an error code 0x800703FA, change a group policy: open the group policy editor (gpedit.msc) go to Computer Configuration->Administrative Templates->System-> UserProfiles, "Do not forcefully unload the user registry at user logoff" Change the setting from "Not Configured" to "Enabled", which disables the new User Profile Service feature ('DisableForceUnload' is the value added to the registry) | 


