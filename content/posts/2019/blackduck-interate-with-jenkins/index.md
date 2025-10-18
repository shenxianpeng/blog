---
title: Black Duck 与 Jenkins 集成
summary: 本文介绍如何将 Black Duck 与 Jenkins 集成，实现对代码仓库的自动化安全扫描和漏洞检测。
tags:
  - BlackDuck
  - Jenkins
date: 2019-12-08
translate: false
authors:
  - shenxianpeng
---

最近做了 Black Duck 与 Jenkins 的集成，目标是给测试和开发提供定制化、定时的对各个开发代码仓库的进行源码扫描。

## 为什么要做源码扫描



在产品开发中经常需要引入一些开源组件，但这些开源的代码会给产品风险。因此我们在发布自己产品的时候需要对这些开源组件的漏洞和许可信息进行评估。
![开源不等于安全](open-source.png)

Black Duck（黑鸭）是一款对源代码进行扫描、审计和代码管理的软件工具（同类型的工具还有 JFrog Xray）。能够搜索安全的开源代码，检测产品的开源代码使用情况，以检查外来代码的开源代码使用情况和风险情况。

如果不能及时的进行代码扫描，在产品发布快要发布才进行扫描，如果发现问题这时候再去解决就会变得非常被动，因此团队需要尽早发现并解决问题，将 CI 工具进行集成，进行每日、每周、每月扫描就变得十分重要。

## Black Duck 手动执行一般步骤

1. 手动下载指定 Git 仓库及分支代码
2. 去掉不相关的代码（也可以通过 Black Duck 参数去指定要扫描的特定文件或文件夹）
3. 手动执行 Black Duck 扫描命令​
4. 扫描成功后，结果传到内部 Black Duck 网站供相关人员进行审查

## Black Duck 与 Jenkins 的集成目标

1. 一个流水线支持定制化仓库的代码下载
2. 给开发和测试提供简单的、可随时可以执行源码扫描的界面
3. 支持定期自动扫描，以及与其他 Jenkins 任务联动执行​

## Black Duck 参数介绍

```bash
--blackduck.url                                       # 你的 Black Duck 网址
--blackduck.username                                  # 你的登录用户
--blackduck.api.token                                 # 你的登录用户 Token
--detect.project.name                                 # Black Duck 下面的项目
--detect.project.version.name                         # 项目版本号
--detect.source.path                                  # 要扫描的代码目录
--logging.level.com.synopsys.integration              # 扫描日志级别
--blackduck.trust.cert=TRUE                           # 是否信任 socket (SSL)
--detect.blackduck.signature.scanner.snippet.matching # 扫描片段模式
```

更多其他参数可以参照官方的 CI 集成文档 [Synopsys Detect for Jenkins](https://synopsys.atlassian.net/wiki/spaces/INTDOCS/pages/71106939/Synopsys+Detect+for+Jenkins)

## Black Duck 配置

首先，安装 Black Duck 插件 [Synopsys Detect](https://wiki.jenkins.io/display/JENKINS/Synopsys+Detect+Plugin) 到 Jenkins

然后，配置 Synopsys Detect 插件

* Jenkins -> Confiruration（系统配置）
* Black Duck URL： 公司内部的 Black Duck 网址，例如 https://yourcompany.blackducksoftware.com
* Black Duck credentials： 注意要选择 credentials 类型为 Secret text, Secret 填写你用户的 Token
![Secret text 配置](blackduck-credentials.png)
* 配置完成后点击 Test connections to Black Duck，显示 Connection successful 表示配置成功。
![Connection successful](blackduck-config.png)

## Black Duck 流水线任务效果

![Build with Parameters](blackduck-Jenkins-job.png)

## Black Duck 流水线代码

```bash
pipeline{
  agent {
    node {
      label 'black-duck'
      customWorkspace "/agent/workspace/blackduck"
    }
  }

  parameters {
    choice(
      name: 'VERSION',
      choices: ['MVSURE_v1.1', 'MVSURE_v1.2', 'MVSURE_v2.2'],
      summary: 'Which version do you want scan on black duck? MVSURE_v1.1, MVSURE_v1.2 or others?')
    choice(
      name: 'REPO',
      choices: ['blog-server', 'blog-client', 'blog-docker'],
      summary: 'Which repository code does above VERSION belong to?')
    string(
      name: 'BRANCH',
      defaultValue: 'develop',
      summary: 'Which branch does above VERSION belong to?')
    choice(
      name: 'SNIPPET-MODES',
      choices: ['SNIPPET_MATCHING', 'SNIPPET_MATCHING_ONLY', 'FULL_SNIPPET_MATCHING', 'FULL_SNIPPET_MATCHING_ONLY', 'NONE'],
      summary: 'What snippet scan mode do you want to choose?')
  }

  environment {
    ROBOT                  = credentials("d1cbab74-823d-41aa-abb7-858485121212")
    hub_detect             = 'https://blackducksoftware.github.io/hub-detect/hub-detect.sh'
    blackduck_url          = 'https://yourcompany.blackducksoftware.com'
    blackduck_user         = 'robot@yourcompany.com'
    detect_project         = 'GITHUB'
    detect_project_version = '${VERSION}'
    detect_source_path     = '${WORKSPACE}/${REPO}/src'
  }

  # 只保留最近十次 Jenkins 执行结果
  options {buildDiscarder(logRotator(numToKeepStr:'10'))}

  # 定时触发可以在这里添加

  stages {
    stage("git clone"){ # 参数化 git clone 代码过程
      steps{
        sh '''
        if [ -d ${REPO} ]; then
            rm -rf ${REPO}
        fi
        git clone -b ${BRANCH} --depth 1 https://$ROBOT_USR:"$ROBOT_PSW"@git.yourcompany.com/scm/github/${REPO}.git
        '''
      }
    }
    stage("black duck scan"){ # 参数化 Black Duck 所用到的参数值
      steps {
        withCredentials([string(credentialsId: 'robot-black-duck-scan', variable: 'TOKEN')]) { # 用 withCredentials 来获得 Token
          synopsys_detect 'bash <(curl -s ${hub_detect}) --blackduck.url=${blackduck_url} --blackduck.username=${blackduck_user} --blackduck.api.token=${TOKEN} --detect.project.name=${detect_project} --detect.project.version.name=${detect_project_version} --detect.source.path=${detect_source_path} --logging.level.com.synopsys.integration=debug --blackduck.trust.cert=TRUE --detect.blackduck.signature.scanner.snippet.matching=${SNIPPET-MODES}'
        }
      }
    }
  }
  post {
    # 不论结果任何都给执行者发送邮件通知
    always {
      script {
        def email = load "vars/email.groovy"
        wrap([$class: 'BuildUser']) {
            def user = env.BUILD_USER_ID
            email.build(currentBuild.result, "${user}")
        }
      }
    }
    success {
      echo "success, cleanup blackduck workspace"
      cleanWs()
    }
  }
}
```
