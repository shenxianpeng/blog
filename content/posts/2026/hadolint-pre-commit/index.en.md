---
title: Stop Manually Downloading Binaries! I've Put Hadolint on PyPI to Completely Solve the pre-commit Pain Point
summary: |
  Hadolint's pre-commit integration has long lacked an automatic installation solution, bothering the community for three years. This article introduces how to package the Hadolint binary into a Python Wheel and publish it to PyPI, allowing pre-commit to integrate Hadolint with one click, just like installing any Python tool, completely eliminating the burden of manual downloads and environment configuration.
tags:
  - Hadolint
  - Pre-Commit
authors:
  - shenxianpeng
date: 2026-03-20
---

If you are a developer who pursues code quality, **Hadolint** must be an essential tool in your toolbox. As the benchmark for Dockerfile syntax checking, it helps you write higher-quality Dockerfiles.

However, when integrated into the `pre-commit` workflow, Hadolint has always had a thorny issue: **it lacks an official, automatically installable binary version for `pre-commit` to use.**

### Pain Point Revisited: The Missing "Automation" Last Mile

If you want to use Hadolint with `pre-commit`, there are usually only two ways:

1.  **System Mode**: You must first manually download the Hadolint binary on your Mac/Linux/Windows and configure environment variables. If there are 10 people on the team, you'd have to teach 10 people how to install it.
2.  **Docker Mode**: Run via `hadolint-docker`. But this requires Docker to be installed in the runtime environment, and running nested Docker containers in a CI environment (like GitHub Actions) is slow and complex to configure.

This issue has been pending on the Hadolint GitHub repository for three years [Issue #886](https://github.com/hadolint/hadolint/issues/886).

---

### The Breakthrough: Making Hadolint "Disguise" as a Python Package

My idea was straightforward: **since `pre-commit` has the most perfect support for Python packages, I'll give Hadolint a Python wrapper.**

The inspiration came from my previous experience packaging [Gnuplot](https://pypi.org/project/gnuplot-wheel/)—by packaging a binary directly into a Python package and uploading it to PyPI, `pre-commit` can install it just like any other Python tool.

Just yesterday, I officially released **`hadolint-py`** and **`hadolint-pre-commit`**, solving this three-year-old problem. The specific approach consists of three steps:

1.  **Binary Encapsulation**: Package Hadolint's latest native binary into a Python Wheel package and upload it to PyPI.
2.  **Zero-Dependency Installation**: When executing `pip install hadolint-py`, the Hadolint executable will automatically land in the `bin/` directory of the Python environment, ready for direct use.
3.  **Seamless Integration**: For `pre-commit`, it's now as simple as calling `flake8` or `black`, no longer requiring any additional software to be pre-installed.

---

### How to Get Started?

Simply add the following configuration to your `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/shenxianpeng/hadolint-pre-commit
    rev: v2.14.0.1
    hooks:
      - id: hadolint
```

**It's that simple.** Whether for local development or CI pipelines, as long as there's a Python environment, Hadolint is plug-and-play.

---

### Is This Solution Reliable?

The idea of "binary to Python package" has already been validated with the `gnuplot-wheel` project, greatly lowering the entry barrier for tools. `hadolint-py` continues with the same approach, just replacing the main character with Hadolint.

*   **Project Address**: [hadolint-pre-commit](https://github.com/shenxianpeng/hadolint-pre-commit)
*   **PyPI Mirror**: [hadolint-py](https://pypi.org/project/hadolint-py/)

If you've also been troubled by Hadolint's installation issues, or are looking for a simpler Dockerfile Lint solution, feel free to try it out and give it a Star. For any questions or suggestions, you're welcome to open an Issue on GitHub for discussion.