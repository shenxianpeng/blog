---
title: Automatically commit code by Jenkins
date: 2019-05-12 21:21:55
tags:
- Jenkins
- Release
- Pipeline
categories:
- Jenkins
author: shenxianpeng
---

When we need to release a product, we should change copyright, build version, release month, release note...
How to modify multiple files automatically?
I used a Jenkins pipeline project, the project is parameterized(string parameter) and regular expressions to implement.

1. Here is the string parameter for copyright:

    * Name: copyright
    * Default Value: 1995—2019
    * Description: Copyright format:1995—2019

        ```bash
        stage('change copyrigh') {
            steps {
                sh label: '', script: 'sed -i -E "s/(1995—[0-9]{4})/${copyright}/" 1033/AutoRun.ini'
            }
        }
        ```

2. Here is the string parameter for build version:
    * Name: build_version
    * Default Value: 1.2.2.1002
    * Description: build version format: 1.2.2.1002

        ```bash
        stage('change build version') {
            steps {
                sh label: '', script: 'sed -i -E "s/([0-9].[0-9].[0-9].[0-9]{4})/${build_version}/" 1033/AutoRun.ini'
            }
        }
        ```

3. Here is the string parameter for build version:
    * Name: release_month
    * Default Value: May 2019
    * Description: release month format: May 2019

        ```bash
        stage('change release month') {
            steps {
                sh label: '', script: '''
                sed -i -E "s/([a-z]* 20[0-9]{2})/${release_month}/" 1033/AutoRun.ini
                sed -i -E "s/([a-z]* 20[0-9]{2})/${release_month}/" 1033/MainMenu.ini
                '''
            }
        }
        ```

4. push change to Git

    ```bash
    stage('git push to Git') {
        steps {
            sshagent(['8dd766ba-ac0f-4302-afa8-bee59c726dee']) {
                sh("git add 1033/AutoRun.ini")
                sh("git add 1033/MainMenu.ini")
                sh("git commit -m 'Bld # ${build_version}'")
                sh("git push -u origin master")
            }
        }
    }
    ```

5. Whole Jenkins Pipeline looks like:

    ```bash
    pipeline {
        agent {
            label 'master'
        }

        stages{
            stage('git clone') {
                steps{
                    git branch: 'master',
                    credentialsId: '8dd766ba-ac0f-4302-afa8-bee59c726dee',
                    url: 'git@github.com:shenxianpeng/blog.git'
                }
            }

            stage('change copyrigh') {
            steps {
                sh label: '', script: 'sed -i -E "s/(1995—[0-9]{4})/${copyright}/" 1033/AutoRun.ini'
            }
            }

            stage('change release month') {
            steps {
                sh label: '', script: '''
                sed -i -E "s/([a-z]* 20[0-9]{2})/${release_month}/" 1033/AutoRun.ini
                sed -i -E "s/([a-z]* 20[0-9]{2})/${release_month}/" 1033/MainMenu.ini
                '''
            }
            }

            stage('change build version') {
            steps {
                sh label: '', script: 'sed -i -E "s/([0-9].[0-9].[0-9].[0-9]{4})/${build_version}/" 1033/AutoRun.ini'
            }
            }

            stage('git push to Git') {
                steps {
                    sshagent(['8dd766ba-ac0f-4302-afa8-bee59c726dee']) {
                        sh("git add 1033/AutoRun.ini")
                        sh("git add 1033/MainMenu.ini")
                        sh("git commit -m 'Bld # ${build_version}'")
                        sh("git push -u origin master")
                    }
                }
            }
        }
    }
    ```
