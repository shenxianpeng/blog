---
title: A Three-Year Community Pain Point—I Put Hadolint on PyPI, Ending Manual Installation
summary: |
  Hadolint's pre-commit integration has long lacked an automatic installation solution, a problem that has plagued the community for three years. This article explains how, by packaging the Hadolint binary into a Python Wheel and publishing it to PyPI, pre-commit can integrate Hadolint with a single command, just like any Python tool, completely eliminating the burden of manual downloads and environment configuration.
tags:
  - Hadolint
  - Pre-Commit
authors:
  - shenxianpeng
date: 2026-03-20
---

If you are a developer who pursues code quality, **Hadolint** must be indispensable in your toolkit. As the benchmark for Dockerfile syntax checking, it helps you write higher-quality Dockerfiles.

However, when integrating into the `pre-commit` workflow, Hadolint has always had a nagging problem: **there is no official, automatically installable binary version for `pre-commit` to use.**

### Pain Point Revisited: The Missing "Automation" Last Mile

If you want to use Hadolint in `pre-commit`, there are usually only two ways:

1.  **System Mode**: You must first manually download the Hadolint binary and configure environment variables on your Mac/Linux/Windows. If there are 10 people on the team, you'd have to teach all 10 how to install it.
2.  **Docker Mode**: Run via `hadolint-docker`. But this requires Docker to be installed in the runtime environment, and running Docker containers in a nested fashion in a CI environment (e.g., GitHub Actions) is slow and complex to configure.

This problem has been hanging in the Hadolint GitHub repository for three years [Issue #886](https://github.com/hadolint/hadolint/issues/886).

---

### The Breakthrough: Making Hadolint "Disguise" Itself as a Python Package

My approach was straightforward: **since `pre-commit` has the most perfect support for Python packages, I'll just give Hadolint a Python shell.**

The inspiration came from my previous experience packaging [Gnuplot](https://pypi.org/project/gnuplot-wheel/)—packaging binary files directly into Python packages and uploading them to PyPI allows `pre-commit` to install them just like any other Python tool.

Just yesterday, I officially released **`hadolint-py`** and **`hadolint-pre-commit`**, solving this three-year-old problem. The specific approach consists of three steps:

1.  **Binary Packaging**: Encapsulate Hadolint's latest native binary into a Python Wheel package and upload it to PyPI.
2.  **Zero-Dependency Installation**: When executing `pip install hadolint-py`, the Hadolint executable will automatically land in the Python environment's `bin/` directory, ready for direct use.
3.  **Seamless Integration**: For `pre-commit`, it's now as simple as calling `flake8` or `black`, no longer requiring any additional software to be pre-installed.

---

### How to Get Started?

Just add the following configuration to `.pre-commit-config.yaml`:
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

The "binary to Python package" approach has already been validated by the `gnuplot-wheel` project, significantly lowering the barrier to entry for tools. `hadolint-py` continues with the same method, simply swapping out the main character for Hadolint.

*   **Project Address**: [hadolint-pre-commit](https://github.com/shenxianpeng/hadolint-pre-commit)
*   **PyPI Package**: [hadolint-py](https://pypi.org/project/hadolint-py/)

If you have also been troubled by Hadolint's installation issues, or are looking for a cleaner Dockerfile Lint solution, feel free to try it out and give it a Star. For any questions or suggestions, please feel free to raise an Issue on GitHub for discussion.