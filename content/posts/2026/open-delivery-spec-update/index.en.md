---
title: "Open Delivery Spec update: AI code shouldn't just pass the gate — it should leave evidence"
summary: |
    Three weeks ago I introduced Open Delivery Spec (ODS), my side project for governing AI-assisted code in CI. Since then the CLI has shipped 5 releases and grown two new pillars: deterministic merge-confidence signals that answer "is this AI PR safe to merge?", and an auto-generated, standards-based evidence document on every PR. As always, this post sticks to what actually ships — no hype.
tags:
 - AI
 - DevOps
 - ODS
 - Open Source
authors:
 - shenxianpeng
series: ["Open Delivery Spec"]
date: 2026-08-08
---

Three weeks ago I wrote about [Open Delivery Spec](open-delivery-spec/) (ODS): an open-source toolchain that reads the AI-attribution signals coding tools already leave in your git history (`Co-Authored-By`, `Assisted-by` trailers), aggregates quality analysis, and hands policy decisions to your team via OPA Rego.

If your reaction back then was "interesting, but not enough to adopt yet," this post is about what's changed. The short version — two new pillars:

1. **Merge confidence**: a set of deterministic signals (no LLM anywhere) that answer "is this AI PR safe to merge?" — did the tests change along with the code, are the changed lines actually covered, and can the tests actually catch faults.
2. **Evidence documents**: every PR now automatically produces an `evidence.cdx.json` — a valid CycloneDX document recording which code was AI-assisted, how strong the evidence is, and what verification it passed. Raw material for audits and compliance.

## What it looks like

