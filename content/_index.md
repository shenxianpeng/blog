---
title: "给软件交付装上开源护栏。"
heroTitle: "给软件交付<br>装上开源护栏。"
heroLead: "代码检查、提交规范、CI/CD 自动化——全部开源维护，跑在 1000 多个公开仓库的 CI 里。"
heroButtons:
  - label: "看项目"
    url: "/zh-cn/portfolio/"
  - label: "读文章"
    url: "/zh-cn/posts/"
    style: "outline"
flagship:
  label: "cpp-linter"
  title: "每个 PR 都自动检查。"
  text: "在每个 PR 上跑 clang-format 和 clang-tidy，提供 GitHub Action、pre-commit hook 和 Python 包三种用法。修改建议直接出现在代码审查里，点一下就能提交。"
  links:
    - label: "文档"
      url: "https://cpp-linter.github.io/"
    - label: "GitHub"
      url: "https://github.com/cpp-linter"
  demo: "cpp-linter"
  demoLabel: "cpp-linter 在 GitHub PR 上的演示动画：检查失败，cpp-linter 给出 clang-format 修改建议，提交建议后检查通过。"
  usersLabel: "这些项目的 CI 在用"
  users: ["Apache", "Samsung", "Qualcomm", "Bloomberg", "LLNL", "Nextcloud"]
products:
  title: "掌握在你自己手里的基础设施。"
  text: "自托管的 Keycloak，跑在你自己租户里的 Atlassian 应用，还有备份到你自己存储的 Mac 备份工具。"
  items:
    - name: "Keelhaven"
      label: "免费 · 开源 · macOS 14+"
      text: "把 Mac 备份到你自己的存储。基于 restic 的原生菜单栏应用，文件离开 Mac 前就已加密。"
      url: "https://keelhaven.app"
      demo: "keelhaven"
      demoLabel: "Keelhaven 菜单栏应用的备份演示动画：名为 Documents 的备份计划备份到外置硬盘，显示进度条，完成后弹出 Backup complete 通知。"
      style: "wide"
    - name: "keelinfra"
      label: "产品"
      text: "生产可用的自托管 Keycloak，升级路径每晚在公开 CI 里重新验证一遍。"
      url: "https://keelinfra.io"
      style: "dark"
    - name: "keelapps"
      label: "Atlassian Marketplace"
      text: "Jira 与 Confluence Cloud 的权限审计、周期任务、定时报表和页面审批。"
      url: "https://keelapps.app"
      demo: "accesslens"
      demoLabel: "AccessLens for Jira 的演示动画：反向查询 contractors 用户组能访问的三个项目，然后在访问审查里确认两个、把匿名用户可浏览的项目标记为需整改，最后签核。"
      style: "wide"
      tone: "mint"
      flip: true
  moreLabel: "了解更多"
writing:
  title: "文章"
  text: "2017 年开始写，中英文双语。"
sponsor:
  text: "省了你的时间，欢迎赞助，让开源这部分持续维护。"
  label: "在 GitHub 上赞助"
  url: "https://github.com/sponsors/shenxianpeng"
---

## 关注公众号

中文文章同步发布在微信公众号「沈显鹏」，扫码关注。

{{< figure src="img/qrcode.jpg" alt="微信公众号「沈显鹏」二维码" class="mx-auto home-qrcode" nozoom="true" >}}
