---
title: PowerShell is not recognized as an internal or external command
tags:
  - ansible-playbook
  - ansible
categories:
  - DevOps
date: 2024-11-18 00:00:00
author: shenxianpeng
---

Recently, while setting up a new Windows Server 2022, I encountered an issue where my Ansible playbook, which previously worked without problems, failed to execute.

Here’s the configuration I used for the Windows host in my Ansible inventory:

```ini
[jenkins-agent-windows:vars]
ansible_user=
ansible_ssh_pass=
ansible_connection=winrm
ansible_winrm_transport=ntlm
ansible_winrm_server_cert_validation=ignore
```

However, when I ran the playbook, the following error occurred:

```bash
winrm send_input failed;
stdout:
stderr 'PowerShell' is not recognized as an internal or external command, operable program or batch file.
```

## Cause of the Issue


This is usually the case when the SYSTEM's `PATH` environment variable has been changed and is no longer able to find `PowerShell.exe` in the path.

Please verify the PATH environment contains the entry `C:\Windows\System32\WindowsPowerShell\v1.0` in there.

## Solution

Right-click This PC > Properties > Advanced system settings > Environment Variables.

After adding `C:\Windows\System32\WindowsPowerShell\v1.0` to `PATH`, the error disappeared, and my Ansible playbook executed successfully.
