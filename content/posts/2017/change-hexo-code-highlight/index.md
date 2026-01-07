---
title: 修改 Hexo 主题代码高亮
summary: Hexo 默认主题代码高亮是黑色的，如果想换个风格？本文介绍如何修改 Hexo 主题代码高亮样式。
date: 2017-11-20
aliases:
  - /2017/11/change-hexo-code-highlight/
tags:
- Hexo
- Hexo
---

Hexo 默认主题代码高亮是黑色的，如果想换个风格？具体操作如下：

```bash
# 修改 highlight.styl 文件，路径
themes/landscape/source/css/_partial/highlight.styl

```

修改默认代码主题 Tomorrow Night Eighties

```js
highlight-background = #2d2d2d
highlight-current-line = #393939
highlight-selection = #515151
highlight-foreground = #cccccc
highlight-comment = #999999
highlight-red = #f2777a
highlight-orange = #f99157
highlight-yellow = #ffcc66
highlight-green = #99cc99
highlight-aqua = #66cccc
highlight-blue = #6699cc
highlight-purple = #cc99cc
```

为主题 Tomorrow

```js
highlight-background = #ffffff
highlight-current-line = #efefef
highlight-selection = #d6d6d6
highlight-foreground = #4d4d4c
highlight-comment = #8e908c
highlight-red = #c82829
highlight-orange = #f5871f
highlight-yellow = #eab700
highlight-green = #718c00
highlight-aqua = #3e999f
highlight-blue = #4271ae
highlight-purple = #8959a8
```

更多详情请参考 [tomorrow-theme](https://github.com/chriskempson/tomorrow-theme) 修改。
