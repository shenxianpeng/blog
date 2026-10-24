---
title: Jira 上云之后，Jenkins 和 Bitbucket 怎么办
summary: |
  Atlassian Data Center 2029 年 3 月停止，但 Bitbucket 和 Bamboo 不在停止名单里。逼着团队动起来的是 Jira 上云，代码要不要跟着走成了躲不开的问题。我搭了一套 Bitbucket DC 9.4 和 Jenkins 2.541.3，把 multibranch job 切到 Bitbucket Cloud，记下哪些地方会坏、哪些不会。
tags:
  - Jenkins
  - Bitbucket
  - DevOps
authors:
  - shenxianpeng
date: 2026-10-24
---

Atlassian 宣布 Data Center 产品 2029 年 3 月 28 日停止。我一开始以为 Bitbucket Data Center 也在里面，跟人聊的时候还这么说过。回头去翻 [Atlassian 的说明][eol]，才发现说错了。

## 先把时间表弄清楚

| 日期 | 发生什么 |
|---|---|
| 2026-03-30 | 新客户买不到任何 Data Center 产品 |
| 2027 年初 | Bitbucket Hybrid License 开放给老客户 |
| 2028-03-30 | 老客户不能再新买、扩容 Data Center |
| 2029-03-28 | Jira、Confluence DC 变成只读；没换 Hybrid License 的 Bitbucket、Bamboo DC 也变成只读 |

Bitbucket 和 Bamboo DC 不在停止名单里。[Hybrid License 的页面][hybrid]原话是 "Bitbucket and Bamboo Data Center will not end of life and will continue beyond the Data Center end of life in 2029"。老客户换成 Hybrid License 以后，一份订阅里有 Bitbucket DC、Bamboo DC 和 Bitbucket Cloud（带 Pipelines），价格没公布。不换的话，同一页的 FAQ 写着 2029-03-28 之后 DC 会变成只读，不能再 push。

所以"Bitbucket DC 要停了，必须搬"这个说法不成立。让团队动起来的是 Jira 和 Confluence：它们必须上云或者换掉，而 Jira 一上云，代码要不要跟着走，就成了躲不开的问题。

## 三条路

1. **留在 Bitbucket DC，换 Hybrid License。** Jenkins 一行都不用改。适合代码必须留在自己机房的团队。代价是价格还不知道，而且 Jira 在云上、代码在机房，两边的集成要重新接。
2. **搬到 Bitbucket Cloud。** 和 Jira Cloud 集成最顺，Hybrid License 里本来就带。
3. **借这次机会换到 GitHub 或 GitLab。** [GitHub Enterprise Importer][gei] 能把 Bitbucket Server/DC 的仓库连同 PR、评论、review 一起搬到 GitHub Enterprise Cloud。

CI 这边，三家都准备了"从 Jenkins 搬过来"的路：GitHub 有 Actions Importer，Atlassian 2025 年 1 月发布了 [Jenkins 到 Bitbucket Pipelines 的迁移工具][bbp]（只自动转换装机率超过 5% 的插件，其余原样抄过去让人改），GitLab 只有一份[迁移文档][gitlab]。这些工具转换的是 Jenkinsfile 的写法。shared library、冷门插件、固定的构建机、内网的部署目标，还是要人来处理。[JetBrains 2025 年的 CI/CD 调查][jb]里，32% 的组织同时在用两种 CI 工具，9% 用三种以上。

我的建议是一次只换一样：先换代码平台，Jenkins 照跑；稳定了，再决定 CI 要不要换。下面说的都是"只换代码平台"这一步会碰到的事。

## 怎么测的

- Bitbucket Data Center 9.4.26，官方 Docker 镜像，用 Atlassian 给插件开发者的 [3 小时测试许可][timebomb]。
- Jenkins 2.541.3（最后一个支持 Java 17 的 LTS），[Bitbucket Branch Source][bbs] 937.3.10，Atlassian 出的 [Bitbucket Server Integration][bsi] 6.0.2。
- 一个仓库，两个分支，`test/Jenkinsfile` 里只有三个 echo stage。
- Cloud 那头用的是 bitbucket.org 上的公开仓库 [atlassian/jenkins-job-trigger][cloudrepo]，分支名和 Jenkinsfile 路径都和 DC 上的一样，匿名扫描。

