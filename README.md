# Peter Shen's Blog

Share knowledge in the fields of CI/CD and DevOps. Blog URL: https://shenxianpeng.github.io

If you have any questions or mistakes, please feel free to ask via [Issues](https://github.com/shenxianpeng/blog/issues), and to receive updates as soon as possible welcome to [Star](https://github.com/shenxianpeng/blog).

![Build](https://github.com/shenxianpeng/blog/workflows/build/badge.svg?branch=master)
[![CodeQL](https://github.com/shenxianpeng/blog/workflows/CodeQL/badge.svg)](https://github.com/shenxianpeng/blog/actions?query=workflow%3ACodeQL)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=shenxianpeng_blog&metric=alert_status)](https://sonarcloud.io/dashboard?id=shenxianpeng_blog)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/c11eed2252634f68a4a4f62a5e069fa6)](https://www.codacy.com/gh/shenxianpeng/blog/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=shenxianpeng/blog&amp;utm_campaign=Badge_Grade)
![Website](https://img.shields.io/website?url=https%3A%2F%2Fshenxianpeng.github.io%2F) ![Blog views](https://gpvc.arturio.dev/blog)

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

## :memo: Article Structure

Articles are saved by folder, with the hierarchy of year/month.

Follow the following steps when creating an article, for example: `abc.md` in August 2019.

1. use command `hexo new "abc"` to generate `abc.md`
2. manually create `2021/05/` under `source/_post` folder
3. move `abc.md` to `source/_post/2021/05/`
4. update `tags`, `categories` and `author` fields in `abc.md` file
5. start writing ... I always use `hexo s` to see how it looks

> Any unfished articles need to be moved to `todo` folder. When it's done, move to `source/_post/...` for publishing.

## 🚀 Deploy

Use below command will automatically update the new article to web site [repository](https://github.com/shenxianpeng/shenxianpeng.github.io).

```bash
sh deploy.sh
```

## 🧰 Format Tools

Format tools for publishing to other medium platforms

* [Convert to Markdown](http://blog.didispace.com/tools/online-markdown/)
* [Markdown Nice](https://www.mdnice.com/)

## 📜 License

[GPL-3.0](https://github.com/shenxianpeng/blog/blob/master/LICENSE) © [Hexo](https://hexo.io)
