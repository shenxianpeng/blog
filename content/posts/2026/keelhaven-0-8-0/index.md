---
title: Keelhaven 0.8.0：用户提的需求，我一条条改了
summary: |
  0.5.0 发布后九天，Keelhaven 连发了三个版本，装进去的大半是真实用户提的需求：新的备份目的地、可自定义的备份参数、备份预览、只保留最近 N 个快照。这篇讲讲反馈都去了哪，什么还在考虑中，以及这个项目接下来会怎么走。
tags:
  - Keelhaven
  - Backup
  - macOS
  - Open Source
authors:
  - shenxianpeng
date: 2026-09-09
translate: false
series: ["我的开源项目"]
series_order: 5
---

8月31日我发布了 Keelhaven 0.5.0，9月3日在[上一篇](../keelhaven/index.md)里介绍了它。上一篇文章发出去之后，我开始收到一些真实用户的反馈：有人发邮件，有人直接开 GitHub issue，有人在 X 上转发，也有人点了 Star。

这些反馈大多是我一个人坐在电脑前想不出来的。有一位用户把五条反馈装进一个 issue，标题叫「有几个就一起反馈吧~」；还有一位从命令行 restic 迁过来的用户，把每天在用的参数抄了一份发到我邮箱。

从 0.5.0 到 0.8.0 只隔了九天，这九天里发了 0.6.0、0.7.0、0.8.0 三个版本，装进去的大半都是这类反馈。

---

## 这些反馈都去哪了

下面是其中一部分的去向。每一条背后都有对应的 issue，细节和进度在 GitHub 上都是公开的：

| 反馈 | 现在的样子 |
|:--|:--|
| 想备份到自己家的服务器（[rest-server](https://github.com/restic/rest-server)） | 0.6.0 起直接选，凭据照旧进钥匙串 |
| 想要更多可调的备份参数（[#37](https://github.com/shenxianpeng/keelhaven/issues/37)） | 0.7.0 起做成具名选项：上传限速、同时读取文件数、打包大小 |
| 邮件里列出的四个参数：跳过缓存目录、不跨磁盘、内容没变化就跳过、备份前不预扫描 | 0.8.0 全部加上了，现在共有七个具名参数 |
| 建计划时就想设好排除规则、保留策略和验证周期（[#39](https://github.com/shenxianpeng/keelhaven/issues/39) 里的几条） | 0.8.0 向导最后一步可以「自定义这个计划」，首次备份也可以选择先不跑 |
| 保留策略想「只留最近 N 个快照」 | 0.8.0 新增第四种保留策略，数值限制在 1–999，不会误删 |
| 改完排除规则，想先看看这次会备份什么 | 0.8.0 计划菜单里有「预览备份」：只计算，不写入 |
| 用 Backblaze B2 的，问 hard delete（[#47](https://github.com/shenxianpeng/keelhaven/issues/47)） | 原因写进了 FAQ，向导里检测到 B2 会直接提示 |

<!-- 建议截图：向导最后一步展开「自定义这个计划」之后的样子 -->

反馈里也有 bug。我自己就在删一个测试计划时撞上过一个：如果正好有别的备份在跑，删除会被静默拦下，屏幕上什么提示都没有（[修复在这里](https://github.com/shenxianpeng/keelhaven/pull/31)）。用户报的 bug 也都在这几个版本里跟着修掉了。完整改动清单可以看 0.8.0 的[发布说明](https://github.com/shenxianpeng/keelhaven/releases/tag/v0.8.0)（英文）。

<!-- 建议截图：预览备份的结果弹窗 -->

---

## 真实用户能告诉我什么

做工具的人有个盲区：太清楚自己写的东西「应该」怎么被用了。0.5.0 发布前，我把创建、备份、删除这些流程在脑子里过了很多遍，觉得该想的都想了。结果用户一用，需求清单就来了。

其中有一条反馈，我第一反应是「这是误会」——编辑按钮明明从来没有被禁用过。查下去发现用户看到的现象是真的，只是原因在我没想到的地方：计划一创建，首次备份立刻就开始了，备份期间操作被锁住，看起来就像「必须先备份一次」。

这类问题，只有真实使用才能暴露出来。所以我特别感谢每一位愿意花时间写下来的用户。

---

## 还没做的，和接下来的打算

不是每条反馈都能立刻落地。下面几件还在考虑或进行中：

- **配置导入导出**（[#44](https://github.com/shenxianpeng/keelhaven/issues/44)）：导出文件不包含钥匙串里的密码，直接导入是「死」的，方案还在定
- **rclone 作为目的地**（[#53](https://github.com/shenxianpeng/keelhaven/issues/53)）：和「凭据只放钥匙串」的设计有冲突，还在等具体的场景
- **自由填写的参数框**：不会做，它会绕过 App 的保护。如果你有具体想要的参数，欢迎去 [#45](https://github.com/shenxianpeng/keelhaven/issues/45) 写下参数名和使用场景，够常用就照同样方式加进来

这个项目会继续做下去。上面这些 issue 都欢迎去留言。

---

## 如果你用 Mac，正在找备份工具

Keelhaven 值得你花十分钟试一下：选好要备份的文件夹、目的地和备份频率，然后就可以忘掉它。它会在后台按计划备份，定期自己检查仓库，出了问题才来提醒你。

加密在本机完成，没有账号系统，备份是标准 restic 格式，随时能恢复、能迁走。开源免费（GPLv3），macOS 14 以上可用。它具体怎么工作，[上一篇](../keelhaven/index.md)介绍得更细。

```bash
brew install --cask shenxianpeng/tap/keelhaven
# 或者
curl -fsSL https://keelhaven.app/install.sh | bash
```

官网：https://keelhaven.app
源码：https://github.com/shenxianpeng/keelhaven

试用之后，无论觉得好用还是踩了坑，都欢迎告诉我：发邮件到 support@keelhaven.app，或者开一个 [GitHub issue](https://github.com/shenxianpeng/keelhaven/issues)；在公众号、知乎或 Twitter 上留言也可以，用中文写完全没问题。

觉得好用的话，欢迎点个 Star，也欢迎转发给身边需要的朋友。谢谢每一位试用它、给它提意见的人。
