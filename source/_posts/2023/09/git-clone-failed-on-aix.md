---
title: 解决在 AIX 通过 Jenkins agent git clone 失败的问题
tags:
  - Git
  - AIX
  - Jenkins
categories:
  - AIX
date: 2023-09-07 18:53:26
author: shenxianpeng
---

最近又遇到了在 AIX 上通过 Jenkins agent 无法下载代码的情况，报了如下错误：

```bash
16:42:47  Caused by: hudson.plugins.git.GitException: Command "git init /disk1/agent/workspace/e_feature-aix-ci-build" returned status code 255:
16:42:47  stdout:
16:42:47  stderr: exec(): 0509-036 Cannot load program git because of the following errors:
16:42:47  	0509-150   Dependent module /usr/lib/libiconv.a(libiconv.so.2) could not be loaded.
16:42:47  	0509-152   Member libiconv.so.2 is not found in archive
16:42:47
16:42:47  	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl.launchCommandIn(CliGitAPIImpl.java:2734)
16:42:47  	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl.launchCommandIn(CliGitAPIImpl.java:2660)
16:42:47  	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl.launchCommandIn(CliGitAPIImpl.java:2656)
16:42:47  	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl.launchCommand(CliGitAPIImpl.java:1981)
16:42:47  	at org.jenkinsci.plugins.gitclient.CliGitAPIImpl$5.execute(CliGitAPIImpl.java:1047)
```

> 上次遇到在 AIX 遇到的 git clone 问题总结在这里 https://shenxianpeng.github.io/2021/06/git-clone-failed-on-aix/

而我在 AIX 机器上手动执行 git clone 命令却没有这个错误发生，从失败的 log 和 `ldd /usr/bin/git` 发现 `libiconv.a` 的路径不同，推测问题应该出在 `LIBPATH` 环境变量上。

因为在本地（AIX）执行 git 命令的时候 `LIBPATH` 是为空，如果设置了 `LIBPATH` 路径为 /usr/lib/ 会出上面一样的错误。

```bash
$ ldd /usr/bin/git
/usr/bin/git needs:
         /usr/lib/libc.a(shr_64.o)
         /usr/lib/libpthreads.a(shr_xpg5_64.o)
         /opt/freeware/lib/libintl.a(libintl.so.8)
         /opt/freeware/lib/libiconv.a(libiconv.so.2)
         /opt/freeware/lib/libz.a(libz.so.1)
         /unix
         /usr/lib/libcrypt.a(shr_64.o)
         /opt/freeware/lib64/libgcc_s.a(shr.o)
$
```

但 Jenkins agent 在执行的时候有默认的 `LIBPATH`，查看这个变量可以通过 Jenkins Agent 上的 Script Console 执行如下命令打印出来

```groovy
println System.getenv("LIBPATH")
```

```bash
# 返回的结果
/usr/java8_64/jre/lib/ppc64/j9vm:/usr/java8_64/jre/lib/ppc64:/usr/java8_64/jre/../lib/ppc64:/usr/java8_64/jre/lib/icc:/usr/lib
```

其中果然有 `/usr/lib`，这导致了 git 是去找 `/usr/lib/libiconv.a` 而不是 `/opt/freeware/lib/libiconv.a`。

我尝试过很多种办法但最终还是无法在 Jenkins agent 在 git clone 的时候 `unset LIBPATH`，包括:

1. 重新 link，将 `/usr/lib/libiconv.a` 链接到 `/opt/freeware/lib/libiconv.a`

```bash
mv /usr/lib/libiconv.a /usr/lib/libiconv.a.bak
ln -s /opt/freeware/lib/libiconv.a /usr/lib/libiconv.a
```

2. 在 pipeline 中使用 `withEnv` 设置 `LIBPATH` 为空

```bash
withEnv(['LIBPATH=\'\'']) {
  checkout scm
}
```

3. 在 Agent 配置页面上尝试通过 Environment variables 来修改 `LIBPATH`（这个看起来像是 Jenkins 的一个 bug [JENKINS-69821](https://issues.jenkins.io/browse/JENKINS-69821))


4. 在配置 Jenkins agent 页面通过添加 `export LIBPATH="" &&` 到 Prefix Start Agent Command 均不起作用。


最后是通过在 AIX 更新 Git 从版本 `2.39.3` 升级到 `2.40.0` 解决了这个错误，这有点巧合并没有真正把 Jenkins agent 的覆盖默认环境变量的问题给解决，但好在这个问题已经没有了。

仅此记录一下，防止以后遇到同样的错误不至于从头开始尝试，也希望这个记录也可能帮助到你。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
