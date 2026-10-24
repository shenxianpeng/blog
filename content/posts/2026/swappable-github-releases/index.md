---
title: OVHcloud 的 release 被换了包：热门 CLI 里四分之三也能这样被换
summary: |
  10 月 19 日，OVHcloud CLI 的 release 文件被人用偷来的开发者凭据换成了窃密程序。我查了 242 个热门 Go 和 Rust CLI 项目的最新 release，179 个可以被同样换掉，而且下载的人没有任何独立的东西可以核对。这篇讲怎么查的、为什么校验和文件不算数，以及维护者能做的三件事。
tags:
  - DevSecOps
  - SLSA
  - GitHub
authors:
  - shenxianpeng
date: 2026-10-24
---

10 月 19 日下午，有人用一位开发者被偷的 GitHub 凭据，把 OVHcloud CLI v0.11.0 到 v0.15.0 的 release 文件换成了窃密程序。源码、tag、构建流水线都没动，只换了 release 里的二进制。被换掉的文件挂了大约一个半小时，下载了 250 次左右（[事件经过][ovh]）。

我每周都会从 GitHub Releases 上装几个命令行工具，所以想知道一件更具体的事：如果有人拿到了仓库的写权限，他能不能换掉最新 release 里的文件？换掉以后，下载的人有没有办法发现？

我查了 242 个项目。179 个（74%）能被换掉，而且下载的人没有办法发现。

## 怎么查的

- **范围**：GitHub 上打了 `cli` 标签、1,000 star 以上的所有 Go 和 Rust 仓库，一共 354 个。只留下最新 release 在一年以内、而且带二进制文件的，剩 242 个。选 Go 和 Rust，是因为这两类项目最常直接在 release 里发二进制。
- **只看最新的那个 release**，2026 年 10 月 24 日通过 GitHub API 记录四件事：
  - **immutable**：这个 release 开了 GitHub 的 [immutable releases][immutable]，文件不能替换也不能删除，tag 也不能移动。
  - **构建来源证明**：二进制文件有 GitHub 的 artifact attestation。不是项目自己的 workflow 构建出来的文件，`gh attestation verify` 会失败。
  - **签名**：release 里有签名文件，比如 cosign 或 Sigstore 的 bundle、GPG 的 `.asc`、minisign、SLSA 的 `.intoto.jsonl`。
  - **校验和**：release 里有 `checksums.txt`、`SHA256SUMS` 这类文件。

一整轮用了 945 次 API 调用，在 GitHub Actions 上跑了几分钟。

## 结果

| 最新 release 上最强的保护 | 项目数 | 占比 |
|---|---|---|
| immutable release | 25 | 10% |
| 有构建来源证明（但没开 immutable） | 19 | 8% |
| 有签名文件（前两项都没有） | 19 | 8% |
| 只有校验和文件 | 112 | 46% |
| 什么都没有 | 67 | 28% |

star 最多的 50 个项目里，有 36 个落在最后两行。

我手工核对了几个：sharkdp/bat v0.26.1 的 21 个文件里确实没有校验和也没有签名；sharkdp/fd 有构建来源证明；cli/cli 开了 immutable，也有构建来源证明。

## 校验和文件为什么不算数

校验和文件和二进制放在同一个 release 里，是同一批人、用同一个权限上传的。能把 `tool_linux_amd64.tar.gz` 换掉的人，也能顺手把旁边的 `checksums.txt` 换掉。它能发现下载不完整，发现不了被换包。

所以我把"只有校验和"和"什么都没有"算在一起：179 个。

## 维护者能做的三件事

按工作量从小到大：

**1. 打开 immutable releases。** 在仓库或组织的设置里打开，之后新建的 release 就不能再改文件了。这个功能 [2025 年 10 月 28 日正式上线][ga]，242 个项目里只有 25 个在用。开了以后，用户可以用 [`gh release verify-asset`][verify-asset] 核对下载的文件。

**2. 在发布 workflow 里生成构建来源证明。** 用 GitHub 自己的 [`actions/attest`][attest]，它会记下每个文件是哪个仓库、哪个 workflow、哪个 commit 构建的：

```yaml
permissions:
  contents: write
  id-token: write
  attestations: write

steps:
  # ... 把要发布的文件构建到 dist/ ...
  - uses: actions/attest@1e69f48acb82d1966a394da916b4c1698aa569d6  # v4.2.2
    with:
      subject-path: dist/*
```

242 个项目里有 31 个这样做了。

**3. 在 README 里告诉用户怎么核对，并且固定到发布 workflow。** 拿到 push 权限的人也能自己写一个 workflow 给恶意文件签名，所以只核对仓库是不够的：

```sh
gh attestation verify tool_linux_amd64.tar.gz --repo owner/tool \
  --signer-workflow owner/tool/.github/workflows/release.yml
```

## 这些防不住什么

同一周还有一件事：10 月 21 日，LiteLLM 1.107.0 带着窃密代码发到了 PyPI 和 Docker Hub（[经过][litellm]）。攻击者用的是 5 月就泄露了、一直没吊销的一个 key，一路拿到维护者的 GitHub token，再把项目自己的发布流水线指向了一个仿冒仓库。

immutable releases 和构建来源证明，能证明文件就是流水线产出的那一份，证明不了流水线没有被人接管。防这种情况，靠的是及时吊销泄露的 key、缩小 token 的权限，以及别人绕不过去的发布审批。

## 还没做的

- 只看了每个项目最新的一个 release，也只看 GitHub Releases。Homebrew 和很多 Linux 发行版在收录时就记下了文件的 hash，事后被换包能发现；直接下载和 `curl | sh` 安装脚本发现不了。
- 构建来源证明每个 release 最多查了两个二进制和一个校验和文件。只给部分文件做了证明的项目，可能被我漏掉。
- release 里有签名文件，不代表有人去验证它。
- 打 `cli` 标签、1,000 star 以上的 Go 和 Rust 项目只是 GitHub 的一小部分，换个范围比例会不一样。

每个项目一行的完整结果在 [cli-releases-2026-10-24.csv](cli-releases-2026-10-24.csv)，扫描脚本在 [keelinfra/release-ledger][script]。

## 我自己的项目

写这篇之前，我先用同一个脚本查了自己的项目。下载量最大的 [clang-tools 静态二进制][clang-tools]，最新 release 是 immutable 的，但没有构建来源证明。keelinfra 的三个仓库都没开 immutable：Keycloak 发行版和 Agent8 只有校验和文件；jenkins-upgrade-check 有构建来源证明，因为它的发布 workflow 用了我写的 [release-ledger][release-ledger]。接下来先把这几个补上。

[ovh]: https://dev.to/anoymask/ovhcloud-cli-supply-chain-attack-release-assets-replaced-to-steal-developer-secrets-2d2i
[immutable]: https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases
[ga]: https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/
[verify-asset]: https://cli.github.com/manual/gh_release_verify-asset
[attest]: https://github.com/actions/attest
[litellm]: https://thehackernews.com/2026/10/leaked-litellm-master-key-let-attackers.html
[script]: https://github.com/keelinfra/release-ledger/blob/b30dd7f6eb7d8084e16fc739878945e0370daaba/research/release-integrity/scan.py
[clang-tools]: https://github.com/cpp-linter/clang-tools-static-binaries
[release-ledger]: https://github.com/keelinfra/release-ledger
