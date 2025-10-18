---
title: 从 XLC 10.1 升级到 IBM Open XL C/C++ for AIX 17.1.0 的问题与解决方案
summary: 本文记录了从 IBM XLC 10.1 升级到 XLC 17.1（IBM Open XL C/C++ for AIX 17.1.0）过程中遇到的问题及解决方法，共涵盖 12 个错误的修复方案。
tags:
  - AIX
  - Clang
  - XLC
date: 2023-10-08
authors:
  - shenxianpeng
---

本文记录了从 **IBM XLC 10.1** 升级到 **XLC 17.1（IBM Open XL C/C++ for AIX 17.1.0）** 过程中遇到的 12 个问题及修复方法。  
如果你遇到了本文未涵盖的错误，欢迎在评论区分享，无论是否有解决方案。

---

## 1. 将 `cc` 替换为 `ibm-clang`

首先需要在全局 Makefile 中，将所有相关的 `cc` 替换为 `ibm-clang`，例如：

```diff
- CC=cc
- CXX=xlC_r
- XCC=xlC_r
- MAKE_SHARED=xlC_r
+ CC=ibm-clang
+ CXX=ibm-clang_r
+ XCC=ibm-clang_r
+ MAKE_SHARED=ibm-clang_r
````

同时，可参考 [选项映射文档](https://www.ibm.com/docs/en/openxl-c-and-cpp-aix/17.1.0?topic=options-mapping) 进行新 Clang 选项的映射。

---

## 2. error: unknown argument: '-qmakedep=gcc'

```diff
- GEN_DEPENDENTS_OPTIONS=-qmakedep=gcc  -E -MF $@.1 > /dev/null
+ GEN_DEPENDENTS_OPTIONS= -E -MF $@.1 > /dev/null
```

---

## 3. should not return a value \[-Wreturn-type]

```diff
- return -1;
+ return;
```

---

## 4. error: non-void function 'main' should return a value \[-Wreturn-type]

```diff
- return;
+ return 0;
```

---

## 5. error: unsupported option '-G' for target 'powerpc64-ibm-aix7.3.0.0'

```diff
- LIB_101_FLAGS := -G
+ LIB_101_FLAGS := -shared -Wl,-G
```

---

## 6. Undefined symbol (libxxxx.so)

```diff
- LIB_10_FLAGS := -bexport:$(SRC)/makefiles/xxxx.def
+ LIB_10_FLAGS := -lstdc++ -lm -bexport:$(SRC)/makefiles/xxxx.def
```

---

## 7. unsupported option -qlongdouble

```diff
- drv_connect.c.CC_OPTIONS=$(CFLAGS) -qlongdouble -brtl
+ drv_loadfunc.c.CC_OPTIONS=$(CFLAGS) $(IDIR) -brtl
```

---

## 8. Undefined symbol: .\_Z8u9\_closei

```diff
- extern int u9_close(int fd) ;
+ extern "C" int u9_close(int fd) ;
```

---

## 9. ERROR: Undefined symbol: .pow

```diff
- CXXLIBES = -lpthread -lC -lstdc++
+ CXXLIBES = -lpthread -lC -lstdc++ -lm
```

---

## 10. 'main' (argument array) must be of type 'char \*\*'

```diff
- d_char *argv[];
+ char *argv[];
```

---

## 11. first parameter of 'main' (argument count) must be of type 'int'

```diff
- int main(char *argc, char *argv[])
+ int main(int argc, char *argv[])
```

---

## 12. ERROR: Undefined symbol: .\_ZdaPv

```diff
- LIB_3_LIBS	:= -lverse -llog_nosig
+ LIB_3_LIBS	:= -lverse -llog_nosig -lstdc++
```

---

转载本文请注明作者与出处，禁止商业用途。欢迎关注公众号「DevOps攻城狮」。
