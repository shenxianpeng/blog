---
title: "Jenkins Needs Java 21, Your Old Build Hosts Stop at Java 8: I Built Agent8"
summary: |
  Jenkins agents must run Java 21 too, so build hosts that stop at Java 8, such as AIX 7.1, Solaris and HP-UX, can no longer join a current Jenkins. Agent8 downgrades the official agent.jar to Java 8 so they keep working as ordinary agents.
tags:
  - Jenkins
  - Java
  - Agent8
authors:
  - shenxianpeng
date: 2026-10-16
series: ["My Open Source Projects"]
series_order: 6
---

Plenty of companies build their product on more than mainstream Linux. They also ship from AIX, HP-UX, Solaris and a set of RHEL 6 machines. These hosts have built releases for years, nobody wants to touch them, and they are Jenkins agents: every platform build comes from them.

The problem is that Java on those systems mostly stops at 8.

Jenkins, meanwhile, keeps raising its Java baseline: Java 11 from 2.361.1 LTS in 2022, Java 17 from 2.479.1 LTS in 2024, and today Java 21 or 25. The [Jenkins Java support policy][java-policy] is clear that the requirement applies to all components of the Jenkins system, **agents included**.

If your oldest build host can only run Java 8, the newest Jenkins it can join is 2.346.3, from August 2022. It has had no security fixes for a long time.

So teams end up picking one:

- Upgrade the controller. The security scan passes, and every AIX, HP-UX, Solaris and old RHEL agent can no longer connect.
- Don't upgrade. The old agents keep working, the whole Jenkins stays on a release nobody patches, and every audit needs an exception.

What many teams actually do is keep a second, old Jenkins just for those platforms, or build them by hand.

## What Agent8 is

[Agent8][agent8] does one thing: it lets a build host that only has Java 8 stay an ordinary Jenkins agent of a current controller on Java 21+.

How it works:

1. [JvmDowngrader][jvmdg] rewrites the official `agent.jar` to Java 8 bytecode ahead of time (Java 11 and 17 builds too).
2. Classes the controller sends to the agent during a build are downgraded as they load.
3. A small Java agent fixes what downgrading breaks: `serialVersionUID` values in serialization, the serial form of collections such as `List.of` that Java 8 does not have, and signed security providers on Solaris and IBM Java.

To the controller it is an ordinary agent: labels, executors, `sh`, file steps, `junit`, `stash`, aborts and the script console work as on any other node. The start command does not change either: still `java -jar agent.jar`.

## Check whether you need it first

Not every old host needs Agent8. Some have an easier route:

- **RHEL / CentOS 6 x86_64**: the OS repositories stop at OpenJDK 8, but Amazon Corretto 21 and Azul Zulu 21 run on CentOS 6.10, and the stock `agent.jar` connects to the current LTS with them. This route lasts until Jenkins requires Java 25 (Corretto 25 needs RHEL 7+).
- **AIX 7.2 TL5+ or 7.3 TL2+ on POWER8 or later**: install IBM Semeru 21 and run a normal agent.

Agent8 is for the rest: AIX 7.1, Solaris and HP-UX on Itanium, which have no Java 21 at all, and hosts whose JDK must not change, such as a certified or validated toolchain.

Which Java each platform can actually run, with sources, is in [this article][background].

## How to use it

On the build host, with its existing Java (8, 11 or 17) and the controller's URL:

```sh
curl -fsSLO https://raw.githubusercontent.com/keelinfra/agent8/main/install.sh
sh install.sh --url https://jenkins.example.com/ --replace /path/to/agent.jar
```

`install.sh` asks the controller for its remoting version, downloads the matching Agent8 jar, checks it against `sha256sums.txt`, test-starts it on the host's Java, and only then swaps it in for the old `agent.jar`. The old jar is kept as `agent.jar.before-agent8`, and `--restore` puts it back. Then restart the agent as usual.

The script sticks to POSIX `sh`, so it runs on old Unix systems. Hosts without internet access can copy the release files over and use `--from DIR`, and there is an Ansible playbook for fleets.

Releases are named after the Jenkins version: `jenkins-2.580.1` is for Jenkins 2.580.1. After upgrading the controller, rerun `install.sh`. Don't skip this: Jenkins keeps raising the oldest agent version it accepts, and Jenkins 2.586 already refuses the Agent8 build for 2.462.3.

## Where it stands

I want to be clear about this part:

| Build host | Java | Status |
|---|---|---|
| Linux, including RHEL/CentOS 6 | HotSpot 8 | Tested in CI |
| Linux (IBM Semeru, OpenJ9) | OpenJ9 8 | Tested in CI, best effort |
| Linux | HotSpot 11, 17 | Tested in CI (LTS) |
| AIX 7.1 / 7.2 | IBM Java 8 | Experimental |
| Solaris | Java 8, 11 | Installs and connects on real Solaris, experimental |
| HP-UX (Itanium) | Java 8 | Installs and connects on real HP-UX, experimental |

Every week CI runs against the latest LTS and weekly: Pipeline builds, Git checkout (JGit), `withCredentials`, aborts, an agent restart mid-build, and the script console.

Not verified yet: full builds on Solaris and HP-UX, real AIX hosts, and plugins that run their own code on the agent (Maven, Docker, artifact uploads, command-line git and so on). If you try it, get one job working on one host before moving the rest.

One more thing: **Agent8 is an independent project. It is not part of, or endorsed or supported by, the Jenkins project.** Please report problems on [Agent8's issues][issues], not the Jenkins issue tracker.

## What the community said

On October 13 I posted it on the [Jenkins community forum][thread], and within a few days got some very practical feedback:

- The Jenkins Platform SIG dropped OpenJ9 back in 2021, and J9 has a history of problems. On AIX, IBM Java 8 is often the only Java there is, so the README now says J9 support is best effort, with problems reported to Agent8.
- Amazon Corretto 21 still supports RHEL 6. I tested it on CentOS 6.10, the stock agent runs, and the README now recommends it first for RHEL 6 x86_64.
- Someone shared the old workaround: check out on Linux, scp the workspace to the old host, run the build over ssh, and copy the results back. It works, but parallel builds and aborts are yours to handle.

As with Keelhaven, much of this feedback was something I had not thought of myself.

## Free, with paid support available

Agent8 is MIT-licensed. Everything in the repository is free, with no gated features.

If you need more than that, such as a pilot on AIX, Solaris or HP-UX with us, a check of whether the plugins you use work on a Java 8 agent, or a tested build ready before every controller upgrade, see [keelinfra's pricing page][pricing]. Prices are fixed, and the first answer is free.

---

Project: https://github.com/keelinfra/agent8
Overview: https://keelinfra.io/jenkins/

If you have AIX, Solaris or HP-UX build hosts and can help verify builds, please open an [issue][issues] or email hello@keelinfra.io. If it's useful to you, a Star helps, and so does passing it on to anyone still looking after old build hosts.

[java-policy]: https://www.jenkins.io/doc/book/platform-information/support-policy-java/
[agent8]: https://github.com/keelinfra/agent8
[jvmdg]: https://github.com/unimined/JvmDowngrader
[background]: https://keelinfra.io/blog/jenkins-java-21-aix-rhel6-build-hosts/
[issues]: https://github.com/keelinfra/agent8/issues
[thread]: https://community.jenkins.io/t/keeping-java-8-build-hosts-aix-solaris-hp-ux-rhel-6-as-agents-of-a-current-jenkins/37378
[pricing]: https://keelinfra.io/jenkins/pricing/
