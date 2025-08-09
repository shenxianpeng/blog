---
title: C-Language 自定义函数
summary: |
  介绍 C 语言中自定义函数的基本概念和使用方法，包括函数的声明、定义和调用。
date: 2018-05-15
tags:
    - C
    - Language
author: shenxianpeng
---
求次幂函数power

```c
#include <stdio.h>


double power(double, int);  // 形式参数

int main()
{
    printf("%.2lf的%d次幂等于:%.2lf\n", 5.2, 2, power(5.2, 2));  //实际参数
    return 0;
}

double power(double num1, int num2) // 形式参数
{
    double result = 1;
    int i;
    for (i = 0; i < num2; i++)
    {
        result *= num1; // 累乘
    }
    return result;
}
```
