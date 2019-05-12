[![Build Status](https://www.travis-ci.org/shenxianpeng/blog.svg?branch=master)](https://www.travis-ci.org/shenxianpeng/blog) 

### This is my [blog](https://shenxianpeng.github.io/) code, use [hexo](https://hexo.io).

## Git Repository
``` bash
$ git clone https://github.com/shenxianpeng/blog.git
```

## Prepare
``` bash
$ npm install                                   #Install dependencies
$ npm install -g hexo-cli                       #Install cmd command
$ npm install hexo-deployer-git --save          #Install deploy
```

## Quick Start

``` bash
$ hexo server                                   #Run server
$ hexo new "My New Post"                        #Create a new post
$ hexo new page "About"                         #Create a about page
$ hexo generate                                 #Generate static files
$ hexo deploy                                   #Deploy to remote sites
or
$ hexo generate -deplogy                        #Generate then deploy
or
$ hexo g -d                                     #Simple write this
```