---
title: GitHub Actions 还能这么玩？自动将发布的博客文章更新到 GitHub 个人主页
tags:
  - Actions
  - GitHub
categories:
  - DevOps
date: 2021-11-09 22:02:15
author: shenxianpeng
---

最近实现了一个很有意思的 Workflow，就是通过 GitHub Actions 自动将每次最新发布的文章自动同步到我的 GitHub 首页。

就像这样在首页显示最近发布的博客文章。

![最终效果](special-repository/final.png)

要实现这样的工作流需要了解以下这几点：

1. 需要创建一个与 GitHub 同名的个人仓库，这个仓库的 `README.md` 信息会显示在首页
2. 通过 GitHub Actions 自动获取博客的最新文章并更新 `README.md`
3. 只有当有新的文章发布的时候才触发自动获取、更新文章 GitHub Action

<!-- more -->

GitHub 同名的个人仓库是一个特殊仓库，即创建一个与你的 GitHub 账号同名的仓库，添加的 `README.md` 会在 GitHub 个人主页显示。

举个例子：如果你的 GitHub 名叫 `GeBiLaoWang`，那么当你创建一个叫 `GeBiLaoWang` 的 Git 仓库，添加 README.md 后就会在主页显示。

针对这个功能 GitHub 上有很多丰富多彩的个人介绍（如下）。更多灵感可以参看这个链接：https://awesomegithubprofile.tech/

![profile](special-repository/profile.png)

## 自动获取文章并更新 `README.md`

在 GitHub 上有很多开发者为 GitHub Actions 开发新的小功能。我这里用到一个开源项目叫 [blog-post-workflow](https://github.com/gautamkrishnar/blog-post-workflow)，它可以通过 RSS（订阅源）来获取到博客的最新文章。

它不但支持 RSS 还支持获取 StackOverflow 以及 Youtube 视频等资源。

我只需要在 GitHub 同名的仓库下添加一个这样的 Workflow YML `.github/workflows/blog-post-workflow.yml` 即可。

```yml
name: Latest blog post workflow
on:
  schedule:
    - cron: '* 2 * * *'
  workflow_dispatch:

jobs:
  update-readme-with-blog:
    name: Update this repo's README with latest blog posts
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: gautamkrishnar/blog-post-workflow@master
        with:
          # 我的博客 RSS 链接
          feed_list: "https://shenxianpeng.github.io/atom.xml"
          # 获取最新 10 篇文章
          max_post_count: 10
```

刚开始我需要让这个 Workflow 能工作即可。因此用的定时触发，即就是每天早上两点就自动获取一次最新文章并更新这个特殊仓库 `README.md`。

这个做法还可以，但不够节省资源也不够完美。最好的做法是：只有当有新文章发布时才触发上面的 Workflow 更新 `README.md`。这就需要有一个 Webhook 当检测到有文章更新时自动触发这里的 Workflow。

## 触发另一个 GitHub Action

GitHub Actions 提供了一个 Webhook 事件叫做 [`repository_dispatch`](https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows#repository_dispatch) 可以来做这件事。

它的原理：使用 GitHub API 来触发一个 Webhook 事件，这个事件叫做 `repository_dispatch`，这个事件里的类型是可以自定义的，并且在要被触发的 workflow 里需要使用 `repository_dispatch` 事件。

即：在存放博客文章的仓库里要有一个 Workflow 通过发送 `repository_dispatch` 事件触发特殊仓库中的 Workflow 来更新 `README.md`。

这里我定义事件类型名叫 `special_repository`，它只接受来自 GitHub API `repository_dispatch` 事件。

再次调整上面的 `.github/workflows/blog-post-workflow.yml` 文件如下：

```yml
# special_repository.yml
name: Latest blog post workflow

on:
  repository_dispatch:
    # 这里的类型是可以自定义的，我将它起名为：special_repository
    types: [special_repository]
  workflow_dispatch:

jobs:
  update-readme-with-blog:
    name: Update this repo's README with latest blog posts
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: gautamkrishnar/blog-post-workflow@master
        with:
          feed_list: "https://shenxianpeng.github.io/atom.xml"
          max_post_count: 10
```

接受事件的 Workflow 修改好了。如何发送类型为 `special_repository` 的 `repository_dispatch` 事件呢？我这里通过 `curl` 直接调用 API 来完成。

```bash
curl -XPOST -u "${{ secrets.PAT_USERNAME}}:${{secrets.PAT_TOKEN}}" \
    -H "Accept: application/vnd.github.everest-preview+json" \
    -H "Content-Type: application/json" https://api.github.com/repos/shenxianpeng/shenxianpeng/dispatches \
    --data '{"event_type": "special_repository"}'
```

最后，发送事件 Workflow YML `.github/workflows/send-dispatch.yml` 如下:

```yml
name: Tigger special repository

on:
  push:
    # 当 master 分支有变更的时候触发 workflow
    branches:
      - master
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Send repository dispatch event
        run: |
          curl -XPOST -u "${{ secrets.PAT_USERNAME}}:${{secrets.PAT_TOKEN}}" \
          -H "Accept: application/vnd.github.everest-preview+json" \
          -H "Content-Type: application/json" https://api.github.com/repos/shenxianpeng/shenxianpeng/dispatches \
          --data '{"event_type": "special_repository"}'
```

注：`PAT_USERNAME` 和 `PAT_TOKEN` 需要在当前的仓库【设置 -> Secrets】里进行添加，这里就不具体介绍了，需要可以自行搜索。

![设置 PAT](special-repository/secrets.png)

以上就是通过 GitHub Actions 实现当博客有新发布的文章后自动更新 GitHub 首页的所有内容了。

如果还有什么有意思的玩法欢迎评论区里分享一下吧。
