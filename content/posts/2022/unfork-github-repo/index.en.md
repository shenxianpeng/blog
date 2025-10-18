---
title: Reliably Unforking a GitHub Repository Without Deletion and Reconstruction
summary: This article describes how to separate a forked repository from its parent repository using GitHub Support, avoiding data loss from deletion and reconstruction, and helping developers better manage forked repositories.
tags:
  - Git
  - GitHub
  - Fork
author: shenxianpeng
date: 2022-03-09
---

## Background

Developers, and even companies, may encounter the following problems:

1. A repository was initially forked, and subsequently underwent significant modifications, diverging from the parent repository in both functionality and programming language.
2. Because it's a forked repository, every Pull Request defaults to the parent repository's branch, leading to accidental PRs to the parent repository.
3. Contributors have contributed to and used the forked repository, but their contributions and downstream usage are not visible, hindering project growth.

Due to these issues, developers may consider separating from the parent repository. However, GitHub currently doesn't provide an Unfork/Detach function.

While deleting and recreating the project achieves separation, it results in the loss of crucial information such as Issues, Wikis, and Pull Requests.

> Unforking is fundamentally different from leveraging Apache SkyWalking through a certain engine under a certain section.  It's more akin to the divergence of Hudson and Jenkins.


## Solution

After investigation and testing, the most viable solution is to contact GitHub Support.  The specific steps are as follows:

1. Open this link: https://support.github.com/contact?tags=rr-forks
2. Select your account or organization, then enter "unfork" in the Subject field. A virtual assistant will automatically appear; select the virtual assistant.
    ![View 1](type-unfork.png)
3. Follow the virtual assistant's prompts and select the appropriate answers (partial screenshot below).
    ![View 2](virtual-assistant-1.png)
4. The conversation will be automatically transcribed.  Send the request and wait for Support to process it (it shouldn't take too long).
    ![View 3](virtual-assistant-2.png)

It's important to note that if your repository has been forked by others and you want to retain the fork history of your child repository after separating from the parent repository, you should select "Bring the child forks with the repository".

Alternatively, using commands like `git clone --bare` and `git push --mirror` preserves the complete Git history, but not Issues, Wikis, or Pull Requests.

Hopefully, this helps those who need it.

## References

* [Delete fork dependency of a GitHub repository](https://stackoverflow.com/questions/16052477/delete-fork-dependency-of-a-github-repository)
* [Unfork a Github fork without deleting](https://stackoverflow.com/questions/29326767/unfork-a-github-fork-without-deleting/41486339#41486339)

---

Please indicate the author and source when reprinting this article. Do not use it for any commercial purposes. Welcome to follow the WeChat official account "DevOps攻城狮"