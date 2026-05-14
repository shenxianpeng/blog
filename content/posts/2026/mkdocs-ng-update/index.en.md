---
title: mkdocs-ng Maintenance Progress — v1.7.x Fix Summary and Next Steps
summary: |
  Since taking over mkdocs-ng maintenance, four versions have been released, over a dozen bugs fixed, and the mergedeep dependency removed. The upcoming v1.8.0 will be a feature release, planning to drop support for older Python versions, remove CDN dependencies from built-in themes, and provide a stable Python API.
tags:
  - OpenSource
  - MkDocs
authors:
  - shenxianpeng
date: 2026-05-14
series: ["MkDocs NG"]
series_order: 2
---

Hello everyone, I'm Shen Gong.

Last month, I wrote the article [Officially Maintaining MkDocs](mkdocs-ng), announcing that I had forked MkDocs and started publishing packages under mkdocs-ng.

At that time, v1.7.0 was released. Since then, four versions have been released, all the way to v1.7.3. This article summarizes the changes in these versions, provides an update to the community, and discusses the plans for v1.8.0.

## Version Update Overview

From April 24th to May 9th, four versions were released:

| Version | Date | Major Changes |
|---|---|---|
| v1.7.0 | 2026-04-24 | First release: rebranded as mkdocs-ng, added Python 3.13/3.14 support |
| v1.7.1 | 2026-04-25 | Bug Fixes: anchor validation, serve cleanup, color mode; removed mergedeep |
| v1.7.2 | 2026-04-27 | Bug Fixes: symlink, malformed IPv6 URLs, navigation dropdown arrow |
| v1.7.3 | 2026-05-09 | Bug Fixes: Click compatibility, livereload, search HTML tags; added content_title API |

Details are provided by version below.

---

## v1.7.0 (2026-04-24)

This is the first version of mkdocs-ng. The main change is the rebrand: the package name changed from `mkdocs` to `mkdocs-ng`, and documentation and repository links were updated to the mkdocs-ng organization. The CLI command remains `mkdocs`, and the configuration file remains `mkdocs.yml`.

In addition:

- Fixed an issue where the `mkdocs serve --livereload` parameter was not recognized.
- Added support for Python 3.13 and 3.14 (declaration and CI testing).
- Set up maintenance infrastructure: issue templates, Dependabot, Release Drafter, pre-commit hooks.

Installation method:

```bash
pip install -U mkdocs-ng
```

---

## v1.7.1 (2026-04-25)

Four bug fixes and one dependency cleanup.

**Anchor validation in `--strict` mode**

Previously, when strictly checking links using `mkdocs build -v --strict`, there were two issues: excluded pages were still checked, leading to false positives; and missing anchors only output a WARNING without returning a non-zero exit code, which couldn't be caught in CI. Both issues have been fixed. ([#30](https://github.com/mkdocs-ng/mkdocs/issues/30), [#32](https://github.com/mkdocs-ng/mkdocs/issues/32))

**Clean up temporary directory on `mkdocs serve` exit**

