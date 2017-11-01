---
title: discoverQA
date: 2017-07-13 10:07:02
tags: test
---


### This automation frameworks was design by Java+Selenium+TestNG

**directory structure**
```
├──discoverQA
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
1. action: all test function write in this folder.<br />
2. config: all config file put in this folder.<br />
3. page: all page element write in this folder.<br />
4. verify: all verify test case write in this folder.<br />
5. testng.xml: test suit file, config all verify test case in this file.<br />
6. pom.xml: configuration need package files.

#### [Get clone discoverQA](https://github.com/shenxianpeng/discoverQA.git)
``` bash
$ git clone https://github.com/shenxianpeng/discoverQA.git
```

Any suggestion and questiosn please feel free to create issue [here](https://github.com/shenxianpeng/discoverQA/issues)