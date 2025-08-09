---
title: C-print
summary: |
  一个 C 语言打印字符的示例，展示如何使用循环和条件语句打印特定模式的字符。
date: 2018-07-08
tags:
    - C
    - Language
author: shenxianpeng
---

如何打印下面的字符？

```c
$

##
$$$
###
$$$
##
$
```

示例 1：

```c
int main()
{
    char array[] = {'#', '$'};
    for (int row = 1; row <= 7; row++) {
        for (int hashNum = 1; hashNum <= 4 - abs(4 - row); hashNum++)
        {
            printf("%c", array[row % 2]);
        }
        printf("\n");
    }
}
```
