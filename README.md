# Blog

## This is my [blog](https://shenxianpeng.github.io/) code used [hexo](https://hexo.io)

[![Build Status](https://www.travis-ci.org/shenxianpeng/blog.svg?branch=master)](https://www.travis-ci.org/shenxianpeng/blog)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=shenxianpeng_blog&metric=alert_status)](https://sonarcloud.io/dashboard?id=shenxianpeng_blog)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2eff1062ed5c4971b06f33feb9696f88)](https://www.codacy.com/manual/xianpeng.shen/blog?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=shenxianpeng/blog&amp;utm_campaign=Badge_Grade)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/shenxianpeng/blog)
![Website](https://img.shields.io/website?url=https%3A%2F%2Fshenxianpeng.github.io%2F)

## :cloud: Installation

```bash
git clone https://github.com/shenxianpeng/blog.git && cd blog
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

Articles are stored according to folder, with the hierarchy of year/month. for example, when create a article `abc.md` in August 2019

1. use command `hexo new "abc"` to generate `abc.md`
2. manually create `2019/08/` under `source/_post` folder
3. move `abc.md` to `source/_post/2019/08/`

## :memo: Post to WeChat public account

Before post this articles to WeChat public account should convert to markdown format first. Here is web tool [convert to markdown](http://blog.didispace.com/tools/online-markdown/) for use.

## 📜 License

[GPL-3.0](https://github.com/shenxianpeng/blog/blob/master/LICENSE) © [Hexo](https://hexo.io)
