---
title: 我又开源了一个新项目：gnuplot-wheel —— 让安装 gnuplot 简单到只要一条 pip 命令
summary: |
   最近我开源了一个新项目 `gnuplot-wheel`，它能让你通过一条 `pip install gnuplot-wheel` 命令就安装好 gnuplot，无需系统级安装。本文分享了这个项目的背景和动机。
tags:
  - gitstats
  - gnuplot
authors:
  - shenxianpeng
date: 2025-11-29
---

最近，我开源了一个全新的小项目 **gnuplot-wheel**。

* GitHub 地址：[https://github.com/shenxianpeng/gnuplot-wheel](https://github.com/shenxianpeng/gnuplot-wheel)
* PyPI 地址：[https://pypi.org/project/gnuplot-wheel/](https://pypi.org/project/gnuplot-wheel/)

这个项目的目标很简单：

**让开发者在 Python 项目中，一条 `pip install gnuplot-wheel` 就能自动获得 gnuplot。**

无需再去用 `apt`、`brew`、`choco` 安装系统级 gnuplot，也无需管理员权限。
只靠 `pip` 就能把它装进你的 Python 环境里。

今天这篇文章，就跟大家简单聊聊我做这个项目的原因和背景。

---

## gnuplot 是什么？

如果你做过科研绘图、数据分析、脚本式可视化，那么你多半见过 gnuplot。

它不是那种“网红工具”，但却是许多工具链背后的稳定支柱。特点包括：

* 跨平台（Linux / macOS / Windows）
* 命令行生成图表
* 支持脚本自动化
* 能生成专业级图表
* 被大量工具当成后端绘图引擎

属于那种“你可能没用过，但你肯定间接依赖过”的老牌开源项目。

## 为什么我要做这个 wheel？

事情的起点来自我维护的一款开源工具 —— [**gitstats**](../../2024/gitstats/) 。
它能生成 Git 仓库的统计报告，而其中绘图部分需要依赖 gnuplot。

这也意味着用户在安装 gitstats 前，需要额外执行：

```bash
sudo apt install gnuplot     # Ubuntu
brew install gnuplot         # macOS
choco install gnuplot        # Windows
```

虽然这不算什么大问题，但我一直觉得：

> 有没有可能做到真正的“开箱即用”？
> 能不能直接通过一个 Python wheel，把 gnuplot 也顺便装好？

这样 gitstats 的安装体验会好得多，尤其现在用户量越来越大，让用户少折腾一点，就是开发者的幸福。

## 最终结论：可以做到！

经过一段时间的研究、编译和打包，我成功把 gnuplot 做成了可跨平台安装的 Python wheel。

于是，gnuplot-wheel 就这么诞生了。

你现在只需要：

```bash
pip install gnuplot-wheel
```

即可自动获得完整的 gnuplot 运行环境 ——
无需系统安装、无需管理员权限、无需任何提前准备。

这也是我做这个项目最期待实现的效果：
像安装一个普通 Python 包一样安装 gnuplot。

## 现在已正式发布到 PyPI

PyPI 地址：
👉 [https://pypi.org/project/gnuplot-wheel/](https://pypi.org/project/gnuplot-wheel/)

目前支持多个平台，满足主流开发环境。

## 如果你在用 gnuplot，我建议你试一下

尤其是你如果：

* 做科研绘图或数据可视化
* 写自动化脚本
* 维护依赖 gnuplot 的工具
* 或者也在使用 gitstats

试一下它，应该能直接提升你的开发体验：
   
```bash
pip install gnuplot-wheel
```

它能让环境更干净、更可控，也更易于迁移。

## 最后

这个项目最初只是为了解决我在维护 gitstats 时遇到的一个“小痛点”。
但发布后我发现，它可能也能帮到更多需要 gnuplot 的开发者。

如果你有需求或建议，欢迎来 GitHub 提 Issue 或 PR，一起让它变得更好。

希望这个项目能给你的开发带来一点点便利。🌟

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
