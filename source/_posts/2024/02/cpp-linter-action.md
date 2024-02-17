---
title: cpp-linter-action 从 v2.9.0 版本开始支持 Pull Request Review 功能了 👏
tags:
  - clang-format
  - clang-tidy
  - clang
  - cpp-linter
categories:
  - cpp-linter
author: shenxianpeng
date: 2024-02-17 11:34:18
---

我作为 [cpp-linter](https://github.com/cpp-linter) 的创建者和贡献者，很高兴的宣布 ———— cpp-linter-action 从 v2.9.0 版本开始支持 Pull Request Review 功能了 👏

这是 cpp-linter-action 的[release notes](https://github.com/cpp-linter/cpp-linter-action/releases)

![release notes](cpp-linter-action/cpp-linter-action@2.9.0.png)

其中 **`Bump cpp-linter from 1.6.5 to 1.7.1 by @dependabot in #191`** 是其最重要的变化。

## 什么是 cpp-linter-action

如果你还不了解 [cpp-linter-action](https://github.com/cpp-linter/cpp-linter-action) 可以查看我[之前的文章](https://shenxianpeng.github.io/2022/08/cpp-linter/)。

简单来说，cpp-linter-action 是 cpp-linter 组织下的一个 [GitHub Action](https://docs.github.com/en/actions/quickstart)，针对 C/C++ 代码做代码格式、诊断和修复典型的编程错误。

目前 cpp-linter-action 大概被上千项目所使用，这里包括微软、Linux基金会、CachyOS、nextcloud、Jupyter 等知名组织或项目。

不谦虚地说，目前 cpp-linter-action 是 GitHub 上 C/C++ 项目的最佳 Linter 选择，没有之一。

## 关于 Pull Request Review 功能

此次新增的 Pull Request Review 功能可以直接在 cpp-linter-action 检查完成后给出 review 建议，开发者无需本地修改检查到的错误，并提交到远程。
而是可以直接点击 GitHub 上的 Commit suggestions 按钮，就可以把建议修改直接应用到当前的 pull request 中，省去了人为的修改和推送。

![format-review](cpp-linter-action/format-review.png)

![format-suggestion](cpp-linter-action/format-suggestion.png)

![tidy-review](cpp-linter-action/tidy-review.png)

**除了 Pull Request Review 功能之外，cpp-linter-action 目前还支持另外三个选项：Annotations，Thread Comment 和 Step Summary。**

### GitHub Annotations

即在指定的需要修改的代码行处提示。

![clang-format annotations](cpp-linter-action/clang-format-annotations.png)
![clang-tidy annotations](cpp-linter-action/clang-tidy-annotations.png)

### Thread Comment

即在 Pull Request 上以评论形式添加检查结果。

![comment](cpp-linter-action/comment.png)

### Step Summary

即在 GitHub Action 界面添加检查结果。

![step summary](cpp-linter-action/step-summary.png)

### Pull Request Review

## 关于本次发布背后的故事

我是终于在大年初八的晚上孩子睡着了之后有点时间坐下来写一篇文章了，来记录一下本次发布背后的故事。

本次发布我要特别感谢与我素未蒙面，但在一起“公事”三年的 cpp-linter 联合创建者 [@2bndy5](https://github.com/2bndy5)。我们的交流仅限于 GitHub 上的 Issues 和 PRs，不公开信息会通过 Gmail 来传达。

正如 @2bndy5 的个人介绍那样：热衷于编程，喜欢 DIY 电子产品，坚持写易懂的文档。他确实也是这么做的，为开源项目贡献了很多力量。

但不久前我收到了他的邮件说：因家中变故，他要休息一段时间，他没有动力坐下来写代码了，并告诉我 Pull Request Review 所有改动似乎都通过测试了，
如果需要我可以主导，他来提供支持。我为发生在他身上的事情表示最深切的同情和慰问🙏

我本想借此机会搞清楚这部分功能，但因为迟迟没有一个充足的时间，想等 2024 年的春节放假找机会弄清楚并发布。

可是还没有到春节放假，就在腊月二十七孩子生病了，并告知需要住院治疗，因为我们发现的早，病症不严重，孩子在除夕当天恢复的很好，期待着再观察两天就可以出院了。
哎，可是意外发生了，孩子不小心胳膊被烫伤了，苦作为父母非常痛心，这是我永远都不想回忆的至暗时刻。

总是就是雪上加霜。就这样我们从年起的腊月二十七一直住院到正月初六，住了 10 天医院。

然后在我缺席的这 10 天里，@2bndy5 完成了对 Pull Request Review 功能的测试、文档修改和发布，我不敢过多询问他的情况，当我相信把时间花在感兴趣的编程上是会让人短暂的逃离现实。

我也一样，回到家中，等孩子休息了在我还有体力的情况下，来审查别人对项目的贡献代码，这次是一个 Title 是来自于德国多特蒙德大学的天体物理学家的贡献者，有点惊讶到我了。

这也确实很有趣，开源能让你有机会和任何高手近距离的过招。如果你给 Linux 内核提交代码，那你极有可能得到 Linus 的指导 ：）

最后，欢迎使用 cpp-linter 组织下的任何项目并提出您的宝贵意见、建议、或贡献代码。


                                                                                                                    ————— 2024 年 2 月 17 日 23:34

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」


