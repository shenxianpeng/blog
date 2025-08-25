---
title: Hexo Configuration and Usage
summary: This article introduces how to configure the RSS subscription function in a Hexo blog, including plugin installation and usage.
date: 2017-10-25
tags:
- Hexo
- Blog
categories:
- Hexo
---

## Configuring RSS Subscription in Hexo

Install the [hexo-generator-feed](https://github.com/hexojs/hexo-generator-feed) plugin

```bash
npm install hexo-generator-feed --save
```

If the npm installation is unsuccessful in China, you can install [cnpm](https://npm.taobao.org/) first.

```bash
npm install -g cnpm --registry=https://registry.npm.taobao.org
```

Then

```bash
cnpm install hexo-generator-feed --save
```

Configure this plugin in `_config.yml`

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

## Inserting Images into Hexo Blog Posts

How do you insert images into a Hexo post?

It's easy to find the Markdown syntax online: `![Alt text](/path/to/img.jpg)`.  "Alt text" refers to the caption below the image, and the following is the image's address. So how do you configure this?


After several attempts, I found that: In the root directory of your Hexo project, create an `images` folder under `source`, and put all the images you will use in this directory.

```bash
![Example Image 1](../images/color.png)
```