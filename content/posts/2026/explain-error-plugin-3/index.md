---
title: Explain Error Plugin 重磅更新：AI 自动修复、用量管控与更多 AI 提供商
summary: |
    Explain Error Plugin 近期迎来多个重要更新：AI Auto-Fix 自动创建修复 PR、用量统计与配额管控、以及新增对 DeepSeek、Qwen、Azure OpenAI、Custom Okta 四个新 AI 提供商的支持。
tags:
  - Jenkins
  - AI
authors:
  - shenxianpeng
date: 2026-04-25
series: ["Explain Error Plugin"]
series_order: 5
---

距离上次更新文章已经过去两个多月了。[Explain Error Plugin][1] 的迭代并没有停下来，反而迎来了一波密集更新。今天一次性梳理清楚。

---

## AI Auto-Fix：构建失败后自动创建修复 PR

这是这两个月来最大的功能。

过去插件的定位是"告诉开发者构建为什么失败"。AI 分析日志、给出建议，剩下还得你自己动手改。

[AI Auto-Fix][2] 把这个闭环补上了——开启后，构建失败时插件会**自动分析错误、生成代码修复、创建分支、提交 PR**。支持 GitHub、GitLab、Bitbucket Cloud 及各自的自托管版本。

安全上做了多层防护：路径穿越检查、低置信度跳过、空变更跳过，默认只允许修改构建配置文件（`pom.xml`、`*.properties`、`*.yml` 等），不碰业务代码。

在 Pipeline 中使用只需几行配置：

```groovy
explainError(
    autoFix: true,
    autoFixCredentialsId: 'github-token',
    autoFixAllowedPaths: 'pom.xml,*.properties,*.yml'
)
```

---

## 用量统计与配额管控

插件用户多了之后，一个很自然的问题：**到底调用了多少次 AI？花了多少钱？**

### 用量统计

[用量统计][3] 在 **Manage Jenkins → Explain Error Plugin - Usage Statistics** 页面提供了直观的可视化：总调用次数、本月用量、Top 10 项目排名。

### 用量配额

[用量配额][4] 让你能控制成本。支持全局和文件夹两个层级，可按小时或天设置调用上限。超限后日志会明确提示，不会产生额外费用。

### Metrics 导出

通过 [MetricsUsageRecorder][5] 自动向 Jenkins Metrics 插件暴露调用统计，方便接入外部监控。

---

## 四个新的 AI 提供商

### Custom Okta AI

社区贡献者 [@mapham][6] 提交的 [PR #138][7]。支持企业 Okta 网关的 OAuth 认证流程，适配 Okta 统一认证的企业场景。

### Azure OpenAI

[PR #147][8] 添加了对 Azure OpenAI 服务的支持。通过 Jenkins 凭证管理，配置 Azure endpoint、deployment 和 API version 即可。

### DeepSeek

[PR #149][9] 支持了 DeepSeek，默认模型 `deepseek-v4-flash`。使用 OpenAI 兼容接口接入，性价比很高。

### Qwen

同样在 [PR #149][9] 中，添加了通义千问（Qwen）的支持，默认模型 `qwen-plus`，通过阿里云 DashScope 接入。

当前支持的 Provider 一览：

| Provider | 说明 |
|----------|------|
| OpenAI | 默认 provider |
| Google Gemini | 2025 年 8 月加入 |
| Ollama | 本地/内网部署 |
| AWS Bedrock | AWS 生态 |
| Custom Okta AI | Okta 企业网关 |
| Azure OpenAI | Azure 托管服务 |
| DeepSeek | 高性价比 |
| Qwen | 阿里云 DashScope |

---

## Bug 修复与体验优化

**修复特定 Pipeline 模式下的日志提取失败**（[PR #109][10]）：`catchError` + `sh(returnStatus: true)` + `error()` 组合场景中，之前无法正确提取失败日志。由社区贡献者 [@lidiams96][10] 修复。

**修复未配置 Provider 时的 NPE**（[PR #126][11]）：新安装插件但未配置 AI 提供商时不再抛空指针异常。

**默认 Provider 设为 OpenAI**（[PR #137][12]）：与文档行为一致，未配置时自动使用 OpenAI。由社区贡献者 [@donhui][12] 提交。

**修复内网代理环境下的连接问题**（[PR #146][13]）：插件现在会读取 Jenkins 代理配置，内网环境也能正常访问外部 AI 服务。

---

## 小结

| 功能 | 类型 |
|------|------|
| AI Auto-Fix | 重大功能 |
| 用量统计 + 配额 + Metrics | 新功能 |
| Custom Okta AI / Azure OpenAI / DeepSeek / Qwen | 新 Provider |
| catchError 日志修复 / NPE 修复 / 代理支持 / 默认 Provider | Bug 修复 & 体验优化 |

如果你在使用过程中有任何问题或建议，欢迎在 [GitHub][14] 上提 Issue。也欢迎社区贡献——这次更新中 Custom Okta AI、catchError 修复、默认 Provider 修复都来自社区贡献者。

[1]: https://plugins.jenkins.io/explain-error/
[2]: https://github.com/jenkinsci/explain-error-plugin/pull/120
[3]: https://github.com/jenkinsci/explain-error-plugin/pull/124
[4]: https://github.com/jenkinsci/explain-error-plugin/pull/140
[5]: https://github.com/jenkinsci/explain-error-plugin/pull/135
[6]: https://github.com/mapham
[7]: https://github.com/jenkinsci/explain-error-plugin/pull/138
[8]: https://github.com/jenkinsci/explain-error-plugin/pull/147
[9]: https://github.com/jenkinsci/explain-error-plugin/pull/149
[10]: https://github.com/jenkinsci/explain-error-plugin/pull/109
[11]: https://github.com/jenkinsci/explain-error-plugin/pull/126
[12]: https://github.com/jenkinsci/explain-error-plugin/pull/137
[13]: https://github.com/jenkinsci/explain-error-plugin/pull/146
[14]: https://github.com/jenkinsci/explain-error-plugin