## 坏的第一处：Atlassian 自己的插件不支持 Cloud

Bitbucket Server Integration 是 Atlassian 官方出的 Jenkins 插件。把它的服务器地址填成 bitbucket.org，校验直接报错：

```text
This plugin does not support connecting to bitbucket.org. It is for Bitbucket Server instances only.
```

用这个插件建的 job，搬到 Cloud 时要全部改成 Bitbucket Branch Source 或者 Git 插件。两个插件名字很像，很容易当成同一个东西。

## 坏的第二处：app password 没了，API token 要新版插件

Bitbucket Cloud 从 2025 年 9 月 9 日起不能再新建 app password，[2026 年 6 月 9 日全部停用][apppw]。替代品是带权限范围的 API token。

Bitbucket Branch Source 从 937.0.0 才支持 API token（[JENKINS-75772][75772]），这个版本要求 Jenkins 2.504.1 以上。我用 update center 的版本数据算了每个 LTS 能装上的最新版本：

| Jenkins LTS | 能装的最新 Bitbucket Branch Source | 支持 API token |
|---|---|---|
| 2.346.3 | 805.v7f97d29dc0f5 | 否 |
| 2.426.3 | 888.v8e6d479a_1730 | 否 |
| 2.462.3 | 912.v3b_f74026941c | 否 |
| 2.479.3、2.492.3 | 936.4.3 | 否 |
| 2.504.3 到 2.528.3 | 937.3.0 | 是 |
| 2.541.3 | 937.3.10 | 是 |

2.492.3 及更早的 Jenkins，想用 API token 接 Bitbucket Cloud，得先升 Jenkins。2.462.3 是最后一个支持 Java 11 的 LTS，更老的 controller 就变成了先换 Java、再升 Jenkins、再换插件，最后才轮到搬代码。插件里另外两个和 API token 有关的修复，fork PR 拉代码失败和只读用户看不到仓库列表，在 937.3.3 和 937.3.5 里，要 Jenkins 2.541.3。

老版本插件还支持 OAuth consumer，理论上可以先拿它顶一阵，这条我没测。

还有一个坑。同一个 API token，[调 REST API 时用户名要填 Atlassian 账号的邮箱，走 Git over HTTPS 时要填 Bitbucket 用户名][apitoken]，或者固定的 `x-bitbucket-api-token-auth`。Branch Source 的文档要求凭据里填邮箱，checkout 由插件自己处理；如果你还有直接用 Git 插件拉代码的 freestyle job 或 `git` 步骤，那边要填用户名。社区里"API token 能列出仓库、clone 却失败"的帖子，不少是这个原因。

## 没坏的：构建历史

我原本担心换了来源以后，分支 job 会被重建，构建编号从 1 重新开始。测下来不会，但有两个情况要注意：

| 怎么改 | 分支 job 和构建历史 | 会不会触发构建 |
|---|---|---|
| 在原来的来源上改地址和仓库（来源 ID 不变） | 保留，编号接着往下走 | commit 没变就不会 |
| 删掉旧来源，加一个新的（来源 ID 变了） | 保留，日志里是 `Takeover ... from source that no longer exists` | 每个分支都重新构建一次（`Branch reopened`） |
| 新旧两个来源同时挂在一个 job 上 | 新来源的同名分支被忽略：`Ignoring ... as source #1 owns the branch name` | 不会 |

第二种在分支多的仓库里就是一场构建风暴，几百个分支同时排队。所以在 Jenkins 界面上，尽量在原来的来源上改，不要删了重加。想在同一个 job 里新旧并行跑一阵也行不通，要并行就另建一个 job。

