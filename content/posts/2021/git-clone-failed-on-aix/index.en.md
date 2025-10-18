---
title: Solving Two Git Clone Failure Issues on AIX
summary: This article documents two issues encountered when using Jenkins for Git clone on AIX and their solutions, including dependent library loading failure and SSH authentication failure.
tags:
  - Git
  - AIX
  - Jenkins
date: 2021-06-20
author: shenxianpeng
---

## Preface

This article documents two Git clone failure issues encountered during continuous integration with Jenkins and AIX, and shares their solutions.

1. Dependent module `/usr/lib/libldap.a(libldap-2.4.so.2)` could not be loaded.
2. Authentication failed during Git clone via SSH


## Issue 1: Dependent module `/usr/lib/libldap.a(libldap-2.4.so.2)` could not be loaded

When Jenkins checked out code via **HTTPS**, the following error occurred:

```bash
[2021-06-20T14:50:25.166Z] ERROR: Error cloning remote repo 'origin'
[2021-06-20T14:50:25.166Z] hudson.plugins.git.GitException: Command "git fetch --tags --force --progress --depth=1 -- https://git.company.com/scm/vas/db.git +refs/heads/*:refs/remotes/origin/*" returned status code 128:
[2021-06-20T14:50:25.166Z] stdout:
[2021-06-20T14:50:25.166Z] stderr: exec(): 0509-036 Cannot load program /opt/freeware/libexec64/git-core/git-remote-https because of the following errors:
[2021-06-20T14:50:25.166Z] 	0509-150   Dependent module /usr/lib/libldap.a(libldap-2.4.so.2) could not be loaded.
[2021-06-20T14:50:25.166Z] 	0509-153   File /usr/lib/libldap.a is not an archive or
[2021-06-20T14:50:25.166Z] 		   the file could not be read properly.
[2021-06-20T14:50:25.166Z] 	0509-026 System error: Cannot run a file that does not have a valid format.
[2021-06-20T14:50:25.166Z]
[2021-06-20T14:50:25.166Z] 	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl.launchCommandIn(CliGitAPIImpl.java:2450)
[2021-06-20T14:50:25.166Z] 	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl.launchCommandWithCredentials(CliGitAPIImpl.java:2051)
[2021-06-20T14:50:25.166Z] 	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl.access$500(CliGitAPIImpl.java:84)
[2021-06-20T14:50:25.167Z] 	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl$1.execute(CliGitAPIImpl.java:573)
[2021-06-20T14:50:25.167Z] 	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl$2.execute(CliGitAPIImpl.java:802)
[2021-06-20T14:50:25.167Z] 	at org.jenkinsci.plugins.gitclient.RemoteGitImpl$CommandInvocationHandler$GitCommandMasterToSlaveCallable.call(RemoteGitImpl.java:161)
[2021-06-20T14:50:25.167Z] 	at org.jenkinsci.plugins.gitclient.RemoteGitImpl$CommandInvocationHandler$GitCommandMasterToSlaveCallable.call(RemoteGitImpl.java:154)
..........................
[2021-06-20T14:50:25.167Z] 	Suppressed: hudson.remoting.Channel$CallSiteStackTrace: Remote call to aix-devasbld-01
[2021-06-20T14:50:25.167Z] 		at hudson.remoting.Channel.attachCallSiteStackTrace(Channel.java:1800)
..........................
[2021-06-20T14:50:25.168Z] 		at java.lang.Thread.run(Thread.java:748)
[2021-06-20T15:21:20.525Z] Cloning repository https://git.company.com/scm/vas/db.git
```

However, directly cloning the code using the command `git clone https://git.company.com/scm/vas/db.git` on the virtual machine was successful without any issues.

* Setting `LIBPATH` to `LIBPATH=/usr/lib` reproduces the error, indicating that Jenkins searches for `libldap.a` under `/usr/lib/` when downloading code.
* Setting the `LIBPATH` variable to empty `export LIBPATH=` or `unset LIBPATH` allows `git clone https://...` to execute normally.

> Attempts to modify the `LIBPATH` variable to empty when starting the Jenkins agent failed to resolve this issue.  The reason remains unclear.

Let's investigate the issue with `/usr/lib/libldap.a`.

```bash
# ldd reveals problems with this static library
$ ldd /usr/lib/libldap.a
/usr/lib/libldap.a needs:
         /opt/IBM/ldap/V6.4/lib/libibmldapdbg.a
         /usr/lib/threads/libc.a(shr.o)
Cannot find libpthreads.a(shr_xpg5.o)
         /opt/IBM/ldap/V6.4/lib/libidsldapiconv.a
Cannot find libpthreads.a(shr_xpg5.o)
Cannot find libc_r.a(shr.o)
         /unix
         /usr/lib/libcrypt.a(shr.o)
Cannot find libpthreads.a(shr_xpg5.o)
Cannot find libc_r.a(shr.o)

# Shows that it links to IBM LDAP
$ ls -l /usr/lib/libldap.a
lrwxrwxrwx    1 root     system           35 Jun 10 2020  /usr/lib/libldap.a -> /opt/IBM/ldap/V6.4/lib/libidsldap.a

# Shows that the same libldap.a in /opt/freeware/lib/ is fine
$ ldd /opt/freeware/lib/libldap.a
ldd: /opt/freeware/lib/libldap.a: File is an archive.

$ ls -l /opt/freeware/lib/libldap.a
lrwxrwxrwx    1 root     system           13 May 27 2020  /opt/freeware/lib/libldap.a -> libldap-2.4.a
```

