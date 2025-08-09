---
title: 备份 Jenkins 的方法
summary: |
  介绍如何使用 ThinBackup 插件或 Shell 脚本备份 Jenkins，确保 Jenkins 配置和构建数据安全存储。
tags:
  - DevOps
  - Jenkins
  - Backup
date: 2020-11-24
author: shenxianpeng
---

大多数人可能已经在使用 **Jenkins Configuration as Code** 的理念，把构建/测试/发布流程写成代码。  
虽然这样很好，但并不是所有配置都在代码中，部分 Jenkins 系统配置是存储在 Jenkins 服务本地的，因此仍然需要定期备份，以防灾难发生。

备份 Jenkins 有两种方式：  
1. 使用插件  
2. 编写 Shell 脚本

---

## 方法一：使用插件备份

我使用的是 [`ThinBackup`](https://plugins.jenkins.io/thinbackup/) 插件，以下是我的配置示例：

![ThinBackup Configuration](thinBackup-Configuration.png)

- 备份到 **jenkins 用户**有写权限的文件夹（非常重要）  
  > 之前我将 Jenkins 备份到挂载目录，结果失败。后来切换到 `jenkins` 用户登录发现该目录无法访问，而我的个人用户可以，所以问题出在权限上。

- 每天备份（周一到周六）
- 最多保留 3 份备份（每份备份超过 400MB）
- 其他勾选项：
  - 备份构建结果
  - 备份 `userContent` 文件夹
  - 备份下一个构建号文件
  - 备份插件包
  - 将旧备份压缩为 ZIP

---

## 方法二：使用 Shell 脚本备份

推荐参考以下资源：

- GitHub 仓库：[sue445/jenkins-backup-script](https://github.com/sue445/jenkins-backup-script)  
- Gist 示例：[abayer/jenkins-backup](https://gist.github.com/abayer/527063a4519f205efc74)  

脚本备份方式适合需要更多定制化的场景，比如结合 `cron` 定时任务或云存储同步。

---

💡 **建议**  
无论使用哪种方法，都应定期验证备份可用性，确保在需要恢复时能快速上线。
