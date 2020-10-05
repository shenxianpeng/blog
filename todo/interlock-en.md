---
title: About Artifactory and Infrastructure Backup Strategy
tags:
  - Infrastructure
  - Artifactory
  - Backup
categories:
  - DevOps
date: 2020-09-25 17:26:03
author: shenxianpeng
---

# Agenda

* Artifactory
* Backup Strategy
* Commit Stardard 
* Ohter CICD work

# Artifactory

At the last Interlock meeting I shared about Jenkins. and two topics were left for next interlock meeting: one was about Artifactory and the other was Infrastructure Backup Strategy。

## Why is Artifactory

Artifactory is not only a very important tool in the DevOps tool chain, but also one of the tools in Rocket's unified tool chain planning. Using Artifactory to manage our build products will bring the following advantages:

* Good integration with CI tools
* Support recording package metadata
    * such as Build results, automated test results, and future vulnerability scan results that we can add to this build.
* Support the storage of multi-language products
    * such as Maven, npm, Docker, etc., reduce maintenance costs caused by the use of multiple tools, and unify product sources.

In order to better realize the CI/CD pipeline, the following series of unified tasks have been done in the design and implementation of integration with Aritifactory.

## First, design the Artifactory workflow

From this picture, you can see that there are a total of four repositories, they are based on the use of Artifactory research and official recommendations. The four repositories are divided according to their maturity. The different parts of their names are `DEV`, `INT`, `STAGE`, `RELEASE`.

`DEV` open access for developers. It is provided for developers to use, they can upload some libs, 3rdParty and other binary files here.

`INT` used by CI builds。This repository is used to store the automated build of the CI tool, and is the place to put the build.

`STAGE` pre-production testing. This used to store the build to be tested, so the build that can be tested by QA or Support should be obtained from here.

`RELEASE` released components or product images. This is where you can store builds that are ready for release or have been released. and builds on RBC will also be backuped here.

About 4 types of Arifactory repositories, all Product Members can R/W to Dev repo, but can only read from Int, Stage, and Release Repos. Server Accounts have can R/W to above repositories. Regarding to apply permission, need to create a RAC ticket to apply.

Base on above repositories, so the CI/CD workflow of our Aritafactory is like this.

* Jenkins Nightly or Pull Request build, if build success, the generated Artifacts will first be placed in the `INT` repo.
* Builds that passed Smoke Test or Manual confirmation of testable builds will be Promote from `INT` repo to `STAGE` repo. QA/Support The usual test build should be obtained from `STAGE`.
* Once the build passes all the tests and reaches the release state, it will build from `STAGE` Promote to `RELEASE` repo.
* The ready-to-package build is downloaded from the `RELEASE` repo, after the packaging is complete
   * Post to Both RBC sites. 
   * Then Upload the `RELEASE` repo for backup.

Any questions about this work process? 

## Second, define the Artifactory directory structure

### Unified branch naming rules

In order to better define the directory structure of Artifactory, and only with the expected directory structure, can it be easier to make the design of Jenkins CI/CD tools and rsmate clear. Here are our branch naming rules.

> Branch naming rules wiki: https://wiki.rocketsoftware.com/display/ML/Branch+naming+rules

The most important principle in this rule is that the branch type needs to be specified when creating a branch, such as `bugfix` `feature` `hotifx` `release` `diag`. In this way, when there are many branches, you can easily find the hotfix branch, and quickly know what a branch does

Not only is there a naming rule set here, but also Bitbucket's Hook is used to further implement the branch naming convention, so that non-compliant branches cannot be pushed to our product warehouse.

> Commit and Branch Specifications wiki https://wiki.rocketsoftware.com/display/ML/Commit+and+Branch+Specifications

### Artifactory directory structure and how the build flows

> Artifactory Directory Structure wiki https://wiki.rocketsoftware.com/display/ML/Artifactory+Directory+Structure

TODO: 插入结构图

By defining branch naming rules and a clear Artifactory directory structure, it helps anyone to easily find the build address corresponding to the branch he wants.

> Of course, you can also search the commit hash to find the Build you want to find https://wiki.rocketsoftware.com/display/ML/Artifactory+User+Guide#ArtifactoryUserGuide-Searchbuildthoughcommithash

When a build is created from Jenkins, it will first be placed in the `INT` repository. According to the name of its branch, it will be placed in a different directory. Each `/` will generate a directory .

