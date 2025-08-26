---
title: Programmer's Self-Cultivation—Git Commit Message and Branch Creation Conventions (Tools)
summary: This article introduces how to use the Commit Check tool to verify whether Git commit messages, branch names, committer usernames, and committer email addresses conform to specifications.
tags:
  - Git
author: shenxianpeng
date: 2023-05-09
---

Git commit message and Git branch naming conventions are a very important part of team collaboration. They can make the codebase more standardized, easier to maintain, and easier to understand.

We need to use tools to help implement Git commit message and branch creation conventions. This article will introduce how to use the [Commit Check](https://github.com/commit-check) tool to verify commit messages, branch names, committer usernames, and committer email addresses to ensure they conform to specifications.

For more information on Git commit messages and branch creation conventions, please refer to my previous article, [“Programmer's Self-Cultivation—Git Commit Message and Branch Creation Conventions”](https://shenxianpeng.github.io/2020/09/commit-messages-specification/).  I will not reiterate them here.


## Commit Check Introduction

Commit Check is a tool that can check Git commit messages, branch names, committer usernames, committer emails, and more. It is an open-source alternative to [Yet Another Commit Checker](https://docs.mohami.io/yet-another-commit-checker-yacc/).

## Commit Check Configuration

### Using Default Settings

Without custom settings, Commit Check will use the default settings.  Specific settings are available [here](https://github.com/commit-check/blob/main/commit_check/__init__.py).

By default, commit messages follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), and branch naming follows the [branch model details](https://support.atlassian.com/bitbucket-cloud/docs/configure-a-projects-branching-model/).


### Using Custom Configuration

You can create a configuration file `.commit-check.yml` in your Git repository to customize the settings. For example:

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

You can modify the values of `regex`, `error`, and `suggest` according to your needs.

## Commit Check Usage

Commit Check supports multiple usage methods.

### Running with GitHub Actions

For example, create a GitHub Actions workflow file `.github/workflows/commit-check.yml`:

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
      - uses: commit-check-action@v1
        with:
          message: true
          branch: true
          author-name: true
          author-email: true
          dry-run: true
          job-summary: true
```

For details, please refer to https://github.com/commit-check-action

### Running with pre-commit hook

First, you need to install [pre-commit](https://pre-commit.com/#install).

Then add the following settings to your `.pre-commit-config.yaml` file.

```yaml
-   repo: https://github.com/commit-check
    rev: the tag or revision
    hooks: # support hooks
    -   id: check-message
    -   id: check-branch
    -   id: check-author-name
    -   id: check-author-email
```

### Running from the Command Line

Install via pip:

```bash
pip install commit-check
```
Then run the `commit-check --help` command to see how to use it.  Details can be found in the [documentation](https://commit-check.github.io/cli_args.html).

### Running with Git Hooks

To configure Git Hooks, you need to create a new script file in the `.git/hooks/` directory of your Git repository.

For example, `.git/hooks/pre-push`, the file contents are as follows:

```bash
#!/bin/sh
commit-check --message --branch --author-name --author-email
```
Make it executable with `chmod +x .git/hooks/pre-push`. Then, when you run the `git push` command, this push hook will execute automatically.

## Commit Check Failure Example

Commit message check failure:

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

Branch name check failure:

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


This concludes the introduction to Commit Check. For more information, please refer to https://github.com/commit-check

---

Please indicate the author and source when reprinting this article.  Do not use it for any commercial purposes. Welcome to follow the WeChat public account "DevOps攻城狮".