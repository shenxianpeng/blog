---
title: About Artifactory and Infrastructure backup strategy
tags:
  - Infrastructure
  - Artifactory
  - Backup
categories:
  - DevOps
date: 2020-09-25 17:26:03
author: 
---


Hello everyone, this is Xianpeng. On our last inter locking meeting, I have shared about MVAS team Jenkins best pracitce, due to time constraints, two topics are left, they are about Artifactory and Infrastructure backup strategy. so I'd like share with you in today's meeting.

# Artifactory

As you all know MV Products builds were put on a FTP server which is den-mvfile01 

Use this FTP to store and management build has some disadvatanges 

* first, we management and backup ourself and it only have 500 GB space for all MV team. we want to extand space but it;s a legacy machine, which IT not extand space anymore.

* second, ftp login user and password are extra separate, which was management in a Jira ticket which need to manually mantaince to add/move new joiner and left rocket guys.

When better product DevOps tools appear, it's easy to see what the disadvatanges of FTP are. compare with Artifactory

* It is not so easy to implement CI/CD with FTP.
* There is no good mechanism to clean up the build and backup regularly

As the more types of products to be managed increase, such as Maven, Docker packages, there is a greater need for a tool to manage all Artifcts. Obviously, traditional methods like FTP cannot be satisfied.

Artifactory is a very popular and powerful tool in the current DevOps tool chain, and it is also one of the tools in Rocket's unified tool chain planning. 

Using it to manage our products artifacts will bring the following advantages:


* very power REST API for interation with CI tools.
* Support the storage of multi-language product artifacts, such as Maven, Docker to reduce maintenance costs caused by the use of multiple tools
* Searching for artifacts based on different criteria 

---

*	Offline access to artifacts and metadata
*	Long and network intensive build processes
*	Security and access control
*	Sharing internal and external artifacts
*	Binary version tracking to reproduce builds
*	Searching for artifacts based on different criteria
*	Stability and reliability of systems hosting artifacts
*	Ensuring compliance with a variety of license requirements
*	Customized handling of artifacts

At present, all of U2 Jenkins automated build tasks have been uploaded to Artifactory. Please allow me to demonstrate how Denver Aritfactory works with Jenkins.

### Login to Artifadctory

#### Home

Open Rocket Denver Aritifactory, use my personal account to login.

From the Homepage, we can recently deploy aritifacts to this the Aritifactory, and this part the most downloaed Artifacts here.

and these part is about user guide, Webinar, REST API document, etc.

Let's move to the sencond tab, **Artifacts**

#### Artifacts

In this table list all Denver Artifactory repositories. You could see there are two teams in this Artiactory. I'm the mvas product member and I have favorited the repositires I care, so click this button will list all my favorite repostires.

we used generic type repositores to store UV/UD/UCC/UNDK products. once we need docker will create docker type repository.

From the repository naming rule, you could find it is following some naming conversion which is JFrog recommended repository naming structure. they are made of <team>-<technology>-<maturity>-<locator>

* product or team - name as the primary identifier of the project
* technology - tool or package type being used.
* package maturity level, such as development, integration, staging and release stages. 
* locator is the physical topology of your artifacts.

Every technology will have 4 repositories, the name different is the maturity level part, here I just called them in short of DEV, INT, STAGE, and RELEASE.

`DEV` open access for developers, it used for developers to store some libs or 3rdParty binary files. our Jenkins weeekly backup is saved here.

`INT` used by CI builds for store the Jenkins automated build. if build successful, the build will apprear in this repo, if not. does not upolod build to here.

`STAGE` pre-production testing. In theory, Only the build passed somke test will be promote from `INT` repo to this `STAGE` repo. or sometimes it is manually confirmed that it is ready to test. so QA or Support should get build from the `STAGE` repo.

`RELEASE` repo store the released builds. one build passed all the testing and ready to release, will promote the build from `STAGE` repository to this `RELEASE` repository. Buy the way, posted to RBC products build like UV, UD, UCC, UNDK will also be saved to this repo for backup. 

Base on the repo maturity has different access permission. for `DEV`, all product members has R/W permission. but for  `INT`, `STAGE`, `RELEASE` repos, products member also has read pession, so they can only download build. 

