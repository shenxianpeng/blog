---
title: Fixed "Remote session was disconnected because there are no Remote Desktop client access licenses available"
tags:
  - Windows
  - RDP
categories:
  - Windows
date: 2020-08-10 15:40:04
author: shenxianpeng
---

## Problem

Sometimes my Windows server 2012 R2 has RDP connect problem below:

```text
The remote session was disconnected because there are no Remote Desktop client access licenses available for this computer.
Please contact the server administrator.
```

![RDP connect problem](rdp-problem/RDP-failed.png)

<!-- more -->

## How to Fix

You could log in to the vSphere Web Client if you have via console or have some other way to log in to the machine.

1. Open regedit.exe and navigate to

    ![Regedit](rdp-problem/regedit.jpg)

2. Search and Delete `LicensingGracePeriod` and `LicensingGracePeriodExpirationWarningDays`

3. If deletion failed, this failure message appears `unable to delete all specified values`, you need change permission. Refer to the related [videos](https://www.youtube.com/results?search_query=unable+to+delete+all+specified+values) on YouTuBe.

4. Reboot the system if it is still doesn't work.

In my case, every 90 to 120 days, the RDP end of grace period shows up, this is not the final solution. please let me know if you have a better solution.

> Finally, thanks to Bill K. shared with me the above solution.
