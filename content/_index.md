---
title: "把软件稳稳发出去。"
heroTitle: "把软件稳稳<br>发出去。"
heroRole: "DevOps 与发布工程师，2009 年入行 · 维尔纽斯"
heroLead: "帮团队把软件稳稳发出去的开源工具，不管代码出自人还是 AI agent 之手，上游不管了也一样。"
heroButtons:
  - label: "看项目"
    url: "/zh-cn/portfolio/"
  - label: "读文章"
    url: "/zh-cn/posts/"
    style: "outline"
heroAlso:
  label: "从 commit 到 release，再到发布之后"
  stages:
    - stage: "commit"
      note: "提交信息、分支名和 AI 署名的统一策略"
      links:
        - label: "commit-check"
          url: "https://commit-check.com/"
        - label: "Conventional Branch"
          url: "https://conventionalbranch.org/"
    - stage: "review"
      note: "每个 PR 上跑 clang-format 和 clang-tidy"
      links:
        - label: "cpp-linter"
          url: "https://cpp-linter.github.io/"
          tag: "主打"
    - stage: "build"
      note: "用 AI 诊断 Jenkins 构建失败；让 Java 8 构建机接入新版 Jenkins"
      links:
        - label: "explain-error"
          url: "https://github.com/jenkinsci/explain-error-plugin"
        - label: "Agent8"
          url: "https://keelinfra.io/jenkins/"
    - stage: "release"
      note: "SBOM、签名的构建溯源、在野漏洞监控，对应欧盟《网络弹性法案》"
      links:
        - label: "release-ledger"
          url: "https://keelinfra.io/cra/"
    - stage: "support"
      note: "给最后一个支持 Java 17 的 Jenkins LTS 补安全修复；持续维护的 MkDocs 1.x"
      links:
        - label: "Jenkins Extended Security"
          url: "https://github.com/keelinfra/jenkins-extended-security"
        - label: "MkDocs NG"
          url: "https://mkdocs-ng.org/"
proof:
  stats:
    - value: "75 万+"
      label: "clang-tools 静态二进制累计下载"
    - value: "1000+"
      label: "个 GitHub 仓库依赖 cpp-linter"
    - value: "5.5 万+"
      label: "commit-check 每月 PyPI 下载"
    - value: "Jenkins 组织"
      label: "成员，jenkinsci 下有两个项目"
    - value: "前 3"
      label: "立陶宛公开贡献排名"
  usersLabel: "这些机构的项目在用 cpp-linter"
  users: ["AWS", "Apache", "Samsung", "Qualcomm", "Bloomberg", "LLNL", "Nextcloud"]
flagship:
  label: "cpp-linter"
  title: "每个 PR 都自动检查。"
  text: "在每个 PR 上跑 clang-format 和 clang-tidy，提供 GitHub Action、pre-commit hook 和 Python 包三种用法。修改建议直接出现在代码审查里，点一下就能提交。"
  chips: ["PR 评论", "审查建议", "步骤摘要", "自动修复"]
  chipActive: "审查建议"
  links:
    - label: "文档"
      url: "https://cpp-linter.github.io/"
    - label: "GitHub"
      url: "https://github.com/cpp-linter"
  demo: "cpp-linter-review"
  demoLabel: "cpp-linter 在 GitHub PR 上的效果：github-actions 对 src/demo.hpp 给出一条 clang-format 修改建议，把构造函数的初始化列表拆成多行，下面是 Commit suggestion 按钮，cpp-linter 检查通过。"
features:
  - label: "commit-check"
    title: "提交策略即代码。"
    text: "提交信息、分支名、作者、签署、标签、文件和 AI 署名，一份配置文件统一检查。可以跑在 CI 里、pre-commit 里，也可以让 AI agent 读它的 JSON 输出。"
    chips: ["GitHub Action", "pre-commit hook", "--format json", "AI 署名"]
    chipActive: "--format json"
    links:
      - label: "commit-check.com"
        url: "https://commit-check.com/"
      - label: "GitHub"
        url: "https://github.com/commit-check/commit-check"
    demo: "commit-check"
    demoLabel: "终端演示：把提交信息 “Fix: add streaming support” 交给 commit-check，并加上 --format json。输出的 checks 数组里失败的那一项，规则是 CC001，状态是 fail，建议改用 “fix: add streaming support”。"
    flip: true
products:
  title: "掌握在你自己手里的基础设施。"
  text: "给 Java 8 构建机用的 Jenkins agent，还有备份到你自己存储的 Mac 备份工具。"
  also: "另外还有 [keelapps](https://keelapps.app)：Jira 与 Confluence Cloud 的管理应用，在 Atlassian Marketplace 上架。"
  items:
    - name: "keelinfra"
      label: "免费 · 开源 · 提供付费支持"
      text: "Agent8 让 AIX、Solaris、HP-UX 构建机继续作为普通节点接入新版 Jenkins。"
      url: "https://keelinfra.io/jenkins/"
      preview: "agent8"
      style: "card"
      tone: "dark"
    - name: "Keelhaven"
      label: "免费 · 开源 · macOS 14+"
      text: "把 Mac 备份到你自己的存储。基于 restic 的菜单栏应用，文件离开 Mac 前就已加密。"
      url: "https://keelhaven.app"
      preview: "keelhaven"
      style: "card"
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
