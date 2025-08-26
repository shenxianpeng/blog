---
title: Understanding Docker, containerd, CRI, CRI-O, OCI, and runc—How They Work Together
summary: This article introduces key components and standards in the container ecosystem, such as Docker, containerd, CRI, CRI-O, OCI, and runc, explaining their relationships and how they work together.
tags:
  - Docker
  - containerd
  - CRI
  - CRI-O
  - runc
author: shenxianpeng
date: 2022-03-29
---

Since Docker ignited the explosive growth in container usage, more and more tools and standards have emerged to help manage and utilize this containerization technology.  Simultaneously, this has led to a proliferation of confusing terminology.

Terms like Docker, containerd, CRI, CRI-O, OCI, and runc might be familiar, but their functions may not be fully understood. This article will clarify these terms and explain how the container ecosystem works together.

## The Container Ecosystem

The container ecosystem is a mix of exciting technologies, abundant jargon, and competition among large corporations.

Fortunately, these companies occasionally collaborate to establish standards that improve interoperability across different platforms and operating systems, reducing reliance on single companies or projects.

This diagram shows how Docker, Kubernetes, CRI, OCI, containerd, and runc interact within this ecosystem.



![container ecosystem](container-ecosystem.png)

The workflow is simple:

1. Tools like Docker and Kubernetes invoke a container runtime (CRI) such as containerd or CRI-O when running a container.
2. The container runtime handles the actual work of creating, running, and destroying containers.
    * Docker uses containerd as its runtime; Kubernetes supports multiple container runtimes, including containerd and CRI-O.
    * These container runtimes adhere to the OCI specification and utilize runc to interact with the operating system kernel, creating and running containers.

Let's examine the terms and specifications in the diagram.

## Docker

Let's start with the familiar Docker, as it's the most popular tool for managing containers.  For many, "Docker" is synonymous with "container."

Docker initiated the container revolution, creating a user-friendly tool for handling containers—also called Docker.  The key points to remember are:

* Docker is not the only container solution.
* Containers are no longer solely tied to the Docker name.

