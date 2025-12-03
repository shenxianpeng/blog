---
title: "Clang Tools Distributions"
weight: 8
summary: "为 clang-format 和 clang-tidy 提供多种分发方式，支持 Docker、静态二进制和 Python Wheel 三种形式。"
showDate: false
showReadingTime: false
showWordCount: false
build:
  render: "false"
  list: "local"
---

## Clang Tools 分发项目

为了让 C/C++ 开发者更方便地使用 `clang-format` 和 `clang-tidy` 代码检查工具，我创建了以下三种分发方式：

> 🎯 **目标**：简化 Clang Tools 的集成和使用，支持不同的使用场景和环境。

---

### 🐳 Docker 镜像

**项目地址**：[clang-tools-docker](https://github.com/cpp-linter/clang-tools-docker)

预构建的 Docker 镜像，包含多个版本的 clang-format 和 clang-tidy，适合 CI/CD 环境和容器化部署。

**适用场景**：
- GitHub Actions / GitLab CI 等 CI/CD 流水线
- 需要隔离环境的代码检查
- 多版本 Clang 工具的快速切换

---

### 📦 静态二进制文件

**项目地址**：[clang-tools-static-binaries](https://github.com/cpp-linter/clang-tools-static-binaries)

跨平台预编译的静态二进制文件，无需依赖系统库，开箱即用。

**适用场景**：
- 无法使用包管理器的受限环境
- 需要特定版本的 Clang 工具
- 快速部署和独立运行

---

### 🎡 Python Wheel 包

**项目地址**：[clang-tools-wheel](https://github.com/cpp-linter/clang-tools-wheel)  
**PyPI 包名**：[clang-tools](https://pypi.org/project/clang-tools/)

通过 `pip install clang-tools` 一键安装，将 Clang 工具集成到 Python 项目中。

**适用场景**：
- Python 项目的开发环境
- 需要通过 pip 管理工具依赖
- 与 Python 工具链集成

---

> 💡 **提示**：这些项目都托管在 [cpp-linter](https://github.com/cpp-linter/) 组织下，我作为核心维护者参与开发和维护。
