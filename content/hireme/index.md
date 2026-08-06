---
title: "沈显鹏的简历"
author: shenxianpeng
aliases:
  - /resume-cn
showDate : false
showDateOnlyInArticle : false
showDateUpdated : false
showHeadingAnchors : false
showPagination : false
showReadingTime : false
showTableOfContents : true
showTaxonomies : false
showWordCount : false
showSummary : false
sharingLinks : false
showEdit: false
showViews: false
showLikes: false
showAuthor: true
layoutBackgroundBlur: false
layoutBackgroundHeaderSpace: false
---

## 个人简介

DevOps / AI 工程师，现居立陶宛维尔纽斯。十六年软件工程经验，走过 QA → 测试开发 → DevOps 的完整路径，2015 年起在 Rocket Software 深耕构建、发布与交付自动化，目前负责企业级 **Agentic DevOps** 应用开发——让 AI agent 在受控工作流中理解代码、调用工具、完成真实的工程任务。

业余是活跃的开源作者：创建并维护 6 个开源组织，我写的工具每天跑在 **Microsoft、Apache、NASA、Samsung、Bloomberg、Qualcomm** 等数百个项目的 CI 里。

**核心亮点**

- 开源 C/C++ 质量工具 [cpp-linter](https://github.com/cpp-linter) 被数百个知名项目采用，包括 Microsoft、Apache、NASA、Samsung、Bloomberg、Qualcomm、Jupyter
- Jenkins **官方插件**（[Explain Error](https://github.com/jenkinsci/explain-error-plugin)）作者，Jenkins GitHub 组织成员
- **Anthropic Open Source Developer Program** 入选者（2026）
- **EuroPython 2025** 议题评审
- 累计发布 250+ 篇原创技术文章（[博客](https://shenxianpeng.github.io) + 公众号「沈显鹏」），2026 年起周更《攻城狮周刊》

---

## 工作经历

**高级 DevOps 工程师** | Rocket Software，立陶宛 | _2024.07 – 至今_

- 开发企业级 **Agentic Application**：基于 **GitHub Copilot SDK** 构建任务执行型 AI agent，连接代码理解、任务编排、工具调用与结果反馈，服务开发者日常工作流。
- 把 AI 落进 CI/CD 的具体环节：构建失败自动分析、代码维护、文档更新——不是做演示，是进流水线。
- 在团队内推动成熟 DevOps 实践与 AI 辅助工具的结合，持续改进交付体系。

**DevOps 工程师** | Rocket Software，大连 | _2015 – 2024.06_

- 主导 CI/CD 转型：多条产品线从手工构建和 Bamboo 迁移到 **Jenkins + 共享库**，构建逻辑全部代码化。
- 用 **Ansible** 实现基础设施即代码，自动化部署 Jenkins 与开发环境。
- 容器化企业级产品：buildx 多架构构建、健康检查、**Kubernetes** 部署。
- 设计 **DevOps 成熟度徽章**体系并推广到部门级；推动 **Conventional Commits** 在多团队落地。
- 用 Jira + Python 自动化虚拟机管理，被全公司采用。
- 为多条产品线引入**代码覆盖率**报告，让质量可见。
- 多次获得 **Rocket Build Award**，多项方案被纳入产品路线图。

**测试开发工程师** | 京东，北京 | _2012 – 2014_ — 自动化测试与持续集成流水线。

**QA 工程师** | SIMCOM（上海）、东软（北京） | _2009 – 2011_ — 测试用例设计与执行，带领小型 QA 团队。

---

## 开源项目

**[cpp-linter](https://github.com/cpp-linter)** — C/C++ 代码质量自动化：clang-format + clang-tidy，以 GitHub Action 和 pre-commit hook 交付。被 Microsoft、Apache、NASA、Samsung、Bloomberg、Qualcomm、Jupyter 等数百个项目用于日常 CI。

**[commit-check](https://github.com/commit-check)** — Git 提交元数据的策略引擎：一份版本化的 TOML 策略，统一校验提交信息、分支命名、作者身份、signoff 与 **AI 署名**，在本地 hook、CI、GitHub Actions 与 AI 自动化之间共享同一套规则。

**[conventional-branch](https://github.com/conventional-branch)** — Git 分支命名规范与工具集，1.1.0 起原生支持 **AI Coding Agent** 分支前缀，为人和 AI 共存的仓库提供统一约定。

**[Explain Error](https://github.com/jenkinsci/explain-error-plugin)** — Jenkins 官方插件：AI 分析构建失败原因，支持 **AI Auto-Fix 自动创建修复 PR**、用量统计与配额管控，兼容 OpenAI、Gemini、Azure OpenAI、DeepSeek、Qwen、Ollama、AWS Bedrock 等 Provider。

**[Open Delivery Spec](https://github.com/open-delivery-spec)** — 检测、分析和治理 AI 生成代码的开源规范与工具集：AI 代码检出、质量评分、策略门禁，作为 CI 质量门运行（本博客仓库的每个 PR 都在用它）。

**其他**：[devops-maturity](https://github.com/devops-maturity)（DevOps 成熟度评估与徽章）、[MkDocs NG](https://github.com/mkdocs-ng)（延续 MkDocs 生态的社区维护）、[gitstats](https://github.com/shenxianpeng/gitstats)（Git 仓库统计可视化）、[jenkinsfilelint](https://github.com/shenxianpeng/jenkinsfilelint)（无需 Jenkins 服务器的 Jenkinsfile 校验）。

---

## 技能

- **工程实践**：CI/CD、构建与发布、容器化（Docker / Kubernetes）、基础设施即代码（Ansible）、代码质量与覆盖率、软件供应链安全（SLSA / SBOM）
- **AI 工程**：Agentic 应用开发、GitHub Copilot SDK、LLM 集成（OpenAI / Gemini / Bedrock / Ollama 等）、AI 代码治理
- **语言**：Python、Shell、Groovy、Go
- **平台**：Jenkins、GitHub Actions、Linux、Windows、AIX 等企业级环境

---

## 社区与分享

- **写作**：250+ 篇原创技术文章，覆盖 DevOps、AI、CI/CD 与开源实践；《攻城狮周刊》每周更新
- **社区**：EuroPython 2025 议题评审；PyCon Lithuania 2025 全程参会并发布三篇大会记录；Jenkins、MkDocs 生态维护者
- **认可**：Anthropic Open Source Developer Program 入选者；GitHub Arctic Code Vault Contributor

---

## 语言

- 中文 — 母语
- 英语 — 专业工作水平
- 立陶宛语 — 初级（A1）

---

## 教育经历

- 辽宁交通高等专科学校 | 软件技术专业 | _2006 – 2009_

---

## 联系我

如果你的团队在找一个能把 AI 真正落进交付流程、而不是停在演示阶段的工程师，欢迎联系：

- 邮箱：[xianpeng.shen@gmail.com](mailto:xianpeng.shen@gmail.com)
- GitHub：[@shenxianpeng](https://github.com/shenxianpeng)
