---
title: Regarding Extremely Slow and Occasional Upload Failures to Artifactory — A Case Study
summary: Encountered slow upload speeds and occasional failures when uploading artifacts to JFrog Artifactory. This post shares the troubleshooting process and lessons learned.
tags:
  - Artifactory
  - Troubleshooting
date: 2021-06-16
author: shenxianpeng
---

Recently, I encountered extremely slow artifact upload speeds when using Artifactory Enterprise. After collaborating with IT and the Artifactory administrator, the issue was finally resolved. I'm sharing the troubleshooting process here.

This might be helpful if you've encountered similar problems.


## Problem Description

Recently, I noticed that uploading artifacts to Artifactory via Jenkins occasionally became extremely slow. This was especially true when a Jenkins stage involved multiple uploads; the second upload often resulted in extremely slow transfer speeds (KB/s).

## Troubleshooting and Resolution

My build environment and Jenkins were unchanged, and all build jobs experienced slow uploads. To rule out the Artifactory plugin as the cause, I tested uploads using the `curl` command, which also exhibited slow speeds.

This pointed to a problem with Artifactory itself.

1. Was Artifactory recently upgraded?
2. Were any settings recently changed in Artifactory?
3. Was there a problem with the Artifactory server?

After communicating with the Artifactory administrator, possibilities 1 and 2 were ruled out. To completely eliminate Artifactory as the source of the problem, I tested using `scp` for copying files, and it also exhibited slow transfer speeds. This indicated a network issue.

This required IT's assistance to troubleshoot the network problem.  IT ultimately suggested trying a different network interface card (NIC) (due to similar past incidents). This would cause a brief network interruption, but the administrator eventually agreed.

Fortunately, after changing the NIC, the speed of Jenkins uploading artifacts to Artifactory returned to normal.

## Summary

A few takeaways from handling this incident:

Because this issue involved several teams, clearly defining the problem, providing well-reasoned hypotheses, and explaining the severity of the consequences (e.g., impact on releases) were crucial for getting everyone involved to prioritize the issue. Otherwise, everyone would wait, and nobody would solve the problem.

When the Artifactory administrator suggested using a different data center instance, I recommended they first try changing the NIC. If the problem persisted, they could create another server in the same data center. Only if the issue remained should they consider migrating to a different data center instance. This significantly reduced the extra work involved in trial-and-error from the user's perspective.
