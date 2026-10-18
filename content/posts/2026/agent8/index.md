---
title: Jenkins 要 Java 21，老构建机只有 Java 8：我做了 Agent8
summary: |
  Jenkins 的 agent 也必须跑 Java 21，Solaris、HP-UX、AIX 7.1 这些最高只有 Java 8 的构建机就连不上新版 Jenkins 了。Agent8 把官方 agent.jar 降级到 Java 8，让它们继续当普通的 agent。
tags:
  - Jenkins
  - Java
  - Open Source
authors:
  - shenxianpeng
date: 2026-10-16
series: ["我的开源项目"]
series_order: 6
---

如果你的 Jenkins 里还挂着几台 Solaris、HP-UX 或 AIX 的构建机，最近可能已经感觉到了：controller 越来越难升级了。

很多公司都有这样一批机器：Solaris、HP-UX、AIX，再加几台 RHEL 6。它们跑了很多年，没人想动，而且都是 Jenkins agent，每个平台的构建都从它们身上来。

问题是，这些系统上的 Java 基本停在 8。

而 Jenkins 一直在抬 Java 版本：2022 年的 2.361.1 LTS 开始要求 Java 11，2024 年的 2.479.1 LTS 要求 Java 17，现在要求 Java 21 或 25。[Jenkins 的 Java 支持策略][java-policy]里写得很清楚，这个要求适用于 Jenkins 系统的所有组件，**agent 也包括在内**。

如果你最老的构建机只能跑 Java 8，它能连上的最新 Jenkins 是 2022 年 8 月的 2.346.3。这个版本早就没有安全更新了。

所以团队通常只能二选一：

- 升级 controller，安全扫描过了，但 AIX、HP-UX、Solaris 和老 RHEL 的 agent 全部连不上；
- 不升级，老 agent 继续能用，整个 Jenkins 停在一个没人打补丁的版本上，每次审计都要申请例外。

最后很多团队的做法是：专门为这些平台留一套旧 Jenkins，或者干脆手工构建。

现在有了 AI，很多报错丢给它就能解决，读日志、改配置都很快。但它改变不了一件事：这些系统上就是没有 Java 21。

## Agent8 是什么

[Agent8][agent8] 让只有 Java 8 的构建机继续当一个普通的 Jenkins agent，连接跑在 Java 21+ 上的新版 controller。

它是怎么做到的：

1. 用 [JvmDowngrader][jvmdg] 把官方的 `agent.jar` 提前降级成 Java 8 字节码（也可以出 Java 11、17 的版本）；
2. controller 在构建过程中发给 agent 的类，在加载时再降级一次；
3. 再加一个小的 Java agent，处理降级带来的兼容问题，比如序列化时的 `serialVersionUID`、`List.of` 这类集合在 Java 8 上没有的序列化格式，以及 Solaris 和 IBM Java 上签名的安全提供者。

对 controller 来说，它就是一个普通的 agent：labels、executors、`sh`、文件步骤、`junit`、`stash`、中止构建、script console 都和其他节点一样。启动命令也不变，还是 `java -jar agent.jar`。

## 先看看你需不需要它

不是每台老机器都需要 Agent8，有些有更简单的路：

- **RHEL / CentOS 6 x86_64**：系统仓库里的 OpenJDK 只到 8，但 Amazon Corretto 21 和 Azul Zulu 21 能在 CentOS 6.10 上跑，官方 `agent.jar` 可以直接连上当前的 LTS。这条路走到 Jenkins 要求 Java 25 为止（Corretto 25 需要 RHEL 7+）。
- **AIX 7.2 TL5+ 或 7.3 TL2+，POWER8 及以上**：装 IBM Semeru 21，跑普通的 agent 就行。

Agent8 是给剩下的机器准备的：AIX 7.1、Solaris、Itanium 上的 HP-UX 这些根本没有 Java 21 的系统，以及 JDK 不能动的机器，比如工具链经过认证或验证的环境。

每个平台最高能跑哪个 Java、出处在哪里，我整理在了[这篇文章][background]里。

## 怎么用

在构建机上，用它现有的 Java（8、11 或 17），带上 controller 的地址：

```sh
curl -fsSLO https://raw.githubusercontent.com/keelinfra/agent8/main/install.sh
sh install.sh --url https://jenkins.example.com/ --replace /path/to/agent.jar
```