Docker is just one of many container tools; others include: [Podman](https://podman.io/), [LXC](https://linuxcontainers.org/lxd/introduction/), [containerd](https://containerd.io/), and [Buildah](https://buildah.io/).

Therefore, considering containers solely in terms of Docker is an incomplete and inaccurate view.

### Docker Components

Docker simplifies building container images, pulling images from Docker Hub, and creating, starting, and managing containers.  In reality, when you run a container with Docker, it's actually executed via the Docker daemon, containerd, and runc.

![Docker](docker.png)

Docker comprises these projects (among others, but these are the main ones):

* `docker-cli`: A command-line interface (CLI) tool for interacting with Docker via commands like `docker pull`, `build`, `run`, and `exec`.
* `containerd`: A daemon that manages and runs containers. It pushes and pulls images, manages storage and networking, and supervises container operations.
* `runc`: A low-level container runtime (the actual component that creates and runs containers).  It includes `libcontainer`, a Go-based native implementation for creating containers.

### Docker Images

Many refer to "Docker images," but these are actually images packaged in the Open Container Initiative (OCI) format.

Therefore, an image pulled from Docker Hub or another registry can be used with Docker commands, on a Kubernetes cluster, with the `podman` tool, or any other tool supporting the OCI image format specification.

### Dockershim

Kubernetes includes a component called `dockershim` to support Docker. Since Docker predates Kubernetes and didn't implement CRI, `dockershim` bridged the gap, essentially hardcoding Docker support into Kubernetes. As containerization became an industry standard, the Kubernetes project added support for additional runtimes via the Container Runtime Interface (CRI).  `Dockershim` thus became an anomaly in the Kubernetes project. The reliance on Docker and `dockershim` permeated various tools and projects within the Cloud Native Computing Foundation (CNCF) ecosystem, leading to code fragility.

`Dockershim` was completely removed from Kubernetes 1.24 in April 2022.  Kubernetes subsequently discontinued direct Docker support, preferring container runtimes that implement its CRI.  This might involve using containerd or CRI-O.  This doesn't mean Kubernetes can't run Docker-formatted containers.  containerd and CRI-O can both run Docker-formatted (actually OCI-formatted) images; they simply don't require the `docker` command or the Docker daemon.


## Container Runtime Interface (CRI)

The CRI (Container Runtime Interface) is a Kubernetes API for controlling different runtimes that create and manage containers.  It simplifies Kubernetes' ability to use various container runtimes. It's a plugin interface, meaning any container runtime implementing the standard can be used by Kubernetes.

The Kubernetes project doesn't need to manually add support for each runtime. The CRI API describes how Kubernetes interacts with each runtime; the runtime determines how to manage containers as long as it adheres to the CRI API.

![CRI](cri.png)

You can use containerd or CRI-O to run containers, as both implement the CRI specification.


## containerd

containerd is an advanced container runtime originating from Docker and implementing the CRI specification.  After being separated from the Docker project, containerd was donated to the Cloud Native Computing Foundation (CNCF) to provide a foundation for the container community to build new container solutions.

Docker itself uses containerd internally, and containerd is installed when you install Docker.

containerd implements the Kubernetes Container Runtime Interface (CRI) via its CRI plugin. It manages the entire container lifecycle, from image transfer and storage to container execution, monitoring, and networking.


## CRI-O

CRI-O is another high-level container runtime implementing the Container Runtime Interface (CRI) that can use Open Container Initiative (OCI)-compatible runtimes. It's an alternative to containerd.

CRI-O originated from RedHat, IBM, Intel, SUSE, Hyper, and other companies.  It was created from scratch to serve as a container runtime for Kubernetes, providing the ability to start, stop, and restart containers, similar to containerd.


## Open Container Initiative (OCI)

The Open Container Initiative (OCI) is a group of technology companies aiming to create open industry standards for container images and runtimes.  They maintain specifications for the container image format and how containers should run.

The idea behind OCI is that you can choose different runtimes that conform to the specification, each with different underlying implementations.

For example, you could have an OCI-compliant runtime for your Linux host and another for your Windows host. This is the advantage of having a standard that can be implemented by many different projects. This "one standard, multiple implementations" approach is prevalent, from Bluetooth devices to Java APIs.


## runc

runc is a lightweight, universal container runtime that adheres to the OCI specification. It's the lowest-level component implementing the OCI interface, interacting with the kernel to create and run containers.

runc provides all the low-level functionality for containers, interacting with existing low-level Linux features like namespaces and cgroups to create and run container processes.

Several runc alternatives exist:

* [crun](https://github.com/containers/crun), a container runtime written in C (in contrast, runc is written in Go).
* [kata-runtime](https://github.com/kata-containers/kata-containers) from the Katacontainers project, which implements the OCI specification as separate lightweight virtual machines (hardware virtualization).
* Google's [gVisor](https://gvisor.dev/), which creates containers with their own kernel.  It implements OCI in its runtime, called `runsc`.

runc is a tool for running containers on Linux, meaning it can run on Linux, bare metal, or within a virtual machine.

On Windows, it's slightly different. The equivalent of runc is Microsoft's Host Compute Service (HCS), which includes a tool called [runhcs](https://docs.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/containerd), itself a fork of runc that also implements the Open Container Initiative specification.


## Summary

Docker is just a small part of the container ecosystem.  A set of open standards allows for interchangeable implementations.

This is why CRI and OCI standards, and projects like containerd, runc, and CRI-O exist.

Now you understand this fascinating and slightly complex world of containers.  Avoid saying you're using "Docker containers" in future discussions!


## References

> [The differences between Docker, containerd, CRI-O and runc](https://www.tutorialworks.com/difference-docker-containerd-runc-crio-oci/)

---

Please cite the author and source when reprinting this article.  Do not use it for commercial purposes.  Follow the WeChat official account "DevOps攻城狮".