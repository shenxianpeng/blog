---
title: "cpp-linter-hooks：C/C++ 项目最完整的 pre-commit 方案"
summary: |
  pre-commit 生态里 C/C++ 的工具一直比较薄弱。cpp-linter-hooks 是目前唯一同时支持 clang-format 和 clang-tidy 的 pre-commit hook，还内置了编译数据库自动检测、版本锁定、自动修复等实用功能。本文介绍它的用法和设计思路。
tags:
  - Pre-Commit
  - C/C++
  - Open Source
authors:
  - shenxianpeng
date: 2026-05-20
---

大家好，我是沈工。

如果你写过 Python 项目，大概率用过 `pre-commit` —— 在 `git commit` 之前自动跑一遍 `black`、`ruff`、`mypy`，格式不对就拦下来，问题多了甚至不让你提交。这套流程在 Python 生态里已经非常成熟。

但如果你写的是 C/C++，情况就不太一样了。

`pre-commit` 官方的 `mirrors-clang-format` 只支持格式化，lint 检查（clang-tidy）需要自己另外折腾。至于编译数据库自动检测、版本锁定、自动修复这些功能，更是想都不要想。

[cpp-linter-hooks](https://github.com/cpp-linter/cpp-linter-hooks) 就是来解决这个问题的。它在 `pre-commit` 里同时提供 `clang-format` 和 `clang-tidy` 两个 hook，并且把 C/C++ 项目实际需要的周边能力一并补齐了。

---

## 为什么不用 mirrors-clang-format？

先看一眼两者对比：

| 功能 | cpp-linter-hooks | mirrors-clang-format |
|------|:---:|:---:|
| clang-format 支持 | ✅ | ✅ |
| clang-tidy 支持 | ✅ | ❌ |
| 通过 `--style` 直接指定格式风格 | ✅ | ❌ |
| 通过 `--version` 锁定工具版本 | ✅ | ❌（靠 rev tag） |
| 自定义 `.clang-tidy` 配置文件 | ✅ | ❌ |
| 编译数据库自动检测 | ✅ | ❌ |
| `--dry-run`（只检查不修改） | ✅ | ❌ |
| `--fix`（自动修复 clang-tidy 问题） | ✅ | ❌ |
| `--verbose` 详细输出 | ✅ | ❌ |
| 并行执行（`--jobs`） | ✅ | ❌ |

`mirrors-clang-format` 做的事情很单一：下载一个 `clang-format` 二进制，然后跑在改动的文件上。如果你的项目只需要格式化，它够用。

但现实中的 C/C++ 项目，真正让人头疼的不是代码风格不统一，而是 clang-tidy 的那些静态分析检查 —— 内存泄漏、未定义行为、性能陷阱。这些才是 `pre-commit` 阶段最值得拦截的问题。

---

## 快速上手

在你的 `.pre-commit-config.yaml` 里加一段配置：

```yaml
repos:
  - repo: https://github.com/cpp-linter/cpp-linter-hooks
    rev: v1.4.1
    hooks:
      - id: clang-format
        args: [--style=file]
      - id: clang-tidy
        args: [--checks=.clang-tidy]
```

然后：

```bash
pre-commit install
pre-commit run --all-files
```

第一次运行会从 PyPI 下载对应的 clang 工具，之后就会缓存在 pre-commit 的环境里。

---

## 几个实用的配置细节

### 锁定工具版本

一个容易被忽略的点：`rev` 是 cpp-linter-hooks 的项目版本，不是 clang 工具的版本。如果你不显式指定，每次升级 `rev` 都可能静默换掉 clang-format / clang-tidy 的版本，导致格式化结果不一致。

建议加上 `--version`：

```yaml
- id: clang-format
  args: [--style=file, --version=21]
- id: clang-tidy
  args: [--checks=.clang-tidy, --version=21]
```

这样工具版本就被锁定在 clang 21，不受项目 `rev` 升级影响。

### 编译数据库

clang-tidy 需要知道编译参数才能做准确的静态分析。如果你的项目用 CMake 或 Meson 构建，生成 `compile_commands.json` 之后，cpp-linter-hooks 会自动检测常见构建目录（`build/`、`out/`、`cmake-build-debug/` 等），不需要额外配置。

也可以显式指定：

```yaml
- id: clang-tidy
  args: [--compile-commands=build, --checks=.clang-tidy]
```

生成编译数据库的命令：

```bash
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -Bbuild .
```

### 自动修复

clang-tidy 的 `--fix` 可以自动修复部分检查项的问题。cpp-linter-hooks 从 v1.4.0 开始支持这个参数，但默认不开 —— 因为自动修改源代码有风险，你需要自己判断是否信任它。

```yaml
- id: clang-tidy
  args: [--checks=.clang-tidy, --fix]
```

注意：开启 `--fix` 后，并行执行（`--jobs`）会自动禁用，防止多个进程同时写入同一个头文件。

### 性能优化

大项目跑全量 clang-tidy 可能会比较慢。两种方式优化：

**限制检查范围**，用 `files` 过滤：

```yaml
- id: clang-tidy
  args: [--checks=.clang-tidy, --version=21]
  files: ^(src|include)/.*\.(cpp|cc|cxx|h|hpp)$
```

**开启并行**：

```yaml
- id: clang-tidy
  args: [--checks=.clang-tidy, --jobs=4]
```

日常开发时，也可以只检查变更的文件：

```bash
pre-commit run --files $(git diff --name-only)
```

---

## 和 cpp-linter-action 的关系

如果你关注过 C/C++ 的 CI 工具，可能见过 [cpp-linter-action](https://github.com/cpp-linter/cpp-linter-action)（GitHub Marketplace 上 139 星）。它是一个 GitHub Action，在 CI 流水线里跑 clang-format 和 clang-tidy，然后把结果以 file annotations、thread comments、PR review 的形式展示出来。

cpp-linter-hooks 和它是同一组织下的两个互补工具：

- **cpp-linter-action**：跑在 CI 里，面向 PR 审查流程
- **cpp-linter-hooks**：跑在本地 `git commit` 之前，面向开发者日常提交

两者共用相同的 `.clang-format` 和 `.clang-tidy` 配置，本地通过的代码到 CI 上也不会出问题。这是一种典型的"本地 + CI 双重保障"模式。

---

## 最后

cpp-linter-hooks 目前是我在 cpp-linter 组织下维护的主要项目之一。从 2022 年到现在，陆续加了版本锁定、编译数据库检测、自动修复、并行执行这些功能，基本上覆盖了 C/C++ 项目在 pre-commit 阶段的核心需求。

如果你在做 C/C++ 开发，或者维护一个 C/C++ 开源项目，可以试试把它加到 `.pre-commit-config.yaml` 里。几分钟就能跑起来，之后每次提交前自动检查格式和潜在问题，不用再等到 CI 红了才回头修。

- GitHub：https://github.com/cpp-linter/cpp-linter-hooks
- PyPI：https://pypi.org/project/cpp-linter-hooks/

有问题去 GitHub 提 Issue，欢迎反馈。

老司机们，我们下期见～

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
