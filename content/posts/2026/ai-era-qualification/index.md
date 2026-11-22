---
title: 一边每天合并 3 万个改动，一边回到古法编程
summary: |
  V2EX 上一家公司因为 AI 写的代码出了线上故障，全面禁了 AI Coding；Anthropic 每天合并的代码改动却从 2,500 涨到了 3 万多。差别不在 AI，在关卡。我的判断是，用不到一年，大部分做软件的公司都会变天，剩下的是能把关、有资格的人。
tags:
  - AI
  - DevOps
  - Thoughts
authors:
  - shenxianpeng
date: 2026-11-22
---

这周 V2EX 上有个帖子，标题叫[《我司全面禁止 AI Coding，一夜之间回到古法编程时代》](https://www.v2ex.com/t/1258200)。

楼主说，同事用 AI 写的代码，评审没看出问题，上线以后出了故障，用户投诉一大片。

老板一气之下，禁止直接用 AI 生成代码，只许拿来分析、出方案。原话是：宁愿慢，也不要出问题。

两百多条回复，吵得很热闹。

我看完想到两点。

一是可能模型不够聪明，写出来的东西有问题，而且 review 的时候人也没发现。

二是反过来想，就算退回到手写，也一样可能出事。review 没发现问题，换谁写代码都会漏。

帖子底下有一条点赞很高的回复，说得更直白：AI 出代码太快了，原来的评审和发布流程根本跟不上。

我觉得这才是那家公司真正的问题。AI 写得多没有错，错在能把关的地方太少。

同样的问题，AI native 的公司也遇到过，而且规模大得多。

Anthropic 截至今年 5 月，合进主代码库的代码 [80% 以上是 Claude 写的](https://www.anthropic.com/institute/recursive-self-improvement)。全公司每天合并的代码改动，5 月是 2,500 个左右，到 9 月[超过了 3 万个](https://www.anthropic.com/engineering/redesigning-source-control)。他们自己也承认，人工评审成了新的瓶颈。

所以每个 PR 都先过一遍 Claude 的自动评审，他们回头算过，以前 claude.ai 出过的事故，这一关大约能拦下三分之一的 bug。

他们在一篇工程文章里写，工程师的角色，是对 Claude 说「不」。

OpenAI 那边也差不多。内部有一套[「智能体软件工厂」](https://newsletter.pragmaticengineer.com/p/openai-software-factory)，写代码、写测试、修 CI、等评审，都是 Codex 在干。高风险的改动，AI 看完还得有人再看一遍；上生产之前，要有人拍板。

前两天我在 X 上看到一句话：从 Claude Code 直接到生产。说实话，我现在业余做的一些不那么要紧的东西，比如个人网站、项目网站，基本都是这么干的。要紧的东西，我不会。

一个每天合并 3 万个改动，一个回到古法编程。差别不在 AI，在关卡。

那家公司能一直手写下去吗？肯定不会。效率这东西，一旦提上去，就回不去了。习惯了用 AI 的人，再让他一行行手敲，就会觉得在浪费生命。

关卡搭好以后，人只需要守在两头：开头说清楚要什么，最后决定能不能上。中间那一大段，交给 AI。

所以我的判断是：用不到一年，大部分做软件的公司都会变天。照现在 AI 的效率，至少三分之二的人是不需要的。

中间那一大段原来站着很多人，人一多，沟通就多，效率反而低了。

如果一家公司现在还是这套流程：产品经理写需求，开 Grooming 会把需求拆成 story，开 Planning 会排迭代，开发写代码，QA 测试，文档团队写文档，最后交给运维发布。在我看来，这已经落后了一个时代了。

这套老东西为什么还在？就像很多地方装的闸机，装上以后大家天天刷卡通过，也就习惯了。想拆，得拿出很充分的理由，还得担拆的责任，担拆了以后万一出事的责任。留着它，什么都不用解释。

V2EX 那家公司禁掉 AI，其实他需要的是关卡，不是又一道闸机。闸机是每个人都拦，关卡是按风险拦。

这些都拆掉以后，还需要什么人？

初级的人，可以肯定地说，不再需要了。初级的活，甚至中级的活，AI 都已经包了。

能留下来的，是能把关的人：离客户近，知道什么该做；有判断力和品味，看得出 AI 写的东西方向对不对、架构合不合理；敢说「这个能上」或者「这个不能上」，并且为这句话负责。

这几种人有个共同点，我管它叫资格。

上个月，CentOS 的作者 Gregory Kurtzer 用 OpenAI 的 Codex，11 天写出了一个[新内核，叫 Ginux](https://itsfoss.com/news/ginux/)，现在 [GitHub 上](https://github.com/gmkurtzer/ginux)有六百多颗星。换一个没人认识的人做同样的事，大概率没这么多人关注。

差在他二十多年前就在做 CentOS，后来又做了 Rocky Linux，被那么多公司放在生产环境里用了这么多年。

在公司里也一样。你说「这个能上线」的时候，同事、领导信不信，看的不是你今天让 AI 写了多少代码，是你以前拍板的那些事出没出过岔子。

代码 11 天就能写出来，资格却要攒一整个职业生涯。

## 参考

- [V2EX，《我司全面禁止 AI Coding，一夜之间回到古法编程时代》](https://www.v2ex.com/t/1258200)
- [Anthropic，《When AI builds itself》（截至 2026 年 5 月，合并代码 80% 以上由 Claude 编写；人工评审成为新瓶颈；每个改动都过 Claude 自动评审，回溯估计能拦下以往 claude.ai 事故约三分之一的 bug）](https://www.anthropic.com/institute/recursive-self-improvement)
- [Anthropic，《Redesigning source control at Anthropic》（2026-10-13，每天合并改动 2,500 → 30,000+；「工程师的角色是对 Claude 说不」）](https://www.anthropic.com/engineering/redesigning-source-control)
- [The Pragmatic Engineer，《Inside OpenAI's agentic software factory》（2026-09-15）](https://newsletter.pragmaticengineer.com/p/openai-software-factory)
- [It's FOSS，Ginux 报道（2026-10-27）](https://itsfoss.com/news/ginux/)
- [Ginux 仓库](https://github.com/gmkurtzer/ginux)

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
