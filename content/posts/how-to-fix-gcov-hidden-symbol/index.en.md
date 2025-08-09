---
title: How to fix "hidden symbol `__gcov_init' in ../libgcov.a(_gcov.o) is referenced by DSO"
summary: |
  This article explains how to resolve the "hidden symbol `__gcov_init' in ../libgcov.a(_gcov.o) is referenced by DSO" error when building a project with Gcov, including how to ensure symbols are not hidden.
tags:
  - Gcov
  - Coverage
  - DevOps
date: 2021-07-27
author: shenxianpeng
---

## Problem

When we introduced Gocv to build my project for code coverage, I encountered the following error message:


### error 1

```bash
g++     -m64 -z muldefs -L/lib64 -L/usr/lib64 -lglib-2.0 -m64 -DUV_64PORT -DU2_64_BUILD -fPIC -g  DU_starter.o
NFA_msghandle.o NFA_svr_exit.o du_err_printf.o  -L/workspace/code/myproject/src/home/x64debug/bin/
-L/workspace/code/myproject/src/home/x64debug/bin/lib/ -lundata -lutcallc_nfasvr
-Wl,-rpath=/workspace/code/myproject/src/home/x64debug/bin/ -Wl,-rpath=/.dulibs28  -Wl,--enable-new-dtags
-L/.dulibs28 -lodbc  -lm -lncurses -lrt -lcrypt -lgdbm -ldl -lpam -lpthread  -ldl -lglib-2.0
-lstdc++ -lnsl -lrt -lgcov -o /workspace/code/myproject/src/home/x64debug/objs/du/share/dutsvr
/usr/bin/ld: /workspace/code/myproject/src/home/x64debug/objs/du/share/dutsvr:
hidden symbol `__gcov_init' in /usr/lib/gcc/x86_64-redhat-linux/4.8.5/libgcov.a(_gcov.o) is referenced by DSO
```

### error 2

It may also be such an error

```bash
/home/p7539c/cutest/CuTest.c:379: undefined reference to `__gcov_init'
CuTest.o:(.data+0x184): undefined reference to `__gcov_merge_add'
```

## Positioning problem

Let's take the **error 1**.

From the error message, I noticed `-lundata -lutcallc_nfasvr` are all the linked libraries (-l*library*)

I checked libraries `undata` and `utcallc_nfasvr` one by one, and found it displayed `U __gcov_init` and `U` means undefined symbols.

> Use the `find` command to search the library and the `nm` command to list symbols in the library.

```bash
-sh-4.2$ find -name *utcallc_nfasvr*
./bin/libutcallc_nfasvr.so
./objs/du/work/libutcallc_nfasvr.so
-sh-4.2$ nm ./bin/libutcallc_nfasvr.so | grep __gcov_init
                 U __gcov_init
```

## How to fix

In my case, I just added the following code `LIB_1_LIBS := -lgcov` to allow the `utcallc_nfasvr` library to call gcov.

```bash
LIB_1 := utcallc_nfasvr
# added below code to my makefile
LIB_1_LIBS := -lgcov
```

Rebuild, the error is gone, then checked library, it displayed `t __gcov_init` this time, it means symbol value exists not hidden.

```bash
-sh-4.2$ nm ./bin/libutcallc_nfasvr.so | grep __gcov_init
                 t __gcov_init
```

Or in your case may build a shared library like so, similarly, just add the compile parameter `-lgcov`

```bash
g++   -shared -o libMyLib.so src_a.o src_b.o src_c.o -lgcov
```

## Summary

I have encountered the following problems many times

```bash
undefined reference to `__gcov_init'

undefined reference to `__gcov_merge_add'

`hidden symbol `__gcov_init' in /usr/lib/gcc/x86_64-redhat-linux/4.8.5/libgcov.a(_gcov.o) is referenced by DSO`
```

Each time I can fix it by adding `-glcov` then recompile. the error has gone after rebuild. (you use the `nm` command to double-check whether the symbol has been added successfully.)

Hopes it can help you.
