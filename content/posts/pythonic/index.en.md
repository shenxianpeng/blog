---
title: Is Your Python Code Pythonic Enough?
summary: This article introduces the concept of Pythonic code and demonstrates through examples how to write more concise and elegant Python code, helping developers improve code quality and readability.
tags:
  - Pythonic
  - Python
date: 2021-03-28
author: shenxianpeng
---

Python, needless to say, is one of the easiest dynamic programming languages to learn.  Its cross-platform compatibility, readability, ease of writing, and rich packages make it one of the most commonly used languages among DevOps/testing/development engineers.

Many have used it to accomplish a lot of work, but do you simply stop at functional implementation and ignore writing more concise and elegant `Pythonic` code?

When I first started using Python, I didn't know the word `Pythonic`.  Years ago, a senior programmer mentioned during my training that some code in a project wasn't `Pythonic` enough and needed refactoring.  From the context, I understood it to mean: the Python code wasn't written in the Pythonic way.


## What is Pythonic

Making full use of Python's features to produce clear, concise, and maintainable code. `Pythonic` means that the code is not only syntactically correct but also follows the conventions of the Python community and uses the language as intended.

## Examples

Here's a snippet of code from a C/C++ programmer:

```c
int a = 1;
int b = 100;
int total_sum = 0;
while (b >= a) {
    total_sum += a;
    a++;
}
```

Without learning Python programming patterns, converting the above code to Python might look like this:

```python
a = 1
b = 100
total_sum = 0
while b >= a:
    total_sum += a
    a += 1
```

A Pythonic way to write this would be:

```python
total_sum = sum(range(1, 101))
```

Here's another common example.  A `for` loop in Java might be written like this:

```java
for(int index=0; index < items.length; index++) {
    items[index].performAction();
}
```

In Python, a cleaner approach would be:

```python
for item in items:
    item.perform_action()
```

Or even a generator expression:

```python
(item.some_attribute for item in items)
```

Essentially, when someone says something isn't `pythonic`, they're saying the code could be rewritten in a way that's more aligned with Python's coding style.
Also, get familiar with Python's [Built-in Functions](https://docs.python.org/3/library/functions.html) instead of reinventing the wheel.


## The "Official Introduction" to Pythonic

In fact, an introduction to `Pythonic` is secretly "hidden" in the Python command line.  Just open the Python console and type `import this`, and you'll see:

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

A direct translation is: Tim Peters' "The Zen of Python"

```text
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
```

Have you grasped the concept of `Pythonic`?