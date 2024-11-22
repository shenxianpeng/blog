---
title: Commit Check 更新：新增两个实用功能提升代码质量保障
tags:
  - commit-check
  - DevOps
categories:
  - DevOps
draft: true
date: 2024-11-23 00:00:00
author: shenxianpeng
---

最近有用户提了两个需求，一个是支持 pull request 增加评论；另外一个是检查 pull request 是否已经 rebase 了。

过去几天经过几个晚上的努力，现在正式宣布在最新的 commit-check 以及 commit-check-action 中增加了两个重要功能：`pr-comments` 和 `base-merge`。

这两个功能旨在进一步提升 Pull Request (PR) 的检查能力。

在本文中，我将为大家详细介绍它们的作用以及如何使用。

1. pr-comments: 自动添加检查结果到 Pull Request
在团队合作开发中，PR 通常是代码审核的主要入口。为了让代码检查结果更直观可见，pr-comments 提供了一种新方式：

当代码提交触发 CI/CD Pipeline 后，commit-check 会自动在 Pull Request 界面中，以评论的形式呈现检查结果。

无需额外点击或者切换到日志文件，开发者可以直接在 PR 的对话区域查看检测结果，方便快速定位问题。

成功和失败的示例效果：

![pr-comments success](commit-check-updates/success-pr-comments.png)

![pr-comments failure](commit-check-updates/failure-pr-comments.png)

注：pr-comments 仅支持 [commit-check-action](https://github.com/commit-check/commit-check-action) 。

2. base-merge: 确保分支基于目标分支

在开发过程中，有些团队希望每个 pull request 都是基于最新的目标分支进行开发。

commit-check 提供了一个新的选项：`base-merge`，这个功能可以帮助团队确保分支是已经 rebase 了。

自动检查当前分支是否基于指定的目标分支（例如 main 或 master）。
如果检测到基线不正确，commit-check 会返回错误，让 CI Pipeline 失败，并给出明确提示。

注：base-merge 不仅支持 [commit-check](https://github.com/commit-check/commit-check)，还支持 [commit-check-action](https://github.com/commit-check/commit-check-action) 。

## 什么是 Commit Check

对了如果你还不知道什么是 commit-check，这里我要隆重的介绍以下：

Commit Check 是一个免费且强大的工具，用于强制执行提交元数据标准，包括提交消息、分支命名、提交者姓名/邮箱以及提交签名，变基。它的错误信息和建议命令都可以完全自定义，确保团队之间的一致性。

作为 [GitHub Enterprise 元数据限制](https://docs.github.com/en/enterprise-server@3.11/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#metadata-restrictions)和 Bitbucket 付费插件 [Yet Another Commit Checker](https://marketplace.atlassian.com/apps/1211854/yet-another-commit-checker?tab=overview&hosting=datacenter) 的替代方案，Commit Check 通过集成 DevOps 原则和基础设施即代码（IaC）脱颖而出。

那么如何使用 commit-check 呢？有以下几种方式。

## 配置

### 使用默认配置

如果你没有设置 `.commit-check.yml`，Commit Check 将使用默认配置。提交消息将遵循 Conventional Commits 规则，分支命名遵循 Conventional Branch 规则。

### 自定义配置

如果你需要更改配置，可以在 `.commit-check.yml` 中进行配置，如下所示：

```yaml
checks:
  - check: message
    regex: '^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test){1}(\([\w\-\.]+\))?(!)?: ([\w ])+([\s\S]*)|(Merge).*|(fixup!.*)'
    error: "The commit message should be structured as follows:\n\n
    <type>[optional scope]: <description>\n
    [optional body]\n
    [optional footer(s)]\n\n
    More details please refer to https://www.conventionalcommits.org"
    suggest: please check your commit message whether matches above regex

  - check: branch
    regex: ^(bugfix|feature|release|hotfix|task|chore)\/.+|(master)|(main)|(HEAD)|(PR-.+)
    error: "Branches must begin with these types: bugfix/ feature/ release/ hotfix/ task/ chore/"
    suggest: run command `git checkout -b type/branch_name`

  - check: author_name
    regex: ^[A-Za-z ,.\'-]+$|.*(\[bot])
    error: The committer name seems invalid
    suggest: run command `git config user.name "Your Name"`

  - check: author_email
    regex: ^.+@.+$
    error: The committer email seems invalid
    suggest: run command `git config user.email yourname@example.com`

  - check: commit_signoff
    regex: Signed-off-by:.*[A-Za-z0-9]\s+<.+@.+>
    error: Signed-off-by not found in latest commit
    suggest: run command `git commit -m "conventional commit message" --signoff`

  - check: merge_base
    regex: main # it can be master, develop, devel etc based on your project.
    error: Current branch is not rebased onto target branch
    suggest: Please ensure your branch is rebased with the target branch
```

## 用法

### 作为 GitHub Actions

```yaml
name: Commit Check

on:
  push:
  pull_request:
    branches: 'main'

jobs:
  commit-check:
    runs-on: ubuntu-latest
    permissions:  # use permissions because of use pr-comments
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}  # checkout PR HEAD commit
          fetch-depth: 0  # required for merge-base check
      - uses: commit-check/commit-check-action@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} # use GITHUB_TOKEN because of use pr-comments
        with:
          message: true
          branch: true
          author-name: true
          author-email: true
          commit-signoff: true
          merge-base: false
          job-summary: true
          pr-comments: ${{ github.event_name == 'pull_request' }}
```

### 作为 pre-commit hook

将下面的配置添加到你的 `.pre-commit-config.yaml` 文件中:

```yaml
-   repo: https://github.com/commit-check/commit-check
    rev: the tag or revision
    hooks: # support hooks
    -   id: check-message  # requires hook prepare-commit-msg
    -   id: check-branch
    -   id: check-author-name
    -   id: check-author-email
    -   id: check-commit-signoff
    -   id: check-merge-base # requires download all git history
```

### 作为 CLI 工具

从 pypi 安装:

```bash
pip install commit-check

# example
commit-check --message --branch --author-name --author-email --commit-signoff --merge-base
```

更多关于 commit-check 的用法，可以参考 [readme](https://github.com/commit-check/commit-check)。


如果有任何问题或建议，欢迎在 [GitHub Issues](https://github.com/commit-check/commit-check/issues) 中提出。


---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
