---
title: 运行 lcov 报错 "Can't locate JSON/PP.pm in @INC ..."
summary: |
  本文介绍在运行 lcov 生成代码覆盖率报告时遇到 "Can't locate JSON/PP.pm in @INC ..." 等 Perl 模块缺失错误的解决方法，包括安装缺失的 Perl 模块。
tags:
  - lcov
  - perl
date: 2021-09-07
author: shenxianpeng
---

在执行以下命令生成代码覆盖率报告时：

```bash
lcov --capture --directory . --no-external --output-file coverage.info
```

我遇到了如下错误：

```bash
Capturing coverage data from .
Can't locate JSON/PP.pm in @INC (@INC contains: /usr/local/lib64/perl5 /usr/local/share/perl5 /usr/lib64/perl5/vendor_perl /usr/share/perl5/vendor_perl /usr/lib64/perl5 /usr/share/perl5 .) at /usr/local/bin/geninfo line 63.
BEGIN failed--compilation aborted at /usr/local/bin/geninfo line 63.
```

---

## 1. Can't locate CPAN.pm

当运行 `perl -MCPAN -e 'install JSON'` 时出现：

```bash
Can't locate CPAN.pm in @INC ...
```

解决方法：安装 `perl-CPAN`

```bash
sudo yum install perl-CPAN
```

---

## 2. Can't locate JSON/PP.pm

安装好 CPAN 后，再运行安装 JSON：

```bash
sudo perl -MCPAN -e 'install JSON'
```

如果依然报找不到 `JSON/PP.pm`，可通过复制 `backportPP.pm` 解决：

```bash
cd /usr/local/share/perl5/JSON
cp backportPP.pm PP.pm
```

---

## 3. Can't locate Module/Load.pm

```bash
geninfo --version
Can't locate Module/Load.pm in @INC ...
```

解决方法：安装 `perl-Module-Load-Conditional`

```bash
sudo yum install perl-Module-Load-Conditional
```

---

## 4. Can't locate Capture/Tiny.pm

```bash
lcov --version
Can't locate Capture/Tiny.pm in @INC ...
```

解决方法：用 CPAN 安装 `Capture::Tiny`

```bash
perl -MCPAN -e 'install Capture::Tiny'
```

---

## 5. Can't locate DateTime.pm

```bash
genhtml --help
Can't locate DateTime.pm in @INC ...
```

在 CentOS 7 下安装：

```bash
sudo yum install 'perl(DateTime)'
```

（但我测试中该方法无效，仅作参考。）

---

## 6. 运行 geninfo 报 Zlib 版本错误

```bash
Compress::Raw::Zlib version 2.201 required--this is only version 2.061 ...
```

解决方法：安装最新 `Compress::Raw::Zlib`

```bash
perl -MCPAN -e 'install Compress::Raw::Zlib'
```

---

通过逐一安装缺失的 Perl 模块，`lcov` 最终恢复正常工作：

```bash
lcov --version
lcov: LCOV version v1.16-16-g038c2ca
```

---

转载本文请注明作者与出处，禁止商业用途。欢迎关注公众号「DevOps攻城狮」。
