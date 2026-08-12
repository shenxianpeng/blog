---
title: mkdocs-ng v1.8.0 Released — Upstream Issues Fixed, Builds ~14% Faster
summary: |
  mkdocs-ng v1.8.0 is out, the first feature release since the fork. Built-in themes no longer copy the entire highlight.js distribution, making clean builds ~14% faster with ~440 fewer files per site. Search finally finds programming keywords like while and if. The next release will bring incremental builds to mkdocs serve.
tags:
  - Open Source
  - Documentation
authors:
  - shenxianpeng
date: 2026-08-13
series: ["MkDocs NG"]
series_order: 3
---

mkdocs-ng v1.8.0 was released on August 13 (UTC: the evening of the 12th) — the first feature release since the fork. The four versions from v1.7.0 to v1.7.3 were about fixing bugs and laying groundwork; 1.8.0 starts delivering the features promised earlier.

For new readers, some background: upstream MkDocs has not had a new release since August 2024, and maintenance has essentially stalled. I forked it and continue to maintain it under the mkdocs-ng organization. The package name is mkdocs-ng, but the CLI command, configuration file, and plugin ecosystem are all unchanged. Why I did this and what v1.7.x fixed are covered in my [earlier posts](https://shenxianpeng.github.io/posts/2026/mkdocs-ng/) ([v1.7.x summary](https://shenxianpeng.github.io/posts/2026/mkdocs-ng-update/)), so I won't repeat them here.

This post covers three things: which long-standing upstream issues have been fixed, how much faster 1.8.0 builds are, and what 1.9.0 plans to do.

## Upstream issues, fixed

Since taking over, the docs include a [Fixed Upstream Issues](https://mkdocs-ng.github.io/mkdocs/about/fixed-upstream-issues/) page tracking "reported upstream but never fixed" problems. Ten are listed so far, all resolved. Here are the ones with the biggest impact.

**`mkdocs serve` stopped watching files ([upstream #4032](https://github.com/mkdocs/mkdocs/issues/4032)).** This is the most-upvoted open issue upstream: 66 reactions and 31 comments. After Click 8.2 changed how default parameters are handled, `mkdocs serve` no longer watched for file changes, and live reload only worked when `--livereload` was passed explicitly. The symptom was so odd that many users misdiagnosed it as a WSL problem. mkdocs-ng fixed the root cause, so there is no need to pin an older Click; the related `use_directory_urls` being silently overridden was fixed along the way.

**Editor temporary files triggered pointless rebuilds ([upstream #2519](https://github.com/mkdocs/mkdocs/issues/2519)).** vim swap files, `~` backups, and Emacs auto-save files each triggered a rebuild on every change, so the page kept refreshing while you wrote. Since 1.7.3 these files are ignored.

**Search could not find programming keywords ([upstream #4167](https://github.com/mkdocs/mkdocs/issues/4167)).** `while`, `if`, `for`, `from` are genuine keywords in technical documentation, yet search filtered them out as English stop words and returned nothing. Since 1.8.0 these words are indexed by default; to restore the old behavior, set `stop_words: true` on the search plugin.

**Two long-standing anchor validation problems.** First, false positives: anchors generated late by extensions like `pymdownx.tabbed` were reported as broken links ([upstream #3690](https://github.com/mkdocs/mkdocs/issues/3690)). Second, weak diagnostics: when an anchor differed only in letter case, the warning said "does not exist" without saying how to fix it ([upstream #3703](https://github.com/mkdocs/mkdocs/issues/3703)). The latter now suggests the correct anchor, e.g. `did you mean '#conflicts'?`.

**Third-party dependencies in the built-in themes ([upstream #2171](https://github.com/mkdocs/mkdocs/issues/2171), 18 reactions).** Theme assets used to load from CDNs, which broke offline and intranet deployments and exposed visitor data to third parties. 1.8.0 bundles highlight.js into the themes, and neither built-in theme has any CDN reference left. The dead Universal Analytics snippet, shut down by Google in 2023, was removed too ([upstream #3630](https://github.com/mkdocs/mkdocs/issues/3630)).

**A stable Python API ([upstream #1240](https://github.com/mkdocs/mkdocs/issues/1240), 10 reactions).** Previously, driving a build from code meant `subprocess` calls or private imports. Now `mkdocs.build()` and `mkdocs.serve()` are documented public API that CI scripts and build systems can call directly.

A few crash-class bugs were also fixed: edge-case markup like `<<>>` triggered an `AssertionError` from `html.parser` on Python 3.13.5+, aborting the build ([upstream #4001](https://github.com/mkdocs/mkdocs/issues/4001)); a broken symlink in the docs directory crashed the whole build; so did a malformed IPv6 URL. All resolved in v1.7.x.

## Performance: builds ~14% faster, ~440 fewer files per site

The biggest performance change in 1.8.0 started with a profiling run: analyzing a 204-page site showed that of 472 static files being copied, 444 came from highlight.js — 192 language grammars and ~250 styles. A site only ever references the handful selected in its configuration. For small sites this fixed cost dominated: on a 10-page site, close to half the build time was spent copying grammar files nothing ever loads.

The fix is straightforward: built-in themes now copy only the assets the configuration actually references — the languages listed in `hljs_languages`, the styles picked by `hljs_style`, and nothing under `highlight/` when `highlightjs` is disabled. Sites overriding the theme via `custom_dir` are unaffected; the filter skips third-party themes and custom directories.

Measured locally (wall time):

| Scenario | Before | After |
|----------|--------|-------|
| Clean build, 10 pages | 200 ms | 172 ms (−14%) |
| Clean build, 200 pages | 2.99 s | 2.54 s (−15%) |
| Files copied per site | 512 | 74 |

Built sites shrink by ~440 files / ~2 MB — faster deploy uploads and a cleaner host.

The same PR removed another waste: when the search plugin is configured with `indexing: titles`, the whole-page HTML parse that was never used is now skipped, with identical index output.

One more thing: since 1.8.0, every pull request runs a performance benchmark suite on CodSpeed, so build-speed regressions are caught before merge. "Performance optimization" without measurement tends to regress quietly; we wanted that institutionalized.

## 1.9.0 preview: the next performance target is serve

The performance work is not done. 1.9.0 will focus on the `mkdocs serve` build pipeline, with incremental builds and a smarter file watcher in mind. The demand comes from [upstream #3695](https://github.com/mkdocs/mkdocs/issues/3695), opened by the Material for MkDocs maintainer: 15 reactions, 22 comments, and the top open item in the mkdocs-ng feature plan.

Why it matters can be shown with numbers. In a scaling study, sites of 100, 400, and 1600 pages cost 7.8 ms, 9.3 ms, and 22.1 ms per page on average. The cost is not linear — the larger the site, the more expensive each page gets. That is the O(N²) navigation-rendering problem #3695 describes: the bigger your docs, the worse serve feels.

The CodSpeed baseline is in place and the optimization work is underway. By the time 1.9.0 ships, I hope these numbers move visibly. If you have a pain point with serve, feel free to comment on the [feature plan](https://github.com/mkdocs-ng/mkdocs/issues/59).

## Switching over

If you are still on the upstream `mkdocs` package:

```bash
pip uninstall mkdocs
pip install -U mkdocs-ng
```

CLI, configuration, and plugins all stay the same; only the package name changes. One note: 1.8.0 requires Python 3.10+, and since Python 3.8 and 3.9 are both end-of-life, pip will keep installing 1.7.x on those versions.

If you use MkDocs, a few things would genuinely help: try `mkdocs-ng` instead of `mkdocs`, open an issue on [GitHub](https://github.com/mkdocs-ng/mkdocs) when something breaks, and star the repo. And if you would like, share this with colleagues still on MkDocs, so they know there is a maintained option beyond upstream.

Repository: [mkdocs-ng/mkdocs](https://github.com/mkdocs-ng/mkdocs) · Release notes: [Release Notes](https://mkdocs-ng.github.io/mkdocs/about/release-notes/) · Fixed upstream issues: [Fixed Upstream Issues](https://mkdocs-ng.github.io/mkdocs/about/fixed-upstream-issues/) · Feature plan: [Feature Plan](https://github.com/mkdocs-ng/mkdocs/issues/59)

---

Please cite the author and source when reproducing articles from this site. Do not use for any commercial purposes. Welcome to follow my WeChat Official Account "沈显鹏".
