---
title: Setup Gitpod Self-Hosted instance on Ubuntu 18.04 troubleshooting
tags:
  - Gitpod
categories:
  - DevOps
date: 2021-12-17 14:41:19
author: shenxianpeng
---


## Problem 1

Error: Kubernetes cluster unreachable: Get "http://localhost:8080/version?timeout=32s": dial tcp [::1]:8080: connect: connection refused

Resovled by this post: https://github.com/k3s-io/k3s/issues/1126

```bash
kubectl config view --raw >~/.kube/config

export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
```

## Problem 2

Error: Kubernetes cluster unreachable: error loading config file "/etc/rancher/k3s/k3s.yaml": open /etc/rancher/k3s/k3s.yaml: permission denied

Fixed by runing following commands

```bash
chmod 644 /etc/rancher/k3s/k3s.yaml
```

## Problem 3

Error: INSTALLATION FAILED: execution error at (gitpod/templates/_helpers.tpl:296:4): please specify the Gitpod version to use in your values.yaml or with the helm flag --set version=x.x.x

Resovled by changing from `version:` to `version: 0.10.0` in `gitpod/chart/values.yaml`

## Problem 4

Error: INSTALLATION FAILED: execution error at (gitpod/templates/ws-manager-deployment.yaml:38:3): minio access key is required, please add a value to your values.yaml or with the helm flag --set minio.accessKey=xxxxx

Resovled by running `openssl rand -hex 20` to generate keys/secrets.

---

By now, I still have problems with configuration on setup Gitpod self-hosted k8s.
