---
title: 你一定要了解这 17 条 Docker 最佳实践！
summary: 本文分享了在编写 Dockerfiles 和使用 Docker 时应遵循的一些最佳实践，包括多阶段构建、镜像优化、安全性等方面的建议。
tags:
  - Dokerfile
  - Docker
date: 2022-01-12
author: shenxianpeng
---

本篇分享在编写 Dockerfiles 和使用 Docker 时应遵循的一些最佳实践。篇幅较长，建议先收藏慢慢看，保证看完会很有收获。

## 文章目录

Dockerfile 最佳实践

1. 使用多阶段的构建
2. 调整 Dockerfile 命令的顺序
3. 使用小型 Docker 基础镜像
4. 尽量减少层的数量
5. 使用无特权的容器
6. 优先选择 `COPY` 而不是 `ADD`
7. 将 `Python` 包缓存到 Docker 主机上
8. 每个容器只运行一个进程
9. 优先选择数组而不是字符串语法
10. 理解 `ENTRYPOINT` 和 `CMD` 之间的区别
11. 添加健康检查 `HEALTHCHECK`

Docker 镜像最佳实践

1. Docker 镜像的版本
2. 不要在镜像中存储密钥
3. 使用 `.dockerignore` 文件
4. 检查和扫描你的 Docker 文件和镜像
5. 签署和验证镜像

## Dockerfile 最佳实践

### 1. 使用多阶段的构建

