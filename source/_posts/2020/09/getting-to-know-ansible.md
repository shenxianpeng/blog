---
title: 初识 Ansible
tags:
  - Ansible
categories:
  - DevOps
date: 2020-09-21 18:40:17
author: shenxianpeng
---

> https://www.edureka.co/blog/chef-vs-puppet-vs-ansible-vs-saltstack/

## 为什么是 Ansible

市面上关于管理虚拟机的工具有很多，比如 Chef，Puppet，Saltstack，Ansible 等等，它们都是行业里常用的 DevOps 工具，

那么为什么要有用 Ansible 呢

## Ansible TroubleShotting

`"msg": "winrm or requests is not installed: No module named winrm"`

Need install `pywinrm` on your master server.

"msg": "plaintext: auth method plaintext requires a password"

when I run `ansible mywin -i hosts -m win_ping -vvv`, I notice the output used Python2.7, so I install `pywinrm` with command `sudo pip2 install pywinrm`, then my problem was resolved.

```json
mywin | UNREACHABLE! => {
    "changed": false,
    "msg": "plaintext: auth method plaintext requires a password",
    "unreachable": true
}
```

Result: You should be using ansible_password and not ansible_pass. [link](https://github.com/ansible/ansible/issues/16858#issuecomment-250908554)
