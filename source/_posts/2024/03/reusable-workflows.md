---
title: 你一定要了解的 GitHub Action 特性：可重用工作流（Reusable Workflows）
tags:
  - GitHub
  - Jenkins
categories:
  - GitHub
author: shenxianpeng
date: 2024-03-25 18:34:18
---

## 什么是 Reusable Workflows

如果你使用过 GitHub Actions，那么你一定要了解 Reusable Workflows 这个特性，它允许你定义工作流并在多个仓库中重复使用它们。

> GitHub Actions 是 GitHub 自家的 CI/CD 工具。其他主流的 CI/CD 工具还有 Jenkins，Azure DevOps，Travis CI 等。

通过 GitHub Reusable Workflows 你可以将常见的工作流程定义在单独的 Git 仓库，然后在其他仓库中引用这些工作流，而无需在每个仓库中重复定义它们，这样做带来的好处包括：

* 一致性: 确保你的团队或组织在不同的仓库中使用相同的标准化工作流程，保持一致性。
* 维护性: 对工作流程进行更改或更新你只需在一个地方进行修改，而不必修改多个仓库中的代码。
* 重用性: 将通用的工作流程分离出来，在需要时可以在任何项目中重用，提高了代码的重用性和可维护性。

总的来说，GitHub Reusable Workflows 使得在 GitHub Actions 中管理和组织工作流程变得更加灵活和可维护。

## 如何使用 Reusable Workflows

使用 GitHub Reusable Workflows 可以让你在 `.github` 或是其他仓库创建一个工作流，然后在其他仓库中调用该工作流。

以下是使用 GitHub Reusable Workflows 的一般步骤：

1. **创建可重用工作流程**：
   - 在你的 GitHub 账户下创建一个新的仓库用于存储你的可重用工作流程。
   - 在仓库中创建一个名为 `.github/workflows` 的目录（如果不存在的话）。
   - 在该目录下创建一个 YAML 文件，用于定义你的工作流程。

2. **定义参数化工作流程（可选）**：
   - 如果你希望你的工作流程是可参数化的，可以在 workflows 中使用 `inputs` 关键字定义参数。

3. **将工作流程提交到仓库**：
   - 将你创建的工作流程 YAML 文件提交到仓库，并确保它位于 `.github/workflows` 目录中。

4. **在其他仓库中使用工作流程**：
   - 打开你希望使用该工作流程的其他仓库。在 `.github/workflows` 目录下创建一个 YAML 文件，指向你之前创建的可重用工作流程的 YAML 文件。

5. **提交更改并触发工作流程**：
   - 将对仓库的更改提交到 GitHub，并将它们推送到远程仓库。
   - GitHub 将自动检测到新的工作流程文件，并根据触发器（例如 `push`、`pull_request` 等）来触发工作流程的执行。

以下是一个简单的示例，演示如何创建和使用可重用工作流程：

假设你在名为 `reuse-workflows-demo` 的仓库中 `.github/workflows` 目录下创建了一个名为 `build.yml` 的工作流程文件，用于构建你的项目。该文件的内容如下：

> 如果不在 `.github/workflows` 目录下，你会遇到这个错误 `invalid value workflow reference: references to workflows must be rooted in '.github/workflows'`

```yaml
name: Build

on:
  workflow_call:
    inputs:
      target:
        required: true
        type: string
        default: ""

jobs:
  build:
    strategy:
      matrix:
        target: [dev, stage, prod]
    runs-on: ubuntu-latest
    steps:
      - name: inputs.target = ${{ inputs.target }}
        if: inputs.target
        run: echo "inputs.target = ${{ inputs.target }}."

      - name: matrix.targe = ${{ matrix.target }}
        if: matrix.target
        run: echo "matrix.targe = ${{ matrix.target }}."
```

然后，在你的其他仓库中的 `.github/workflows` 目录下你可以创建一个 workflow `build.yml` 指向该文件，例如：

```yaml
name: Build

on:
  push:
  pull_request:
  workflow_dispatch:

jobs:
  call-build:
    uses: shenxianpeng/reuse-workflows-demo/.github/workflows/build.yml@main
    with:
      target: stage
```

### GitHub Reusable Workflows 的 7 点最佳实践：

1. **模块化设计**：将工作流程分解为小的、可重用的模块，每个模块专注于执行特定的任务。这样可以提高工作流程的灵活性和可维护性，并使其更容易被重用和组合。
2. **参数化配置**：使工作流程能够接受参数，以便在每次使用时进行配置。这样可以使工作流程更通用，适应不同项目和环境的需求。
3. **版本控制**：确保你的可重用工作流程受到版本控制，并定期更新以反映项目需求的变化。可以使用 GitHub 的分支或 tag 来管理工作流程的不同版本，并在需要时轻松切换或回滚。
4. **文档和注释**：为工作流程提供清晰的文档和注释，以帮助其他开发人员理解其目的和操作步骤。注释关键步骤的目的和实现细节，以便其他人可以轻松理解和修改工作流程。
5. **安全性**：谨慎处理包含敏感信息（如凭据、密钥等）的工作流程文件，确保它们不会意外地泄露。将敏感信息存储在 GitHub 的 Secrets 中，并在工作流程中使用 Secrets 来访问这些信息。
6. **测试和验证**：在引入可重用工作流程到项目之前，进行测试和验证，确保它们能够正确地集成和执行所需的操作。可以在单独的测试仓库中模拟和测试工作流程，以确保其正确性和可靠性。
7. **优化性能**：优化工作流程的性能，尽量减少不必要的步骤和资源消耗，以确保工作流程能够在合理的时间内完成任务，并尽量减少对系统资源的占用。

遵循这些最佳实践可以帮助你更好地利用 GitHub Reusable Workflows 并为你的项目和团队提供更高效和可维护的自动化工作流程。

## Reusable Workflows 和 Jenkins Shared Library 有什么不同和相同

最后，说一下我对 GitHub Reusable Workflows 和 Jenkins Shared Library 的理解和总结。有一些相似之处，但也有一些区别。

**相同点：**

1. 可重用性: 两者都旨在提供一种机制，使得可以将通用的自动化工作流程定义为可重用的组件，并在多个项目中共享和重用。
2. 组织性: 都有助于更好地组织和管理自动化工作流程，使其易于维护和更新。
3. 参数化: 都支持参数化，使得可以根据需要在不同的上下文中定制和配置工作流程。

**不同点：**

1. 平台: Reusable Workflows 是 GitHub Actions 的一部分，而 Shared Library 是 Jenkins 的功能。它们在不同的平台上运行，具有不同的生态系统和工作原理。
2. 语法: Reusable Workflows 使用 YAML 语法来定义工作流程，而 Shared Library 使用 Groovy 语言来定义共享库。
3. 易用性: Reusable Workflows 在 GitHub 平台上使用起来相对较简单，特别是对于那些已经在 GitHub 上托管代码的项目。Shared Library 则需要配置 Jenkins 服务器和相关插件，并且需要对 Jenkins 构建流程有一定的了解。

综上所述，尽管 GitHub Reusable Workflows 和 Jenkins Shared Library 都旨在提供可重用的自动化工作流程，并且具有一些相似之处，但是它们在平台、语法、易用性等方面存在显著的差异。

具体选择使用哪种取决于你的需求、工作流程和所需要使用的平台。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