利用多阶段构建的优势来创建更精简、更安全的Docker镜像。多阶段 Docker 构建([multi-stage builds](https://docs.docker.com/develop/develop-images/multistage-build/))允许你将你的 Dockerfile 分成几个阶段。

例如，你可以有一个阶段用于编译和构建你的应用程序，然后可以复制到后续阶段。由于只有最后一个阶段被用来创建镜像，与构建应用程序相关的依赖关系和工具就会被丢弃，因此可以留下一个精简的、模块化的、可用于生产的镜像。

Web 开发示例：



```Dockerfile
# 临时阶段
FROM python:3.9-slim as builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# 最终阶段
FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*
```

在这个例子中，GCC 编译器在安装某些 Python 包时是必需的，所以我们添加了一个临时的、构建时的阶段来处理构建阶段。

由于最终的运行时映像不包含 GCC，所以它更轻，也更安全。镜像大小比较：

```bash
REPOSITORY                 TAG                    IMAGE ID       CREATED          SIZE
docker-single              latest                 8d6b6a4d7fb6   16 seconds ago   259MB
docker-multi               latest                 813c2fa9b114   3 minutes ago    156MB
```

再来看一个例子：

```Dockerfile
# 临时阶段
FROM python:3.9 as builder

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels jupyter pandas


# 最终阶段
FROM python:3.9-slim

WORKDIR /notebooks

COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*
```

镜像大小比较：

```bash
REPOSITORY                  TAG                   IMAGE ID       CREATED         SIZE
ds-multi                    latest                b4195deac742   2 minutes ago   357MB
ds-single                   latest                7c23c43aeda6   6 minutes ago   969MB
```

总之，多阶段构建可以减少你的生产镜像的大小，帮助你节省时间和金钱。此外，这将简化你的生产容器。由于尺寸较小和简单，相对会有较小的攻击面。

### 2. 调整 Dockerfile 命令的顺序

密切注意你的 Dockerfile 命令的顺序，以利用层缓存。

Docker 在一个特定的 Docker 文件中缓存每个步骤（或层），以加快后续的构建。当一个步骤发生变化时，不仅该步骤，而且所有后续步骤的缓存都将被废止。

例如：

```Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY sample.py .

COPY requirements.txt .

RUN pip install -r /requirements.txt
```

在这个 Dockerfile 中，我们在安装需求之前复制了应用程序的代码。现在，每次我们改变 sample.py 时，构建都会重新安装软件包。这是非常低效的，特别是在使用 Docker 容器作为开发环境时。因此，把经常变化的文件放在 Dockerfile 的末尾是很关键的。

> 你也可以通过使用 .dockerignore 文件来排除不必要的文件，使其不被添加到 Docker 构建环境和最终镜像中，从而帮助防止不必要的缓存失效。更多信息后面会提到。

因此，在上面的 Dockerfile 中，你应该把 `COPY sample.py .` 命令移到底部，如下所示：

```Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r /requirements.txt

COPY sample.py .
```

注意。

1. 总是把可能发生变化的层放在 Dockerfile 中尽可能的低。
2. 将多个 `RUN apt-get update`，`RUN apt-get install` 等命令结合到一起执行。(这也有助于减少镜像的大小，后面会很快就会提到这一点)。
3. 如果你想关闭某个 Docker 构建的缓存，可以添加 `--no-cache=True` 标志。

### 3. 使用小型 Docker 基础镜像

较小的 Docker 镜像更具有模块化和安全性。较小的 Docker 基础镜像在构建、推送和拉动镜像的速度较小，它们也往往更安全，因为它们只包括运行应用程序所需的必要库和系统依赖。

你应该使用哪个 Docker 基础镜像？这个没有一个固定的答案，它这取决于你要做什么。下面是 Python 的各种 Docker 基础镜像的大小比较。

```bash
REPOSITORY   TAG                 IMAGE ID       CREATED      SIZE
python       3.9.6-alpine3.14    f773016f760e   3 days ago   45.1MB
python       3.9.6-slim          907fc13ca8e7   3 days ago   115MB
python       3.9.6-slim-buster   907fc13ca8e7   3 days ago   115MB
python       3.9.6               cba42c28d9b8   3 days ago   886MB
python       3.9.6-buster        cba42c28d9b8   3 days ago   886MB
```

虽然基于 Alpine Linux 的 Alpine flavor 是最小的，但如果你找不到可以与之配合的编译二进制文件，往往会导致构建时间的增加。因此，你最终可能不得不自己构建二进制文件，这可能会增加镜像的大小（取决于所需的系统级依赖）和构建时间（由于必须从源头编译）。

> 关于为什么最好不要使用基于 Alpine 的基础镜像，请参考[适用于 Python 应用程序的最佳 Docker 基础映像](https://pythonspeed.com/articles/base-image-python-docker-images/) 和 [使用 Alpine 可以使 Python Docker 构建速度慢 50 倍](https://pythonspeed.com/articles/alpine-docker-python/) 了解更多关于为什么最好避免使用基于 Alpine 的基础镜像。

归根结底，这都是关于平衡的问题。如果有疑问，从 `*-slim` flavor 开始，特别是在开发模式下，因为你正在构建你的应用程序。你想避免在添加新的 `Python` 包时不得不不断地更新 Dockerfile 以安装必要的系统级依赖。当你为生产强化你的应用程序和 Dockerfile 时，你可能想探索使用 Alpine 来完成多阶段构建的最终镜像。

另外，别忘了定期更新你的基础镜像，以提高安全性和性能。当一个基础镜像的新版本发布时，例如：`3.9.6-slim` --> `3.9.7-slim`，你应该拉出新的镜像并更新你正在运行的容器以获得所有最新的安全补丁。

### 4. 尽量减少层的数量

尽量把 `RUN`、`COPY` 和 `ADD` 命令结合起来使用，因为它们会创建层。每一层都会增加镜像的大小，因为它们是被缓存的。因此，随着层数的增加，镜像大小也会增加。

你可以用 `docker history` 命令来测试一下。

```bash
docker images
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
dockerfile   latest    180f98132d02   51 seconds ago   259MB

docker history 180f98132d02

IMAGE          CREATED              CREATED BY                                      SIZE      COMMENT
180f98132d02   58 seconds ago       COPY . . # buildkit                             6.71kB    buildkit.dockerfile.v0
<missing>      58 seconds ago       RUN /bin/sh -c pip install -r requirements.t…   35.5MB    buildkit.dockerfile.v0
<missing>      About a minute ago   COPY requirements.txt . # buildkit              58B       buildkit.dockerfile.v0
<missing>      About a minute ago   WORKDIR /app
...
```

请注意尺寸。只有 `RUN`、`COPY` 和 `ADD` 命令增加了镜像的尺寸，你可以尽可能地通过合并命令来减少镜像的大小。比如：

```Dockerfile
RUN apt-get update
RUN apt-get install -y gcc
```

可以合并成一个 `RUN` 命令：

```Dockerfile
RUN apt-get update && apt-get install -y gcc
```

因此，创建一个单层而不是两个，这就减少了最终镜像的大小。虽然减少层数是个好主意，但更重要的是，这本身不是一个目标，而是减少镜像大小和构建时间的一个副作用。换句话说呢，与其试图优化每一条命令，你更应该关注前面的三种做法！！！

1. 多阶段构建
2. Dockerfile命令的顺序
3. 以及使用一个小的基础镜像。

#### 注意

1. `RUN`、`COPY` 和 `ADD` 都会创建图层
2. 每个图层都包含与前一个图层的差异
3. 图层会增加最终镜像的大小

#### 提示

1. 合并相关命令
2. 在创建过程中执行 `RUN` 步骤中删除不必要的文件
3. 尽量减少运行 `apt-get upgrade` 的次数，因为它将所有软件包升级到最新版本。
4. 对于多阶段的构建，不要太担心过度优化临时阶段的命令

最后，为了便于阅读，建议将多行参数按字母数字排序。

```Dockerfile
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    matplotlib \
    pillow  \
    && rm -rf /var/lib/apt/lists/*
```

### 5. 使用无特权的容器

默认情况下，Docker 在容器内以 root 身份运行容器进程。然而，这是一个糟糕的做法，因为在容器内以 root 身份运行的进程在 Docker 主机中也是以 root 身份运行。

因此，如果攻击者获得了对容器的访问权，他们就可以获得所有的 root 权限，并可以对 Docker 主机进行一些攻击，例如：

1. 将敏感信息从主机的文件系统复制到容器中
2. 执行远程命令

为了防止这种情况，确保以非 root 用户运行容器进程。

```Dockerfile
RUN addgroup --system app && adduser --system --group app

USER app
```

你可以更进一步，删除 shell 权限，确保没有主目录。

```Dockerfile
RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app

USER app
```

验证

```bash
docker run -i sample id

uid=1001(app) gid=1001(app) groups=1001(app)
```

在这里，容器内的应用程序在一个非 root 用户下运行。然而，请记住，Docker 守护进程和容器本身仍然是以 root 权限运行的。

请务必查看以非根用户身份运行 Docker 守护进程，以获得以非根用户身份运行守护进程和容器的帮助。

### 6. 优先选择 `COPY` 而不是 `ADD`

除非你确定你需要 `ADD` 所带来的额外功能，否则请使用 `COPY`。

那么 `COPY` 和 `ADD` 的区别是什么？

首先，这两个命令都允许你从一个特定的位置复制文件到 Docker 镜像中。

```dockerfile
ADD <src> <dest>
COPY <src> <dest>
```

虽然它们看起来作用相同，但 `ADD` 有一些额外的功能。

* `COPY` 用于将本地文件或目录从 Docker 主机复制到镜像上。
* `ADD` 可以用于同样的事情，也可以用于下载外部文件。另外，如果你使用压缩文件（tar、gzip、bzip2等）作为 <src> 参数，`ADD` 会自动将内容解压到指定位置。

```dockerfile
# 将主机上的本地文件复制到目的地
COPY /source/path  /destination/path
ADD /source/path  /destination/path

# 下载外部文件并复制到目的地
ADD http://external.file/url  /destination/path

# 复制和提取本地压缩文件
ADD source.file.tar.gz /destination/path
```

最后 `COPY` 在语义上比 `ADD` 更加明确和更容易理解。

### 7. 缓存安装包到 Docker 主机上

当一个需求文件被改变时，镜像需要被重建以安装新的包。先前的步骤将被缓存，正如在最小化层数中提到的。在重建镜像时下载所有的包会导致大量的网络活动，并需要大量的时间。每次重建都要占用同等的时间来下载不同构建中的通用包。

以 Python 为例，你可以通过将 pip 缓存目录映射到主机上的一个目录来避免这种情况。所以对于每次重建，缓存的版本会持续存在，这可以提高构建速度。

在 Docker 运行中添加一个卷，作为 `-v $HOME/.cache/pip-docker/:/root/.cache/pip` 或者作为 Docker Compose 文件中的映射。

上面介绍的目录只供参考，要确保你映射的是 cache 目录，而不是 site-packages（内置包所在的位置）。

将缓存从 docker 镜像中移到主机上可以为你节省最终镜像的空间。

```dockerfile

# 忽略 ...

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
        pip install -r requirements.txt

# 忽略 ...

```

### 8. 每个容器只运行一个进程

为什么建议每个容器只运行一个进程？

让我们假设你的应用程序栈由两个 Web 服务器和一个数据库组成。虽然你可以很容易地从一个容器中运行所有三个，但你应该在一个单独的容器中运行每个服务，以便更容易重复使用和扩展每个单独的服务。

* 扩展性 - 由于每个服务都在一个单独的容器中，你可以根据需要水平地扩展你的一个网络服务器来处理更多的流量。
* 可重用性 - 也许你有另一个服务需要一个容器化的数据库，你可以简单地重复使用同一个数据库容器，而不需要带着两个不必要的服务。
* 日志 - 耦合容器会让日志变得更加复杂。（我们将在本文后面进一步详细讨论这个问题）
* 可移植性和可预测性 - 当容器有较少的部分在工作时，制作安全补丁或调试问题就会容易得多。

### 9. 优先选择数组而不是字符串语法

你可以在你的 Dockerfiles 中以数组（exec）或字符串（shell）格式

在 Dockerfile 中，你可以以数组（exec）或字符串（shell）格式来使用 `CMD` 和 `ENTRYPOINT` 命令

```dockerfile
# 数组（exec）
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app"]

# 字符串（shell）
CMD "gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app"
```

两者都是正确的，并且实现了几乎相同的事情；但是，你应该尽可能地使用 exec 格式。

以下来自 [Docker的官方文档](https://docs.docker.com/compose/faq/#why-do-my-services-take-10-seconds-to-recreate-or-stop)内容：

* 确保你在 Dockerfile 中使用 `CMD` 和 `ENTRYPOINT` 的 exec 形式。
* 例如，使用 `["program", "arg1", "arg2"]` 而不是 `"program arg1 arg2"`。使用字符串形式会导致 Docker 使用 `bash` 运行你的进程，而 `bash` 并不能正确处理信号。Compose 总是使用 JSON 形式，所以不用担心如果你在你的 Compose 文件中覆盖了命令或入口。

因此，由于大多数 shell 不处理对子进程的信号，如果你使用 shell 格式，CTRL-C（产生 `SIGTERM`）可能不会停止一个子进程。

例子:

```dockerfile
FROM ubuntu:18.04

# BAD: 字符串（shell）格式
ENTRYPOINT top -d

# GOOD: 数组（exec）格式
ENTRYPOINT ["top", "-d"]
```

这两种情况执行效果一样。但请注意，在字符串（shell）格式的情况下，`CTRL-C` 不会杀死这个进程。相反，你会看到 `^C^C^C^C^C^C^C^C^C^C`。

另一个注意事项是，字符串（shell）格式携带的是 shell 的 PID，而不是进程本身。

```dockerfile
# 数组格式
root@18d8fd3fd4d2:/app# ps ax
  PID TTY      STAT   TIME COMMAND
    1 ?        Ss     0:00 python manage.py runserver 0.0.0.0:8000
    7 ?        Sl     0:02 /usr/local/bin/python manage.py runserver 0.0.0.0:8000
   25 pts/0    Ss     0:00 bash
  356 pts/0    R+     0:00 ps ax


# 字符串格式
root@ede24a5ef536:/app# ps ax
  PID TTY      STAT   TIME COMMAND
    1 ?        Ss     0:00 /bin/sh -c python manage.py runserver 0.0.0.0:8000
    8 ?        S      0:00 python manage.py runserver 0.0.0.0:8000
    9 ?        Sl     0:01 /usr/local/bin/python manage.py runserver 0.0.0.0:8000
   13 pts/0    Ss     0:00 bash
  342 pts/0    R+     0:00 ps ax
```

#### 10. 了解 `ENTRYPOINT` 和 `CMD` 之间的区别

我应该使用 `ENTRYPOINT` 还是 `CMD` 来运行容器进程？有两种方法可以在容器中运行命令。

```dockerfile
CMD ["gunicorn", "config.wsgi", "-b", "0.0.0.0:8000"]

# 和

ENTRYPOINT ["gunicorn", "config.wsgi", "-b", "0.0.0.0:8000"]
```

两者本质上做的是同一件事：用 `Gunicorn` 服务器在 `config.wsgi` 启动应用程序，并将其绑定到 `0.0.0.0:8000`。

`CMD` 很容易被重写。如果你运行 `docker run <image_name> uvicorn config.asgi`，上述 `CMD` 就会被新的参数所取代。

例如，`uvicorn config.asgi`。而要覆盖 `ENTRYPOINT` 命令，必须指定 `--entrypoint` 选项。

```bash
docker run --entrypoint uvicorn config.asgi <image_name>
```

在这里，很明显，我们正在覆盖入口点。所以，建议使用 `ENTRYPOINT` 而不是 `CMD`，以防止意外地覆盖命令。

它们也可以一起使用。比如说

```dockerfile
ENTRYPOINT ["gunicorn", "config.wsgi", "-w"]
CMD ["4"]
```

当像这样一起使用时，为启动容器所运行的命令就变成了：

```bash
gunicorn config.wsgi -w 4
```

如上所述，`CMD` 很容易被重写。因此，`CMD` 可以被用来向 `ENTRYPOINT` 命令传递参数。比如很容易更改 workers 的数量，就像这样：

```bash
docker run <image_name> 6
```

这样就将有 6 个 Gunicorn workers 启动容器，而不是默认的 4 个。

### 11. 添加健康检查 `HEALTHCHECK`

使用 `HEALTHCHECK` 来确定容器中运行的进程是否不仅已启动并正在运行，而且是“健康”的。

Docker 公开了一个 API 来检查容器中运行的进程的状态，它提供的信息不仅仅是进程是否“正在运行”，因为“运行”涵盖了“它正在运行”、“仍在启动”、甚至“陷入某种无限循环错误状态”。你可以通过 [`HEALTHCHECK`](https://docs.docker.com/engine/reference/builder/#healthcheck) 指令与此 API 交互。

例如，如果你正在提供 Web 应用程序，则可以使用以下内容来确定 `/` 端点是否已启动并可以处理服务请求：

```dockerfile
HEALTHCHECK CMD curl --fail http://localhost:8000 || exit 1
```

如果你运行 `docker ps`，你可以看到 `HEALTHCHECK` 的状态。

健康的示例

```bash
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS                            PORTS                                       NAMES
09c2eb4970d4   healthcheck   "python manage.py ru…"   10 seconds ago   Up 8 seconds (health: starting)   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   xenodochial_clarke
```

不健康的示例

```bash
CONTAINER ID   IMAGE         COMMAND                  CREATED              STATUS                          PORTS                                       NAMES
09c2eb4970d4   healthcheck   "python manage.py ru…"   About a minute ago   Up About a minute (unhealthy)   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   xenodochial_clarke
```

你可以更进一步，设置一个仅用于健康检查的自定义端点，然后配置 `HEALTHCHECK` 以针对返回的数据进行测试。

例如，如果端点返回 `{"ping": "pong"}` 的 JSON 响应，你可以指示 `HEALTHCHECK` 验证响应正文。

以下是使用 `docker inspect` 查看运行状况检查状态的方法：

> 这里省略了部分输出。

```bash
❯ docker inspect --format "{{json .State.Health }}" ab94f2ac7889
{
  "Status": "healthy",
  "FailingStreak": 0,
  "Log": [
    {
      "Start": "2021-09-28T15:22:57.5764644Z",
      "End": "2021-09-28T15:22:57.7825527Z",
      "ExitCode": 0,
      "Output": "..."
```

你还可以向 Docker Compose 文件添加运行状况检查：

```yml
version: "3.8"

services:
  web:
    build: .
    ports:
      - '8000:8000'
    healthcheck:
      test: curl --fail http://localhost:8000 || exit 1
      interval: 10s
      timeout: 10s
      start_period: 10s
      retries: 3
```

选项：

* `test`：要测试的命令。
* `interval`：要测试的间隔 - 即，测试每 x 时间单位。
* `timeout`：等待响应的最长时间。
* `start_period`：何时开始健康检查。它可以在容器准备就绪之前执行其他任务时使用，例如运行迁移。
* `retries`：在将测试指定为失败之前的最大重试次数。

如果你使用的是 Docker Swarm 以外的编排工具（比如 Kubernetes 或 AWS ECS），它们很可能有自己的内部系统来处理健康检查。在添加 `HEALTHCHECK` 指令之前，请参阅特定工具的文档。

## Docker 镜像最佳实践

### 1. Docker 镜像版本

只要有可能，就要避免使用 `latest` 标签的镜像。

如果你依赖 `latest` 标签（这并不是一个真正的 "标签"，因为当镜像没有明确的标签时，它是默认应用的），你无法根据镜像标签来判断你的代码正在运行哪个版本。

如果你想回滚就变得很困难，并且很容易被覆盖（无论是意外还是恶意的）。标签，就像你的基础设施和部署，应该是不可改变的。

所以无论你如何对待你的内部镜像，都不应该对基本镜像使用 `latest` 标签，因为你可能会无意中把一个带有破坏性变化的新版本部署到生产中。

对于内部镜像，应使用描述性的标签，以便更容易分辨哪个版本的代码正在运行，处理回滚，并避免命名冲突。例如，你可以使用以下描述符来组成一个标签。

1. 时间戳
2. Docker 镜像 ID
3. Git 提交哈希值
4. 语义版本 (Semantic version)

关于更多的选择，也可以参考 Stack Overflow [问题](https://stackoverflow.com/a/56213290/1799408) "Properly Versioning Docker Images" 中的这个答案。

比如说

```bash
docker build -t web-prod-b25a262-1.0.0 .
```

在这里，我们用下面的内容来形成标签

1. 项目名称：web
2. 环境名称: prod
3. Git commit short hash: b25a262 (通过命令 `git rev-parse --short HEAD` 来获得)
4. 语义学版本：1.0.0

选择一个标签方案并与之保持一致是至关重要的。由于提交哈希值（commit hashes）可以很容易地将镜像标签与代码联系起来，建议将它们纳入你的标签方案。

### 2. 不要在镜像中存储机密信息

Secrets 是敏感的信息，如密码、数据库凭证、SSH密钥、令牌和 TLS 证书等。这些信息不应该在没有加密的情况下被放入你的镜像中，因为未经授权的用户如果获得了镜像的访问权，只需要检查这些层就可以提取密钥。

因此不要在 Docker 文件中添加明文的密钥，尤其是当你把镜像推送到像 Docker Hub 这样的公共仓库！！

```dockerfile
FROM python:3.9-slim

ENV DATABASE_PASSWORD "SuperSecretSauce"
```

相反，它们应该通过以下方式注入

1. 环境变量（在运行时)
2. 构建时参数（在构建时)
3. 协调工具，如 Docker Swarm（通过 Docker secrets）或 Kubernetes（通过 Kubernetes secrets）。

此外，你还可以通过在你的 `.dockerignore` 文件中添加常见的密钥文件和文件夹来帮助防止密钥的泄露。

```bash
**/.env
**/.aws
**/.ssh
```

最后，要明确哪些文件会被复制到镜像中，而不是递归地复制所有文件。

```dockerfile
# 不好的做法
COPY . .

# 好的做法
COPY ./app.py .
```

明确的做法也有助于限制缓存的破坏。

#### 环境变量

你可以通过环境变量来传递密钥，但它们会在所有子进程、链接的容器和日志以及 `docker inspect` 中可见。要更新它们也很困难。

```bash
docker run --detach --env "DATABASE_PASSWORD=SuperSecretSauce" python：3.9-slim

b25a262f870eb0fdbf03c666e7fcf18f9664314b79ad58bc7618ea3445e39239

docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' b25a262f870eb0fdbf03c666e7fcf18f9664314b79ad58bc7618ea3445e39239

DATABASE_PASSWORD=SuperSecretSauce
PATH=/usr/local/bin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
LANG=C.UTF-8
GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568
python_version=3.9.7
python_pip_version=21.2.4
python_setuptools_version=57.5.0
python_get_pip_url=https://github.com/pypa/get-pip/raw/c20b0cfd643cd4a19246ccf204e2997af70f6b21/public/get-pip.py
PYTHON_GET_PIP_SHA256=fa6f3fb93cce234cd4e8dd2beb54a51ab9c247653b52855a48dd44e6b21ff28b
```

这是最直接的密钥管理方法。虽然它不是最安全的，但它会让诚实的人保持诚实，因为它提供了一个薄薄的保护层，有助于使密钥不被好奇的游荡的眼睛发现。

使用共享卷传递密钥是一个更好的解决方案，但它们应该被加密，通过 Vault 或 AWS密钥管理服务（KMS），因为它们被保存到磁盘。

#### 构建时参数

你可以在构建时使用构建时参数来传递密钥，但这些密钥对于那些可以通过 docker 历史访问镜像的人来说是可见的。

例子

```dockerfile
FROM python:3.9-slim


ARG DATABASE_PASSWORD
```

构建

```bash
docker build --build-arg "DATABASE_PASSWORD=SuperSecretSauce" .
```

如果你只需要临时使用密钥作为构建的一部分。例如，用于克隆私有 repo 或下载私有软件包的 SSH 密钥。你应该使用多阶段构建，因为构建者的历史会被临时阶段忽略。

```dockerfile
# 临时阶段
FROM python:3.9-slim as builder

# 密钥参数
arg ssh_private_key

# 安装 git
RUN apt-get update && （运行 apt-get update）。
    apt-get install -y --no-install-recommends git

# 使用 ssh 密钥来克隆 repo
RUN mkdir -p /root/.ssh/ && \\
    echo "${PRIVATE_SSH_KEY}" > /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts & &
    ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts
RUN git clone git@github.com:testdrivenio/not-real.git


# 最后阶段
FROM python:3.9-slim

工作目录 /app

# 从临时镜像中复制版本库
COPY --from=builder /your-repo /app/your-repo

```

多阶段构建只保留了最终镜像的历史。你可以把这个功能用于你的应用程序需要的永久密钥，比如数据库凭证。

你也可以使用 docker build 中新的 `--secret` 选项来向 Docker 镜像传递密钥，这些密钥不会被存储在镜像中。

```dockerfile
# "docker_is_awesome" > secrets.txt

FROM alpine

# 从默认的密钥位置显示密钥。
RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret
```

这将装载 `secrets.txt` 文件中的密钥。

构建镜像

```bash
docker build --no-cache --progress=plain --secret id=mysecret,src=secrets.txt .

# 输出
...
#4 [1/2] FROM docker.io/library/alpine
#4 sha256:665ba8b2cdc0cb0200e2a42a6b3c0f8f684089f4cd1b81494fbb9805879120f7
#4 缓存的

#5 [2/2] RUN --mount=type=secret,id=mysecret cat /run/secrets/myecret
#5 sha256:75601a522ebe80ada66dedd9dd86772ca932d30d7e1b11bba94c04aa55c237de
#5 0.635 docker_is_awesome#5 DONE 0.7s

#6 导出到镜像
```

最后，检查历史记录，看看密钥是否泄露了。

```bash
❯ docker history 49574a19241c
IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
49574a19241c   5 minutes ago   CMD ["/bin/sh"]                                 0B        buildkit.dockerfile.v0
<missing>      5 minutes ago   RUN /bin/sh -c cat /run/secrets/mysecret # b…   0B        buildkit.dockerfile.v0
<missing>      4 weeks ago     /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
<missing>      4 weeks ago     /bin/sh -c #(nop) ADD file:aad4290d27580cc1a…   5.6MB
```

#### Docker 密钥

如果你正在使用 Docker Swarm，你可以用 Docker secrets 来管理密钥。

例如，启动 Docker Swarm 模式。

```bash
docker swarm init
```

创建一个 docker 密钥。

```bash
echo "supersecretpassword" | docker secret create postgres_password -
qdqmbpizeef0lfhyttxqfbty0

docker secret ls
ID                          NAME                DRIVER    CREATED         UPDATED
qdqmbpizeef0lfhyttxqfbty0   postgres_password             4 seconds ago   4 seconds ago
```

当一个容器被赋予上述密钥的访问权时，它将挂载在 `/run/secrets/postgres_password`。这个文件将包含明文的密钥的实际值。

使用其他的编排工具？

* [使用 AWS Secrets Manager 的密钥与 Kubernetes 的密钥](https://docs.aws.amazon.com/eks/latest/userguide/manage-secrets.html)
* DigitalOcean Kubernetes - [保护 DigitalOcean Kubernetes 集群的推荐步骤](https://www.digitalocean.com/community/tutorials/recommended-steps-to-secure-a-digitalocean-kubernetes-cluster)
* Google Kubernetes引擎 - [与其他产品一起使用密钥管理器](https://cloud.google.com/secret-manager/docs/using-other-products#google-kubernetes-engine)
* Nomad - [Vault 集成和检索动态密钥](https://learn.hashicorp.com/tutorials/nomad/vault-postgres?in=nomad/integrate-vault)

### 3. 使用 .dockerignore 文件

之前已经提到过几次使用 `.dockerignore` 文件。这个文件用来指定你不希望被添加到发送给 Docker 守护进程的初始构建上下文中的文件和文件夹，后者将构建你的镜像。换句话说，你可以用它来定义你需要的构建环境。

当一个 Docker 镜像被构建时，整个 Docker 上下文 - 即你的项目的根在 `COPY` 或 `ADD` 命令执行之前就被发送给了 Docker 守护进程。

这可能是相当费资源，尤其是当你的项目中有许多依赖关系、大量的数据文件或构建工件时。

另外，当 Docker CLI 和守护程序不在同一台机器上。比如守护进程是在远程机器上执行的，你就更应该注意构建环境的大小了。

你应该在 `.dockerignore` 文件中添加什么？

1. 临时文件和文件夹
2. 构建日志
3. 本地 secrets
4. 本地开发文件，如 `docker-compose.yml`
5. 版本控制文件夹，如 ".git"、".hg" 和 ".vscode" 等

例子：

```bash
**/.git
**/.gitignore
**/.vscode
**/coverage
**/.env
**/.aws
**/.ssh
Dockerfile
README.md
docker-compose.yml
**/.DS_Store
**/venv
**/env
```

总之，结构合理的 .dockerignore 可以帮助

1. 减少 Docker 镜像的大小
2. 加快构建过程
3. 防止不必要的缓存失效
4. 防止泄密

### 4. 检查并扫描你的 Dockerfile 和镜像

Linting 是检查源代码中是否存在可能导致潜在缺陷的编程和风格错误以及不良做法的过程。就像编程语言一样，静态文件也可以被 lint。特别是对于你的 Dockerfile，linter 可以帮助确保它们的可维护性、避免弃用语法并遵守最佳实践。整理镜像应该是 CI 管道的标准部分。

[Hadolint](https://github.com/hadolint/hadolint) 是最流行的 Dockerfile linter：

```bash
hadolint Dockerfile

Dockerfile:1 DL3006 warning: Always tag the version of an image explicitly
Dockerfile:7 DL3042 warning: Avoid the use of cache directory with pip. Use `pip install --no-cache-dir <package>`
Dockerfile:9 DL3059 info: Multiple consecutive `RUN` instructions. Consider consolidation.
Dockerfile:17 DL3025 warning: Use arguments JSON notation for CMD and ENTRYPOINT arguments
```

这是 Hadolint 一个在线的链接 https://hadolint.github.io/hadolint/ 也可以安装 VS Code [插件](https://marketplace.visualstudio.com/items?itemName=exiasr.hadolint)

你可以将 Dockerfile 与扫描镜像和容器的漏洞结合使用。

以下是一些有影响力的镜像扫描工具：

* [Snyk](https://docs.docker.com/engine/scan/) 是 Docker 本地漏洞扫描的独家提供商。你可以使用 `docker scan` CLI 命令来扫描镜像。
* [Trivy](https://aquasecurity.github.io/trivy/) 可用于扫描容器镜像、文件系统、git 存储库和其他配置文件。
* [Clair](https://github.com/quay/clair) 是一个开源项目，用于对应用程序容器中的漏洞进行静态分析。
* [Anchore](https://github.com/anchore/anchore-engine) 是一个开源项目，为容器镜像的检查、分析和认证提供集中式服务。

总而言之，对你的 Dockerfile 和镜像进行 lint 和扫描，来发现任何偏离最佳实践的潜在问题。

### 5. 签名和验证镜像

你怎么知道用于运行生产代码的镜像没有被篡改？

篡改可以通过中间人（MITM）攻击或注册表被完全破坏来实现。Docker 内容信任（DCT）可以对来自远程注册中心的 Docker 镜像进行签名和验证。

为了验证镜像的完整性和真实性，请设置以下环境变量。

```bash
DOCKER_CONTENT_TRUST=1
```

现在，如果你试图拉一个没有被签名的镜像，你会收到以下错误。

```bash
Error: remote trust data does not exist for docker.io/namespace/unsigned-image:
notary.docker.io does not have trust data for docker.io/namespace/unsigned-image
```

你可以从使用 Docker 内容信任签署镜像文档中了解签署镜像的情况。

当从 Docker Hub下 载镜像时，确保使用官方镜像或来自可信来源的经过验证的镜像。较大的团队应该使用他们自己的内部私有容器仓库

### 6. 设置内存和 CPU 的限制

限制 Docker 容器的内存使用是一个好主意，特别是当你在一台机器上运行多个容器时。这可以防止任何一个容器使用所有可用的内存，从而削弱其他容器的功能。

限制内存使用的最简单方法是在 Docker cli 中使用 `--memory` 和 `--cpu` 选项。

```bash
docker run --cpus=2 -m 512m nginx
```

上述命令将容器的使用限制在 2 个 CPU 和 512 兆的内存。

你可以在 Docker Compose 文件中做同样的事情，像这样。

```yml
version: "3.9"
services:
  redis:
    image: redis:alpine
    deploy:
      resources:
        limits:
          cpus: 2
          memory: 512M
        reservations:
          cpus: 1
          memory: 256M
```

请注意 `reservations` 字段。它是用来设置软限制的，当主机的内存或CPU资源不足时，它就会优先考虑。

其他相关资源

1. 带有内存、CPU和GPU的运行时选项：https://docs.docker.com/config/containers/resource_constraints/
2. Docker Compose 的资源限制：https://docs.docker.com/compose/compose-file/compose-file-v3/#resources

## 总结

以上就是本文介绍的 17 条最佳实践，掌握这些最佳实践一定会让你的 Dockerfile 和 Docker Image 变得精简，干净，和安全。

本文出自 [Docker Best Practices for Python Developers](https://testdriven.io/blog/docker-best-practices/)。

---

欢迎扫码关注公众号「DevOps攻城狮」- 专注于DevOps领域知识分享。

![ ](https://github.com/shenxianpeng/shenxianpeng.github.io/blob/master/about/index/qrcode.jpg?raw=true)
