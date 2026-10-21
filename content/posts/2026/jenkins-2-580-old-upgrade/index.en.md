---
title: "Old Jenkins Straight to 2.580.1: 12 LTS Lines Fail to Start, Online or Not"
summary: |
  Jenkins 2.580.1 no longer bundles the plugins that were split out of core. I replaced only the core of 38 old LTS controllers with 2.580.1, and from 12 of them Jenkins did not start, with or without the update center. What the log looks like, why it happens, and how to upgrade an old controller instead.
tags:
  - Jenkins
  - Troubleshooting
authors:
  - shenxianpeng
date: 2026-10-21
---

Jenkins 2.574 and 2.577 removed the plugins that were split out of core over the years from `jenkins.war`, such as Instance Identity, SSH server and JAXB. 2.580.1 is the first LTS release without them.

The [2.580.1 upgrade guide][guide] says most instances are not affected: if the update center is reachable, Jenkins installs what is missing, and only offline instances need to do anything.

I wanted to see what happens to a controller that has not been upgraded for a few years, so I rehearsed the upgrade from every LTS line. The result does not match the guide.

## How I tested

- **Starting points:** the last release of 38 LTS lines, from 2.60.3 to 2.568.3. In the March 2026 Jenkins usage statistics, these lines run on 79% of the 234,780 controllers that reported.
- **Plugins:** the 100 and the 300 most installed plugins, each at the newest release that line can load. That is the good case: an administrator who kept plugins up to date.
- **Core only:** the same plugin files, with only the war (or the package, or the image) replaced by 2.580.1. Jenkins starts as an upgrade from the old version, in a container with no network.
- **Step by step:** the same controller upgraded through intermediate LTS releases (2.346.3, 2.462.3 and 2.541.3 as needed), with plugins updated at each stop.

Every starting point was also started on its own version first, to check the baseline. A full run is 328 Jenkins starts, all in the official Docker images.

## Results

| | 100 plugins | 300 plugins |
|---|---|---|
| Core only: Jenkins does not start | 0 / 38 | 12 / 38 |
| Core only: starts, some plugins fail or load in part | 21 / 38 | 12 / 38 |
| Step by step: every stop loads cleanly | 38 / 38 | 38 / 38 |

Some starting points already had a plugin that did not load before the upgrade (2 with 100 plugins, 5 with 300); they are counted in the second row.

Every problem the upgrade itself caused started from 2.346.3 or older:

- With 300 plugins, Jenkins did not start from the 12 lines 2.164.3 to 2.277.4 and 2.319.3 to 2.346.3.
- With 100 plugins it always started, but from 2.319.3 to 2.346.3 the GitHub and SSH server plugins loaded only in part.

In the usage statistics, 10.8% of controllers still run 2.346.3 or older.

## What the log looks like

Right after the upgrade message, Jenkins reports that it installed nothing:

```text
Upgrading Jenkins. The last running version was 2.346.3. This Jenkins is version 2.580.1.
Upgraded Jenkins from version 2.346.3 to version 2.580.1. Loaded detached plugins (and dependencies): []
```

Before 2.577, that list held the split plugins the controller was missing, installed from copies inside the war. Now the copies are gone. Plugins built against an old core depend on the split plugins only optionally, so they still load, and fail later, when Jenkins looks up their extensions:

```text
Failed to create Guice container from all the plugins
java.lang.ClassNotFoundException: org.jenkinsci.main.modules.instance_identity.InstanceIdentity
```

Worse, when Jenkins does not start, the last error names a plugin that is not the cause, and not always the same one. In my runs it named Bitbucket Server Integration, Kubernetes Credentials Provider and Git:

```text
SEVERE hudson.util.BootFailure#publish: Failed to initialize Jenkins
java.lang.IllegalArgumentException: Unable to inject class com.atlassian.bitbucket.jenkins.internal.jenkins.auth.OAuthFilterRegistrar
```

Reading the 2.580.1 code, there are two layers. First, Bitbucket Server Integration 3.3.2 uses Instance Identity classes without declaring the dependency, and when Guice builds its container it hits that class and fails as a whole. Second, after Guice fails, a fallback tries again with core's extensions only. But that fallback does not bind the `Jenkins` object, and a core extension injects it, so the fallback always fails too. From then on every initializer that needs injection fails, and the error names whichever plugin runs first.

The smallest reproduction I found is Bitbucket Server Integration 3.3.2 and its dependencies, 60 plugins. 3.3.2 is the newest release that installs on 2.346.3.

I also searched the class files of the 300 plugins: at the newest releases for 2.346.3, 7 of them use Instance Identity classes without declaring the dependency, including the widely used Mailer and GitHub plugins.

## The update center does not help

I ran the 2.346.3 and 2.277.4 upgrades again with network access, after checking from the same image that `updates.jenkins.io` answered.

Same result: no split plugin was downloaded, and Jenkins did not start. From the code, Jenkins adds split plugins from the update center only when you install a plugin through the plugin manager. Nothing downloads them when Jenkins starts after a core upgrade.

## How to upgrade an old controller

First, find out which version the controller last ran:

```sh
cat "$JENKINS_HOME/jenkins.install.InstallUtil.lastExecVersion"
```

If it is 2.356 or older, do not jump straight to 2.580.1. Either of these worked in my tests.

**Step through an older LTS release.** Upgrade to an LTS release that still bundles the split plugins (2.568.3 or earlier), start it once so it installs them, update all plugins in the plugin manager, then go on. This is the path that loaded cleanly from all 38 starting points.

Do not skip the plugin update at the intermediate stop. When I upgraded 2.346.3 to 2.568.3 core only without updating plugins, the SSH server plugin did not load, because its newly installed dependencies needed a newer SSH Credentials plugin.

**Install the split plugins with their dependencies before starting 2.580.1.** `jenkins-plugin-cli` ships in the official image:

```sh
jenkins-plugin-cli --jenkins-version 2.580.1 --plugins instance-identity \
  --plugin-download-directory /tmp/split
```

It downloads Instance Identity and the newer bouncycastle API it needs. Copy both into `$JENKINS_HOME/plugins`, replacing the older files of the same plugins.

Copying `instance-identity.jpi` alone does not work: it needs a newer bouncycastle API than a 2.346.3 controller has. From 2.277.4 or older, more plugins are missing. In my 300-plugin test, placing them created a dependency cycle with older plugins, and 213 of 307 plugins did not load. There I would step through an intermediate LTS release.

The version each plugin was split out of is listed in [`split-plugins.txt`][split].

Whichever way you choose, rehearse the upgrade on a copy of `JENKINS_HOME` before touching the real controller. A controller that does not start is much easier to deal with on a copy.

## What I have not done

The fallback problem above comes from reading the code; I have not changed core to verify a fix. The plugin sets come from install counts, not from real controllers, and have no jobs, credentials or agents, so a real controller may hit other problems.

The full results for every starting version, including which plugins failed, are at [keelinfra.io/jenkins/upgrade-matrix][matrix].

[guide]: https://www.jenkins.io/doc/upgrade-guide/2.580/
[split]: https://github.com/jenkinsci/jenkins/blob/master/core/src/main/resources/jenkins/split-plugins.txt
[matrix]: https://keelinfra.io/jenkins/upgrade-matrix/
