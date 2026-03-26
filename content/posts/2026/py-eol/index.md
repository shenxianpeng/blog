---
title: 你的项目还在跑 Python 3.9 吗？我写了个工具来盯着这件事
summary: |
    py-eol 是一个专门用来检查 Python 版本是否快到期的工具。它可以扫描项目文件，精确到行号，告诉你哪些地方还在用 EOL 的版本。还可以接入 CI，让检查自动跑，不让过期版本偷偷混进来。
tags:
  - py-eol
  - python
authors:
  - shenxianpeng
date: 2026-03-23
translate: false
series: ["我的开源项目"]
series_order: 2
---

# 你的项目还在跑 Python 3.9 吗？我写了个工具来盯着这件事

上个月，Python 3.9 正式 EOL 了。

EOL，End of Life——官方停止维护，不再修安全漏洞。如果你的项目还在跑 3.9，理论上你就在裸奔。

但现实是：大多数人不会专门去盯这件事。`pyproject.toml` 写完就忘了，Dockerfile 里的基础镜像版本从来没动过，GitHub Actions 里的 Python 版本也是两年前配的。等你想起来检查，往往已经过了好几个月。

我最近发布了 **py-eol v1.0.0**，专门用来解决这个问题。

---

## 它做一件事：告诉你 Python 版本快到期了

```bash
pip install py-eol
```

装好之后，可以直接查版本状态：

```bash
py-eol versions 3.9
# ⚠️ Python 3.9 is already EOL since 2025-10-31

py-eol versions 3.10 --warn-before 180
# ⏰ Python 3.10 will be EOL on 2026-10-31 (229 days remaining)

py-eol versions 3.12
# ✅ Python 3.12 is still supported until 2028-10-31
```

`--warn-before DAYS` 是我觉得最实用的参数——不想等到 EOL 当天才知道，提前 N 天就开始报警，给团队留出迁移时间。

---

## 扫描项目文件，精确到行号

更实用的是直接扫描整个项目：

```bash
py-eol files pyproject.toml Dockerfile .github/workflows/ci.yml
```

输出会告诉你哪个文件、第几行用了 EOL 的版本：

```
pyproject.toml:9: ⚠️ Python 3.7 is already EOL since 2023-06-27
.github/workflows/ci.yml:16: ⚠️ Python 3.9 is already EOL since 2025-10-31
Dockerfile:1: ⚠️ Python 3.8 is already EOL since 2024-10-07
```

支持的文件类型：`pyproject.toml`、`setup.py`、`.python-version`、`tox.ini`、`Dockerfile`、GitHub Actions workflow 文件。

---

## 接入 CI，让检查自动跑

### GitHub Action

```yaml
- name: Check Python EOL
  uses: shenxianpeng/py-eol@main
  with:
    warn-before: "180"
```

每次 push 或 PR 自动检查，发现问题直接让流水线失败。也可以配定时任务，每周一早上主动跑一次：

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

每次 commit 之前自动扫描，有问题当场拦住。

---

## 也可以当 Python 模块用

```python
from py_eol import is_eol, get_eol_date, days_until_eol, is_eol_soon
from py_eol import supported_versions, eol_versions, latest_supported_version

print(is_eol("3.7"))               # True
print(days_until_eol("3.12"))      # 还有多少天
print(is_eol_soon("3.10", 365))    # True，如果一年内到期
print(supported_versions())        # 当前所有受支持版本列表
print(latest_supported_version())  # 3.14
```

---

## 退出码

| 退出码 | 含义 |
|--------|------|
| `0` | 全部版本在支持期内 |
| `1` | 发现 EOL 版本（或即将到期） |
| `2` | 遇到未知版本 |

方便直接在 shell 脚本和 CI 里做判断。

---

Python 版本的生命周期管理，是大多数团队的盲区——不是不知道 EOL 这件事，而是它不紧急、不显眼，总被优先级更高的事情挤掉。

py-eol 的目的很简单：把这件事从「需要人主动记住」变成「CI 自动提醒你」。

如果你维护着 Python 项目，装上试试，说不定会发现有几个版本早就该升了。

**https://github.com/shenxianpeng/py-eol**