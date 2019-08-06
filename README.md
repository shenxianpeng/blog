# Blog

[![Build Status](https://www.travis-ci.org/shenxianpeng/blog.svg?branch=master)](https://www.travis-ci.org/shenxianpeng/blog)

## This is my [blog](https://shenxianpeng.github.io/) code, use [hexo](https://hexo.io)

## Git Repository

```bash
git clone https://github.com/shenxianpeng/blog.git
```

## Prepare

```bash
npm install                                 # Install dependencies
npm install -g hexo-cli                     # Install cmd command
npm install hexo-deployer-git --save        # Install deploy
```

## Hexo Commands

```bash
hexo server                                 # Starts a local server. By default, this is at http://localhost:4000/
hexo new "My New Post"                      # Creates a new article
hexo new page "About"                       # Create a about page
hexo clean                                  # Cleans the cache file (db.json) and generated files (public).
hexo generate                               # Generates static files
hexo deploy                                 # Deploys your website

hexo generate -deplogy                      # Generate then deploy
hexo g -d                                   # Simple write this
```

## New article

Articles are stored according to folder, with the hierarchy of year/month. For example, article folder like' 2019/08/jenkins-multi-branch-pipeline.md'.

## Post to WeChat public account

[convert to markdown](http://blog.didispace.com/tools/online-markdown/)
