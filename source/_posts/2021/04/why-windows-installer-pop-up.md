---
title: Why Windows installer pop up? (Resolved)
tags:
  - Windows
  - installer
categories:
  - Troubleshooting
date: 2021-04-22 13:33:01
author: shenxianpeng
---

## What's the Problem?

Today I am having a problem where the Windows installer I created is not installing and the following Windows installer box pops up.

![Windows installer](why-windows-installer-pop-up/windows-installer.png)

This worked in the previous build and I didn't make any code changes. This is very strange. Actually, fix this problem exactly very eary but not easy to find. 

## How to fix?

In my case: just remove the space from my build folder naming. I made follow mistakes

My previours build name is `v2.2.2.3500-da121sa-Developer`, but for this build I named it to `v2.2.2.3500-32jkjdk - Developer`

## How to find the solution?

This problem takes me several hours until I google this article [article](https://community.spiceworks.com/topic/874022-msiexec-just-returns-a-pop-up) inspired me. 

I immediately remove the spaces from the build folder, then the installer back to work. Just like this acticle, if try to use the command line `msiexec.exe .....`, campare with the works installer, I will also quickly to find the root casue.

If this happens to you, hopes it aslo works for you. good luck.
