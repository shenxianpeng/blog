---
title: Hexo 配置 rss 订阅功能
summary: 本文介绍如何在 Hexo 博客中配置 RSS 订阅功能，包括安装插件和配置文件。
date: 2017-10-25
tags:
- Hexo
- Blog
ategories:
- Hexo
---

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
