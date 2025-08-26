---
title: Docker—containerd—CRI—CRI-O—OCI—runc Explained and How They Work Together
summary: This article introduces the key components and standards in the container ecosystem, such as Docker, containerd, CRI, CRI-O, OCI, and runc, explaining their relationships and how they work together.
tags:
  - Docker
  - containerd
  - CRI
  - CRI-O
  - runc
author: shenxianpeng
date: 2022-03-29
---

Since Docker ignited the explosive growth of container usage, more and more tools and standards have emerged to help manage and utilize this containerization technology.  Simultaneously, this has led to a plethora of confusing terminology.

For example, Docker, containerd, CRI, CRI-O, OCI, and runc. This article will introduce these terms you've heard of but may not understand, and explain how the container ecosystem works together.

## The Container Ecosystem

The container ecosystem is composed of many exciting technologies, a large amount of specialized terminology, and large companies vying for dominance.

Fortunately, these companies occasionally find common ground, cooperating to agree on standards that improve the ecosystem's interoperability across different platforms and operating systems, reducing reliance on any single company or project.

This diagram shows how Docker, Kubernetes, CRI, OCI, containerd, and runc fit together in this ecosystem.



![container ecosystem](container-ecosystem.png)

The workflow is simple:

1. Tools like Docker and Kubernetes call a container runtime (CRI) such as containerd or CRI-O when running a container.
2. The container runtime handles the actual work of creating, running, and destroying containers.
    * Docker uses containerd as its runtime; Kubernetes supports multiple container runtimes, including containerd and CRI-O.
    * These container runtimes adhere to the OCI specification and use runc to interact with the operating system kernel to create and run containers.


Let's introduce the terms and specifications mentioned in the diagram.

## Docker

Let's start with the familiar Docker, as it's the most popular tool for managing containers. For many, the name "Docker" is synonymous with "container."

Docker initiated the container revolution, creating a user-friendly tool for handling containers, also called Docker. The key points to understand here are:

* Docker is not the only container contender.
* Containers are no longer inextricably linked to the name Docker.

