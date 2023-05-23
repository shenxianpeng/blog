---
title: 程序员自我修养之Git提交信息和分支创建规范（工具篇）
tags:
  - Git
  - Branch
categories:
  - Git
author: shenxianpeng
date: 2023-05-09 19:00:00
---

Git 提交信息和 Git 分支命名规范是团队协作中非常重要的一部分，它们能够使代码库更加规范、易于维护和理解。

我们需要通过工具来帮助实现Git提交信息和分支创建规范，本篇将介绍如何使用 [Commit Check](https://github.com/commit-check/commit-check) 这个工具来验证提交信息、分支命名、提交用户名字、提交用户邮箱等是否符合规范。

更多关于Git提交信息和分支创建规范可以参看我之前发布的文章[《程序员自我修养之Git提交信息和分支创建规范》](https://shenxianpeng.github.io/2020/09/commit-messages-specification/)，这里不再赘述。

## Commit Check 简介

Commit Check 是一个可以检查 Git 提交信息，分支命名、提交者用户名、提交者邮箱等等。它是 [Yet Another Commit Checker](https://docs.mohami.io/yet-another-commit-checker-yacc/) 的开源平替版。

## Commit Check 的配置

### 使用默认设置

如果没有进行自定义设置，Commit Check 会使用默认设置。具体设置[在此](https://github.com/commit-check/commit-check/blob/main/commit_check/__init__.py)

默认设置中，提交信息遵循[约定式提交](https://www.conventionalcommits.org/zh-hans/v1.0.0/)，分支命名见[分支模型详细信息](https://support.atlassian.com/bitbucket-cloud/docs/configure-a-projects-branching-model/)


### 使用自定义配置

你可以在你的 Git 仓库下创建一个配置文件 `.commit-check.yml` 来自定义设置，例如：

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
    regex: ^(bugfix|feature|release|hotfix|task)\/.+|(master)|(main)|(HEAD)|(PR-.+)
    error: "Branches must begin with these types: bugfix/ feature/ release/ hotfix/ task/"
    suggest: run command `git checkout -b type/branch_name`
  - check: author_name
    regex: ^[A-Za-z ,.\'-]+$|.*(\[bot])
    error: The committer name seems invalid
    suggest: run command `git config user.name "Your Name"`
  - check: author_email
    regex: ^\S+@\S+\.\S+$
    error: The committer email seems invalid
    suggest: run command `git config user.email yourname@example.com`
```

你可以根据自己的需要来修改 `regex`, `error`, `suggest` 的值。

## Commit Check 使用

Commit Check 支持多种使用方式

### 以 GitHub Action 来运行

例如创建一个 GitHub Action workflow 文件 `.github/workflows/commit-check.yml`

```yaml
name: Commit Check

on:
  push:
  pull_request:
    branches: 'main'

jobs:
  commit-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: commit-check/commit-check-action@v1
        with:
          message: true
          branch: true
          author-name: true
          author-email: true
          dry-run: true
          job-summary: true
```

详细请参考 https://github.com/commit-check/commit-check-action

### 以 pre-commit hook 运行

首选需要安装了 [pre-commit](https://pre-commit.com/#install)

然后将如下设置添加到你的 `.pre-commit-config.yaml` 文件中。

```yaml
-   repo: https://github.com/commit-check/commit-check
    rev: the tag or revision
    hooks: # support hooks
    -   id: check-message
    -   id: check-branch
    -   id: check-author-name
    -   id: check-author-email
```

### 以命令行来运行

可以通过 pip 先安装

```bash
pip install commit-check
```
然后运行 `commit-check --help` 命令就可以查看如何使用了，具体可以参见[文档](https://commit-check.github.io/commit-check/cli_args.html)

### 以 Git Hooks 来运行

要配置 Git Hooks ，你需要在 Git 存储库的 `.git/hooks/` 目录中创建一个新的脚本文件。

例如 `.git/hooks/pre-push`，文件内容如下：

```bash
#!/bin/sh
commit-check --message --branch --author-name --author-email
```
并修改为可执行权限 `chmod +x .git/hooks/pre-push`，然后当你运行 `git push` 命令时，这个 push hook 会自动执行。

## Commit Check 执行失败示例

检查提交信息失败

```bash
Commit rejected by Commit-Check.

  (c).-.(c)    (c).-.(c)    (c).-.(c)    (c).-.(c)    (c).-.(c)
   / ._. \      / ._. \      / ._. \      / ._. \      / ._. \
 __\( C )/__  __\( H )/__  __\( E )/__  __\( C )/__  __\( K )/__
(_.-/'-'\-._)(_.-/'-'\-._)(_.-/'-'\-._)(_.-/'-'\-._)(_.-/'-'\-._)
   || E ||      || R ||      || R ||      || O ||      || R ||
 _.' '-' '._  _.' '-' '._  _.' '-' '._  _.' '-' '._  _.' '-' '._
(.-./`-´\.-.)(.-./`-´\.-.)(.-./`-´\.-.)(.-./`-´\.-.)(.-./`-´\.-.)
 `-´     `-´  `-´     `-´  `-´     `-´  `-´     `-´  `-´     `-´

Invalid commit message => test
It doesn't match regex: ^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test){1}(\([\w\-\.]+\))?(!)?: ([\w ])+([\s\S]*)

The commit message should be structured as follows:

<type>[optional scope]: <description>
[optional body]
[optional footer(s)]

More details please refer to https://www.conventionalcommits.org
Suggest: please check your commit message whether matches above regex
```

检查分支命名失败

```bash
Commit rejected by Commit-Check.

  (c).-.(c)    (c).-.(c)    (c).-.(c)    (c).-.(c)    (c).-.(c)
   / ._. \      / ._. \      / ._. \      / ._. \      / ._. \
 __\( C )/__  __\( H )/__  __\( E )/__  __\( C )/__  __\( K )/__
(_.-/'-'\-._)(_.-/'-'\-._)(_.-/'-'\-._)(_.-/'-'\-._)(_.-/'-'\-._)
   || E ||      || R ||      || R ||      || O ||      || R ||
 _.' '-' '._  _.' '-' '._  _.' '-' '._  _.' '-' '._  _.' '-' '._
(.-./`-´\.-.)(.-./`-´\.-.)(.-./`-´\.-.)(.-./`-´\.-.)(.-./`-´\.-.)
 `-´     `-´  `-´     `-´  `-´     `-´  `-´     `-´  `-´     `-´

Commit rejected.

Invalid branch name => test
It doesn't match regex: ^(bugfix|feature|release|hotfix|task)\/.+|(master)|(main)|(HEAD)|(PR-.+)

Branches must begin with these types: bugfix/ feature/ release/ hotfix/ task/
Suggest: run command `git checkout -b type/branch_name`
```


以上就是 Commit Check 的使用介绍了，更多新信息请参考 https://github.com/commit-check/commit-check

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
