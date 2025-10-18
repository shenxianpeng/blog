---
title: 用于 DevOps 的 Nix 和 NixOS
summary: 本文介绍了 Nix 和 NixOS 在 DevOps 中的应用，包括可重复性、声明式配置和可靠性，并通过实际示例展示其在开发和部署中的优势。
tags:
  - Nix
  - NixOS
draft: true
translate: false
date: 2024-11-26
author: shenxianpeng
---

当 CI 或更糟的是生产发生灾难性故障时，“在我的计算机上工作”一直是毫无帮助的答案。除其他外，Nix 是一种通过提供可重复、声明性和可靠的系统来解决此问题的方法。这使得它成为通常称为 DevOps 的两个方面的绝佳工具：操作系统的开发和流程。这篇文章将通过一个实际示例展示这两个方面，但首先，让我们从鸟瞰的角度看看这些承诺到底意味着什么。



## 可重复

Nix 的灵感来自一种函数式编程语言，它将软件包和配置本身的构建过程建模为“纯”函数。相同的输入应该始终产生相同的输出。虽然这听起来相当抽象，但在实践中，这意味着如果它在你的笔记本电脑上运行，它将在生产服务器、CI 或你的同事的机器上运行完全相同。Nix 严格禁止你使用未声明的依赖项，所有内容都由加密哈希固定，并且软件包的评估和构建彼此独立。

## 声明式

虽然简单的脚本或其他更复杂的工具（如 Ansible）会告诉你的机器“该做什么”才能达到某种状态，但在编写 Nix 代码时，你将“定义某物是什么”。对于任何做过函数式编程的人来说，这不是一个新概念。但是，虽然差异很小，但影响却很大。声明式配置是上面讨论的可重复性和部署过程的幂等性的重要组成部分。Nix 不仅允许共享配置和构建说明，还允许共享项目本身的开发和构建环境。只需几行代码，你就可以添加一个开发环境，其中包含团队中每个开发人员在项目上工作所需的所有工具、编程语言和固定版本。

## 可靠的

安装软件包时绝不会破坏其他软件包。同一软件的不同版本之间的升级也是如此。Nix 不仅提供原子升级，还确保一个软件包永远不会破坏其他软件包。你甚至可以（并且通常会）在同一系统上愉快地共存同一软件包的多个版本或配置。甚至更好的是，你可以根据需要回滚或在所谓的代之间切换。在升级过程中，永远不会出现不一致的状态，想象一下在旧版本旁边安装和配置新版本的软件包，并在一切准备就绪后切换到新版本。

## 好的，它是如何工作的？

首先，为了避免混淆，先介绍一些术语。Nix 指两件事：

* 声明式包管理器
* 用于定义包和配置的编程语言

另一方面，NixOS 是一个围绕 Nix 包管理器构建的 Linux 发行版，它使用其功能来定义整个系统配置。

Nix 打破了众所周知的 Linux 文件系统层次结构。如果你曾经使用过它，你会偶然发现下面有一个相当大的目录/nix/store，里面有很多神秘的路径。这就是所谓的 Nix 存储，Nix 将所有软件包存储在其自己独特的子目录中，例如：

```bash
/nix/store/b6gvzjyb2pg0kjfwrjmg1vfhh54ad73z-firefox-33.1/
```

将所有内容放入一个大目录中可能听起来违反直觉，但这实际上是实现 Nix 大部分魔力的概念。每个存储路径都具有相同的结构：

```bash
/nix/store/<hash>-<name>-<version>
```

其中哈希是根据包的所有依赖项计算得出的唯一标识符（准确地说：包的构建依赖关系图的加密哈希）。


**但为什么？**

这种非常简单的结构允许很多理想的特性。首先，相同的路径将具有完全相同的内容。这是我们确保可重复性的第一步。它还确保文件不会在你不知情的情况下被篡改，因为哈希会以数学方式验证内容。

现在，你可以同时拥有同一软件包的多个版本。它们将具有不同的哈希值，因此位于存储中的不同路径中。不再存在软件包之间的依赖版本冲突（即“DLL-hell”），每个软件包都可以引用和使用自己所需的版本。

