---
title: 花了两天时间解决了使用 Jenkins Artifactory plugin 在 AIX 上无法上传制品到 Artifactory 的问题
tags:
  - Troubleshooting
  - JFrog
categories:
  - Jenkins
date: 2020-06-03 19:30:03
author: shenxianpeng
---

分享一个花了两天时间才解决的一个只在 AIX 平台上只出现的问题。该问题对于同样在 AIX 遇到此问题的人会非常有帮助。如果想了解解决过程可继续阅读，否则无需继续阅读了 :)

最近计划将之前使用的 Artifactory OSS 版本迁移到 Aritifactory Enterprise 版本上。

为什么要迁移？这里有一个 Artifactory 对比的矩阵图 https://www.jfrog.com/confluence/display/JFROG/Artifactory+Comparison+Matrix

可以看到开源版版本缺少与CI集成时常用的功能，比如保留策略(Retention)，提升(Promote)，设置属性(set properties)等这些常用功能，正好公司已经有企业版了，那就开始迁移吧。本以为会很顺利的完成，没想到唯独在 IBM 的 AIX 出现上传制品失败的情况。

以下是完整的错误信息。(去掉了无相关的敏感信息)

```java
[2020-06-03T09:01:00.105Z] [consumer_0] Deploying artifact: https://artifactory.company.com/artifactory/generic-int-den/database/develop/10/database2_cdrom_opt_AIX_24ec6f9.tar.Z
[2020-06-03T09:01:27.834Z] Error occurred for request GET /artifactory/api/system/version HTTP/1.1: A system call received a parameter that is not valid. (Read failed).
[2020-06-03T09:01:28.388Z] Error occurred for request PUT /artifactory/generic-int-den/database/develop/10/database2_cdrom_opt_AIX_24ec6f9.tar.Z;build.timestamp=1591170116591;build.name=develop;build.number=10 HTTP/1.1: A system call received a parameter that is not valid. (Read failed).
[2020-06-03T09:01:28.442Z] Error occurred for request PUT /artifactory/generic-int-den/database/develop/10/database2_cdrom_opt_AIX_24ec6f9.tar.Z;build.timestamp=1591170116591;build.name=develop;build.number=10 HTTP/1.1: A system call received a parameter that is not valid. (Read failed).
[2020-06-03T09:01:28.445Z] [consumer_0] An exception occurred during execution:
[2020-06-03T09:01:28.446Z] java.lang.RuntimeException: java.net.SocketException: A system call received a parameter that is not valid. (Read failed)
[2020-06-03T09:01:28.446Z] 	at org.jfrog.build.extractor.clientConfiguration.util.spec.SpecDeploymentConsumer.consumerRun(SpecDeploymentConsumer.java:44)
[2020-06-03T09:01:28.446Z] 	at org.jfrog.build.extractor.producerConsumer.ConsumerRunnableBase.run(ConsumerRunnableBase.java:11)
[2020-06-03T09:01:28.447Z] 	at java.lang.Thread.run(Thread.java:785)
[2020-06-03T09:01:28.447Z] Caused by: java.net.SocketException: A system call received a parameter that is not valid. (Read failed)
[2020-06-03T09:01:28.448Z] 	at java.net.SocketInputStream.socketRead(SocketInputStream.java:127)
[2020-06-03T09:01:28.448Z] 	at java.net.SocketInputStream.read(SocketInputStream.java:182)
[2020-06-03T09:01:28.448Z] 	at java.net.SocketInputStream.read(SocketInputStream.java:152)
[2020-06-03T09:01:28.449Z] 	at com.ibm.jsse2.a.a(a.java:227)
[2020-06-03T09:01:28.449Z] 	at com.ibm.jsse2.a.a(a.java:168)
[2020-06-03T09:01:28.449Z] 	at com.ibm.jsse2.as.a(as.java:702)
[2020-06-03T09:01:28.449Z] 	at com.ibm.jsse2.as.i(as.java:338)
[2020-06-03T09:01:28.450Z] 	at com.ibm.jsse2.as.a(as.java:711)
[2020-06-03T09:01:28.450Z] 	at com.ibm.jsse2.as.startHandshake(as.java:454)
[2020-06-03T09:01:28.450Z] 	at org.apache.http.conn.ssl.SSLConnectionSocketFactory.createLayeredSocket(SSLConnectionSocketFactory.java:436)
[2020-06-03T09:01:28.451Z] 	at org.apache.http.conn.ssl.SSLConnectionSocketFactory.connectSocket(SSLConnectionSocketFactory.java:384)
[2020-06-03T09:01:28.451Z] 	at org.apache.http.impl.conn.DefaultHttpClientConnectionOperator.connect(DefaultHttpClientConnectionOperator.java:142)
[2020-06-03T09:01:28.452Z] 	at org.apache.http.impl.conn.PoolingHttpClientConnectionManager.connect(PoolingHttpClientConnectionManager.java:374)
[2020-06-03T09:01:28.452Z] 	at org.apache.http.impl.execchain.MainClientExec.establishRoute(MainClientExec.java:393)
[2020-06-03T09:01:28.452Z] 	at org.apache.http.impl.execchain.MainClientExec.execute(MainClientExec.java:236)
[2020-06-03T09:01:28.453Z] 	at org.apache.http.impl.execchain.ProtocolExec.execute(ProtocolExec.java:186)
[2020-06-03T09:01:28.453Z] 	at org.apache.http.impl.execchain.RetryExec.execute(RetryExec.java:89)
[2020-06-03T09:01:28.453Z] 	at org.apache.http.impl.execchain.ServiceUnavailableRetryExec.execute(ServiceUnavailableRetryExec.java:85)
[2020-06-03T09:01:28.454Z] 	at org.apache.http.impl.execchain.RedirectExec.execute(RedirectExec.java:110)
[2020-06-03T09:01:28.454Z] 	at org.apache.http.impl.client.InternalHttpClient.doExecute(InternalHttpClient.java:185)
[2020-06-03T09:01:28.454Z] 	at org.apache.http.impl.client.CloseableHttpClient.execute(CloseableHttpClient.java:83)
[2020-06-03T09:01:28.455Z] 	at org.jfrog.build.client.PreemptiveHttpClient.execute(PreemptiveHttpClient.java:89)
[2020-06-03T09:01:28.455Z] 	at org.jfrog.build.client.ArtifactoryHttpClient.execute(ArtifactoryHttpClient.java:253)
[2020-06-03T09:01:28.455Z] 	at org.jfrog.build.client.ArtifactoryHttpClient.upload(ArtifactoryHttpClient.java:249)
[2020-06-03T09:01:28.456Z] 	at org.jfrog.build.extractor.clientConfiguration.client.ArtifactoryBuildInfoClient.uploadFile(ArtifactoryBuildInfoClient.java:692)
[2020-06-03T09:01:28.456Z] 	at org.jfrog.build.extractor.clientConfiguration.client.ArtifactoryBuildInfoClient.doDeployArtifact(ArtifactoryBuildInfoClient.java:379)
[2020-06-03T09:01:28.456Z] 	at org.jfrog.build.extractor.clientConfiguration.client.ArtifactoryBuildInfoClient.deployArtifact(ArtifactoryBuildInfoClient.java:367)
[2020-06-03T09:01:28.457Z] 	at org.jfrog.build.extractor.clientConfiguration.util.spec.SpecDeploymentConsumer.consumerRun(SpecDeploymentConsumer.java:39)
[2020-06-03T09:01:28.457Z] 	... 2 more
[2020-06-03T09:01:28.457Z] 
Failed uploading artifacts by spec
```

