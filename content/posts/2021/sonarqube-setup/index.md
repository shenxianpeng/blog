---
title: SonarQube 安装与常见问题排查
summary: |
  本文记录了 SonarQube 的安装步骤，包括 LDAP 配置与 PostgreSQL 数据库设置，并附带一些常见问题的排查方法。
tags:
  - SonarQube
  - LDAP
  - PostgreSQL
date: 2021-08-05
aliases:
  - /2021/08/sonarqube-setup/
authors:
  - shenxianpeng
---

## 背景

相较于 Jenkins、Artifactory 等 DevOps 工具，SonarQube 的安装与配置并不算简单。除了启动脚本外，还需要提前准备数据库、在配置文件中设置 LDAP 等。

这里记录我在安装 SonarQube 9.0.1 版本时的关键步骤（LDAP、PostgreSQL 等），以便后续参考，也希望能帮到其他人。

---

## 前置条件与下载

1. **JRE/JDK 11 必须已安装**  
   官方要求参考：<https://docs.sonarqube.org/latest/requirements/requirements/>

2. **下载 SonarQube**

    ```bash
    wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-9.0.1.46107.zip
    unzip sonarqube-9.0.1.46107.zip
    cd sonarqube-9.0.1.46107/bin/linux-x86-64
    sh sonar.sh console
    ```

---

## 切换 Java 版本

CentOS 7 默认 Java 版本为 1.8.0，但 SonarQube 要求 JDK 11。若机器已安装 JDK 11，可使用 `alternatives` 切换：

```bash
alternatives --config java
# 选择 java-11-openjdk
java -version
```

---

## 安装数据库

SonarQube 需依赖外部数据库，支持 Oracle、PostgreSQL、SQL Server 等。推荐使用开源、轻量的 PostgreSQL。
安装方法参考：[https://www.postgresql.org/download/linux/redhat/](https://www.postgresql.org/download/linux/redhat/)

---

## 常见问题

### 1. 配置 PostgreSQL 连接

在 `sonar.properties` 中设置，例如：

```properties
sonar.jdbc.username=sonarqube
sonar.jdbc.password=mypassword
sonar.jdbc.url=jdbc:postgresql://localhost/sonarqube
```

---

### 2. 配置 LDAP 登录

```properties
sonar.security.realm=LDAP
ldap.url=ldap://den.example-org:389
ldap.bindDn=user@example-org.com
ldap.bindPassword=mypassword
ldap.authentication=simple
ldap.user.baseDn=DC=example-org,DC=com
ldap.user.request=(&(objectClass=user)(sAMAccountName={login}))
ldap.user.realNameAttribute=cn
ldap.user.emailAttribute=email
```

---

### 3. LDAP 登录缓慢

注释掉以下配置可提升首次登录速度：

```properties
# ldap.followReferrals=false
```

参考：[https://community.sonarsource.com/t/ldap-login-takes-2-minutes-the-first-time/1573/7](https://community.sonarsource.com/t/ldap-login-takes-2-minutes-the-first-time/1573/7)

---

### 4. 修复 "Could not resolve file paths in lcov.info"

当使用 `sonar.javascript.lcov.reportPaths=coverage/lcov.info` 时，如果路径包含 `..\`，SonarQube 会无法解析。
解决方法：运行 `sed` 移除前缀。

```bash
sed -i 's/\..\\//g' coverage/lcov.info
```

---

### 5. 输出更多日志

将：

```properties
sonar.log.level=INFO
```

改为：

```properties
sonar.log.level=DEBUG
```

重启 SonarQube 生效。

---

## 完整 `sonar.properties` 示例

可参考：[Gist 链接](https://gist.github.com/shenxianpeng/a1eec786210b421f8be34e3263f1a002) 或下方配置：

```properties
sonar.jdbc.username=sonarqube
sonar.jdbc.password=mypassword
sonar.jdbc.url=jdbc:postgresql://localhost/sonarqube
sonar.web.host=10.118.245.19
sonar.web.port=9000
sonar.security.realm=LDAP
ldap.url=ldap://den.example-org:389
ldap.bindDn=user@example-org.com
ldap.bindPassword=mypassword
ldap.authentication=simple
ldap.user.baseDn=DC=example-org,DC=com
ldap.user.request=(&(objectClass=user)(sAMAccountName={login}))
ldap.user.realNameAttribute=cn
ldap.user.emailAttribute=email
sonar.search.javaAdditionalOpts=-Dbootstrap.system_call_filter=false
sonar.log.level=INFO
sonar.path.data=/var/sonarqube/data
sonar.path.temp=/var/sonarqube/temp
```

---

转载本文请注明作者与出处，禁止商业用途。欢迎关注公众号「DevOps攻城狮」。
