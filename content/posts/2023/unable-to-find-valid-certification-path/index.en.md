---
title: Resolving Jenkins Artifactory Plugin Artifact Upload Failure "unable to find valid certification path to requested target"
summary: |
  This article describes how to resolve SSL certificate validation issues when uploading artifacts from a Jenkins agent to Artifactory, including generating a security certificate file and importing it into Java's cacerts.
tags:
  - Artifactory
  - Java
  - Jenkins
date: 2023-09-11
authors:
  - shenxianpeng
---

Recently, I encountered an issue where artifacts could not be uploaded from a Jenkins agent to Artifactory. The specific error is as follows:


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

This problem occurs because the Java security certificate does not validate the HTTPS connection when uploading files.  The solution is to regenerate the certificate file and import it. The steps are as follows.

## Generating the Security Certificate File

Steps:

1. First, open your Artifactory URL in a browser.
2. There should be a lock icon on the left side of the URL. Click on "Connection is secure" -> "Certificate is valid" -> "Details" -> "Export".
3. Select "DER-encoded binary, single certificate (*.der)" to generate the certificate file.

For example, I named my security certificate file: `artifactory.mycompany.der` (the name can be arbitrary, as long as the extension remains unchanged).

## Importing the Security Certificate via Command Line

Log in to the problematic Solaris agent, upload `artifactory.mycompany.der` to a specified directory, find the path to `cacerts`, and execute the following command:

```bash
root@mysolaris:/# keytool -import -alias example -keystore /usr/java/jre/lib/security/cacerts -file /tmp/artifactory.mycompany.der
# Then select yes
```

You will be prompted to enter the password. The default password is `changeit`. Enter it and restart your JVM or VM.  Once you retry uploading artifacts through this agent, everything should return to normal.

> Reference: https://stackoverflow.com/questions/21076179/pkix-path-building-failed-and-unable-to-find-valid-certification-path-to-requ
---

Please indicate the author and source when reprinting this article.  Do not use for any commercial purposes.  Welcome to follow the WeChat official account "DevOps攻城狮"