---
title: 如何把自己的 Python 代码打包发布到 PyPI
tags:
  - Python
  - PyPI
  - Release
categories:
  - Python
date: 2020-08-02 08:13:17
author: shenxianpeng
---

## 背景

使用 Python 编程的人都知道，Python 的优势之一就是有大量的第三方库，通常使用如下命令

```
pip install xxxx
```

就可以轻松下载，真是即酷炫又方便，你有没有想过这个是怎么实现的？最近正好赶上又开始写 Python 借此机会分享一下。

<!-- more -->

## 什么是 PyPI

PyPI 是 The Python Package Index 的缩写，意思是 Python 包索引仓库，用来查找、安装和发布 Python 包。

PyPI 又两个环境，一个是测试环境 [TestPyPI](https://test.pypi.org/) 和 正式环境 [PyPI](https://pypi.org/)

## 准备

1. 如果想熟悉 PyPI 发布工具和发布流程可以使用测试环境 [TestPyPI](https://test.pypi.org/) 
2. 如果已经熟悉了 PyPI 的发布工具和流程可以直接使用正式环境 [PyPI](https://pypi.org/)
3. TestPyPI 和 PyPI 需要单独注册，即在正式环境注册了，如果去使用测试环境也同样需要注册。
4. 已经写好并且可以正常使用的项目/库/方法。

## 如何发布

官方有详细的示例和文档，这里就不多做演示和翻译了，攒点耐心看完 https://packaging.python.org/tutorials/packaging-projects/

全当（一定要）锻炼自己的阅读官方有英文文档的能力，你就完全了解如何发布项目到 PyPI 上面了。

## 总结

发布一个 Python 项目到 PyPI 还是非常简单的，遵照上述的步骤，每个人都可以将上面的项目发布到自己账户下。

只是有一个问题需要注意一下，作为公司一般情况下开发者无需担心 License 的选择，一般公司是由法务部门完成版权相关问题。如果是个人开发者，就需要了解一下 License，推荐一篇[文章](https://mp.weixin.qq.com/s?src=11&timestamp=1595346878&ver=2474&signature=Ct0nRc7fLMxhZV2OPjsc2bDnBkBZIclPMI1qRGdFf3hbWM3Q-*jPYwVknsa9laPvvgyRgXTXUHGZcigY0HLZNtUHMkYbDjCQp6LYMNT5zN9s5zNM44BxismGcfbxNA7D&new=1)供参考。

另外如果是正式版本，在发布还需要注意版本号的选择。如果是功能很简答，完成度也不高，建议从 0.0.1 版本开始。如果是一个完成度很高的产品了，那么可以从 1.0.0 版本开始。

至此，一个 Python 代码就可以正式发布了，你可以使用 `pip install xxx` 来安装了，想想就觉得自己特别酷。
