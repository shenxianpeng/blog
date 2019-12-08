# Blog

[![Build Status](https://www.travis-ci.org/shenxianpeng/blog.svg?branch=master)](https://www.travis-ci.org/shenxianpeng/blog) ![GitHub commit activity](https://img.shields.io/github/commit-activity/y/shenxianpeng/blog) ![Website](https://img.shields.io/website?url=https%3A%2F%2Fshenxianpeng.github.io%2F)

## This is my [blog](https://shenxianpeng.github.io/) code used [hexo](https://hexo.io)

## Prepare ENV

```bash
git clone https://github.com/shenxianpeng/blog.git

cd blog
npm install                                 # Install dependencies
npm install -g hexo-cli                     # Install cmd command
npm install hexo-deployer-git --save        # Install deploy
```

## 📖 Hexo Commands

```bash
hexo server                                 # Start local server. by default is http://localhost:4000/
hexo new "My New Post"                      # Create new article
hexo new page "About"                       # Create new page named About
hexo clean                                  # Cleans the cache file (db.json) and generate files (public)
hexo generate                               # Generate static files
hexo deploy                                 # Deploy your website

hexo generate -deplogy                      # Generate then deploy
hexo g -d                                   # Abbreviations generate then deploy
```

## Contribute new article

Articles are stored according to folder, with the hierarchy of year/month. For example, article folder like '2019/08/jenkins-multi-branch-pipeline.md'.

## Post to WeChat public account

Before post this blog articles to WeChat public account should convert to markdown format first.

Here is [convert to markdown](http://blog.didispace.com/tools/online-markdown/) web tool for use.
