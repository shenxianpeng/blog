---
title: "cpp-linter-hooks: The Most Complete pre-commit Solution for C/C++ Projects"
summary: |
  C/C++ tooling in the pre-commit ecosystem has long been limited. cpp-linter-hooks is currently the only pre-commit hook that supports both clang-format and clang-tidy, with built-in compilation database auto-detection, version pinning, and auto-fix capabilities.
tags:
  - Pre-Commit
  - C/C++
  - Open Source
authors:
  - shenxianpeng
date: 2026-05-20
---

If you work on Python projects, you've probably used `pre-commit` — running `black`, `ruff`, `mypy` before every `git commit`, blocking anything that doesn't meet the standard. This workflow is well-established in the Python ecosystem.

For C/C++ projects, it's a different story.

The official `mirrors-clang-format` hook only handles formatting. If you want clang-tidy for static analysis, you're on your own. Features like compilation database auto-detection, version pinning, or auto-fix? Not even on the radar.

[cpp-linter-hooks](https://github.com/cpp-linter/cpp-linter-hooks) fills this gap. It provides both `clang-format` and `clang-tidy` hooks in a single pre-commit repo, along with the supporting capabilities that C/C++ projects actually need.

---

## Why Not Just Use mirrors-clang-format?

Here's a quick comparison:

| Feature | cpp-linter-hooks | mirrors-clang-format |
|------|:---:|:---:|
| clang-format | ✅ | ✅ |
| clang-tidy | ✅ | ❌ |
| Inline style string (`--style`) | ✅ | ❌ |
| Tool version pinning (`--version`) | ✅ | ❌ (via rev tag) |
| Custom `.clang-tidy` config | ✅ | ❌ |
| Compilation database auto-detection | ✅ | ❌ |
| Dry-run mode | ✅ | ❌ |
| Auto-fix (`--fix` for clang-tidy) | ✅ | ❌ |
| Verbose output | ✅ | ❌ |
| Parallel execution (`--jobs`) | ✅ | ❌ |

`mirrors-clang-format` does one thing: download a `clang-format` binary and run it on changed files. If formatting is all you need, it works fine.

But in real-world C/C++ projects, the true headache isn't inconsistent formatting — it's clang-tidy diagnostics: memory leaks, undefined behavior, performance pitfalls. These are exactly the issues worth catching at commit time.

---

## Quick Start

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/cpp-linter/cpp-linter-hooks
    rev: v1.4.1
    hooks:
      - id: clang-format
        args: [--style=file]
      - id: clang-tidy
        args: [--checks=.clang-tidy]
```

Then:

```bash
pre-commit install
pre-commit run --all-files
```

The first run downloads the clang tools from PyPI. Subsequent runs use the cached environment.

---

## Practical Configuration Details

### Pin Your Tool Version

An easy detail to miss: `rev` is the project version of cpp-linter-hooks, not the clang tool version. Without an explicit version, upgrading `rev` may silently change your clang-format or clang-tidy version, leading to inconsistent results across your team.

Always add `--version`:

```yaml
- id: clang-format
  args: [--style=file, --version=21]
- id: clang-tidy
  args: [--checks=.clang-tidy, --version=21]
```

This locks the tool at clang 21 regardless of project `rev` upgrades.

### Compilation Database

clang-tidy needs compiler flags for accurate static analysis. If your project uses CMake or Meson, generate `compile_commands.json` and cpp-linter-hooks auto-detects it from common build directories (`build/`, `out/`, `cmake-build-debug/`, etc.) — no extra configuration needed.

You can also specify it explicitly:

```yaml
- id: clang-tidy
  args: [--compile-commands=build, --checks=.clang-tidy]
```

To generate the compilation database:

```bash
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -Bbuild .
```

### Auto-Fix

clang-tidy's `--fix` can auto-apply fixes for certain checks. cpp-linter-hooks supports this since v1.4.0, but it's opt-in — auto-modifying source code carries risk, and you should decide whether you trust it.

```yaml
- id: clang-tidy
  args: [--checks=.clang-tidy, --fix]
```

Note: enabling `--fix` automatically disables parallel execution (`--jobs`) to prevent concurrent writes to the same header file.

### Performance

Running full clang-tidy on a large codebase can be slow. Two ways to optimize:

**Limit scope** with the `files` filter:

```yaml
- id: clang-tidy
  args: [--checks=.clang-tidy, --version=21]
  files: ^(src|include)/.*\.(cpp|cc|cxx|h|hpp)$
```

**Enable parallelism**:

```yaml
- id: clang-tidy
  args: [--checks=.clang-tidy, --jobs=4]
```

For day-to-day development, you can also check only changed files:

```bash
pre-commit run --files $(git diff --name-only)
```

---

## Relationship with cpp-linter-action

If you've looked into C/C++ CI tooling, you might have seen [cpp-linter-action](https://github.com/cpp-linter/cpp-linter-action) (139 stars on GitHub Marketplace). It's a GitHub Action that runs clang-format and clang-tidy in CI pipelines and surfaces results as file annotations, thread comments, and PR reviews.

cpp-linter-hooks and cpp-linter-action are two complementary tools under the same organization:

- **cpp-linter-action**: runs in CI, designed for the PR review workflow
- **cpp-linter-hooks**: runs locally before `git commit`, designed for daily development

Both share the same `.clang-format` and `.clang-tidy` configuration files. Code that passes locally won't break in CI — a classic "local + CI dual-gate" pattern.

---

## Wrapping Up

cpp-linter-hooks is one of the main projects I maintain under the cpp-linter organization. Since 2022, it has grown to include version pinning, compilation database detection, auto-fix, and parallel execution — covering the core needs of C/C++ projects at the pre-commit stage.

If you develop in C/C++ or maintain a C/C++ open-source project, give it a try. Add it to your `.pre-commit-config.yaml`, and within minutes you'll have automatic formatting and static analysis running before every commit — no more waiting for CI to go red before fixing things.

- GitHub: https://github.com/cpp-linter/cpp-linter-hooks
- PyPI: https://pypi.org/project/cpp-linter-hooks/

Issues and feedback are welcome on GitHub.

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
