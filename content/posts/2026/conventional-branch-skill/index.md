---
title: Conventional Branch 官方 Skill 来了，安装只需一行命令
summary: |
  有用户提 Issue 希望 Conventional Branch 能提供官方 Agent Skill，我觉得这个需求很合理。当天就把它做了出来，现在通过 npx skills add 一行命令就能下载使用。恰逢本周项目也突破了 100 个 Star，一并聊聊。
tags:
  - Conventional Branch
  - Skills
  - Coding Agent
  - Open Source
authors:
  - shenxianpeng
date: 2026-05-17
---

大家好，我是沈工。

Conventional Branch 现在有官方 Skill 了。

事情起源于 [@ruzickap](https://github.com/ruzickap) 在 GitHub 上提的一个 [Issue](https://github.com/conventional-branch/conventional-branch/issues/119)：

> I'm looking for an official agent skill that will help my agent properly create the Conventional Branch when needed.

他的需求是：希望有一个官方的 Agent Skill，让 AI coding agent 在创建分支时，能够按照 Conventional Branch 的规则来命名。

这个想法我之前其实也考虑过。

早在 Skills 这个概念刚开始出现的时候，就想过我维护的这么多项目里，哪些项目是应该提供一份给 agent 使用的规则说明的。

当时没去做，后来也就忘了这个念头。

这次有人把需求提出来，我觉得真的太好了，还不算晚。

当天就把这个 Skill 写出来并提交了（PR [#120](https://github.com/conventional-branch/conventional-branch/pull/120)）。

## 一行命令安装

现在只需要执行一条命令：

```bash
npx skills add conventional-branch/conventional-branch --skill conventional-branch
```

你可以选择安装到哪个 agent 下面，是作为项目范围内的还是全局范围内的，在执行命令过程中就能选择。

安装完成后，当 coding agent 需要创建分支时，就可以参考这套规则：应该使用什么前缀，description 应该怎么写，哪些命名是合法的，哪些命名可能会被 commit-check 拦截。

对用户来说，最大的好处是：不用每次都重复提醒 agent。

以前你可能需要反复说：

> 请使用 Conventional Branch 规范。
> 分支名要用 kebab-case。
> 不要用大写字母。
> 不要用下划线。
> feature 分支要用 feature/xxx。

现在这些规则可以直接放进 Skill 里，让 agent 在合适的时候自己读取。

## 这个 Skill 里包含了什么

这份 Skill 是按照 [Conventional Branch 规范](https://conventional-branch.github.io) 写的，主要覆盖下面几类规则。

第一，分支命名格式。

Conventional Branch 使用的是：

```
type/description
```

目前支持的 type 包括：

* feature
* bugfix
* hotfix
* release
* chore

description 使用小写字母和 kebab-case，例如：

```
feature/add-login-page
bugfix/fix-user-cache
chore/update-ci-config
```

第二，常见错误检查。

Skill 里明确说明了哪些分支名是不符合规范的，例如：

```
feature/AddLoginPage
feature/add_login_page
feature/add--login-page
bugfix/fix user cache
```

这些问题在人工创建分支时很常见，在 agent 创建分支时也一样容易出现。

有了 Skill 之后，agent 在生成分支名之前，就有机会先参考这些规则，避免生成明显不符合规范的名字。

第三，基准分支检测。

不同仓库的 trunk 分支可能不一样。

有的项目用 main，有的还在用 master，也有一些团队使用 develop。

所以 Skill 里也写明了创建新分支前应该优先检测当前仓库已有的基准分支，而不是默认假设所有项目都使用 main。

第四，和 Conventional Commits 的关系。

Conventional Branch 和 Conventional Commits 本身是可以配合使用的。
比如：

```
feature/add-login-page  -> feat: add login page
bugfix/fix-user-cache   -> fix: fix user cache
chore/update-ci-config  -> chore: update ci config
```

分支名负责表达“这项工作属于什么类型”，commit message 负责表达“这次提交做了什么”。

两者放在一起，整个 Git workflow 会更容易被人和工具理解。

第五，和 commit-check 配合。

Skill 解决的是 agent 创建分支时的上下文问题。
但最终要不要强制执行规范，还是建议交给工具来兜底。

这也是我在 Skill 里提到 [commit-check](https://github.com/commit-check/commit-check) 的原因。

如果 agent 偶尔生成了不符合规范的分支名，commit-check 仍然可以在本地、CI 或团队流程中把不符合规范的分支拦下来。

换句话说：Skill 负责让 agent 尽量做对，commit-check 负责在流程上兜底。

它们配合起来，才比较完整。

## 为什么我觉得这件事值得做

AI coding agent 已经越来越常见了。越来越少的人会去你的 Contributing guide 里看那些写给人类贡献者的说明了。

即使你在文档里写明要按照 Conventional Branch 规范创建分支，AI 还是会创建出来下面各种形式的分支：

```
My_New_Feature
feature/newFeature
fix-login-bug
```

这让 CI 规则也不好写，release note、changelog、issue 关联等自动化流程也会变得更难维护。

以前规范主要写在文档里，靠人去读、去记、去执行。

现在有了 agent，规范也应该可以变成 agent 能读取的上下文。

这就是 Skill 的价值。它不是替代文档，也不是替代校验工具，而是把“规范”前移到了 agent 工作的入口处。

当 agent 开始做事之前，它就能先知道：这个仓库希望分支怎么命名。

## 怎么参与

如果你还不了解 Conventional Branch，可以从这里开始：

- [规范文档](https://conventional-branch.github.io)
- [GitHub 仓库](https://github.com/conventional-branch/conventional-branch)
- [commit-check 验证工具](https://github.com/commit-check/commit-check)

如果你已经安装并使用了这个 Skill，也欢迎反馈真实使用体验。

欢迎在 [Issue #119](https://github.com/conventional-branch/conventional-branch/issues/119) 下面留言，或者直接开新 Issue。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
