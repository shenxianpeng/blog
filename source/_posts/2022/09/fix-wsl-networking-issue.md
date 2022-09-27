---
title: How to fix "Temporary Failure in name resolution" in WSL
tags:
  - WSL
categories:
  - OS
author: shenxianpeng
date: 2022-09-27 09:56:50
---

## Problem

I have encountered a problem when I ping google.com failed and return some error like "Temporary failure in name resolution"

## How to fix

1. Inside WSL2, create or append file: `/etc/wsl.conf`
2. Put the following lines in the file in order to ensure the your DNS changes do not get blown away

    ```bash
    sudo tee /etc/wsl.conf << EOF
    [network]
    generateResolvConf = false
    EOF
    ```
<!-- more -->
3. In a cmd windows (!!), run `wsl --shutdown`
4. Start WSL2
5. Run the following inside WSL2 (line with search is optional)

  ```bash
  sudo rm -rf /etc/resolv.conf
  sudo tee /etc/resolv.conf << EOF
  search yourbase.domain.local
  nameserver 8.8.8.8
  nameserver 1.1.1.1
  EOF
  ```

  In my case, I can remove `/etc/resolv.conf` and error is "rm: cannot remove '/etc/resolv.conf': Operation not permitted"

  ```bash
  # use following command instead fixed.
  sudo chattr -a -i /etc/resolv.conf
  ```

## Reference links

> https://askubuntu.com/questions/1192347/temporary-failure-in-name-resolution-on-wsl
> https://askubuntu.com/questions/125847/un-removable-etc-resolv-conf

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
