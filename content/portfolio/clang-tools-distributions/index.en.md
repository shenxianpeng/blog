---
title: "Clang Tools Distributions"
weight: 8
summary: "Multiple distribution methods for clang-format and clang-tidy, supporting Docker, static binaries, and Python Wheel packages."
showDate: false
showReadingTime: false
showWordCount: false
build:
  render: "false"
  list: "local"
---

## Clang Tools Distribution Projects

To make it easier for C/C++ developers to use `clang-format` and `clang-tidy` code checking tools, I created the following three distribution methods:

> 🎯 **Goal**: Simplify the integration and usage of Clang Tools, supporting different use cases and environments.

---

### 🐳 Docker Images

**Project**: [clang-tools-docker](https://github.com/cpp-linter/clang-tools-docker)

Pre-built Docker images containing multiple versions of clang-format and clang-tidy, ideal for CI/CD environments and containerized deployments.

**Use Cases**:
- GitHub Actions / GitLab CI and other CI/CD pipelines
- Code checking in isolated environments
- Quick switching between multiple Clang tool versions

---

### 📦 Static Binaries

**Project**: [clang-tools-static-binaries](https://github.com/cpp-linter/clang-tools-static-binaries)

Cross-platform pre-compiled static binaries with no system library dependencies, ready to use out of the box.

**Use Cases**:
- Restricted environments without package managers
- Specific versions of Clang tools needed
- Quick deployment and standalone execution

---

### 🎡 Python Wheel Packages

**Project**: [clang-tools-wheel](https://github.com/cpp-linter/clang-tools-wheel)  
**PyPI Package**: [clang-tools](https://pypi.org/project/clang-tools/)

Install with a single command `pip install clang-tools`, integrating Clang tools into Python projects.

**Use Cases**:
- Python project development environments
- Managing tool dependencies via pip
- Integration with Python toolchains

---

> 💡 **Note**: These projects are hosted under the [cpp-linter](https://github.com/cpp-linter/) organization, where I participate as a core maintainer in development and maintenance.