---
title: "给软件交付装上开源护栏。"
heroCaption: "沈显鹏 · Engineer. Builder. Maintainer."
heroLead: "代码检查、提交规范、CI/CD 自动化——全部开源维护，跑在 1000 多个公开仓库的 CI 里。"
heroButtons:
  - label: "看项目"
    url: "/zh-cn/portfolio/"
  - label: "读文章"
    url: "/zh-cn/posts/"
    style: "outline"
---

我是沈显鹏，现居立陶宛维尔纽斯。做软件十六年，从测试、测试开发、开发一路做到 DevOps，从 Jenkins 集群到容器，构建、测试、发布这一段的活都干过。[cpp-linter](https://github.com/cpp-linter) 和 [commit-check](https://github.com/commit-check/commit-check) 就是从这些活里长出来的；[keelinfra](https://keelinfra.io)（生产可用的自托管 Keycloak）和 [keelapps](https://keelapps.app)（Jira 与 Confluence 的管理工具）是我做的产品。哪个对得上你的场景，拿去用。省了你的时间，欢迎[赞助](https://github.com/sponsors/shenxianpeng)，让它持续维护。

## 我在做什么

{{< feature-grid columns="2" align="left" >}}
{{< feature icon="check" title="cpp-linter" url="https://github.com/cpp-linter" label="开源" >}}
每个 PR 上自动跑 clang-format 和 clang-tidy，提供 GitHub Action、pre-commit hook 和 Python 包三种用法。Apache、Samsung、Qualcomm、Bloomberg、LLNL、Nextcloud 都在用。
{{< /feature >}}
{{< feature icon="lock" title="keelinfra" url="https://keelinfra.io" label="产品" >}}
生产可用的自托管 Keycloak：高可用、备份与时间点恢复、监控、升级路径，每晚在公开 CI 里重新验证一遍。
{{< /feature >}}
{{< feature icon="list-check" title="keelapps" url="https://keelapps.app" label="产品" >}}
Jira 与 Confluence Cloud 的管理工具：权限审计、周期任务、定时报表、页面审批。基于 Atlassian Forge，每个应用都跑在你自己的租户里。
{{< /feature >}}
{{< feature icon="apple" title="Keelhaven" url="https://keelhaven.app" label="免费应用" >}}
把 Mac 备份到你自己的存储。基于 restic 的原生菜单栏应用，文件离开 Mac 前就已加密。免费、开源。
{{< /feature >}}
{{< /feature-grid >}}

## 关注公众号

中文文章同步发布在微信公众号「沈显鹏」，扫码关注。

{{< figure src="img/qrcode.jpg" alt="微信公众号「沈显鹏」二维码" class="mx-auto home-qrcode" nozoom="true" >}}
