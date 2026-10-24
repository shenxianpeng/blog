---
title: Jira Is Moving to the Cloud. What Happens to Jenkins and Bitbucket?
summary: |
  Atlassian Data Center reaches end of life in March 2029, but Bitbucket and Bamboo are not on the list. What forces teams to move is Jira going to the cloud, which reopens the question of where the code lives. I set up Bitbucket DC 9.4 with Jenkins 2.541.3, switched multibranch jobs to Bitbucket Cloud, and wrote down what breaks and what doesn't.
tags:
  - Jenkins
  - Bitbucket
  - DevOps
authors:
  - shenxianpeng
date: 2026-10-24
---

Atlassian has announced that its Data Center products reach end of life on March 28, 2029. I assumed Bitbucket Data Center was part of that, and I said so in a few conversations. Then I went back to [Atlassian's announcement][eol] and found I was wrong.

## Get the timeline straight first

| Date | What happens |
|---|---|
| 2026-03-30 | New customers can no longer buy any Data Center product |
| Early 2027 | The Bitbucket Hybrid License opens to existing customers |
| 2028-03-30 | Existing customers can no longer buy new Data Center subscriptions or expansions |
| 2029-03-28 | Jira and Confluence DC go read-only; Bitbucket and Bamboo DC also go read-only unless moved to the Hybrid License |

Bitbucket and Bamboo DC are not on the end-of-life list. The [Hybrid License page][hybrid] says "Bitbucket and Bamboo Data Center will not end of life and will continue beyond the Data Center end of life in 2029". With the Hybrid License, one subscription covers Bitbucket DC, Bamboo DC and Bitbucket Cloud with Pipelines. Pricing is not published. Without it, the FAQ on the same page says DC switches to read-only after 2029-03-28 and you can no longer push.

So "Bitbucket DC is ending, everyone has to move" is not true. What gets teams moving is Jira and Confluence: they have to go to the cloud or be replaced, and once Jira is in the cloud, whether the code should follow becomes a question nobody can dodge.

## Three paths

1. **Stay on Bitbucket DC with the Hybrid License.** Not a single line of Jenkins changes. This fits teams whose code has to stay in their own data center. The costs: the price is unknown, and with Jira in the cloud and code on premises, the integration between them has to be rebuilt.
2. **Move to Bitbucket Cloud.** The smoothest integration with Jira Cloud, and it is already included in the Hybrid License.
3. **Use the occasion to switch to GitHub or GitLab.** [GitHub Enterprise Importer][gei] moves Bitbucket Server/DC repositories to GitHub Enterprise Cloud along with pull requests, comments and reviews.

On the CI side, all three vendors offer a way off Jenkins: GitHub has Actions Importer, Atlassian released a [Jenkins to Bitbucket Pipelines migration tool][bbp] in January 2025 (it converts only plugins used by more than 5% of instances and copies the rest over for manual review), and GitLab has a [migration guide][gitlab]. These tools convert how a Jenkinsfile is written. Shared libraries, niche plugins, fixed build machines and internal deployment targets still need a person. In [JetBrains' 2025 State of CI/CD survey][jb], 32% of organizations use two CI tools and 9% use three or more.

My advice is to change one thing at a time: move the code first and keep Jenkins running, then decide about CI once things are stable. Everything below is about that first step.

## How I tested

- Bitbucket Data Center 9.4.26 from the official Docker image, with the [3-hour test license][timebomb] Atlassian provides to app developers.
- Jenkins 2.541.3 (the last LTS that supports Java 17), [Bitbucket Branch Source][bbs] 937.3.10, and Atlassian's [Bitbucket Server Integration][bsi] 6.0.2.
- One repository with two branches; `test/Jenkinsfile` has three stages that only echo.
- On the Cloud side, the public repository [atlassian/jenkins-job-trigger][cloudrepo] on bitbucket.org, with the same branch names and Jenkinsfile path as the DC copy, scanned anonymously.

## First break: Atlassian's own plugin doesn't support Cloud

Bitbucket Server Integration is the Jenkins plugin Atlassian publishes. Point it at bitbucket.org and validation fails right away:

```text
This plugin does not support connecting to bitbucket.org. It is for Bitbucket Server instances only.
```

Every job built on this plugin has to move to Bitbucket Branch Source or the Git plugin. The two plugin names are close enough that people often treat them as the same thing.

## Second break: app passwords are gone, and API tokens need a newer plugin

Bitbucket Cloud stopped creating new app passwords on September 9, 2025 and [disabled all of them on June 9, 2026][apppw]. The replacement is a scoped API token.

Bitbucket Branch Source supports API tokens starting with 937.0.0 ([JENKINS-75772][75772]), which requires Jenkins 2.504.1 or newer. Using update center version data, here is the newest release each LTS can install:

| Jenkins LTS | Newest Bitbucket Branch Source | API token support |
|---|---|---|
| 2.346.3 | 805.v7f97d29dc0f5 | No |
| 2.426.3 | 888.v8e6d479a_1730 | No |
| 2.462.3 | 912.v3b_f74026941c | No |
| 2.479.3, 2.492.3 | 936.4.3 | No |
| 2.504.3 to 2.528.3 | 937.3.0 | Yes |
| 2.541.3 | 937.3.10 | Yes |

On Jenkins 2.492.3 or older, using API tokens with Bitbucket Cloud means upgrading Jenkins first. 2.462.3 is the last LTS that runs on Java 11, so older controllers face a chain: upgrade Java, upgrade Jenkins, update the plugin, and only then move the code. Two more API-token fixes, for fork PR fetches failing and for read-only users seeing an empty repository list, landed in 937.3.3 and 937.3.5, which need Jenkins 2.541.3.

Older plugin versions still support OAuth consumers, which could serve as a stopgap. I did not test that.

One more trap. With the same API token, [the REST API wants your Atlassian account email as the username, while Git over HTTPS wants your Bitbucket username][apitoken] or the static `x-bitbucket-api-token-auth`. The Branch Source docs say to put the email in the credential and let the plugin handle checkout. If you also have freestyle jobs or `git` steps that clone through the Git plugin directly, those need the username. Many community posts about "the API token lists repositories but clone fails" come down to this.

## What didn't break: build history

I expected that changing the source would recreate branch jobs and restart build numbers at 1. It didn't, but two cases need care:

| How you change it | Branch jobs and build history | Does it trigger builds? |
|---|---|---|
| Edit the existing source's server and repository (source ID unchanged) | Kept, numbering continues | Not if the commits are unchanged |
| Delete the old source and add a new one (new source ID) | Kept; the log says `Takeover ... from source that no longer exists` | Every branch builds once (`Branch reopened`) |
| Attach old and new sources to the same job | Same-named branches from the new source are ignored: `Ignoring ... as source #1 owns the branch name` | No |

The second case turns into a build storm on a repository with many branches: hundreds of branches queue at once. So in the Jenkins UI, edit the existing source rather than deleting and re-adding it. Running old and new side by side inside one job doesn't work either; for a parallel run, create a separate job.

The test machine's network doesn't allow git to reach bitbucket.org directly, so the builds after switching to Cloud all failed at `git fetch`. That doesn't affect the results above, which are about jobs and numbers, not build outcomes. The "no rebuild when commits are unchanged" result comes from a second DC repository with identical commits.

## Take inventory before moving

Before making any of these changes, you need to know which jobs talk to Bitbucket. Run this in the Script Console to list every job and global configuration file that references your Bitbucket address:

```groovy
// Manage Jenkins > Script Console
def needle = "bitbucket.example.com"   // your Bitbucket DC host
def j = jenkins.model.Jenkins.get()
j.getAllItems(hudson.model.Item).each { item ->
  if (item.parent instanceof jenkins.scm.api.SCMSourceOwner) return  // branch jobs follow their multibranch parent
  if (item.configFile.asString().contains(needle)) println "job: ${item.fullName}"
}
// Global configuration: shared libraries, Bitbucket endpoints, etc.
new File(j.rootDir.path).listFiles().findAll { it.name.endsWith(".xml") && it.text.contains(needle) }.each {
  println "global: ${it.name}"
}
return
```

On the test Jenkins I added a freestyle job and a Pipeline with a hard-coded git URL; the script found both, plus the global Bitbucket endpoint configuration. It cannot see Jenkinsfiles or shared library code stored in repositories; search the code for those.

The Bitbucket side also depends on Jenkins: merge checks ("builds must pass" relies on the status Jenkins reports back), webhooks, service accounts and SSH keys.

Finally, the network flips direction. Bitbucket and Jenkins used to share an internal network. Once the code is in the cloud, cloud webhooks have to reach your internal Jenkins (allow [Atlassian's IP ranges][ips], add a relay, or fall back to periodic scanning), and every agent needs outbound access to fetch code.

## What I didn't test

- Private Bitbucket Cloud repositories with an API token. I didn't use a real account; the test scanned a public repository anonymously.
- Moving to GitHub. The test environment couldn't reach the GitHub API, so GitHub Branch Source wasn't covered.
- Whether git and OpenSSH on old machines such as AIX or Solaris can connect to bitbucket.org. The test environment goes out through a proxy, so the result wouldn't mean anything.

If you are planning a Jira cloud migration and Jenkins is also yours to run, I'd like to hear in the comments how you plan to handle the code and CI.

[eol]: https://www.atlassian.com/licensing/data-center-end-of-life
[hybrid]: https://www.atlassian.com/migration/bitbucket-hybrid-license
[gei]: https://docs.github.com/en/migrations/using-github-enterprise-importer/migrating-from-bitbucket-server-to-github-enterprise-cloud/about-migrations-from-bitbucket-server-to-github-enterprise-cloud
[bbp]: https://www.atlassian.com/blog/bitbucket/general-availability-of-the-jenkins-to-bitbucket-pipelines-migration-tool
[gitlab]: https://docs.gitlab.com/ci/migration/jenkins
[jb]: https://blog.jetbrains.com/teamcity/2025/10/the-state-of-cicd/
[timebomb]: https://developer.atlassian.com/platform/marketplace/timebomb-licenses-for-testing-server-apps/
[bbs]: https://plugins.jenkins.io/cloudbees-bitbucket-branch-source/
[bsi]: https://plugins.jenkins.io/atlassian-bitbucket-server-integration/
[cloudrepo]: https://bitbucket.org/atlassian/jenkins-job-trigger
[apppw]: https://www.atlassian.com/blog/bitbucket/bitbucket-cloud-enters-phase-2-of-app-password-deprecation
[75772]: https://issues.jenkins.io/browse/JENKINS-75772
[apitoken]: https://support.atlassian.com/bitbucket-cloud/docs/using-api-tokens/
[ips]: https://support.atlassian.com/bitbucket-cloud/docs/what-are-the-bitbucket-cloud-ip-addresses-i-should-use-to-configure-my-corporate-firewall/