Repos on `open-delivery-spec/validate-action@v1` now get a PR comment like this (excerpted from a real PR in ODS's own repos):

![ods-report-comment](ods-report-comment.png)

Every row is a **deterministic fact** computed from the diff and your test artifacts. Same inputs, same outputs, every time. Not a single line comes from "an AI thinks so."

## Pillar one: is this AI PR safe to merge?

In the last post I argued that human review can't keep pace with AI generation, and the only workable answer is routing scarce human attention to where it's actually needed. But routing based on *what*? I went through what maintainers are actually saying in public — the GitHub community discussions, the FastAPI and curl threads, the Linux kernel's coding-assistants doc — and two points of consensus stand out:

- **Nobody wants an LLM as the judge.** "Any detector good enough to identify AI code is good enough to train AI that evades it."
- The first question maintainers actually ask is disarmingly simple: **"does it have tests?"**

And the signature failure mode of AI code is exactly this: **coverage is green, assertions are hollow, logic is subtly wrong**. So ODS pursues the question "are the tests real?" through three deterministic layers, each stronger than the last:

**Layer one — pure diff signals (zero config, on by default).** Did source changes come with test changes? Is the diff a suspicious "wide but shallow" shape? Does it touch sensitive paths (CI config, auth, lockfiles)?

**Layer two — patch coverage (automatic if you produce coverage).** Not project-wide coverage — coverage of **the lines this change adds**. A project at 80% overall can happily merge new code with zero tests; patch coverage catches exactly that. Go `coverage.out`, LCOV, and Cobertura are auto-detected from the workspace; below the threshold (default 0.8) you get a warning.

**Layer three — mutation score (opt-in, the deepest layer).** Mutation testing deliberately plants bugs in your added lines and checks whether the tests notice — the most direct test of "are these assertions hollow?" Since mutation runs are heavy, ODS **ingests an existing report** rather than running one: generate it with a tool like [gremlins](https://github.com/go-gremlins/gremlins), pass it via `mutation-report`, and ODS computes the kill rate scoped to your diff.

All three layers follow the same rules: **advisory by default — warn and route, never block**; AI attribution raises the bar (AI-authored + low patch coverage → review tier escalates to `elevated`); teams that want hard blocking write one `deny` rule in their own Rego policy.

And the standing disclaimer still stands: none of this **proves correctness**. It proves the change is **tested, scanned, and shaped like real work** — the criteria maintainers already use by hand, turned into machine-readable, policy-consumable signals, so human attention stops being spent where the answer is already clear.

## Pillar two: leave evidence

This pillar has a date attached: **the EU AI Act's technical-documentation requirements (Article 11 / Annex IV) took effect on August 2, 2026.** "Which parts of your codebase were AI-assisted, with what tools, and what verification was applied?" is turning from an engineering question into a procurement and compliance question.

Here's the gap: the existing AI-BOM ecosystem (CycloneDX ML-BOM, OWASP AIBOM tooling) answers a *different* question — "which models and datasets are **components of** your system?" Nobody covers the layer where ODS lives: "which of your **source code** was AI-assisted, and how strong is the evidence?" ODS already computes every input that layer needs, on every PR.

So the CLI grew an `ods attest` command, and the Action runs it automatically on every PR, producing `evidence.cdx.json` — a document that **validates against the official CycloneDX 1.6 schema** (no proprietary format invented). At its core are six verifiable claims: AI involvement is disclosed (R1), evidence is graded (R2), changed lines are covered by tests (R3), tests catch faults (R4), policy was evaluated (R5), the pipeline ran intact (R6). Each claim looks like this:

```json
{
  "requirement": "req:ods-r3",
  "conformance": { "score": 0.75 },
  "confidence":  { "score": 0.9 }
}
```

The two scores are deliberately separate: `conformance` is the **measured value** (patch coverage measured at 75%), `confidence` is the **strength of the evidence behind it**. That strength comes from another capability shipped these three weeks — **evidence tiers**. The same "AI was involved" fact can rest on very different footing:

- 🟢 **corroborated**: backed by tool-measured, line-level records;
- 🟡 **attested**: actively declared by the tool or author (commit trailer, PR body);
- 🟠 **inferred**: circumstantial only (e.g. branch naming).

The PR comment shows this grade up front. Alongside it ships **pipeline integrity**: if any analysis stage fails, the report says so explicitly, marks results as potentially incomplete, and refuses to present a failure as a clean pass — **a report that can lie is worthless as evidence**. Every evidence entry carries a re-fetchable locator (the workflow-run URL), and the document states its own boundary in an affirmation: *attribution reflects signals volunteered by tools and authors; it is not forensic proof of authorship, and no claim asserts code correctness.*

Honestly: this is a starting point. The document isn't signed yet (GitHub artifact attestations / sigstore is the next phase), and release-level aggregation — "the evidence summary for all AI-assisted code in this release," the file an audit actually asks for — is on the roadmap. But as of today, every repo on `@v1` is accumulating this ledger automatically, one PR at a time.

## Bugs our own reports caught

Every ODS repo is gated by ODS itself, and in these three weeks its reports caught three real bugs in ODS. Two worth telling:

- A PR's report flagged "analyze stage exited abnormally" — which led straight to a CLI bug that conflated "docs-only change, nothing to analyze" with "analyzer crashed." **The pipeline-integrity check exposed a bug in its own upstream.**
- Another PR's report used outdated wording — revealing that our dogfooding workflow was pinned to a stale release. After fixing it we switched all dependency bots to daily checks, so upstream releases get picked up same-day.

I tell these stories to make one point: these reports aren't decoration. They're read as real signals — and that's the strongest evidence I have that the thing is worth anything.

## Getting started

Minimal setup is still one workflow:

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
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0   # full history — needed for diffs and attribution
      - uses: open-delivery-spec/validate-action@v1
```

That alone gets you: the PR report, evidence tiers, the pure-diff merge-confidence signals, and the `evidence.cdx.json` document. For the deeper signals, add ingredients as needed:

```yaml
      # Run tests with coverage before ODS → patch coverage lights up
      - run: go test ./... -coverprofile=coverage.out

      - uses: open-delivery-spec/validate-action@v1
        with:
          mutation-report: gremlins.json   # optional: mutation report → mutation score
          failure-mode: block              # optional: block when a pipeline stage fails (default: warn)
```

Existing users don't change anything: `@v1` rolls forward automatically, and the new capabilities show up on your next PR.

## Boundaries and limitations (still the important part)

- **Attribution can still be evaded**: squash away the trailers and it's gone. ODS measures *declared* AI use — evidence tiers exist precisely to price that uncertainty honestly, not to hide it.
- **Mutation score requires your own report**: ODS ingests and scopes it to the diff; it doesn't run mutation testing for you.
- **The evidence document isn't signed yet**: today it proves "CI computed these facts at that moment"; tamper-resistance arrives with the sigstore phase.
- **Patch coverage depends on coverage you already produce**: with no coverage file, the signal reads "not measured" — never a fake 0 or 100.

## Closing

The conclusion of the last post has only gotten more true: agents opening PRs autonomously is now routine, and **the merge point is the last, most important point of human control**. What ODS built in these three weeks arms that point better on both sides: before the merge, deterministic signals tell you whether this AI change deserves trust; after the merge, a standards-based evidence document is waiting when the auditors come asking.

If your team writes code with AI, the cost of trying this is one workflow file. If you've already adopted, just look at your next PR's report. And as before: **one piece of real feedback is worth more to ODS right now than a star** (stars welcome too).

- Spec & evidence-document proposal: https://github.com/open-delivery-spec/spec
- CLI: https://github.com/open-delivery-spec/cli
- GitHub Action: https://github.com/open-delivery-spec/validate-action

If a colleague of yours is wrestling with AI code governance or compliance, send this their way.
