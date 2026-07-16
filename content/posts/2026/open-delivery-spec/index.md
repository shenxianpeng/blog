---
title: Open Delivery Spec：我为 AI 写的代码做了一道 CI 质量门
summary: |
    过去几个月我业余做了一个开源组织 Open Delivery Spec (ODS)。起因是 AI 生成的代码越来越多，但团队缺乏可靠的治理手段。本文基于项目真实现状，记录思路、进展与边界，不做任何夸大。
tags:
 - AI
 - DevOps
 - ODS
 - Open Source
authors:
 - shenxianpeng
date: 2026-07-17
---

过去几个月，我在业余时间启动了一个新的开源项目——[Open Delivery Spec](https://github.com/open-delivery-spec)（简称 ODS）。这篇文章想诚实地介绍它：为什么做、怎么做、目前能做到什么，以及它做不到什么。

## 一个被忽视的细节

使用 Claude Code、GitHub Copilot 或 Cursor 提交代码时，你大概率会在 git log 中看到它们自动添加的这一行：

```text
Co-Authored-By: Claude <noreply@anthropic.com>
```

很多开发者其实见过这个细节，但**真正把它系统性读出来、并在 CI 质量门中用起来的团队却很少**。

另一边，大量团队的 AI 使用规范仍然停留在 PR 模板里的手动勾选框：“本 PR 包含 AI 生成的代码”，靠开发者自觉申报，却几乎没有工具去校验或消费这个信息。

一边是可靠、自动、机器可读的信号，躺在 git 历史里沉睡；另一边是不可靠的手动流程，却成了治理的主要依赖。这正是 ODS 想弥合的差距。

## Linux kernel 选择了同一条路

最近，Linux kernel 官方文档 [Documentation/process/coding-assistants](https://docs.kernel.org/process/coding-assistants.html) 将 AI 归属标准化为 commit trailer：

```text
Assisted-by: Claude:claude-3-opus coccinelle sparse
```

带工具名、模型版本和辅助工具。这么严肃的项目选择用 trailer 声明 AI 参与，坚定了我对 ODS 技术路线的信心。ODS 已完整支持 `Assisted-by` 与 `Co-Authored-By`，并将解析结果纳入证据链。

## 先说清楚：是“归属”，不是“检测”

ODS **不做代码风格检测**。这类检测在行级别误报率通常过高，无法用于有实际后果的场景。

ODS 依赖的是 **AI 工具自己声明的归属信息**。如果开发者 squash 提交并抹掉 trailer，ODS 无法发现。它不是测谎仪，而是一本“工具申报了什么”的可靠台账。这对团队治理来说，反而是更务实的基础。

项目文档里我特意写了一句话：**ODS 是 signal producer（信号生产者），不是 quality oracle（质量裁判）**。PASS 只代表未触发策略规则，不代表代码无问题。

## ODS 组织架构

目前主要由三个仓库组成：

- **[spec](https://github.com/open-delivery-spec/spec)**：核心规范、JSON Schema、策略契约和一致性测试套件。
- **[cli](https://github.com/open-delivery-spec/cli)**：Go 实现的参考 CLI（`ods detect / analyze / score / check`）。
- **[validate-action](https://github.com/open-delivery-spec/validate-action)**：开箱即用的 GitHub Action。

多个项目已在 dogfooding，包括 devops-maturity 和 conventional-branch（完整列表见 [ADOPTERS.md](https://github.com/open-delivery-spec/spec/blob/main/ADOPTERS.md)）。

典型 PR 流程四步：

1. **Detect**：识别 AI 参与（trailer、PR 描述等）
2. **Analyze**：聚合质量问题（内置规则 + SARIF 导入）
3. **Score**：计算技术债（AI 参与作为风险加权）
4. **Check**：根据 Rego 策略决定放行/警告/拦截

接入只需一个 workflow：

```yaml
# .github/workflows/ods.yml
name: ODS AI Code Quality
on:
  pull_request:
    types: [opened, synchronize, reopened]
jobs:
  ods:
    runs-on: ubuntu-latest
    steps:
      - uses: open-delivery-spec/validate-action@v1
```

输出包括 PR 评论、Job summary、HTML 报告和质量徽章。支持 `semgrep: true` 时还会自动运行 Semgrep 并合并结果。

## 策略完全由你定义（OPA Rego）

这是 ODS 最坚持的设计：把“什么该拦”的决定权彻底交给团队。

使用 CNCF 项目 OPA 的 Rego 语言编写策略，输入是结构化 JSON（检测+分析+评分结果）。示例：

```rego
package ods.policy
default allow := true

# 高危问题一律拦截
deny[msg] {
    issue := input.issues[_]
    issue.severity == "high"
    msg := sprintf("%s: %s (%s:%d)", [issue.severity, issue.rule, issue.file, issue.line])
}
```

策略文件随代码一起版本管理、Review。修改规则不需要等工具发版。

## 真实案例：拦截命令注入漏洞

在 spec 仓库的 [walkthrough 示例](https://github.com/open-delivery-spec/spec/tree/main/examples/walkthrough) 中，AI 辅助变更引入了经典的 `subprocess.run(..., shell=True)` 隐患。Semgrep 通过 SARIF 报告后，ODS 策略直接拦截，CI 失败。修复后正常放行。

**分工明确**：发现漏洞的是 Semgrep，ODS 负责归属聚合和策略执行。

## 打分哲学：用 AI 不是罪

早期我曾把“AI 代码占比”直接算作债务，后来纠正了。现在的模型是：

- 基础债务来自真实质量信号（高危 issue、覆盖率缺口、重复等）
- AI 参与度仅作为有限风险乘数（1.0~1.5x）叠加
- 干净的 100% AI 变更得分接近 0

同时优化了小 PR 惩罚过重的问题——同一条发现代价一致，鼓励小步提交。

## 核心瓶颈：人工 Review 速度赶不上 AI 生成

这是所有重度使用 AI 编码团队迟早会面对的问题。字面意义上的“让人读得更快”无解。可行的方案是**把稀缺的人工注意力路由到真正需要的地方**。

ODS 支持在 Rego 中声明 `review_tier`（`auto` / `standard` / `elevated`），自动打标签、请求额外 reviewer。低风险变更可走快速通道（甚至自动合并），高风险自动升级。

## 边界与不足（重要）

- **归属可被规避**：squash + 改写 message 就能抹掉。ODS 度量的是“申报的 AI 使用”。
- **内置规则是兜底**：主力缺陷发现仍应依赖 Semgrep 等成熟工具（SARIF 接入）。
- **评分是启发式**：用自己的 Rego 策略覆盖默认值。
- **项目还年轻**：早期用户欢迎真实反馈。

## 写在最后

AI 写代码已是现实，agent 自主开 PR 也在发生。**PR 合并点是人类最后的、最重要的控制点**。

ODS 是一套开源装备：不阻拦、不猎巫，把已有信号读出来，把质量判断交给专业分析器，把政策决定权交给团队，把人工注意力集中到高风险处。

如果你仓库里已积累了大量 AI 署名数据，接入只需一个 workflow。欢迎试用、提 issue、给反馈——对现在的 ODS 来说，一条真实反馈胜过一颗 star（当然 star 也欢迎）。

- 规范与示例：https://github.com/open-delivery-spec/spec
- CLI：https://github.com/open-delivery-spec/cli
- GitHub Action：https://github.com/open-delivery-spec/validate-action

欢迎把这篇文章转给正在为 AI 代码治理头疼的同事。