---
title: nightwatchjs-guilde
date: 2017-10-19 16:31:57
tags: nightwatch
---


#### 为何放弃JAVA改用Nightwatch？

- 项目初期用的是Java+Selenium+TestNG 自动化框架，由于之前推行的力度不够，加上繁重的功能测试和频繁的项目变更导致自动化测试代码跟不上开发的进度，大量的测试代码无法正在运行。
- 其次，我们的项目采用的AngularJS开发，前端开发人员对js对Java更精通，以后的自动化脚本开发也可以参与编写。
- 再次，Nightwatch的环境配置和执行都很简单只要npm install、npm test就可以运行起来，方便配置，运行和继续集成。

因此，与其维护不可用的代码不如好好整理，不如在项目领导和开发的强力支持下重新开始做一套可用的E2E测试。

当我在使用Nightwatch做JavaScript自动化测试的时发现没有完整的中文文档，所以就有了这个 [Nightwatch中文参考手册](https://shenxianpeng.gitbooks.io/nightwatch-js-cn/content/)。