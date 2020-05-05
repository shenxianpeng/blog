---
title: GitSCM clone code don't display branch
date: 2019-05-14 22:41:22
tags: 
- Jenkins
- pipeline
categories: 
- Jenkins
author: shenxianpeng
---

最近遇到一个 regression bug，是产品完成构建之后，build commit number 不对，显示的 HEAD 而不是常见的 97b34931ac HASH number,这是什么原因呢？
我检查了 build 脚本没有发现问题，branch 的输出是正确的，那我怀疑是引入 Jenkins 的原因，果然登录到远程的 agent 上去查看分支名称如下：

```git
C:\workspace\blog>git branch
* (HEAD detached at 97b3493)
```

果然问题出在了 Jenkins 上。这个问题有简单办法解决，就是直接使用git命令来clone代码，而不使用Git插件

```bash
git clone --depth 1 -b u2opensrc https://username:"passwowrd"@git.github.com/scm/blog.git blog
```

这种方式固然简单，不会出错，但它是明码显示，我岂能容忍这种不堪的处理方式吗？肯定还是要在 Git 插件上找到解决办法的。
随后google一下，果然有遇到和我一样问题的人，问题链接 [这里](https://stackoverflow.com/questions/44006070/jenkins-gitscm-finishes-the-clone-in-a-detached-head-state-how-can-i-make-sure)。

他说他做了很多调查，还跟专业的 Jenkins 人士联系，试了很多次，最后找到这个办法

```bash
checkout([$class: 'GitSCM', branches: [[name: '*/feature/*']], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'LocalBranch', localBranch: "**"]], submoduleCfg: [], userRemoteConfigs: [[credentialsId: '99f978af-XXXX-XXXX-8147-2cf8f69ef864', url: 'http://TFS_SERVER:8080/tfs/DefaultCollection/Product/_git/Project']]])
```

主要是在 extensions:[] 中加入这句 [$class: 'LocalBranch', localBranch: "**"]

这是 Jenkins 的 Bug 吗？带着这个疑问随后通过 Pipeline Syntax，找到 checkout: Check out from version control，在 Additional Behaviours 里有 Check out to specific local branch 这个配置项

If given, checkout the revision to build as HEAD on this branch.
If selected, and its value is an empty string or "**", then the branch name is computed from the remote branch without the origin. In that case, a remote branch origin/master will be checked out to a local branch named master, and a remote branch origin/develop/new-feature will be checked out to a local branch named develop/newfeature.

看介绍原来 Jenkins 自带这个设置，只是它不是默认选项，所以才遇到刚才那个问题。随后选择这个设置，然后填入"**"，然后生成 Pipeline 脚本，就跟上面的脚本一样了。
