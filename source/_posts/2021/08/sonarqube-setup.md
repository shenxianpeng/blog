---
title: The problems encountered while installing SonarQube
tags:
  - SonarQube
  - LDAP
  - PostgreSQL
categories:
  - SonarQube
date: 2021-08-05 12:30:22
author: shenxianpeng
---

## Backgroud

In my opinion, SonarQube is not a very easy setup DevOps tool to compare with Jenkins, Artifactory. You can't just run some script under the bin folder to let the server boot up.

You must have an installed database, configuration LDAP in the config file, etc.

So I'd like to document some important steps for myself, like setup LDAP or PostgreSQL when I install SonarQube of v9.0.1. It would be better if it can help others.

## Prerequisite and Download

1. Need to be installed JRE/JDK 11 on the running machine.

    Here is the prerequisites overview: https://docs.sonarqube.org/latest/requirements/requirements/

2. Download SonarQube: https://www.sonarqube.org/downloads/

    ```bash
    cd sonarqube/
    ls
    wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-9.0.1.46107.zip

    unzip sonarqube-9.0.1.46107.zip
    cd  sonarqube-9.0.1.46107/bin/linux-x86-64
    sh sonar.sh console
    ```

## Change Java version

I installed SonarQube on CentOS 7 machine, the Java version is OpenJDK 1.8.0_242 by default, but the prerequisite shows at least need JDK 11. There is also JDK 11 available on my machine, so I just need to change the Java version.

I recommend using the `alternatives` command change Java version，refer as following:

```bash
$ java -version
openjdk version "1.8.0_242"
OpenJDK Runtime Environment (build 1.8.0_242-b08)
OpenJDK 64-Bit Server VM (build 25.242-b08, mixed mode)

$ alternatives --config java

There are 3 programs which provide 'java'.

  Selection    Command
-----------------------------------------------
   1           java-1.7.0-openjdk.x86_64 (/usr/lib/jvm/java-1.7.0-openjdk-1.7.0.251-2.6.21.1.el7.x86_64/jre/bin/java)
*+ 2           java-1.8.0-openjdk.x86_64 (/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.242.b08-1.el7.x86_64/jre/bin/java)
   3           java-11-openjdk.x86_64 (/usr/lib/jvm/java-11-openjdk-11.0.12.0.7-0.el7_9.x86_64/bin/java)

Enter to keep the current selection[+], or type selection number: 3
$ java -version
openjdk version "11.0.12" 2021-07-20 LTS
OpenJDK Runtime Environment 18.9 (build 11.0.12+7-LTS)
OpenJDK 64-Bit Server VM 18.9 (build 11.0.12+7-LTS, mixed mode, sharing)
```

## Install Database

SonarQube needs you to have installed a database. It supports several database engines, like Microsoft SQL Server, Oracle, and PostgreSQL. Since PostgreSQL is open source, light, and easy to install, so I choose PostgreSQL as its database.

How to download and install PostgreSQL please see this page: https://www.postgresql.org/download/linux/redhat/

## Problems

### 1. How to establish a connection with SonarQube and PostgreSQL

Please refer to the `sonar.properties` file at the end of this post.

### 2. How to setup LDAP for users to log in

```bash
sonar.security.realm=LDAP
ldap.url=ldap://den.exmaple-org:389
ldap.bindDn=user@exmaple-org.com
ldap.bindPassword=mypassword
ldap.authentication=simple
ldap.user.baseDn=DC=exmaple-org,DC=com
ldap.user.request=(&(objectClass=user)(sAMAccountName={login}))
ldap.user.realNameAttribute=cn
ldap.user.emailAttribute=email
```

### 3. How to fix LDAP login SonarQube is very slowly

Comment out `ldap.followReferrals=false` in sonar.properties file would be help.

Related post: https://community.sonarsource.com/t/ldap-login-takes-2-minutes-the-first-time/1573/7

### 4. How to output to more logs

To output more logs, change `sonar.log.level=INFO` to `sonar.log.level=DEBUG` in below.

> Note: all above changes of `sonar.properties` need to restart the SonarQube instance to take effect.

## Final `sonar.properties`

For the `sonar.properties` file, please see below or [link](https://gist.github.com/shenxianpeng/a1eec786210b421f8be34e3263f1a002)

<!-- more -->
```bash
# DATABASE
#
# IMPORTANT:
# - The embedded H2 database is used by default. It is recommended for tests but not for
#   production use. Supported databases are Oracle, PostgreSQL and Microsoft SQLServer.
# - Changes to database connection URL (sonar.jdbc.url) can affect SonarSource licensed products.

# User credentials.
# Permissions to create tables, indices and triggers must be granted to JDBC user.
# The schema must be created first.
sonar.jdbc.username=sonarqube
sonar.jdbc.password=mypassword


#----- PostgreSQL 9.6 or greater
# By default the schema named "public" is used. It can be overridden with the parameter "currentSchema".
sonar.jdbc.url=jdbc:postgresql://localhost/sonarqube


# Binding IP address. For servers with more than one IP address, this property specifies which
# address will be used for listening on the specified ports.
# By default, ports will be used on all IP addresses associated with the server.
sonar.web.host=10.118.245.19

# Web context. When set, it must start with forward slash (for example /sonarqube).
# The default value is root context (empty value).
sonar.web.context=
# TCP port for incoming HTTP connections. Default value is 9000.
sonar.web.port=9000

# LDAP CONFIGURATION

# Follow or not referrals. See http://docs.oracle.com/javase/jndi/tutorial/ldap/referral/jndi.html (default: true)
ldap.followReferrals=false

# Enable the LDAP feature
sonar.security.realm=LDAP

# Set to true when connecting to a LDAP server using a case-insensitive setup.
# sonar.authenticator.downcase=true

# URL of the LDAP server. Note that if you are using ldaps, then you should install the server certificate into the Java truststore.
ldap.url=ldap://den.exmaple-org:389

# Bind DN is the username of an LDAP user to connect (or bind) with. Leave this blank for anonymous access to the LDAP directory (optional)
ldap.bindDn=user@exmaple-org.com

# Bind Password is the password of the user to connect with. Leave this blank for anonymous access to the LDAP directory (optional)
ldap.bindPassword=mypassword

# Possible values: simple | CRAM-MD5 | DIGEST-MD5 | GSSAPI See http://java.sun.com/products/jndi/tutorial/ldap/security/auth.html (default: simple)
ldap.authentication=simple

# USER MAPPING

# Distinguished Name (DN) of the root node in LDAP from which to search for users (mandatory)
ldap.user.baseDn=DC=exmaple-org,DC=com

# LDAP user request. (default: (&(objectClass=inetOrgPerson)(uid={login})) )
ldap.user.request=(&(objectClass=user)(sAMAccountName={login}))

# Attribute in LDAP defining the user’s real name. (default: cn)
ldap.user.realNameAttribute=cn

# Attribute in LDAP defining the user’s email. (default: mail)
ldap.user.emailAttribute=email


sonar.search.javaAdditionalOpts=-Dbootstrap.system_call_filter=false

# Global level of logs (applies to all 4 processes).
# Supported values are INFO (default), DEBUG and TRACE
sonar.log.level=INFO

# Paths to persistent data files (embedded database and search index) and temporary files.
# Can be absolute or relative to installation directory.
# Defaults are respectively <installation home>/data and <installation home>/temp
sonar.path.data=/var/sonarqube/data
sonar.path.temp=/var/sonarqube/temp
```
