---
title: py-eol：你可能一直在用“过期 Python”，只是没发现
summary: |
  py-eol 是一个轻量的小工具，帮助你快速判断某个 Python 版本是否已过期或即将 EOL，适合本地使用，也能集成到 CI/CD 中，让项目在版本管理上更可靠。
tags:
  - Python
authors:
  - shenxianpeng
date: 2025-12-04
---

近年来，Python 版本更新挺频繁的 —— 新版本不断发布，而旧版本也会陆续停止维护（EOL: End-Of-Life）。

很多时候，我们在项目里写 Python 版本，却没意识到它可能早已停止维护，甚至埋下了安全隐患。为了解决这个“小却容易忽略”的问题，我做了一个轻量工具 —— [**py-eol**](https://github.com/shenxianpeng/py-eol)。

它的目标很简单：
**帮你在日常开发里更轻松地察觉 Python 版本是否已 EOL。**

---

## py-eol 是什么？

**py-eol** 能够检查 Python 版本是否已经（或即将）EOL，支持：

* Python 模块调用
* 命令行调用
* pre-commit hook 集成

适合本地检查，也适合 CI/CD 与团队协作。

---

## 快速安装与使用

```bash
pip install py-eol
```

### 作为模块

```python
from py_eol import is_eol, get_eol_date, supported_versions, eol_versions, latest_supported_version

# 例如：
print(is_eol("3.7")) # True
print(get_eol_date("3.8")) # 2024-10-07
print(supported_versions()) # ['3.14', '3.13', '3.12', '3.11', '3.10', '3.9']
print(eol_versions()) # ['3.8', '3.7', '3.6', '3.5', '3.4', '3.3', '3.2', '2.7', '3.1', '3.0', '2.6']
print(latest_supported_version()) # 3.14
```

### 作为命令行

```bash
# 检查指定 Python 版本是否 EOL
py-eol versions 3.9

# 检查当前 Python 版本是否 EOL
py-eol check-self

# 检查 pyproject.toml 或 setup.py 中的 Python 版本是否 EOL
py-eol files pyproject.toml setup.py

# 列出当前支持的 Python 版本
py-eol list
```

### 作为 pre-commit hook

```yaml
repos:
  - repo: https://github.com/shenxianpeng/py-eol
    rev: v0.4.0
    hooks:
      - id: py-eol
```

当发现 EOL 版本时，会标出具体文件和行号，便于定位。

---

## 为什么值得关注？

**1. 避免隐性风险**
EOL 后不再有安全补丁，继续使用可能会引来潜在漏洞。

**2. 和团队协作更顺畅**
通过 hook 或 CI 在提交阶段就能提示，避免“某个文件里的版本忘记更新”的问题。

**3. 轻量好用，没有学习成本**
安装即用，不依赖外部服务，随时可检查。

---

## 做这个工具的初衷

py-eol 是我在日常开发中的一个小痛点：
**借助工具来维护 Python 版本是否 EOL，避免经常被忽略。**

既然是大家都会遇到的场景，我想做一个简单的工具，把这个 EOL 问题提前暴露出来。

py-eol 完全开源（MIT），欢迎随意使用、改进或交流。

---

如果你身边也有同事、朋友在写 Python，

转发这一篇文章或分享 py-eol，也许能帮他们。对我来说也是继续完善它的一份动力。

py-eol 项目地址：https://github.com/shenxianpeng/py-eol

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
