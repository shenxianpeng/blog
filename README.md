# Blog

## This is my [blog](https://shenxianpeng.github.io/) code used [hexo](https://hexo.io)

![Build](https://github.com/shenxianpeng/blog/workflows/build/badge.svg?branch=master)
[![Build Status](https://travis-ci.org/shenxianpeng/blog.svg?branch=master)](https://travis-ci.org/shenxianpeng/blog)
[![CodeQL](https://github.com/shenxianpeng/blog/workflows/CodeQL/badge.svg)](https://github.com/shenxianpeng/blog/actions?query=workflow%3ACodeQL)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=shenxianpeng_blog&metric=alert_status)](https://sonarcloud.io/dashboard?id=shenxianpeng_blog)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2eff1062ed5c4971b06f33feb9696f88)](https://www.codacy.com/manual/xianpeng.shen/blog?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=shenxianpeng/blog&amp;utm_campaign=Badge_Grade)
![Website](https://img.shields.io/website?url=https%3A%2F%2Fshenxianpeng.github.io%2F)

## :cloud: Installation

```bash
git clone https://github.com/shenxianpeng/blog.git
cd blog
npm install                                 # Install dependencies
npm install -g hexo-cli                     # Install hexo cli
npm install hexo-deployer-git --save        # Install hexo deploy
```

## :clipboard: Example commands

```bash
hexo server                                 # Start local server. by default is http://localhost:4000/
hexo new "My New Post"                      # Create a new article
hexo new page "About"                       # Create a new page named About
hexo clean                                  # Cleans the cache file (db.json) and generate files (public)
hexo generate                               # Generate static files
hexo deploy                                 # Deploy your website

hexo generate -deploy                       # Generate then deploy
hexo g -d                                   # Abbreviations generate then deploy
```
## :memo: Article storage structure

Articles are saved by folder, with the hierarchy of year/month. 

I follow below steps when I create an article, for example `abc.md` in August 2019. 


1. use command `hexo new "abc"` to generate `abc.md`
2. manually create `2021/05/` under `source/_post` folder
3. move `abc.md` to `source/_post/2021/05/`
4. update `tags`, `categories` and `author` fields in `abc.md` file
5. start writing... I always use `hexo s` to see how it looks

> Any unfished posts need to be moved `todo` folder first. when done move to `source/_post/...` in published.

## 🚀 Auto deploy

Use below command will automatically update the new article to web site [repository](https://github.com/shenxianpeng/shenxianpeng.github.io).

```bash
sh deploy.sh
```


## 🧰 Format optimization tools

Before publishing the article to other sharing platforms, I need to optimize the format first.

* For WeChat: 
    * [Convert to Markdown](http://blog.didispace.com/tools/online-markdown/)
    * [Markdown Nice](https://www.mdnice.com/)
* For Medium: [markdown to medium](http://markdown-to-medium.surge.sh/)

## 📜 License

[GPL-3.0](https://github.com/shenxianpeng/blog/blob/master/LICENSE) © [Hexo](https://hexo.io)
