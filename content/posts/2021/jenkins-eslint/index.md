---
title: 解决 ESlint HTML 报告在 Jenkins 作业中无法正常显示的问题
summary: |
  本文记录了 ESlint HTML 报告在 Jenkins 中因内容安全策略（CSP）限制而无法正确显示的问题，并介绍了如何通过修改 Jenkins 配置使报告正常加载。
tags:
  - ESlint
  - Jenkins
  - Troubleshooting
date: 2021-06-07
author: shenxianpeng
---

在将 ESlint 报告集成到 Jenkins 时，我遇到了一个问题：

- 本地打开 `eslint-report.html` 显示正常
- 上传到 Jenkins 并通过 [HTML Publisher](https://plugins.jenkins.io/htmlpublisher/) 插件展示时，报告样式和脚本无法加载
- 其他 HTML 报告在 Jenkins 中显示正常，只有 ESlint 报告有问题
- 将 Jenkins 中的 `eslint-report.html` 下载到本地后又能正常显示

这让我怀疑是 Jenkins 的安全策略导致的，最终在 [Stack Overflow](https://stackoverflow.com/questions/34315723/jenkins-error-blocked-script-execution-in-url-because-the-documents-frame/46197356?stw=2#46197356) 找到了答案。

---

## 解决步骤

1. 打开 Jenkins 首页  
2. 进入 **Manage Jenkins**  
3. 点击 **Script Console**  
4. 在控制台中粘贴以下代码并执行  

```java
System.setProperty("hudson.model.DirectoryBrowserSupport.CSP", "")
```

5. 执行后刷新页面，CSS 和 JS 就能正常加载

---

## 原因说明

Jenkins 引入了新的 [Content Security Policy (CSP)](https://www.jenkins.io/doc/book/security/configuring-content-security-policy/)
在 Chrome 控制台中查看 Elements 时会看到类似 `No frames allowed` 的提示，这正是导致 ESlint 报告无法加载样式和脚本的原因。

通过清空 `hudson.model.DirectoryBrowserSupport.CSP`，我们允许 Jenkins 在 HTML 报告中加载 CSS 和 JS，从而解决了问题。

---

📌 提示：此方法会放宽安全策略，请在内网环境或可信项目中使用。
