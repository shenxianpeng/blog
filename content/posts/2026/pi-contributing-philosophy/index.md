---
title: pi 项目里那些反直觉的设计：从 AGENTS.md 到「先把你的 PR 关掉」
summary: |
    读完 Mario Zechner 的「I've sold out」，又翻了 pi 仓库里的 AGENTS.md 和 CONTRIBUTING.md，我发现这个项目在很多地方都和常见的开源协作方式不太一样。新贡献者的 issue 和 PR 默认关闭、周末不 review、不懂代码就别提 PR。看起来很强硬，但背后其实是在认真处理一个问题：AI 时代，开源项目要怎么避免被低质量贡献拖垮。
tags:
  - AI
  - Open Source
  - pi
authors:
  - shenxianpeng
date: 2026-04-26
---

周末写了一篇[用 pi + DeepSeek 做 Codex 备用方案](/posts/2026/pi-deepseek/)的文章。

写完之后，我又顺手翻了翻 pi 这个项目的其他内容，结果发现，真正有意思的地方不只是工具本身，而是它背后的一套协作方式。

尤其是它的 AGENTS.md 和 CONTRIBUTING.md，读完之后我有点意外。

这个项目的很多规则，和我们平时理解的开源社区几乎是反着来的。

* 新贡献者的 issue 和 PR 默认关闭。
* 周末提交的 issue 不处理。
* 如果你不理解自己提交的代码，PR 会直接被关掉。

这些规则看起来很硬，但结合 Mario Zechner 最近那篇文章一起看，就会发现它不是单纯的「不欢迎贡献者」，而是在认真思考一件事：

**AI 时代，开源项目到底该怎么可持续地维护下去。**

## 从 Mario 的那篇博客说起

