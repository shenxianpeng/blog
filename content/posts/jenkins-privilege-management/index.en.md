---
title: Jenkins—privilege management
summary: This article introduces how to manage permissions in Jenkins, including how to set access and execution permissions for Jobs, to ensure a secure and efficient CI/CD process.
tags:
  - Jenkins
date: 2019-09-24
author: shenxianpeng
---

How to manage different strategies for different Jobs in Jenkins. For example, everyone can view a certain Job, but only some people can execute it. In this case, you need to set Job execution permissions.

The plugin used here is Role-based Authorization Strategy. After successful installation, open the Job to be set, and configure as follows:


![Enable project-based security](jenkins-privilege-management.png)