一个重要的结果是，升级或卸载应用程序等操作不会破坏其他应用程序，因为这些操作永远不会“破坏性地”更新或删除其他软件包使用的文件。这使我们能够实现所谓的原子升级和回滚。

`/usr/lib` 像在传统 Linux 系统上一样摆脱全局位置可确保不存在未在包中指定的隐藏依赖项。如果它在一个系统上构建，它将在另一个系统上构建，无论安装了什么其他软件。

实际上，软件包是根据 Nix（语言）表达式构建的。从这里开始，Nix 计算出派生。这最好被描述为“构建操作”，即构建特定软件包所需的所有依赖项、工具、环境变量、源和步骤的完整规范。派生与编程语言无关，并且具有确定性。

通过哈希严格标识系统的每个包和部分还可以实现强大的缓存。当指示构建

```bash
/nix/store/b6gvzjyb2pg0...-firefox-33.1
```

从源头开始，Nix 会首先检查它是否已存在于商店或任何已配置的缓存中，如果已存在，则从那里提取。实际上，从源头构建只是常用软件包的后备方法

## Flakes

Flakes 是 Nix 的一个新功能，最好被描述为“将 Nix 表达式打包成可组合实体的机制”。实际上，flake 是一个文件系统树（通常从 Git 存储库或 tarball 中获取），其中包含根目录中名为 flake.nix 的文件。

它们是一种标准化接口，用于拆分和分发 Nix 代码，并使重用和组合变得容易。我们将在以下部分中使用此格式，并flake.nix逐步构建你的文件，并在过程中进一步解释。

## 一个实际的例子

说完这些，让我们看看 Nix 在实践中是如何使用的。以下示例将演示使用 Nix 在任何可能的地方构建（DevOps 中的“Dev”）和部署（DevOps 中的“Ops”）示例 Go 应用程序的 DevOps 流程。

### 开发（Dev）

对于“开发”部分，我们首先介绍一下我们的示例应用程序。一个用 Go 编写的非常简单的 Web 服务器。假设我们使用 Go 模块，即运行 `go mod init` 并为我们的应用程序 `go mod tidy` 创建一个 `go.mod` 和 `go.sum` 文件。`package main`

```go
import (
  "fmt"
  "net/http"
)

func hello(w http.ResponseWriter, req *http.Request) {
  fmt.Fprintf(w, "Hello World!\n")
}

func main() {
  http.HandleFunc("/", hello)
  http.ListenAndServe(":8080", nil)
}
```

最简单的形式是，flake 是定义属性的outputs和 （可选）inputs和 的属性集description。输入是 flake 中使用的源或依赖项，在大多数情况下是 git 存储库或要从中获取的纯 URL。输出通常是要在其他 flakes 中使用的包、部署说明、配置或 Nix 代码（函数）。虽然输出属性集可以采用你想要的任何形式，但常见输出有标准化名称。

为了“nixify”我们的项目，让我们首先在flake.nix 存储库的根目录中添加一个名为的文件，其中包含一个非常基本的薄片：


```nix

{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixpkgs";
  };

  outputs = { self, nixpkgs }: { };
}

{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixpkgs";
  };

  outputs = { self, nixpkgs }: { };
}
```

我们的 flake 定义github.com/nixpkgs为输入，目前没有输出。虽然它目前还不是很有用，但它是有用的。我们可以用它nix flake metadata 来显示一些关于它的信息。

```bash
❯ nix flake metadata
Resolved URL: git+file:///home/pinpox/code/example_app
Locked URL: git+file:///home/pinpox/code/example_app
Description: A very basic flake
Path: /nix/store/c4vxaphd27qjl253m5lmqrb3isg9rc5h-source
Last modified: 2022-05-30 12:09:33
Inputs:
└───nixpkgs: github:nixpkgs/0907dc851fa2e56db75ae260a8ecc9880dc7b49
```

如果尚不存在，这还将 `flake.lock ` 为我们创建一个文件，将我们所有的输入固定到特定版本，并通过输入的哈希值进行验证。


## 添加包

完成基本样板后，我们可以添加第一个输出：应用程序的包。

