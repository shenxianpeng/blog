---
title: 如何修复 WSL 中的 "Temporary Failure in name resolution" 错误
summary: |
  本文介绍如何通过配置 DNS 并确保修改持久化，来解决 WSL 中的 "Temporary failure in name resolution" 问题。
tags:
  - WSL
authors:
aliases:
  - /2022/09/fix-wsl-networking-issue/
  - shenxianpeng
date: 2022-09-27
---

## 问题描述

我在 WSL 中执行 `ping google.com` 时失败，并提示：

```
Temporary failure in name resolution
```

---

## 解决方法

1. 在 **WSL2** 中创建或修改 `/etc/wsl.conf` 文件  
2. 添加以下内容，以防止 DNS 修改被系统覆盖：

    ```bash
    sudo tee /etc/wsl.conf << EOF
    [network]
    generateResolvConf = false
    EOF
    ```

3. 在 **Windows CMD** 中运行：

    ```cmd
    wsl --shutdown
    ```

4. 重启 **WSL2**  
5. 在 WSL2 中执行以下命令（`search` 行可选）：

    ```bash
    sudo rm -rf /etc/resolv.conf
    sudo tee /etc/resolv.conf << EOF
    search yourbase.domain.local
    nameserver 8.8.8.8
    nameserver 1.1.1.1
    EOF
    ```

    如果删除 `/etc/resolv.conf` 时出现：

    ```
    rm: cannot remove '/etc/resolv.conf': Operation not permitted
    ```

    则先运行以下命令解锁文件：

    ```bash
    sudo chattr -a -i /etc/resolv.conf
    ```

---

## 参考链接

> https://askubuntu.com/questions/1192347/temporary-failure-in-name-resolution-on-wsl  
> https://askubuntu.com/questions/125847/un-removable-etc-resolv-conf  

---

转载本文请注明作者与出处，禁止商业用途。欢迎关注公众号「DevOps攻城狮」。