After `mkdocs serve` exits, it leaves behind temporary build directories in `/tmp`. Previously, cleanup only occurred on normal exit, not when a `SIGTERM` was received. Now, `SIGTERM` also triggers cleanup. ([#36](https://github.com/mkdocs-ng/mkdocs/issues/36))

**Color mode switch fails when highlightjs is disabled**

The dark/light mode toggle button in the built-in themes depended on highlightjs's loading status. If you disabled `highlightjs` in `mkdocs.yml`, the toggle button would stop working. Now, they are decoupled. ([#39](https://github.com/mkdocs-ng/mkdocs/issues/39))

**Remove mergedeep dependency**

`mergedeep` is an unmaintained third-party library that has been replaced with an inline deep-merge utility function. This reduces an external dependency and eliminates a potential supply chain risk. ([#29](https://github.com/mkdocs-ng/mkdocs/issues/29))

---

## v1.7.2 (2026-04-27)

Three bug fixes.

**Broken symlink causes build to crash**

If there was a dangling symlink (pointing to a deleted file) in the documentation directory, the entire `mkdocs build` would crash. Now, such symlinks are skipped, and the build continues. ([#46](https://github.com/mkdocs-ng/mkdocs/issues/46), [#43](https://github.com/mkdocs-ng/mkdocs/issues/43))

**Malformed URL causes build to crash**

If a malformed URL was configured in `mkdocs.yml` — for example, an incomplete IPv6 address like `https://[::1` — the entire build would also crash. This has been changed to output a clear warning, no longer interrupting the build. ([#45](https://github.com/mkdocs-ng/mkdocs/issues/45))

**Navigation dropdown submenu arrow invisible**

In the Material theme's navigation bar, items with submenus should have a small arrow icon on the right. Previously, this arrow inexplicably disappeared, making it unclear to users that there were submenus. This has been fixed. ([#44](https://github.com/mkdocs-ng/mkdocs/issues/44))

---

## v1.7.3 (2026-05-09)

Four bug fixes, one new API.

**New Click version causes abnormal CLI default values**

Starting with Click 8.3.0, the default parameter handling logic changed, causing abnormal behavior for parameters like `mkdocs serve`'s `--livereload` and `mkdocs build`'s `--strict` and `--use-directory-urls` — values configured in `mkdocs.yml` would be overridden by command-line defaults. Fixed. ([#60](https://github.com/mkdocs-ng/mkdocs/issues/60))

**Livereload overly sensitive to editor temporary files**

Editor-generated temporary files such as vim's swap files (`.md.swp`), Emacs's auto-save files (`#file.md#`), and tilde backup files (`file.md~`) would trigger a livereload rebuild on every change. Now these files are ignored, preventing frequent page refreshes while writing documentation. ([#55](https://github.com/mkdocs-ng/mkdocs/issues/55))

**Edge case HTML markup causes build to crash**

When `<<>>` or similar edge case markup was used in Markdown, Python's standard `html.parser` library would raise an `AssertionError`, interrupting the entire build. Fixed. ([#51](https://github.com/mkdocs-ng/mkdocs/issues/51))

**Raw HTML tags displayed in search results**

If a page's title contained HTML tags (e.g., a command name wrapped in `` `<code>` ``), the search index would include these tags verbatim, leading to a mess of HTML source in search results. Now, titles in the search index automatically strip HTML tags. ([#53](https://github.com/mkdocs-ng/mkdocs/issues/53))

**Added `page.content_title` attribute**

A new API, `page.content_title`, has been provided for plugin developers to directly get the plain text of the first heading on a page (HTML tags are stripped). Previously, plugin authors had to write regex to parse H1s themselves in `on_page_content`; now, they can simply access the attribute. ([#52](https://github.com/mkdocs-ng/mkdocs/issues/52))

---

Full changelog available at: [mkdocs-ng Release Notes](https://mkdocs-ng.github.io/mkdocs/about/release-notes/)

---

## About v1.8.0

The core mission for the v1.7.x series was bug fixing and stabilizing the foundation. Now that these are mostly done, the upcoming v1.8.0 will be a feature-rich version. Here's the current plan.

**Dropping Python 3.8 and 3.9**

Python 3.8 reached EOL in October 2024, and 3.9 will reach EOL in October 2025. v1.8.0 will remove these officially unsupported Python versions from the support matrix, raising the minimum supported version to Python 3.10. This means we can use more modern syntax like `|` type union and `match`/`case`, which will benefit future maintenance and feature development. ([#33](https://github.com/mkdocs-ng/mkdocs/issues/33))

**Remove external CDN dependencies from built-in themes**

The `mkdocs` and `readthedocs` built-in themes load fonts and CSS from Google Fonts and CDNs. For deployment scenarios requiring complete offline access or privacy, this has been a long-standing pain point (18 👍 on the upstream issue). v1.8.0 plans to bundle necessary resources within the themes, eliminating third-party requests. ([mkdocs/mkdocs#2171](https://github.com/mkdocs/mkdocs/issues/2171))

**Provide a stable Python API**

MkDocs currently lacks an officially supported Python API — to call build or serve in code, one must either use internal functions or `subprocess`. v1.8.0 plans to provide a documented public API (e.g., `mkdocs.build()`, `mkdocs.serve()`) to facilitate integration with CI scripts and build systems. ([mkdocs/mkdocs#1240](https://github.com/mkdocs/mkdocs/issues/1240))

**Automatically generated navigation uses index page title**

When `nav` is not explicitly configured in `mkdocs.yml`, MkDocs uses directory names as navigation group titles. Changing this to use the index page's title would be more natural — for example, if `index.md` in the `about/` directory has the title "About This Project", the navigation bar would display "About This Project" instead of `about`. ([#54](https://github.com/mkdocs-ng/mkdocs/issues/54))

**Clean up more outdated dependencies**

Following the removal of `mergedeep` in v1.7.1, v1.8.0 plans to continue auditing and cleaning up unmaintained dependencies to reduce the overall number of external dependencies.

The complete feature plan is continuously updated in [MkDocs-NG Feature Plan](https://github.com/mkdocs-ng/mkdocs/issues/59). If you're using MkDocs and have any persistent issues that haven't been addressed upstream, you can leave a comment in that issue or open a separate issue in the repository.

---

## How to Switch Over

If you were previously using the old `mkdocs` package:

```bash
pip uninstall mkdocs
pip install mkdocs-ng
```

The CLI commands, configuration files, and plugin namespaces all remain unchanged. The only change is the package name from `mkdocs` to `mkdocs-ng`.

If you are using `requirements.txt` or `pyproject.toml`:

```diff
- mkdocs>=1.6.0
+ mkdocs-ng>=1.7.3
```

The same applies to Material for MkDocs users:

```bash
pip uninstall mkdocs-material
pip install mkdocs-ng-material
```

---

Repository addresses:

- [mkdocs-ng/mkdocs](https://github.com/mkdocs-ng/mkdocs)
- [mkdocs-ng/mkdocs-material](https://github.com/mkdocs-ng/mkdocs-material)

Feel free to open issues, give a Star, and share with friends still using MkDocs.

---

Please cite the author and source when reproducing articles from this site. Do not use for any commercial purposes. Welcome to follow my WeChat Official Account "沈显鹏".