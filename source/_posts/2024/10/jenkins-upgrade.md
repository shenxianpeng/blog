---
title: 从 Jenkins 升级，我做了哪些优化
tags:
  - Jenkins
  - DevOps
categories:
  - Jenkins
date: 2024-10-24 00:00:00
author: shenxianpeng
---

## 背景

我最近在做的一件事情是迁移并升级 Jenkins。主要动机是因为这个漏洞 [CVE-2024-23897](https://nvd.nist.gov/vuln/detail/CVE-2024-23897)

> Jenkins 2.441 及更早版本、LTS 2.426.2 及更早版本未禁用其 CLI 命令解析器的一项功能，该功能会将参数中文件路径后的“@”字符替换为文件内容，从而允许未经身份验证的攻击者读取 Jenkins 控制器文件系统上的任意文件。

因此需要将 Jenkins 至少升级到 2.442 或 LTS 2.426.3 及以上版本，也趁此机会重新重构之前没有做满意的部分。


<!-- more -->
## 升级之前的 Jenkins

升级之前我们使用的是 Jenkins 2.346.3，这是最后一个支持 Java 8 的版本。由于老的操作系统不支持 Java 17，导致无法升级 Jenkins。

实际上，在升级之前我们已经做得还不错：

* 遵循了 Infrastructure as Code 原则，我们通过 Docker Compose 部署 Jenkins。
* 遵循了 Configuration as Code 原则，使用 Jenkins Shared Library 来管理所有的 Jenkins Pipeline。
* 使用 Jenkins Multibranch Pipeline 来构建和测试项目。

但也存在一些不足之处，比如：

* Jenkins 服务器没有一个固定的域名，比如 jenkinsci.organization.com，而是 http://234.345.999:8080 这样的格式。所有配置到这台 Jenkins 上的 Webhook 当 IP 或 hostname 变化时，需要从 Git 仓库同时修改。
* 没有使用 Docker Cloud，虽然很多任务已经使用 Docker 构建，但没有使用 Docker JNLP，也就是动态创建 Agent 来进行构建，完成后自动销毁。
* Jenkins Shared Library 的名字和代码结构需要重构。当初创建时只是为一个团队而做，因此仓库名字比较受限。
* 没有使用 Windows Docker Container。
* 有的 Jenkins 插件可能已经不再使用，但仍然存在。
* 由于 Jenkins Agent 版本的限制，Jenkins 和插件没有及时更新。

## 升级后的 Jenkins

在保留了之前好的实践的基础上，我们进行了以下优化：

* 继续遵循 Infrastructure as Code 原则，同时通过 Nginx 作为代理，使用 Docker Compose 与 Jenkins 一起部署，确保拥有一个固定的域名。
* 继续遵循 Configuration as Code 原则。
* 继续使用 Jenkins Multibranch Pipeline 来构建和测试项目。
* 尽可能使用 Docker Cloud 来构建。
* 将 Jenkins Shared Library 重命名为 pipeline-library（与 Jenkins 官方命名一致），并对大量 Jenkinsfile 和 Groovy 文件进行了重构。
* 引入 Windows Docker Container 构建 Windows 部分。
* 使用 Jenkins Configuration as Code 插件，定期备份配置。
* 仅安装必要的 Jenkins 插件，并通过 plugin 命令导出当前的插件列表。
* 尝试在升级前自动备份插件，确保升级失败时能够快速回滚。

## 总结

我希望通过这些努力，将 Infrastructure 的维护和 Pipeline 的开发通过 GitOps 方式进行管理。

不断探索、尝试和应用最佳实践，使 CI/CD 成为一个健康的、可持续维护的、自我改进和成长的 DevOps 系统。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