本以为 Google 一下就能找到此类问题的解决办法，可惜这个问题在其他平台都没有，只有 AIX 上才有这个问题，肯定这个 AIX 有什么“过人之处”，非得搞得和其他 Linux/Unix 那么不一样。以下列出了两种处理办法。

## 使用 `curl` 来替代

由于上述问题重现在需要重新构建，比较花时间，我就先试试用 `curl` 命令是否能否上传呢？

做了一下测试，直接使用 curl 来查看 Artifactory 的版本，果然出错了，`curl` 也不行。

```bash
curl  https://artifactory.company.com/artifactory/api/system/version
curl: (35) Unknown SSL protocol error in connection to artifactory.company.com:443

# 打开 -v 模式，输出更多信息
bash-4.3$ curl -v  https://artifactory.company.com/artifactory/api/system/version
*   Trying 10.18.12.95...
* Connected to artifactory.company.com (10.18.12.95) port 443 (#0)
* Cipher selection: ALL:!EXPORT:!EXPORT40:!EXPORT56:!aNULL:!LOW:!RC4:@STRENGTH
* TLSv1.2 (OUT), TLS handshake, Client hello (1):
* TLSv1.2 (IN), TLS handshake, Server hello (2):
* NPN, negotiated HTTP1.1
* TLSv1.2 (IN), TLS handshake, Certificate (11):
* TLSv1.2 (OUT), TLS alert, Server hello (2):
* Unknown SSL protocol error in connection to artifactory.company.com:443
* Closing connection 0
curl: (35) Unknown SSL protocol error in connection to artifactory.company.com:443
```