```nix
packages.x86_64-linux = {
  default = pkgs.buildGoModule {
    pname = "example_app";
    version = "1.0.0";
    src = ./.;
    vendorSha256 = "sha256-aCFVUq58hpK7O9DoYJ/7Sr4ICSUzz/JHNrse40um1n4=";
  };
};
```

上面指定了如何在具有系统架构的 Linux 系统上构建我们的应用程序x64_64。我们可以使用通用mkDerivation函数来定义我们的包（派生），但 Nix 包含大多数常见编程语言和框架的辅助函数。这里buildGoModule用于定义我们的 Golang 项目的包，指定源为当前目录./.、名称、版本以及我们文件中指定的依赖项的哈希值go.mod，因为所有版本都必须用哈希值固定。

我们现在可以使用来构建我们的应用程序。这将构建我们的应用程序并在 nix 存储中nix build创建指向它的符号链接。result


```bash
❯ ls -l
lrwxrwxrwx 61 pinpox 7 Jun 16:17 result -> /nix/store/0yasl97rl4drf9rgmbaqbcbii0rsizsi-example_app-1.0.0
.rwxr-xr-x 6,2M pinpox 7 Jun 16:06 example_app
.rw-r--r-- 534 pinpox 7 Jun 15:44 flake.lock
.rw-r--r-- 571 pinpox 7 Jun 16:08 flake.nix
.rw-r--r-- 80 pinpox 7 Jun 15:20 go.mod
.rw-r--r-- 189 pinpox 7 Jun 15:20 go.sum
.rw-r--r-- 415 pinpox 7 Jun 15:22 main.go
```

好吧，但我们本可以省去麻烦，直接go build买同样的东西，对吧？嗯，不完全是。

Nix 和 flakes 承诺为我们提供密封评估，这意味着构建应用程序所需的一切都固定在特定版本并使用校验和进行验证。这包括应用程序本身的代码，也包括使用的编译器、任何其他依赖项、工具和软件包以及系统架构本身。这不仅确保我们的应用程序不会因外部因素而中断，而且还可以在任何机器上构建。无论是同事的笔记本、CI 还是生产，都不再有“（仅）在我的计算机上工作”的情况。由于 Nix 与语言无关且不特定于 Go，因此我们还拥有一个用于以任何语言构建软件的通用接口。构建和运行（nix run）nixified go 应用程序的过程保持不变。

需要明确指出的是，在使用 Nix 构建或运行应用程序之前，系统上不需要安装任何先决条件，例如 go 编译器或任何其他工具（Nix 本身除外）。Nix 将创建 flake 指定的完整环境。第一次运行时将获取输入，然后从那里开始使用哈希进行检查，以确保确定性构建，同时尽可能多地缓存。

## 添加 shell（临时环境）

虽然包定义已经允许我们构建和运行我们的应用程序，但它并不真正适合开发。通过在输出中添加 Nix shell，我们可以创建一个开发环境，其中包含所有开发人员都可以使用的特定版本的所有工具。我们不必让每个开发人员浪费时间为新项目设置技术堆栈，而是可以传递一个 shell，其中包含在其指定版本中可用的所有工具。

由于我们项目的要求都已打包在 nixpkgs 中，因此我们可以在输出中添加一个简单的 shell，其中包含以下几行：

```nix
devShell.x86_64-linux = pkgs.mkShell {
  buildInputs = with pkgs; [
    go
    gopls
    gotools
    go-tools
  ];

  shellHook = ''
    GOPATH=$HOME/go
  '';
};
```

现在，`nix flake show` 将向我们展示两个输出：我们之前指定的包和新添加的shell。

```bash
❯ nix flake show
git+file:///home/pinpox/code/example_app
├───devShell
│ └───x86_64-linux: development environment 'nix-shell'
└───packages
└───x86_64-linux
└───default: package 'example_app-1.0.0'
```

我们可以通过运行进入 shell nix develop，然后会进入一个
包含我们需要的所有工具的 shell。

```bash
❯ nix develop
[pinpox@ahorn:~/code/example_app]$ go version
go version go1.17.10 linux/amd64
```

