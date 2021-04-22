---
title: How to download the entire folder artifacts when Artifactory "Download Folder functionality is disabled"?
tags:
  - JFrog
  - Artifactory
  - API
categories:
  - DevOps
date: 2021-04-22 23:47:49
author: shenxianpeng
---

## Problem

When you do contiguous integration with JFrog Artifactory when you want to download the entire folder artifacts, but IT doesn't enable this function, whatever some seasons.

For example, I want to use this API [Retrieve Folder or Repository Archive](https://www.jfrog.com/confluence/display/JFROG/Artifactory+REST+API#ArtifactoryRESTAPI-RetrieveFolderorRepositoryArchive)to download the entire folder artifacts.


Just visit the API URL

`https://den-artifactory.company.com/artifactory/api/archive/download/team-generic-release-den/project/abc/main/?archiveType=zip`

And an error message returned.

```
{
  "errors": [
    {
      "status": 403,
      "message": "Download Folder functionality is disabled."
    }
  ]
}
```

How can I get a workaround to download the entire folder artifacts programmatically? This post will show you how to use other [Artifactory REST API](https://www.jfrog.com/confluence/display/JFROG/Artifactory+REST+API) to get a workaround.

## Workaround