`install.sh` 会问 controller 用的是哪个 remoting 版本，下载对应的 Agent8 jar，用 `sha256sums.txt` 校验，再用本机的 Java 试启动一下，确认没问题之后才替换原来的 `agent.jar`。原来的 jar 会保留为 `agent.jar.before-agent8`，`--restore` 可以换回去。然后照常重启 agent 就行。

脚本只用 POSIX `sh`，在老 Unix 上也能跑。不能上网的机器可以把 release 里的文件拷过去用 `--from DIR`，机器多的话有 Ansible playbook。

Release 按 Jenkins 版本命名，比如 `jenkins-2.580.1` 就是给 Jenkins 2.580.1 用的。升级 controller 之后重新跑一次 `install.sh` 就好。这一步不能省：Jenkins 会不断抬高它接受的最低 agent 版本，比如 Jenkins 2.586 已经不接受给 2.462.3 构建的 Agent8 了。

## 现在到了哪一步

这部分我想说清楚，免得误导：

| 构建机 | Java | 状态 |
|---|---|---|
| Linux，包括 RHEL/CentOS 6 | HotSpot 8 | CI 中测试 |
| Linux（IBM Semeru，OpenJ9） | OpenJ9 8 | CI 中测试，尽力支持 |
| Linux | HotSpot 11、17 | CI 中测试（LTS） |
| AIX 7.1 / 7.2 | IBM Java 8 | 实验阶段 |
| Solaris | Java 8、11 | 已在真机上跑通 |
| HP-UX（Itanium） | Java 8 | 已在真机上跑通 |

CI 每周都会对着最新的 LTS 和 weekly 跑一遍：Pipeline 构建、Git checkout（JGit）、`withCredentials`、中止构建、构建中途重启 agent、script console。

还没验证的：真实的 AIX 机器，以及会在 agent 上跑自己代码的插件（Maven、Docker、制品上传、命令行 git 等）。如果你要用，建议先挑一台机器把 job 跑通，再整体迁移。

**Agent8 是独立项目，不属于 Jenkins 项目，也没有得到 Jenkins 项目的认可或支持。** 遇到问题请提到 [Agent8 的 issues][issues]，不要提到 Jenkins 的 issue tracker。

## 社区的反馈

10 月 13 日我把它发到了 [Jenkins 社区论坛][thread]，几天里收到了几条很实在的反馈：

- 有人指出，Jenkins Platform SIG 早在 2021 年就放弃了对 OpenJ9 的支持，而且历史上有不少 J9 相关的问题。AIX 上往往只有 IBM Java 8 可用，所以我在 README 里把 J9 的支持改成了"尽力支持"，问题请报给 Agent8。
- 有人提醒 Amazon Corretto 21 仍然支持 RHEL 6。我在 CentOS 6.10 上测了，确实能跑官方 agent，就把它写进了 README，作为 RHEL 6 x86_64 的首选方案。
- 还有人分享了以前的做法：在 Linux 上 checkout，用 scp 把工作区拷到老机器上，通过 ssh 执行构建，再把结果拷回来。能用，但并行构建和中止构建都要自己处理。

和上次 Keelhaven 一样，这些反馈很多是我自己没想到的。

## 免费，也有付费支持

Agent8 是 MIT 协议，仓库里的东西全部免费，没有阉割的功能。

如果你需要更多保障，比如在 AIX、Solaris 或 HP-UX 上和我们一起做试点、检查你用到的插件能不能在 Java 8 agent 上工作，或者每次 controller 升级之前都有一个测试过的版本，可以看看 [keelinfra 的定价页][pricing]。都是固定价格，第一个问题的回答免费。

---

项目地址：https://github.com/keelinfra/agent8  
介绍页：https://keelinfra.io/jenkins/

如果你手上正好有 AIX、Solaris 或 HP-UX 的构建机，愿意帮忙验证一下，欢迎开 [issue][issues] 或者发邮件到 hello@keelinfra.io。觉得有用的话，也欢迎点个 Star，转给还在维护老构建机的朋友。

[java-policy]: https://www.jenkins.io/doc/book/platform-information/support-policy-java/
[agent8]: https://github.com/keelinfra/agent8
[jvmdg]: https://github.com/unimined/JvmDowngrader
[background]: https://keelinfra.io/blog/jenkins-java-21-aix-rhel6-build-hosts/
[issues]: https://github.com/keelinfra/agent8/issues
[thread]: https://community.jenkins.io/t/keeping-java-8-build-hosts-aix-solaris-hp-ux-rhel-6-as-agents-of-a-current-jenkins/37378
[pricing]: https://keelinfra.io/jenkins/pricing/
