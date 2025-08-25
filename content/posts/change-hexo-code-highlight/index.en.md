---
title: Modifying Hexo Theme Code Highlighting
summary: Hexo's default theme uses black code highlighting. Want a different style? This article explains how to modify Hexo theme code highlighting styles.
date: 2017-11-20
tags:
- Hexo
- Hexo
---

Hexo's default theme uses black code highlighting. Want a different style?  Here's how to do it:

```bash
# Modify the highlight.styl file, located at
themes/landscape/source/css/_partial/highlight.styl
```

Modify the default code theme to Tomorrow Night Eighties:

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

For the Tomorrow theme:

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

For more details, please refer to the [tomorrow-theme](https://github.com/chriskempson/tomorrow-theme) modifications.