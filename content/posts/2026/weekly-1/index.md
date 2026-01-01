---
title: 攻城狮周刊（第 1 期）：AI 工程化与 DevOps 韧性：2026 年技术发展双主线
summary: 这里记录每周值得分享的 DevOps 与 AI 技术内容，周五发布。本杂志开源，欢迎投稿。
tags: 
  - Weekly
translate: false
authors: 
  - shenxianpeng
date: 2026-01-01
---

这里记录每周值得分享的 DevOps 与 AI 技术内容，周五发布。

本杂志[开源](https://github.com/shenxianpeng/weekly)，欢迎[投稿](https://github.com/shenxianpeng/weekly/issues)。合作请[邮件联系](mailto:xianpeng.shen@gmail.com)（xianpeng.shen@gmail.com）。

## 本周封面

![](featured.png)

看龙家昇与他的精灵们，如何把怪异化作可爱，更亲揭 Labubu 九颗尖牙的设计巧思！

## AI 工程化与 DevOps 韧性

过去一周，技术领域最引人注目的趋势无疑是人工智能在工程实践中的深度融合，以及 DevOps 实践中对系统韧性的前所未有的关注。2025 年见证了 AI 模型从实验性工具转变为生产关键基础设施，这迫使 DevOps 团队开始像管理数据库一样思考 AI 模型的延迟、成本和服务等级协议（SLA）。谷歌发布的 Gemini 3 Flash 模型，以及 Z.ai 的 GLM-4.7 和 MiniMax 的 M2.1 等模型的更新，进一步推动了 AI 在编码、任务自动化和多语言编程中的应用，预示着 AI 优先的云平台将成为 2026 年的主导趋势。

与此同时，随着 AI 驱动的交付加速了发布周期和产出量，DevOps 团队也面临着新的挑战：如何在追求速度的同时，确保软件部署的安全性与可靠性。2025 年的经验表明，基础设施的脆弱性通过连锁中断暴露无遗，促使企业重新审视其技术堆栈的韧性。平台工程和内部开发者平台（IDP）的兴起，旨在通过提供标准化、自服务的“铺设之路”，减少手动工作，并为安全与合规提供统一的控制平面，从而提升整体韧性。2026 年，DevOps 的成功将不再仅仅取决于软件交付的速度，更将取决于系统应对持续变化和需求的能力，韧性将成为新的衡量标准。

## 行业动态

1、[AI 模型进入生产核心：成本与性能成为关键考量](https://www.datastudios.org/post/google-gemini-3-vs-chatgpt-5-2-full-report-and-comparison-of-features-performance-pricing-and-mo?utm_source=chatgpt.com)

![](gemini-chatgpt.jpg)

2025 年末，AI 模型已不再是实验性工具，而是生产环境中的关键基础设施。谷歌的 Gemini 3.0 和 OpenAI 的 GPT 5.2 等大型语言模型（LLM）的发布，使得 DevOps 团队必须关注其延迟、请求成本、SLA 和供应商锁定等问题。例如，Gemini 3.0 的平均延迟为 2.1 秒，每月 100 万次请求的成本为 4.8 万美元，而 GPT 5.2 的平均延迟为 4.8 秒，成本则高达 33 万美元。这标志着 AI 已从研究问题转变为基础设施经济学问题。

**工程师视角的点评：** 这对 DevOps/AI 工程师意味着，LLM 的成本优化将像云成本优化一样成为常态。团队可能需要根据任务需求运行多个模型（例如，Gemini 用于高吞吐量，GPT 用于推理密集型任务），并且 LLM 可观测性和成本跟踪工具将迅速成熟。

2、[Kubernetes 成为 AI 工作负载的事实标准](https://securityboulevard.com/2025/12/2026-kubernetes-playbook-ai-at-scale-self%E2%80%91healing-clusters-growth/)

![](k8s+ai.png)

到 2026 年，最繁重的 AI 工作负载，特别是机器学习操作（MLOps）平台，将以 Kubernetes 为骨干。Kubernetes 提供了统一的控制平面来调度、扩展和管理 AI 组件，无论是突发性的资源密集型任务（数据处理和训练）还是高吞吐量的持续运行服务（实时推理）。这一趋势反映了 GPU 密集型工作负载的快速增长以及最大化昂贵加速器硬件利用率的需求。

3、[Google Cloud 与 Palo Alto Networks 达成百亿美元安全合作](https://www.cnbc.com/2025/12/19/palo-alto-networks-google-cloud-ai-threats.html)

![](paloalto.png)

2025 年 12 月 22 日，Google Cloud 和 Palo Alto Networks 宣布了一项近 100 亿美元的合作，这是历史上最大的云安全交易。Palo Alto 将其工作负载迁移到 GCP，并利用 Gemini AI 为其安全协处理器提供支持。

4、**其他**

（1）[RondoDox Botnet 利用 React2Shell 漏洞](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHyDa8Gw5HzDMOToLjouW4VA57zurQQMonVi7vraOemRHd9HlO3-qNIHXz-leldg0I9v4-E5m-l23w1EvKf3OCoOqGFi0fSRluMJ6U0UDTbvGQbmCQZ)

![](react2shell.png)

网络安全研究人员披露了一个持续九个月的 RondoDox 僵尸网络活动细节，该僵尸网络利用最近披露的 React2Shell（CVE-2025-55182，CVSS 评分：10.0）漏洞劫持 IoT 设备和 Web 服务器。

（2）[Stack Overflow 2025 开发者调查：开发者对 AI 仍持谨慎态度](https://survey.stackoverflow.co/2025/)

![](stackoverflow-survey.png)

Stack Overflow 于 2025 年 12 月 29 日发布了开发者调查结果，显示开发者仍然愿意使用 AI，但AI工具的积极评价在2025年呈现下降趋势。

## 深度阅读

1、[2025 年 DevOps 年度回顾：五大基础设施转变及其对 2026 年的意义](https://medium.com/@inboryn/2025-devops-year-in-review-the-5-biggest-infrastructure-shifts-and-what-they-mean-for-2026-ffb7a6735139)（英文）

![](devops-review.png)

这篇文章回顾了 2025 年 DevOps 领域的五大基础设施转变，包括 AI 模型进入生产、云安全重塑、平台工程成为必需、eBPF 的普及以及厂商锁定的回归。文章深入分析了这些转变对 2026 年的影响，强调了 LLM 成本优化、云安全作为差异化因素以及平台工程的重要性。

2、[现代 DevOps CI/CD 管道内部：自动化、工具和最佳实践](https://mantraideas.com/cicd-pipeline-implementation-guide-2025/)（英文）

![](cicd.png)

这篇发布于 2025 年 12 月 31 日的文章探讨了现代 DevOps CI/CD 管道的工作原理、涉及的工具以及构建可扩展和可靠管道的最佳实践。它强调了持续反馈循环、模块化管道设计、左移安全以及微服务架构下的独立部署等关键要素。

3、[MLOps：2025 年部署和监控机器学习模型](https://dasroot.net/posts/2025/12/mlops-deploying-monitoring-ml-models-2025/)（英文）

该文章聚焦于 2025 年 MLOps 在企业环境中部署和监控机器学习模型，强调了可扩展性和可靠性。它介绍了 ModelBit 3.2 和 Control Plane 等 MLOps 工具，以及实施最佳实践和现实世界应用。

## 效率工具

1、[LangChain](https://github.com/langchain-ai/langchain)

![](langchain.png)

一个开源框架，用于连接大型语言模型与外部数据源，简化和加速 AI 应用和代理的开发。LangChain 1.0 于 2025 年 10 月 22 日发布了第一个主要稳定版本。

2、[GoReleaser](https://github.com/goreleaser/goreleaser)

![](goreleaser.png)

自动化 Go 项目的打包、发布和分发，帮助开发者更快、更轻松地交付软件。

3、[Uptime Kuma](https://github.com/louislam/uptime-kuma)

![](uptime-kuma.jpg)

一个免费的开源服务器监控工具，支持容器化部署。

## AI 相关

1、[A2UI：Google 的代理驱动界面开放项目](https://github.com/google/a2ui)

![](a2ui_gallery_examples.png)

Google 于 2025 年 12 月 15 日公开了 A2UI 项目，这是一个用于代理驱动界面的开放项目。A2UI 旨在解决可互操作、跨平台、生成式或基于模板的代理 UI 响应的特定挑战，允许代理生成最适合当前对话的界面，并发送到前端应用程序。

2、[Moondream：小巧而强大的视觉语言模型](https://moondream.ai/)

![](moondream.png)

Moondream 是一个开源的视觉语言模型，体积小巧（1GB），性能卓越，无需 GPU 即可在笔记本电脑到边缘设备上运行。它允许开发者使用自然语言提示来标注图像、检测物体、跟踪视线、阅读文档等。该项目在 GitHub 上拥有数千颗星。

## 学习资源

1、[2025 年 DevOps 学习资源路线图](https://github.com/milanm/DevOps-Roadmap)

![](devops-roadmap.png)

KodeKloud 提供的 2025 年 DevOps 学习路线图，包含大量免费实验室、课程和指南。它涵盖了从 Linux 基础到 Git、脚本、容器、Kubernetes、IaC、CI/CD、云平台以及监控、安全和可观测性等全面的 DevOps 技能。

## 精彩摘录

1、[2025 年 DevOps 年度回顾](https://medium.com/@inboryn/2025-devops-year-in-review-the-5-biggest-infrastructure-shifts-and-what-they-mean-for-2026-ffb7a6735139)

“如果科技界的一年感觉像十年，那么 2025 年就是整整十年。DevOps 团队目睹了 AI 模型从实验性辅助工具变为生产关键基础设施，经历了历史上最大的云安全合作，并不得不弄清楚哪些‘下一个大事件’真正重要。当我们结束 2025 年时，以下是诚实的总结：真正改变我们构建、部署和操作系统的 5 大基础设施转变——以及它们对 2026 年的意义。”

## 行业观点

1、

“AI 现在是基础设施：它不再是实验性的。DevOps 团队拥有 LLM 的成本、延迟和 SLA。云安全再次变得重要：GCP 的 100 亿美元赌注证明了这一点。平台工程不是可选的：如果开发者还在与 Kubernetes YAML 搏斗，你就落后了。eBPF 赢了：网络、可观测性和安全都在 eBPF 上运行得更好。在 2026 年学习它。锁定又回来了：‘多云一切’的梦想已经破灭。”

-- Rick Whiting 在 CRN 上的评论，总结 2025 年的开源工具趋势。

2、

“2026 年，DevOps 的未来不会根据软件交付的速度来评判，而是根据其运行的可靠性来评判。韧性是新的速度——而运行时是其获得之处。”

-- Marcus Holm 在 Tech Monitor 上的评论，关于 2026 年 DevOps 的转变。

（完）