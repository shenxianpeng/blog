---
title: Processing Jenkins Shell's Returned String as a Character Array
summary: How to process a string returned by a Shell script in a Jenkins Pipeline as a character array for further processing and use.
tags:
  - Jenkins
date: 2020-06-22
author: shenxianpeng
---

> Jenkins Tips 2 — Each issue describes a small Jenkins tip with brief text and images.

## Problem

We want to send different text data from Linux to different people via Jenkins email.

## Approach

We want to pre-process the data using Shell and then return it to the Jenkins pipeline. However, only the string returned by the Shell is obtained, so we need to process the string into an array in the Jenkinsfile and then process the values in the array using a for loop.

The following is the text data to be processed:

```bash
# Example
$ ls
fail-list-user1.txt  fail-list-user2.txt  fail-list-user3.txt
```

We need to process the above files separately through Jenkins, get users user1, user2, user3, and then send emails.

## Solution

### String Extraction

Filter out only user1, user2, user3 using Shell expressions:

```bash
# List all files starting with fail-list and assign them to an array l
l=$(ls -a fail-list-*)

for f in $l;
do
  f=${f#fail-list-} # Use # to extract left-side characters
  f=${f%.txt}       # Use % to extract right-side characters
  echo $f           # Final output contains only the user string
done
```

Test result:

```bash
$ ls
fail-list-user1.txt  fail-list-user2.txt  fail-list-user3.txt
$ l=$(ls -a fail-list-*) && for f in $l; do f=${f#fail-list-}; f=${f%.txt}; echo $f ; done;
user1
user2
user3
```

### Processing String into an Array

The following Jenkinsfile uses Groovy to process the string returned by Shell into a character array.

```groovy
// Jenkinsfile
// Ignoring other irrelevant steps like stage, steps, etc.
...

scripts {
  // Assign the Shell returned string to the owners variable. Note that \ is needed before $ for escaping.
  def owners = sh(script: "l=\$(ls -a fail-list-*) && for f in \$l; do f=\${f#fail-list-}; f=\${f%.txt}; echo \$f ; done;", returnStdout:true).trim()

  // Check if the owners array is empty. isEmpty() is a built-in Groovy method.
  if ( ! owners.isEmpty() ) {
    // Use .split() to split the owners string, returning a string array. Then use .each() to loop through the returned string array.
    owners.split().each { owner ->
      // Print the final user returned
      println "owner is ${owner}"

      // Send email, example
      email.SendEx([
          'buildStatus'  : currentBuild.currentResult,
          'buildExecutor': "${owner}",
          'attachment'   : "fail-list-${owner}.txt"
      ])
    }
  }
}
```

Finally, we have successfully processed the string returned by Shell into a character array using Groovy, achieving the email notification requirement for different people in the above example.

Hopefully, the above example will inspire and help you with similar needs.