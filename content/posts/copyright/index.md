---
title: CPython 停止更新 Copyright 了，为什么？
summary: |
  CPython 停止更新 Copyright 的原因和过程。了解 Python 项目法律团队的建议，以及如何处理开源项目中的版权声明。
tags:
  - Python
  - Copyright
translate: false
author: shenxianpeng
date: 2025-01-20
---

最近逛 CPython 的仓库发现了这个 Issue [gh-126133](https://github.com/python/cpython/issues/126133):

Hugo van Kemenade 他作为 Python 3.14 & 3.15 发布经理提出是否可以停止更新 Copyright。

在工作中，我其中的职责之一也是发布，因此我这个想法的提出也非常感兴趣，跟 CPython 项目一样，我们的项目在每年的年初都要更新 Copyright。

下面我们就一起来看看 Hugo 提出的理由以及最终这个想法被 Python 项目法律团队采纳并最终合并到 CPython 的主分支的过程。



## Hugo 提出问题的内容是这样的

每年一月，我们会在代码库中更新 PSF 的版权年份：

```bash
Copyright © 2001-2024 Python Software Foundation. All rights reserved.
```

2025年即将到来。

我们能否获得 PSF 的许可，采用一种无需每年更新的版权声明？

我建议使用如下之一：

```bash
Copyright © Python Software Foundation. All rights reserved.
Copyright © 2001 Python Software Foundation. All rights reserved.
Copyright © 2001-present Python Software Foundation. All rights reserved.
```

然后他列出了许多以前很多关于更新 Copyright 的 PR 的例子。

其中很多还有重复的，浪费了开发者的时间。并表示不仅这些工作枯燥无趣，而且可能完全没有必要。

许多大型项目已经停止更新版权年份，比如：

```bash
Copyright (c) 2009 The Go Authors. All rights reserved.
Copyright (c) 2015 - present Microsoft Corporation
Copyright 2013 Netflix, Inc.
Copyright (c) Meta Platforms, Inc. and affiliates.
Copyright (c) Microsoft Corporation. All rights reserved.
Copyright (c) .NET Foundation and Contributors
```

这些要么只有首年，要么完全省略年份，要么以“present”结尾。

我们可以效仿类似的做法吗？

---

这里面有其他人发表的观点。

Gregory P. Smith（Python 指导委员会成员）给出了很好的建议：

他说：我不会从任何地方删除整个版权声明。Hugo 应该向 PSF（作为版权持有者）寻求建议。我们的目标是简化我们的生活，制定一项可参考的政策，减少劳累。我们应该将这些建议编入开发指南，并简单地回复任何试图修改版权声明的人，并提供该文档的链接。

## 最终 Hugo 给 PFS 法律发了邮件，并得到如下回复

首先要理解的是，版权声明是可选的/信息性的。曾经有一段时间，版权所有者必须包含一份声明，以保护他们的版权；根据国际条约，这一要求已被废除。因此，版权声明的形式不会影响版权所有者的权利。

然而，版权声明仍然可以发挥有用的信息作用。根据美国版权局的说法，有效的版权声明的要素包括：

版权符号 ©；“copyright”一词；或缩写 “copr.”；
作品首次出版的年份；和
版权所有者的姓名。

示例：© 2024 John Doe

对于只出版过一次的作品，首次出版的年份很简单。另一方面，开源项目中的文件本质上是修订或衍生作品的累积，每个作品都有不同的首次出版年份。这就是为什么您会在相应的版权声明中看到多个日期或日期范围。例如，如果某个文件是在 2015 年创建的，并在 2017 年、2018 年、2019 年和 2022 年进行了修订，则您可以采用以下方式之一呈现版权声明：

© 2015、2017-2019、2022 John Doe
© 2015、2017、2018、2019、2022 John Doe
在这种情况下，使用“2015-2022”作为日期范围可能相当普遍，尽管这提供的有关各个修订的首次发布日期的信息较少，并且可能错误地暗示该文件在该范围内的每一年都进行了修订。

无论相应文件是否最近更新过，在每个版权声明的日期范围末尾更新声明以添加当前年份都没有特别的意义。但它也不会影响任何人的权利，也不会使用“-present”来代替。

所以我认为你提出的包含年份的两种格式都可以。我不建议完全省略首次出版的年份，因为它是有效版权声明的要素之一。

我还要指出的是，“Python 软件基金会”可能不是 PSF 项目作者的准确陈述，因为 PSF 不需要（据我所知）版权转让。话虽如此，为文件的所有作者包含声明也是不切实际且容易出错的。一些常见的替代方案是 “FOO 项目贡献者”或“贡献者中列出的作者”。这些都不是理想的，因为它们要么实际上没有命名作者，要么随着作者的贡献随着时间的推移而消失，它们可能会变得不准确。

简而言之，没有理想的解决方案，但幸运的是声明并不那么重要。选择一些合理的内容并尽力坚持下去。

以上就是 PFS 法律的回复。

---

期间还有人提议 Hugo 要争得 PFS 董事会的同意。

但有人这样回复这个提议：PSF 法律列表由 PSF 员工（包括我自己）监控，是解决此类问题的正确途径。需要董事会全员参与的主题会被提交，不需要董事会全员参与的主题会在那里决定，根据主题的不同，是否需要法律顾问。在这个特定情况下，我们确实请来了律师，以确保 PSF 履行我们作为版权持有人的法律义务。

此回答并获得了 Hugo 及其他人的点赞👍和❤️。

最终 Hugo 的提议 **“只包含首次出版的年份，删除结束年份”** 修改被合并到了 CPython 的主分支了。详见：https://github.com/python/cpython/pull/126236

## 总结

从这个问题我们可以学到，关于 Copyright 中的年份，我们可以仿照 Python，谷歌，微软和 Netflix，只包含首次出版的年份即可。

我不是律师，所以不要把这当作我的法律建议。

我只想说，如果这对 Python，谷歌、微软和 Netflix 的律师来说是可以的，那么对我来说也是可以的。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
