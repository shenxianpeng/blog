---
title: Explain Error Plugin Adds Two Major Enterprise Features—Custom Context and Folder-Level Configuration
summary: |
    The Explain Error Plugin introduces two significant updates: support for custom context information and folder-level AI provider configurations. These two features make the plugin more flexible and robust for use in enterprise environments.
tags:
  - Jenkins
  - AI
authors:
  - shenxianpeng
date: 2026-02-13
---

The Explain Error Plugin has recently received two more significant feature updates. Both of these features were developed based on actual user feedback, making the plugin more flexible and powerful in enterprise environments.

These two new features are:

1.  **Custom Context Support** - Helping AI better understand your business scenarios
2.  **Folder-Level AI Provider Configuration** - Enabling different teams to use different AI services

## I. Custom Context Support

### Why is this feature needed?

When using AI to explain build errors, we often encounter this problem: **AI can identify errors, but it doesn't understand your specific business scenarios and environment information.**

For example:
- Your project uses a specific build environment or toolchain
- You want AI to provide solutions based on company best practices
- You need AI to consider specific constraints (e.g., not being able to upgrade a specific dependency version)

Through [PR #83][1], the plugin now supports adding **custom context information** at both the global configuration and Pipeline step levels. This information is passed to the AI to help generate more accurate and contextually relevant error explanations.

### How to use custom context

#### 1. Global Configuration

In Jenkins system configuration, you can set global custom context:

1.  Navigate to **Manage Jenkins** → **Configure System**
2.  Find the **Explain Error Plugin** configuration area
3.  Enter your context information in the **Custom Context** field

For example:
```
Our project runs in an Ubuntu 20.04 environment and uses Docker for builds.
We cannot upgrade to the latest version of Node.js; we must use version 14.x.
Please prioritize using the company's internal image registry to resolve dependency issues.
```

#### 2. Pipeline Step Level Override

You can also override the global configuration in a specific Pipeline:

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'make build'
            }
        }
    }
    post {
        failure {
            script {
                def explanation = explainError(
                    customContext: '这是一个前端项目，使用 pnpm 作为包管理器。请不要建议使用 npm。'
                )
                echo explanation
            }
        }
    }
}
```

### Actual Effect Comparison

**Without custom context:**

```
Summary: The build failed because the `make` command was not found.

Resolution Steps:
- Install make using: apt-get install make
- Ensure make is in your PATH
```

**With custom context:**

```
Summary: The build failed because the `make` command was not found. 
Given that your project runs in a Docker environment, this issue is likely 
related to your base image.

Resolution Steps:
- Update your Dockerfile to include: RUN apt-get update && apt-get install -y make
- Use a base image that already includes build tools, such as our internal 
  ubuntu-buildenv:20.04 image from the company registry
- Ensure your CI pipeline is using the correct Docker image version
```

As you can see, by adding context information, the AI's response is more aligned with the actual situation, and the provided solutions are more targeted.

---

## II. Folder-Level AI Provider Configuration

### Real-World Needs in Enterprise Scenarios

In large enterprise environments, different teams may have different needs:

-   **Team A** uses the Azure OpenAI service centrally procured by the company.
-   **Team B** uses open-source, self-hosted LLMs due to budget constraints.
-   **Team C** is working on sensitive projects and requires a completely isolated private AI service.
-   **Test environments** might not need AI explanation enabled to save costs.

Previous versions only supported **global configuration**, meaning all projects had to use the same AI provider, which is clearly not flexible enough for enterprise environments.

### Advantages of Folder-Level Configuration

Through [PR #88][2], the plugin introduces the **Folder-Level Configuration** feature, which now allows you to:

-   ✅ Configure AI providers separately at the Jenkins folder level.
-   ✅ Have different teams/projects use different AI services.
-   ✅ Support configuration inheritance, where child folders automatically inherit parent folder configurations.
-   ✅ Completely disable AI explanation functionality at the folder level.
-   ✅ Automatically fall back to global configuration if not explicitly configured.

### How to Configure Folder-Level Settings

#### 1. Create or Configure a Folder

In Jenkins, go to your folder's (Folder) configuration page:

1.  Click on the folder name.
2.  Click on **Configure**.
3.  Find the **Explain Error Configuration** area.

#### 2. Configuration Options

You will see the following configuration options:

**Enable Error Explanation**
-   Check this box to enable AI error explanation in this folder.
-   Uncheck to completely disable AI explanation for all projects under this folder.

**AI Provider**
-   You can choose a different AI provider than the global one.
-   Supports mainstream services like OpenAI, Azure OpenAI, Google Gemini, etc.
-   Fill in the corresponding API Key and configuration information.

#### 3. Configuration Priority

The configuration priority is as follows:

```
Folder configuration > Parent folder configuration > Global configuration
```

This means:
1.  If the current folder has a configuration, use it.
2.  If the current folder does not have a configuration, look for the parent folder's configuration.
3.  If no configuration is found throughout the folder chain, use the global configuration.

### Real-World Usage Scenarios

#### Scenario 1: Different Teams Using Different AI Services

```
Jenkins Root (Uses OpenAI - Global configuration)
├── Team-A-Folder (Inherits global configuration, uses OpenAI)
├── Team-B-Folder (Configured to use Google Gemini)
└── Team-C-Folder (Configured to disable AI explanation)
```

#### Scenario 2: Separation of Production and Testing Environments

```
Jenkins Root (Global configuration OpenAI)
├── Production (Inherits global configuration)
│   ├── App1-Pipeline
│   └── App2-Pipeline
└── Testing (Disables AI explanation to save costs)
    ├── Test-Pipeline-1
    └── Test-Pipeline-2
```

---

## Summary

| Feature                 | Problem Solved                                        | Usage Scenario                                              |
|-------------------------|-------------------------------------------------------|-------------------------------------------------------------|
| **Custom Context**      | AI doesn't understand your specific business scenarios | Provide project environment information, constraints, best practices, etc. |
| **Folder-Level Configuration** | Global configuration cannot meet the needs of different teams | Different teams use different AI services, or isolate by environment |

The addition of these two features makes the [Explain Error Plugin][3] more practical for enterprise-level application scenarios:

-   **Custom context** makes AI explanations more accurate and relevant to your specific situation.
-   **Folder-level configuration** allows different teams to flexibly use different AI services, meeting various business needs.

If you have any suggestions or encounter issues during use, feel free to submit an Issue or PR on [GitHub][4].

Happy CI/CD! 🚀

---

[1]: https://github.com/jenkinsci/explain-error-plugin/pull/83
[2]: https://github.com/jenkinsci/explain-error-plugin/pull/88
[3]: https://plugins.jenkins.io/explain-error/
[4]: https://github.com/jenkinsci/explain-error-plugin