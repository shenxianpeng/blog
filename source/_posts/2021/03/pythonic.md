---
title: 你的 Python 代码够不够 Pythonic？
tags:
  - Pythonic
  - Python
categories:
  - Python
date: 2021-03-28 10:27:57
author: shenxianpeng
---

Python 不必多说，它是众多编程语言中最容易学习的动态类型语言。它的跨平台、易读、易写、丰富的 Packages 等众多特性，也是众多DevOps/测试/开发工程师是最常用的语言之一。

相信不少人用它完成了很多工作，但你是不是仅仅止步于功能的实现而忽略了去写出更加简洁，优美的 `Pythonic` 代码呢？

在我最开始用 Python 时，我还不知道 `Pythonic` 这个词，直到多年前一位资深的程序员在给我培训的时候提到了项目中有一些代码不够 `Pythonic`，需要重构。根据语境，我理解他的意思：就是 Python 的代码没有按照 Python 的方式来写。

## 什么是 Pythonic

充分利用 Python 语言的特性来产生清晰、简洁和可维护的代码。`Pythonic` 的意思是指代码不仅仅是语法正确，而是遵循 Python 社区的惯例，并以其预期的方式使用该语言。

## 举例

以下是 C/C++ 程序员的一段代码:

```c
int a = 1;
int b = 100;
int total_sum = 0;
while (b >= a) {
    total_sum += a;
    a++;
}
```

如果没有学习 Python 编程模式，那么将上面的代码改用 Python 来写可能会是这样：

```python
a = 1
b = 100
total_sum = 0
while b >= a:
    total_sum += a
    a += 1
```

如果用 Pythonic 的方式来写，应该是这样的：

```python
total_sum = sum(range(1, 101))
```

再举个常见的例子，如果用 Java 可能是这样写出来一个 For 循环

```java
for(int index=0; index < items.length; index++) {
    items[index].performAction();
}
```

在 Python中，使用以下方法会更干净一些：

```python
for item in items:
    item.perform_action()
```

甚至是一个生成器表达式：

```python
(item.some_attribute for item in items)
```

因此，从本质上讲，当有人说某件事情不符合 `pythonic` 时，他们是在说这段代码可以用一种更适合 Python 编码风格的方式来重新编写。
另外，去了解 Python [Built-in Functions](https://docs.python.org/3/library/functions.html)，而不是重新造轮子。

## 关于 Pythonic 的“官方介绍”

其实，Python 命令行里已经秘密“隐藏”了关于 `Pythonic` 的介绍。只要打开 Python 控制台，输入 `import this`，你就能看到：

```text
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

直译过来是：Tim Peters 的《Python的禅意》

```text
美丽的比丑陋的好。
明确的比含蓄的好。
简单的比复杂的好
复杂的比复杂的好
扁平的比嵌套的好。
稀疏比密集好。
可读性很重要。
特殊情况不特殊，不足以打破规则。
虽然实用性胜过纯粹性。
错误永远不应该默默地通过。
除非明确沉默。
在面对模棱两可的情况下，拒绝猜测的诱惑。
应该有一个--最好只有一个--明显的方法。
虽然这种方式一开始可能并不明显，除非你是荷兰人。
现在总比不做要好。
虽然从不比现在*好。
如果实现很难解释，那就是个坏主意。
如果实现很容易解释，它可能是个好主意。
命名空间是一个非常棒的想法--让我们做更多的命名空间!
```

关于 `Pythonic` 你 get 到了吗？