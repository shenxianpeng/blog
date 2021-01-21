---
title: Write Pythonic Code
tags:
  - null
  - Python
categories:
  - Python
date: 2021-01-21 10:27:57
author: shenxianpeng
---

接触 Python 是从我早年在京东做自动化测试的时候开始的，那时我还不懂什么规范，只要能让自动化测试用例顺利的跑下来就是万事大吉。

直到几年前，一位非常资深的华人程序员，他在给我培训的时候提到了项目中有一些代码不 `Pythonic` 需要重构，这是我第一次接触到这个词。根据语境，我理解他的意思：Pythonic 就是以 Python 的方式写出简洁优美的代码！

那么什么样的 Python 代码才算是 Pythonnic 呢？写出 Pythonic 的代码的意义是什么？测试、开发、DevOps要不要学习这些？

```
C:\Users\xshen>python
Python 3.8.6 (tags/v3.8.6:db45529, Sep 23 2020, 15:52:53) [MSC v.1927 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import this
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
>>>
```
