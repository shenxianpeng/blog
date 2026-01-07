---
title: 从 AIX 上传构件到 Artifactory 失败
summary: |
  本文介绍在 AIX 上通过 Jenkins 上传构件到 Artifactory 时遇到的 SSL 证书验证问题，包括更新 Java 的 cacerts 文件来解决问题。
tags:
  - Artifactory
  - Troubleshooting
authors:
aliases:
  - /2023/08/upload-artifacts-failed-on-aix/
  - shenxianpeng
date: 2023-08-29
---

最近，我的 CI 流水线在 **AIX 7.1** 上突然无法运行，出现如下错误：

```bash
Caused by: javax.net.ssl.SSLHandshakeException: com.ibm.jsse2.util.h: PKIX path building failed: java.security.cert.CertPathBuilderException: PKIXCertPathBuilderImpl could not build a valid CertPath.
```


<details>
<summary>点击查看详细的失败日志</summary>

```bash
22:13:30  Executing command: /bin/sh -c git log --pretty=format:%s -1
22:13:36  [consumer_0] Deploying artifact: https://artifactory.company.com/artifactory/generic-int-den/myproject/PRs/PR-880/1/myproject_bin_rel_AIX_5797b20.tar.Z
22:13:36  Error occurred for request GET /artifactory/api/system/version HTTP/1.1: com.ibm.jsse2.util.h: PKIX path building failed: java.security.cert.CertPathBuilderException: PKIXCertPathBuilderImpl could not build a valid CertPath.; internal cause is:
22:13:36  	java.security.cert.CertPathValidatorException: The certificate issued by CN=DigiCert Global Root G2, OU=www.digicert.com, O=DigiCert Inc, C=US is not trusted; internal cause is:
22:13:36  	java.security.cert.CertPathValidatorException: Certificate chaining error.
22:13:36  Error occurred for request PUT /artifactory/generic-int-den/myproject/PRs/PR-880/1/cpplinter_bin_rel_AIX_5797b20.tar.Z;build.timestamp=1693273923987;build.name=PR-880;build.number=1 HTTP/1.1: com.ibm.jsse2.util.h: PKIX path building failed: java.security.cert.CertPathBuilderException: PKIXCertPathBuilderImpl could not build a valid CertPath.; internal cause is:
22:13:36  	java.security.cert.CertPathValidatorException: The certificate issued by CN=DigiCert Global Root G2, OU=www.digicert.com, O=DigiCert Inc, C=US is not trusted; internal cause is:
22:13:36  	java.security.cert.CertPathValidatorException: Certificate chaining error.
22:13:36  [consumer_0] An exception occurred during execution:
22:13:36  java.lang.RuntimeException: javax.net.ssl.SSLHandshakeException: com.ibm.jsse2.util.h: PKIX path building failed: java.security.cert.CertPathBuilderException: PKIXCertPathBuilderImpl could not build a valid CertPath.; internal cause is:
22:13:36  	java.security.cert.CertPathValidatorException: The certificate issued by CN=DigiCert Global Root G2, OU=www.digicert.com, O=DigiCert Inc, C=US is not trusted; internal cause is:
22:13:36  	java.security.cert.CertPathValidatorException: Certificate chaining error
22:13:36  	at org.jfrog.build.extractor.clientConfiguration.util.spec.SpecDeploymentConsumer.consumerRun(SpecDeploymentConsumer.java:44)
22:13:36  	at org.jfrog.build.extractor.producerConsumer.ConsumerRunnableBase.run(ConsumerRunnableBase.java:11)
22:13:36  	at java.lang.Thread.run(Thread.java:785)
22:13:36  Caused by: javax.net.ssl.SSLHandshakeException: com.ibm.jsse2.util.h: PKIX path building failed: java.security.cert.CertPathBuilderException: PKIXCertPathBuilderImpl could not build a valid CertPath.; internal cause is:
22:13:36  	java.security.cert.CertPathValidatorException: The certificate issued by CN=DigiCert Global Root G2, OU=www.digicert.com, O=DigiCert Inc, C=US is not trusted; internal cause is:
22:13:36  	java.security.cert.CertPathValidatorException: Certificate chaining error
22:13:36  	at com.ibm.jsse2.j.a(j.java:3)
22:13:36  	at com.ibm.jsse2.as.a(as.java:213)
22:13:36  	at com.ibm.jsse2.C.a(C.java:339)
22:13:36  	at com.ibm.jsse2.C.a(C.java:248)
22:13:36  	at com.ibm.jsse2.D.a(D.java:291)
22:13:36  	at com.ibm.jsse2.D.a(D.java:217)
22:13:36  	at com.ibm.jsse2.C.r(C.java:373)
22:13:36  	at com.ibm.jsse2.C.a(C.java:352)
22:13:36  	at com.ibm.jsse2.as.a(as.java:752)
22:13:36  	at com.ibm.jsse2.as.i(as.java:338)
22:13:36  	at com.ibm.jsse2.as.a(as.java:711)
22:13:36  	at com.ibm.jsse2.as.startHandshake(as.java:454)
22:13:36  	at org.apache.http.conn.ssl.SSLConnectionSocketFactory.createLayeredSocket(SSLConnectionSocketFactory.java:436)
22:13:36  	at org.apache.http.conn.ssl.SSLConnectionSocketFactory.connectSocket(SSLConnectionSocketFactory.java:384)
22:13:36  	at org.apache.http.impl.conn.DefaultHttpClientConnectionOperator.connect(DefaultHttpClientConnectionOperator.java:142)
22:13:36  	at org.apache.http.impl.conn.PoolingHttpClientConnectionManager.connect(PoolingHttpClientConnectionManager.java:376)
22:13:36  	at org.apache.http.impl.execchain.MainClientExec.establishRoute(MainClientExec.java:393)
22:13:36  	at org.apache.http.impl.execchain.MainClientExec.execute(MainClientExec.java:236)
22:13:36  	at org.apache.http.impl.execchain.ProtocolExec.execute(ProtocolExec.java:186)
22:13:36  	at org.apache.http.impl.execchain.RetryExec.execute(RetryExec.java:89)
22:13:36  	at org.apache.http.impl.execchain.ServiceUnavailableRetryExec.execute(ServiceUnavailableRetryExec.java:85)
22:13:36  	at org.apache.http.impl.execchain.RedirectExec.execute(RedirectExec.java:110)
22:13:36  	at org.apache.http.impl.client.InternalHttpClient.doExecute(InternalHttpClient.java:185)
22:13:36  	at org.apache.http.impl.client.CloseableHttpClient.execute(CloseableHttpClient.java:83)
22:13:36  	at org.jfrog.build.client.PreemptiveHttpClient.execute(PreemptiveHttpClient.java:76)
22:13:36  	at org.jfrog.build.client.PreemptiveHttpClient.execute(PreemptiveHttpClient.java:64)
22:13:36  	at org.jfrog.build.client.JFrogHttpClient.sendRequest(JFrogHttpClient.java:133)
22:13:36  	at org.jfrog.build.extractor.clientConfiguration.client.JFrogService.execute(JFrogService.java:112)
22:13:36  	at org.jfrog.build.extractor.clientConfiguration.client.artifactory.services.Upload.execute(Upload.java:77)
22:13:36  	at org.jfrog.build.extractor.clientConfiguration.client.artifactory.ArtifactoryManager.upload(ArtifactoryManager.java:267)
22:13:36  	at org.jfrog.build.extractor.clientConfiguration.client.artifactory.ArtifactoryManager.upload(ArtifactoryManager.java:262)
22:13:36  	at org.jfrog.build.extractor.clientConfiguration.util.spec.SpecDeploymentConsumer.consumerRun(SpecDeploymentConsumer.java:39)
22:13:36  	... 2 more
22:13:36  Caused by: com.ibm.jsse2.util.h: PKIX path building failed: java.security.cert.CertPathBuilderException: PKIXCertPathBuilderImpl could not build a valid CertPath.; internal cause is:
22:13:36  	java.security.cert.CertPathValidatorException: The certificate issued by CN=DigiCert Global Root G2, OU=www.digicert.com, O=DigiCert Inc, C=US is not trusted; internal cause is:
22:13:36  	java.security.cert.CertPathValidatorException: Certificate chaining error
22:13:36  	at com.ibm.jsse2.util.f.a(f.java:107)
22:13:36  	at com.ibm.jsse2.util.f.b(f.java:143)
22:13:36  	at com.ibm.jsse2.util.e.a(e.java:6)
22:13:36  	at com.ibm.jsse2.aA.a(aA.java:99)
22:13:36  	at com.ibm.jsse2.aA.a(aA.java:112)
22:13:36  	at com.ibm.jsse2.aA.checkServerTrusted(aA.java:28)
22:13:36  	at com.ibm.jsse2.D.a(D.java:588)
22:13:36  	... 29 more
22:13:36  Caused by: java.security.cert.CertPathBuilderException: PKIXCertPathBuilderImpl could not build a valid CertPath.; internal cause is:
22:13:36  	java.security.cert.CertPathValidatorException: The certificate issued by CN=DigiCert Global Root G2, OU=www.digicert.com, O=DigiCert Inc, C=US is not trusted; internal cause is:
22:13:36  	java.security.cert.CertPathValidatorException: Certificate chaining error
22:13:36  	at com.ibm.security.cert.PKIXCertPathBuilderImpl.engineBuild(PKIXCertPathBuilderImpl.java:422)
22:13:36  	at java.security.cert.CertPathBuilder.build(CertPathBuilder.java:268)
22:13:36  	at com.ibm.jsse2.util.f.a(f.java:120)
22:13:36  	... 35 more
22:13:36  Caused by: java.security.cert.CertPathValidatorException: The certificate issued by CN=DigiCert Global Root G2, OU=www.digicert.com, O=DigiCert Inc, C=US is not trusted; internal cause is:
22:13:36  	java.security.cert.CertPathValidatorException: Certificate chaining error
22:13:36  	at com.ibm.security.cert.BasicChecker.<init>(BasicChecker.java:111)
22:13:36  	at com.ibm.security.cert.PKIXCertPathValidatorImpl.engineValidate(PKIXCertPathValidatorImpl.java:199)
22:13:36  	at com.ibm.security.cert.PKIXCertPathBuilderImpl.myValidator(PKIXCertPathBuilderImpl.java:749)
22:13:36  	at com.ibm.security.cert.PKIXCertPathBuilderImpl.buildCertPath(PKIXCertPathBuilderImpl.java:661)
22:13:36  	at com.ibm.security.cert.PKIXCertPathBuilderImpl.buildCertPath(PKIXCertPathBuilderImpl.java:607)
22:13:36  	at com.ibm.security.cert.PKIXCertPathBuilderImpl.engineBuild(PKIXCertPathBuilderImpl.java:368)
22:13:36  	... 37 more
22:13:36  Caused by: java.security.cert.CertPathValidatorException: Certificate chaining error
22:13:36  	at com.ibm.security.cert.CertPathUtil.findIssuer(CertPathUtil.java:316)
22:13:36  	at com.ibm.security.cert.BasicChecker.<init>(BasicChecker.java:108)
22:13:36  	... 42 more
22:13:36
```

