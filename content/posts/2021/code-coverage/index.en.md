---
title: About Code Coverage
summary: This article briefly introduces the concept, importance, common metrics, working principle, and mainstream tools of code coverage, emphasizing that code coverage metrics should not be over-relied upon.
tags:
  - Coverage
  - DevOps
date: 2021-07-14
author: shenxianpeng
---

This article briefly introduces: What is code coverage? Why measure code coverage? Code coverage metrics, working principles, mainstream code coverage tools, and why not to overestimate code coverage metrics.

## What is Code Coverage?

Code coverage is a measure of the amount of code executed during the entire testing process. It measures which statements in the source code have been executed during testing and which have not.


## Why Measure Code Coverage?

As we all know, testing can improve the quality and predictability of software releases. But do you know how effective your unit tests or even your functional tests are in actually testing the code? Are more tests needed?

These are the questions that code coverage can attempt to answer. In short, we need to measure code coverage for the following reasons:

* Understand the effectiveness of our test cases on the source code
* Understand whether we have done enough testing
* Maintain test quality throughout the software lifecycle

Note: Code coverage is not a panacea. Coverage measurement cannot replace good code review and excellent programming practices.

Generally, we should adopt a reasonable coverage target and strive for uniform coverage across all modules, rather than just looking at whether the final number is high enough to be satisfactory.

For example: Suppose the code coverage is very high in some modules, but there are not enough test cases covering some key modules. Even though the code coverage is high, it does not mean that the product quality is high.

## Types of Code Coverage Metrics

Code coverage tools typically use one or more standards to determine whether your code has been executed after being subjected to automated testing. Common metrics seen in coverage reports include:

* **Function Coverage:** What percentage of defined functions have been called
* **Statement Coverage:** What percentage of statements in the program have been executed
* **Branch Coverage:** What percentage of branches in control structures (e.g., `if` statements) have been executed
* **Condition Coverage:** What percentage of Boolean sub-expressions have been tested as true and false
* **Line Coverage:** What percentage of lines of source code have been tested


## How Code Coverage Works

Code coverage measurement primarily uses three methods:

### 1. Source Code Instrumentation

Instrumentation statements are added to the source code, and the code is compiled using a normal compiler toolchain to generate an instrumented assembly. This is what we commonly call instrumentation; Gcov belongs to this category of code coverage tools.

### 2. Runtime Instrumentation

This method collects information from the runtime environment while the code is executing to determine coverage information. In my understanding, the principles of JaCoCo and Coverage tools belong to this category.

### 3. Intermediate Code Instrumentation

New bytecode is added to instrument compiled class files, generating a new instrumented class. To be honest, I Googled many articles and didn't find a definitive statement on which tools belong to this category.


Understanding the basic principles of these tools, combined with existing test cases, helps in correctly selecting code coverage tools. For example:

* If the product's source code only has E2E (end-to-end) test cases, usually only the first type of tool can be selected, i.e., an executable file compiled through instrumentation, followed by testing and result collection.
* If the product's source code has unit test cases, usually the second type of tool is selected, i.e., runtime collection. This type of tool has high execution efficiency and is easy to integrate continuously.

## Current Mainstream Code Coverage Tools

There are many code coverage tools. Below are code coverage tools I've used for different programming languages. When selecting tools, try to choose those that are open-source, popular (active), and easy to use.

| Programming Language | Code Coverage Tool |
| ----------- | ----------- |
| C/C++ | Gcov |
| Java | JaCoCo |
| JavaScript | Istanbul |
| Python | Coverage.py |
| Golang | cover |

## Don't Overestimate Code Coverage Metrics

Code coverage is not a panacea; it only tells us which code has not been "executed" by test cases. A high percentage of code coverage does not equal high-quality and effective testing.

First, high code coverage is not enough to measure effective testing. Instead, code coverage more accurately gives a measure of the extent to which code has *not* been tested. This means that if our code coverage metric is low, then we can be sure that important parts of the code have not been tested; however, the converse is not necessarily true.  High code coverage does not fully indicate that our code has been adequately tested.

Second, `100%` code coverage should not be one of our explicit goals. This is because there is always a trade-off between achieving `100%` code coverage and actually testing important code. While it is possible to test all code, the value of testing is also likely to diminish as you approach this limit, considering the tendency to write more meaningless tests to meet coverage requirements.

Borrowing a quote from Martin Fowler's article on [Test Coverage](https://www.martinfowler.com/bliki/TestCoverage.html):

> Code coverage is a useful tool for finding untested parts of your codebase, but it's not much use as a number telling you how good your tests are.

## References

> https://www.lambdatest.com/blog/code-coverage-vs-test-coverage/
> https://www.atlassian.com/continuous-delivery/software-testing/code-coverage
> https://www.thoughtworks.com/insights/blog/are-test-coverage-metrics-overrated