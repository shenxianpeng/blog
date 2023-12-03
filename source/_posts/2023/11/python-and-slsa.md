---
title: Python 和 SLSA 💃
tags:
  - SLSA
  - Python
categories:
  - DevSecOps
author: shenxianpeng
date: 2023-11-15 14:25:39
---

由于近些年针对软件的供应链的攻击越来越频繁，据 SonaType 的统计从 2019 年到 2022 年针对开源软件的攻击增长了 742%，因此 2021 年 Google 提出的解决方案是软件工件供应链级别（Supply chain Levels for Software Artifacts，"SLSA"）

![Software supply chain attacks](python-and-slsa/attacks.png)

本篇将介绍在 Python 生态系统中，我们如何使用 SLSA 框架来生成和验证 Python 工件的来源，从而让你的 SLSA Level 从 L0/L1 到 L3。

注意：本文介绍的是针对**托管在 GitHub 上的 Python 项目**。SLSA 框架可通过 GitHub Actions 来实现开箱即用，只需较少的配置即可完成。

对于托管在非 GitHub 上的项目（例如 Bitbucket）可以尝试 [Witness](https://witness.dev/)，下一篇我将更新关于如何使用 Witness。

## 内容

1. [构建纯净的Python包](#构建纯净的Python包)
2. [生成出处证明](#生成出处证明)
3. [上传到PyPI](#上传到PyPI )
4. [验证Python包的来源](#验证Python包的来源)
5. [文中用到的项目](#文中用到的项目)

下面是从维护人员到用户的端到端工作流程：从构建 Wheel package -> 生成出处 -> 验证出处 -> 发布到 PyPI -> 以及用户验证出处 -> 安装 wheel。接下来让我们一起来完成这其中的每一步。

如果你想了解 Python 打包的流程或是术语可以参见[Python 打包用户指南](https://packaging.python.org/en/latest/overview/#packaging-python-libraries-and-tools)。

![端到端流程](python-and-slsa/workflows.svg)

<!-- more -->

## 构建纯净的Python包

构建纯 Python 包通常只有两个工件：即纯 Python Wheel Package 和源代码 distribution。可以使用命令 [`python3 -m build`](https://pypi.org/project/build/) 从源代码构建。

下面是 GitHub Actions job 定义来构建 Wheel Package 和源代码 distribution，并为每个工件创建 SHA-256 哈希值：

```yaml
jobs:
  build:
    steps:
      - uses: actions/checkout@...
      - uses: actions/setup-python@...
        with:
          python-version: 3.x
      - run: |
          # 安装 build，创建 sdist 和 wheel
          python -m pip install build
          python -m build

          # 收集所有文件的哈希值
          cd dist && echo "hashes=$(sha256sum * | base64 -w0)" >> $GITHUB_OUTPUT
      - uses: actions/upload-artifacts@...
        with:
          path: ./dist
```

这里将 build 完的 wheel package 上传到 GitHub Artifacts 存起来，用作后续在 “上传到PyPI” job 中使用。另外还将 `dist` 下的所有文件的哈希值存储在 `hashes` 用作后续的 `provenance` job 的输入。

> 注意： SLSA 使用 `sha265sum` 的输出作为出处证明中 `subject-base64` 字段的输入。`sha256sum` 的输出是一个或多个对散列 + 名称。

## 生成出处证明

现在我们已经构建了 sdist 和 wheel，我们可以从文件哈希生成来出处证明。

因为我们需要将 Build 阶段的的输出作为这里生成出处的输入，因此这里使用了 [needs](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idneeds) 选项来作为 `provenance` job 执行的前提条件。可以看到上面生成的哈希值在这里被 `subject-base64` 所使用。

```yaml
jobs:
  provenance:
    needs: [build]
    uses: slsa-framework/slsa-github-builder/.github/workflows/generator_generic_slsa3.yml@v1.9.0
    permissions:
      # 需要检测 GitHub 操作环境
      actions: read
      # 需要通过 GitHub OIDC 创建出处
      id-token: write
      # 需要创建并上传到 GitHub Releases
      contents: write
    with:
      # 生成的 package SHA-256 哈希值
      subject-base64: ${{ provenance.needs.build.output.hashes }}
      # 将出处文件上传到 GitHub Release
      upload-assets: true
```

你会注意到 SLSA builders 使用[可重用工作流](https://docs.github.com/en/actions/using-workflows/reusing-workflows)功能来证明给定的 builders 行为不能被用户或其他进程修改。

出处证明文件是 [JSON lines](https://jsonlines.org/)，以 `.intoto.jsonl` 结尾。`*.intoto.jsonl` 文件可以包含多个工件的证明，也可以在同一文件中包含多个出处证明。该 `.jsonl` 格式意味着该文件是一个 “JSON lines” 文件，即每行一个 JSON 文档。

> 注意：这里有一点令人困惑的是 GitHub job 中的 `id-token` 需要 `write` 权限才能读取 GitHub OIDC 令牌。`read` 不允许你读取 OIDC...🤷。有关 `id-token` 权限的更多信息，请参阅 [GitHub 文档](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect#adding-permissions-settings)。

## 上传到PyPI 

我们使用官方 [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) GitHub Action 将 wheel 包上传到 PyPI。

注意：`publish` job 需要在 `build` 和 `provenance` 都完成后开始执行，这意味着我们可以假设  `provenance` job 已经为我们起草了 GitHub Release（因为 `upload-assets: true` 的设置），并且我们可以假设该 job 已成功。如果不先创建来 provenance 文件，我们不想将这些 wheel 包上传到 PyPI，因此我们最后上传到 PyPI。

![发布](python-and-slsa/publish.svg)

```yaml
publish:
  needs: ["build", "provenance"]
  permissions:
    contents: write
  runs-on: "ubuntu-latest"
  steps:
  # 下载已构建的 distributions
  - uses: "actions/download-artifact@..."
    with:
      name: "dist"
      path: "dist/"
  # 上传 distributions 到 GitHub Release
  - env:
      GITHUB_TOKEN: "${{ secrets.GITHUB_TOKEN }}"
    run: gh release upload ${{ github.ref_name }} dist/* --repo ${{ github.repository }}
  # 发布 distributions 到 PyPI
  - uses: "pypa/gh-action-pypi-publish@..."
    with:
      user: __token__
      password: ${{ secrets.PYPI_TOKEN }}
```

## 验证Python包的来源

让我们使用一个真正的 Python 项目来验证它的出处。以 urllib3 项目为例，它在 GitHub Releases 发布了版本中包含出处证明，这里演示的是使用它的最新版本 [`2.1.0`](https://github.com/urllib3/urllib3/releases/tag/2.1.0) 。

首先我们需要下载 [slsa-verifier](https://github.com/slsa-framework/slsa-verifier/releases) 用来验证出处。下载完 `slsa-verifier` 工具后，让我们从 PyPI 获取 urllib3 wheel 包，而不使用 [pip download](https://pip.pypa.io/en/stable/cli/pip_download/). 我们使用该 [`--only-binary`](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-only-binary) 选项强制 pip 下载 wheel。

![安装](python-and-slsa/install.svg)

```bash
python3 -m pip download --only-binary=:all: urllib3
Collecting urllib3
  Downloading urllib3-2.1.0-py3-none-any.whl.metadata (6.4 kB)
Downloading urllib3-2.1.0-py3-none-any.whl (104 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 104.6/104.6 kB 761.0 kB/s eta 0:00:00
Saved ./urllib3-2.1.0-py3-none-any.whl
Successfully downloaded urllib3
```

下载软件包后，我们需要从 GitHub 版本下载出处证明。我们需要使用与包版本相同的 GitHub Release 来确保获得正确的出处证明，因此 tag 也是 2.1.0。

```bash
curl --location -O https://github.com/urllib3/urllib3/releases/download/2.1.0/multiple.intoto.jsonl
```

该出处文件的名称为 `multiple.intoto.jsonl`，这是一个包含多个工件证明的出处证明的标准名称。

此时，我们当前的工作目录中应该有两个文件：wheel 和出处证明，`ls` 浏览一下确保已经准备好了：

```bash
ls
multiple.intoto.jsonl  urllib3-2.1.0-py3-none-any.whl
```

从这里我们可以使用 `slsa-verifier` 来验证出处。我们可以验证最重要的事情，即哪个 GitHub 仓库实际构建了 wheel，以及其他信息，例如 git 标签、分支和建造者 ID：

源存储库 (`--source-uri`)
建造者 ID (`--builder-id`)
Git 分支 (`--source-branch`)
git 标签 (`--source-tag`)

```bash
# 这里仅验证 wheel package 的 GitHub 仓库
slsa-verifier verify-artifact --provenance-path multiple.intoto.jsonl --source-uri github.com/urllib3/urllib3 urllib3-2.1.0-py3-none-any.whl 
Verified signature against tlog entry index 49513169 at URL: https://rekor.sigstore.dev/api/v1/log/entries/24296fb24b8ad77a08c2f012d69948ed5d12e8e020852bb7936ea9208d684688e5108cca859a3302
Verified build using builder "https://github.com/slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@refs/tags/v1.9.0" at commit 69be2992f8a25a1f27e49f339e4d5b98dec07462
Verifying artifact urllib3-2.1.0-py3-none-any.whl: PASSED

PASSED: Verified SLSA provenance
```

**成功了**！🥳 我们已经验证了这个 wheel 的出处，所以现在我们可以放心的安装它，因为我们知道它是按照我们的预期构建的：

```bash
python3 -m pip install urllib3-2.1.0-py3-none-any.whl 
Defaulting to user installation because normal site-packages is not writeable
Processing ./urllib3-2.1.0-py3-none-any.whl
Installing collected packages: urllib3
  Attempting uninstall: urllib3
    Found existing installation: urllib3 2.0.5
    Uninstalling urllib3-2.0.5:
      Successfully uninstalled urllib3-2.0.5
Successfully installed urllib3-2.1.0
```

## 文中用到的项目

以下这些是本文使用的所有项目和工具：

* [SLSA GitHub Builder](https://github.com/slsa-framework/slsa-github-generator/blob/main/internal/builders/generic/README.md)
* [slsa-framework/slsa-verifier](https://github.com/slsa-framework/slsa-verifier)
* [pypa/gha-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)
* [pypa/build](https://github.com/pypa/build)
* [urllib3/urllib3](https://github.com/urllib3/urllib3/blob/main/.github/workflows/publish.yml)

> 英文原文：https://sethmlarson.dev/python-and-slsa 

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