In the current landscape of container tools, Docker is just one among many. Other notable container tools include: [Podman](https://podman.io/), [LXC](https://linuxcontainers.org/lxd/introduction/), [containerd](https://containerd.io/), and [Buildah](https://buildah.io/).

Therefore, believing containers are solely about Docker is inaccurate and incomplete.

### Docker Components

Docker simplifies building container images, pulling images from Docker Hub, and creating, starting, and managing containers.  In reality, when you run a container with Docker, it's actually run through the Docker daemon, containerd, and runc.

![Docker](docker.png)

To achieve this, Docker comprises these projects (among others, but these are the major ones):

* **docker-cli:** A command-line interface (CLI) for interacting with commands like `docker pull`, `build`, `run`, and `exec`.
* **containerd:** A daemon that manages and runs containers. It pushes and pulls images, manages storage and networking, and supervises container operation.
* **runc:** A low-level container runtime (the actual component that creates and runs containers). It includes libcontainer, a Go-based native implementation for creating containers.

### Docker Images

Many refer to Docker images, which are actually images packaged in the Open Container Initiative (OCI) format.

Therefore, if you pull an image from Docker Hub or another registry, you should be able to use it with Docker commands, on a Kubernetes cluster, with the Podman tool, or with any other tool supporting the OCI image format specification.

### Dockershim

Kubernetes included a component called `dockershim` to support Docker.  Because Docker predates Kubernetes and didn't implement CRI, `dockershim` was necessary to integrate Docker into Kubernetes. As containerization became an industry standard, the Kubernetes project added support for additional runtimes, supporting container execution via the Container Runtime Interface (CRI). Thus, `dockershim` became an anomaly in the Kubernetes project. The dependence on Docker and `dockershim` permeated various tools and projects within the Cloud Native Computing Foundation (CNCF) ecosystem, resulting in fragile code.

In April 2022, `dockershim` was completely removed from Kubernetes 1.24.  Kubernetes discontinued direct Docker support, opting to utilize only container runtimes implementing its Container Runtime Interface. This likely means using containerd or CRI-O. This doesn't imply Kubernetes cannot run Docker-formatted containers.  containerd and CRI-O can both run Docker-formatted (actually OCI-formatted) images; they simply don't require the `docker` commands or the Docker daemon.

## Container Runtime Interface (CRI)

The CRI (Container Runtime Interface) is a Kubernetes API for controlling different runtimes used to create and manage containers. It makes Kubernetes more adaptable to various container runtimes. It's a plugin interface, meaning any compliant container runtime can be used by Kubernetes.

The Kubernetes project doesn't need to manually add support for each runtime. The CRI API describes how Kubernetes interacts with each runtime; the runtime determines how to actually manage containers, provided it adheres to the CRI API.

![CRI](cri.png)

You can use containerd or CRI-O to run your containers because both runtimes implement the CRI specification.

## containerd

containerd is a high-level container runtime from Docker that implements the CRI specification.  It was separated from the Docker project and later donated to the Cloud Native Computing Foundation (CNCF) to provide the container community with a foundation for creating new container solutions.

Docker itself internally uses containerd; it's installed when you install Docker.

containerd implements the Kubernetes Container Runtime Interface (CRI) via its CRI plugin. It manages the entire container lifecycle, from image transfer and storage to container execution, monitoring, and networking.


## CRI-O

CRI-O is another high-level container runtime that implements the Container Runtime Interface (CRI) and can use OCI (Open Container Initiative)-compliant runtimes. It's an alternative to containerd.

CRI-O originated from RedHat, IBM, Intel, SUSE, Hyper, and others.  It was created from scratch as a container runtime for Kubernetes, providing the ability to start, stop, and restart containers, similar to containerd.

## Open Container Initiative (OCI)

The Open Container Initiative (OCI) is a group of technology companies aiming to create open industry standards around container images and runtimes. They maintain specifications for the container image format and how containers should run.

The idea behind OCI is that you can choose different runtimes that comply with the specification, each with different underlying implementations.

For instance, you might have an OCI-compliant runtime for your Linux hosts and another for your Windows hosts. This is the advantage of having a standard that can be implemented by many different projects. This "one standard, multiple implementations" approach is widely used, from Bluetooth devices to Java APIs.

## runc

runc is a lightweight, universal runtime for containers. It adheres to the OCI specification and is the lowest-level component implementing the OCI interface; it interacts with the kernel to create and run containers.

runc provides all low-level functionality for containers, interacting with existing low-level Linux features like namespaces and cgroups, using these to create and run container processes.

Several alternatives to runc exist:

* [crun](https://github.com/containers/crun): A container runtime written in C (in contrast, runc is written in Go).
* [kata-runtime](https://github.com/kata-containers/kata-containers) from the Katacontainers project, which implements the OCI specification as separate lightweight virtual machines (hardware virtualization).
* Google's [gVisor](https://gvisor.dev/), which creates containers with their own kernel. It implements OCI in its runtime, called `runsc`.

runc is a tool for running containers on Linux, meaning it can run on Linux, bare metal, or within a virtual machine.

On Windows, it's slightly different.  The equivalent of runc is Microsoft's Host Compute Service (HCS), which includes a tool called [runhcs](https://docs.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/containerd), itself a fork of runc, also implementing the Open Container Initiative specification.


## Summary

This article demonstrates that Docker is just a small part of the container ecosystem.  A set of open standards allows for interchangeable implementations.

This is why standards like CRI and OCI exist, along with projects like containerd, runc, and CRI-O.

Now you understand the intriguing and slightly complex world of containers.  Next time, avoid saying you're using "Docker containers"! :)

## References

> [The differences between Docker, containerd, CRI-O and runc](https://www.tutorialworks.com/difference-docker-containerd-runc-crio-oci/)

---

Please indicate the author and source when reprinting this article.  Do not use for any commercial purposes.  Follow the official account "DevOps攻城狮".