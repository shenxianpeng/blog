---
title: C - Score Input Sort Show
date: 2018-05-17 14:42:48
tags: C
categories: Snippet
author: shenxianpeng
---
```C
#include "stdafx.h"
#include <stdio.h>
#define N 5
//Score Input Sort Show
void input(double[]);
void sortAsc(double[]);
void sortDesc(double[]);
void show(double[]);

int main()
{
    double scores[N];
    input(scores);

    printf("[SORT ASC]\n");
    sortAsc(scores);
    show(scores);

    printf("[SORT DESC]\n");
    sortDesc(scores);
    show(scores);

    return 0;
}

void input(double socres[])
{
    int i;
    for (i = 0; i < N; i++) {
        printf("Please enter %d student's score: ", i+1);
        scanf_s("%lf", &socres[i]);
    }
}

void sortAsc(double socres[])
{
    int i, j;
    double temp;
    for (i = 0; i < N - 1; i++)
    {
        {
            for (j = 0; j < N - i - 1; j++)
            {
                if (socres[j] > socres[j + 1])
                {
                    temp = socres[j];
                    socres[j] = socres[j + 1];
                    socres[j + 1] = temp;
                }
            }
        }
    }
}

void sortDesc(double socres[])
{
    int i, j;
    double temp;
    for (i = 0; i < N - 1; i++)
    {
        {
            for (j = 0; j < N - i - 1; j++)
            {
                if (socres[j] < socres[j + 1])
                {
                    temp = socres[j];
                    socres[j] = socres[j + 1];
                    socres[j + 1] = temp;
                }
            }
        }
    }
}

void show(double scores[])
{
    int i;
    printf("********************************************\n");
    printf("Chinese\tMath\tEnglish\tPhysics\tChemistry\t\n");

    for (i = 0; i< N; i++)
    {
        printf("%.2lf\t", scores[i]);
    }
    printf("\n********************************************\n");
}
```
