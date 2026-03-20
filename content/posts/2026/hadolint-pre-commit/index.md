---
title: 别再手动下载 Binary 了！我把 Hadolint 塞进了 PyPI，彻底解决 pre-commit 痛点
summary: |
  Hadolint 的 pre-commit 集成长期缺少自动安装方案，困扰社区三年。本文介绍如何通过将 Hadolint 二进制封装成 Python Wheel 包并发布到 PyPI，让 pre-commit 像安装任何 Python 工具一样一键集成 Hadolint，彻底消除手动下载与环境配置的负担。
tags:
  - Hadolint
  - Pre-Commit
authors:
  - shenxianpeng
date: 2026-03-20
---

如果你是一个对代码质量有追求的开发者，你的工具箱里一定少不了 **Hadolint**。作为 Dockerfile 语法检查的标杆，它能帮你写出更高质量的 Dockerfile。

但在集成到 `pre-commit` 工作流时，Hadolint 一直有个让人如鲠在喉的问题：**它没有一个官方的、自动安装的 Binary 版本供 `pre-commit` 使用。**

### 痛点回顾：消失的"自动化"最后一公里

如果你想在 `pre-commit` 里用 Hadolint，通常只有两条路：

1. **System 模式**：你必须先在自己的 Mac/Linux/Windows 上手动下载 Hadolint 的二进制文件并配置好环境变量。如果团队里有 10 个人，你就得教 10 个人怎么装。
2. **Docker 模式**：通过 `hadolint-docker` 运行。但这要求运行环境里必须装有 Docker，而且在 CI 环境下（如 GitHub Actions）套娃运行 Docker 容器，速度慢且配置复杂。

这个问题在 Hadolint GitHub 仓库上已经挂了三年之久 [Issue #886](https://github.com/hadolint/hadolint/issues/886)。

---

### 破局：让 Hadolint "伪装"成 Python 包

我的思路很直接：**既然 `pre-commit` 对 Python 包的支持最完美，那我就给 Hadolint 套个 Python 的壳。**

灵感来自之前打包 [Gnuplot](https://pypi.org/project/gnuplot-wheel/) 的经历——将二进制文件直接打包成 Python 包上传到 PyPI，就能让 `pre-commit` 像安装任何其他 Python 工具一样安装它。

就在昨天，我正式发布了 **`hadolint-py`** 和 **`hadolint-pre-commit`**，解决了这个三年的老问题。具体做法分三步：

1. **二进制封装**：将 Hadolint 最新的原生二进制文件封装进 Python Wheel 包并上传到 PyPI。
2. **零依赖安装**：执行 `pip install hadolint-py` 时，Hadolint 可执行文件会自动落到 Python 环境的 `bin/` 目录，直接可用。
3. **无感集成**：对于 `pre-commit` 来说，它现在就像调用 `flake8` 或 `black` 一样简单，不再需要预装任何额外软件。

---

### 如何开始使用？

只需在 `.pre-commit-config.yaml` 中加入以下配置：
```yaml
repos:
  - repo: https://github.com/shenxianpeng/hadolint-pre-commit
    rev: v2.14.0.1
    hooks:
      - id: hadolint
```

**就这么简单。** 无论本地开发还是 CI 流水线，只要有 Python 环境，Hadolint 就能即插即用。

---

### 这种方案可靠吗？

"二进制转 Python 包"的思路在 `gnuplot-wheel` 项目上已经得到验证，能极大地降低工具的准入门槛。`hadolint-py` 延续了同样的做法，只是把主角换成了 Hadolint。

* **项目地址**：[hadolint-pre-commit](https://github.com/shenxianpeng/hadolint-pre-commit)
* **PyPI 镜像**：[hadolint-py](https://pypi.org/project/hadolint-py/)

如果你也曾被 Hadolint 的安装问题困扰过，或者正在寻找更简洁的 Dockerfile Lint 方案，欢迎试用并给个 Star。有任何问题或建议，也欢迎在 GitHub 上提 Issue 交流。
