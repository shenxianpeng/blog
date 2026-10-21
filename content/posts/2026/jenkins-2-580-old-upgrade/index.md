---
title: 老 Jenkins 直接升到 2.580.1：12 个 LTS 版本起不来，联网也一样
summary: |
  Jenkins 2.580.1 不再在 war 里自带拆分出去的插件。我把 38 个 LTS 版本的 controller 只换核心升到 2.580.1，从 12 个版本起来就失败，联网也救不回来。这篇讲日志长什么样、为什么会这样，以及老 controller 该怎么升。
tags:
  - Jenkins
  - Troubleshooting
authors:
  - shenxianpeng
date: 2026-10-21
---

Jenkins 2.574 和 2.577 这两个周版本，把这些年从核心里拆出去的插件从 `jenkins.war` 里删掉了，比如 Instance Identity、SSH server、JAXB。2.580.1 是第一个不带这些插件的 LTS。

[2.580.1 的升级指南][guide]说，大多数实例不受影响：只要能连上 update center，缺的插件 Jenkins 会自己装上，只有离线的实例才需要手工处理。

我想看看一台几年没升级的 controller 直接升上去会怎样，就把每个 LTS 版本都试了一遍。结果和指南说的不一样。

## 怎么测的

- **起点**：38 个 LTS 版本各自的最后一个 release，从 2.60.3 到 2.568.3。按 2026 年 3 月的 Jenkins 使用统计，这 38 个版本覆盖了 234,780 个上报数据的 controller 里的 79%。
- **插件**：装机量最高的 100 个和 300 个插件，每个都用这个版本能装的最新 release。也就是说，假设管理员一直有在更新插件，这已经是比较理想的情况。
- **只换核心**：插件文件不动，只把 war（或安装包、镜像）换成 2.580.1，Jenkins 以“从旧版本升级”的状态启动，容器不联网。
- **分步升级**：同一台 controller 先经过中间的 LTS（按需要经过 2.346.3、2.462.3、2.541.3），每一站都更新插件，再往下走。

每个起点都先在它自己的版本上启动一次，确认起点本身是好的。一整轮是 328 次 Jenkins 启动，全部用官方 Docker 镜像。

## 结果

| | 100 个插件 | 300 个插件 |
|---|---|---|
| 只换核心：Jenkins 起不来 | 0 / 38 | 12 / 38 |
| 只换核心：能起来，但有插件失败或只加载了一部分 | 21 / 38 | 12 / 38 |
| 分步升级：每一站都干净加载 | 38 / 38 | 38 / 38 |

有几个起点在升级之前就已经有插件加载不了（100 个插件时 2 个，300 个插件时 5 个），算在第二行里。

升级本身带来的问题，全部出在 2.346.3 及更老的版本上：

- 300 个插件时，从 2.164.3 到 2.277.4、从 2.319.3 到 2.346.3 这 12 个版本，Jenkins 直接起不来。
- 100 个插件时都能起来，但从 2.319.3 到 2.346.3，GitHub 和 SSH server 插件只加载了一部分。

使用统计里，10.8% 的 controller 还跑在 2.346.3 或更老的版本上。

## 日志长什么样

升级信息之后，Jenkins 紧接着告诉你它什么都没装：

```text
Upgrading Jenkins. The last running version was 2.346.3. This Jenkins is version 2.580.1.
Upgraded Jenkins from version 2.346.3 to version 2.580.1. Loaded detached plugins (and dependencies): []
```

2.577 之前，这个列表里会列出 controller 缺的拆分插件，从 war 里自带的副本装上。现在副本没了。针对老核心构建的插件，对这些拆分插件的依赖是可选的，所以照样能加载，要到 Jenkins 查找它们的扩展时才出错：

```text
Failed to create Guice container from all the plugins
java.lang.ClassNotFoundException: org.jenkinsci.main.modules.instance_identity.InstanceIdentity
```

更麻烦的是，起不来的时候，最后一条报错点名的插件并不是原因，而且每次还不一样。我的测试里，它点过 Bitbucket Server Integration、Kubernetes Credentials Provider 和 Git：

