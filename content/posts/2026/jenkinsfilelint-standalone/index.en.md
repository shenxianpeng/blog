---
title: Jenkinsfile Lint 1.5.0 Released— Standalone Mode Without a Jenkins Server
summary: |
  Previously, jenkinsfilelint required connecting to an available Jenkins server for syntax validation. Now, v1.5.0 introduces a new standalone mode. With just Docker, you can launch a minimal Jenkins environment locally to validate Jenkinsfile syntax. This article details the implementation idea and usage of this mode.
tags:
  - Jenkins
  - Open Source
  - pre-commit
  - Pipeline
  - Docker
authors:
  - shenxianpeng
date: 2026-07-12
---

Hello everyone, I'm Shen Gong.

I previously wrote an article about [jenkinsfilelint](https://github.com/jenkinsci/jenkinsfilelint)—one detailing its journey from my personal project into the official Jenkins organization. Today, let's talk about the newly released **v1.5.0** version.

The biggest change in this version is the addition of a **standalone mode**.

This feature was requested by a community user. Someone on GitHub asked: "Can we run syntax validation without a Jenkins server?"

I gave it some thought, and this request is indeed reasonable—the goal of jenkinsfilelint is to make Jenkinsfile syntax checking convenient enough. If it still relies on a Jenkins server, the barrier to entry is a bit high.

In short: **You no longer need a Jenkins server to validate Jenkinsfile syntax.**

Before this, jenkinsfilelint worked by calling Jenkins' built-in Pipeline Linter API:

```
$JENKINS_URL/pipeline-model-converter/validate
```

The advantage is accurate validation results and faster feedback, as it uses the real logic of Jenkins in your production environment. The disadvantages are also obvious—**you need to have a Jenkins server first and configure credentials.**

If you don't have a Jenkins server, or you're just making a temporary change to a Jenkinsfile and still have to configure a Jenkins server, it becomes quite troublesome.

Hence, the solution for v1.5.0: providing users with a minimal Jenkins runtime environment, packaging the dependencies into an image. Users only need to:

- Have Docker (or Podman works too)
- Add the `--local` parameter to `.pre-commit-config.yaml`

Syntax validation will then automatically be completed locally.

---

## How to Use Local Mode

If your `.pre-commit-config.yaml` was previously like this:

```yaml
repos:
  - repo: https://github.com/jenkinsci/jenkinsfilelint
    rev: v1.5.0
    hooks:
      - id: jenkinsfilelint
```

Then you needed to configure environment variables `JENKINS_URL`, `JENKINS_USER`, `JENKINS_TOKEN`, pointing to your Jenkins server.

Now you just need to add `args: ["--local"]`:

```yaml
repos:
  - repo: https://github.com/jenkinsci/jenkinsfilelint
    rev: v1.5.0
    hooks:
      - id: jenkinsfilelint
        args: ["--local"]
```

**The only dependency is Docker; no Jenkins address or credentials need to be configured.**

The installation and commit process is just as smooth:

```bash
pip install pre-commit
pre-commit install
git commit -m "Update Jenkinsfile"
```

The first run will have a cold start delay, as it needs to pull and start the Jenkins container, which takes about **20–40 seconds**. After that, the container will remain running, and subsequent validations will complete in seconds.

You might be thinking: How is the container's lifecycle managed?

I've provided two ways:

1.  **Automatic Reuse**: Once the container starts, it will continue to run. The next commit will directly reuse it, with no additional waiting time.
2.  **Manual Stop**: If you're done and want to clean up resources, just run `jenkinsfilelint server stop`.

---

## Implementation Idea: Minimal Jenkins Runtime

The core of this standalone mode is a custom Docker image.

After being packaged into an image, it's published on GitHub Container Registry:

```
ghcr.io/jenkinsci/jenkinsfilelint-server:latest
```

The sole purpose of this image is to: **receive POST requests, call the Pipeline Model Converter to perform syntax validation, and return the result.** It has no unnecessary plugins.

If you have special requirements for maintaining your own image, you can also specify a custom image via the `JENKINSFILELINT_SERVER_IMAGE` environment variable.

---

## Limitations of Local Mode

While convenient, this mode does have some limitations that need to be clarified.

The power of Jenkins Pipeline lies in its **plugin ecosystem**—different plugins provide various types of agents, steps, and options. If your Jenkinsfile uses features from custom plugins (e.g., specific shared libraries, non-standard agent labels, etc.), the minimal Jenkins environment in local mode cannot cover these plugins, and thus cannot validate those parts.

Therefore, my recommendation is:

| Scenario                                          | Recommended Mode                |
| :------------------------------------------------ | :------------------------------ |
| Quick syntax check, local development             | `--local`                       |
| Authoritative validation (including business plugin logic) | Remote mode (connect to official Jenkins) |
| CI pipeline                                       | Remote mode                     |

**`--local` is for quick syntax gating, while the remote mode is for authoritative validation.** These two are not mutually exclusive and can be used in combination.

---

## Summary

This community-feedback-driven development experience has been quite good—someone proposes a requirement, I assess its feasibility, and then implement it. It's not about me just deciding what's good and blindly building it.

If your team uses Jenkins, you might want to try Jenkinsfilelint. It can help you catch Jenkinsfile syntax errors before committing. If you have any questions, feel free to open an issue on GitHub.

Project Address: [github.com/jenkinsci/jenkinsfilelint](https://github.com/jenkinsci/jenkinsfilelint)

---

Please attribute the author and source when reprinting articles from this site. Do not use for any commercial purposes. Welcome to follow the WeChat official account "Shen Xianpeng".