4 月 8 日，pi 的作者 Mario Zechner 发了一篇博客：[I've sold out][1]。

标题有点自嘲，内容却很真诚。

他在文章里回顾了自己从 2009 年开始做开源的经历。先是 [libGDX][2]，一个跨平台游戏开发框架，曾经是 Android 上很流行的游戏引擎，Ingress 和《杀戮尖塔》（Slay the Spire）都用过它。

后来他参与了一家叫 RoboVM 的创业公司，做 JVM 到 iOS 的 AOT 编译器。再后来，RoboVM 被 Xamarin 收购，Xamarin 又被微软收购，微软最终关掉了 RoboVM。

作为当时的「OSS guy」，Mario 不得不去写那篇「抱歉，不再开源了」的公告。结果可以想象，他在社交网络和邮件里被骂得很惨。

问题是，这个决定并不是他能控制的。

这段经历让他对 VC、创业公司和开源之间的关系有了非常清醒的认识。说得更直白一点，就是他被现实教育过。

所以当 pi 因为 [OpenClaw][3] 爆火，被越来越多 VC、大厂和潜在投资人关注时，他面对的不是一个简单的「要不要变现」问题，而是一个他以前已经踩过坑的问题：

如果一个开源项目突然有了商业价值，接下来该怎么办？

他最后的选择不是自己出来开公司，而是加入 [Earendil][4]。

原因也很简单：他有一个四岁的孩子。他想陪孩子长大。

如果自己做 CEO，接下来的就是找 co-founder、找 PMF、搭团队、搞企业文化、处理各种人和钱的问题，然后慢慢停止写代码，变成一个他不喜欢的「管理者」。

加入 Earendil 之后，他可以继续写代码，继续维护 pi，同时也有一个团队来帮他处理商业化的事情。

Mario 在文章里也说：pi 的核心代码会继续保持 MIT 协议，可以 fork，可以使用，可以基于它做产品。真有一天方向不对，fork 按钮还在那里。

因为他当年亲眼看过 libGDX 社区在 RoboVM 闭源之后 fork 出 MobiVM，所以他知道这件事真的会发生。

## Armin Ronacher 的加入

Mario 加入 Earendil 的另一个关键原因，是 Armin Ronacher。

如果你写过 Python Web，大概率见过这个 ID @mitsuhiko。他是 [Flask][5] 的创建者，也写过 Jinja2、Click、Werkzeug 等这些 Python 生态里非常重要的项目。同时，他也是 [Sentry][6] 的联合创始人，对「开源项目如何商业化」这件事有实际经验。

Armin 也写了一篇文章，欢迎 Mario 加入 Earendil：[Mario and Earendil][7]。

他对 pi 的评价：pi 并不是靠喊得最大声、跑得最快来吸引人的，而是能看出来作者很在意软件质量、设计感、可扩展性和长期维护。

现在很多 AI coding 工具给人的感觉是：先发出来，先占坑，先把声量打起来。至于设计是不是统一，代码是不是干净，长期能不能维护，反而经常被放到后面。

pi 给人的感觉不太一样。

它不是最会宣传的那个，但你越往仓库里看，越能感觉到作者对工程细节是有要求的。

Mario 和 Armin 认识已经十几年了。最早是在 Reddit 的 r/austria 版块互相辩论，后来在线下见面，慢慢成了朋友。2025 年 AI 编码工具爆发之后，Steinberger、Mario 和 Armin 经常交流、实验、互相 review 博客文章，后来还被人调侃成「维也纳编码代理学派」。

这个背景也挺重要。

很多商业合作看起来是突然发生的，其实背后往往是长期信任的结果。尤其是开源项目，一旦涉及所有权、商标、协议和未来路线，只靠一份合同是不够的。

你得相信一起做事的人不会乱来。

## AGENTS.md：给 AI agent 的项目入职手册

pi 仓库里有一个 [AGENTS.md][8] 文件。

我一开始只是随便点进去看了一眼，结果发现它写得非常细。

里面规定了 AI agent 参与 pi 开发时要遵守的规则，包括：

- 回复要简洁，不要表情符号，不要废话
- 不要随便使用 `any` 类型
- 不要使用内联 `import`
- 不要为了绕过类型错误而删除或降级代码
- 修改代码之后要跑 `npm run check`
- 不要在没理解的情况下删除看起来「没用」的代码
- 新增 LLM Provider 要改哪些文件、补哪些测试
- 多个 agent 并行工作时，不能用 `git add -A`
- 不能用 `git stash`
- 不能用 `git reset --hard`
- 发布流程该怎么走

这些规则看起来很细，甚至有点啰嗦，但如果你真的用过 coding agent，就会知道它们很有必要。

现在的 agent 不缺能写多少代码，缺的是写出高质量代码。

有些规则不是靠 prompt 临时补充，这样很容易漏掉。AGENTS.md 的价值就在这里：它把项目里的工程习惯写成了一份固定的上下文。

这样就给 AI agent 一个「操作手册」。

如果你的项目也已经开始大量使用 AI 编码工具，可以认真参考一下 pi 的做法，给自己的项目也写一份 AGENTS.md。

不用一上来写得很复杂。先把最容易出错的几件事写进去，就已经能减少很多无效修改和 Token 浪费了。

## CONTRIBUTING.md：先把你的 PR 关掉

如果 AGENTS.md 写给机器，[CONTRIBUTING.md][9] 就是写给人的——措辞直接，不讲客气。

**一、不懂就别提。** 用 AI 写代码可以，但如果你解释不了自己的 PR 做了什么、怎么跟系统交互，直接关掉。你用 AI 省下的时间，不该变成 maintainer 替你兜底的成本。

**二、新人默认关闭。** 所有新贡献者的 issue 和 PR 自动关闭。想「转正」？靠 maintainer 在 issue 下回复的信任标记——不是 GitHub label，是评论内容：回复 `lgtmi`，未来 issue 不再自动关闭；回复 `lgtm`，issue 和 PR 都不再自动关闭。每天 maintainer 会浏览被关闭的 issue，有价值的挑出来重新打开并给出标记。pi 不是拒绝新贡献者，是要求你先证明自己的提交值得 review——agent 让制造 issue/PR 的成本越来越低，门槛就越来越重要。

**三、周末不受理。** 周五到周日提交的 issue 自动关闭，不进入周一 review 队列。着急就去 Discord。FAQ 里的解释很直白：*"Maintainers need uninterrupted time away from the issue tracker."*

**四、两次无视规则封禁。** 如果两次无视 CONTRIBUTING.md，或用 agent 向 issue tracker 批量灌水，会被 Pi 项目永久封禁。

## 这些规则背后的逻辑

表面上看 pi 的规则让人觉得它不欢迎贡献者，不欢迎社区参与。

但继续读 CONTRIBUTING.md 的 FAQ，就能看到它真正想解决的问题。

pi 收到的 issue 数量已经超过了维护者能实时认真 review 的范围。很多 issue 没有达到质量要求，也没有遵守 CONTRIBUTING.md。更麻烦的是，有些内容是被 agent 没怎么思考就直接丢到仓库里的。

这就是现在很多项目会越来越头疼的问题。

AI 降低了写代码和写 issue 的成本，但没有自动提高提交质量。

甚至很多时候，它会让低质量内容变得更像高质量内容。格式完整，语气礼貌，文字通顺，但问题可能是错的、重复的、不可复现的，或者需要 maintainer 花大量时间去验证。

这对开源维护者来说很危险。

因为每一个看起来「还行」的 issue，背后都可能是一笔隐藏成本。

* 你要读。
* 你要判断。
* 你要复现。
* 你要回复。
* 你要解释为什么不接受。

这些都是维护成本。所以 pi 的自动关闭机制，本质上是在给 maintainer 创造缓冲区。

不是所有东西都立刻进入正式 review 流程，而是先被挡在外面，再由维护者按自己的节奏挑出真正值得处理的内容。

这和 Mario 在博客里讲的生活选择是连在一起的。

他不想再过那种孩子哭着说「daddy isn't here」的生活。Earendil 团队里很多人也都有孩子，公司文化上也重视这一点。

这就解释了为什么 pi 的规则会这么强调边界。

它不是单纯为了控制贡献者，也不是为了显得高冷，而是在保护两件事：

* 维护者的生活质量。
* 项目的代码质量。

这两件事如果保不住，开源项目表面再热闹，最后也很容易走向 burnout。

## 对你的项目有什么参考价值

pi 的做法不一定适合所有项目。

如果项目很小，贡献者也不多，这个门槛就是在自嗨。

但如果你的项目已经开始受到 AI 生成 issue、AI 生成 PR、低质量自动化提交的影响，那 pi 的做法确实值得参考。

但不管项目大小，以下可以直接借鉴的点：

1. **写一份 AGENTS.md**

如果你的项目里已经开始使用 AI coding agent，就不要只依赖临时 prompt。

把项目规则写下来。

比如测试怎么跑、哪些命令不能跑、代码风格是什么、哪些目录不能随便改、提交前必须检查什么。

这些内容写进 AGENTS.md，比每次重新解释更稳定。

2. **把质量要求写具体**

不要只写「欢迎高质量贡献」。

应该写清楚什么样的 issue 会被处理，什么样的 issue 会被关闭。

比如：

- 必须使用 issue template
- 必须说明问题是什么
- 必须解释为什么重要
- bug 必须提供复现方式
- 大需求先讨论，不要直接上 PR

规则越具体，maintainer 的解释成本越低。

3. **保护维护者的时间**

开源维护不是客服。

不是所有时间都应该是响应时间。

可以明确写出来：自测通过了再找 maintainer review，低质量问题不保证回复。

这听起来有点冷，但比长期消耗到不想维护要好得多。

4. **建立信任机制**

pi 对于新贡献者的 issue 和 PR 默认关闭，但通过了 maintainer 的回复之后就可以解锁。然后这个人的 ID 就会被记录下来，后续提交就不会再被自动关闭了。

## 不只是协作：pi 的工具设计也是同一个思路

上面聊的是 pi 怎么对待贡献者。但其实 pi 这个工具本身的很多设计，遵循的是同一套逻辑：**去掉所有不必要的抽象，只保留真正有用的东西。**

Mario 在另一篇博客 [What I learned building an opinionated and minimal coding agent][10] 里详细讲了这些设计选择，读完会发现它们和 CONTRIBUTING.md 背后的想法是通的。

### 极简的系统 prompt

pi 的系统 prompt 只有不到 1000 个 token。

对比一下：Claude Code 的系统 prompt 有上万 token，opencode 也差不多。pi 只告诉 agent 四件事：你是谁、你能用什么工具、怎么用、文档在哪。

这和 CONTRIBUTING.md 的风格一模一样。不写长篇欢迎词，不堆砌礼貌用语，直接说清楚规则。

Mario 的解释是：前沿模型已经被 RL 训练得足够好了，它们天生理解什么是 coding agent。不需要用一万个 token 去解释。

Benchmark 结果也证明了这一点：pi + Claude Opus 4.5 在 Terminal-Bench 2.0 上的表现排在所有参赛 agent 的前列，只输给了 Codex 的原生模型。一个系统 prompt 不到 1000 token 的工具，和那些系统 prompt 上万 token 的工具打得有来有回。

### 只有四个工具

pi 默认只给 agent 四个工具：`read`、`write`、`edit`、`bash`。

没有内置的 Web 搜索、没有 Git 操作、没有 to-do 列表、没有 plan mode。

这听起来像功能缺失，但 Mario 认为四个工具已经够了。模型知道怎么用 bash，也已经被训练过类似 `read`、`write`、`edit` 的工具。

而且他很抗拒在工具层加抽象。比如：

- **没有内置 to-do**：要追踪任务，就在项目里放一个 `TODO.md`，agent 自己读写。用 checkbox 标记完成状态。简单、可见、可控。
- **没有 plan mode**：要规划，就写一个 `PLAN.md`。和那种只存在于 session 里的规划不同，文件可以跨 session 共享，可以 commit 到仓库，人可以随时看到和修改。Mario 特别强调了一点：**plan 这件事，他需要完全的可观测性。** 在 Claude Code 里，plan mode 会 spawn 一个 sub-agent，你根本看不到它做了什么。但在 pi 里，agent 读了哪些文件、产出了什么 markdown，全都在你眼皮底下。
- **没有 MCP 支持**：MCP server 会把二三十个工具描述一股脑塞进 context，光工具定义就可能吃掉 7–9% 的 context window。Mario 的做法是把这些功能写成 CLI 工具 + README，agent 需要的时候自己读 README、用 bash 调用。只在需要的时候才消耗 token（他称之为 progressive disclosure），而不是每个 session 开局先扣掉几万 token。
- **没有后台 bash**：要跑 dev server 或者调试进程？用 tmux。agent 在 tmux 里操作，人可以随时 attach 进去看、甚至可以 co-debug。比起一个你看不到内部状态的后台进程管理模块，tmux 给了你完整的可观测性。
- **没有 sub-agent 工具**：agent 如果需要 spawn 自己，直接用 bash 跑 `pi --print`。虽然不完全等于 sub-agent，但输出的结果是完全可见的。Mario 对 sub-agent 的批评很直接："It's a black box within a black box." 而且他认为，很多人用 sub-agent 做 context gathering，其实是工作流有问题——应该先在独立 session 里收集上下文，产出 artifact，再在新 session 里带着 artifact 开始工作。

这些设计选择放在一起看，有一条很清晰的线：

**宁可让 agent 用最简单的方式操作文件、跑命令，也不要在中间加一层你看不透的抽象。**

### 这和 CONTRIBUTING.md 有什么联系

回到协作这件事上，pi 的 CONTRIBUTING.md 做的是同样的事：

- 用一个简单的规则（默认关闭）代替复杂的 review 流程
- 用一个明确的信任标记（`lgtmi` / `lgtm`）代替模糊的「欢迎贡献」
- 用一个固定的 FAQ 代替每次都要解释为什么关掉你的 PR

两边都是同一个思路：**去掉中间层。**

工具设计里，去掉的是不必要的 feature 和抽象层。

协作规则里，去掉的是不必要的礼貌用语和不保证质量的 openness。

Mario 在博客里反复提到一个词：observability。

他想要看到 agent 做的每一件事。他不想要 sub-agent 在黑箱里操作，不想要后台进程不可见，不想要 plan mode 只给结果不给过程。

CONTRIBUTING.md 也可以从这个角度理解：

它让维护者的决策过程对贡献者可见。你被 close 了不是因为 maintainer 心情不好，而是因为规则就是这样。FAQ 里把原因写清楚了。你只要按规则来，就有路可以走。

从工具到协作，pi 这个项目有一个很一致的审美：

**简单、直接、可见。不为了「看起来更好」而加东西。**

这也是为什么我觉得它的做法值得认真看。它不是一个大型开源项目的治理模板，但它是一个思考得很透彻的案例——关于一个开源项目在 AI 时代到底应该怎么设计自己和外界的接口。

## 最后

我看完 pi 的这些规则，最大的感受是：

**热门开源项目的稀缺资源可能不再是贡献者，而是 maintainer 的时间。**

尤其是 AI Agent 爆发后，贡献的数量可能会越来越多，质量却未必同步提高。

这时候，一个项目真正需要保护的可能不是「欢迎更多人来贡献」，只是「欢迎更多有价值的贡献」。

pi 的规则看起来反直觉，但它至少诚实地面对了这个问题。

* 它没有假装所有贡献都是好贡献。
* 也没有假装 maintainer 的时间是无限的。

AI 时代的开源项目，可能需要更多这样的思考和设计，让项目真正保持可持续的维护和高质量的发展。

[1]: https://mariozechner.at/posts/2026-04-08-ive-sold-out/
[2]: https://libgdx.com
[3]: https://openclaw.ai
[4]: https://earendil.com
[5]: https://flask.palletsprojects.com/
[6]: https://sentry.io
[7]: https://lucumr.pocoo.org/2026/4/8/mario-and-earendil/
[8]: https://github.com/badlogic/pi-mono/blob/main/AGENTS.md
[9]: https://github.com/badlogic/pi-mono/blob/main/CONTRIBUTING.md
[10]: https://mariozechner.at/posts/2025-11-30-pi-coding-agent/
