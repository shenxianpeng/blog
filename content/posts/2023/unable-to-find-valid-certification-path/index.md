---
title: 解决通过 Jenkins Artifactory plugin 上传 artifacts 失败的问题 “unable to find valid certification path to requested target”
summary: |
  本文介绍了如何解决 Jenkins agent 上传 artifacts 到 Artifactory 时遇到的 SSL 证书验证问题，包括生成安全认证文件和导入到 Java 的 cacerts 中。
tags:
  - Artifactory
  - Java
  - Jenkins
date: 2023-09-11
aliases:
  - /2023/09/unable-to-find-valid-certification-path/
authors:
  - shenxianpeng
---

最近遇到了通过 Jenkins agent 无法上传 artifacts 到 Artifactory 的情况，具体错误如下：


```bash
[2023-09-11T08:21:53.385Z] Executing command: /bin/sh -c git log --pretty=format:%s -1
[2023-09-11T08:21:54.250Z] [consumer_0] Deploying artifact: https://artifactory.mycompany.com/artifactory/generic-int-den/my-project/hotfix/1.2.0.HF5/3/pj120_bin_opt_SunOS_3792bcf.tar.Z

[2023-09-11T08:21:54.269Z] Error occurred for request GET /artifactory/api/system/version HTTP/1.1: sun.security.validator.ValidatorException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target.
[2023-09-11T08:21:54.282Z] Error occurred for request PUT /artifactory/generic-int-den/my-project/hotfix/1.2.0.HF5/3/pj120_bin_opt_SunOS_3792bcf.tar.Z;build.timestamp=1694418199972;build.name=hotfix%2F1.2.0.HF5;build.number=3 HTTP/1.1: sun.security.validator.ValidatorException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target.
[2023-09-11T08:21:54.284Z] [consumer_0] An exception occurred during execution:
[2023-09-11T08:21:54.284Z] java.lang.RuntimeException: javax.net.ssl.SSLHandshakeException: sun.security.validator.ValidatorException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
[2023-09-11T08:21:54.284Z] 	at org.jfrog.build.extractor.clientConfiguration.util.spec.SpecDeploymentConsumer.consumerRun(SpecDeploymentConsumer.java:44)
[2023-09-11T08:21:54.284Z] 	at org.jfrog.build.extractor.producerConsumer.ConsumerRunnableBase.run(ConsumerRunnableBase.java:11)
[2023-09-11T08:21:54.284Z] 	at java.lang.Thread.run(Thread.java:745)
[2023-09-11T08:21:54.285Z] Caused by: javax.net.ssl.SSLHandshakeException: sun.security.validator.ValidatorException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
```

这个问题产生的原因是通过 HTTPS 来上传文件的时候没有通过 Java 的安全认证。解决这个问题的办法就是重新生成认证文件，然后导入即可，具体的步骤如下。

## 生成安全认证（Security Certificate）文件

步骤如下：

1. 首先生成通过浏览器打开的你的 Artifactory 网址
2. 在网址的左侧应该有一个锁的图标，点击 Connection is secure -》Certificate is valid -》Details -》 Export
3. 选择 DER-encoded binary, single certificate (*.der) 生成认证文件

比如我生成的安全认证文件的名字叫：`artifactory.mycompany.der`（名字可以任意起，只要后缀名不变即可）

## 通过命令行导入安全认证

登录到那台有问题的 Solaris agent，上传 `artifactory.mycompany.der` 到指定目录下，然后找到 cacerts 的路径，执行如下命令：

```bash
root@mysolaris:/# keytool -import -alias example -keystore /usr/java/jre/lib/security/cacerts -file /tmp/artifactory.mycompany.der
# 然后选择 yes
```

这时候会提示你输入密码，默认密码为 `changeit`，输入即可。然后重启你的 JVM 或是 VM。等再次通过该 Agent 上传 artifacts，一切恢复正常。

> 可参考： https://stackoverflow.com/questions/21076179/pkix-path-building-failed-and-unable-to-find-valid-certification-path-to-requ
---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
