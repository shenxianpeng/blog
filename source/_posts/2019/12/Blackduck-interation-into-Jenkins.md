---
title: Blackduck 与 Jenkins 集成
tags:
  - Blackduck
  - Jenkins
  - Synopsys
  - Detect
categories:
  - Jenkins
date: 2019-12-06 14:48:02
author: shenxianpeng
---

Black Duck（黑鸭软件）是一款对源代码进行扫描、审计和代码管理的软件工具。能够搜索安全的开源代码，检测产品的开源代码使用情况，以检查外来代码的开源代码使用情况和风险情况。

但是如果不能定期的进行代码扫描，在产品发布后期才进行扫描如果发现问题，这时候再去解决这些问题就会变得非常被动，因此能够与 CI 工具进行集成就显示十分必要。

这里有一份官方的 CI 集成文档供参考。[Synopsys Detect for Jenkins](https://synopsys.atlassian.net/wiki/spaces/INTDOCS/pages/71106939/Synopsys+Detect+for+Jenkins)。

如下是实施并测试通过的 Jenkinsfile.

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
      description: 'Which version do you want scan on black duck? MVSURE_v1.1, MVSURE_v1.2 or others?')
    choice(
      name: 'REPO', 
      choices: ['blog-server', 'blog-client', 'blog-docker'], 
      description: 'Which repository code does above VERSION belong to?')
    string(
      name: 'BRANCH', 
      defaultValue: 'develop', 
      description: 'Which branch does above VERSION belong to?')
    choice(
      name: 'SNIPPET-MODES', 
      choices: ['SNIPPET_MATCHING', 'SNIPPET_MATCHING_ONLY', 'FULL_SNIPPET_MATCHING', 'FULL_SNIPPET_MATCHING_ONLY', 'NONE'], 
      description: 'What snippet scan mode do you want to choose?')
  }

  environment {
    ROBOT                  = credentials("d1cbab74-823d-41aa-abb7-858485121212")
    hub_detect             = 'https://blackducksoftware.github.io/hub-detect/hub-detect.sh'
    blackduck_url          = 'https://yourcompany.blackducksoftware.com'
    blackduck_user         = 'robot@yourcompany.com'
    detect_project         = 'MVAS'
    detect_project_version = '${VERSION}'
    detect_source_path     = '${WORKSPACE}/${REPO}/src'
  }

  options {buildDiscarder(logRotator(numToKeepStr:'10'))}

  stages {
    stage("git clone"){
      steps{
        sh '''
        if [ -d ${REPO} ]; then
            rm -rf ${REPO}
        fi
        git clone -b ${BRANCH} --depth 1 https://$ROBOT_USR:"$ROBOT_PSW"@git.yourcompany.com/scm/mvas/${REPO}.git
        '''
      }
    }
    stage("black duck scan"){
      steps {
        withCredentials([string(credentialsId: 'robot-black-duck-scan', variable: 'TOKEN')]) {
          synopsys_detect 'bash <(curl -s ${hub_detect}) --blackduck.url=${blackduck_url} --blackduck.username=${blackduck_user} --blackduck.api.token=${TOKEN} --detect.project.name=${detect_project} --detect.project.version.name=${detect_project_version} --detect.source.path=${detect_source_path} --logging.level.com.synopsys.integration=debug --blackduck.trust.cert=TRUE --detect.blackduck.signature.scanner.snippet.matching=${SNIPPET-MODES}'
        }
      }
    }
  }
  post {
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
