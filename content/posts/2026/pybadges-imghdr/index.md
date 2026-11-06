---
title: "pybadges 在 Python 3.13 上报错 No module named 'imghdr'，怎么办"
summary: |
  pybadges 3.0.1 用到了 imghdr 和 pkg_resources。前者在 Python 3.13 被移出标准库，后者在 setuptools 82 里被删掉，所以 import 时会报 "No module named 'imghdr'" 或 "No module named 'pkg_resources'"。项目已经归档，不会再修。这篇讲三种办法：临时锁版本、用 Debian 打过补丁的包，或者换成我维护的 badgepy。
tags:
  - Python
  - Troubleshooting
authors:
  - shenxianpeng
date: 2026-11-06
---

如果你用 [pybadges][pybadges] 生成徽章，最近又把项目或 CI 镜像升到了 Python 3.13，多半是看到了这个：

```text
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from pybadges import badge
  File ".venv/lib/python3.13/site-packages/pybadges/__init__.py", line 33, in <module>
    import imghdr
ModuleNotFoundError: No module named 'imghdr'
```

还有一个报错，就算不升级 Python 也可能碰上：

```text
  File ".venv/lib/python3.12/site-packages/pybadges/precalculated_text_measurer.py", line 21, in <module>
    import pkg_resources
ModuleNotFoundError: No module named 'pkg_resources'
```

下面说说原因和三种解决办法。先说明一下，第三种办法里的 badgepy 是我维护的项目，读的时候请心里有数。

## 为什么会报错

pybadges 的最后一个版本是 2023 年 10 月发布的 3.0.1，它 import 了两个正在消失的模块。

- `imghdr`：Python 3.13 按照 [PEP 594][pep594] 把它从标准库里删掉了。
- `pkg_resources`：它从来不在标准库里，是 setuptools 自带的。pybadges 没把 setuptools 列为依赖，只是假定环境里装了它。可是 Python 3.12 起新建的虚拟环境不再自带 setuptools，2026 年 2 月 8 日发布的 [setuptools 82.0.0][setuptools] 更是直接去掉了 `pkg_resources`。

| 环境 | 结果 |
|---|---|
| Python 3.13 及以上 | `No module named 'imghdr'` |
| Python 3.12 及以下，环境里没有 setuptools | `No module named 'pkg_resources'` |
| Python 3.12 及以下，setuptools 82.0.0 或更新 | `No module named 'pkg_resources'` |
| Python 3.12 及以下，setuptools 低于 82 | 能用，但会有一条 `pkg_resources` 已弃用的 `UserWarning` |

上游也不会再修了。[google/pybadges][pybadges] 在 2025 年 8 月 11 日归档，最后一次提交是 2024 年 6 月。

根据 [pypistats][pypistats] 的数据，它现在每个月还有大约 36,700 次下载，其中三分之二来自 Python 3.10、3.11 和 3.12。Python 3.10 已经在 2026 年 10 月停止维护，接下来一年，这些安装里会有不少撞上第一个报错。

## 办法一：锁版本绕过去（只能撑一阵）

Python 3.12 及以下，装一个还带 `pkg_resources` 的 setuptools 就行：

```sh
pip install "pybadges==3.0.1" "setuptools<82"
```

Python 3.13 及以上，还得把 `imghdr` 补回来。[standard-imghdr][deadlib] 这个包就是被删掉的那个模块的拷贝：

```sh
pip install "pybadges==3.0.1" "setuptools<82" standard-imghdr
```

这两种我在 Python 3.12、3.13 和 3.14 上都试过，生成的徽章和原来一样。代价是这个环境里的 setuptools 被卡在旧版本，还要依赖一个标准库已经丢掉的模块。这样能争取一些时间，问题本身还在。

## 办法二：用 Debian 或 Ubuntu 的包

如果你是用 apt 而不是 pip 装的 pybadges，多半已经没事了。Debian Python Team 维护的 [python3-pybadges 3.0.1-3][debian] 给这两处 import 都打了补丁：

```sh
sudo apt install python3-pybadges
```

它只对系统 Python 上跑的代码有用。在虚拟环境或 CI 里 `pip install`，拿到的仍然是 PyPI 上没打补丁的版本。

## 办法三：换成 badgepy

[badgepy][badgepy] 是 pybadges 的延续版本，一直有人维护。当初我有个项目要用 pybadges，碰到几个 bug，issue 提了也没人回，就 fork 了一份自己修。

`badge()` 的参数和顺序没变，命令行参数也没变。同样的参数生成的 SVG 逐字节相同，只有迁移指南里列出的两处 bug 修复例外。它不依赖 `imghdr` 和 `pkg_resources`，支持 Python 3.10 到 3.15，和 pybadges 一样是 Apache-2.0 协议。

大多数项目只要改两行：

```diff
- pybadges==3.0.1
+ badgepy>=2.0
```

```diff
- from pybadges import badge
+ from badgepy import badge
```

命令行里把 `python -m pybadges` 换成 `badgepy`：

```sh
badgepy --left-text=build --right-text=passing --right-color=green
```

如果你还在用 Python 3.9（上个月 pybadges 的下载里大约四分之一来自 3.9），请锁定 `badgepy>=1.3,<2`，因为 badgepy 2.0 要求 Python 3.10 及以上。

## badgepy 还能做什么

pybadges 只能把文字变成徽章。badgepy 还能直接读取 CI 已经生成的文件，把徽章写成文件，不需要任何外部服务：

```sh
badgepy from-coverage coverage.xml -o badges/coverage.svg
badgepy from-junit results.xml -o badges/tests.svg
badgepy from-pyproject --query project.version --label version -o badges/version.svg
badgepy preset build passing -o badges/build.svg
```

这些 SVG 可以直接提交到仓库，或者作为构建产物发布。README 引用它们，就不用每次打开页面都去请求 shields.io。

## 完整的迁移指南

更多细节在 [pybadges 迁移指南][guide]（英文）里：文字宽度测量的几个模块、`pybadges.version` 用什么替代、一行命令批量改掉仓库里的 import，以及 badgepy 有意改变的几处行为，比如拉取远程 logo 时设了 10 秒超时。

换过去以后，如果有在 pybadges 里正常、在 badgepy 里不正常的地方，欢迎[提 issue][issues]。

[pybadges]: https://github.com/google/pybadges
[pep594]: https://peps.python.org/pep-0594/
[setuptools]: https://setuptools.pypa.io/en/stable/history.html#v82-0-0
[pypistats]: https://pypistats.org/packages/pybadges
[deadlib]: https://pypi.org/project/standard-imghdr/
[debian]: https://packages.debian.org/sid/python3-pybadges
[badgepy]: https://github.com/shenxianpeng/badgepy
[guide]: https://github.com/shenxianpeng/badgepy/blob/main/docs/pybadges-migration.md
[issues]: https://github.com/shenxianpeng/badgepy/issues
