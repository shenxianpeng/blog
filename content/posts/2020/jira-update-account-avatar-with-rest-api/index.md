---
title: 使用 REST API 更新 Jira Server 账号头像
summary: |
  介绍如何通过 Jira REST API 更新 Jira Server 账号的头像，并提供 Python 和 Postman 示例。
tags:
  - Jira
date: 2020-08-17
author: shenxianpeng
---

## 背景

在 CI/CD 中使用 **Jira Server** 账号（例如 `robot`）时，如果希望该账号在 Jira 中的头像更专业，但该账号无法登录 Jira GUI，就需要通过 **REST API** 更新头像。

以下提供 **Python** 与 **Postman** 两种示例。

---

## Python 示例

```python
import http.client

conn = http.client.HTTPSConnection("jira.your-company.com")

payload = """{
    "id": "24880",
    "isSelected": false,
    "isSystemAvatar": true,
    "urls": {
        "16x16": "https://jira.your-company.com/secure/useravatar?size=xsmall&avatarId=24880",
        "24x24": "https://jira.your-company.com/secure/useravatar?size=small&avatarId=24880",
        "32x32": "https://jira.your-company.com/secure/useravatar?size=medium&avatarId=24880",
        "48x48": "https://jira.your-company.com/secure/useravatar?avatarId=24880"
    }
}"""

headers = {
    "content-type": "application/json",
    "authorization": "Basic Ymx3bXY6SzhNcnk5ZGI=",  # Base64(username:password)
    "cache-control": "no-cache"
}

conn.request("PUT", "/rest/api/latest/user/avatar?username=robot", payload, headers)
res = conn.getresponse()
print(res.read().decode("utf-8"))
```

---

## Postman 示例

**URL & Method**

```
PUT https://jira.your-company.com/rest/api/latest/user/avatar?username=robot
```

**Authorization**

* Type: Basic Auth
* Username: `server-account-username`
* Password: `server-account-password`

**Body**

```json
{
  "id": "24880",
  "isSelected": false,
  "isSystemAvatar": true,
  "urls": {
    "16x16": "https://jira.your-company.com/secure/useravatar?size=xsmall&avatarId=24880",
    "24x24": "https://jira.your-company.com/secure/useravatar?size=small&avatarId=24880",
    "32x32": "https://jira.your-company.com/secure/useravatar?size=medium&avatarId=24880",
    "48x48": "https://jira.your-company.com/secure/useravatar?avatarId=24880"
  }
}
```

---

## 如何获取 avatar ID

1. 进入 Jira 个人资料页面。
2. 在头像选择界面右键查看图片地址。
3. URL 中的 `avatarId` 参数即为头像 ID。

示例：
`https://jira.your-company.com/secure/useravatar?avatarId=24880`

![find avatar id](find-avatar-id.png)
