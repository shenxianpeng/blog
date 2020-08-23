---
title: 如何在 GitHub 上发布一个企业级的 Python 项目
tags:
  - Python
  - PyPI
  - Release
categories:
  - Python
date: 2020-08-23 16:13:17
author: shenxianpeng
---

## 目录

* 选择 License
* 配置 setup.py
* 发布到 PyPI
* 关于 pydoc
* 关于版本号

<!-- more -->

## 选择 License

这里由一篇关于如何选择 GitHub License 的文章 [Github仓库如何选择开源许可证](https://mp.weixin.qq.com/s/CjeWol3BdGkmGZi-zMnDkQ)，这里就不过多介绍。

## 配置 setup.py

官方有详细的示例和文档 https://packaging.python.org/tutorials/packaging-projects/。

这里还有一个 sample 项目供你参考 https://github.com/pypa/sampleproject

攒点耐心将上面两个链接阅读，就基本可以满足一般项目的发布要求了。

这里着重介绍下引入 `MANIFEST.in` 文件的作用。它是用来定制化生成 `dist/*.tar.gz` 时需要用到的。

假设你的项目目录结构如下：

```
demo
├── LICENSE
├── README.md
├── MANIFEST.in
├── demo
│   └── __init__.py
├── setup.py
├── tests
│   └── __init__.py
│   └── __pycache__/
└── docs
```

在使用打包命令 `python setup.py sdist bdist_wheel`，将会生成在 dist 目录下生成两个文件 `demo-1.0.0-py3-none-any.whl` 和 `demo-1.0.0.tar.gz`

`.whl` 文件是用于执行 `pip install dist/demo-1.0.0-py3-none-any.whl` 将其安装到 `...\Python38\Lib\site-packages\demo` 目录时使用的文件。

`.tar.gz` 是打包后的源代码的存档文件。而 `MANIFEST.in` 则是用来控制这个文件里到底要有哪些内容。

以下面的 `MANIFEST.in` 文件为例：

```python
include LICENSE
include README.md
include MANIFEST.in
graft demo
graft tests
graft docs
global-exclude __pycache__
global-exclude *.log
global-exclude *.pyc
```

根据以上文件描述，在使用命令 `python setup.py sdist bdist_wheel` 生成 `demo-1.0.0.tar.gz` 文件时会包含 `LICENSE`, `README.md`, `MANIFEST.in` 这三个文件，并且还会包含 `demo`, `tests`, `docs` 三个目录下的所有文件，最后排除掉所有的 `__pycache__`, `*.log`, `*.pyc` 文件。

更多关于  `MANIFEST.in` 文件的语法请参看 https://packaging.python.org/guides/using-manifest-in/

## 发布到 PyPI

使用 Python 编程的人都知道，Python 的优势之一就是有大量的第三方库，通常使用如下命令

```
pip install xxxx
```

就可以轻松下载，真是即酷炫又方便。

### 什么是 PyPI

PyPI 是 The Python Package Index 的缩写，意思是 Python 包索引仓库，用来查找、安装和发布 Python 包。

PyPI 又两个环境，一个是测试环境 [TestPyPI](https://test.pypi.org/) 和 正式环境 [PyPI](https://pypi.org/)

### 准备

1. 如果想熟悉 PyPI 发布工具和发布流程可以使用测试环境 [TestPyPI](https://test.pypi.org/) 
2. 如果已经熟悉了 PyPI 的发布工具和流程可以直接使用正式环境 [PyPI](https://pypi.org/)
3. TestPyPI 和 PyPI 需要单独注册，即在正式环境注册了，如果去使用测试环境也同样需要注册。
4. 已经写好并且可以正常使用的项目/库/方法。

发布一个 Python 项目到 PyPI 还是非常简单的，遵照上述的步骤，每个人都可以将上面的项目发布到自己账户下。

## 关于 pydoc

Python 内置了 doc 的功能，叫 `pydoc`。执行 `python -m pydoc` 可以看到它有哪些选项和功能。

执行 `python -m pydoc -b` 可以在本地理解启动一个 web 页面来访问你 `...\Python38\Lib\site-packages\` 目录下所有项目的文档。

![以 elasticsearch 文档为例](how-to-release-python-project/pydoc-es.png)

如何让用户可以在线访问你的 doc 呢？

GitHub 有内置的 GitHub Pages 功能，可以很容易的提供一个在线网址。只要打开你的 python 项目设置选项 -> 找到 GitHub Pages -> Source 选择你的分支和路径，保存后就立刻拥有了一个网址。例如：

* https://xxxxx.github.io/demo/ 是你的项目主页，显示是 README.md 信息 
* https://xxxxx.github.io/demo/docs/demo.html 是你的项目的 pydoc 文档

## 关于版本号

另外如果是正式版本，在发布还需要注意版本号的选择。如果是功能很简答，完成度也不高，建议从 0.0.1 版本开始。

如果是一个完成度很高的产品了，那么可以从 1.0.0 版本开始。



