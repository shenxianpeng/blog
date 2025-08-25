---
title: Must-Know GitHub Action Feature: Reusable Workflows
summary: This article introduces the Reusable Workflows feature of GitHub Actions, helping developers and teams manage and reuse CI/CD processes more efficiently.
tags:
  - GitHub
  - Jenkins
author: shenxianpeng
date: 2024-03-25
---

## What are Reusable Workflows

If you've used GitHub Actions, you must know about the Reusable Workflows feature. It allows you to define workflows and reuse them across multiple repositories.

> GitHub Actions is GitHub's own CI/CD tool. Other mainstream CI/CD tools include Jenkins, Azure DevOps, Travis CI, etc.

With GitHub Reusable Workflows, you can define common workflows in a separate Git repository and then reference these workflows in other repositories without having to redefine them in each repository.  The benefits include:

* **Consistency:** Ensures your team or organization uses the same standardized workflows across different repositories, maintaining consistency.
* **Maintainability:** Changes or updates to the workflow only need to be made in one place, eliminating the need to modify code in multiple repositories.
* **Reusability:** Separates common workflows, allowing reuse in any project as needed, improving code reusability and maintainability.

In general, GitHub Reusable Workflows makes managing and organizing workflows in GitHub Actions more flexible and maintainable.


## How to Use Reusable Workflows

GitHub Reusable Workflows allows you to create a workflow in `.github` or another repository and then call that workflow from other repositories.

Here are the general steps for using GitHub Reusable Workflows:

1. **Create a Reusable Workflow:**
   - Create a new repository under your GitHub account to store your reusable workflows.
   - Create a directory named `.github/workflows` in the repository (if it doesn't exist).
   - Create a YAML file in this directory to define your workflow.

2. **Define a Parameterized Workflow (Optional):**
   - If you want your workflow to be parameterized, you can define parameters using the `inputs` keyword in your workflow.

3. **Commit the Workflow to the Repository:**
   - Commit your created workflow YAML file to the repository, ensuring it's located in the `.github/workflows` directory.

4. **Use the Workflow in Other Repositories:**
   - Open the other repository where you want to use this workflow. Create a YAML file in the `.github/workflows` directory that points to the YAML file of your previously created reusable workflow.

5. **Commit Changes and Trigger the Workflow:**
   - Commit the changes to the repository and push them to the remote repository.
   - GitHub will automatically detect the new workflow file and trigger workflow execution based on triggers (e.g., `push`, `pull_request`, etc.).

Here's a simple example demonstrating how to create and use a reusable workflow:

Suppose you create a workflow file named `build.yml` in the `.github/workflows` directory of the `reuse-workflows-demo` repository to build your project. The file contents are as follows:

> If not in the `.github/workflows` directory, you will encounter this error `invalid value workflow reference: references to workflows must be rooted in '.github/workflows'`

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

Then, in the `.github/workflows` directory of your other repository, you can create a workflow `build.yml` pointing to this file, for example:

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

For more real-world examples of Reusable Workflows, refer to the [.github](https://github.com/cpp-linter/.github) repository under the [cpp-linter organization](https://github.com/cpp-linter).

```bash
# cpp-linter/.github/.github/workflows
.
├── codeql.yml
├── main.yml
├── mkdocs.yml
├── pre-commit.yml
├── py-coverage.yml
├── py-publish.yml
├── release-drafter.yml
├── snyk-container.yml
├── sphinx.yml
└── stale.yml
```

### 7 Best Practices for GitHub Reusable Workflows:

1. **Modular Design:** Break down workflows into small, reusable modules, each focusing on a specific task. This improves workflow flexibility and maintainability, making them easier to reuse and combine.
2. **Parameterized Configuration:** Allow workflows to accept parameters for configuration with each use. This makes workflows more versatile, adapting to different project and environment needs.
3. **Version Control:** Ensure your reusable workflows are version-controlled and updated regularly to reflect changing project requirements. Use GitHub branches or tags to manage different workflow versions and easily switch or roll back when needed.
4. **Documentation and Comments:** Provide clear documentation and comments for workflows to help other developers understand their purpose and steps.  Comment on the purpose and implementation details of key steps so others can easily understand and modify the workflow.
5. **Security:** Carefully handle workflow files containing sensitive information (such as credentials, keys, etc.) to prevent accidental leaks. Store sensitive information in GitHub Secrets and use Secrets to access this information in the workflow.
6. **Testing and Validation:** Test and validate reusable workflows before introducing them to projects to ensure they integrate and execute correctly.  Simulate and test workflows in a separate test repository to ensure correctness and reliability.
7. **Performance Optimization:** Optimize workflow performance, minimizing unnecessary steps and resource consumption to ensure workflows complete tasks within a reasonable time and minimize system resource usage.

Following these best practices helps you better utilize GitHub Reusable Workflows and provides your projects and teams with more efficient and maintainable automated workflows.

## Differences and Similarities between Reusable Workflows and Jenkins Shared Library

Finally, let's discuss my understanding and summary of GitHub Reusable Workflows and Jenkins Shared Library. There are similarities, but also differences.

**Similarities:**

1. **Reusability:** Both aim to provide a mechanism to define common automated workflows as reusable components, sharing and reusing them across multiple projects.
2. **Organization:** Both help better organize and manage automated workflows, making them easier to maintain and update.
3. **Parameterization:** Both support parameterization, allowing workflows to be customized and configured in different contexts as needed.

**Differences:**

1. **Platform:** Reusable Workflows are part of GitHub Actions, while Shared Library is a Jenkins feature. They run on different platforms with different ecosystems and working principles.
2. **Syntax:** Reusable Workflows use YAML syntax to define workflows, while Shared Library uses Groovy to define shared libraries.
3. **Ease of Use:** Reusable Workflows are relatively simple to use on the GitHub platform, especially for projects already hosted on GitHub. Shared Library requires configuring the Jenkins server and related plugins and requires some understanding of the Jenkins build process.

In summary, although GitHub Reusable Workflows and Jenkins Shared Library both aim to provide reusable automated workflows and share some similarities, they have significant differences in platform, syntax, and ease of use.

The specific choice depends on your needs, workflow, and the platform you need to use.

---

Please indicate the author and source when reprinting this article, and do not use it for any commercial purposes. Welcome to follow the WeChat official account "DevOps攻城狮"