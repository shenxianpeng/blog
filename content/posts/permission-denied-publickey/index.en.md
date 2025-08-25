---
title: 'Error—Permission denied (publickey)'
summary: This article describes how to resolve the "Permission denied (publickey)" error when configuring multiple SSH Git keys, ensuring that SSH connections to GitHub and Bitbucket work correctly.
date: 2018-05-06
tags:
- Git
- Git
author: shenxianpeng
---

If you want to configure both GitHub and Bitbucket on one computer, how do you configure multiple SSH Git keys?
Generate SSH keys using the following command.  Note that it's best to enter new names during generation, such as `id_rsa_github` and `id_rsa_bitbucket`:

```bash
ssh-keygen -t rsa -C "your_email@youremail.com"
```

Then copy the contents of the generated SSH key file to the corresponding personal user settings on the website. However, even after following the official tutorial, I encountered the following problem when `git clone`ing:

Error: Permission denied (publickey)

This error plagued me for several days before I finally solved it.

[See this document](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/)

Because I'm using macOS Sierra 10.13.3, [this part of the document](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/#adding-your-ssh-key-to-the-ssh-agent) states that for macOS Sierra 10.12.2 and later, you need to create a `config` file in the `~/.ssh` directory.
The specific configuration of the `config` file is as follows:

```bash
Host *
 AddKeysToAgent yes
 UseKeychain yes
 IdentityFile ~/.ssh/id_rsa_github

Host *
 AddKeysToAgent yes
 UseKeychain yes
 IdentityFile ~/.ssh/id_rsa_bitbucket
```

After configuring this file, I tried again:

```bash
git clone git@github.com:shenxianpeng/blog.git
```

I was able to download the code, and both SSH Git keys worked! :)