---
title: "pybadges Fails on Python 3.13: How to Fix \"No module named 'imghdr'\""
summary: |
  pybadges 3.0.1 imports imghdr, which Python 3.13 removed, and pkg_resources, which setuptools 82 removed, so it fails with "No module named 'imghdr'" or "No module named 'pkg_resources'". The project is archived and will not get a fix. Three ways out: pin around it for now, use the patched Debian package, or switch to badgepy, a drop-in continuation that I maintain.
tags:
  - Python
  - Troubleshooting
authors:
  - shenxianpeng
date: 2026-11-06
---

If you generate badges with [pybadges][pybadges] and just moved a project or a CI image to Python 3.13, this is probably what brought you here:

```text
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from pybadges import badge
  File ".venv/lib/python3.13/site-packages/pybadges/__init__.py", line 33, in <module>
    import imghdr
ModuleNotFoundError: No module named 'imghdr'
```

Or this one, which can show up without touching Python at all:

```text
  File ".venv/lib/python3.12/site-packages/pybadges/precalculated_text_measurer.py", line 21, in <module>
    import pkg_resources
ModuleNotFoundError: No module named 'pkg_resources'
```

Below is why it happens and three ways to fix it. One of them is badgepy, which I maintain, so keep that in mind when you read option 3.

## Why it happens

pybadges 3.0.1, the last release (October 2023), imports two modules that are going away:

- `imghdr` was removed from the standard library in Python 3.13, as part of [PEP 594][pep594].
- `pkg_resources` was never in the standard library. It comes with setuptools, and pybadges does not list setuptools as a dependency; it assumes setuptools is installed. Virtual environments created with Python 3.12 or later don't include setuptools, and [setuptools 82.0.0][setuptools] (released on 8 February 2026) no longer ships `pkg_resources` at all.

| Your environment | What you get |
|---|---|
| Python 3.13 or later | `No module named 'imghdr'` |
| Python 3.12 or earlier, no setuptools in the environment | `No module named 'pkg_resources'` |
| Python 3.12 or earlier, setuptools 82.0.0 or later | `No module named 'pkg_resources'` |
| Python 3.12 or earlier, setuptools older than 82 | Works, with a `UserWarning` that `pkg_resources` is deprecated |

No fix is coming. [google/pybadges][pybadges] was archived on 11 August 2025, and its last commit is from June 2024.

It still gets about 36,700 downloads a month, according to [pypistats][pypistats], and two thirds of them come from Python 3.10, 3.11 and 3.12. Python 3.10 reached end of life in October 2026, so a lot of those installs will meet the first error over the next year.

## Option 1: pin around it (short-term)

On Python 3.12 or earlier, install a setuptools that still has `pkg_resources`:

```sh
pip install "pybadges==3.0.1" "setuptools<82"
```

On Python 3.13 or later, you also need `imghdr` back. The [standard-imghdr][deadlib] package is a copy of the removed module:

```sh
pip install "pybadges==3.0.1" "setuptools<82" standard-imghdr
```

I tried both on Python 3.12, 3.13 and 3.14, and the badges came out the same as before. But you are now holding setuptools back in that environment and relying on a module the standard library dropped. That buys time; it doesn't fix anything.

## Option 2: the Debian or Ubuntu package

If you install pybadges with apt rather than pip, you are probably fine already. The distribution package [python3-pybadges 3.0.1-3][debian], maintained by the Debian Python Team, patches both imports:

```sh
sudo apt install python3-pybadges
```

This only helps code that runs on the system Python. A `pip install` in a virtual environment or in CI still gets the unpatched release from PyPI.

## Option 3: switch to badgepy

[badgepy][badgepy] is a maintained continuation of pybadges. I forked it when I needed pybadges for a project and its open issues had stopped getting answers. The `badge()` function takes the same arguments in the same order, the command line takes the same flags, and for the same arguments the SVG is the same, byte for byte, apart from two bug fixes listed in the migration guide. It doesn't use `imghdr` or `pkg_resources`, supports Python 3.10 to 3.15, and is Apache-2.0 licensed like pybadges.

For most projects the change is two lines:

```diff
- pybadges==3.0.1
+ badgepy>=2.0
```

```diff
- from pybadges import badge
+ from badgepy import badge
```

On the command line, `python -m pybadges` becomes `badgepy`:

```sh
badgepy --left-text=build --right-text=passing --right-color=green
```

If you are still on Python 3.9 (about a quarter of pybadges downloads last month), pin `badgepy>=1.3,<2`. badgepy 2.0 needs Python 3.10 or later.

## What else badgepy does

pybadges only turns text into a badge. badgepy can also read the files your CI already produces and write the badge to a file, with no external service involved:

```sh
badgepy from-coverage coverage.xml -o badges/coverage.svg
badgepy from-junit results.xml -o badges/tests.svg
badgepy from-pyproject --query project.version --label version -o badges/version.svg
badgepy preset build passing -o badges/build.svg
```

Commit the SVG files or publish them as build artifacts, and your README can show them without a request to shields.io on every page view.

## The full migration guide

The [pybadges migration guide][guide] covers the rest: the text measurer modules, what replaces `pybadges.version`, a one-line command to rename every import in a repository, and the few places where badgepy behaves differently on purpose, such as a 10-second timeout when it fetches a remote logo.

If something that worked with pybadges breaks after the switch, please [open an issue][issues].

[pybadges]: https://github.com/google/pybadges
[pep594]: https://peps.python.org/pep-0594/
[setuptools]: https://setuptools.pypa.io/en/stable/history.html#v82-0-0
[pypistats]: https://pypistats.org/packages/pybadges
[deadlib]: https://pypi.org/project/standard-imghdr/
[debian]: https://packages.debian.org/sid/python3-pybadges
[badgepy]: https://github.com/shenxianpeng/badgepy
[guide]: https://github.com/shenxianpeng/badgepy/blob/main/docs/pybadges-migration.md
[issues]: https://github.com/shenxianpeng/badgepy/issues
