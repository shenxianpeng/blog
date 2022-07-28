# Peter Shen's Blog

![Build](https://github.com/shenxianpeng/blog/workflows/build/badge.svg?branch=master)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/5067/badge)](https://bestpractices.coreinfrastructure.org/projects/5067)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=shenxianpeng_blog&metric=alert_status)](https://sonarcloud.io/dashboard?id=shenxianpeng_blog)
[![CodeQL](https://github.com/shenxianpeng/blog/workflows/CodeQL/badge.svg)](https://github.com/shenxianpeng/blog/actions?query=workflow%3ACodeQL)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/c11eed2252634f68a4a4f62a5e069fa6)](https://www.codacy.com/gh/shenxianpeng/blog/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=shenxianpeng/blog&amp;utm_campaign=Badge_Grade)
![Website](https://img.shields.io/website?url=https%3A%2F%2Fshenxianpeng.github.io%2F)

微信公众号「DevOps攻城狮」- 专注于分享CI/CD、DevOps领域知识。

![欢迎扫码关注](source/about/index/qrcode.jpg)

Share knowledge in the fields of CI/CD and DevOps. Blog URL: https://shenxianpeng.github.io

If you find any mistakes or questions, please feel free to ask via [issues](https://github.com/shenxianpeng/blog/issues).

## Start web with Docker

```bash
git clone https://github.com/shenxianpeng/blog.git
cd blog
docker-compose up
```

## Start web on host

### Installation

```bash
git clone https://github.com/shenxianpeng/blog.git
cd blog
npm install                                 # Install dependencies
npm install -g hexo-cli                     # Install hexo cli
npm install hexo-deployer-git --save        # Install hexo deploy
```

### Build and run

```bash
make server     # Start server
make help       # Help for make
```

## Create and publish new post

Posts are saved by folder, with the hierarchy of year/month.

Creating an post with following steps:

1. Running command `hexo new "post"` can generate `post.md` under `source/_drafts`
2. Then update `post.md`, and fields such as `tags`, `categories` or `author`
3. Once it's ready to post, move `post.md` to `source/_post/2022/01/` and run `hexo s` to see how it looks like

If some all look good, run this following command to publish 🚀

```bash
make publish
```

A new commit will be pushed to the blog static files [repository](https://github.com/shenxianpeng/shenxianpeng.github.io)

## Format tools

Format tools for publishing to other medium platforms

* [Convert to Markdown](http://blog.didispace.com/tools/online-markdown/)
* [Markdown Nice](https://www.mdnice.com/)

## Licenses

[GPL-3.0](https://github.com/shenxianpeng/blog/blob/master/LICENSE) © [Hexo](https://hexo.io)

[署名-非商业性使用-相同方式共享 3.0 中国大陆 (CC BY-NC-SA 3.0 CN)](https://creativecommons.org/licenses/by-nc-sa/3.0/cn/deed.zh)

[Attribution-NonCommercial-ShareAlike 3.0 China Mainland (CC BY-NC-SA 3.0 CN)](https://creativecommons.org/licenses/by-nc-sa/3.0/cn/deed.en)

![Blog views](https://gpvc.arturio.dev/blog)
[![Netlify Status](https://api.netlify.com/api/v1/badges/93d6583c-4dfd-4e07-a606-1d0108eb39fe/deploy-status)](https://app.netlify.com/sites/shenxianpeng-blog/deploys)
