---
title: -fprofile-arcs -ftest-coverage
tags:
  - -ftest-coverage
  - -fprofile-arcs
  -
categories:
  - GCC
date: 2021-06-27 17:22:32
author: shenxianpeng
---

## error 0

```
g++     -m64  -m64 -DU2_64_BUILD -fPIC   genconfig.o  -L/workspace/mvas-code/uvuddb/src/uvhome/releasex64/bin/ -L/workspace/mvas-code/uvuddb/src/uvhome/releasex64/lib/ -luniverse  -Wl,-rpath=/workspace/mvas-code/uvuddb/src/uvhome/releasex64/bin/ -Wl,-rpath=/.uvlibs  -Wl,--enable-new-dtags -L/.uvlibs -lodbc   -lutil -lpthread  -lglib-2.0 -lstdc++ -lnsl -lrt -ldl -lacl -lgcov -o /workspace/mvas-code/uvuddb/src/uvhome/releasex64/objs/uv/uvsrc/build_tools/genconfig
/usr/bin/ld: /workspace/mvas-code/uvuddb/src/uvhome/releasex64/objs/uv/uvsrc/build_tools/genconfig: hidden symbol `__gcov_init' in /usr/lib/gcc/x86_64-redhat-linux/4.8.5/libgcov.a(_gcov.o) is referenced by DSO
/usr/bin/ld: final link failed: Bad value
collect2: error: ld returned 1 exit status
gmake[1]: *** [/workspace/mvas-code/uvuddb/src/uvhome/releasex64/objs/uv/uvsrc/build_tools/genconfig] Error 1
gmake: *** [config_tools] Error 2

```

## solution 0

```bash
# add -shared after g++. like

g++  -shared   -m64  -m64 -DU2_64_BUILD -fPIC   genconfig.o  ....

```

## error 1

```
g++     -m64  -m64 -DU2_64_BUILD -fPIC   loadfile.o U_preprint2.o  -L/workspace/mvas-code/uvuddb/src/uvhome/releasex64/bin/ -L/workspace/mvas-code/uvuddb/src/uvhome/releasex64/lib/ -luniverse -lu2gci /workspace/mvas-code/uvuddb/src/uvhome/releasex64/lib/libu2ssldl.a -Wl,-rpath=/workspace/mvas-code/uvuddb/src/uvhome/releasex64/bin/ -Wl,-rpath=/.uvlibs  -Wl,--enable-new-dtags -L/.uvlibs -lodbc -lm -lcrypt -ldl -lstdc++ -lpam -lcurses -lacl  -Wl,-rpath=/workspace/mvas-code/uvuddb/src/uvhome/releasex64/bin/ -Wl,-rpath=/.uvlibs  -Wl,--enable-new-dtags -L/.uvlibs -lodbc   -lutil -lpthread  -lglib-2.0 -lstdc++ -lnsl -lrt -ldl -lacl -lgcov -o /workspace/mvas-code/uvuddb/src/uvhome/releasex64/objs/exe/loadfile
/usr/bin/ld: /workspace/mvas-code/uvuddb/src/uvhome/releasex64/objs/exe/loadfile: hidden symbol `__gcov_init' in /usr/lib/gcc/x86_64-redhat-linux/4.8.5/libgcov.a(_gcov.o) is referenced by DSO
/usr/bin/ld: final link failed: Bad value
collect2: error: ld returned 1 exit status
gmake[1]: *** [/workspace/mvas-code/uvuddb/src/uvhome/releasex64/objs/exe/loadfile] Error 1
gmake: *** [loadfile] Error 2

```

## solution 1

```bash
# also add -shared before g++, like
g++   -shared  -m64  -m64 -DU2_64_BUILD -fPIC   loadfile.o ...
```

## error 3


```bash
gmake -C include -f gMakefile.uv prebuild
/workspace/mvas-code/uvuddb/src/uv/uvsrc/build_tools/smp /workspace/mvas-code/uvuddb/src/u2/include/uvh.smp uv.h COMP_TYPE=RHLINUX
gmake[1]: *** [uv.h] Segmentation fault (core dumped)
gmake: *** [prebuild] Error 2

```