For service account they have R/W pemssion to all maturity level repos.

TODO：about Admini permission and retention policies haven't been finalized, it's not yet fully supported by IT

To better mamangent the directory and straight forward for interation with CI tools and rsmate, we have many discusstions in the team and we need to define and unify the branch naming conversions.

Refer to Bitubcket naming conversion, our regular branch starts with `bugfix/`, `diag/`, `feature/`, `hotifx/`, `release/`, so when we build a branch,

different type branch build will appears to different folders. take a look at the Artifactory, you could see `bugfix`,  `diag`, `feature`, `hotifx`, `release` will the branch start with these word, `*-dev` folders. `PRs` folder is used to store out Pull Request builds here.

As you konw, we have enabled Bibuket hooks to standardize commit message and branch naming, so any commit message not meet the our conventions will not allowed to push to our Bitbucket remote repositories.

take Unidata 8.2.2 Release as a example, before relese, there is a new branch named `release/8.2.2` was be created. 

Jenkins build will be deploy package to `INT` repo, then it will be promote to `STAGE` repo when pass the smoke test, the the build is ready to realse, will promote the build from `STAGE` to `RELEASE` repo.

for this build you could see it has some properties, `build.status` was added when it build success, `smoketest.status` was added when passed smoke test. they all automaticly by Jenkins job.

`release.status`, `polaris.scan`, `blackduck.scan` were manullay added for demo, properties is not only for collection information, but also for search.

> Artifactory Directory Structure wiki https://wiki.rocketsoftware.com/display/ML/Artifactory+Directory+Structure \
> search build by commit hash https://wiki.rocketsoftware.com/display/ML/Artifactory+User+Guide#ArtifactoryUserGuide-Searchbuildthoughcommithash \
> Artifactory Work Process https://wiki.rocketsoftware.com/display/ML/Artifactory+Work+Process

## Backup Strategy

> U2 Infra Backup Strategy https://wiki.rocketsoftware.com/display/ML/U2+Infra+Backup+Strategy

Next is our infratucture backup strategy. from the business continuity /ˌkɑːntɪˈnuːəti/ perspective, backup is a very important part of our products.

Before I take build engineer work, we have RBC, den-mvfile01 and Bamboo server need to backup. before 2020, we used three external hard drives for backup. 

Before 2020, we used three external hard drives for backup, including RBC, mvfile01 and Bamboo Server. 

In 2020 execpt this three infra need to backup, we have Jenkins and Denver Artifctory (this is because which is not full take over by IT, for save we'd best to backup)

However, from this year, the company's security policy has changed, and no one can continue to use external hard drives. 

Our backup methods should also be adjusted accordingly. In the current restricted backup strategy, there is no absolutely safe method, but from the perspective of business continuity, we need to ensure relative security, so we have done cross backup. In this case, unless all Rocket's infrastructure is destroyed at the same time otherwise our data is safe.

Different important levels of infrastructure should adopt different backup strategies. Here I divide this kind of infrastructure into two levels, level one and level two.

* For the level one infrastructure, we must ensure data security. 
* For the level second infrastructure, we only need to ensure that it can be rebuilt once it is destroyed.

First I talk about level infratuctures.

* RBC is the most important for MV, it store all teams products build to customer, but IT only backup last one year data, this is not enough to us, we need backup all the year data, so we backup it to SharePoint, mvfile01 and Denver Artifactory.

* mvfile01 is store our test build and released build

* Some team's CI build still on Bamboo server, so we need also keep to backup. I have make this backup method from manual to auto.

* Jenkins is our new infrature, even though we used configuration as code, but if we save the Jenkins workspace, it also very help to quickly rebuild a new server site once current server destory.

* For my Rocket Denver Artifactory, I asked a few months ago, it still not fully take over by IT, so we'd best to backup ourself, so I create a auto job to dailly backup to a self-host artifactory.

Next, level 2 infratuctures is about build machines. for currently products build machines we have knowlage to know how to set up a new build environment. and we will create new snapshot once the build env has upgrade.

For the legacy build machines, we create a daily monitor job to watch it's status, if it was power off or deleted. these build machines is in planning try to migrate, some machines that we don't has same os verions, need to be keeped.










