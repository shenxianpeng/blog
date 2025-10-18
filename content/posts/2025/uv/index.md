---
title: 还在用 pip 和 venv？那你可真落伍了，赶紧体验 uv！
summary: |
  uv 是一个由 Astral 团队开发的 Python 包管理工具，它能替代 pip、venv、pip-tools 的功能，提供更快的依赖解析速度和更现代的项目管理方式。
tags:
  - uv
  - pip
authors:
  - shenxianpeng
date: 2025-05-05
---

如果你已经习惯了 `pip install`、手动创建虚拟环境、自己管理 requirements.txt，那你可能会对 [uv](https://docs.astral.sh/uv/) 有些惊喜。

这是一个由 [Astral](https://astral.sh/) 团队开发、用 Rust 写的 Python 包管理工具，它不仅能替代 pip、venv、pip-tools 的功能，还带来了更快的依赖解析速度，以及一套更现代的项目管理方式。

### 从 `uv init` 开始，一键创建项目骨架

我们不从 “怎么装 uv” 讲起，而是从 “怎么用 uv 创建一个项目” 开始。



```bash
uv init
```

运行这条命令后，uv 会帮你：

* 创建 `.venv` 虚拟环境；
* 初始化 `pyproject.toml` 配置文件；
* （可选）添加依赖；
* 生成 `uv.lock` 锁定文件；
* 将 `.venv` 设置为当前目录默认环境（无需手动激活）；

整个过程只需一个命令，就能完成以往多个步骤，是构建 Python 项目的更优起点。

### 使用 `uv add` 安装依赖（而不是 pip install）

传统的写法是：

```bash
pip install requests
```

但在 uv 的世界里，添加依赖是这样的：

```bash
uv add requests
```

这样做的好处是：

* 自动写入 `pyproject.toml` 的 `[project.dependencies]`；
* 自动安装到 `.venv` 中；
* 自动更新 `uv.lock` 锁定文件；
* 无需再维护 `requirements.txt`。

如果你想添加开发依赖（比如测试或格式化工具），可以：

```bash
uv add --dev pytest ruff
```

想移除依赖？

```bash
uv remove requests
```

### 运行项目脚本或工具：`uv venv` + `uvx`

uv 的虚拟环境默认安装在 `.venv` 中，但你**不需要每次 source activate**，只需执行：

```bash
uv venv
```

这会确保 `.venv` 存在并自动配置成当前 shell 的默认 Python 环境。之后你运行脚本或工具时，不用担心路径问题。

更妙的是，uv 提供了一个 `uvx` 命令，跟 `pipx` 以及 Node.js 的 `npx` 类似，可以直接运行安装在项目里的 CLI 工具。

比如我们用 `ruff` 来检查或格式化 Python 代码：

```bash
uvx ruff check .
uvx ruff format .
```

现在用 `uvx`，你不需要再装一堆全局工具，也不用再通过 `pre-commit` 来统一调用命令——项目内直接用，跨平台还省心。

### 项目结构示例

经过 `uv init` 和一些 `uv add` 之后，一个干净的 Python 项目结构可能是这样的：

```
my-project/
├── .venv/               ← 虚拟环境
├── pyproject.toml       ← 项目配置（依赖、元数据等）
├── uv.lock              ← 锁定的依赖版本
├── main.py              ← 项目入口脚本
```

### 使用体验如何？

我最近已经把 uv 作为新项目的默认工具：

* 不再手动写 `requirements.txt`
* 不再纠结 `poetry.lock` 和 `pyproject.toml` 的混用
* 依赖安装速度非常快，第一次装大型项目时速度能快 3～5 倍
* 搭配 `ruff` 作为 Lint + Format 工具，完全不需要再装 black、flake8

在 CI 中，我也逐步用它替代 `pip install -r requirements.txt`，用锁定文件构建环境，一致性更强。

### 总结

如果你：

* 对 `pip install` 安装慢感到不满；
* 不想再写一堆 requirements 文件；
* 想要更现代、更快、更自动化的 Python 项目结构；

那你应该试试 `uv`。它是更快、更更现代的包管理器工具集。

从下个项目开始，不妨从 `uv init` 开始吧。

项目地址：[https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
