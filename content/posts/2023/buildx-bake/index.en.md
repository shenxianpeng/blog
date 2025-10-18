---
title: Docker Buildx Bake—A Powerful Tool for Accelerating Builds and Managing Multi-platform Images
summary: This article introduces the concept, advantages, use cases, and how to use Docker Buildx Bake to accelerate the building and management of multi-platform images.
tags:
 - Docker
date: 2023-07-17
authors:
  - shenxianpeng
---

With the increasing popularity and application scenarios of containerization technology, building and managing multi-platform images has become increasingly important. [Docker Buildx](https://github.com/docker/buildx) is an extension of the official Docker CLI that provides Docker users with more powerful and flexible build capabilities.  These include:

1. **Multi-platform Builds:** Docker Buildx allows users to build container images for multiple different platforms in a single build command. This allows you to build images for multiple CPU architectures, such as x86, ARM, etc., all at once, so that the same image can run on different hardware devices.
2. **Build Cache Optimization:** Docker Buildx improves the caching mechanism during the build process by automatically identifying which parts of the Dockerfile are cacheable, thus reducing redundant builds and speeding up the build process.
3. **Parallel Builds:** Buildx allows parallel building of multiple images, improving build efficiency.
4. **Multiple Output Formats:** Buildx supports different output formats, including Docker images, OCI images, and rootfs.
5. **Build Strategies:** By supporting multiple build strategies, users can better control the build process, such as building on multiple nodes, using remote builds, etc.

> Using `docker buildx` requires a Docker Engine version of 19.03 or higher.

Docker Buildx Bake is a subcommand of Buildx, and this article will focus on its concept, advantages, usage scenarios, and how to use this feature to accelerate the building and management of multi-platform images.


## What is Docker Buildx Bake?

Docker Buildx Bake is a feature of Docker Buildx designed to simplify and accelerate the image building process. Bake is a declarative build definition method that allows users to define multiple build configurations and target platforms in a single command, enabling automated batch building and publishing of cross-platform images.


## Why Use Docker Buildx Bake?

### 1. Improved Build Efficiency

Bake improves build efficiency through parallel builds and caching mechanisms. Using Bake, you can define and build multiple images at once without having to execute the build process separately for each image, which can significantly reduce build time and improve work efficiency.


### 2. Support for Multiple Platforms and Architectures

Another advantage of Docker Buildx Bake is its ability to build images for multiple platforms and architectures. By specifying different platform parameters in the Bake configuration, you can easily build images suitable for different operating systems and architectures. This is very useful for the development and deployment of cross-platform applications.


### 3. Consistent Build Environment

Using a `docker-bake.hcl` file (in addition to HCL configuration files, JSON or YAML files can also be used) to describe the build process ensures a consistent build environment, so that different build configurations and target platforms have the same build process and results. This consistency helps reduce errors in the build process and makes build configurations easier to maintain and manage.


## How to Use Docker Buildx Bake?

Here are the basic steps for using Docker Buildx Bake for efficient builds. First, ensure you have Docker Engine or Docker Desktop version 19.03 or higher installed.

Then your docker command will become `docker buildx bake`. The following is the help output of `docker buildx bake --help`:

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

Next, let's try how to use `docker buildx bake`.


### 1. Create a Bake Configuration File

For example, create a Bake configuration file named `docker-bake.dev.hcl` and define the build context, target platforms, and other build options in it. Here is a simple example:

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

### 2. Run Bake Build

Run the following command to start building images using Bake:

`$ docker buildx bake -f docker-bake.dev.hcl db webapp-release`

### 3. Print Build Options

You can also print the build options without building, using `--print` to see if a particular target build meets expectations. For example:

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

### 4. Publish Built Images

By adding the `--push` option, you can push the built images to the image repository in one step. For example, `$ docker buildx bake -f docker-bake.dev.hcl --push db webapp-release`

The demo in the above example is located here: https://github.com/shenxianpeng/docker-buildx-bake-demo

### 5. Advanced Buildx Bake Usage

Buildx Bake has many more usage tips, such as `variable`, `function`, `matrix`, etc., which will not be introduced here. For details, please refer to the official [Buildx Bake reference](https://docs.docker.com/build/bake/reference/) documentation.


## Summary

Docker Buildx Bake is a powerful build tool that provides a way to simplify and accelerate the build process.  By using Bake, you can efficiently build and test multiple images and build across multiple platforms and architectures.  Bake is an important tool for developers and build engineers; mastering the use of Docker Buildx Bake will help you better address the challenges of multi-image builds and speed up application delivery.

---

Please indicate the author and source when reprinting this article, and do not use it for any commercial purposes.  Welcome to follow the official account "DevOps攻城狮"