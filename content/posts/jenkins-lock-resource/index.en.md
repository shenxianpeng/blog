---
title: How to Lock and Unlock Resources via Jenkins
summary: This article introduces how to use the Jenkins Lockable Resources plugin to manage and lock resources, ensuring exclusivity and security of resources in a multi-task environment.
date: 2019-08-10
tags:
- Jenkins
- Pipeline
- Jenkins
author: shenxianpeng
---

## Business Scenario

Daily work requires switching to different versions on different platforms (including Linux, AIX, Windows, Solaris, HP-UX) for development and problem verification. However, due to limited virtual machines, it cannot be guaranteed that every developer and tester has virtual machines for all platforms with different versions installed. Therefore, preparing various development and testing environments can be time-consuming.



## Requirements Analysis

For such requirements, Docker is usually the first consideration; secondly, fetching builds from Artifactory and installing them via CI tools; finally, building from source code and then installing.

* Regarding Docker, because we support numerous platforms, including Linux, AIX, Windows, Solaris, and HP-UX, Docker is only suitable for Linux and Windows, so it cannot meet this requirement.

* Due to other reasons, our Artifactory is temporarily unavailable, so we can only choose to build from source code and then install. Both methods need to address the issue of resource locking and unlocking. If the current environment is being used by someone, the resources of that virtual machine should be locked, preventing Jenkins from calling the node in use again, to ensure that the environment is not damaged during use.

This article mainly introduces how to achieve resource locking and unlocking using the Jenkins Lockable Resources Plugin.

## Demo

1. Setting up Lockable Resources

    * Jenkins -> Manage Jenkins -> Configure System -> Lockable Resources Manager -> Add Lockable Resource
    ![I have set up two Resources ](config-lock-resource.png)
    The Labels here are the Labels of your nodes, set in Jenkins -> Manage Jenkins -> Manage Nodes and Clouds

2. Viewing the Lockable Resources Pool

    ![Showing that I have two resources available ](lock-resource-pool.png)

3. Testing Resource Locking
    * Here, I have configured a parameterized job that allows selection of different platforms and repositories for building.
    ![ Build With Parameters ](build-with-parameters.png)
    * Running the first job
    ![ The first Job is running ](build-with-parameters-1.png)
    * Viewing the current number of available resources: Free resources = 1, showing that it is being used by Job #47.
    ![Current number of available resources is 1](lock-resource-pool-1.png)
    * Running a second job
    ![ The second Job is running ](build-with-parameters-2.png)
    * Viewing the current number of available resources: Free resources = 0, showing that it is being used by Job #48.
    ![Current number of available resources is 0](lock-resource-pool-2.png)
    * Crucially, if a third job is run, will it be executed?
    ![ The third Job is queued ](build-with-parameters-3.png)
    *  The task is not executed. Checking the log shows it's waiting for available resources.
    ![ The third Job log ](build-with-parameters-3-log.png)

4. Testing Resource Unlocking
    * Now, releasing a resource, let's see if the third job can acquire the resource and execute.
    ![ Releasing Job 1 lock ](unlock-job-1.png)
    * The following image shows that the third job has run successfully.
    ![ The third Job running ](unlock-job-1-after.png)

## Jenkins Pipeline Code

The most crucial part of the entire pipeline is how to lock and unlock. This is achieved using `lock` and `input` steps.

The current job will remain unfinished until the user clicks Yes, and its lock will remain in effect.  The lock is released once Yes is clicked and the job ends.

Refer to the following `Jenkinsfile` for details.

```bash
pipeline {
    agent {
        node {
            label 'PreDevENV'
        }
    }
    options {
        lock(label: 'PreDevENV', quantity: 1)
    }

    parameters {
        choice(
            name: 'platform',
            choices: ['Linux', 'AIX', 'Windows', 'Solris', 'HP-UX'],
            summary: 'Required: which platform do you want to build')
        choice(
            name: 'repository',
            choices: ['repo-0.1', 'repo-1.1', 'repo-2.1', 'repo-3.1', 'repo-4.1'],
            summary: 'Required: which repository do you want to build')
        string(
            name: 'branch',
            defaultValue: '',
            summary: 'Required: which branch do you want to build')
    }

    stages {
        stage('git clone'){
            steps {
                echo "git clone source"
            }
        }
        stage('start build'){
            steps {
                echo "start build"
            }
        }
        stage('install build'){
            steps{
                echo "installing"
            }
        }
        stage('unlock your resource'){
            steps {
                input message: "do you have finished?"
                echo "Yes, I have finished"
            }
        }
    }
}
```