在此示例中，我们仅使用了 中预先打包的工具和依赖项nixpkgs。当然，也可以指定 之外的工具nixpkgs或覆盖特定版本的软件包。这可以通过添加你自己的软件包定义或使用overrides和覆盖) 来动态修改现有软件包来实现。在我们的 shell 中指定的工具buildInputs当然也固定到某个版本，因为我们的nixpkgs输入在 flake.lock 文件中固定到特定的 git 提交。

## 行动 (Ops)
到目前为止，我们只使用了 Nix，即包管理器，正如开头所述，它是一个单独的工具。对于操作部分，让我们以 Linux 发行版 NixOS 为例，它采用了 Nix 原则并将其应用于完整的系统配置。核心思想很简单，只是我们已经看到的 Nix 的自然延伸：就像我们的包存储在商店中的隔离路径中一样，我们也将其应用于配置。例如，SSH 服务器的配置可以用 Nix 语言定义，并在评估后/nix/store/5rnfzla9kcx4mj5zdc7nlnv8na1najvg-firefox-3.5.4/存储在路径中。/nix/store/s2sjbl85xnrc18rl4fhn56irkxqxyk4p-sshd_config

这使得整个操作系统利用了我们在软件包中看到的优势：它是独立的，可以回滚，并且不会在没有通知的情况下发生变化，因为所有内容都再次通过哈希进行验证。

该nixos-rebuild工具用于执行这些操作。要切换到新配置：

```bash
nixos-rebuild switch
```

每次构建配置后，你都会获得所谓的代数。这是你可以切换或回滚到的点。同样，如果出现问题或无法按预期工作

```bash
nixos-rebuild switch --rollback
```

将带你回到上一代。在启动时，你可以选择任何已保存的一代。

为了澄清这一点，NixOS 完全围绕 Nix 包管理器构建。它用于以纯函数式语言构建内核、应用程序、系统包和配置文件。这可以实现原子系统升级和回滚整个系统等功能。此外，该系统完全可复制，这使得重新安装或复制变得容易。另一个例子：

```bash
$ nixos-rebuild build-vm
$ ./result/bin/run-*-vm
```

将在虚拟机内构建你的系统配置并启动它。虚拟机将具有与你的主机系统本身相同的配置，允许你根据需要进行测试、实验和“预览”，而不会冒破坏主机的风险。

## 配置

系统配置通常在名为 `configuration.nix`

一个非常简单的例子如下

```nix
{
    boot.loader.grub.device = "/dev/sda";
    fileSystems."/".device = "/dev/sda1";
    services.sshd.enable = true;
}
```

这个最小配置足以构建一个运行 SSH 守护进程的机器。使用 flake 时，我们还将flake.nix在输出下将配置添加到我们的 flake中nixosConfiguration 。

```nix
{
  outputs = { self, nixpkgs }: {
    # replace 'my-hostname' with your hostname here.
    nixosConfigurations.my-hostname = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [ ./configuration.nix ];
    };
  };
}
```

然后将薄片传递给nixos-rebuild命令

```bash
nixos-rebuild switch --flake '/path/to/flake#my-hostname'
```

## 模块

你可以在系统配置中设置的所有选项都来自模块，这些模块是包含 NixOS 表达式的文件。该configuration.nix文件也是一个模块。大多数其他模块位于nixpkgs 存储库中。模块是随后由 NixOS 组合以生成完整系统配置的文件。

完整解释模块系统超出了本文的范围，因此我们重点介绍上述应用程序的一个实际示例。我们将向你的flake.nix文件添加一个模块，以便任何人都可以导入它，从而生成应用程序的运行实例。

该模块只有一个名为“enable”的选项，设置为 true 时会将下面的部分添加config=到系统配置中。这是保存在 中的完整模块module.nix：

```nix
{ lib, pkgs, config, ... }:
with lib;
let
  cfg = config.services.hello;
in
{
  options.services.hello = {
    enable = mkEnableOption "hello service";
  };

  config = mkIf cfg.enable {
    systemd.services.hello = {
      wantedBy = [ "multi-user.target" ];
      serviceConfig.ExecStart = "${pkgs.hello}/bin/hello -g'Hello, ${escapeShellArg cfg.greeter}!'";
    };
  };
}
```

要导入它，只需nixosConfigurations按照添加文件的方式将其添加到输出中 configuration.nix：

