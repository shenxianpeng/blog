---
title: 启用与禁用 Git sparse-checkout
summary: |
  介绍如何启用与禁用 Git sparse-checkout，包括配置只检出指定目录的示例，以及如何恢复到完整检出状态。
tags:
  - Git
date: 2021-01-11
authors:
  - shenxianpeng
---

本文是我在自己环境中测试可行的笔记，并未在更多场景中验证。

---

## 启用 sparse-checkout

有时在 Windows 平台上克隆仓库会遇到某些文件夹问题，可以用 sparse-checkout 作为一种**只检出部分目录**的解决方案。

### 情况 1：尚未克隆仓库时

```bash
mkdir git-src
cd git-src
git init
git config core.sparseCheckout true
echo "/assets/" >> .git/info/sparse-checkout
git remote add origin git@github.com:shenxianpeng/shenxianpeng.git
git fetch
git checkout master
```

### 情况 2：已克隆仓库时

```bash
cd git-src
git config core.sparseCheckout true
echo "/assets/" >> .git/info/sparse-checkout
rm -rf <不需要的文件或目录>
git checkout
```

---

## 禁用 sparse-checkout

如果需要恢复到完整检出状态，可以执行：

```bash
git config core.sparseCheckout false
git read-tree --empty
git reset --hard
```

---

✅ **提示**

* sparse-checkout 适合只需要仓库部分内容的场景，例如减少下载量或规避平台限制。
* Git 2.25+ 提供了 `git sparse-checkout` 子命令，可以更方便地管理此功能。
