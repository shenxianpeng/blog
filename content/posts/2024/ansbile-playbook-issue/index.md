---
title: PowerShell 不是内部或外部命令
summary: 介绍在 Windows Server 2022 上执行 Ansible playbook 时出现 PowerShell 无法识别的问题原因及解决方法。
tags:
  - Ansible
date: 2024-11-18
author: shenxianpeng
---

最近在配置一台新的 Windows Server 2022 时，我遇到了一个问题：之前运行正常的 Ansible playbook 无法执行了。

以下是我在 Ansible inventory 中为 Windows 主机配置的内容：

```ini
[jenkins-agent-windows:vars]
ansible_user=
ansible_ssh_pass=
ansible_connection=winrm
ansible_winrm_transport=ntlm
ansible_winrm_server_cert_validation=ignore
````

但是，当我运行 playbook 时，出现了如下错误：

```bash
winrm send_input failed;
stdout:
stderr 'PowerShell' is not recognized as an internal or external command, operable program or batch file.
```

---

## 问题原因

这种情况通常是由于 **SYSTEM** 用户的 `PATH` 环境变量被修改，导致系统无法找到 `PowerShell.exe` 的路径。

请检查 `PATH` 环境变量中是否包含以下路径：

```
C:\Windows\System32\WindowsPowerShell\v1.0
```

---

## 解决方法

依次执行：

1. 右键 **此电脑** → **属性**
2. 点击 **高级系统设置**
3. 进入 **环境变量**
4. 在 `PATH` 中添加：

```
C:\Windows\System32\WindowsPowerShell\v1.0
```

添加完成后，重新运行 Ansible playbook，问题即可解决。
