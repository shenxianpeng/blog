---
title: Docker Buildx Bake 加速构建和管理多平台镜像的利器
summary: 本文介绍 Docker Buildx Bake 的概念、优势、使用场景以及如何使用该功能来加速构建和管理多平台镜像。
tags:
 - Docker
date: 2023-07-17
aliases:
  - /2023/07/buildx-bake/
authors:
  - shenxianpeng
---

随着容器化技术的普及和应用场景的增多，构建和管理多平台镜像变得越来越重要。[Docker Buildx](https://github.com/docker/buildx) 是 Docker 官方对于 Docker CLI 的一个扩展，为 Docker 用户提供了更强大和灵活的构建功能。包括：

1. 多平台构建：Docker Buildx 允许用户在一个构建命令中为多个不同的平台构建容器镜像。这样，你可以一次性构建适用于多种 CPU 架构的镜像，比如 x86、ARM 等，从而在不同的硬件设备上运行相同的镜像。
2. 构建缓存优化：Docker Buildx 改进了构建过程中的缓存机制，通过自动识别 Dockerfile 中哪些部分是可缓存的，从而减少重复构建和加快构建速度。
3. 并行构建：Buildx 允许并行构建多个镜像，提高了构建的效率。
4. 多种输出格式：Buildx 支持不同的输出格式，包括 Docker 镜像、OCI 镜像、以及 rootfs 等。
5. 构建策略：通过支持多种构建策略，用户可以更好地控制构建过程，例如，可以在多个节点上构建、使用远程构建等。

> 使用 `docker buildx` 需要 Docker Engine 版本不低于 19.03。

其中，Docker Buildx Bake 是 Buildx 的一个子命令，也是本篇文章要重点介绍包括概念、优势、使用场景以及如何使用该功能来加速构建和管理多平台镜像。


## 什么是 Docker Buildx Bake？

Docker Buildx Bake 是 Docker Buildx 的一项功能，它旨在简化和加速镜像构建过程。Bake 是一种声明式的构建定义方式，它允许用户在一个命令中定义多个构建配置和目标平台，实现自动化批量构建和发布跨平台镜像。

## 为什么使用 Docker Buildx Bake？

### 1. 提高构建效率

Bake 通过并行构建和缓存机制来提高构建效率。使用 Bake 可以一次性定义和构建多个镜像，而无需为每个镜像分别执行构建过程，这样可以大大节省构建时间，提高工作效率。

### 2. 支持多个平台和架构

Docker Buildx Bake 的另一个优势是它能够构建多个平台和架构的镜像。通过在 Bake 配置中指定不同的平台参数就可以轻松构建适用于不同操作系统和架构的镜像。这对于跨平台应用程序的开发和部署非常有用。

### 3. 一致的构建环境

通过 docker-bake.hcl （除了 HCL 配置文件之外还可以是 JSON 或是 YAML 文件）文件描述构建过程确保一致的构建环境，使不同的构建配置和目标平台之间具有相同的构建过程和结果。这种一致性有助于减少构建过程中的错误，而且构建配置更易于维护和管理。

## 如何使用 Docker Buildx Bake？

以下是使用 Docker Buildx Bake 进行高效构建的基本步骤，首先确保你已经安装了 Docker Engine 或 Docker Desktop 版本 19.03 以及以上。

然后你的 docker 命令将变成这样 `docker buildx bake`。以下 `docker buildx bake --help` 的帮助输出：

```bash
docker buildx bake --help

Usage:  docker buildx bake [OPTIONS] [TARGET...]

Build from a file

Aliases:
  docker buildx bake, docker buildx f

Options:
      --builder string         Override the configured builder instance
  -f, --file stringArray       Build definition file
      --load                   Shorthand for "--set=*.output=type=docker"
      --metadata-file string   Write build result metadata to the file
      --no-cache               Do not use cache when building the image
      --print                  Print the options without building
      --progress string        Set type of progress output ("auto", "plain", "tty"). Use plain to show container output (default "auto")
      --provenance string      Shorthand for "--set=*.attest=type=provenance"
      --pull                   Always attempt to pull all referenced images
      --push                   Shorthand for "--set=*.output=type=registry"
      --sbom string            Shorthand for "--set=*.attest=type=sbom"
      --set stringArray        Override target value (e.g., "targetpattern.key=value")
```

接下来尝试一下如何使用 `docker buildx bake`

### 1. 创建 Bake 配置文件

比如创建一个名为 `docker-bake.dev.hcl` 的 Bake 配置文件，并在其中定义构建上下文、目标平台和其他构建选项。以下是一个简单的示例：

```bash
# docker-bake.dev.hcl
group "default" {
  targets = ["db", "webapp-dev"]
}

target "db" {
  dockerfile = "Dockerfile.db"
  tags = ["xianpengshen/docker-buildx-bake-demo:db"]
}

target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["xianpengshen/docker-buildx-bake-demo:webapp"]
}

target "webapp-release" {
  inherits = ["webapp-dev"]
  platforms = ["linux/amd64", "linux/arm64"]
}
```

### 2. 运行 Bake 构建

运行以下命令开始使用 Bake 构建镜像：

`$ docker buildx bake -f docker-bake.dev.hcl db webapp-release`

### 3. 打印构建选项

你还可以无需构建打印构建选项，使用用 `--print` 来查看某个目标构建是否符合预期。例如：

```bash
$ docker buildx bake -f docker-bake.dev.hcl --print db
[+] Building 0.0s (0/0)
{
  "group": {
    "default": {
      "targets": [
        "db"
      ]
    }
  },
  "target": {
    "db": {
      "context": ".",
      "dockerfile": "Dockerfile.db",
      "tags": [
        "xianpengshen/docker-buildx-bake-demo:db"
      ]
    }
  }
}
```

### 4. 发布构建镜像

通过添加 `--push` 选项可以将构建完成的镜像一键发布的镜像仓库，例如 `$ docker buildx bake -f docker-bake.dev.hcl --push db webapp-release`

以上示例中的 demo 放在这里了：https://github.com/shenxianpeng/docker-buildx-bake-demo

### 5. Buildx Bake 高级用法

Buildx Bake 还有其他更多的使用技巧，比如 `variable`, `function `, `matrix` 等这里就不一一介绍了，详情请参见官方 [Buildx Bake reference](https://docs.docker.com/build/bake/reference/) 文档。

## 总结

Docker Buildx Bake 是一个功能强大的构建工具，它提供了一种简化和加速构建过程的方法。通过使用 Bake 你可以高效地构建和测试多个镜像，并且可以跨多个平台和架构进行构建。所以说 Bake 是开发人员和构建工程师的重要利器，掌握 Docker Buildx Bake 的使用方法将帮助你更好地应对多镜像构建的带来的挑战、加快应用程序的交付速度。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
