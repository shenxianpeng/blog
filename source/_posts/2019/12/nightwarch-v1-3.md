---
title: Nightwarch v1.3 介绍
tags:
  - Javascript
  - Nightwatch
categories:
  - Automation
date: 2019-12-16 09:00:00
author: shenxianpeng
---

Nightwatch js 是我之前写自动化测试用例一直使用的测试框架，之后我还对 v0.9 官方的使用说明和 API 进行了翻译，由于是旧版本的介绍，我就不附地址了。以下是对最新版的 Nightwatch 的介绍

Nightwarch.js 是一个端到端的基于 Node.js 使用 W3C Webdriver （以前是 Selenium ）的自动化测试框架。

Nightwatch 是一个完整的集成解决方案，用于 web 应用程序和网站的端到端测试，以及 Node.js 单元测试和集成测试。

目前 Nightwatch v1.3的已经发布。如果要从v1.0之前的版本升级，参阅如下升级指南。

## 升级和启动

从NPM安装Nightwatch

```bash
npm install nightwatch --save-dev
```

### 安装浏览器驱动程序

#### Geckodriver（Firefox）

Geckodriver是用于驱动Mozilla Firefox浏览器的WebDriver服务。

```bash
npm install geckodriver --save-dev
```

#### Chromedriver

Chromedriver是用于驱动Google Chrome浏览器的WebDriver服务。

```bash
npm install chromedriver --save-dev
```

或用一行安装所有内容：

```bash
npm i nightwatch geckodriver chromedriver --save-dev
```

## 运行演示测试

Nightwatch 带有一个 example 文件夹，其中包含一些示例测试。

下面将运行一个基本测试，该测试打开搜索引擎 Ecosia.org，搜索 “nightwatch” 一词，并验证术语“第一个结果”是否是 Nightwatch.js 网站。

```bash
./node_modules/.bin/nightwatch node_modules/nightwatch/examples/tests/ecosia.js
```

Windows用户可能需要运行节点 node node_modules/.bin/nightwatch

## 手动下载浏览器驱动程序

Nightwatch 使用兼容 WebDriver 的服务器来控制浏览器。 WebDriver 是 W3C 规范和行业标准，提供了与浏览器进行交互的平台和 HTTP 协议。

Nightwatch包括对自动管理以下服务的支持：

### ChromeDriver

* 针对 Chrome 浏览器运行测试
* 下载网址 https://sites.google.com/a/chromium.org/chromedriver/downloads。

从版本75开始，Chromedriver 默认启用 W3C Webdriver 协议。如果您现在想坚持使用 JSONWire，请调整 chromeOptions：
```bash
desiredCapabilities : {
  browserName : 'chrome',
  chromeOptions: {
    w3c: false
  }
}
```

### GeckoDriver

针对 Mozilla Firefox 浏览器运行测试；
下载网址：https://github.com/mozilla/geckodriver/releases.

### Selenium Standalone Server

* 在一个地方管理多个浏览器配置，还可以利用 Selenium Grid 服务；
* 可以从 Selenium 发布页面下载 selenium 服务器 jar 文件 selenium-server-standalone-3.x.x.jar：https://selenium-release.storage.googleapis.com/index.html

重要的是要注意，尽管较早的 Nightwatch 版本（v0.9 及更低版本）需要 Selenium Server，但从 1.0 版本开始不再需要 Selenium。

特定的 WebDriver 设置指南可在 Docs 网站上找到。旧版 Selenium 驱动程序安装指南以及调试说明可以在 Wiki 上找到。

## 例子

示例文件夹中包含示例测试，这些示例演示了多个 Nightwatch 功能的用法。

你还可以查看 nightwatch-website-tests (https://github.com/nightwatchjs/nightwatch-website-tests) 存储库，例如针对 nightwatchjs.org (https://nightwatchjs.org/) 网站的测试。

## Nightwatch 单元测试

Nightwatch 的测试是使用 Mocha 编写的。

1.克隆项目

```bash
$ git clone https://github.com/nightwatchjs/nightwatch.git
$ cd nightwatch
$ npm install
```

2.运行测试

要运行完整的测试套件：
```bash
$ npm test
```

要检查测试范围，请运行以下命令：

```bash
$ npm run mocha-coverage
```

然后在浏览器中打开生成的 coverage/index.html 文件。
