---
title: Jenkins Explain Error Plugin 支持 Google Gemini 了！🤖
summary: 本文介绍了 Jenkins Explain Error Plugin 的新功能，支持 Google Gemini 模型进行错误分析，并提供了配置方法和示例视频。
tags:
  - Jenkins
  - AI
author: shenxianpeng
date: 2025-08-03
---

上周我发布了 [Jenkins Explain Error Plugin](https://shenxianpeng.github.io/2025/07/explain-error-plugin/)，旨在帮助 Jenkins 用户通过内置 AI 来更快地分析和解决 Jenkins 构建中的错误。

有读者朋友在评论区提到，希望插件支持 Google Gemini 模型进行错误分析，因为他们公司只能使用 Google 的 AI 服务。

今天，我很高兴地宣布，这个插件现在已经支持 Google Gemini 模型了！🎉

## 插件更新

- 新增对 Google Gemini 模型的支持
- 优化文档并补充了示例视频

## 如何使用 Google Gemini

在开始使用之前，请确保插件已更新到最新版本。
你可以在 Jenkins 插件管理器中找到 Explain Error Plugin，并将其升级到最新版

更新后，在插件配置中，你可以选择使用 Google Gemini 模型进行错误分析。只需在 `Manage Jenkins → Configure System` 页面下的 **Explain Error Plugin Configuration** 中，将模型设置为 `Google Gemini`，并提供相应的 API 地址和密钥。



![Explain Error Plugin Configuration](explain-error-plugin-configuration.png)

点击 Test Configuration，确保你的 Google Gemini API Key、URL 和 Model 均已正确填写且可正常访问。

## 插件示例视频

考虑到不少用户可能对插件的使用还不够熟悉，我录制了一段简短的视频，演示如何在 Jenkins 中使用 Explain Error Plugin 进行错误分析。

你可以在 [YouTube](https://www.youtube.com/watch?v=rPI9PMeDQ2o) 上观看这个视频。

## 结语

如果你在使用过程中有任何问题或建议，欢迎在 GitHub 上提交 issue，或在评论区留言。

仓库地址：[jenkinsci/explain-error-plugin](https://github.com/jenkinsci/explain-error-plugin)

欢迎 Star ⭐️ 支持一下！

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
