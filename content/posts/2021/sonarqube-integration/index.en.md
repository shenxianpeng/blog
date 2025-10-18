---
title: How does SonarQube Community Edition integrate with the project
summary: |
  This article explains how to integrate SonarQube Community Edition with Maven, Gradle, and other projects, including the necessary configurations and Jenkins pipeline setup.
tags:
  - SonarQube
  - Gradle
date: 2021-09-18
authors:
  - shenxianpeng
---

After you have set up the SonarQube instance, you will need to integrate SonarQube with project.

Because I used the community edition version, it doesn't support the C/C++ project, so I only demo how to integrate with Maven, Gradle, and Others.

For example, the demo project name and ID in SonarQube are both `test-demo`, and I build with Jenkins.


## Build with Maven

1. Add the following to your `pom.xml` file:

    ```xml
    <properties>
      <sonar.projectKey>test-demo</sonar.projectKey>
    </properties>
    ```

2. Add the following code to your `Jenkinsfile`:

    ```Jenkinsfile
    stage('SonarQube Analysis') {
      def mvn = tool 'Default Maven';
      withSonarQubeEnv() {
        sh "${mvn}/bin/mvn sonar:sonar"
      }
    }
    ```

## Build with Gradle

1. Add the following to your `build.gradle` file:

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

2. Add the following code to your `Jenkinsfile`:

    ```Jenkinsfile
    stage('SonarQube Analysis') {
      withSonarQubeEnv() {
        sh "./gradlew sonarqube"
      }
    }
    ```

## Build with Other(for JS, TS, Python, ...)

1. Create a `sonar-project.properties` file in your repository and paste the following code:

    ```text
    sonar.projectKey=test-demo
    ```

2. Add the following code to your `Jenkinsfile`:

    ```Jenkinsfile
    stage('SonarQube Analysis') {
      def scannerHome = tool 'SonarScanner';
      withSonarQubeEnv() {
        sh "${scannerHome}/bin/sonar-scanner"
      }
    }
    ```

More about how to integrate with SonarQube, please visit your SonarQube instance documentation: http://localhost:9000/documentation
