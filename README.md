# Peter Shen's Blog

微信公众号「DevOps攻城狮」- 持续分享CI/CD、DevOps领域内容。

![欢迎扫码关注](source\about\index\qrcode.jpg)

Share knowledge in the fields of CI/CD and DevOps. Blog URL: https://shenxianpeng.github.io

If you find any mistakes or questions, please feel free to ask via [issues](https://github.com/shenxianpeng/blog/issues).

![Build](https://github.com/shenxianpeng/blog/workflows/build/badge.svg?branch=master)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/5067/badge)](https://bestpractices.coreinfrastructure.org/projects/5067)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=shenxianpeng_blog&metric=alert_status)](https://sonarcloud.io/dashboard?id=shenxianpeng_blog)
[![CodeQL](https://github.com/shenxianpeng/blog/workflows/CodeQL/badge.svg)](https://github.com/shenxianpeng/blog/actions?query=workflow%3ACodeQL)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/c11eed2252634f68a4a4f62a5e069fa6)](https://www.codacy.com/gh/shenxianpeng/blog/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=shenxianpeng/blog&amp;utm_campaign=Badge_Grade)
![Website](https://img.shields.io/website?url=https%3A%2F%2Fshenxianpeng.github.io%2F)

## :cloud: Installation

```bash
git clone https://github.com/shenxianpeng/blog.git
cd blog
npm install                                 # Install dependencies
npm install -g hexo-cli                     # Install hexo cli
npm install hexo-deployer-git --save        # Install hexo deploy
```

## :clipboard: Commands

```bash
hexo server                                 # Start the local server. by default is http://localhost:4000/
hexo new "My New Post"                      # Create a new article
hexo new page "About"                       # Create a new page named About
hexo clean                                  # Cleans the cache file (db.json) and generate files (public)
hexo generate                               # Generate static files
hexo deploy                                 # Deploy your website

hexo generate -deploy                       # Generate then deploy
hexo g -d                                   # Abbreviations generate then deploy
```

## :memo: Article structure

Articles are saved by folder, with the hierarchy of year/month.

Follow the following steps when creating an article, for example: `abc.md` in August 2019.

1. use command `hexo new "abc"` to generate `abc.md`
2. manually create `2021/05/` under `source/_post` folder
3. move `abc.md` to `source/_post/2021/05/`
4. update `tags`, `categories` and `author` fields in `abc.md` file
5. start writing ... I always use `hexo s` to see how it looks

> Any unfished articles need to be moved to `todo` folder. When it's done, move to `source/_post/...` for publishing.

## 🚀 Deploy

Automatically update new commits to web site [repository](https://github.com/shenxianpeng/shenxianpeng.github.io) by following command.

```bash
sh deploy.sh
```

## 🧰 Format tools

Format tools for publishing to other medium platforms

* [Convert to Markdown](http://blog.didispace.com/tools/online-markdown/)
* [Markdown Nice](https://www.mdnice.com/)

## 📜 Licenses

[GPL-3.0](https://github.com/shenxianpeng/blog/blob/master/LICENSE) © [Hexo](https://hexo.io)

[署名-非商业性使用-相同方式共享 3.0 中国大陆 (CC BY-NC-SA 3.0 CN)](https://creativecommons.org/licenses/by-nc-sa/3.0/cn/deed.zh)

[Attribution-NonCommercial-ShareAlike 3.0 China Mainland (CC BY-NC-SA 3.0 CN)](https://creativecommons.org/licenses/by-nc-sa/3.0/cn/deed.en)

![Blog views](https://gpvc.arturio.dev/blog)
