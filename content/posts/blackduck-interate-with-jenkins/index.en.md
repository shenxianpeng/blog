---
title: Black Duck—Jenkins Integration
summary: This article introduces how to integrate Black Duck with Jenkins to achieve automated security scanning and vulnerability detection for code repositories.
tags:
  - BlackDuck
  - Jenkins
date: 2020-12-08
translate: fase
author: shenxianpeng
---

Recently, I integrated Black Duck with Jenkins. The goal is to provide customized and scheduled source code scans for various development code repositories to testing and development teams.

## Why Perform Source Code Scanning



In product development, we often need to introduce open-source components. However, these open-source codes can pose risks to the product. Therefore, when releasing our products, we need to evaluate the vulnerabilities and license information of these open-source components.
![Open Source Does Not Equal Security](open-source.png)

Black Duck is a software tool for scanning, auditing, and managing source code (similar tools include JFrog Xray). It can search for secure open-source code, detect the use of open-source code in products, and check the usage and risks of external open-source code.

If code scanning is not performed in a timely manner, and scanning is only done right before product release, addressing any discovered issues becomes very passive. Therefore, the team needs to identify and resolve problems early. Integrating with a CI tool for daily, weekly, and monthly scans becomes crucial.

## General Steps for Manual Black Duck Execution

1. Manually download the code from the specified Git repository and branch.
2. Remove irrelevant code (Alternatively, specify the specific files or folders to scan using Black Duck parameters).
3. Manually execute the Black Duck scan command.
4. After successful scanning, upload the results to the internal Black Duck website for review by relevant personnel.

## Black Duck and Jenkins Integration Goals

1. A pipeline that supports customized code downloads from repositories.
2. Provide developers and testers with a simple interface for executing source code scans at any time.
3. Support regular automated scans and linkage with other Jenkins tasks.

## Black Duck Parameter Introduction

```bash
--blackduck.url                                       # Your Black Duck URL
--blackduck.username                                  # Your login username
--blackduck.api.token                                 # Your login user Token
--detect.project.name                                 # Project in Black Duck
--detect.project.version.name                         # Project version number
--detect.source.path                                  # Code directory to scan
--logging.level.com.synopsys.integration              # Scan log level
--blackduck.trust.cert=TRUE                           # Whether to trust socket (SSL)
--detect.blackduck.signature.scanner.snippet.matching # Scan snippet mode
```

For more parameters, refer to the official CI integration documentation [Synopsys Detect for Jenkins](https://synopsys.atlassian.net/wiki/spaces/INTDOCS/pages/71106939/Synopsys+Detect+for+Jenkins)

## Black Duck Configuration

First, install the Black Duck plugin [Synopsys Detect](https://wiki.jenkins.io/display/JENKINS/Synopsys+Detect+Plugin) into Jenkins.

Then, configure the Synopsys Detect plugin:

* Jenkins -> Configuration (System Configuration)
* Black Duck URL: Your company's internal Black Duck URL, for example, `https://yourcompany.blackducksoftware.com`
* Black Duck credentials: Note that the credentials type should be Secret text.  Enter your user's Token in the Secret field.
![Secret text Configuration](blackduck-credentials.png)
* After configuration, click "Test connections to Black Duck".  "Connection successful" indicates successful configuration.
![Connection successful](blackduck-config.png)

## Black Duck Pipeline Task Result

![Build with Parameters](blackduck-Jenkins-job.png)

## Black Duck Pipeline Code

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
      summary: 'Which version do you want to scan on Black Duck? MVSURE_v1.1, MVSURE_v1.2 or others?')
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

  # Only keep the last ten Jenkins execution results
  options {buildDiscarder(logRotator(numToKeepStr:'10'))}

  # Scheduled triggers can be added here

  stages {
    stage("git clone"){ # Parameterized git clone process
      steps{
        sh '''
        if [ -d ${REPO} ]; then
            rm -rf ${REPO}
        fi
        git clone -b ${BRANCH} --depth 1 https://$ROBOT_USR:"$ROBOT_PSW"@git.yourcompany.com/scm/github/${REPO}.git
        '''
      }
    }
    stage("black duck scan"){ # Parameterized Black Duck parameters
      steps {
        withCredentials([string(credentialsId: 'robot-black-duck-scan', variable: 'TOKEN')]) { # Use withCredentials to obtain Token
          synopsys_detect 'bash <(curl -s ${hub_detect}) --blackduck.url=${blackduck_url} --blackduck.username=${blackduck_user} --blackduck.api.token=${TOKEN} --detect.project.name=${detect_project} --detect.project.version.name=${detect_project_version} --detect.source.path=${detect_source_path} --logging.level.com.synopsys.integration=debug --blackduck.trust.cert=TRUE --detect.blackduck.signature.scanner.snippet.matching=${SNIPPET-MODES}'
        }
      }
    }
  }
  post {
    # Send email notification to the executor regardless of the result
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