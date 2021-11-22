---
title: Python Lambda Functions
tags:
  - Python
  - lambda
categories:
  - Python
date: 2020-08-16 14:21:19
author: Joe Marini
---

如果你用其他语言（例如JavaScript，C＃或Java）进行过任何编程，则可能已经看过或使用过匿名函数。 Python 也支持这些功能，它们被称为 lambda 函数。

* Small, anonymours functions
* Can be passed as arguments

Lambda 函数可以作为参数传递给其他函数以执行某些处理工作，就像 JavaScript 语言中的回调函数一样。通常，你会在定义整个单独功能的情况下不必要地增加代码的复杂性并降低可读性的情况下使用它们。通过使用关键字 lambda 定义 Lambda，后跟 lambda 函数采用的所有参数，然后是表达式。因此，让我们看一下它们在实际中的用法，因为这通常是理解某些事物的最佳方法。

在文件的顶部，我有两个常规函数，每个函数都执行从一个温度标度到另一个温度标度的转换。这一温度将摄氏温度转换为华氏温度，而与此相反。在主要功能中，我有两个温度列表，一个以摄氏度为单位，一个以华氏度为单位。现在，假设我想将每个列表转换为另一个温度标度。为此，我使用 map 函数。并且，回想一下 map 函数将一个函数作为第一个参数，将一个可迭代对象（如列表）作为第二个参数。因此，要转换这两个列表，我将编写类似于 map 的内容，然后将 FahrenheitToCelsius 称为函数，然后传递 ftemps 列表。然后，要打印出来，我将其放入列表中以生成列表，然后我将对整个对象进行打印，然后将其复制并粘贴并使用 CelsiusToFahrenheit 进行相同的操作，然后传递给 temps。好吧，让我们运行我们所拥有的。

```python
def CelsiusToFahrenheit(temp):
  return (temp * 9/5) + 32

def FahrenheitToCelsius(temp):
  return (temp-32) * 5/9

ctemps = [0, 12, 34, 100]
ftemps = [32, 65, 100, 212]

# 使用通常的方法来转换 temps
print(list(map(FahrenheitToCelsius, ftemps)))
print(list(map(CelsiusToFahrenheit, ctemps)))

# 使用 lambdas 来实现同样的转换
print(list(map(lambda t: (t-32) * 5/9, ftemps)))
print(list(map(lambda t: (t * 9/5) + 32, ctemps)))
```

我将去调试视图。而且，请记住，如果你不想使用 VS Code，则可以从终端命令行运行。因此，我将运行它。并且，你可以在这里看到每个温度都已转换的结果。

现在，我可以通过将每个函数编写为内联 lambda 来降低代码的复杂性，因为它们非常简单。所以，让我们回去做。我将清除控制台。而且，我将复制这两行并将其粘贴到此处。现在，我将每个函数替换为 lambda 等效项。

因此，我将输入 lambda t，因为每个 lambda 函数都将一个温度作为参数。然后，对于 FahrenheitToCelsius 案例，我将复制此表达式并将其粘贴到此处。而且，我必须将其更改为，因为它不再是临时的。而且，这里也是一样。我将编写 lambda t，现在我将获得 CelsiusToFahrenheit 版本。因此，我将其复制，粘贴并更改为 t。好吧，现在你可以看到结果是相同的。在这种特殊情况下，使用 lambda 表达式确实可以简化我的代码，因为我可以在使用它的地方看到计算结果，并且即使现在已经是我几年了，也需要其他人来处理我的代码，而不必仔细研究所有源代码，以了解定义转换函数的位置。现在，很明显，lambda 并不是适合每种情况。当然，实际上，你将继续在程序中使用常规函数，但是当定义一个完整的函数比花费更多的精力时，lambda 可以帮助使你的代码更具可读性。
