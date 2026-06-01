---
title: Conventional Branch 有了自己的域名：conventionalbranch.org
summary: |
  Conventional Branch 项目网站正式从 conventional-branch.github.io 迁移到 conventionalbranch.org。从去年用户提议到今年最终落地，聊聊域名迁移背后那些犹豫、踩坑和思考。
tags:
  - Conventional Branch
  - Open Source
authors:
  - shenxianpeng
date: 2026-05-31
---

大家好，我是沈工。

Conventional Branch 终于有了自己的独立域名。

从今天开始，你可以通过 **[conventionalbranch.org](https://conventionalbranch.org)** 访问 Conventional Branch 的官方网站，项目文档（规范说明、安装指南、FAQ 等）都已迁移到新域名。

旧域名 `conventional-branch.github.io` 仍然会保留跳转，但正式地址已经切换到 conventionalbranch.org。

## 为什么要这么做

这件事的起点，其实是去年一位用户提出的建议。

当时他在 GitHub issue 上留言说，Conventional Branch 作为一个有明确规范的独立项目，用 GitHub Pages 的二级域名感觉不太正式，建议我考虑注册一个独立的域名。

说实话，我当时挺犹豫的。

Conventional Branch 是一个纯开源项目，没有任何商业收入。注册域名、每年续费，这些费用都得自己承担。我不是不想做，只是觉得“有没有必要”。

但用户的这个建议我一直记在心里。后来想了想，还是先把域名注册了再说。

## 一个不太满意的开始

随后我其实我买下了一个域名：**conventionalbranches.org**。

为什么是 branches 而不是 branch？

买的时候比较匆忙，当时只是想着“项目叫 Conventional Branch，分支是 branches，用复数好像也合理”。

但买完之后越想越觉得不对——项目名是 **Conventional Branch**，单数。`conventionalbranches.org` 读起来不顺，跟项目名也不完全匹配。

所以这个域名买完之后就一直放在那里，没有启用。

## 今年的转折

今年情况发生了一些变化。

首先是 Conventional Branch 的用户量和使用量都在增长。

项目网站每月的访问量已经相当可观，GitHub 仓库的 Star 也在稳步增长。越来越多的团队在日常开发中使用 Conventional Branch 规范来管理分支命名。

其次，今年我给项目加了不少新东西。

比如上个月刚推出的[官方 Agent Skill](https://github.com/conventional-branch/conventional-branch/blob/main/skills/conventional-branch/SKILL.md)，让 AI coding agent 也能按照 Conventional Branch 的规则来创建分支。通过 `npx skills add conventional-branch/conventional-branch --skill conventional-branch` 就能安装这个 Skill，让 AI 在创建分支时自动遵循规范。 

另外我也将这个 Skill 提交到 GitHub 官方的 [awesome-copilot](https://github.com/github/awesome-copilot) 项目里了。

通过 `gh skills install github/awesome-copilot conventional-branch` 可以直接安装这个 Skill，让 Copilot 在创建分支时自动遵循 Conventional Branch 的规范。

另外，Conventional Branch 的生态也在扩展。除了核心规范本身，配套的 [commit-check](https://github.com/commit-check/commit-check) 工具也在持续迭代，帮助开发者更方便地检查 Git Metadata 是否符合规范。

综合这些变化，我觉得是时候给 Conventional Branch 一个正式的域名了。用 GitHub Pages 的域名其实功能上没什么问题，但作为一个有完整生态、有明确规范的开源项目，有一个独立的域名会让项目显得更加正式和可靠。

所以这一次，我买了域名：**conventionalbranch.org**。

## 迁移做了哪些事

域名迁移本身不算复杂，主要做了几件事：

* **DNS 和托管配置。** 将 conventionalbranch.org 指向 GitHub Pages，同时启用了 HTTPS。
* **旧域名跳转。** conventional-branch.github.io 保留了跳转，访问旧域名的用户会自动重定向到新域名。已有的书签、文档链接、README 里的引用都不会断。
* **网站认证（Verify）。** 完成了 GitHub 的域名验证，确保新域名在 GitHub Pages 上被正确识别和使用。
* **文档更新。** 项目仓库里的 README、文档内链接、Skill 配置等，凡是引用了旧域名的地方，都更新成了新域名。

整个过程下来，对用户没有感知影响，访问到的内容是一样的，只是地址栏里的 URL 变了。

## 写在最后

从去年用户提建议，到买错域名，到上周末终于买了正确的域名并完成迁移，这件事拖了挺久。

但对于一个开源项目来说，有些事情急不得。

用户量不够的时候买域名，可能只是自我感动；当用户量、生态、项目成熟度都到了一个合适的节点，再做这件事就顺理成章了。

感谢那位去年提出建议的用户，也感谢所有使用 Conventional Branch 的开发者。

如果你愿意支持 Conventional Branch，可以通过以下方式：

- 在 GitHub 上 Follow / Star 项目：[github.com/conventional-branch](https://github.com/conventional-branch)
- 在社交媒体上分享和推荐 Conventional Branch
- 参与项目的讨论和贡献，提交 issue 或 pull request
- 通过打赏或 [GitHub Sponsors](https://github.com/sponsors/shenxianpeng) 来支持我继续维护和发展 Conventional Branch 及其以外的开源项目

如果你想了解更多，可以访问：

- 官网：[conventionalbranch.org](https://conventionalbranch.org)
- GitHub：[github.com/conventional-branch/conventional-branch](https://github.com/conventional-branch/conventional-branch)
- 配套工具：[commit-check/scommit-check](https://github.com/commit-check/commit-check)

感谢关注，我们下期见～

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
