---
title: Creating a NuGet Organization—Pitfalls Encountered
summary: This article documents the problems and solutions encountered when creating a NuGet Organization, especially regarding the use of corporate email addresses.
tags:
  - NuGet
author: shenxianpeng
date: 2023-08-25
---

Actually, there's nothing much to say about creating an account on a package management platform, but recently, when I was preparing to create an Organization on https://www.nuget.org before releasing a product, I encountered a problem.

## Here's What Happened

As a company employee, when I first opened the NuGet website (www.nuget.org) and clicked "Sign in," I saw "Sign in with Microsoft."  I clicked, went through the next steps, and successfully registered my first NuGet account using my company email address.

When I tried to create an Organization, entering my company email address resulted in a message saying the email address was already in use. What???

OK. So I tried entering my colleague's company email address.

After receiving the email notification, my colleague followed the steps: opened NuGet.org, clicked "Sign in with Microsoft," and filled in their account details.  However, after completing this process and trying to register an Organization using their email address, they also received the message that the email was already in use.  What's going on!!!  I was baffled...


## How It Was Solved

At this critical juncture, while anxiously awaiting the release, I suddenly had a flash of inspiration.  With a "desperate measures" mentality, I changed the company email address associated with my personal NuGet account to my Gmail address. Then, when creating the Organization, I used my company email address, and the Organization was successfully created!

This document records the problem I encountered while registering with NuGet. I don't know if it will be helpful to you, but if it does, please let me know.

---

Please indicate the author and source when reprinting this article. Do not use it for any commercial purposes.  Welcome to follow the WeChat public account "DevOps攻城狮"