---
title: Ansible 实践（一）
tags:
  - Ansible
categories:
  - DevOps
date: 2020-10-28 10:09:41
author: shenxianpeng
---

最近在思考如何将团队里的所有的虚拟机都很好的管理并监控起来，但是由于我们的虚拟机的操作系统繁多，包括 Windows, Linux, AIX, HP-UX, Solaris SPARC 和 Solaris x86. 到底选择哪种方式来管理比较好呢？这需要结合具体场景来考虑。

## 选择合适的工具

### 仅管理 Windows 和 Linux

如果你的虚拟机没有这么多平台，只是 Windows 和 Linux，假如你已经有了 VMware vSphere 来管理了，那么可以通过 VMware vSphere API 来查看这些机器的状态。

这里是 VMware 官方的 API Library 供使用：

* [VMware vSphere API Python Bindings](https://github.com/vmware/pyvmomi)
* [Go library for the VMware vSphere API](https://github.com/vmware/govmomi)

### 管理多个操作系统

如果你和我的情况一下，想监控很多个操作操作系统，那么就只能通过 ssh 来登录到每一台机器上去查看，比如执行 `uptime` 等命令。可以写 shell 脚本来完成这些登录、检测等操作。

另外就是使用 Ansible 的 Playbook。Playbook 里描述了你要做的操作，这是一个权衡，学习 Ansible 的 Playbook 需要花些时间的。

如果想了解下 Ansible 那么可以试试 Ansible Playbook。以下是我使用 Ansible 做了一些练习。

#### Playbook结构

```
+- vars                
|   +- vars.yml
|   +- ...
+- hosts               # save all hosts you want to monitor
+- run.yml             # ansible executable file
```

#### Playbook具体代码

vars/vars.yml

```yml
---
# system
ip: "{{ ansible_default_ipv4['address'] }}"
host_name: "{{ ansible_hostname }}"
os: "{{ ansible_distribution }}"
version: "{{ ansible_distribution_version }}"
total_mb: "{{ ansible_memtotal_mb }}"
vcpus: "{{ ansible_processor_vcpus }}"
```

hosts

```
[unix-vm]
aix ansible_host=walbld01.dev.company.com ansible_user=test ansible_become_pass=test
hp-ux  ansible_host=walbld04.dev.company.com ansible_user=test ansible_become_pass=test
linux ansible_host=walbld05.dev.company.com ansible_user=test ansible_become_pass=test

[win-vm]
win-bld02 ansible_host=walbld02.dev.company.com ansible_user=Administrator ansible_password=admin ansible_port=5985 ansible_connection=winrm ansible_winrm_server_cert_validation=ignore

[other-vm]
solaris ansible_host=walbld07.dev.company.com ansible_user=test ansible_become_pass=test
win-udb03 ansible_host=walbld03.dev.company.com ansible_user=administrator ansible_become_pass=admin
```

run.yml

```yml
---
# this playbook is simple test
- name: "get unix build machine info"
  hosts: unix-vm
  gather_facts: True

  tasks:
  - name: get uname, hostname and uptime
    shell: "uname && hostname && uptime"
    register: output
  - debug: var=output['stdout_lines']

- name: "get windows build machine os info"
  hosts: win-vm
  gather_facts: True

  tasks:
    - debug: var=hostvars['win-bld02'].ansible_facts.hostname
    - debug: var=hostvars['win-bld02'].ansible_distribution
```

#### 如何执行

首先需要安装了 ansible，然后执行

```sh
# run with playbook
ansible-playbook -i hosts run.yml
```
> 注：上面的代码是脱敏过的，不保证能一次性运行成功 :)


