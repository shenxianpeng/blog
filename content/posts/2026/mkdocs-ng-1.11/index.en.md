---
title: "MkDocs NG 1.11.0 Released: Six Months of Maintaining MkDocs, Further Than I Expected"
summary: |
  Six months into maintaining MkDocs, 10 of the 15 most-upvoted open upstream issues are fixed, 1.11.0 builds multi-language sites from a single mkdocs.yml, and clean builds are faster than both upstream 1.6.1 and the Rust-based Zensical. Plus how to choose between Sumi and Material, and the new plugin catalog website.
tags:
  - Open Source
  - Documentation
authors:
  - shenxianpeng
date: 2026-11-04
series: ["MkDocs NG"]
series_order: 4
---

Six months ago I wrote "[Why I Forked MkDocs and Material for MkDocs](/posts/2026/mkdocs-ng/)" and started maintaining MkDocs. Follow-ups on [v1.7.x](/posts/2026/mkdocs-ng-update/) and [the 1.8.0 release](/posts/2026/mkdocs-ng-1.8/) came after.

On November 4, MkDocs NG 1.11.0 came out, so this is a good moment to look back at the last six months.

## Where MkDocs stands

Many of you have probably used MkDocs for a project's docs. Markdown for content, YAML for configuration, any plugin you like, Material on top, and you have a decent docs site in minutes.

Over the past two years, though, MkDocs ran into two problems.

**First, 1.x is no longer maintained.** The last upstream 1.x release is 1.6.1 from August 2024. There has been no release in more than two years, and reported bugs just sit there.

**Second, 2.0 is a complete rewrite.** Upstream's effort went into MkDocs 2.0, which is still a pre-release (the latest is 2.0.dev6 from September 2026). It has no plugins and no themes, and it exits with an error when it finds a `mkdocs.yml`. Existing sites can't upgrade to it, and the plugin ecosystem can't follow.

For users, that means either staying on an old version that no longer gets fixes, or paying a high migration cost.

The community has gone in a few directions:

