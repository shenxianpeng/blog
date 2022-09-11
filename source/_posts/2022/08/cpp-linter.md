---
title: C/C++ 代码格式化和静态分析检查的一站式的解决方案
tags:
  - Clang-Format
  - Clang-Tidy
  - Clang
categories:
  - DevOps
author: shenxianpeng
date: 2022-08-23 17:27:31
---

目前 C/C++ 语言的代码格式化和检查工具使用的最为广泛的是使用 [LLVM](https://llvm.org/) 项目中的 [Clang-Format](https://clang.llvm.org/docs/ClangFormat.html) 和 [Clang-Tidy](https://clang.llvm.org/extra/clang-tidy/)。

> LLVM 项目是模块化和可重用的编译器和工具链技术的集合。

对于 C/C++ 代码格式化和静态分析检查用到是 LLVM 项目中 clang-format 和 clang-tidy，放在一起我们称它为 clang-tools。

虽然我们有了工具，但**如何把工具更好的集成到我们的工作流中**才是本篇重点要讨论的。

[cpp-linter](https://github.com/cpp-linter) 组织的诞生就是为 C/C++ 代码格式化和静态分析检查提供一站式的工作流，主要包括：

1. 方便的下载 clang-tools，提供了下载 Docker images 和 binaries；
2. 方便的与 CI 工作流进行集成，包括 cpp-linter-action 和 cpp-linter-hooks。

下面分别介绍如何使用 clang-tools 下载工具，以及集成到工作流中。

## 下载 clang-tools Docker images

如果你想通过 Docker 来使用 clang-format 和 clang-tidy，[clang-tools](https://github.com/cpp-linter/clang-tools) 项目是来提供 Docker 镜像。

例如：下载 clang-tools 镜像，使用 clang-format 来进行代码格式化

```bash
# 检查 clang-format 版本
$ docker run xianpengshen/clang-tools:12 clang-format --version
Ubuntu clang-format version 12.0.0-3ubuntu1~20.04.4

# 格式化代码 (helloworld.c 在仓库的 demo 目录下)
$ docker run -v $PWD:/src xianpengshen/clang-tools:12 clang-format --dry-run -i helloworld.c
```

使用 clang-tidy 来进行代码格诊断

```bash
# 查看 clang-tidy 版本
$ docker run xianpengshen/clang-tools:12 clang-tidy --version
LLVM (http://llvm.org/):
  LLVM version 12.0.0

  Optimized build.
  Default target: x86_64-pc-linux-gnu
  Host CPU: cascadelake
# 诊断代码 (helloworld.c 在仓库的 demo 目录下)
$ docker run -v $PWD:/src xianpengshen/clang-tools:12 clang-tidy helloworld.c \
-checks=boost-*,bugprone-*,performance-*,readability-*,portability-*,modernize-*,clang-analyzer-cplusplus-*,clang-analyzer-*,cppcoreguidelines-*
```

## 下载 clang-tools binaries

当如如果你需要下载 clang-tools binaries，以 Windows 为例，通常下载这指定版本 clang-tools 你需要先安装 LLVM 这个大的安装包才能获得 clang-format & clang-tidy 这些工具；在 Linux 上会方便很多可以使用命令来下载，但如果想下载指定版本的 clang-format & clang-tidy 也不是那么容易获得。

[clang-tools-pip](https://github.com/cpp-linter/clang-tools-pip) 项目提供了支持在 Windows，Linux，MacOs 上面通过命令行下载任何指定版本的 clang-tools 可执行文件。

只需要通过 `pip` 安装 `clang-tools`，即 `pip install clang-tools`，然后通过 `clang-tools` 命令就可以安装任何版本的可执行文件了。

例如，安装 clang-tools 版本 13：

`$ clang-tools --install 13`

也可以将它安装到指定目录下面：

`$ clang-tools --install 13 --directory .`

安装成功后，可以查看安装版本：

```bash
$ clang-format-13 --version
clang-format version 13.0.0

$ clang-tidy-13 --version
LLVM (http://llvm.org/):
  LLVM version 13.0.0
  Optimized build.
  Default target: x86_64-unknown-linux-gnu
  Host CPU: skylake
```

更多关于 `clang-tools` CLI 提供的选项可以查看它的 CLI [文档](https://cpp-linter.github.io/clang-tools-pip/cli_args.html)。

## 把 clang-tools 集成到工作流

虽然上面提供了很方便的下载 clang-tools 的 Docker images 和 binaries，但如何把它们集成到工作流中才是我们最终所关心的。

通常在使用 clang-format 和 clang-tidy 可以在 IDE 中安装插件，然后利用 IDE 进行代码的格式化和静态检查。但这样的问题是：

1. 当有多个开发人员时，他们可能会使用不同的 IDE，这样在不同的 IDE 上安装插件需要比较高的学习成本。
2. 另外没法保证所有开发人员在提交代码的时候运行了 Clang-Format 或 Clang-Tidy。

那么怎样确保每次提交代码都执行了 Clang-Format 或 Clang-Tidy 呢？

1. [cpp-linter-action](https://github.com/cpp-linter/cpp-linter-action) 提供了通过 CI 在代码合并前做自动检查，如果 CI 没有通过则无法进行 Merge，这样倒逼开发提交代码之前运行 Clang-Format 和 Clang-Tidy。
2. [cpp-linter-hooks](https://github.com/cpp-linter/cpp-linter-hooks) 通过 git hook 在开发提交代码的时候自动运行 Clang-Format 和 Clang-Tidy，如果不符合规范则提示并自动格式化；符合规范则提交成功。

## cpp-linter-action 在代码合并前做自动检查

如果你的代码是放在 GitHub 上，那么非常推荐你使用 [cpp-linter-action](https://github.com/cpp-linter/cpp-linter-action) 这个 GitHub Action。

> 目前 [cpp-linter](https://github.com/cpp-linter/cpp-linter) 还没有与除 GitHub 以外其他 SCM 做深度集成，例如 Bitbucket 和 GitLab，可以使用后面介绍的 [cpp-linter-hooks](https://github.com/cpp-linter/cpp-linter-hooks)

以下是它的一些重要特性：

1. 运行结果支持 Annotations 和 Thread Comment 两种方式展示
2. 支持 GitHub 的 public 和 private 仓库
3. 支持绝大多数 Clang 版本，从最新版本 `v14` 到最旧版本 `v3`
4. 还有很多其他的 [optional-inputs](https://github.com/cpp-linter/cpp-linter-action#optional-inputs)

那么如何来使用这个 Action，只需要在 `.github/workflows/` 下面创建一个 cpp-linter.yml，内容如下：

```yaml
name: cpp-linter

on:
  pull_request:
    types: [opened, reopened]
  push:

jobs:
  cpp-linter:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: cpp-linter/cpp-linter-action@v1
        id: linter
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          style: file

      - name: Fail fast?!
        if: steps.linter.outputs.checks-failed > 0
        run: |
          echo "Some files failed the linting checks!"
          exit 1
```

如果发现没有进行格式化的代码或是静态检查问题，这个 workflow 就会失败，并且默认会有如下注释说明，默认是开启的。

![annotations](cpp-linter/annotations.png)

如果开启了 Thread Comment 选项（即 `thread-comments: true`）就会将在 Pull Request 中自动添加下面的错误评论。

![comment](cpp-linter/comment.png)

目前该项目已经受到了很多知名项目所使用，在 GitHub Marketplace 上面搜索它的排名也非常靠前，开发者也在积极维护可以放心使用。

如果你使用的不是 GitHub 作为代码管理工具，比如 Bitbucket，GitLab 等，可以直接使用该项目的 core package [cpp-linter](https://github.com/cpp-linter/cpp-linter)

注意 annotations 和 comment 这两个功能目前只支持 GitHub，该项目未来考虑支持其他 SCM，像 Bitbucket，GitLab。

## cpp-linter-hooks 在提交代码时自动检查

[cpp-linter-hooks](https://github.com/cpp-linter/cpp-linter-hooks) 是通过 git hook 在提交代码时做自动检查，这种方式不限制使用任何 SCM。

只需要在项目仓库中添加一个 `.pre-commit-config.yaml` 配置文件，然后将 [cpp-linter-hooks](https://github.com/cpp-linter/cpp-linter-hooks) 这个 hook 添加进去，具体设置如下：

> `.pre-commit-config.yaml` 是 [`pre-commit`](https://pre-commit.com/) framework 的默认配置文件。

1. 安装 `pre-commit` 。

    ```python
    pip install pre-commit
    ```

2. 添加 `pre-commit` 的配置文件，更多配置可以参考 [README](https://github.com/cpp-linter/cpp-linter-hooks)

    ```yaml
    repos:
    - repo: https://github.com/cpp-linter/cpp-linter-hooks
      rev: v0.2.1
      hooks:
        - id: clang-format
          args: [--style=file]  # to load .clang-format
        - id: clang-tidy
          args: [--checks=.clang-tidy] # path/to/.clang-tidy
    ```

    > 这里的 file 是指 `.clang-format`, clang-format 默认支持的编码格式包括 LLVM, GNU, Google, Chromium, Microsoft, Mozilla, WebKit，如果需要特殊设置可以在仓库的根目录下面创建配置文件 `.clang-format`。同理，如果默认的静态分析设置不满足要求，可以在仓库的根目录下创建 `.clang-tidy` 配置文件。

3. 安装 git hook 脚本

    ```bash
    $ pre-commit install
    pre-commit installed at .git/hooks/pre-commit
    ```

4. 之后每次提交代码都会自动执行 clang-format 和 chang-tidy。

    如果检查到没有格式化或有静态分析错误，会提示如下错误信息：

    chang-format 的输出

    ```bash
    clang-format.............................................................Failed
    - hook id: clang-format
    - files were modified by this hook
    ```

    并自动帮你进行格式化

    ```diff
    --- a/testing/main.c
    +++ b/testing/main.c
    @@ -1,3 +1,6 @@
    #include <stdio.h>
    -int main() {for (;;) break; printf("Hello world!\n");return 0;}
    -
    +int main() {
    +  for (;;) break;
    +  printf("Hello world!\n");
    +  return 0;
    +}
    ```

    chang-tidy 的输出

    ```bash
    clang-tidy...............................................................Failed
    - hook id: clang-tidy
    - exit code: 1

    418 warnings and 1 error generated.
    Error while processing /home/ubuntu/cpp-linter-hooks/testing/main.c.
    Suppressed 417 warnings (417 in non-user code).
    Use -header-filter=.* to display errors from all non-system headers. Use -system-headers to display errors from system headers as well.
    Found compiler error(s).
    /home/ubuntu/cpp-linter-hooks/testing/main.c:3:11: warning: statement should be inside braces [readability-braces-around-statements]
      for (;;) break;
              ^
              {
    /usr/include/stdio.h:33:10: error: 'stddef.h' file not found [clang-diagnostic-error]
    #include <stddef.h>
            ^~~~~~~~~~
    ```

## 选择 CI 还是 git hook

如果你的团队已经在使用 [`pre-commit`](https://pre-commit.com/)，那么推荐使用 git hook，只需要添加 [cpp-linter-hooks](https://github.com/cpp-linter/cpp-linter-hooks) 即可。如果不希望引入 `pre-commit` 则可以通过添加 CI 来进行检查。

当然也可以两个都选。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