看起来问题可能是 curl 没有找到制定证书，查了help `--cacert` 参数可以指定 cacert.pem 文件，试了下成功了！

```bash
bash-4.3$ curl --cacert /var/ssl/cacert.pem https://artifactory.company.com/artifactory/api/system/version
{
  "version" : "6.9.0",
  "revision" : "60900900",
  "addons" : [ "build", "docker", "vagrant", "replication", "filestore", "plugins", "gems", "composer", "npm", "bower", "git-lfs", "nuget", "debian", "opkg", "rpm", "cocoapods", "conan", "vcs", "pypi", "release-bundle", "replicator", "keys", "chef", "cran", "go", "helm", "rest", "conda", "license", "puppet", "ldap", "sso", "layouts", "properties", "search", "filtered-resources", "p2", "watch", "webstart", "support", "xray" ],
  "license" : "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

到这里问题已经解决了，只要使用 `curl` 调用 Artifactory REST API 就能完成上传操作了。但是我用的 Artifactory Jenkins Plugin 如果使用 `curl` 我需要把之前的实现都转换一遍，还要测试，就为了 AIX 一个平台的问题，做这样的转换实在是“懒”。就本着这样懒惰的性格，还得继续解决 Jenkins 调用 agent 去执行上传失败的问题。

## 继续使用 Artifactory 插件

> Jenkins 的 master 管理 agent 是通过在 agent 上启动一个 remote.jar, 

用同样的办法来解决 Jenkins 的问题。如果有一个环境变量能设置指定 cacert.pem 文件的路径，那样在 Jenkins 调用 agent 执行上传时候可能就能解决同样的问题了。果然有这样的环境变量，设置如下

```bash
set SSL_CERT_FILE=/var/ssl/cacert.pem
```
设置之后通过 `curl` 调用，经测试不需要再用 `--cacert` 参数了。带着喜悦的喜悦的心情去 Jenkins 设置如下或是可以修改 `/etc/environment` 文件，把上述的环境变量加到 agent 机器上。

![](Java-net-SocketException-on-AIX/configure-agent-environment-variable.png)

结果经测试错误信息依旧，看来执行的 remote.jar 去进行上传跟本地配置环境没有关联。看来需要从执行 remote.jar 把相应的设置或是环境变量传进去。`java` 的 `-D` 参数可以完成这一点。

废话不多说了，进行了浩瀚的搜索和尝试，最终在 IBM 的官方找到了这篇文档 https://www.ibm.com/support/knowledgecenter/SSYKE2_8.0.0/com.ibm.java.security.component.80.doc/security-component/jsse2Docs/matchsslcontext_tls.html

文档大意是，IBM SDK system property `com.ibm.jsse2.overrideDefaultTLS =[true|false]` 有 `true` 和 `false` 两个值，如果想要与 Oracle `SSLContext.getInstance("TLS")` 的行为相匹配，请将此属性设置为 `true`，默认值为 `false`。

最终我在 Jenkins 的 agent 配置里 JVM Options 区域加上 `-Dcom.ibm.jsse2.overrideDefaultTLS=true` 解决了我的这样问题。