## Issue 1: Solution

```bash
# Attempt a replacement
# First rename libldap.a to libldap.a.old (don't delete in case of needing to restore)
$ sudo mv /usr/lib/libldap.a /usr/lib/libldap.a.old
# Recreate the symbolic link
$ sudo ln -s /opt/freeware/lib/libldap.a /usr/lib/libldap.a
$ ls -l /usr/lib/libldap.a
lrwxrwxrwx    1 root     system           27 Oct 31 23:27 /usr/lib/libldap.a -> /opt/freeware/lib/libldap.a
```

After recreating the symbolic link, reconnect the AIX agent and rerun the Jenkins job to clone the code.  Success!


## Issue 2: Authentication failed during Git clone via SSH

Due to AIX 7.1-TL4-SP1 nearing its End of Service Pack Support, an upgrade was necessary. However, after upgrading to AIX 7.1-TL5-SP6, SSH code downloads failed.

```bash
$ git clone ssh://git@git.company.com:7999/vas/db.git
Cloning into 'db'...
Authentication failed.
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

This type of error is frequently encountered when using the Git SSH method for cloning code, typically due to a missing public key.  Generating keys with `ssh-keygen -t rsa -C your@email.com` and adding the `id_rsa.pub` content to the GitHub/Bitbucket/GitLab public key usually resolves this.

But this time was different.  The error persisted even after setting the public key.  Surprisingly, it worked fine on AIX 7.1-TL4-SP1 but failed after upgrading to AIX 7.1-TL5-SP6.

Using the command `ssh -vvv <git-url>` to examine debug information during the request to the Git server revealed the following:

```bash
# AIX 7.1-TL4-SP1
bash-4.3$ oslevel -s
7100-04-01-1543
bash-4.3$ ssh -vvv git.company.com
OpenSSH_6.0p1, OpenSSL 1.0.1e 11 Feb 2013
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: Failed dlopen: /usr/krb5/lib/libkrb5.a(libkrb5.a.so):   0509-022 Cannot load module /usr/krb5/lib/libkrb5.a(libkrb5.a.so).
        0509-026 System error: A file or directory in the path name does not exist.

debug1: Error loading Kerberos, disabling Kerberos auth.
.......
.......
ssh_exchange_identification: read: Connection reset by peer
```

```bash
# New machine AIX 7.1-TL5-SP6
$ oslevel -s
7100-05-06-2015
$ ssh -vvv git.company.com
OpenSSH_7.5p1, OpenSSL 1.0.2t  10 Sep 2019
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: Failed dlopen: /usr/krb5/lib/libkrb5.a(libkrb5.a.so):   0509-022 Cannot load module /usr/krb5/lib/libkrb5.a(libkrb5.a.so).
        0509-026 System error: A file or directory in the path name does not exist.

debug1: Error loading Kerberos, disabling Kerberos auth.
.......
.......
ssh_exchange_identification: read: Connection reset by peer
```

The difference is the OpenSSH version, which may be the cause. This led to quickly finding similar problems and answers (Stackoverflow [link](https://stackoverflow.com/questions/54191112/bitbucket-ssh-clone-on-aix-7-1-fails))

## Issue 2: Solution

Add the option `AllowPKCS12keystoreAutoOpen no` to the `~/.ssh/config` file.

However, this option is a custom AIX option and does not exist on Linux.

This results in successful Git clone via SSH for the same domain account on AIX but failure on Linux.

```bash
# Linux does not recognize this option
stderr: /home/****/.ssh/config: line 1: Bad configuration option: allowpkcs12keystoreautoopen
/home/****/.ssh/config: terminating, 1 bad configuration options
fatal: Could not read from remote repository.
```

1. Conditional options in the `config` file would be ideal—adding `AllowPKCS12keystoreAutoOpen no` only for AIX. Unfortunately, `config` does not support this.
2.  Separately setting the current AIX ssh config file would be helpful. Modifying `/etc/ssh/ssh_config` as follows, restarting the service, and retrying the SSH clone was successful~!

```bash
Host *
  AllowPKCS12keystoreAutoOpen no
#   ForwardAgent no
#   ForwardX11 no
#   RhostsRSAAuthentication no
#   RSAAuthentication yes
#   PasswordAuthentication yes
#   HostbasedAuthentication no
#   GSSAPIAuthentication no
#   GSSAPIDelegateCredentials no
#   GSSAPIKeyExchange no
#   GSSAPITrustDNS no
#   ....omitted
```