---
title: Git 管理
date: 2019-07-07 17:55:18
tags:
- Git
categories: 
- Git
---

## 查找是否有遗漏提交

从一个分支找到所有的 commit 和 ticket 号，然后去另外一个分支去查找这些提交是否也在这个分支里。

找一个分支的所有 commit 和 ticket 号

```bash
# 从 develop 分支上获取所有的 commit 和 ticket 号，然后根据 ticket 号进行排序
git log origin/develop --pretty=oneline --abbrev-commit | cut -d' ' -f2,1 | sort -t ' ' -k 2 >> develop_involve_tickets.txt

--pretty=oneline    # 显示为一行
--abbrev-commit     # 显示短的提交号

cut --help          # 切出来所需要的字段
-d                  # 字段分隔符, ' '分隔空格
-f                  # 只选择某些字段

sort --help         # 利用 sort 将剪出来的字段进行排序
-t                  # 字段分隔， ' '分隔空格
-k                  # 通过键进行键定义排序;KEYDEF 给出位置和类型
```

然后去另外一个分支去找是否有次提交

由于在 SVN 时代时，每次修改都会在描述里添加 ticket 号，所以切换到 master 分支后，直接搜索所有 ticket 号是否存在就好了.

```bash
#!/bin/bash

filename='C:\develop_involve_tickets.txt'
while read line
do
    echo $line
    var=`grep -ir $line src`
    if [[ -z $var ]];then
        echo "not found"
        echo $line >> ../not_found_in_master.txt
    else
        echo "found"
        echo $line >> ../found_in_master.txt
    fi
done < "$filename"
```
