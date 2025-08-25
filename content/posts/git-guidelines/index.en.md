---
title: Git Common Settings Guide
summary: This article introduces some common settings needed before submitting code using Git, including configuring username and email, handling line endings, writing standardized commit messages, etc., to help developers better manage code versions.
tags:
  - Git
date: 2021-05-14
author: shenxianpeng
---

It's recommended to make the following settings before submitting code using Git.

Calling this a guide might be a bit exaggerated, as it's not applicable in some cases, such as when you already have files like `.gitattributes` or `.editorconfig`, in which case some of these settings are unnecessary.

Therefore, let's call it a compass instead; it's still very useful in most cases.

Without further ado, let's see what settings are needed.


## 1. Configure name and email

```bash
# Note: You need to replace my name and email in the example below with your own
$ git config --global user.name "shenxianpeng"
$ git config --global user.email "xianpeng.shen@gmail.com"

```

Additionally, I recommend setting an avatar for easy identification among colleagues.

Without an avatar, you only know who the Pull Request Reviewers are by hovering over their placeholder (from Bitbucket).

![Bitbucket avatar](avatar.png)

## 2. Set core.autocrlf=false

To prevent issues with CRLF (Windows) and LF (UNIX/Linux/Mac) line endings. To avoid obscuring history when submitting code using Git, it is strongly recommended that every Git user executes the following command:

```bash
$ git config --global core.autocrlf false
# Check and see if "core.autocrlf=false" is output, which means the command was set successfully.
$ git config --list
```

If your project already has `.gitattributes` or `.editorconfig` files, these files usually contain settings for handling CRLF and LF conversion issues.

In this case, you don't need to specifically execute the command `git config --global core.autocrlf false`.

## 3. Write standardized commit messages

I've shared in a previous article about how to set commit message standards, please refer to [《Git Commit Message and Branch Creation Specifications》](https://shenxianpeng.github.io/2020/09/commit-messages-specification/).

## 4. Compressing commit history

For example, if you fix a bug, let's say it took three commits on your personal branch to fix it.  When you submit a Pull Request, it will show three commits.

If the commit history is not compressed, after this PR is merged into the main branch, anyone viewing this bug fix in the future will have to go through these three commits one by one, comparing them to understand exactly what was changed.

Compressing commit history means combining three commits into one.

This can be done using the `git rebase` command. For example, to compress the last three commits into one:

```bash
git rebase -i HEAD~3
```

## 5. Delete merged branches

Some SCMs, such as Bitbucket, do not support the default selection of `Delete source branch after merging`. This issue was finally fixed in Bitbucket version 7.3. See [BSERV-9254](https://jira.atlassian.com/browse/BSERV-9254) and [BSERV-3272](https://jira.atlassian.com/browse/BSERV-3272) (created in 2013) for details.

Remember to select the option to delete the source branch when merging code; otherwise, a large number of development branches will remain in the Git repository.

---

If there are any other settings not mentioned here, feel free to add them.