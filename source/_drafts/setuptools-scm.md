---
title: 通过 setuptools_scm 实现 Python Package 自动化发布
tags:
  - Python
  - Release
categories:
  - DevOps
author: shenxianpeng
date: 2022-08-14 11:38:13
---

## 问题

之前我在 GitHub 上通过 GitHub Action 发布一个 Python 包的时候需要先将版本号更新到一个新的版本、提交（比如修改 setup.py），然后通过 CI pipeline 来自动打包和上传。

但是如果我没有提前将你的包更新到一个最新的版本号，那么执行发布 pipeline 会报错，因为 PyPi 上是不允许同一个版本号发布两次，如果需要发布每次需要更新的新的版本号。

当然我可以通过编写脚本来实现自动每次发布时更新版本号，但有没有更好的方式呢？

有的，今天就来介绍一下 `setuptools_scm`。

## setuptools_scm 简介

[setuptools_scm](https://github.com/pypa/setuptools_scm) 是从 git 元数据中提取 Python 包版本，而不是将它们声明为版本参数或在 SCM 托管文件中。

此外，`setuptools_scm` 为 `setuptools` 提供了由 SCM 管理的文件列表，即它自动将所有 SCM 管理的文件添加到 sdist（如果需要排除需要通过 MANIFEST.in ）。

`setuptools_scm` 支持 git 和 mercurial。

## setuptools_scm 使用

本文主要介绍如何通过 setuptools_scm 自动化发布，这里不过多的翻译官方文档，只介绍一下几个常用的例子，更多用法可以去查看官方 [README](https://github.com/pypa/setuptools_scm/blob/main/README.rst)

如果你需要确认正在生成哪个版本字符串或调试配置，你可以直接在工作环境中安装 `setuptools-scm` 并运行：

```bash
$ python -m setuptools_scm

# 要探索其他选项，请尝试：
$ python -m setuptools_scm --help
```

### 使用 pyproject.toml

如果你正在使用的是 pyproject.toml，这是首选方式。需要在 `pyproject.toml` 的 `tool.setuptools_scm` 部分中编写你的设置。

此功能需要 2019 年 11 月发布的 Setuptools 42 或更高版本。如果你的项目需要支持在旧版本的 Setuptools 上从 sdist 构建，你还需要为这些旧环境实现 `setup.py` 使用。

首先，通过将 `setuptools_scm` 指定为构建要求之一，确保在项目构建步骤期间存在 `setuptools_scm`。

```yml
# pyproject.toml
[build-system]
requires = ["setuptools>=45", "setuptools-scm"]

[tool.setuptools_scm]
```

### 使用 setup.py

如果你正在使用的是 setup.py（已弃用），注意 `setup_requires` 已被弃用，取而代之的是 `pyproject.toml`

以下设置被视为遗留行为并被 `pyproject.toml` 用法取代，但为了最大程度的兼容性 `setuptools_scm` 也支持这种旧形式的配置。

要使用 `setuptools_scm` 只需像这样修改项目的 `setup.py` 文件：

* 将 `setuptools_scm` 添加到 `setup_requires` 参数
* 添加 `use_scm_version` 参数并将其设置为 `True`。

```python
from setuptools import setup
setup(
    ...,
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    ...,
)
```

## 如何实现自动发布

以一个实际的 GitHub 项目为例 [clang-tools-pip](https://github.com/cpp-linter/clang-tools-pip)

先来看看 pyproject.toml 的配置

```yml
[build-system]
requires = ["setuptools>=45", "setuptools-scm"]

# 省略
# ....

[tool.setuptools_scm]
# It would be nice to include the commit hash in the version, but that
# can't be done in a PEP 440-compatible way.
version_scheme= "no-guess-dev"
# Test PyPI does not support local versions.
local_scheme = "no-local-version"
fallback_version = "0.0.0"
```

再来看看 GitHub Action 的发布 Pipeline，全部 YAML 在[这里](https://github.com/cpp-linter/clang-tools-pip/blob/main/.github/workflows/python-publish.yml)。

我们主要来看下这个发布 pipeline 中的一下这两个部分：

```yml
- name: Publish package (to TestPyPI)
      if: github.event_name == 'workflow_dispatch' && github.repository == 'cpp-linter/clang-tools-pip'
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.TEST_PYPI_TOKEN }}
      run: twine upload --repository testpypi dist/*
```

当用户运行这个发布 pipeline的时候会自动发布到 testpypi（测试环境）

```yml
- name: Publish package (to PyPI)
      if: github.event_name != 'workflow_dispatch' && github.repository == 'cpp-linter/clang-tools-pip'
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

如果是通过 [GitHub 的发布页面进行发布](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)，则会发布的正式的 pypi 环境上。

这过程中你只需填写你本次发布的 tag 即可，比如 `0.2.0`, `setuptools_scm` 会拿到这 tag 并将它作为最新的版本号发布到 pypi 上面。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
