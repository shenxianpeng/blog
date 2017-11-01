---
title: Hexo博客文章中插入图片
date: 2017-10-25 17:07:11
tags: hexo
---

如果想在Hexo文章中插入图片怎么做？

网络上很容易搜到Markdown的语法是 `![Alt text](/path/to/img.jpg)`
前面Alt text是指在图片下面命名，后面是图片的地址。那么如何配置？

经过几番尝试得知：在你的hexo项目根目录下面source创建一个images文件夹，
把你以后用的到图片都放在这个目录下面就OK了。
<pre>
![示例图1](../images/color.png)
</pre>