For example, its branch is `hotfix/11.3.2.HF1` branch, then after the first build is successfully completed, it will be placed in `mvas-generic-int-den/uv113/hotfix/11.3.2.HF1/1/` dnder this directory.

> Among them, `uv113` not only indicates its version, but also the abbreviation of the name of their Git repo `uvuddb-uv113`, which is `uv113`. By analogy, the Git repositories corresponding to `ud82` `uv121` are `uvuddb-ud82` 和 `uvuddb` respectively.

If it is testable (build successful, Smoke Test passed, etc.), it will build promote to a higher maturity `STAGE` repo, except that the repo name is changed (from `mvas-generic-int-den` to `mvas-generic-stage-den`) Its directory structure remains unchanged, it will be `mvas-generic-stage-den/uv113/hotfix/11.3.2.HF1/1/`

Normally, this release may go through many builds before it is released. If the build passes all the tests during the fifth build, it is ready for release. At this time I will promote it from the `STAGE` repo to the `RELEASE` repo, and its directory becomes `mvas-generic-release-den/uv113//hotfix/11.3.2.HF1/5/`.

Then pack it. The packaged zip files will be published to both RBC sites, and they will also be saved to the Artifactory. `mvas-generic-release-den/RBC/UNV/v11.3.2.7001.HF1/` directory. This is also part of Backup Strategy.

After successful release, all other related `hotfix/11.3.2.HF1` builds under the `INT` 和 `STAGE` repositories will be deleted. In the end, only `mvas-generic-release-den/uv113//hotfix/11.3.2.HF1/5/` and `mvas-generic-release-den/RBC/UNV/v11.3.2.7001.HF1/` are retained builds.

TODO: 需要修改diagram里 RBC 的图例。

> Artifactory Work Process https://wiki.rocketsoftware.com/display/ML/Artifactory+Work+Process

# Backup Strategy

> U2 Infra Backup Strategy https://wiki.rocketsoftware.com/display/ML/U2+Infra+Backup+Strategy

Backing up some infrastructure is also a very important part of our products. Before 2020, Bill used three external hard drives for backup, including RBC, mvfile01 and Bamboo Server. However, after 2020, the company's security policy has changed, and no one can continue to use external hard drives. Although we elaborated on the reasons, we still did not get consent. Therefore, our backup strategy has changed accordingly.

For the infrastructure we need to back up, we divide them into two levels, level 1 and level 2, according to their importance.

## Level 1 Infrastructure includes

* RBC
* Denver Artifactory(This is because the current Denver Artifactory has not been completely taken over by IT.)
* den-mvfile01.u2lab.rs.com
* MV Bamboo Server
* U2 Jenkins Server

This level of infrastructure is that we cannot afford to lose data, so we perform maximum backup according to existing IT strategies and our resources.

For example, RBC stores the builds we delivered to customers for decades, but because IT backup only keeps files which are in 1 year old, but we need to keep all the data, we also exist in SharePoint, Denver Artifactory, den-mvfile01.u2lab.rs.com, and the data before 2020 is still in an external hard drive.

Denver Artifactory is the main place for building and backup in the future, but because it has not been completely taken over by IT, its backup strategy has not been finalized, so we still need to back up ourselves. The builds here are built from Jenkins except for the RBC (RBC we have made a proper backup on it), so as long as the code is in and Jenkins is in, we can build whatever we want build. Therefore, for Denver Artifactory, we only synchronize all the builds in its `STAGE`, `RELEASE` repositories to another Arifactory that we built for backup.

For den-mvfile01.u2lab.rs.com, all the Artifacts of other teams including MV U2, SB, wIntergrate, etc., including Builds, and releases of many years are also stored, so we also need to back up as much as possible. Currently, I manually back up the latest Artifacts to a 500 GB virtual machine every one to two weeks.

Next is MV Bamboo Server, which will upload the automatic backup of Bamboo to Self-created Artifactory once a week.

Finally, U2 Jenkins. Although our Jenkins uses Configuration as code, once this server crashes, the working directory of Jenkins can be restored more quickly if the server crashes. Therefore, regular backups are performed every week and the backup information is uploaded to Denver Artifactory

## Level 2 Infrastructure

Build machines 

* U2 Windows/Linux/Unix build machines 
* UCC Windows build machines 

This level of infrastructure is usually are build machines.

So, for all build machines, we have created snapshots for each build machine. And if the product build environment upgrade will need to take another snapshot to capture the previous build environment.

For Linux/Unix build machines, except for the very odl products build machine, most of machines we have knowlage how to set up a new build environment.











