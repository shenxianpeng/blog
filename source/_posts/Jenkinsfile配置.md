---
title: Jenkinsfile配置
date: 2018-04-14 13:07:49
tags: Jenkins
categories: CI/CD
---

最近在做有关DevOps Build的时候，学习了Jenkins的Pipeline的功能，不得不提到的就是Jenkinsfile这个文件。
以下面是我配置的Jenkinsfile文件及简单说明，更多有关[Pipeline](https://jenkins.io/doc/book/pipeline/)请看官方文档

```JavaScript
pipeline {
    agent any

    stages {
        // Build阶段
        stage('Build') {
            steps {
                echo 'Building...'
                bat 'npm run build webcomponent-sample'
            }
        }

        // 单元测试阶段
        stage('Unit Test') {
            steps {
                echo 'Unit Testing...'
                bat 'npm test webcomponent-sample'
            }

            post {
                success {
                // 执行成功后生产报告
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

        // E2E测试阶段
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
        // 执行成功是触发
        success {  
            mail bcc: 'email@qq.com',
            body: "<b>Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br>Build URL: ${env.BUILD_URL} ", cc: '', charset: 'UTF-8', from: 'jenkins@qq.com', mimeType: 'text/html', replyTo: '', subject: "SUCCESS: Project Name -> ${env.JOB_NAME}", to: "";    
        } 

        // 执行失败时触发
        failure {  
            mail bcc: 'email@qq.com',
            body: "<b>Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br>Build URL: ${env.BUILD_URL} ", cc: '', charset: 'UTF-8', from: 'jenkins@qq.com', mimeType: 'text/html', replyTo: '', subject: "FAILURE: Project Name -> ${env.JOB_NAME}", to: "";  
        }
    }
}
```
