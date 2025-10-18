---
title: Resolving the "Could not read from remote repository" Issue
summary: |
  Resolving the "Could not read from remote repository" error encountered when cloning code using Git, analyzing the causes, and providing solutions.
tags:
  - Git
  - Troubleshooting
date: 2019-09-01
author: shenxianpeng
---

Recently, while running a Jenkins Job, I encountered this error during a git clone operation:

```bash
$ git clone ssh://git@git.companyname.com:7999/repo/opensrc.git
Cloning into 'opensrc'...
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

I only encountered this error when I first started using Git, back when I didn't know how to clone code using SSH.  Why did this error appear now? I haven't changed anything, which is very confusing.

## Common Solutions



My Google searches didn't yield a solution for my specific problem. Most results suggested that the issue was due to not having generated an SSH key, and that generating one and adding the public key to GitHub or another web Git management platform would solve the problem.  Using GitHub as an example:

First, generate an SSH key:

```bash
# Remember to replace with your own email address
ssh-keygen -t rsa -C xianpeng.shen@gmail.com
```

Second, copy the SSH public key to your Git web platform, such as GitHub.

```bash
cd %userprofile%/.ssh
# Open id_rsa.pub and copy its contents
notepad id_rsa.pub
```

Finally, open <https://github.com/settings/ssh/new> and paste the copied content there to save it.

This solution was ineffective for my problem, because the same account worked without issue on other virtual machines. Since it was also an HP-UX virtual machine, I generated an SSH key using a different account and the git clone operation worked perfectly. This led me to suspect a difference between the two accounts.

## Troubleshooting via SSH Connection Test

First, I examined the `.gitconfig` files for both accounts and found differences. Copying the contents of the `.gitconfig` file from the working account to the problematic one didn't resolve the issue.

Second, I noticed that a core file was generated in the current directory during the `git clone` execution, indicating a coredump. However, opening the core file mostly resulted in gibberish, making it difficult to pinpoint the error.

Finally, I tested the SSH connection using commands. For GitHub, the command is:

```bash
ssh -T git@github.com
```

My problematic clone was using Bitbucket, and its SSH connection test command is:

```bash
ssh -vvv git\@bitbucket.org
```

First, I tested with the account that successfully performed `git clone`. I'm omitting some of the output here for brevity.

```bash
$ ssh -vvv git\@bitbucket.org
OpenSSH_6.2p1+sftpfilecontrol-v1.3-hpn13v12, OpenSSL 0.9.8y 5 Feb 2013      # Different OpenSSH version
HP-UX Secure Shell-A.06.20.006, HP-UX Secure Shell version                  # Different call path
debug1: Reading configuration data /opt/ssh/etc/ssh_config
debug3: RNG is ready, skipping seeding
debug2: ssh_connect: needpriv 0
debug1: Connecting to bitbucket.org [18.205.93.1] port 22.
debug1: Connection established.

... ...

debug2: we did not send a packet, disable method
debug1: No more authentication methods to try.
Permission denied (publickey).
```

Then, I tested with the account that failed the `git clone` operation:

```bash
$ ssh -vvv git\@bitbucket.org
OpenSSH_8.0p1, OpenSSL 1.0.2s  28 May 2019                                  # Different OpenSSH version
debug1: Reading configuration data /usr/local/etc/ssh_config                # Different call path
debug2: resolving "bitbucket.org" port 22
debug2: ssh_connect_direct
debug1: Connecting to bitbucket.org [180.205.93.10] port 22.
debug1: Connection established.
Memory fault(coredump)
$
```

Clearly, different versions of OpenSSH were used, indicating differences in their environment variables. I had previously checked the environment variables, but the large number of variables made it difficult to immediately identify the culprit.

## Final Solution

I revisited the `.profile` file for the account where the `git clone` failed.  There was an extra `/usr/bin` entry in the environment variables, causing this account to use a different version of OpenSSH.  HP-UX has very strict requirements on package dependencies and versions. After removing this environment variable, saving the changes, logging back into the virtual machine, and executing `git clone`, the operation returned to normal.