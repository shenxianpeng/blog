---
title: Run lcov failed "Can't locate JSON/PP.pm in @INC ..."
tags:
  - lcov
  - perl
categories:
  - Coverage
date: 2021-09-07 10:18:22
author: shenxianpeng
---

When execute command: `lcov --capture --directory . --no-external --output-file coverage.info` to generate code coverage report, I encountered the following error:

```bash
$ lcov --capture --directory . --no-external --output-file coverage.info
Capturing coverage data from .
Can't locate JSON/PP.pm in @INC (@INC contains: /usr/local/lib64/perl5 /usr/local/share/perl5 /usr/lib64/perl5/vendor_perl /usr/share/perl5/vendor_perl /usr/lib64/perl5 /usr/share/perl5 .) at /usr/local/bin/geninfo line 63.
BEGIN failed--compilation aborted at /usr/local/bin/geninfo line 63.
sh-4.2$ perl -MCPAN -e 'install JSON'
Can't locate CPAN.pm in @INC (@INC contains: /usr/local/lib64/perl5 /usr/local/share/perl5 /usr/lib64/perl5/vendor_perl /usr/share/perl5/vendor_perl /usr/lib64/perl5 /usr/share/perl5 .).
BEGIN failed--compilation aborted.
```

## Can't locate CPAN.pm

fixed this problem "Can't locate CPAN.pm" by running the command `yum install perl-CPAN`

```bash
sh-4.2$ sudo perl -MCPAN -e 'install JSON'
[sudo] password for sxp:
Can't locate CPAN.pm in @INC (@INC contains: /usr/local/lib64/perl5 /usr/local/share/perl5 /usr/lib64/perl5/vendor_perl /usr/share/perl5/vendor_perl /usr/lib64/perl5 /usr/share/perl5 .).
BEGIN failed--compilation aborted.
sh-4.2$ sudo yum install perl-CPAN
```

Then run `sudo perl -MCPAN -e 'install JSON'` again, it works.

## Can't locate JSON/PP.pm

fixed this problem by copying backportPP.pm to the PP.pm file.

```bash
$ cd /usr/local/share/perl5/JSON
$ ls
backportPP  backportPP.pm
$ cp backportPP.pm PP.pm
```

## Can't locate Module/Load.pm

```bash
bash-4.2$ geninfo --version
Can't locate Module/Load.pm in @INC (@INC contains: /usr/local/lib64/perl5 /usr/local/share/perl5 /usr/lib64/perl5/vendor_perl /usr/share/perl5/vendor_perl /usr/lib64/perl5 /usr/share/perl5 .) at /usr/local/bin/geninfo line 63.
BEGIN failed--compilation aborted at /usr/local/bin/geninfo line 63.
bash-4.2$
```

Install `perl-Module-Load-Conditional` can resolved.

```bash
sudo yum install perl-Module-Load-Conditional
```
