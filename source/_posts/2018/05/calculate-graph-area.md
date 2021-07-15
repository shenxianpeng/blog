---
title: C-Language 计算图形的面积
date: 2018-05-16 10:11:33
tags:
    - C
categories:
    - Language
author: shenxianpeng
---

```c
#include "stdafx.h"
#include <stdio.h>

/*
计算图形的面积：
1. 圆的面积 = π * radius * radius
2. 矩形面积 = weight * height
3. 三角形面积 = 1/2 * weight * height
@author Xianpeng Shen
*/

double calcCircle(double);
double calcSquare(double, double);
double calcTriangle(double, double);
int validate(double);

int main()
{
    int choice;                // 用户选择
    double area;               // 图形面积
    double radius;             // 圆半径
    double weight, height;     // 图形的宽和高
    printf("1. 圆\n2. 矩形\n3. 三角形\n");
    printf("本系统支持三种图形面积计算，请选择：");
    scanf_s("%d", &choice);
    while (choice > 3 || choice < 1) {
        printf("只能输入1~3整数，请重新输入：");
        scanf_s("%d", &choice);
    }

    switch (choice)
    {
    case 1:
        printf("请输入圆的半径：");
        do
        {
            scanf_s("%lf", &radius);
            if (!(validate(radius))) {
                printf("不能为负数，请重新输入一个整数：");
            }
        } while (!validate(radius));
        area = calcCircle(radius);
        break;
    case 2:
        printf("请输入矩形的长和宽：");
        do
        {
            scanf_s("%lf%lf", &weight, &height);
            if (!validate(weight) || !validate(height)) {
                printf("不能为负数，请重新输入两个正数：");
            }
        } while (!validate(weight) || !validate(height));
        area = calcSquare(weight, height);
        break;
    case 3:
        printf("请输入三角形的底和高：");
        do
        {
            scanf_s("%lf%lf", &weight, &height);
            if (!validate(weight) || !validate(height)) {
                printf("不能为负数，请重新输入两个正数：");
            }
        } while (!validate(weight) || !validate(height));
        area = calcTriangle(weight, height);
        break;
    default:
        printf("只能输入1~3整数，请重新输入：");
        break;
    }
    printf("图形面积为：%.2lf\n", area);
}

double calcCircle(double radius)
{
    return 3.14 * radius * radius;
}

double calcSquare(double weight, double height)
{
    return weight * height;
}

double calcTriangle(double weight, double height)
{
    return weight * height / 2;
}

int validate(double num)
{
    return num > 0;        // 如果 num>0, 返回一个非零值，表示真。
}
```