测试机器的网络不让 git 直连 bitbucket.org，切到 Cloud 之后的构建都在 `git fetch` 这一步失败了。这不影响上面的结论，要看的是 job 和编号，不是构建结果。"commit 不变就不会重建"这一条，是我在 DC 里另建一个 commit 完全相同的仓库测的。

## 搬之前先盘点

做这些改动之前，先要知道哪些 job 连着 Bitbucket。在 Script Console 里跑下面这段，能列出所有引用了 Bitbucket 地址的 job 和全局配置：

```groovy
// Manage Jenkins > Script Console
def needle = "bitbucket.example.com"   // 换成你的 Bitbucket DC 域名
def j = jenkins.model.Jenkins.get()
j.getAllItems(hudson.model.Item).each { item ->
  if (item.parent instanceof jenkins.scm.api.SCMSourceOwner) return  // multibranch 下的分支 job，跟着父 job 走
  if (item.configFile.asString().contains(needle)) println "job: ${item.fullName}"
}
// 全局配置：shared library、Bitbucket endpoint 等
new File(j.rootDir.path).listFiles().findAll { it.name.endsWith(".xml") && it.text.contains(needle) }.each {
  println "global: ${it.name}"
}
return
```

我在测试 Jenkins 上加了一个 freestyle job 和一个把 git 地址写死在脚本里的 Pipeline，都找出来了，Bitbucket endpoint 的全局配置也在。它找不到写在仓库里的 Jenkinsfile 和 shared library 代码，那部分要去代码里搜。

Bitbucket 那头也有依赖 Jenkins 的东西：合并检查（"构建通过才能合并"靠的是 Jenkins 回写的状态）、webhook、服务账号和 SSH key。

最后是网络方向。以前 Bitbucket 和 Jenkins 都在内网，代码上云以后，云端的 webhook 要能打到内网的 Jenkins（放行 [Atlassian 的 IP 段][ips]、加一层转发，或者退回定时扫描），每台 agent 也要能出网拉代码。

## 没测的

- Bitbucket Cloud 的私有仓库和 API token。我没有拿真实账号测，用的是公开仓库匿名扫描。
- 搬到 GitHub。测试环境连不上 GitHub API，GitHub Branch Source 这条没测。
- AIX、Solaris 这类老机器上的 git 和 OpenSSH 能不能连上 bitbucket.org。测试环境出网走代理，测出来不算数。

如果你正在做 Jira 上云的规划，Jenkins 也归你管，欢迎留言说说你们打算怎么处理代码和 CI。

[eol]: https://www.atlassian.com/licensing/data-center-end-of-life
[hybrid]: https://www.atlassian.com/migration/bitbucket-hybrid-license
[gei]: https://docs.github.com/en/migrations/using-github-enterprise-importer/migrating-from-bitbucket-server-to-github-enterprise-cloud/about-migrations-from-bitbucket-server-to-github-enterprise-cloud
[bbp]: https://www.atlassian.com/blog/bitbucket/general-availability-of-the-jenkins-to-bitbucket-pipelines-migration-tool
[gitlab]: https://docs.gitlab.com/ci/migration/jenkins
[jb]: https://blog.jetbrains.com/teamcity/2025/10/the-state-of-cicd/
[timebomb]: https://developer.atlassian.com/platform/marketplace/timebomb-licenses-for-testing-server-apps/
[bbs]: https://plugins.jenkins.io/cloudbees-bitbucket-branch-source/
[bsi]: https://plugins.jenkins.io/atlassian-bitbucket-server-integration/
[cloudrepo]: https://bitbucket.org/atlassian/jenkins-job-trigger
[apppw]: https://www.atlassian.com/blog/bitbucket/bitbucket-cloud-enters-phase-2-of-app-password-deprecation
[75772]: https://issues.jenkins.io/browse/JENKINS-75772
[apitoken]: https://support.atlassian.com/bitbucket-cloud/docs/using-api-tokens/
[ips]: https://support.atlassian.com/bitbucket-cloud/docs/what-are-the-bitbucket-cloud-ip-addresses-i-should-use-to-configure-my-corporate-firewall/
