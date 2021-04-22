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

## What's the problem?

Today I am having a problem where the Windows installer I created is not installing, and the following Windows installer box pops up.

![Windows installer](why-windows-installer-pop-up/windows-installer.png)

But it works well in the previous build, and I didn't make any code changes. It is strange, actually fix this problem is very easy but not easy to find. 

## How to fix it?

In my case, I just remove the space from my build folder naming. 

I made follow mistakes, my previous build name is `v2.2.2.3500-da121sa-Developer`, but for this build, I named it `v2.2.2.3500-32jkjdk - Developer`

## How to find the solution?

This problem takes me several hours until I google this article [article](https://community.spiceworks.com/topic/874022-msiexec-just-returns-a-pop-up) inspired me. 

I immediately remove the spaces from the build folder, then the installer back to work. 

Just like the above article, if I try to use the command line `msiexec.exe .....`, compare with the works installer will also quick to find the root cause.

If this happens to you, I hope it also works for you, and leave a comment if it works for you.
