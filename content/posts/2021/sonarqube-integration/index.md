---
title: SonarQube Community Edition 如何集成到项目中
summary: |
  本文介绍如何将 SonarQube Community Edition 集成到 Maven、Gradle 及其他类型项目中，包括必要的配置和 Jenkins 流水线示例。
tags:
  - SonarQube
  - Gradle
date: 2021-09-18
author: shenxianpeng
---

在你搭建好 SonarQube 实例后，需要将其与项目集成。

由于我使用的是 **Community Edition**，它不支持 C/C++ 项目，所以这里只演示 Maven、Gradle 及其他类型项目的集成方法。

假设在 SonarQube 中的项目名称和 ID 都为 `test-demo`，并通过 Jenkins 进行构建。

---

## Maven 项目集成

1. 在 `pom.xml` 中添加：

    ```xml
    <properties>
      <sonar.projectKey>test-demo</sonar.projectKey>
    </properties>
    ```

2. 在 `Jenkinsfile` 中添加：

    ```groovy
    stage('SonarQube Analysis') {
      def mvn = tool 'Default Maven'
      withSonarQubeEnv() {
        sh "${mvn}/bin/mvn sonar:sonar"
      }
    }
    ```

---

## Gradle 项目集成

1. 在 `build.gradle` 中添加：

    ```gradle
    plugins {
      id "org.sonarqube" version "3.3"
    }

    sonarqube {
      properties {
        property "sonar.projectKey", "test-demo"
      }
    }
    ```

2. 在 `Jenkinsfile` 中添加：

    ```groovy
    stage('SonarQube Analysis') {
      withSonarQubeEnv() {
        sh "./gradlew sonarqube"
      }
    }
    ```

---

## 其他类型项目（JS、TS、Python 等）

1. 在代码仓库根目录创建 `sonar-project.properties` 文件：

    ```text
    sonar.projectKey=test-demo
    ```

2. 在 `Jenkinsfile` 中添加：

    ```groovy
    stage('SonarQube Analysis') {
      def scannerHome = tool 'SonarScanner'
      withSonarQubeEnv() {
        sh "${scannerHome}/bin/sonar-scanner"
      }
    }
    ```

---

更多关于 SonarQube 集成的方法，可以访问你本地的 SonarQube 文档页面：  
[http://localhost:9000/documentation](http://localhost:9000/documentation)

---

转载本文请注明作者与出处，禁止商业用途。欢迎关注公众号「DevOps攻城狮」。