</details>


---

我尝试从 Artifactory 下载 `certificate.pem` 并运行以下命令导入证书，但在 AIX 7.1 上问题依旧：

```bash
/usr/java8_64/jre/bin/keytool -importcert \
  -alias cacertalias \
  -keystore /usr/java8_64/jre/lib/security/cacerts \
  -file /path/to/your/certificate.pem
````

奇怪的是，在 **Windows、Linux 和 AIX 7.3** 构建机上无法复现该问题。

---

## 差异分析

唯一的区别是 **Java 运行时版本**。

在有问题的 **AIX 7.1** 构建机上，我使用的是共享 Java 运行时：

```bash
/tools/AIX-7.1/Java8_64-8.0.0.401/usr/java8_64/bin/java -version
java version "1.8.0"
Java(TM) SE Runtime Environment (build pap6480sr4fp1-20170215_01(SR4 FP1))
...
JCL - 20170215_01 based on Oracle jdk8u121-b13
```

而该机器上其实还有另一个本地安装的 Java 运行时：

```bash
/usr/java8_64/bin/java -version
java version "1.8.0_241"
Java(TM) SE Runtime Environment (build 8.0.6.5 - pap6480sr6fp5-20200111_02(SR6 FP5))
...
JCL - 20200110_01 based on Oracle jdk8u241-b07
```

---

## 解决方法

我将 Jenkins 节点的 `JavaPath` 从：

```
/tools/AIX-7.1/Java8_64-8.0.0.401/usr/java8_64/bin/java
```

改为：

```
/usr/java8_64/bin/java
```

然后断开并重新启动 Jenkins Agent，问题就解决了。

---

我不太清楚具体原因，可能与 Java 运行时自带的证书存储（cacerts）版本或证书链支持有关。
如果你对此有更多见解，欢迎在评论区留言告诉我。

---

转载本文请注明作者与出处，禁止商业用途。欢迎关注公众号「DevOps攻城狮」。
