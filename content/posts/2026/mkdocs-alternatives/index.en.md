---
title: "MkDocs Alternatives in 2026: Where Existing Sites Can Go"
summary: |
  The mkdocs package was downloaded 4.3 million times in a single week, yet its last release is from August 2024. An existing site has five ways forward: stay on 1.6.1, upstream 2.0, ProperDocs, Zensical or MkDocs NG. This post compares them with data you can check: whether your plugins run, whether your commands and CI change, build speed, who maintains each one and for how long.
tags:
  - Open Source
  - Documentation
authors:
  - shenxianpeng
date: 2026-11-14
series: ["MkDocs NG"]
series_order: 5
---

In the past seven days, the `mkdocs` package was downloaded 4.3 million times from PyPI. Its last release is 1.6.1, from August 30, 2024.

1.6.1 still builds today, but newly reported bugs don't get fixed, and the Python versions it declares support for stop at 3.12. The theme most often installed with it, Material for MkDocs, is in maintenance mode too: it [reaches end of life on May 5, 2027](https://zensical.org/upcoming-changes/), and since 9.8.0 it prints a notice saying so on every build.

This post tries to answer one concrete question: you already have an MkDocs site, so what should you do in 2026?

First, a disclosure: I maintain [MkDocs NG](https://mkdocs-ng.org/), one of the projects compared below. So I've stuck to facts you can check. Every number comes with a source or a way to reproduce it, and what I say about other projects follows their own documentation. Facts were checked on November 14, 2026. If something is wrong or out of date, please say so in the comments or in an [issue](https://github.com/mkdocs-ng/mkdocs/issues), and I'll fix it.

## Five ways forward

1. **Stay on MkDocs 1.6.1** and change nothing.
2. **Upstream MkDocs 2.0.** It's published as pre-releases of the `mkdocs` package; the latest is 2.0.dev6 (2026-09-15). It's a rewrite: no configuration file, plugins or themes, and it stops with an error when it finds a `mkdocs.yml`. Existing sites can't use it, so I won't cover it further. One thing to watch for: `pip install --pre` or `uv --prerelease allow` will install it.
3. **[ProperDocs](https://properdocs.org/)**, a fork of MkDocs 1.6. By its own account, the team formed in March 2026, started out as the mkdocs-community organization, and aims to preserve MkDocs 1.x and its feature set. It has its own package and its own command, `properdocs`.
4. **[Zensical](https://zensical.org/)**, a new site generator from the team behind Material for MkDocs, with a core written in Rust. It reads existing `mkdocs.yml` files. 0.1.0 came out on November 5 and started a three-month beta, after which the team plans to call it stable.
5. **MkDocs NG**, the fork of MkDocs 1.x that I maintain. The package is `mkdocs-ng`; the command and configuration stay the same.

Moving to Docusaurus, Starlight or Sphinx is also an option, but that means rewriting the site, which is beyond the scope of this post.

## Where things stand

| | MkDocs 1.6.1 | ProperDocs | Zensical | MkDocs NG |
| --- | --- | --- | --- | --- |
| Version | 1.6.1 | 1.6.7 | 0.1.1 | 1.11.2 |
| Released | 2024-08-30 | 2026-03-20 | 2026-11-10 | 2026-11-11 |
| Package | `mkdocs` | `properdocs` | `zensical` | `mkdocs-ng` |
| Command | `mkdocs` | `properdocs` | `zensical` | `mkdocs` |
| Config | `mkdocs.yml` | `properdocs.yml` or `mkdocs.yml` | `mkdocs.yml` or `zensical.toml` | `mkdocs.yml` |
| MkDocs plugins | Yes | Yes | No; 33 rewritten natively | Yes |
| MkDocs themes | Yes | Yes | No; own theme, takes Material settings | Yes |
| `hooks`, `gh-deploy` | Yes | Yes | Not supported | Yes |
| Python | 3.8–3.12 | 3.9+ | 3.11+ | 3.10+ |
| Downloads (7 days) | 4.3 million | 545,000 | 512,000 | 616 |

Download counts are from [pypistats.org](https://pypistats.org/), checked on November 14. They count installs, not sites, and a package installed as another package's dependency counts too. For example, the popular plugins `mkdocs-redirects`, `mkdocs-gen-files`, `mkdocs-literate-nav` and `mkdocs-section-index` now depend on both `mkdocs` and `properdocs`, so installing them installs both.

The 616 in the MkDocs NG column also tells you something: very few people use it today. I'd rather say that up front.

## Four questions to answer first

### 1. Which plugins does your site use?

Start here. Open `mkdocs.yml` and look at the `plugins:` and `hooks:` sections.

ProperDocs and MkDocs NG both run MkDocs plugins directly, so your plugins stay.

Zensical doesn't run MkDocs plugins. It reimplements popular ones natively: its [list](https://zensical.org/docs/compatibility/mkdocs/plugins/) has 33 today, with 3 git-related plugins planned. Its documentation says that configuration for plugins not on the list is silently ignored, and the build doesn't fail, so check them one by one before you migrate.

I checked the 26 popular plugins in the MkDocs NG compatibility tests against Zensical's list:

- **13 are supported:** mkdocstrings, macros, glightbox, mike, redirects, rss, markdown-exec, include-markdown, minify, awesome-nav, literate-nav, markdownextradata, autorefs.
- **2 are planned:** git-revision-date-localized, git-authors.
- **11 aren't on the list:** techdocs-core, mkdocs-jupyter, mermaid2, monorepo, awesome-pages, encryptcontent, static-i18n, bibtex, kroki, swagger-ui-tag, gen-files. Some have a replacement: Material already renders Mermaid diagrams, so you don't need mermaid2 there.

If your site only uses plugins from the first group, Zensical is a real option. If it uses any from the last group, you'll need a replacement, or a tool that runs MkDocs plugins.

### 2. Can you change your commands and CI?

With MkDocs NG you change one package name: replace `mkdocs` with `mkdocs-ng` in your dependencies. `mkdocs build`, `mkdocs.yml`, your CI scripts and `.readthedocs.yaml` stay as they are. Plugins that list `mkdocs` as a dependency are fine: when `mkdocs-ng` is installed alongside it, MkDocs NG is what runs.

ProperDocs uses the `properdocs` command and Zensical uses `zensical build` and `zensical serve`, so the places in CI that call the command need to change. Both read your existing `mkdocs.yml`. Zensical doesn't provide `gh-deploy`, so deployment needs another method, such as GitHub Actions' Pages deployment.

### 3. Which theme do you use?

Most MkDocs sites use Material for MkDocs. It's no longer maintained after May 5, 2027, so before then you'll want to choose where to go:

- **Zensical:** made by the same team, and it keeps Material's look and configuration. This is the closest thing to the "official" path. Template overrides (`overrides/`) based on Material 9.6.18 or later [should generally work unchanged](https://zensical.org/docs/compatibility/mkdocs/migration/); older or heavily customized ones need testing, since its template engine is MiniJinja, which can't call Python functions.
- **[MkDocs NG Material](https://material.mkdocs-ng.org/)** (`mkdocs-ng-material`): the fork of Material I maintain in the NG organization. The theme name is still `material`, and switching means changing two dependency lines. After May 5, 2027 it keeps getting security and compatibility fixes, with no new features.
- **[MaterialX](https://github.com/jaywhj/mkdocs-materialx):** another continuation of Material that adds features of its own. It depends on ProperDocs.
- **[Sumi](https://sumi.mkdocs-ng.org/):** a new theme I made for MkDocs NG. It's at 0.4.0 and still young.

Sites using a built-in MkDocs theme or another third-party theme can't run on Zensical; they run on both ProperDocs and MkDocs NG. A site on the built-in theme that moves to ProperDocs also needs the `properdocs-theme-mkdocs` package; ProperDocs tells you so when you build.

### 4. How long do you need it maintained, and by whom?

This is the hardest one to measure, so here's what can be checked:

- **Zensical** is backed by Zensical LLC, the team that built Material, and its development is funded in part by paid products, Spark and Studio. A full-time, funded team is its biggest strength.
- **ProperDocs** is maintained by the ProperDocs team. Its latest release is 1.6.7, from March 20, 2026.
- **MkDocs NG** promises in its [versioning and support policy](https://mkdocs-ng.org/about/release-notes/#versioning-and-support) that 1.x gets bug, security and compatibility fixes until at least **December 31, 2028**. If a new major version comes out, 1.x keeps getting security fixes for at least 12 months after it, and never stops before that date. Releases are published by GitHub Actions through PyPI trusted publishing, with a signed attestation for every file. The weakness is written down in its [governance document](https://mkdocs-ng.org/about/governance/) too: today I'm the only maintainer, and finding a second one is the project's most important open task.

## How plugin compatibility is tested

The MkDocs NG repository has a [compatibility test suite](https://github.com/mkdocs-ng/mkdocs/tree/main/compat). It takes the 32 most popular plugins, themes and Markdown extensions from the [plugin catalog](https://catalog.mkdocs-ng.org/), builds a small site with each, once on upstream MkDocs 1.6.1 and once on MkDocs NG, in `--strict` mode, so a warning counts as a failure. It runs on every pull request, and again every Monday to catch new plugin releases.

The run for the 1.11.2 release on November 11: MkDocs 1.6.1 passed 32/32, MkDocs NG passed 32/32.

The tests have limits. They show that these plugins build a small site successfully; they don't cover every option of every plugin. PlantUML and Kroki are only checked to load, because rendering needs an external server. If your site uses an unusual combination, the only real test is building it yourself.

## Build speed

Speed shouldn't be the first thing you choose on, but people always ask, so I measured it.

The same generated 1,000-page site, the same 4-core Linux machine, Python 3.13. Each tool did 5 builds into an empty output directory, and the table shows the median. Measured on November 14, 2026 with [`benchmarks/compare.py`](https://github.com/mkdocs-ng/mkdocs/tree/main/benchmarks) from the MkDocs NG repository, which you can run on your own machine.

| Tool | Theme | Time |
| --- | --- | --- |
| MkDocs NG 1.11.2 | Built-in `mkdocs` | 6.4 s |
| MkDocs NG 1.11.2 | Material (`mkdocs-ng-material` 9.8.1) | 8.7 s |
| MkDocs NG 1.11.2 | Sumi 0.4.0 | 9.3 s |
| Zensical 0.1.1 | Its own, based on Material | 12.4 s; 4.6 s with its cache |
| ProperDocs 1.6.7 | Built-in `mkdocs` | 13.0 s |
| MkDocs 1.6.1 | Built-in `mkdocs` | 13.3 s |
| ProperDocs 1.6.7 | Material 9.8.1 | 24.1 s |
| MkDocs 1.6.1 | Material 9.8.1 | 25.7 s |

Read these together:

- **Zensical has a build cache.** Rebuilding with the cache kept and nothing changed, it's the fastest. MkDocs NG has no cache between builds yet.
- **Compare like with like.** Zensical's theme is based on Material, so the closest comparison is with the Material rows.
- **The order changes with size.** In early November, on a 5,000-page site (MkDocs NG 1.11.0rc1 and Zensical 0.0.74 at the time), MkDocs NG with Material took 134.5 s, and Zensical 185.7 s with its cache cleared and 59.2 s with it kept. With Material every page carries the whole navigation, so that site is more than 4 GB of HTML.
- **From editing a page in `mkdocs serve` to seeing it**, measured on November 4 on the 1,000-page site: Zensical and MkDocs NG (built-in theme) both took 1.2 s, MkDocs NG with Material 2.7 s. MkDocs 1.6.1 and ProperDocs rebuild the whole site on each change and took about 18 s.

This is one kind of generated site, and yours may behave differently. If you think any tool is set up unfairly, tell me and I'll fix it.

## How to choose

Going by the four questions:

- **The site should keep building as is, plugins included:** MkDocs NG or ProperDocs. The difference is that MkDocs NG keeps the `mkdocs` command, while ProperDocs uses `properdocs`.
- **You use Material, every plugin you use is on Zensical's list, and you're ready to switch tools:** Zensical. The original team, funding, and very fast cached builds make it the natural next step for Material users.
- **You use Material, but also plugins or `hooks` that Zensical doesn't support, or you don't want to switch tools now:** MkDocs NG with `mkdocs-ng-material`. Two dependency lines change, and it keeps getting fixes after May 5, 2027.
- **Staying on 1.6.1 for now:** fine in the short term, as long as you know bugs won't be fixed and newer Python versions are outside its declared support.

Whichever you pick, you can try it on a branch first without touching your live site:

```sh
# MkDocs NG: add one package, same command
pip install mkdocs-ng
mkdocs build --strict

# ProperDocs
pip install properdocs
properdocs build --strict

# Zensical
pip install zensical
zensical build --strict
```

`--strict` turns warnings into errors, which is the quickest way to surface migration problems. Once the build passes, open a few pages that use your plugins and compare them. To go back, uninstall the package you added.

The detailed MkDocs NG steps are in [Switching to MkDocs NG](https://mkdocs-ng.org/user-guide/migrating/), a fuller comparison with the other projects is on the [comparison page](https://mkdocs-ng.org/about/comparison/), and Material users can read [Material for MkDocs End of Life](https://mkdocs-ng.org/user-guide/material-end-of-life/).

If you hit a problem moving to MkDocs NG, please open an [issue](https://github.com/mkdocs-ng/mkdocs/issues). And if anything this post says about another project is inaccurate, please let me know.
