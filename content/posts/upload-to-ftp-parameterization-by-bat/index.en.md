---
title: Uploading Files to an FTP Server via Parameterization
summary: This article describes how to use a Windows Batch script to upload files to an FTP server using parameterized input, avoiding hardcoding FTP credentials in the script.
date: 2019-05-13
tags:
- Automation
- Shell
- FTP
- Automation
author: shenxianpeng
---

During CI/CD implementation, it's often necessary to upload the built artifacts to a public server for testing and development teams to access the latest build.  How can we upload build artifacts to an FTP server without storing the FTP server login username and password directly in the script? How can we achieve this parameterization?

```bash
upload_to_ftp.bat [hostname] [username] [password] [local_path] [remote_path]
```

Windows batch scripting, due to its limitations, makes this relatively cumbersome, but it's still achievable. How can we implement this using a Windows batch script?  We can use a temporary file to write the required parameters, then use the `ftp -s` parameter to read the file, and finally delete the temporary file.

```bash
@echo off

set ftp_hostname=%1
set ftp_username=%2
set ftp_password=%3
set local_path=%4
set remote_path=%5

if %ftp_hostname%! == ! ( echo "ftp_hostname not set correctly" & goto USAGE )
if %ftp_username%! == ! ( echo "ftp_username not set correctly" & goto USAGE )
if %ftp_password%! == ! ( echo "ftp_password not set correctly" & goto USAGE )
if %local_path%! == ! ( echo "local_path not set correctly" & goto USAGE )
if %remote_path%! == ! ( echo "remote_path not set correctly" & goto USAGE )

echo open %ftp_hostname% > ftp.txt
echo user %ftp_username% %ftp_password% >> ftp.txt
echo cd %remote_path% >> ftp.txt
echo lcd %local_path% >>ftp.txt
echo prompt off >>ftp.txt
echo bin >> ftp.txt
echo mput * >> ftp.txt
echo bye >> ftp.txt
ftp -n -s:ftp.txt

del ftp.txt
goto END

:USAGE
echo.
echo.   - -------------------------------------------------------------------------------
echo.   - upload_to_ftp.bat [hostname] [username] [password] [local_path] [remote_path]  -
echo.   - Example:                                                                      -
echo.   - upload_to_ftp.bat 192.168.1.1 guest guest D:\Media\* C:\Builds\               -
echo.   - -------------------------------------------------------------------------------
echo.

:END
```