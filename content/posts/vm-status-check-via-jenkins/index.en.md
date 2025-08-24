---
title: This Can Be Done with Jenkins Too? Quickly Implement a Jenkins Job for Periodic Batch Login to Remote Virtual Machines and Support Adding New Hostnames
summary: This article introduces how to use Jenkins to implement periodic batch login to remote virtual machines and support users adding new hostnames. It provides complete implementation code and steps.
tags:
  - Shell
  - Jenkins
date: 2020-06-13
author: shenxianpeng
---

## Background

Implementing periodic batch login to remote virtual machines and then performing some specified operations, while also supporting users adding new hostnames.



## Requirements Breakdown

Periodic SSH login can be achieved through a simple shell script, but making it more elegant requires some thought, such as:

1. Automatic periodic execution
2. More intuitive login test result output
3. Support for users adding new virtual machine hostnames to the check list
4. Notify users after execution

Without introducing additional web pages, how can this be implemented using Jenkins and shell scripts?

1. Write a script to loop through all hostnames in a list.  This list should ideally be a file for easier management.
2. When a user submits a new hostname via the Jenkins job, use `grep` to check if the hostname already exists in the file.
3. If found, don't add it; if not found, add the hostname to the file.
4. Add the modified file to the Git repository, so the next Jenkins scheduled task will execute with the newly added hostname.

## Implementation Highlights

1. Using `expect`.  When using ssh to connect to a remote virtual machine, interaction with the remote connection is needed, such as expecting screen output and then providing corresponding input.  `expect` needs to be installed first. For Redhat, use: `sudo yum install expect`.

    > For more information on using `expect`, see this link: http://xstarcd.github.io/wiki/shell/expect.html

2. Using Shell arrays.  The shell script reads data from the file, performs login operations, and logs failed operations to an array, which is then printed.

3. When submitting a new hostname to the Git repository through Jenkins, the origin URL needs to be `https://${USERNAME}:${PASSWORD}@git.company.com/scm/vmm.git` or `git@company.com:scm/vmm.git` (an `id_rsa.pub` needs to be generated on the execution machine beforehand).

> The code has been uploaded to GitHub. Please refer to https://github.com/shenxianpeng/vmm.git

## Final Result

### Starting execution, providing input for new hostnames

![Bulid with parameters](pipeline-start.png)

### Execution complete, archiving the results for review

![VM 检查结果](pipeline-result.png)

### Archived results:

```bash
#####################################################
######### VM login check via SSH results ############
#####################################################
#                                                   #
# Compelted (success) 14/16 (total) login vm check. #
#                                                   #
# Below 2 host(s) login faied, need to check.       #
#                                                   #
      abc.company.com
      xyz.company.com
#                                                   #
#####################################################
```

## Conclusion

Technology is constantly evolving, especially for DevOps engineers, with new tools emerging all the time. Mastering every tool is almost impossible.

Merely knowing how to use a tool without understanding its underlying principles means that when a new tool replaces it, there's no real progress.

Only by thoroughly understanding the ins and outs of every problem encountered at work can we build a solid foundation.  This way, no matter how tools change, learning will be quick.

Mastering operating systems, shell scripting, and a proficient programming language before learning those tools is essential; otherwise, you'll always be adrift.