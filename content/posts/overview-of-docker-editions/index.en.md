---
title: Docker Version Overview
summary: |
  Overview of different Docker versions, including Community Edition, Enterprise Edition, and Enterprise solutions, suitable for users of different scales and needs.
tags:
  - Docker
date: 2019-12-01
author: shenxianpeng
---

## Docker can be divided into three versions

* Docker Engine - Community
* Docker Engine - Enterprise

* Docker Enterprise

Docker Engine - Community is ideal for individual developers and small teams who want to get started with Docker and try container-based applications.

Docker Engine - Enterprise is designed for enterprise development of container runtimes, taking into account security and enterprise-grade SLAs.

Docker Enterprise is designed for enterprise development and IT teams who build, deliver, and run mission-critical applications at scale.

| Capability  | Docker Engine - Community | Docker Engine - Enterprise  | Docker Enterprise|
|---|---|---|---|
| Container engine and built-in orchestration, networking, security | √ | √ | √ |
| [Certified infrastructure, plugins, and ISV containers](https://docs.docker.com/ee/supported-platforms/#docker-enterprise) | |  √ | √ |
| [Image Management](https://docs.docker.com/ee/dtr/) | | | √ |
| [Container Application Management](https://docs.docker.com/ee/ucp/) | | | √ |
| [Image Security Scanning](https://docs.docker.com/ee/dtr/user/manage-images/scan-images-for-vulnerabilities/) | | | √ |

## Installing Docker Community Edition

* CentOS installation example: https://docs.docker.com/install/linux/docker-ce/centos/

## Installing Other Docker Versions

* Refer to the Docker official website: https://docs.docker.com/install/overview/