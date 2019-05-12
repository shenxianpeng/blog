---
title: C-print
date: 2018-07-08 21:53:01
tags: 
- dev
- C
---

如何打印下面的字符？
```
$
##
$$$
###
$$$
##
$
```
示例1：
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