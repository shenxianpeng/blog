---
title: JST automation framework
date: 2017-07-13 10:07:02
tags:
- Java
- TestNG
- Selenium
categories:
- Automation
---

This automation framework was design by Java+Selenium+TestNG when I did automation test work, so I called it JST-automation.

## Directory Structure
<!-- more -->

```bash
├──JST-automation
|   ├── src
|   |   └── main
|   |   |   └── java
|   |   |   |   └── com
|   |   |   |   |   └── action
|   |   |   |   |   |   └── case01
|   |   |   |   |   |   └── case02
|   |   |   |   |   |   └── common
|   |   |   |   |   |   └── .....
|   |   |   |   |   └── config
|   |   |   |   |   |   └── UserConfig
|   |   |   |   |   |   └── DriverConfig
|   |   |   |   |   |   └── UrlConfig
|   |   |   |   |   |   └── ......
|   |   |   |   |   └── page
|   |   |   |   |   |   └── LoginPage
|   |   |   |   |   |   └── HomePage
|   |   |   |   |   |   └── ......
|   |   |   |   |   └── verify
|   |   |   |   |   |   └── case01
|   |   |   |   |   |   └── case02
|   |   |   |   |   |   └── ......
|   └── testng.xml
|   └── pom.xml
```

1. action: all test function write in this folder
2. config: all config file put in this folder
3. page: all page element write in this folder
4. verify: all verify test case write in this folder
5. testng.xml: test suit file, config all verify test case in this file
6. pom.xml: configuration need package files

## Download Code

```bash
git clone https://github.com/shenxianpeng/JST-automation.git
```

Any suggestion and questions please feel free to create issue [here](https://github.com/shenxianpeng/JST-automation/issues)
