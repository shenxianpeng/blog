---
title: JaCoCo 代码覆盖率实践
tags:
  - JaCoCo
  - Gradle
categories:
  - DevOps
date: 2020-11-17 19:18:33
author: shenxianpeng
---

## `build.gradle` 文件配置

比如使用 gradle 来管理的项目可以在 `build.gradle` 里添加如下代码

```java
plugins {
    id 'jacoco'
}


jacoco {
    toolVersion = "0.8.5"
}

test {
    useJUnitPlatform()
    exclude '**/**IgnoreTest.class'  // 如果有 test case 不通过，如有必要可以通过这样忽略掉
    finalizedBy jacocoTestReport       // report is always generated after tests run
}

jacocoTestReport {
    dependsOn test // tests are required to run before generating the report
    reports {
        xml.enabled true
        csv.enabled false
        html.destination file("${buildDir}/reports/jacoco")
    }
}
```

## 执行测试，生成代码覆盖率报告

然后执行 `gradle test` 就可以了。之后可以可以在 `build\reports\jacoco` 目录下找到报告了。

![JaCoCo报告](jacoco-imp/reports.png)

重点是如何分析报告。打开 index.html，报告显示如下：

![JaCoCo报告首页](jacoco-imp/index.png)

<!-- more -->

## 从代码覆盖率报告中忽略指定的包或代码

对于有些包和代码可能不属于你的项目，但也被统计在内，可以通修改在 `build.gradle` 将指定的代码或是包从 JaCoCo 报告中忽略掉。如下：

```java

// 省略部分代码 ...

jacocoTestReport {
    dependsOn test // tests are required to run before generating the report
    reports {
        xml.enabled true
        csv.enabled false
        html.destination file("${buildDir}/reports/jacoco")
    }
    afterEvaluate {
        classDirectories.setFrom(files(classDirectories.files.collect {
            fileTree(dir: it, exclude: [
			'com/vmware/antlr4c3/**'])
			'com/vmware/antlr4c3/**', 
            'com/basic/parser/BasicParser*'
            ])
        }))
    }
}
```


