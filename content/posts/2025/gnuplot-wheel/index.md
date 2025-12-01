---
title: 为了让大家少敲两行命令，我把 gnuplot 封成了一个开箱即用的 Python 包
summary: |
  作为一个开源项目维护者，我深知“安装依赖”的痛苦。为了让用户少敲两行命令，我花时间把 gnuplot 封装成了一个开箱即用的 Python 包——gnuplot-wheel。本文分享了这个小轮子的诞生故事和实用价值。
tags:
  - gitstats
  - gnuplot
authors:
  - shenxianpeng
date: 2025-12-01
---

写代码写久了，人多少都会变得有点“偏执”。

一种是对 **秩序** 的偏执——命名要统一、缩进要整齐、格式化必须干净利落。

另一种，是对 **简单** 的偏执——越自动化越好、越开箱即用越好、越无感越好。

尤其是当你兴致勃勃地想试一个新开源项目、敲下安装命令回车的那一刻，你期待看到的是：

* 一行行绿色的进度条
* 一眼就能看懂的 “Successfully installed”

而不是：

* 满屏的红色报错
* 冷冰冰的一句 “请先安装 XXX 系统依赖”

那种感觉，就像你饥肠辘辘打开外卖盒，结果——

> **店家忘了给你筷子。**
> 饭就在那儿，香味都飘出来了，但你就是吃不到嘴里。

这种挫败感，是所有开发者心中共同的痛。

最近，我在维护自己的开源项目时，也被这根“筷子”折腾得够呛。
为了彻底解决它，我干脆……造了一个新的“轮子”。

今天就来聊聊它背后的故事。

---

## **起因：gitstats 与它唯一“不够顺滑”的地方**

我一直在维护一个工具叫 [**gitstats**](https://github.com/shenxianpeng/gitstats)，主要用来生成 Git 仓库的统计报表：

* 提交活跃度
* 贡献者排行
* 项目增长趋势
* 图表可视化展示

它开源、简单、好用——除了一个点：
**它依赖 gnuplot。**

[gnuplot](http://www.gnuplot.info/) 是一个非常成熟的绘图工具，在科研与数据分析领域非常常见。

问题在于：它必须在系统层面手动安装。

Linux 需要 `apt install`；
macOS 需要 `brew install`；
Windows……你懂的，更麻烦。

这就像流程里唯一的一粒沙子，让整个体验不够丝滑。

我开始思考：
**能不能把 gnuplot 做成一个 Python 包，用一条 `pip install` 就能装好？**

* 不需要管理员权限
* 不污染系统环境
* 不管你是 Linux / Windows / macOS 都能自动匹配
* 只要有 Python，就能跑

这样，开发者就能像安装普通 Python 包一样，把 gnuplot 一并带上。

---

## **于是，gnuplot-wheel 诞生了**

经过一番调研与折腾，我终于把 **gnuplot 的二进制文件打包成了 Python 的 wheel 文件。**

从此以后，你只需要敲下：

```bash
pip install gnuplot-wheel
```

* gnuplot 的二进制文件会自动安装到虚拟环境
* 不需要系统级依赖
* 不会和已安装的 gnuplot 冲突
* 不需要管理员权限

安装完成后，你就能直接执行 `gnuplot` 命令了——
**无需额外安装任何东西。**

当我第一次在干净环境里看到它顺滑运行时，心里只有一个念头：

> **啊，这就是技术的浪漫——把复杂留给自己，把简单留给用户。**

---

## **谁会用到这个小轮子？**

其实这个轮子不复杂，但非常实用。

### **如果你做科研或数据可视化**

你可以在 Python 程序里直接调用 gnuplot，无需折腾系统依赖。

### **如果你做 DevOps 或自动化**

你可以让脚本自动渲染曲线图、趋势图，而不必在每台机器上手装 gnuplot。

### **如果你在开发依赖 gnuplot 的工具（比如我）**

你可以直接把 `gnuplot-wheel` 加进依赖，让用户上手零成本。

目前，`gnuplot-wheel` 已支持主流平台，并发布在 **PyPI**。

---

## **这个“小轮子”，也反哺了 gitstats**

我已经把它集成进 gitstats。

现在，最新版本的 gitstats 再也不需要用户手动安装 gnuplot。

只要：

```bash
pip install gitstats
```

它就会自动把依赖一并准备好，用户无需关心背后发生了什么。

这就是开源社区最迷人的地方：

> **我为了解决自己的小痛点造了个“痒痒挠”，结果发现它也能帮别人止痒。**

---

## **想试试吗？**

如果你的项目、工作流或脚本里需要用到 gnuplot，不妨试试它。
它不会改变世界，但能让你的开发过程——**顺滑那么一点点。**

项目链接：

* GitHub：[https://github.com/shenxianpeng/gnuplot-wheel](https://github.com/shenxianpeng/gnuplot-wheel)
* PyPI：[https://pypi.org/project/gnuplot-wheel/](https://pypi.org/project/gnuplot-wheel/)

欢迎看看、使用、提 Issue，甚至来一起贡献。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
