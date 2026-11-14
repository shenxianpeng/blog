---
title: "A rule in AGENTS.md doesn't stop AI: one month of commits in 31 popular projects"
summary: |
  31 popular open source projects tell AI agents, in AGENTS.md or their contributing guide, not to add AI attribution to commits. A month later, 20 of the 25 projects that only wrote the rule down had violating commits on their main branch, 389 in total. The 4 projects that check the rule in CI had none. How I measured it, and why I think Everything as Code matters more now that AI writes the code.
tags:
  - AI
  - DevOps
  - Commit-Check
authors:
  - shenxianpeng
date: 2026-11-14
---

On November 7, JUnit merged [#6254](https://github.com/junit-team/junit-framework/pull/6254). The PR added an "AI Usage" section to [CONTRIBUTING.md](https://github.com/junit-team/junit-framework/blob/main/CONTRIBUTING.md) and, at the same time, a workflow.

One AI policy, written down two ways. "Say in the PR description how much AI you used" lives in CONTRIBUTING.md, and maintainers check it during review. "No AI attribution in commit messages" became a [workflow](https://github.com/junit-team/junit-framework/blob/main/.github/workflows/_forbid-ai-attribution.yml) that runs on every PR:

```yaml
- uses: commit-check/commit-check-action@d68e05baf9511853193e2749f8a64bf2a221619a # v2.22.0
  env:
    CCHK_AI_ATTRIBUTION: forbid
  with:
    message-ai-attribution: true
    branch: false
```

A disclosure first: I maintain [commit-check](https://github.com/commit-check/commit-check), the tool JUnit uses here. Seeing that PR made my day. Because it is my own tool, I stick to the data below and leave the conclusions to you.

For years I have pushed Everything as Code at work: builds, releases, environments, team conventions, anything that can be code should be code. The usual reasons are that it is repeatable, reviewable and auditable. I now think there is one more: more and more code is written by AI, and a rule that only lives in a document is something AI reads but does not always follow.

That is easy to say. I wanted to check it against data.

## How I measured it

- **Sample**: on November 14, 2026, the 1,000 most-starred GitHub repositories pushed to in the last month (no forks, no archived repos; the smallest has 29,000 stars).
- **Finding the rule**: download `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md` and `CONTRIBUTING.md` from each default branch, and keep the projects that explicitly say not to add AI attribution to commits, such as "do not add `Co-Authored-By: Claude`".
- **Making sure the rule was already there**: go back to the code as of October 15 and confirm the rule was in the repository by then.
- **Counting violations**: count the commits on the default branch between October 15 and November 14 that still carry AI attribution. Only the clearest forms count: a `Co-authored-by` trailer with Claude (`noreply@anthropic.com`), Cursor (`cursoragent@cursor.com`) or Copilot's noreply address, and Claude Code's "Generated with Claude Code" footer.
- **Looking for a check**: search each project with GitHub code search for a CI job or git hook that enforces the rule, then open each hit to confirm it.

## Results

Of the 1,000 repositories, **507** have a rule file written for AI (`AGENTS.md`, `CLAUDE.md` or `copilot-instructions.md`). In big projects, writing instructions for AI is now routine.

**31** of them said, before October 15, not to put AI attribution in commits. Thirty days later:

| Where the rule lives | Projects | Projects with violations | Violating commits |
|---|---:|---:|---:|
| Only in documents | 25 | 20 | 389 |
| Local git hook | 2 | 1 | 1 |
| CI check | 4 | 0 | 0 |

Of the 25 projects that only wrote the rule down, 20 were violated within a month, close to 20 commits per project on average. The largest numbers:

| Project | Rule (excerpt) | Violating commits in 30 days |
|---|---|---:|
| [BerriAI/litellm](https://github.com/BerriAI/litellm/blob/main/AGENTS.md) | Do not add `Co-Authored-By: Claude` or any Claude attribution to commit messages. | 73 |
| [tldraw/tldraw](https://github.com/tldraw/tldraw/blob/main/AGENTS.md) | Do not include AI attribution in commits, PR descriptions, issues, docs… | 46 |
| [reactive-resume](https://github.com/reactive-resume/reactive-resume/blob/main/AGENTS.md) | Never add AI attribution, co-author trailers naming AI tools… | 41 |
| [HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading/blob/main/CONTRIBUTING.md) | Do NOT add `Co-Authored-By:` trailers or AI-assistant attribution lines… | 38 |
| [vercel/next.js](https://github.com/vercel/next.js/blob/canary/AGENTS.md) | Do NOT add "Generated with Claude Code" or co-author footers to commits or PRs | 34 |
| [webpack/webpack](https://github.com/webpack/webpack/blob/main/AGENTS.md) | no `Co-authored-by` trailers | 33 |
| [elastic/elasticsearch](https://github.com/elastic/elasticsearch/blob/main/AGENTS.md) | Do not add "Co-Authored-By" or any AI attribution trailers to commit messages, by any means… | 23 |

One example from next.js: [#101225](https://github.com/vercel/next.js/pull/101225), merged on November 6, ends its commit message with:

```text
Co-authored-by: Claude Code (kimi-k3) <noreply@anthropic.com>
```

The project's `AGENTS.md` says "Do NOT add … co-author footers to commits or PRs".

On the other side, the 4 projects that check the rule in CI had no violations in those 30 days. Their checks are plain:

- [moby/moby](https://github.com/moby/moby/blob/master/.github/scripts/check-agent-coauthors.js): a JavaScript script that fails when any commit in a PR credits an AI agent through `Co-authored-by`.
- [nautilus_trader](https://github.com/nautechsystems/nautilus_trader/blob/develop/scripts/ci/check_commit_message.py): a Python script that matches names such as anthropic, claude, codex, copilot and cursor in `Co-authored-by` lines.
- [floci](https://github.com/floci-io/floci/blob/main/.github/workflows/pr-hygiene.yml): a workflow whose comment quotes the rule from CONTRIBUTING.md and AGENTS.md.
- [VoiceStudio](https://github.com/debpalash/VoiceStudio/blob/main/.github/scripts/agent_identities.py): a list of AI agent identities shared by the CLA check and the commit-identity check.

Of the two projects that use a local git hook, [FlClash](https://github.com/chen08209/FlClash/blob/main/tool/hooks/commit_msg.sh) had 0 and [OmniRoute](https://github.com/cheaper-inference/OmniRoute/blob/main/.husky/commit-msg) let 1 through. Every contributor has to install a local hook themselves, and the repository cannot see whether they did or whether they skipped it.

The result for each of the 31 projects is in [ai-attribution-rules-2026-11-14.csv](ai-attribution-rules-2026-11-14.csv).

## Why a written rule still gets broken

I did not trace how each of the 389 commits got in, so this section only covers what I can say for sure.

Most AI coding tools add attribution to commits by default. As I wrote in [July](/posts/2026/commit-check-ai-attribution/), Claude Code adds `Co-authored-by: Claude` by default, and Copilot, Cursor and Devin each have their own marker. Asking it in `AGENTS.md` not to do that means asking it to remember, on every commit, to go against its own default.

The human side is the same. Maintainers review the diff and rarely look at the last line of a commit message. A rule that only lives in a document depends on every review remembering to check it.

[cozystack](https://github.com/cozystack/cozystack/blob/main/hack/check-commit-trailers.sh) put a sentence at the top of their check script that I agree with:

> All three are review blockers decided by the text alone, which is exactly the kind of thing a human should not be spending a review round on.

Before turning their rules into a script, they ran it over every commit on main at the time: 6,062 commits, 1,300 rejected.

## Two layers of rules

Looking back at the data, I think rules for AI come in two layers.

The first layer tells AI what the rules are: `AGENTS.md` and files like it. Half of the 1,000 projects already have one, and it clearly matters: without it, AI does not even know the rule exists.

The second layer makes the rule impossible to break: a check that runs at commit time or in CI. Only 4 of the 31 projects got to CI, and all 4 had zero violations for the month. Five of the 25 document-only projects also had zero; the sample is small and I cannot tell why.

This is the extra reason I now see for Everything as Code: **a rule in a document is something AI reads; a rule in a check is something AI cannot get around.**

AI attribution is just the easiest rule to measure. Commit message format, branch names, directories nobody should touch, dependencies nobody should add: if a rule can be decided from the text or the diff alone, it can be handled the same way.

## Limits

1. **One rule only.** AI attribution is the easiest thing for a machine to judge; other rules may behave differently.
2. **The violation count is a floor.** I only counted three email addresses and one footer; other tools' attribution formats are not included.
3. **A check may have been missed.** GitHub code search is not complete, so some project may have a check I did not find. Still, 20 of the 25 document-only projects had violations, so whatever they had did not stop them.
4. **Conflicting rules.** Some projects word the rule differently in different files. Homebrew's CONTRIBUTING.md allows AI attribution alongside a human author, while its AGENTS.md tells agents not to add it. I counted a project if at least one file clearly forbids it.
5. **Biased toward big projects.** The smallest of the 1,000 repositories has 29,000 stars; this says little about typical projects.

## One thing you can do today

Go through your team's `AGENTS.md`, contributing guide or wiki, find one rule that can be decided from the text alone, turn it into a check and put it in CI.

If that rule happens to be AI attribution, commit-check does it with one line of configuration. If you would rather not add a dependency, a script of a hundred-odd lines like moby's works just as well. What matters is that it runs on every commit.
