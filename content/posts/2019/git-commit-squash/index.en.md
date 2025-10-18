---
title: Git Commit Squash
summary: |
  How to squash multiple Git commits into a single commit, both locally and remotely, using interactive rebase and merge strategies in Bitbucket.
tags:
  - Squash
  - Git
date: 2019-08-20
authors:
  - shenxianpeng
---

## If your commits on local not pushed to remote

### combine local commits, you could follow this flow


Here is [short video](https://www.youtube.com/watch?v=V5KrD7CmO4o) (only 3 minutes) and good explanation of `git rebase -i` usage.

list your local repository log

![list your logs in oneline](example-01.png)

If you want to combine these 3 commits (add6152, 3650100, 396a652) to 1 commit, execute this command

```bash
git rebase -i HEAD~3      # last three commits
```

![list last three commits](example-02.png)

Select which commit you want to squash (type s or squash are OK)

![combine three commits to one](example-03.png)

then press ESC, enter :wq! to save and exit.

![comment out some commits message you don't need](example-04.png)

Comment out some commits message you don't need, press ESC, enter :wq! to save and exit.

![comment out some commits message you don't need](example-05.png)

Check log, you will see your local repository logs has combine to one commit

![comment out some commits message you don't need](example-06.png)

## If your commits had pushed to remote

### combine remote commits, you could follow this flow

list your repository logs

![list your logs in oneline](example-07.png)

```bash
# so you can create another branch from bugfix/UNV-1234 named bugfix/UNV-1234-for-squash
xshen@dln-l-xs01 MINGW64 /c/U2GitCode/git-test (bugfix/UNV-1234)
$ git checkout -b bugfix/UNV-1234-for-squash
Switched to a new branch 'bugfix/UNV-1234-for-squash'

# combine last 2 commits
$ git rebase -i HEAD~2
```

change one commit from pick to squash, see the screenshot below. press ESC, enter :wq! to save and exit.

![select a commit you want to squash](example-08.png)

change commit message, for example "UNV-1234 combine all commit to one commit", then press ESC, enter :wq! to save and exit.

![comment out commit message you don't want to display](example-09.png)

```bash
# push your new create branch to remote.
git push -u origin bugfix/UNV-1234-for-squash
```