```nix
modules = [ ./configuration.nix ./module.nix ];
```

该模块创建一个运行我们应用程序的 systemd 单元。通常，你还会在此处添加反向代理的配置，以及环境变量、其他依赖应用程序和设置、用户、组以及我们的应用程序运行时应存在的其他属性。

## 部署

假设我们有一个正在运行的 NixOS 主机，并且具有 SSH 访问权限，我们可以部署你的配置

```bash
nixos-rebuild build --flake '.#my-hostname' --target-host root@our.host.tld
```

瞧，我们的应用程序正在运行！

## 关于 Docker 的说明

在介绍 nix 时，一个反复出现的问题是：“那么 docker 呢？”虽然 Nix 和 Docker 本质上是用于不同事物的工具，但毫无疑问人们会滥用两者来解决重叠的问题。


## Docker 缺少可重复性

对于可重现的环境，Docker镜像可用于存档类似内容。请注意，这里特指构建镜像，因为 Dockerfile 或容器定义不可重现。这可以通过多次构建镜像并比较其校验和来轻松确认

```bash
docker save $(docker build --no-cache -q .) -o img1.tar
docker save $(docker build --no-cache -q .) -o img2.tar

sha256sum img1.tar
b830edb19a8653ef6ef5846a115b7ab90fdd8ce828a072c3698b21f13429e8c7 img1.tar

sha256sum img2.tar
c07301820e59aefad9b36feeca4c0da911e88b56b56a083fdea8d1763bd0c5f3 img2.tar
```

这可以归因于多种因素，例如 Dockerfile 命令

这个表达式中的“latest”是什么意思？

```Dockerfile
FROM ubuntu:latest
```

运行此代码时将安装哪个版本的 Python？

```Dockerfile
RUN apt-get update && apt-get install python -y
```

在可能的多个条目中哪一个$PATH将会运行？

```Dockerfile
CMD [ "somebin" ]
```

对于其中一些问题，有一些解决方法，但是 Docker（或者更具体地说是 Dockerfile）首先不是为可重现而构建的，并且今天有许多现实世界的映像构建示例，但几个月后就不会了。

## Nix + Docker

但问题并不一定非此即彼。事实上，Nix 和 Docker 一起使用，可以完美地互补。

## Nix 构建 Docker 镜像

Nix 可用于构建 docker 镜像。Nix 提供了多个实用函数，例如pkgs.dockerTools.buildImage和，pkgs.dockerTools.buildLayeredImage它们可用于将 docker 镜像构建为 flake 输出，就像任何其他包一样。Matthew Croughan 最近在 MCH2022 上发表了关于其使用的简短演讲。

它还可以用于对 Docker 层缓存进行更细粒度的优化，正如Graham Christensen 所详述的那样。

## NixOS 部署容器

NixOS 提供了一种非常优雅的运行容器的方式。这是配置 NixOS 以运行容器的示例

```nix
virtualisation.oci-containers.containers = {
  bitwardenrs = {
    autoStart = true;
    image = "bitwardenrs/server:latest";
    environment = {
      ADMIN_TOKEN = "myAdminTokenString";
      DOMAIN = "https://pw.mydomain.com";
      INVITATIONS_ALLOWED = "true";
      SIGNUPS_ALLOWED = "true";
    };
    ports = [
      "80:80"
    ];
    volumes = [
      "/var/docker/bitwarden/:/data/"
    ];
  };
};
```

它将设置运行容器所需的一切，并生成匹配的 systemd 单元来启动、停止和管理容器。全部由哈希固定。

将 Nix 和 NixOS 与容器运行时结合使用是一个过于广泛的主题，无法在此完全涵盖，并且上述示例只能触及可能性的表面。

## 进一步阅读

这只是 Nix 和 NixOS 的冰山一角。上面和下面有多层抽象，还有简化使用和配置的工具。部署工具用于管理大量主机，如nixOps或lollypops，机密管理，如sops-nix或agenix ，以及 CI 系统，如Hydra 。Nix 与容器配合得很好，其生态系统不断发展和演变，仅上个月就有 534 人合并了 2,981 个 Pull 请求。

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
