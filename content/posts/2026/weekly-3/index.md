---
title: 攻城狮周刊（第 3 期）：AI 与平台工程的深度融合，重塑开发者未来
summary: 这里记录每周值得分享的 DevOps 与 AI 技术内容，周五发布。本杂志开源，欢迎投稿。
tags: 
  - Thoughts
translate: false
authors: 
  - shenxianpeng
draft: true
date: 2026-01-09
---

这里记录每周值得分享的 DevOps 与 AI 技术内容，周五发布。

> 抱歉本周迟了一天发布是因为孩子生病了。

本杂志[开源](https://github.com/shenxianpeng/weekly)，欢迎[投稿](https://github.com/shenxianpeng/weekly/issues)。合作请[邮件联系](mailto:xianpeng.shen@gmail.com)（xianpeng.shen@gmail.com）。

## 本周封面

![封面图](featured.png)


## 



## 行业动态

1、**CES 2026 聚焦 AI 与机器人，消费电子步入智能新纪元**

![LG Robot](ces2026-robot.jpg)

2026 年国际消费电子展（CES）1 月 6 日在拉斯维加斯开幕，AI 和机器人成为焦点。从 AI 家用机器人到智能家居，从显示技术到边缘计算，AI 正在成为消费电子的核心。LG 展示了"情感智能"机器人，三星、索尼等也推出了 AI 新品。NVIDIA 发布了 G-Sync Pulsar 显示技术和 DLSS 4.5，Intel 推出 Panther Lake AI 芯片，摩托罗拉发布搭载 AI 的可折叠手机 Razr Fold。

2、[**平台工程市场正处于高速增长期，预计 2035 年达到约 473 亿美元规模**](https://www.cervicornconsulting.com/platform-engineering-market)

![Platform Engineering Market Size](platform-engineering-market-size.png)

根据最新报告，全球平台工程服务市场将从 2025 年的 57.6 亿美元增长到 2035 年的 473.2 亿美元，复合年增长率达 23.4%。平台工程已从新兴概念发展为软件开发的核心。目前 55% 的组织已采纳平台工程实践，通过内部开发者平台（IDP）提升生产力、管理系统复杂性。

3、[**OpenAI 发布 AI 在医疗健康领域的报告，强调 AI 作为医疗盟友的潜力**](https://cdn.openai.com/pdf/2cb29276-68cd-4ec6-a5f4-c01c5e7a36e9/OpenAI-AI-as-a-Healthcare-Ally-Jan-2026.pdf)

![AI as a Healthcare Ally](ai-as-a-healthcare-ally.png)

OpenAI 在 1 月发布了 AI 医疗健康报告，数据显示全球超过 5% 的 ChatGPT 消息与医疗相关，每周有四分之一用户咨询医疗问题。报告强调 AI 在加速科学发现、强化医疗基础设施、支持医护人员等方面的潜力。OpenAI 计划发布完整的医疗保健政策蓝图，通过安全连接全球医疗数据，加速药物研发和治疗创新。

## 深度阅读

1、[**当AI编写几乎所有代码时，软件工程会发生什么？**](https://newsletter.pragmaticengineer.com/p/when-ai-writes-almost-all-code-what)

![AI Writing Code](ai-assisted-coding.png)

Pragmatic Engineer 创始人 Gergely Orosz 的开年长文，探讨 AI 编码工具的颠覆性影响。文章记录了多位大佬的"顿悟时刻"：Andrej Karpathy 从批评 AI 工具为"垃圾"到承认"从未如此落后"；Boris Cherny 一个月内提交的代码全由 AI 生成；Malte Ubl 断言"软件生产成本趋向于零"。

对软件工程师来说，2026 年最重要的技能不再是"写代码"，而是"指导 AI 写代码"。

2、[**2026年开发者工作流的25款AI编码工具**](https://devin-rosario.medium.com/25-ai-coding-tools-for-dev-workflows-in-2026-28ffc7384306)

![25 Tools](25-tools.png)

Devin Rosario 在 Medium 上详细介绍了 25 款 AI 编码工具。文章指出，软件开发已从"AI 辅助"进入"AI 编排"时代，高级工程师现在管理自主代理来处理复杂重构和安全补丁。

重点提到了 Cursor 这个 AI 原生代码编辑器，支持跨文件编辑和重构，以及 Cody AI 结合代码搜索和 AI 理解的能力。

3、[**塑造2026年的6大软件开发和DevOps趋势**](https://dzone.com/articles/software-devops-trends-shaping-2026)

![AI DevOps Trend 2026](ai-devops-2026.png)

Boris Zaikin 在 DZone 概述了 2026 年软件开发和 DevOps 的六大趋势：AI 代理、语义层、平台工程、供应链安全、可观测性和 FinOps。重点是平台工程 2.0 向 AI 就绪平台的演进，以及供应链安全成为 DevSecOps 新基线。

4、[**OpenTelemetry能否拯救2026年的可观测性？**](https://thenewstack.io/can-opentelemetry-save-observability-in-2026/)

![OpenTelemetry](opentelemetry.png)

The New Stack 聚焦 2025 年爆发的可观测性危机：84% 的企业被遥测成本和复杂性困扰。当前可观测性面临成本失控、复杂度爆炸、供应商锁定三大问题。

AI 在其中扮演双重角色：一方面 AI 工作负载带来更多监控复杂性，另一方面 AI 技术能帮助降低数据量和成本。

5、[**容器vs虚拟机:2026年家庭实验室的转变**](https://www.virtualizationhowto.com/2025/12/why-containers-will-be-more-important-than-ever-in-the-2026-home-lab/)

![Containers vs VMs](homelab.png)

Virtualization Howto 观察到一个有趣趋势：家庭实验室（Home Lab）爱好者正从虚拟机转向容器优先架构。驱动因素包括资源限制（AI 模型和大型应用消耗大量 RAM，虚拟机开销难以承受）、快速部署（容器秒级启动 vs 虚拟机分钟级）、以及 Kubernetes 技能成为职场必备。

关键观察：许多人开始用单个虚拟机运行 Kubernetes，然后在 K8s 上部署所有应用作为容器，而不是为每个服务创建单独虚拟机。这种方式既保持隔离性，又最大化资源利用率。

## 效率工具

1、**[6 个轻量级 Docker 容器，每周节省数小时](https://www.xda-developers.com/tiny-docker-containers-that-save-hours-every-week/)**

XDA Developers 推荐的 6 个超轻量级 Docker 容器，通过自动化日常任务提升生产力。

![IT Tools](it-tools.png)

这些容器体积小（几十 MB）、资源占用低、启动快，适合在家庭服务器或 VPS 上长期运行。

2、**[4 个 Docker 容器通过 Chrome 扩展增强功能](https://www.xda-developers.com/docker-containers-with-chrome-extensions/)**

![](docker-chrome-extensions.png)

XDA Developers 介绍了 4 个自托管 Docker 容器，通过浏览器扩展实现更好的工作流集成。这些工具的优势是数据完全自主可控，避免隐私风险和订阅费用，同时保持与云服务相当的体验。

3、**[Valkey 发布官方 Kubernetes Helm Chart](https://valkey.io/blog/valkey-released-helm-chart/)**

![Valkey](valkey.png)

Valkey（Redis 的开源分支）发布官方 Kubernetes Helm Chart。这是继 Bitnami 宣布政策变更后，社区维护的官方版本。支持 Standalone、Replicated、Sentinel 等部署模式，提供 ACL 和 TLS 加密、Prometheus metrics 集成、持久化存储配置。

4、[**n8n**](https://n8n.io/)

![n8n](n8n.png)

n8n 是开源工作流自动化工具，类似 Zapier 和 Integromat，但更灵活且可自托管。支持超过 200 种应用集成，通过可视化界面创建自动化工作流。

## AI 相关

1、**Meta 的"Conversation Focus"**

![Conversation Focus](conversation-focus.png)

Meta 在 2025 年 12 月为 Ray-Ban Meta 和 Oakley Meta HSTN 智能眼镜发布的 v21 更新功能。利用 AI 音频处理技术，在嘈杂环境中放大你正在看的人的声音，同时抑制背景噪音，解决"鸡尾酒会问题"（在嘈杂环境中选择性聆听特定人说话的能力）。

## 学习资源

1、[如何构建个人 Python 学习路线图](https://realpython.com/build-python-learning-roadmap/)

![Python Learning Roadmap](realpython.png)

Real Python 的系统性指南，教你制定个人化 Python 学习计划。基于 Dominican 大学 Gail Matthews 博士的目标设定研究，提供三个步骤。核心观点："为什么"比"做什么"更重要，没有强烈目的感很难在遇到困难时坚持。

提供免费 PDF 学习路线图模板，可打印填写。

2、[2026 年 1 月最佳免费 AI 培训课程](https://tech.co/news/best-free-ai-courses-january-2026)

Tech.co 整理的 2026 年 1 月最佳免费 AI 培训课程清单，涵盖从生成式 AI 基础到提示工程、机器学习和大型语言模型（LLMs）实际应用。包括杜克大学的"GenAI 基础 – LLMs 如何工作"和 Udemy 的"AI 基础：从基础到生成式 AI"等课程。

3、[2026 年工程师应学习的顶级 AI 技能](https://www.morson.com/blog/top-ai-skills-engineers-should-learn-2026)
![Top AI Skills 2026](ai-skills.png)

Morson Jobs 列出了 2026 年工程师最应学习的 AI 技能，包括 Python 熟练度、LLM 微调、MLOps、机器学习、深度学习和数据分析。强调提示工程、数据和自然语言处理（NLP）工程、云 AI 平台、计算机视觉以及 AI 伦理等关键领域。AI 正在重新定义"优秀"的工程实践，工程师需要学会智能地应用 AI 提高决策质量和减少重复工作。

## 精彩摘要

1、"我从未感到作为程序员如此落后。这个职业正在被大幅重构，程序员贡献的代码越来越稀疏。我有种感觉，如果我能恰当地串联起过去一年所出现的工具，我可以强大 10 倍，而未能获得这种提升明显是一个技能问题。"
—— Andrej Karpathy，OpenAI 联合创始人

2、"上个月是我作为工程师的第一个月，完全没有打开 IDE。Opus 4.5 写了大约 200 个 PR，每一行代码都是它写的。软件工程正在发生根本性变化，即使对于像我们这样的早期采用者和从业者来说，最困难的部分是持续重新调整我们的期望。而这仍然只是开始。"
—— Boris Cherny，Claude Code 创建者

3、"软件生产的成本正在趋向于零。"
—— Malte Ubl，Vercel CTO

## 行业观点

1、你不能因为充斥着“垃圾内容”和令人尴尬的产出，就否认 AI 所带来的奇迹。无论这些噪音多么刺耳，这仍然是自我们把计算机连接到互联网以来，最令人兴奋的一次技术飞跃。如果你在 2025 年对 AI 感到悲观或怀疑，也许可以在 2026 年，用一点乐观与好奇重新审视它。
—— DHH，Ruby on Rails 创建者

从怀疑到拥抱，DHH 的态度转变代表了许多资深开发者的心路历程。

2、"AI 不会终结工程职业，它正在对它们进行分类。" —— Morson Jobs

这个观点准确概括了当前趋势：AI 不是取代工程师，而是重新定义"优秀工程师"的标准。那些能够有效利用 AI 工具、具备产品思维、掌握架构能力的工程师将更有价值，而仅仅是"代码编写者"的角色将逐渐消失。

（完）