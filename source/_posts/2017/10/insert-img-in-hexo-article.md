---
title: Hexo 博客文章中插入图片
date: 2017-10-25 17:07:11
tags:
- Hexo
categories:
- Hexo
---

如果想在 Hexo 文章中插入图片怎么做？

网络上很容易搜到 Markdown 的语法是 `![Alt text](/path/to/img.jpg)`
前面 Alt text 是指在图片下面命名，后面是图片的地址。那么如何配置？

<!-- more -->
经过几番尝试得知：在你的 hexo 项目根目录下面 source 创建一个 images 文件夹，
把你以后用的到图片都放在这个目录下面就 OK 了。

```bash
![示例图1](../images/color.png)
```
