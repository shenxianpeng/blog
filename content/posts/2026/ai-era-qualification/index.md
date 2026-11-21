---
title: 代码 11 天就能写出来，资格要攒一整个职业生涯
summary: |
  CentOS 和 Rocky Linux 的作者用 AI 11 天写出一个内核，六百多颗星，换个没人认识的人大概没这么大讨论度。AI 让写代码几乎免费，我的判断是一年左右大部分软件公司会变天，剩下值钱的是资格：别人愿不愿意把事交给你。最后说说我自己的资格，和一个没做成的项目。
tags:
  - AI
  - DevOps
  - Thoughts
  - Open Source
authors:
  - shenxianpeng
date: 2026-11-21
---

前些天我写过一篇，说 AI 时代，小人物的机会来了。

那篇说的是好消息。这篇说另一半：对传统企业里的很多人，这不是好消息；对想抓住机会的小人物，机会也不是白给的。

## 一年左右，大部分公司会变天

我的判断是：一年左右，大部分做软件的公司都会变天，可能至少三分之二的人会被裁掉。

在 AI-native 的公司里，这件事已经发生了。

先说 OpenAI。今年 9 月，The Pragmatic Engineer 写了 [OpenAI 内部的「智能体软件工厂」](https://newsletter.pragmaticengineer.com/p/openai-software-factory)（agentic software factory），整套东西围着 Codex 转。

人在开头只做一件事：说清楚要什么结果。接下来写代码、跑测试、测挂了自己修、提 PR、盯着 CI 直到变绿，都是 Codex 在干。

评审先由几个分管不同领域的 AI 来做：高风险的改动，AI 看完还必须有人再看一遍；低风险的，可以让 AI 自动批准。

上生产之前，要有人点头，然后另一个 agent 接手上线和监控。线上出了事，也是一个 agent 先去查原因、给出处理办法，但它只给办法不动手，动不动手由值班的人说了算。

OpenAI 今年 2 月还公开过[一个内部实验](https://openai.com/index/harness-engineering/)：一个小团队花了五个月，做出一个测试版产品，代码大约一百万行，没有一行是人手写的。工程师的活，变成了搭环境、讲清楚意图、给反馈。

再说 Anthropic。他们自己没用「软件工厂」这个词，但做法很像。合进代码库的代码，80% 以上是 Claude 写的。10 月他们发了[一篇工程文章](https://www.anthropic.com/engineering/redesigning-source-control)：今年 5 月，全公司每天合并大约 2,500 个代码改动，到 9 月已经超过 30,000 个。

为了接住这么多改动，他们自己做了一套版本控制系统，把主代码库从 Git 上搬了下来，还做了一个代码评审工具，能把只改注释的小改动和敏感的逻辑改动分开，好让人把精力放在最要紧的改动上。负责这套系统的工程师仍然会看每一个改动，但看的是这次改动想干什么，不再一行一行读代码。

文章里有一句话我印象很深：工程师的角色，是对 Claude 说「不」。

两家的说法不一样，结构是一样的：写代码、测试、修 bug、评审、上线，主要靠 agent；人在环里，定方向，在要紧的地方点头或者说不。这就是常说的 human in the loop。

再看裁员。美国的 Challenger 公司每个月统计裁员公告。[到今年 10 月](https://www.challengergray.com/blog/october-layoffs-at-three-year-low-seasonal-hiring-plans-up-26/)，雇主公开说「因为 AI」裁掉的岗位有 12.1 万个，占全部裁员的两成左右。科技行业前 10 个月裁了 17 万人，已经超过去年全年。

有人会说，今年美国的裁员总数比去年还少了 44%，10 月是三年来最少的一个月，哪来的变天？

我看这只是变天前的平静。AI-native 公司已经证明，一小拨人加一群智能体，就能干完原来一整个部门的活。这套做法能稳定交付，别的公司就没有理由不跟。技术已经到了，现在等的只是组织转过弯来。

## 墙要全推掉

很多传统软件公司做事是这样的：产品经理写需求，开 Grooming 会把需求拆成一个个 story，再开 Planning 会估点、排迭代，然后开发写代码，QA 测试，文档团队写文档，最后交给运维发布。每一段都有自己的人、自己的会、自己的交接。

拆 story、估点、Grooming、Planning，这一整套敏捷仪式，在我看来纯纯是在浪费时间。一个小改动，AI 十几分钟就能做完，前面却要先开两个会，讨论它值几个点、排进哪个迭代。

这套东西为什么还在？我也理解。它就像国内很多地方装的闸机，大学门口也有。一旦装上，大家每天刷卡进出，慢慢也就习惯了，没人再问它为什么还在。

可你要是想把它拆了，就得拿出很充分的理由，还得担责任：拆的责任，拆了以后万一出事的责任。留着它什么都不用解释。

当年 DevOps 喊的口号是打破开发和运维之间的墙。确实打破了一点，但远远不够，大部分墙和闸机都还在。

AI 来了以后，这些得全推掉。墙里面的活，AI 已经压到了几分钟；墙和墙之间的会和交接，还是要好几天。不拆，买再多的 AI 也快不起来。

拆完墙，还需要什么人？

我觉得最需要的，是离客户很近的人：知道用户要什么，能很快把它做出来，自己测，自己发。最好还有很好的工程功底。

东西可以让 AI 写，但人的品味得在线。Claude Code 的负责人 Boris Cherny 说，软件工程师这个头衔会慢慢被 builder 取代，我理解说的就是这种人。

我说的是墙，不是人。墙那边的人，最好自己先翻过来，往客户那边站近一点。

## 人人都能做出来以后

讲到这儿，好像只要会用 AI、离客户近就够了。

但问题在于，AI 让「做出来」这件事变得几乎免费。你能做出来，别人也能。客户面前摆着十个差不多的东西，都是 AI 一个周末搓出来的，他凭什么选你？

我的答案是信任。客户只为他信任的人付钱。

这也是前些天那篇没说完的那一半：小人物的机会是真的，但只留给有资格的小人物。

所以我认为，大部分软件以后都会免费，真正能收钱的是咨询和服务。这件事在基础软件这一层早就发生了。

Rocky Linux 免费下载，背后的公司 CIQ 卖的是技术支持、长期维护和企业订阅。冯若航的 Pigsty 是开源的，他靠咨询和服务撑起一人公司。Linux 本身就更不用说了。

代码可以白送，出了事有人负责，这个要收钱。AI 让前一样越来越便宜，后一样一点没便宜。

当然，现在还有很多收费软件活得好好的，我也不觉得它们明天就会消失。但一个东西如果 AI 几天就能做出差不多的，它的价格迟早会往零走。

## CentOS 的作者，11 天写了个内核

说到 Rocky Linux，正好讲一个上个月的新闻。

Gregory Kurtzer，CentOS 的作者。2020 年底 Red Hat 改了 CentOS 的路线，他又发起了 Rocky Linux。

10 月底，他发了一个新项目，叫 [Ginux](https://github.com/gmkurtzer/ginux)。他用 OpenAI 的 Codex 写代码，自己定架构和验收标准，11 天做出了一个全新的、用 Rust 写的内核，大约 13.9 万行代码，能在虚拟机里把 Rocky Linux 10 启动起来。现在 GitHub 仓库有六百多颗星。

如果换一个没人认识的人来做同样的事，讨论度大概率没有这么大。

差在哪了？差在人家二十多年前就在做 CentOS，后来又做了 Rocky Linux，这些东西被很多公司放在生产环境里用了这么多年。

这就是信任，我管它叫资格。

他自己也说，长期维护、社区这些，才是真正的护城河。一个用 AI 11 天写出内核的人，自己说护城河不在代码上。代码 11 天就能写出来，资格却要攒一整个职业生涯。

## 资格到底是什么

我们大部分人的职业生涯，都是在跟同事、合作伙伴、领导打交道。资格说的就是：跟你打交道的这些人，觉得你够不够格，这件事该不该由你来做。

在我看来，资格就是你在一件事上长期、公开地负过责。或者不落到哪件具体的事上：出了事、有了问题，大家知道找你绝对靠谱，你能把别人的问题解决掉。

它看两样东西。

第一样，是你平时怎么做事。别人找你，你多久回，水平怎么样，认不认真，给的答案对不对。有的人在公司里成天混日子，别人心里都有数，真遇到事，没人会信任他。信任是一点一点攒出来的，你是个什么样的人，同事们看得清清楚楚。

第二样，跟 AI 直接有关：你能不能看懂 AI 写的东西。同样在用 AI，技术底子强的人，知道 AI 写的代码在干什么，方向对不对，架构合不合理，一眼能看出来。这要很多年的积累。看不懂的人，没法为结果负责。别人觉得你看不看得懂，也是你资格的一部分。

## 我的资格

那我自己的资格在哪？

这十年，我一直在 build、release、DevOps 这条线上。这条路我趟得很熟，也能挑大梁：有相关的活交给我，我能稳稳地做好。而且我做事不是做成了就完，一直在琢磨最佳实践是什么，怎么把它做到最好。

除了工作，我业余时间也做开源，攒这方面的资格。这些年我没有偏离过这条主线，做的开源都在它上面：

- [cpp-linter](https://github.com/cpp-linter)：C/C++ 代码检查。GitHub Action 被 1,000 多个仓库用着，其中有 AWS 的 s2n-tls；配套的 clang-tools 每月在 PyPI 上下载一万七千多次。
- [commit-check](https://github.com/commit-check/commit-check)：检查提交和分支规范，每月下载七万多次，JUnit 和 FreeBSD 的项目都在用。
- [Conventional Branch](https://github.com/conventional-branch/conventional-branch)：Git 分支命名规范，GitHub 上 149 颗星。
- Jenkins 这边：[explain-error](https://github.com/jenkinsci/explain-error-plugin) 插件，用 AI 解释构建为什么失败，现在有 168 个 Jenkins 装着；还有 [jenkinsfilelint](https://github.com/jenkinsci/jenkinsfilelint)，最近我又有了一些新想法，后面单独写一篇。

星星不算多，这几个加起来六百多颗，跟 Ginux 一个多月拿到的差不多。但它们每天都在别人的 CI 里跑着。对我来说，这比星星更像资格。

我也审一下自己，有些事我就没有资格做成。

比如之前做的 [Open Delivery Spec](/zh-cn/posts/2026/open-delivery-spec-update/)。我当时想给 AI 时代的软件交付做一个卡点，也就是验证点：AI 交出来的东西，过了这一关才算能交付。我想把它做成像 Conventional Commits、Conventional Branch 那样大家都在用的规范。

做了一阵发现很难。一是竞争太激烈，做这件事的人太多了。二是卡在一个两难里：光靠写死的规则去检查，不借助 agent 的能力，很多事判断不了；可要是借助 agent 的能力，这个卡点早晚会被 AI 自己替代。标准这种东西，已经不像以前那么好做了。再加上背书、资格这几样我也没有，所以后来我果断把它归档了。

## 你的资格是什么

最后把这个问题留给你：AI 时代，你的资格是什么？

可以拿这几个问题问问自己：

1. 出了问题，别人第一个想到的是不是你？
2. 跟你打交道的人，觉得你够不够格？
3. AI 写出来的东西，你看得懂吗？

## 参考

- [The Pragmatic Engineer，《Inside OpenAI's agentic software factory》（2026-09）](https://newsletter.pragmaticengineer.com/p/openai-software-factory)
- [OpenAI，《Harness engineering: leveraging Codex in an agent-first world》（2026-02-11）](https://openai.com/index/harness-engineering/)
- [Anthropic Institute，《When AI builds itself》（80% 以上代码由 Claude 编写）](https://www.anthropic.com/institute/recursive-self-improvement)
- [Anthropic Engineering，《Redesigning source control at Anthropic》（2026-10-13，每天合并改动 2,500 → 30,000+，Antique 评审工具，「工程师的角色是对 Claude 说不」）](https://www.anthropic.com/engineering/redesigning-source-control)
- [Lenny's Podcast，Boris Cherny（产品、设计都写代码；builder 取代软件工程师头衔）](https://www.lennysnewsletter.com/p/188147394)
- [Challenger, Gray & Christmas，2026 年 10 月裁员报告（2026-11-05）](https://www.challengergray.com/blog/october-layoffs-at-three-year-low-seasonal-hiring-plans-up-26/)
- [CIQ 的 Rocky Linux 商业订阅（The New Stack）](https://thenewstack.io/ciq-launches-rlc-pro-for-enterprise-linux-for-the-ai-era/)
- [Pigsty FAQ（一人公司、咨询服务）](https://pigsty.io/docs/about/faq/)
- [It's FOSS，《Rocky Linux Creator Built a New "Not Linux" Kernel in 11 Days Using AI》（2026-10-27）](https://itsfoss.com/news/ginux/)
- [LinuxToday，《CentOS Founder Builds Linux-Compatible Rust Kernel with AI in Just 11 Days》（2026-11-09）](https://www.linuxtoday.com/blog/centos-founder-builds-linux-compatible-rust-kernel-with-ai-in-just-11-days/)
- [Ginux 仓库](https://github.com/gmkurtzer/ginux)
- 开源数据（2026-11-21 查）：GitHub 星数和 dependents 页（cpp-linter-action 1,072 个仓库、commit-check-action 195 个仓库），pypistats.org 近 30 天下载（commit-check 74,677、clang-tools 17,694、cpp-linter 12,404），plugins.jenkins.io（explain-error 168 个安装）

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
