---
title: 在不删除和重建 GitHub 仓库的情况下如何跟 Fork 的父仓库分离
tags:
  - Git
  - GitHub
  - Fork
categories:
  - Git
author: shenxianpeng
date: 2022-03-09 11:16:05
---

## 背景

有开发者可能会遇到过以下四个问题：

1. 最开始 Fork 了一个仓库，之后做了大量的修改，从功能到开发语言，已经与父仓库分道扬镳了
2. 由于是 Fork 的仓库，在每次提 Pull Request 的默认目标分支是父仓库，经常会一不注意就会提 PR 到父仓库里去了
3. Fork 的仓库中不能显示贡献者以及数量，还有该项目被哪些其他的项目所使用

因此开发者会考虑与父仓库进行分离，但目前 GitHub 没有直接提供 Unfork/Detach 的功能。

如果直接删除项目并重建可以达到分离的目的，但这样会丢失一些重要的信息，比如项目中的 Issues，Wikis 以及 Pull Requests 等。

## 解决办法

在经过一番调查和测试，目前最可行的办法就是通过 GitHub Support 来处理。具体操作如下：

1. 打开这个连接：https://support.github.com/contact?tags=rr-forks
2. 选择账户或是组织，然后在 Subject 中输入 "unfork"，会自动弹出虚拟助手，点击按钮
    ![](unfork-github-repo/type-unfork.png)
3. 然后根据虚拟助手的问题进行答案的选择（如下是部分截图）
     ![](unfork-github-repo/virtual-assistant-1.png)
4. 最后这些对话会自动转换成文字脚本，然后 Send request，之后就等着 Support 处理就可以了。
    ![](unfork-github-repo/virtual-assistant-2.png)

注意：如果你的仓库被其他人 Fork 了，你想跟父仓库分离之后继续保留你的子仓库记录，你应该选择 "Bring the child forks with the repository"。

另外，通过其他方式，比如命令 `git clone --bare` 和 `git push --mirror`，这可以保留完成的 Git 历史，但不能保留 Issues，Wikis 以及 Pull Requests 等信息。

## 参考

* [Delete fork dependency of a GitHub repository](https://stackoverflow.com/questions/16052477/delete-fork-dependency-of-a-github-repository)
* [Unfork a Github fork without deleting](https://stackoverflow.com/questions/29326767/unfork-a-github-fork-without-deleting/41486339#41486339)

---

![ ](https://github.com/shenxianpeng/shenxianpeng.github.io/blob/master/about/index/qrcode.jpg?raw=true)

关注公众号「DevOps攻城狮」（转载本站文章请注明作者和出处，请勿用于任何商业用途）
