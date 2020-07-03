---
title: 通过参数化上传文件到 FTP 服务器
date: 2019-05-13 23:43:21
tags: 
- Automation
- Batch
categories: 
- Automation
author: shenxianpeng
---

实现 CI/CD 过程中，常常需要将构建好的 build 上传到一个公共的服务器，供测试、开发来获取最新的 build。如何上传 build 成果物到 FTP server，又不想把 FTP server登录的用户名和密码存在脚本里，想做这样的参数化如何实现呢？

```bash
upload_to_ftp.bat [hostname] [username] [password] [local_path] [remote_pat]
```

<!-- more -->

windows batch 由于它的局限性，在实现上是比较麻烦的，但还是有办法。如何用 windows batch 来实现呢？借助一个临时文件，把需要的参数写入到临时文件里，然后通过 ftp -s 参数读取文件，最后把临时文件删除的方式来实现。

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
echo.   - upload_to_ftp.bat [hostname] [username] [password] [local_path] [remote_pat]  -
echo.   - Example:                                                                      -
echo.   - upload_to_ftp.bat 192.168.1.1 guest guest D:\Media\* C:\Builds\               -
echo.   - -------------------------------------------------------------------------------
echo.

:END
```
