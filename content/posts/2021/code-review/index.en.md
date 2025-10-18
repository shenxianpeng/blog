---
title: Thoughts and Practices Based on Google's Code Review Principles
summary: This article introduces Google's code review principles and shares practical experience on how to effectively implement code review in a team, including process control and automated checks.
tags:
  - CodeReview
date: 2021-03-20
authors:
  - shenxianpeng
---

## Background

Code review is the process of having someone else examine your code. Its purpose is to ensure that the overall code health of the codebase continuously improves over time.


There's a Chinese proverb:  "Three people walking together, one is bound to be my teacher."

The same is true for code review:

* Others' reviews may offer different perspectives and suggestions;
* Everyone makes mistakes, and having an extra pair of eyes reduces the chance of errors.

Therefore, code review is the most important check before merging your code into the main branch. It's also an excellent and low-cost way to find bugs in software.


Given the importance and obvious benefits of code review, it's often heard that code review is difficult to implement and ineffective in teams. Where does the problem lie?


From my observation, there are two main reasons:

First, reading other people's code takes time, often requiring the code submitter to explain the business logic to the reviewer, thus consuming time for both parties;
Second, if the code reviewer is overworked and stressed and doesn't have time, it's easy to lead to inadequate execution and going through the motions;

How can we conduct code reviews more effectively? Let's first look at how large companies do it.  Google's article on code review provides specific principles.

## Google's Code Review Principles

When conducting a code review, ensure that:

* The code is well-designed
* The functionality is helpful to the code's users
* Any UI changes are sensible and look good
* Any concurrent programming is done safely
* The code is no more complex than necessary
* The developer hasn't implemented things they might need in the future
* The code has appropriate unit tests
* The tests are well-designed
* The developer has used clear names for everything
* The comments are clear, useful, and primarily explain *why* rather than *what*
* The code is properly documented
* The code follows our style guide

Ensure you examine every line of code you are asked to review, look at the context, ensure you are improving code health, and praise the developer for good work.

> Original: https://google.github.io/eng-practices/review/reviewer/looking-for.html

## Implementation of Code Review Principles

To better implement code review, it's necessary to first establish principles. You can adapt, remove, or add to the above principles based on your actual situation;

Second, technical leadership should actively promote the unified code review principles to developers;

Third, the specific rules in the principles should be incorporated into the Pull Request process as much as possible through process control and automated checks.


Also, remember to be peaceful as a Reviewer!!! When reviewing code, avoid giving suggestions with a "teaching" tone, as this can easily backfire.


Here are some incomplete practices for reference.

### Process Control

### Preventing any code without review from entering the main branch

> Using Bitbucket as an example. GitHub and GitLab have similar settings.

* Turn on the option `Prevent changes without a pull request` in the branch permission settings. Of course, if necessary, you can add exceptions to this option, allowing the added person to commit code without a Pull Request.

* Enable the `Minimum approvals` option in Merge Check. For example, set Number of approvals = 1, so at least one Reviewer needs to click the Approve button to allow merging.

### Automated Checks

### Verify compilation and testing through the CI pipeline

* Establish an automated build and test pipeline so that builds, tests, and checks can be automatically performed when creating a Pull Request. Jenkins' Multi-branch pipeline can meet this need.

* Turn on the `Minimum successful builds` option in Bitbucket's Merge Check to verify build/test results, preventing any code that hasn't passed build and tests from merging into the main branch.

* Additionally, you can achieve this by writing your own tools or integrating other CI tools for checks, such as:

  * Analyze the commit history of the Pull Request to suggest Reviewers;
  * Use Lint tools to check coding standards;
  * Use REST APIs to check if commits need to be compressed to ensure a clear commit history;
  * Use SonarQube to check the Quality Gate, etc.


Implementing automated checks can help Reviewers focus their review efforts on the specific implementation of the code, leaving other aspects to the tools.

### Conclusion

The effectiveness of code review is positively correlated with whether a team has a good technical atmosphere or whether there is technical leadership and influential senior engineers.

* If most engineers in a team are high-quality, they will enjoy writing excellent code (or nitpicking).
* Conversely, if the team doesn't value standards and only pursues short-term performance, it will only lead to accumulating more and more technical debt and products becoming increasingly worse.

Welcome to leave comments and share your opinions or suggestions.