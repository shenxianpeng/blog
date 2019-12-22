---
title: Nightwatchjs 中文参考手册
date: 2017-10-19 16:31:57
tags: 
- Nightwatch
- Automation
categories: 
- Automation
author: shenxianpeng
---

[Nightwatch中文参考手册](https://shenxianpeng.gitbooks.io/nightwatch-js-cn/content/)

## 为何放弃 JAVA 改用 Nightwatch

- 项目初期用的是 Java + Selenium + TestNG 自动化框架，由于之前推行的力度不够，加上繁重的功能测试和频繁的项目变更导致自动化测试代码跟不上开发的进度，大量的测试代码无法正在运行。
- 我们的产品采用的 AngularJS 开发，前端开发人员对js对Java更精通，以后的自动化脚本开发也可以一起编写。
- Nightwatch 的环境配置和执行简单，只要 npm install、npm test 就可以运行起来，方便配置，运行和继续集成。

因此，与其维护不可用的代码不如好好整理，不如在项目领导和开发的强力支持下重新开始做一套可用的 E2E 测试。

## 关于 Nightwatch 翻译

学习中发现 Nightwatch 没有比较完整的中文参考手册，因此决定学习之余翻译下官方文档，如有问题，欢迎纠正。
