---
title: Open Delivery Spec—I Built a CI Quality Gate for AI-Generated Code
summary: |
    Over the past few months, I've been working on an open-source organization called Open Delivery Spec (ODS) in my spare time. The initiative stemmed from the increasing volume of AI-generated code and the lack of reliable governance mechanisms within teams. This article records the thought process, progress, and boundaries based on the project's real-world status, without any exaggeration.
tags:
 - AI
 - DevOps
 - ODS
 - Open Source
authors:
 - shenxianpeng
date: 2026-07-17
---

Over the past few months, I've launched a new open-source project in my spare time—[Open Delivery Spec](https://github.com/open-delivery-spec) (ODS). This article aims to honestly introduce it: why I built it, how it works, what it can currently achieve, and what it cannot.

## An Overlooked Detail

When using Claude Code, GitHub Copilot, or Cursor to submit code, you'll most likely see this line automatically added in your git log:

```text
Co-Authored-By: Claude <noreply@anthropic.com>
```

Many developers have seen this detail, but **very few teams actually systematically interpret it and utilize it in their CI quality gates**.

Meanwhile, many teams' AI usage guidelines still rely on manual checkboxes in PR templates: "This PR contains AI-generated code," depending on developers' self-declaration, with almost no tools to verify or consume this information.

On one side, a reliable, automatic, machine-readable signal lies dormant in git history; on the other, an unreliable manual process becomes the primary reliance for governance. This is precisely the gap ODS aims to bridge.

## The Linux Kernel Chose the Same Path

Recently, the official Linux kernel documentation [Documentation/process/coding-assistants](https://docs.kernel.org/process/coding-assistants.html) standardized AI attribution as a commit trailer:

```text
Assisted-by: Claude:claude-3-opus coccinelle sparse
```

Including tool names, model versions, and assisting tools. Such a serious project choosing to use a trailer to declare AI involvement reinforced my confidence in ODS's technical approach. ODS fully supports `Assisted-by` and `Co-Authored-By`, incorporating the parsing results into the chain of evidence.

## To Be Clear: It's 'Attribution,' Not 'Detection'

ODS **does not perform code style detection**. Such detections typically have too high a false positive rate at the line level to be used in scenarios with actual consequences.

ODS relies on **attribution information declared by AI tools themselves**. If a developer squashes a commit and removes the trailer, ODS cannot detect it. It's not a lie detector, but a reliable ledger of 'what tools have declared.' For team governance, this is actually a more pragmatic foundation.

In the project documentation, I specifically wrote a sentence: **ODS is a signal producer, not a quality oracle**. PASS only means policy rules were not triggered, not that the code is problem-free.

## ODS Architecture

It currently consists of three main repositories:

-   **[spec](https://github.com/open-delivery-spec/spec)**: Core specification, JSON Schema, policy contracts, and conformance test suite.
-   **[cli](https://github.com/open-delivery-spec/cli)**: Reference CLI (`ods detect / analyze / score / check`) implemented in Go.
-   **[validate-action](https://github.com/open-delivery-spec/validate-action)**: Out-of-the-box GitHub Action.

Multiple projects are already dogfooding, including `devops-maturity` and `conventional-branch` (see [ADOPTERS.md](https://github.com/open-delivery-spec/spec/blob/main/ADOPTERS.md) for a complete list).

Typical PR process in four steps:

1.  **Detect**: Identify AI involvement (trailer, PR description, etc.)
2.  **Analyze**: Aggregate quality issues (built-in rules + SARIF import)
3.  **Score**: Calculate technical debt (AI involvement as a risk weighting)
4.  **Check**: Decide whether to allow/warn/block based on Rego policy

Integration requires just one workflow:

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

Outputs include PR comments, Job summary, HTML reports, and quality badges. When `semgrep: true` is supported, Semgrep will automatically run, and results will be merged.

## Policies Are Fully Defined By You (OPA Rego)

This is ODS's most steadfast design principle: completely handing over the decision-making power of 'what to block' to the team.

Policies are written using OPA's Rego language (a CNCF project), with structured JSON as input (detection + analysis + scoring results). Example:

```rego
package ods.policy
default allow := true

# Block all high-severity issues
deny[msg] {
    issue := input.issues[_]
    issue.severity == "high"
    msg := sprintf("%s: %s (%s:%d)", [issue.severity, issue.rule, issue.file, issue.line])
}
```

Policy files are version-controlled and reviewed along with the code. Modifying rules doesn't require waiting for tool releases.

## Real Case: Blocking Command Injection Vulnerability

In the [walkthrough example](https://github.com/open-delivery-spec/spec/tree/main/examples/walkthrough) of the spec repository, an AI-assisted change introduced the classic `subprocess.run(..., shell=True)` vulnerability. After Semgrep reported it via SARIF, the ODS policy directly blocked it, causing CI to fail. It passed normally after the fix.

**Clear division of labor**: Semgrep discovers vulnerabilities, ODS is responsible for attribution aggregation and policy enforcement.

## Scoring Philosophy: Using AI Is Not a Sin

Initially, I directly counted 'AI code percentage' as debt, but I later corrected this. The current model is:

-   Base debt comes from real quality signals (high-severity issues, coverage gaps, duplication, etc.)
-   AI involvement is only superimposed as a limited risk multiplier (1.0~1.5x)
-   Clean 100% AI changes score close to 0

At the same time, the problem of over-penalizing small PRs has been optimized—the cost for the same finding is consistent, encouraging small, incremental commits.

## Core Bottleneck: Human Review Speed Cannot Keep Up With AI Generation

This is a problem all teams heavily using AI for coding will eventually face. Literally making 'humans read faster' has no solution. A feasible approach is to **route scarce human attention to where it's truly needed**.

ODS supports declaring `review_tier` (`auto` / `standard` / `elevated`) in Rego, automatically tagging and requesting additional reviewers. Low-risk changes can go through a fast lane (even auto-merge), while high-risk changes are automatically escalated.

## Boundaries and Limitations (Important)

-   **Attribution can be circumvented**: Squashing and rewriting the message can erase it. ODS measures 'declared AI usage.'
-   **Built-in rules are a fallback**: Primary defect detection should still rely on mature tools like Semgrep (SARIF integration).
-   **Scoring is heuristic**: Override default values with your own Rego policies.
-   **The project is still young**: Early adopters are welcome to provide real feedback.

## In Closing

AI writing code is a reality, and agents autonomously opening PRs are also happening. **The PR merge point is humanity's last, most crucial control point**.

ODS is a set of open-source tools: it doesn't obstruct, it doesn't witch-hunt. It reads existing signals, delegates quality judgments to professional analyzers, hands policy decision-making power to teams, and focuses human attention on high-risk areas.

If your repository has already accumulated a lot of AI attribution data, integration only requires one workflow. We welcome you to try it out, raise issues, and provide feedback—for the current ODS, one genuine piece of feedback is worth more than a star (though stars are also welcome).

-   Specification and examples: https://github.com/open-delivery-spec/spec
-   CLI: https://github.com/open-delivery-spec/cli
-   GitHub Action: https://github.com/open-delivery-spec/validate-action

Feel free to share this article with colleagues who are struggling with AI code governance.