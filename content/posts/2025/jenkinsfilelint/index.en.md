---
title: Tired of Jenkinsfile Errors Only After Committing—Try This Pre-check Tool!
summary: A magical local Jenkinsfile checker, uses API validation, perfectly supports pre-commit.
tags:
  - Jenkins
  - DevOps
translate: true
authors:
  - shenxianpeng
date: 2025-11-27
---

Hello everyone!

Today, I'd like to share an open-source tool I recently developed: **jenkinsfilelint**.

#### **Why I wrote this tool?**

I believe anyone who has written Jenkins Pipelines has experienced this painful process:

1.  You painstakingly write your `Jenkinsfile`.
2.  Commit the code and push it to the repository.
3.  Watch Blue Ocean or the Console, waiting for the build to start.
4.  **Boom!** A few seconds later, the build fails because of a missing brace `}` or a misspelled keyword.
5.  Modify code -> Commit again -> Wait -> Pray...

To solve this problem, I searched for Jenkinsfile linting tools. While there are existing solutions, I found that they were either overly complicated to configure or **couldn't be well integrated into a `pre-commit` workflow**.

Since there wasn't a convenient tool available, I decided to build one myself! And that's how **jenkinsfilelint** came to be.

#### **What is it?**

`jenkinsfilelint` is a command-line tool developed in Python, designed to help you validate the syntax of your Jenkinsfile before committing code.

It performs validation by calling Jenkins' native API, thus ensuring that the inspection results are fully consistent with the parsing logic during actual runtime.

**Project Address:**

> [https://github.com/shenxianpeng/jenkinsfilelint](https://github.com/shenxianpeng/jenkinsfilelint)

#### **Core Features**

  * ✅ **Jenkins API-based**: Utilizes Jenkins' official `/pipeline-model-converter/validate` endpoint for validation. The results are not only accurate but also provide specific error line numbers.
  * 🚀 **Perfect pre-commit support**: This was my original motivation for developing it. You can easily integrate it into your project's git hooks to ensure automatic checks before every commit.
  * 🛠 **Flexible Configuration**: Supports configuring Jenkins URL and credentials via environment variables or command-line parameters.
  * 🔍 **Intelligent Filtering**: When using Jenkins Shared Libraries, your repository might contain pure Groovy helper class files (not Pipeline scripts). The tool supports skipping these files using the `--skip` parameter to avoid false positives.

#### **How to Use?**

##### 1\. Installation

You can install it directly using pip:

```bash
pip install jenkinsfilelint
```

##### 2\. Integrate into pre-commit (highly recommended)

Create or modify the `.pre-commit-config.yaml` file in your project's root directory and add the following configuration:

```yaml
repos:
  - repo: https://github.com/shenxianpeng/jenkinsfilelint
    rev: v1.2.0  # It is recommended to use the latest version tag
    hooks:
      - id: jenkinsfilelint
```

Then install the hooks:

```bash
pre-commit install
```

##### 3\. Configure Credentials

Since validation requires calling Jenkins' API, you need to provide the Jenkins URL and access credentials.

⚠️ **Security Tip**: It is strongly recommended not to hardcode credentials in configuration files! It is recommended to use environment variables:

```bash
# Linux/macOS
export JENKINS_URL=https://your-jenkins-instance.com
export JENKINS_USER=your-username
export JENKINS_TOKEN=your-api-token
```

Once configured, when you try to execute `git commit`, `jenkinsfilelint` will automatically check the Jenkinsfile(s) in your changes!

#### **Command-line Manual Check**

Of course, you can also run it manually locally to check specific files:

```bash
# Check a single file
jenkinsfilelint Jenkinsfile

# Check multiple files
jenkinsfilelint Jenkinsfile Jenkinsfile.prod

# Skip files matching a specific pattern (e.g., Groovy files in the src directory)
jenkinsfilelint --skip '*/src/*.groovy' Jenkinsfile src/Utils.groovy
```

#### **In Conclusion**

This project is currently published on PyPI, and everyone is welcome to download and try it out.

If you're also tired of 'post-commit errors' with your Jenkinsfiles, why not give `jenkinsfilelint` a try? If you find it useful, please give it a **⭐️ Star** on GitHub to show your support!

If you have any questions or suggestions, feel free to open an Issue or PR.

**GitHub Portal:**
[https://github.com/shenxianpeng/jenkinsfilelint](https://github.com/shenxianpeng/jenkinsfilelint)
