---
title: Explain Error Plugin Major Update — AI Auto-Fix, Usage Management, and More AI Providers
summary: |
    The Explain Error Plugin has recently received several important updates: AI Auto-Fix for automatically creating fix PRs, usage statistics and quota management, and added support for four new AI providers: DeepSeek, Qwen, Azure OpenAI, and Custom Okta.
tags:
  - Jenkins
  - AI
authors:
  - shenxianpeng
date: 2026-04-25
series: ["Explain Error Plugin"]
series_order: 5
---

It's been over two months since the last update article. The [Explain Error Plugin][1] iteration hasn't stopped; instead, it has received a wave of intensive updates. Today, I'll clarify them all at once.

---

## AI Auto-Fix: Automatically Create Fix PRs After Build Failures

This is the biggest feature in the past two months.

Previously, the plugin's positioning was "telling developers why the build failed." AI analyzed logs, provided suggestions, but you still had to make the changes yourself.

[AI Auto-Fix][2] completes this closed loop—when enabled, upon a build failure, the plugin will **automatically analyze errors, generate code fixes, create branches, and submit PRs**. It supports GitHub, GitLab, Bitbucket Cloud, and their self-hosted versions.

Multiple layers of protection have been implemented for security: path traversal checks, skipping low-confidence changes, skipping empty changes. By default, it only allows modifications to build configuration files (`pom.xml`, `*.properties`, `*.yml`, etc.), and does not touch business code.

To use in Pipeline, only a few lines of configuration are needed:

```groovy
explainError(
    autoFix: true,
    autoFixCredentialsId: 'github-token',
    autoFixAllowedPaths: 'pom.xml,*.properties,*.yml'
)
```

---

## Usage Statistics and Quota Management

As the number of plugin users grows, a natural question arises: **How many times has AI been invoked? How much did it cost?**

### Usage Statistics

[Usage Statistics][3] provides intuitive visualization on the **Manage Jenkins → Explain Error Plugin - Usage Statistics** page: total invocations, current month's usage, and Top 10 project rankings.

### Usage Quota

[Usage Quota][4] allows you to control costs. It supports both global and folder levels, with invocation limits configurable by hour or day. Logs will clearly indicate when the limit is exceeded, preventing additional costs.

### Metrics Export

Through [MetricsUsageRecorder][5], invocation statistics are automatically exposed to the Jenkins Metrics plugin, facilitating integration with external monitoring systems.

---

## Four New AI Providers

### Custom Okta AI

Submitted by community contributor [@mapham][6] via [PR #138][7]. Supports OAuth authentication flow for enterprise Okta gateways, adapting to corporate scenarios with Okta unified authentication.

### Azure OpenAI

[PR #147][8] adds support for Azure OpenAI Service. Simply configure Azure endpoint, deployment, and API version through Jenkins Credentials Management.

### DeepSeek

[PR #149][9] adds support for DeepSeek, with the default model `deepseek-v4-flash`. It integrates using an OpenAI-compatible API, offering high cost-performance.

### Qwen

Also in [PR #149][9], support for Tongyi Qianwen (Qwen) has been added, with the default model `qwen-plus`, integrated via Alibaba Cloud DashScope.

Current supported Providers:

| Provider | Description |
|----------|-------------|
| OpenAI | Default provider |
| Google Gemini | Joined in August 2025 |
| Ollama | Local/intranet deployment |
| AWS Bedrock | AWS ecosystem |
| Custom Okta AI | Okta enterprise gateway |
| Azure OpenAI | Azure managed service |
| DeepSeek | High cost-performance |
| Qwen | Alibaba Cloud DashScope |

---

## Bug Fixes and Experience Optimizations

**Fixed log extraction failure in specific Pipeline patterns** ([PR #109][10]): In scenarios combining `catchError` + `sh(returnStatus: true)` + `error()`, failed logs could not be extracted correctly previously. Fixed by community contributor [@lidiams96][10].

**Fixed NPE when Provider is not configured** ([PR #126][11]): A null pointer exception is no longer thrown when the plugin is newly installed but no AI provider is configured.

**Default Provider set to OpenAI** ([PR #137][12]): Consistent with documentation behavior, OpenAI is automatically used when not configured. Submitted by community contributor [@donhui][12].

**Fixed connection issues in intranet proxy environments** ([PR #146][13]): The plugin now reads Jenkins proxy configurations, allowing normal access to external AI services even in intranet environments.

---

## Summary

| Feature | Type |
|---------|-----------------------------|
| AI Auto-Fix | Major Feature |
| Usage Statistics + Quota + Metrics | New Features |
| Custom Okta AI / Azure OpenAI / DeepSeek / Qwen | New Providers |
| catchError Log Fix / NPE Fix / Proxy Support / Default Provider | Bug Fixes & Experience Optimizations |

If you encounter any problems or have suggestions during use, feel free to raise an Issue on [GitHub][14]. Community contributions are also welcome—Custom Okta AI, catchError fix, and default Provider fix in this update all came from community contributors.

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