---
title: Git管理
date: 2019-07-07 17:55:18
tags: [Git, Shell]
categories: Git
---

# Git管理 - 查找是否有遗漏提交

从一个分支找到所有的commit和ticket号，然后去另外一个分支去查找这些提交是否也在这个分支里。

1. 找一个分支的所有commit和ticket号
```
# 从develop分支上获取所有的commit和ticket号，然后根据ticket号进行排序
git log origin/develop --pretty=oneline --abbrev-commit | cut -d' ' -f2,1 | sort -t ' ' -k 2 >> develop_involve_tickets.txt

--pretty=oneline    # 显示为一行
--abbrev-commit     # 显示短的提交号

cut --help          # 切出来所需要的字段 
-d                  # 字段分隔符, ' '分隔空格
-f                  # 只选择某些字段

sort --help         # 利用sort将剪出来的字段进行排序
-t                  # 字段分隔， ' '分隔空格
-k                  # 通过键进行键定义排序;KEYDEF给出位置和类型
```

 2. 然后去另外一个分支去找是否有次提交

* 由于在SVN时代时，每次修改都会在描述里添加ticket号，所以切换到master分支后，直接搜索所有ticket号是否存在就好了。
```
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




 