- **[Zensical](https://zensical.org/)**: a new project from the team behind Material for MkDocs, with a core written in Rust, currently at 0.0.74. It reads `mkdocs.yml`, but it doesn't run MkDocs plugins; it reimplements about thirty popular ones natively.
- **[ProperDocs](https://properdocs.org/)**: a fork of 1.6 started by a former MkDocs maintainer, with its own package and command name. Its last release, 1.6.7, came out in March 2026, and there has been no release in the seven months since.

Each project has its own goals and trade-offs, and I'm not going to rank them. I'll just share my own view.

## What I care about is the will to keep going

When people look at a fork, their first question is often: is it the original team?

I don't think that matters much. Original authors leave, original teams move on to new things, and that's normal. Whether a project keeps going depends on whether someone is **willing** to maintain and improve it for the long haul. Without that will, the original team stops too.

Why do I have it?

Because over my years in open source, almost every project I've worked on has had its docs built with MkDocs. I'm a heavy user. I know first-hand what works and where it gets in the way.

So when I took it over, I wasn't looking to reinvent it. The goal was simple: **this supply chain must not break.** I still need MkDocs for my own docs, and everyone's plugins need to keep working.

## The most-upvoted upstream issues: mostly cleared

Since taking over, most of my time has gone into fixing issues left behind upstream, especially the most-upvoted ones.

Sort upstream's open issues by upvotes, and of the top 15:

- **10 are fixed in MkDocs NG.** Among them the most-upvoted one, `mkdocs serve` not watching for file changes ([#4032](https://github.com/mkdocs/mkdocs/issues/4032), 70 upvotes), livereload needing an explicit flag ([#4055](https://github.com/mkdocs/mkdocs/issues/4055)), built-in themes loading from CDNs ([#2171](https://github.com/mkdocs/mkdocs/issues/2171)), no Python API for running MkDocs ([#1240](https://github.com/mkdocs/mkdocs/issues/1240)), `INHERIT` accepting only one file ([#2624](https://github.com/mkdocs/mkdocs/issues/2624)), and external links lacking `rel="external"` ([#3914](https://github.com/mkdocs/mkdocs/issues/3914)).
- **1 is much improved**: the performance and authoring experience of `mkdocs serve` ([#3695](https://github.com/mkdocs/mkdocs/issues/3695)), more on that below.
- The remaining 4: one is a joke ([#892](https://github.com/mkdocs/mkdocs/issues/892), "No beer me button"), and the other three are architectural changes (cache busting, splitting out the search plugin, decoupling themes from the core), planned for 1.12.

The full list is on the [Fixed Upstream Issues](https://mkdocs-ng.org/about/fixed-upstream-issues/) page, which currently covers 27 upstream issues.

## What's in 1.11.0

1.11.0 is the first final release since 1.9.0. There are no breaking changes: configuration, themes and plugins that work with 1.9 keep working. The highlights:

- **One `mkdocs.yml` for every language.** With the new `languages` setting, the default language goes at the site root and the others under `/zh/`, `/de/` and so on. Translations sit next to the original (`page.zh.md`), and untranslated pages fall back to the default language, so no link breaks. Each language is an ordinary build, so plugins need no changes. See [Multi-language Sites](https://mkdocs-ng.org/user-guide/multi-language-sites/).
- **`mkdocs serve` is much faster.** Unchanged pages are no longer converted or rendered again. On a 1,000-page site, the time from saving to seeing the change dropped from 5.1 seconds to about 0.9 (default theme).
- **Installing a plugin no longer swaps MkDocs NG out.** Some plugins and themes used to quietly replace MkDocs NG with upstream 1.6.1, and some printed a "switch to ProperDocs" warning. Both problems are gone.
- **Ready for editors and AI.** Sites created with `mkdocs new` come with `llms.txt` and an `AGENTS.md`, and `mkdocs.yml` now has a JSON Schema, so editors can complete and validate your settings.
- Smaller improvements: GitHub-style `> [!NOTE]` alerts render as admonitions, `mkdocs serve` picks another port when 8000 is taken, and `docs_dir: .` works.

See the [Release Notes](https://mkdocs-ng.org/about/release-notes/) for everything.

## The biggest surprise: AI

The biggest surprise of these six months was what AI changed.

Maintaining a project alone used to be limited by energy above all. Now I explain the vision and the trade-offs (what I want, what I don't, what must never break) and AI helps me deliver the implementation, the tests and the docs together.

An example: from October 31 to November 4, five days, MkDocs NG shipped four releases: 1.9.0, 1.10.0rc1, 1.11.0rc1 and 1.11.0. One person in their spare time couldn't have done that before.

The direction is still mine to set. No renamed command, no renamed config file, no broken plugins: these rules haven't changed since day one. AI did once suggest adding an `mkdocs-ng` command; I said no.

## Somehow, it became the fastest

The other surprise was performance.

Among all the forks and alternatives, MkDocs NG now has the fastest clean builds. That comes from keeping a close eye on performance all along.

Since 1.8.0, every PR runs performance benchmarks on [CodSpeed](https://codspeed.io/), and any regression gets caught before merging. With that in place we kept optimizing: navigation rendering is no longer O(N²), `serve` reuses unchanged pages, the search plugin reads pages three times faster. Bit by bit, the speed went up.

We built the same 1,000 pages of Markdown with each tool on the same 4-core machine, clean builds without caches:

![Clean build of a 1,000-page site: MkDocs NG with Material 11.5 s, Zensical 17.4 s, MkDocs 1.6.1 with Material 34.8 s](build-speed.svg)

| Tool | Theme | Time |
| --- | --- | --- |
| MkDocs NG 1.11 | Default | 7.9 s |
| MkDocs NG 1.11 | Material | 11.5 s |
| MkDocs NG 1.11 | Sumi | 12.0 s |
| Zensical 0.0.74 | Its own (based on Material) | 17.4 s |
| ProperDocs 1.6.7 | Default | 18.8 s |
| MkDocs 1.6.1 | Default | 18.9 s |
| MkDocs 1.6.1 | Material | 34.8 s |

With Material on both, MkDocs NG takes 11.5 seconds and upstream 1.6.1 takes 34.8, a third of the time. Without caches it is also faster than the Rust-based Zensical (17.4 seconds).

A few things to be clear about, so this doesn't mislead:

- Zensical has a build cache. **With its cache kept** it takes only 6.4 seconds, faster than us. MkDocs NG has no cache between builds yet.
- For showing an edit in `serve`, Zensical takes 0.8 seconds; 1.11.0 gets us to about 0.9. Close, but not ahead.
- Zensical is still at 0.0.x and will surely get faster.

The method and the script are public under [Build speed](https://mkdocs-ng.org/about/comparison/#build-speed). Feel free to reproduce it on your own machine.

From 1.6.1 to 1.11 the language didn't change; it's still Python. All of the speed-up comes from changes like not re-rendering the navigation for every page and not recomputing pages that didn't change.

## Sumi: MkDocs NG's own theme

Next, let me introduce [Sumi](https://sumi.mkdocs-ng.org/).

Sumi is Japanese for "ink": paper, ink and a vermilion seal. It's the documentation theme I made for MkDocs NG, with ideas borrowed from [Oink](https://oink.pgsty.com/). What it offers:

- **Components are plain Markdown.** Callouts are `> [!NOTE]`, steps are a list with `{.steps}`, tabs are code fences with `{tab="…"}`. No MDX, no shortcodes, and your source still reads well on GitHub.
- **Local-first.** Fonts, 2,000 icons, search, Mermaid and KaTeX ship with the theme, no CDN, so it works on an intranet. Mermaid and KaTeX load only on pages that use them.
- **⌘K search that handles Chinese and Japanese.** The search box doubles as a command palette.
- **Written for AI too.** Every page has a clean Markdown copy, the site has `llms.txt`, and pages can be copied as Markdown in one click.
- **One design for the whole project site.** Docs, landing page, blog, release downloads and a whole-site print edition.
- **Keeps your MkDocs content.** Admonitions, `pymdownx` tabs, `mike` versions and Material's `extra` settings keep working.

The MkDocs NG [website](https://mkdocs-ng.org/), Sumi's own docs and the [plugin catalog](https://catalog.mkdocs-ng.org/) are all built with Sumi.

Trying it takes three steps:

```sh
pip install mkdocs-sumi
```

```yaml
# mkdocs.yml
theme:
  name: sumi

plugins:
  - search
  - llms_txt
  - sumi
```

```sh
mkdocs serve
```

### How is Sumi different from Material for MkDocs?

First, where Material for MkDocs stands. Since November 2025 it has been in maintenance mode: the upstream team moved on to Zensical, and there are no new features, only critical fixes. According to [Zensical's announcement](https://zensical.org/upcoming-changes/), that critical maintenance runs until May 5, 2027.

I forked Material into the MkDocs NG organization too. The package is `mkdocs-ng-material`, now at 9.8.0 with upstream's 9.8.0 security fixes, and its docs are at [material.mkdocs-ng.org](https://material.mkdocs-ng.org/). The theme name is still `material`, so your config doesn't change:

```sh
pip install mkdocs-ng-material
```

So both paths are open: install `mkdocs-ng-material` to keep using Material, or try Sumi.

Roughly, they differ like this:

| | Material for MkDocs | Sumi |
| --- | --- | --- |
| Status | Critical fixes only upstream; `mkdocs-ng-material` maintained in the NG organization | New theme, 0.2.x, under active development |
| Maturity | Years of work, the most features and users | Released in November 2026, still filling gaps |
| Components | Extension syntax such as `!!! note` and `=== "Tab"` | `> [!NOTE]` and `{tab="…"}`, so your source renders on GitHub too |
| External resources | Loads fonts from Google Fonts by default (can be turned off) | Fonts and icons ship with the theme, no CDN at all |
| Whole-site pages | Blog plugin built in; a landing page needs your own template | Landing page, blog, releases page and print edition built in |

When would I pick Sumi?

- **A new docs site** where you want clean source files that also read well on GitHub.
- **Intranet or offline hosting** with no external requests at all.
- **One design** for docs, landing page, blog and downloads.

If your site already relies heavily on Material's features, stay on `mkdocs-ng-material`; there's no need to switch. If you want to try Sumi, it reads most Material content as is, and switching usually means changing two lines. See [Migrating from Material](https://sumi.mkdocs-ng.org/docs/start/migrate/).

## The plugin catalog is now a website

This time I also turned the MkDocs plugin catalog into a website: [catalog.mkdocs-ng.org](https://catalog.mkdocs-ng.org/).

It updates itself every week, ranks projects by downloads and activity, and marks the plugins tested on MkDocs NG. It also discovers new plugins on PyPI automatically: after this week's update it will list more than 470 plugins, themes and Markdown extensions. For comparison, [mkdocs/catalog](https://github.com/mkdocs/catalog) and [ProperDocs/catalog](https://github.com/ProperDocs/catalog) list about 300 each. As far as I know, it is the most complete MkDocs plugin directory today.

If your plugin isn't there, please [open an issue](https://github.com/mkdocs-ng/catalog/issues).

## How to switch

If your site still uses upstream `mkdocs`, try MkDocs NG in a throwaway environment with uv first. It leaves your own environment alone:

```sh
uvx --from mkdocs-ng --with-requirements requirements.txt mkdocs build --strict
```

If that works, switching is one line, and you don't need to uninstall `mkdocs` first:

```sh
pip install -U mkdocs-ng
```

The command is still `mkdocs`, the config is still `mkdocs.yml`, and plugins and themes stay as they are. Switching back is one line too. See the [migration guide](https://mkdocs-ng.org/user-guide/migrating/).

## Finally

Six months ago I wrote that code is only the first half of a project's reach; the second half is people.

I've given the code my best this half year. Now I need your help:

- **Try Sumi and MkDocs NG** on your docs site.
- **Open an [issue](https://github.com/mkdocs-ng/mkdocs/issues)** when something breaks or you need something. The roadmap is [#59](https://github.com/mkdocs-ng/mkdocs/issues/59); tell us what you want most.
- **Contributions are welcome**: code, docs, translations, or adding a plugin you use to the [plugin catalog](https://catalog.mkdocs-ng.org/).
- If you find it useful, star [mkdocs-ng/mkdocs](https://github.com/mkdocs-ng/mkdocs) and [mkdocs-ng/mkdocs-sumi](https://github.com/mkdocs-ng/mkdocs-sumi), or share this with friends who still use MkDocs.

Website: [mkdocs-ng.org](https://mkdocs-ng.org/) · Sumi: [sumi.mkdocs-ng.org](https://sumi.mkdocs-ng.org/) · Plugin catalog: [catalog.mkdocs-ng.org](https://catalog.mkdocs-ng.org/)

Thanks, everyone.

---

Please cite the author and source when reproducing articles from this site. Do not use for any commercial purposes. Welcome to follow my WeChat Official Account "沈显鹏".
