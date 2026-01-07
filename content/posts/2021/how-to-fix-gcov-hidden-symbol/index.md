---
title: 修复 "hidden symbol `__gcov_init' in ../libgcov.a(_gcov.o) is referenced by DSO" 错误
summary: |
  本文介绍在使用 Gcov 编译项目进行代码覆盖率统计时，出现 "hidden symbol `__gcov_init'..." 等错误的原因及解决方法，包括如何在构建时确保符号不被隐藏。
tags:
  - Gcov
  - Coverage
  - DevOps
date: 2021-07-27
aliases:
  - /2021/07/how-to-fix-gcov-hidden-symbol/
authors:
  - shenxianpeng
---

## 问题描述

在项目中引入 Gcov 做代码覆盖率构建时，可能遇到以下报错：

### 错误 1
```bash
hidden symbol `__gcov_init' in /usr/lib/gcc/x86_64-redhat-linux/4.8.5/libgcov.a(_gcov.o) is referenced by DSO
```

### 错误 2

```bash
undefined reference to `__gcov_init'
undefined reference to `__gcov_merge_add'
```

---

## 问题定位

以 **错误 1** 为例，从报错中可看到涉及多个 `.so` 动态库，例如：

```bash
-lundata -lutcallc_nfasvr
```

使用 `nm` 命令查看库文件符号，发现 `__gcov_init` 被标记为 **U**（未定义符号）：

```bash
find -name *utcallc_nfasvr*
nm ./bin/libutcallc_nfasvr.so | grep __gcov_init
# 输出：
#                  U __gcov_init
```

---

## 解决方法

在我的项目中，只需在 Makefile 中为对应的库添加 `-lgcov` 链接选项即可：

```makefile
LIB_1 := utcallc_nfasvr
LIB_1_LIBS := -lgcov
```

重新构建后，查看符号时标记变为 **t**（符号已定义）：

```bash
nm ./bin/libutcallc_nfasvr.so | grep __gcov_init
# 输出：
#                  t __gcov_init
```

对于直接构建 `.so` 库的情况，也可以在编译命令中直接添加 `-lgcov`：

```bash
g++ -shared -o libMyLib.so src_a.o src_b.o src_c.o -lgcov
```

---

## 总结

我遇到过以下多种形式的报错：

```bash
undefined reference to `__gcov_init`
undefined reference to `__gcov_merge_add`
hidden symbol `__gcov_init' in libgcov.a(_gcov.o) is referenced by DSO
```

**通用修复方式**：在链接阶段添加 `-lgcov` 选项，然后重新编译，并用 `nm` 检查符号是否已正确引入。

---

转载本文请注明作者与出处，禁止用于商业用途。欢迎关注公众号「DevOps攻城狮」。
