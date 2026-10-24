---
title: "After OVHcloud's Release Was Swapped: Three in Four Popular CLIs Could Be Too"
summary: |
  On 19 October, the files in OVHcloud CLI releases were replaced with a credential stealer using a developer's stolen credentials. I checked the latest release of 242 popular Go and Rust CLI projects: 179 could be swapped the same way, with nothing independent for a downloader to check. How I checked, why a checksum file doesn't count, and three things maintainers can do.
tags:
  - DevSecOps
  - SLSA
  - GitHub
authors:
  - shenxianpeng
date: 2026-10-24
---

On the afternoon of 19 October, someone used a developer's stolen GitHub credentials to replace the files in OVHcloud CLI releases v0.11.0 to v0.15.0 with a credential stealer. The source code, the tags and the build pipeline were untouched; only the release binaries changed. The swapped files were up for about an hour and a half and were downloaded around 250 times ([write-up][ovh]).

I install a few command-line tools from GitHub Releases every week, so I wanted to know something narrower: if someone got write access to a repository, could they replace the files in its latest release? And if they did, would anyone downloading them be able to tell?

I checked 242 projects. For 179 of them (74%), the files could be replaced and a downloader would have no way to tell.

## How I checked

- **Scope**: every Go and Rust repository on GitHub tagged `cli` with at least 1,000 stars, 354 in all. I kept the ones whose latest release is less than a year old and ships binaries: 242. Go and Rust because those projects most often ship binaries straight from their releases.
- **Latest release only**, recorded through the GitHub API on 24 October 2026:
  - **Immutable**: the release has GitHub's [immutable releases][immutable] turned on, so its files can't be replaced or deleted and its tag can't move.
  - **Build provenance**: its binaries have a GitHub artifact attestation. A file that wasn't built by the project's own workflow fails `gh attestation verify`.
  - **Signed**: the release ships signature files, such as cosign or Sigstore bundles, GPG `.asc`, minisign, or SLSA `.intoto.jsonl`.
  - **Checksums**: the release ships a file like `checksums.txt` or `SHA256SUMS`.

The whole run took 945 API calls and a few minutes on GitHub Actions.

## Results

| Best protection on the latest release | Projects | Share |
|---|---|---|
| Immutable release | 25 | 10% |
| Build provenance (not immutable) | 19 | 8% |
| Signature files (neither of the above) | 19 | 8% |
| Checksum file only | 112 | 46% |
| Nothing | 67 | 28% |

Among the 50 most-starred projects, 36 are in the last two rows.

I checked a few by hand: the 21 files in sharkdp/bat v0.26.1 have no checksum or signature; sharkdp/fd has build provenance; cli/cli has immutable releases and build provenance.

## Why a checksum file doesn't count

The checksum file sits in the same release as the binaries, uploaded by the same people with the same access. Whoever can replace `tool_linux_amd64.tar.gz` can replace the `checksums.txt` next to it. It catches a broken download, not a swapped one.

That's why I count "checksums only" and "nothing" together: 179.

## Three things maintainers can do

From least to most work:

**1. Turn on immutable releases.** It's a repository or organization setting; releases created after you turn it on can't have their files changed. It has been [generally available since 28 October 2025][ga], and 25 of the 242 projects use it. Users can then check a download with [`gh release verify-asset`][verify-asset].

**2. Attest build provenance in the release workflow** with GitHub's own [`actions/attest`][attest]. It records which repository, workflow and commit built each file:

```yaml
permissions:
  contents: write
  id-token: write
  attestations: write

steps:
  # ... build the release files into dist/ ...
  - uses: actions/attest@1e69f48acb82d1966a394da916b4c1698aa569d6  # v4.2.2
    with:
      subject-path: dist/*
```

31 of the 242 projects do this.

**3. Tell users in the README how to verify, pinned to the release workflow.** Someone with push access can write a workflow of their own and attest a malicious file with it, so checking the repository alone isn't enough:

```sh
gh attestation verify tool_linux_amd64.tar.gz --repo owner/tool \
  --signer-workflow owner/tool/.github/workflows/release.yml
```

## What this doesn't stop

Two days later, on 21 October, LiteLLM 1.107.0 was published to PyPI and Docker Hub with a credential stealer inside ([details][litellm]). The attacker started from a key that leaked in May and was never revoked, worked their way to maintainers' GitHub tokens, and pointed the project's own release pipeline at a lookalike repository.

Immutable releases and build provenance prove that a file is what the pipeline produced. They can't prove the pipeline wasn't taken over. For that you need leaked keys revoked quickly, tokens with narrow permissions, and release approvals nobody can get around.

## What I didn't check

- Only each project's latest release, and only GitHub Releases. Homebrew and many Linux distributions record a file's hash when they package it, so they would notice a later swap; direct downloads and `curl | sh` install scripts would not.
- Build provenance was looked up for at most two binaries and one checksum file per release. A project that attests only some of its files could be missed.
- Shipping a signature isn't the same as anyone verifying it.
- Go and Rust projects tagged `cli` with 1,000+ stars are a small slice of GitHub; a different slice would give different numbers.

The full results, one row per project, are in [cli-releases-2026-10-24.csv](/zh-cn/posts/2026/swappable-github-releases/cli-releases-2026-10-24.csv), and the scan script is in [keelinfra/release-ledger][script].

## My own projects

Before writing this I ran the same script on my own projects. The latest release of the [clang-tools static binaries][clang-tools], my most-downloaded files, is immutable but has no build provenance. None of keelinfra's three repositories have immutable releases: the Keycloak distribution and Agent8 ship checksum files only, and jenkins-upgrade-check has build provenance because its release workflow uses [release-ledger][release-ledger], a GitHub Action I wrote. Those are next on my list.

[ovh]: https://dev.to/anoymask/ovhcloud-cli-supply-chain-attack-release-assets-replaced-to-steal-developer-secrets-2d2i
[immutable]: https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases
[ga]: https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/
[verify-asset]: https://cli.github.com/manual/gh_release_verify-asset
[attest]: https://github.com/actions/attest
[litellm]: https://thehackernews.com/2026/10/leaked-litellm-master-key-let-attackers.html
[script]: https://github.com/keelinfra/release-ledger/blob/b30dd7f6eb7d8084e16fc739878945e0370daaba/research/release-integrity/scan.py
[clang-tools]: https://github.com/cpp-linter/clang-tools-static-binaries
[release-ledger]: https://github.com/keelinfra/release-ledger
