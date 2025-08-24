---
title: Hexo 的配置和使用
summary: 本文介绍如何在 Hexo 博客中配置 RSS 订阅功能，包括安装插件和使用。
date: 2017-10-25
tags:
- Hexo
- Blog
categories:
- Hexo
---

## Hexo 配置 rss 订阅功能

安装 [hexo-generator-feed](https://github.com/hexojs/hexo-generator-feed) 插件

```bash
npm install hexo-generator-feed --save

```

如果国内 npm 安装不成功，可以先安装 [cnpm](https://npm.taobao.org/)

```bash
npm install -g cnpm --registry=https://registry.npm.taobao.org
```

然后再

```bash
cnpm install hexo-generator-feed --save
```

在 _config.yml 中配置这个插件

```bash
feed:
  type: atom
  path: atom.xml
  limit: 20
  hub:
  content:
  content_limit: 140
  content_limit_delim: ' '
```

## Hexo 博客文章中插入图片

如果想在 Hexo 文章中插入图片怎么做？

网络上很容易搜到 Markdown 的语法是 `![Alt text](/path/to/img.jpg)`
前面 Alt text 是指在图片下面命名，后面是图片的地址。那么如何配置？


经过几番尝试得知：在你的 hexo 项目根目录下面 source 创建一个 images 文件夹，
把你以后用的到图片都放在这个目录下面就 OK 了。

```bash
![示例图1](../images/color.png)
```
