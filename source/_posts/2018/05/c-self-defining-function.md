---
title: C-Language 自定义函数
date: 2018-05-15 09:49:34
tags:
    - C
categories:
    - Language
author: shenxianpeng
---
求次幂函数power

```c
#include <stdio.h>

<!-- more -->
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
