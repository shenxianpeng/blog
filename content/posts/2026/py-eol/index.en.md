---
title: "py-eol 1.0: Catch End-of-Life Python Versions in CI"
summary: |
  py-eol checks whether the Python versions your project uses have reached end of life. It scans project files and reports each EOL version with its file and line number, warns ahead of time with --warn-before, and runs in CI as a GitHub Action or a pre-commit hook so expired versions cannot slip back in.
tags:
  - py-eol
  - Python
authors:
  - shenxianpeng
date: 2026-03-23
series: ["My Open Source Projects"]
series_order: 2
---

Python 3.9 reached end of life on 31 October 2025.

End of life means the core developers stop maintaining that version, security fixes included. If your project still runs on 3.9, nobody is patching the interpreter underneath it anymore.

In practice, most people don't keep an eye on this. `pyproject.toml` gets written once and forgotten. The base image in the Dockerfile has never been touched. The Python version in the GitHub Actions workflow was set two years ago. By the time someone thinks to check, months have gone by.

I've just released **py-eol 1.0.0** to deal with exactly this. I [first wrote about py-eol](../../2025/py-eol/) in December 2025. Version 1.0 adds more file types, early warnings with `--warn-before`, and a GitHub Action.

---

## It does one thing: tell you when a Python version expires

```bash
pip install py-eol
```

Once installed, you can check any version directly:

```bash
py-eol versions 3.9
# ⚠️ Python 3.9 is already EOL since 2025-10-31

py-eol versions 3.10 --warn-before 365
# ⏰ Python 3.10 will be EOL on 2026-10-31 (229 days remaining)

py-eol versions 3.12
# ✅ Python 3.12 is still supported until 2028-10-31
```

`--warn-before DAYS` is the option I find most useful. You don't want to learn about an EOL on the day it happens. Start warning N days ahead and the team has time to plan the migration.

---

## Scan your project files, down to the line

The more practical use is scanning the project itself:

```bash
py-eol files pyproject.toml Dockerfile .github/workflows/ci.yml
```

The output tells you which file, and which line, uses an EOL version:

```text
pyproject.toml:9: ⚠️ Python 3.7 is already EOL since 2023-06-27
.github/workflows/ci.yml:16: ⚠️ Python 3.9 is already EOL since 2025-10-31
Dockerfile:1: ⚠️ Python 3.8 is already EOL since 2024-10-07
```

Supported files: `pyproject.toml`, `setup.py`, `.python-version`, `tox.ini`, `Dockerfile`, and GitHub Actions workflow files.

---

## Run it in CI

### GitHub Action

```yaml
- name: Check Python EOL
  uses: shenxianpeng/py-eol@main
  with:
    warn-before: "180"
```

It checks on every push or pull request and fails the pipeline when it finds a problem. You can also put it on a schedule, for example every Monday morning:

```yaml
on:
  schedule:
    - cron: "0 8 * * 1"
```

### pre-commit hook

```yaml
repos:
  - repo: https://github.com/shenxianpeng/py-eol
    rev: v1.0.0
    hooks:
      - id: py-eol
```

It scans before every commit and stops the problem right there.

---

## Or use it as a Python module

```python
from py_eol import is_eol, get_eol_date, days_until_eol, is_eol_soon
from py_eol import supported_versions, eol_versions, latest_supported_version

print(is_eol("3.7"))               # True
print(days_until_eol("3.12"))      # days remaining
print(is_eol_soon("3.10", 365))    # True if EOL within a year
print(supported_versions())        # all currently supported versions
print(latest_supported_version())  # 3.14
```

---

## Exit codes

| Exit code | Meaning |
|-----------|---------|
| `0` | All versions are supported |
| `1` | An EOL version was found (or one EOL soon, with `--warn-before`) |
| `2` | An unknown version was found |

That makes it easy to branch on the result in shell scripts and CI.

---

Python version lifecycles are a blind spot for most teams. Everyone knows EOL dates exist. They are just never urgent and never visible, so more pressing work keeps pushing them aside.

The point of py-eol is to move this from "someone has to remember" to "CI reminds you".

If you maintain Python projects, give it a try. You may find a few versions that should have been upgraded a while ago.

**https://github.com/shenxianpeng/py-eol**

**Update, October 2026:** Python 3.10 is next. It reaches end of life on 31 October 2026. The current release is [py-eol 1.2.0](https://github.com/shenxianpeng/py-eol/releases).