```text
SEVERE hudson.util.BootFailure#publish: Failed to initialize Jenkins
java.lang.IllegalArgumentException: Unable to inject class com.atlassian.bitbucket.jenkins.internal.jenkins.auth.OAuthFilterRegistrar
```

读了 2.580.1 的代码，原因有两层。第一层，Bitbucket Server Integration 3.3.2 用到了 Instance Identity 的类，但没有声明依赖，Guice 创建容器时碰到这个类就整体失败了。第二层，Guice 失败后有一段兜底逻辑，本来是只用核心的扩展再建一次容器，可这段逻辑没有绑定 `Jenkins` 这个对象，而核心里有扩展要注入它，所以兜底也一定失败。之后所有需要注入的初始化步骤都会报错，哪个先跑，报错就点名哪个插件。

我找到的最小复现是 Bitbucket Server Integration 3.3.2 加上它的依赖，一共 60 个插件。3.3.2 是 2.346.3 上能装的最新版本。

我还扫了一遍这 300 个插件的 class 文件：在 2.346.3 能装的最新版本里，有 7 个用了 Instance Identity 的类却没有声明依赖，包括很常用的 Mailer 和 GitHub。

## update center 帮不上忙

我把 2.346.3 和 2.277.4 的升级在联网的情况下又跑了一遍，先在同一个镜像里确认能访问 `updates.jenkins.io`。

结果一样：没有下载任何拆分插件，Jenkins 照样起不来。从代码看，只有在插件管理器里安装插件时，Jenkins 才会顺带从 update center 装上拆分插件；核心升级后启动的那一刻，没有任何地方会去下载它们。

## 老 controller 该怎么升

先看看这台 controller 上一次跑的是哪个版本：

```sh
cat "$JENKINS_HOME/jenkins.install.InstallUtil.lastExecVersion"
```

如果是 2.356 或更老，别直接跳到 2.580.1。下面两种做法在我的测试里都能用：

**经过一个老一点的 LTS。** 先升到一个还自带拆分插件的 LTS（2.568.3 或更早），启动一次让它把插件装上，在插件管理器里把所有插件更新一遍，然后再往上升。38 个起点全部干净加载的，就是这条路。

注意中间那一站的插件更新不能省。我试过从 2.346.3 只换核心到 2.568.3 不更新插件，SSH server 插件加载不了，因为它新装的依赖要求更新版本的 SSH Credentials 插件。

**启动 2.580.1 之前，把拆分插件连同依赖一起放进去。** 官方镜像里自带 `jenkins-plugin-cli`：

```sh
jenkins-plugin-cli --jenkins-version 2.580.1 --plugins instance-identity \
  --plugin-download-directory /tmp/split
```

它会下载 Instance Identity 和它需要的新版 bouncycastle API。把这两个文件拷进 `$JENKINS_HOME/plugins`，替换掉同名的旧文件。

只放 `instance-identity.jpi` 是不行的，它要求的 bouncycastle API 比 2.346.3 上的版本新。2.277.4 或更老的版本缺的插件更多，我在 300 个插件的测试里把它们放进去以后，和老插件之间形成了依赖环，307 个插件里有 213 个加载失败。这种情况我会选择经过中间的 LTS。

每个插件是在哪个版本拆出去的，可以查 [`split-plugins.txt`][split]。

不管选哪种，先在 `JENKINS_HOME` 的副本上演练一遍，再动真正的 controller。起不来的 controller 在副本上处理要轻松得多。

## 还没做的

上面说的兜底逻辑的问题，是我读代码得出的，没有改核心去验证修复。测试用的插件组合是按装机量排出来的，不是真实的 controller，没有 job、凭据和 agent，真实环境可能遇到别的问题。

每个起点的完整结果，包括哪些插件失败了，在 [keelinfra.io/jenkins/upgrade-matrix][matrix]。

[guide]: https://www.jenkins.io/doc/upgrade-guide/2.580/
[split]: https://github.com/jenkinsci/jenkins/blob/master/core/src/main/resources/jenkins/split-plugins.txt
[matrix]: https://keelinfra.io/jenkins/upgrade-matrix/
