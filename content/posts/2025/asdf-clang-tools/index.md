---
title: asdf-clang-tools：使用 asdf 安装 Clang 工具的新选择
summary: |
  asdf-clang-tools 是一个 asdf 插件，用于安装和管理 Clang Tools 相关工具（如 clang-format、clang-tidy、clang-query 和 clang-apply-replacements 等）。
tags:
  - clang-tools
  - asdf
author: shenxianpeng
date: 2025-05-29
---

最近，我在 cpp-linter 组织下发布了一个名为 **[asdf-clang-tools](https://github.com/cpp-linter/asdf-clang-tools)** 的全新仓库。这个项目是从 amrox/asdf-clang-tools fork 而来。由于原作者多年没有维护，我对其进行了修复、升级和功能扩展，使其焕然一新。简单来说，asdf-clang-tools 是一个 **asdf 插件**，用于安装和管理 Clang Tools 相关工具（如 clang-format、clang-tidy、clang-query 和 clang-apply-replacements 等）。

## 新的安装方式：除了 pip 还有 asdf

在此之前，我曾推出过 **clang-tools-pip** 工具包，用户可以通过 `pip install clang-tools` 的方式安装包括 clang-format、clang-tidy、clang-query、clang-apply-replacements 在内的一整套 Clang 可执行工具。

而 asdf-clang-tools 则提供了另一种途径——利用 [asdf](https://asdf-vm.com) 版本管理器来安装这些工具。简而言之，这为喜欢用 asdf 管理工具版本的开发者多了一个选择。

这两种方式并不是互斥的：你可以通过 pip 或 asdf 轻松安装和管理 Clang 工具。至于选择哪种方式取决于你的工作流和个人喜好。

## 什么是 asdf 版本管理器

很多开发者可能还不太熟悉 asdf。**asdf** 是一个多语言、多工具的版本管理器。

它可以用一个命令行工具管理多种运行时环境的版本，支持插件机制。

举例来说，你可以通过 asdf 来管理 Python、Node.js、Ruby 等语言的版本，也可以管理 Clang 工具（像我介绍的 asdf-clang-tools）。

所有工具的版本信息都记录在一个共享的 `.tool-versions` 文件中，这样团队可以轻松在不同机器间同步配置。

总之，asdf 的好处就是“一个工具管理所有的依赖”，让项目所需的各类工具版本统一起来，免去在每个工具里使用不同版本管理器的麻烦。

## 安装与使用示例

使用 asdf-clang-tools 安装 Clang 工具非常简单。假设你已经安装好了 asdf，只需按照官方仓库的说明进行操作：

* 首先 **添加插件**：以 `clang-format` 为例，在终端运行：

  ```bash
  asdf plugin add clang-format https://github.com/cpp-linter/asdf-clang-tools.git
  ```

  类似地，`clang-query`、`clang-tidy`、`clang-apply-replacements` 等工具也使用相同的仓库地址，只需把插件名改为对应的名称即可。

* **查看可用版本**：添加插件后，可以运行 `asdf list all clang-format` 来列出所有可安装的 clang-format 版本。

* **安装工具**：选择一个版本（例如最新的 `latest`），执行：

  ```bash
  asdf install clang-format latest
  ```

  这会下载并安装指定版本的 clang-format 二进制文件。

* **设置全局版本**：安装完成后，可以执行：

  ```bash
  asdf set clang-format latest
  ```

  这会把版本写入 `~/.tool-versions` 文件，实现全局可用。此后，你就可以直接在命令行中使用 `clang-format` 等命令了。

以上操作完成后，clang-format、clang-tidy 等工具就已集成到 asdf 管理下。更多细节可参考 asdf 官方文档。

## 欢迎试用并反馈建议

总的来说，asdf-clang-tools 为需要 Clang Tools 的开发者提供了一种新的安装方式。

它与 cpp-linter 组织的其它工具（如 clang-tools-pip）互为补充。

我诚挚欢迎大家尝试 cpp-linter 提供的整个 C/C++ lint 解决方案，选择最适合自己工作流的工具。

同时，如果在使用过程中有任何问题或改进建议，欢迎通过 GitHub Issues、讨论区等渠道提出，一起完善 Cpp Linter 工具链，让 C/C++ 格式化和静态分析工作更加便捷高效！

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
