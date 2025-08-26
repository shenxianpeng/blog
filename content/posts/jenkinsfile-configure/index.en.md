---
title: Jenkinsfile Configuration
summary: This article introduces how to configure Jenkins Pipeline using Jenkinsfile, including examples of build, test, and release stages, and how to handle email notifications.
date: 2018-04-14
tags:
- Jenkins
- Pipeline
translate: fase
author: shenxianpeng
---

Recently, while working on DevOps Build, I learned about Jenkins Pipeline functionality, and the Jenkinsfile is worth mentioning.

Below is my configured Jenkinsfile and a brief explanation. For more information about [Pipeline](https://jenkins.io/doc/book/pipeline/), please refer to the official documentation.


```JavaScript
pipeline {
    agent any

    stages {
        // Build stage
        stage('Build') {
            steps {
                echo 'Building...'
                bat 'npm run build webcomponent-sample'
            }
        }

        // Unit Test stage
        stage('Unit Test') {
            steps {
                echo 'Unit Testing...'
                bat 'npm test webcomponent-sample'
            }

            post {
                success {
                // Generate report after successful execution
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: false,
                    keepAll: true,
                    reportDir: 'components/webcomponent-sample/coverage/chrome',
                    reportFiles: 'index.html',
                    reportName: 'RCov Report'
                    ]
                }
            }
        }

        // E2E Test stage
        stage('E2E Test') {
            steps {
                bat 'node nightwatch e2e/demo/test.js'
            }
        }

        stage('Release') {
            steps {
                echo 'Release...'
            }
        }
    }

    post {
        // Triggered on successful execution
        success {
            mail bcc: 'email@qq.com',
            body: "<b>Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br>Build URL: ${env.BUILD_URL} ", cc: '', charset: 'UTF-8', from: 'jenkins@qq.com', mimeType: 'text/html', replyTo: '', subject: "SUCCESS: Project Name -> ${env.JOB_NAME}", to: "";
        }

        // Triggered on failed execution
        failure {
            mail bcc: 'email@qq.com',
            body: "<b>Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br>Build URL: ${env.BUILD_URL} ", cc: '', charset: 'UTF-8', from: 'jenkins@qq.com', mimeType: 'text/html', replyTo: '', subject: "FAILURE: Project Name -> ${env.JOB_NAME}", to: "";
        }
    }
}
```