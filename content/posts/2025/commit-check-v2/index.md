---
title: Commit Check v2.0.0 重磅发布：支持 TOML 配置、简化 CLI & Hooks、重构验证引擎！
summary: 经过了断断续续一个月的开发和测试，我终于完成了这次重大更新。这也是 Commit Check 迎来了自诞生以来最大的一次更新。
tags:
  - Commit-Check
  - DevOps
author: shenxianpeng
date: 2025-10-13
---

每次 Code Review，总有同事的 commit message 五花八门？

“fix”、“temp change”、“update”… 看得人直摇头。

开发者都知道，一个干净清晰的提交历史有多重要。

它不仅记录了代码的变化，更记录了团队的“思考过程”。

这正是 [Commit Check](https://github.com/commit-check) 的初衷 —— 帮助你和团队保持提交信息、分支命名的规范性与一致性。

它的目标很简单：**让每一次代码提交都遵循一致的规范。**

从 2022 年开始，我就一直在维护这个开源项目 —— Commit Check。

三年来，它从一个小工具成长为一个在社区中有一定影响力的 DevOps 工具，很多团队把它纳入到了 CI/CD 流程中。

随着我对这类工具的理解加深，我意识到 Commit Check 还可以做得更好。

所以经过断断续续一个月的开发与测试，我终于完成了这次重大更新。

这也是 Commit Check 自诞生以来最大的一次版本升级。 🎉

## Commit Check v2.0.0 有哪些新变化？

这次更新主要包括三大亮点：

* TOML 配置文件支持
* 简化 CLI & Hooks
* 重构验证引擎

一句话总结：**更简洁、更快、更易用。**

## 为什么要改用 TOML？

过去 Commit Check 使用 `.commit-check.yml` 作为配置文件。

它的用户高度可定制化也带来了维护上的复杂性，以及不够直观的配置体验，不够现代化，也容易被缩进、格式等搞错。

于是决定——**全面切换到 TOML**。

TOML 的语法更直观，更适合这种**声明式配置**。

我们先来看一下配置文件的前后对比：

### 旧的 YAML 配置文件

```yaml
# .commit-check.yml
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
```

### 新的 TOML 配置文件

```toml
# commit-check.toml or cchk.toml
[commit]
conventional_commits = true
allow_commit_types = ["feat", "fix", "docs", "style", "refactor", "test", "chore", "ci"]

[branch]
conventional_branch = true
allow_branch_types = ["feature", "bugfix", "hotfix", "release", "chore", "feat", "fix"]
```

是不是瞬间清爽多了？

没有嵌套、没有缩进坑，一眼就能看懂。

TOML 的结构天然适合这种“规则声明式”的配置方式，可以直接读懂配置内容。

## 其他更新与改进

其他的更新基本都是围绕着配置文件的迁移、简化 CLI 和 Hooks 以及重构验证引擎进行的。

除了代码更新，这次我还重写了整个 [Commit Check 文档](https://commit-check.github.io/commit-check/) 体系，以及[官网](https://commit-check.github.io)。

现在你可以在官网直接找到完整的示例配置和常见问题：

[What's New in v2.0.0](https://commit-check.github.io/commit-check/what-is-new.html)

## 结语

如果你还没有用过 Commit Check，
强烈建议你现在就试试，也欢迎转发给身边的开发者朋友。

它能帮你和团队轻松采用 [Conventional Commits](https://www.conventionalcommits.org) 和 [Conventional Branch](https://conventional-branch.github.io) 并通过自动化检查，让代码提交更规范、整洁、可追溯。

📍 项目地址：**github.com/commit-check/commit-check**

📄 更多详情：https://commit-check.github.io/commit-check/

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
