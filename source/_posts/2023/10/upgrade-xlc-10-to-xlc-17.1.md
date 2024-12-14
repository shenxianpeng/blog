---
title: Problems and solutions when upgrading XLC from 10.1 to IBM Open XL C/C++ for AIX 17.1.0
tags:
  - AIX
  - Clang
  - XLC
categories:
  - AIX
date: 2023-10-08 18:53:26
author: shenxianpeng
---

In this article, I would like to document the problems encountered when upgrading from IBM XLC 10.1 to XLC 17.1 (IBM Open XL C/C++ for AIX 17.1.0) and how to fix the following 12 errors.

If you've encountered any other errors, feel free to share your comments with or without a solution.

<!-- more -->
## 1. Change cc to ibm-clang

First you need to change all the related `cc` to `ibm-clang` in the the global Makefile. for example:

```diff
- CC=cc
- CXX=xlC_r
- XCC=xlC_r
- MAKE_SHARED=xlC_r
+ CC=ibm-clang
+ CXX=ibm-clang_r
+ XCC=ibm-clang_r
+ MAKE_SHARED=ibm-clang_r
```

And check following link of [Mapping of options](https://www.ibm.com/docs/en/openxl-c-and-cpp-aix/17.1.0?topic=options-mapping
) to map new Clang options if any.

## 2. error: unknown argument: '-qmakedep=gcc'

```diff
- GEN_DEPENDENTS_OPTIONS=-qmakedep=gcc  -E -MF $@.1 > /dev/null
+ GEN_DEPENDENTS_OPTIONS= -E -MF $@.1 > /dev/null
```

## 3. should not return a value [-Wreturn-type]


```diff
- return -1;
+ return;
```

## 4. error: non-void function 'main' should return a value [-Wreturn-type]

```diff
- return;
+ return 0;
```

## 5. error: unsupported option '-G' for target 'powerpc64-ibm-aix7.3.0.0'

```diff
- LIB_101_FLAGS := -G
+ LIB_101_FLAGS := -shared -Wl,-G
```

## 6. Undefined symbol (libxxxx.so)

```diff
- LIB_10_FLAGS := -bexport:$(SRC)/makefiles/xxxx.def
+ LIB_10_FLAGS := -lstdc++ -lm -bexport:$(SRC)/makefiles/xxxx.def
```

## 7. unsupported option -qlongdouble

```diff
- drv_connect.c.CC_OPTIONS=$(CFLAGS) -qlongdouble -brtl
+ drv_loadfunc.c.CC_OPTIONS=$(CFLAGS) $(IDIR) -brtl
```

## 8. Undefined symbol: ._Z8u9_closei

```diff
- extern int u9_close(int fd) ;
+ extern "C" int u9_close(int fd) ;
```

## 9. ERROR: Undefined symbol: .pow

```diff
- CXXLIBES = -lpthread -lC -lstdc++
+ CXXLIBES = -lpthread -lC -lstdc++ -lm
```

## 10. 'main' (argument array) must be of type 'char **'

```diff
- d_char *argv[];
+ char *argv[];
```

## 11. first parameter of 'main' (argument count) must be of type 'int'

```diff
- int main(char *argc, char *argv[])
+ int main(int argc, char *argv[])
```

## 12. ERROR: Undefined symbol: ._ZdaPv

```diff
- LIB_3_LIBS	:= -lverse -llog_nosig
+ LIB_3_LIBS	:= -lverse -llog_nosig -lstdc++
```

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
