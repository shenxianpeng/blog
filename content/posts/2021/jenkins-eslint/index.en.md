---
title: Resolved problem that ESlint HTML report is not displayed correctly in Jenkins job
summary: |
  This article explains how to resolve the issue of ESlint HTML report not displaying correctly in Jenkins jobs due to Content Security Policy restrictions, including the steps to configure Jenkins to allow the report to load properly.
tags:
  - ESlint
  - Jenkins
  - Troubleshooting
date: 2021-06-07
author: shenxianpeng
---

> I'm just documenting to myself that it was solved by following.

When I want to integrate the ESlint report with Jenkins. I encourage a problem

That is eslint-report.html display different with it on my local machine, and I also log to Jenkins server and grab the eslint-report.html to local, it works well.

I used [HTML Publisher](https://plugins.jenkins.io/htmlpublisher/) plugin to display the HTML report, but only the ESlint HTML report has problems other report work well, so I guess this problem may be caused by Jenkins.

Finally, I find it. (Stackoverflow [URL](https://stackoverflow.com/questions/34315723/jenkins-error-blocked-script-execution-in-url-because-the-documents-frame/46197356?stw=2#46197356))


## Follow the below steps for solution

1. Open the Jenkin home page.
2. Go to Manage Jenkins.
3. Now go to Script Console.
4. And in that console paste the below statement and click on Run.

```java
System.setProperty("hudson.model.DirectoryBrowserSupport.CSP", "")
```

5. After that, it will load CSS and JS.

According to Jenkins's new [Content Security Policy](https://www.jenkins.io/doc/book/security/configuring-content-security-policy/) and I saw `No frames allowed`.

That is exactly the error I get on chrome by right-clicking on Elements.
