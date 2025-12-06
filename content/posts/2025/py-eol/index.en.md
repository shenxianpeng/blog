```markdown
---
title: py-eol — You Might Be Using 'Expired Python' Without Realizing It
summary: |
  py-eol is a lightweight tool that helps you quickly determine if a Python version is expired or approaching EOL. It's suitable for local use and can also be integrated into CI/CD for more reliable version management in projects.
tags:
  - Python
authors:
  - shenxianpeng
date: 2025-12-04
---

In recent years, Python versions have been updated quite frequently — new versions are constantly released, while older versions are gradually End-Of-Life (EOL).

Many times, we specify Python versions in our projects without realizing they might have already stopped being maintained, potentially introducing security vulnerabilities. To address this "small but easily overlooked" issue, I developed a lightweight tool — [**py-eol**](https://github.com/shenxianpeng/py-eol).

Its goal is simple:
**To help you more easily detect if your Python version is EOL in your daily development.**

---

## What is py-eol?

**py-eol** can check whether a Python version is already (or soon to be) EOL. It supports:

*   Python module calls
*   Command-line calls
*   pre-commit hook integration

It's suitable for local checks, as well as CI/CD and team collaboration.

---

## Quick Installation and Usage

```bash
pip install py-eol
```

### As a Module

```python
from py_eol import is_eol, get_eol_date, supported_versions, eol_versions, latest_supported_version

# For example:
print(is_eol("3.7")) # True
print(get_eol_date("3.8")) # 2024-10-07
print(supported_versions()) # ['3.14', '3.13', '3.12', '3.11', '3.10', '3.9']
print(eol_versions()) # ['3.8', '3.7', '3.6', '3.5', '3.4', '3.3', '3.2', '2.7', '3.1', '3.0', '2.6']
print(latest_supported_version()) # 3.14
```

### As a Command-line Tool

```bash
# Check if a specified Python version is EOL
py-eol versions 3.9

# Check if the current Python version is EOL
py-eol check-self

# Check if Python versions in pyproject.toml or setup.py are EOL
py-eol files pyproject.toml setup.py

# List currently supported Python versions
py-eol list
```

### As a pre-commit hook

```yaml
repos:
  - repo: https://github.com/shenxianpeng/py-eol
    rev: v0.4.0
    hooks:
      - id: py-eol
```

When an EOL version is detected, it will pinpoint the specific file and line number for easy identification.

---

## Why You Should Care?

**1. Avoid Hidden Risks**
After EOL, there are no more security patches. Continuing to use it may introduce potential vulnerabilities.

**2. Smoother Team Collaboration**
With hooks or CI, you get prompts at the commit stage, avoiding issues like "forgetting to update the version in a certain file."

**3. Lightweight, Easy to Use, No Learning Curve**
Install and use immediately, no external service dependencies, can be checked anytime.

---

## The Motivation Behind This Tool

py-eol addresses a small pain point I encountered in my daily development:
**Using a tool to maintain awareness of Python EOL versions, preventing them from being frequently overlooked.**

Since this is a scenario everyone encounters, I wanted to create a simple tool to expose this EOL issue proactively.

py-eol is fully open source (MIT). Feel free to use, improve, or discuss it.

---

If you have colleagues or friends who write Python,

forwarding this article or sharing py-eol might help them. For me, it's also a motivation to continue improving it.

py-eol project address: https://github.com/shenxianpeng/py-eol

---

Please credit the author and source when reprinting articles from this site. Do not use for any commercial purposes. Welcome to follow the official account 「DevOps攻城狮」
```