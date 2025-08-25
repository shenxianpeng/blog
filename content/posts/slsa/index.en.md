---
title: The SLSA Framework and Software Supply Chain Security Protection
summary: This article introduces the concept, purpose, and levels of the SLSA framework, and how to apply SLSA in the software supply chain to improve security. It helps readers understand the importance of SLSA in software development and deployment.
tags:
  - SLSA
author: shenxianpeng
date: 2023-03-23
---

With the increasing number of attacks targeting software supply chains in recent years, Google has released a series of guidelines to ensure the integrity of software packages, aiming to prevent unauthorized code modifications from affecting the software supply chain.

Google's SLSA framework (Supply-chain Levels for Software Artifacts) provides recommendations for achieving more secure software development and deployment processes by identifying and mitigating issues in CI/CD pipelines.

## Table of Contents

1. [What is SLSA](#what-is-slsa)
2. [Problems in the Software Supply Chain](#problems-in-the-software-supply-chain)
2.1 [What are Supply Chain Attacks?](#what-are-supply-chain-attacks)
2.2 [Real-world Examples](#real-world-examples)
3. [SLSA Levels](#slsa-levels)
3.1 [Detailed Explanation](#detailed-explanation)
3.2 [Limitations](#limitations)
4. [SLSA Implementation](#slsa-implementation)
5. [Other Tools](#other-tools)

## What is SLSA

[SLSA](https://slsa.dev/) stands for Supply chain Levels for Software Artifacts, or SLSA (pronounced "salsa").

SLSA is an end-to-end framework, a standard and checklist of controls to ensure the security of software building and deployment processes, preventing threats arising from tampering with source code, build platforms, and component repositories.

## Problems in the Software Supply Chain

Any software supply chain can introduce vulnerabilities. As systems become increasingly complex, it becomes crucial to implement best practices to ensure the integrity of delivered artifacts. Without certain standards and systematic development plans, it is difficult to cope with the next hacker attack.

### What are Supply Chain Attacks?

![Supply Chain Threats](supply-chain-threats.png)

A Submitting unauthenticated modifications
B Leaking the source code repository
C Building from modified source code
D Leaking the build process
E Using compromised dependencies
F Uploading modified packages
G Leaking the package repository
H Using compromised packages

### Real-world Examples

| Integrity Threat | Known Example | How SLSA Helps |
|-----------|---------|-------------------|
| A Submitting unauthenticated modifications | Researchers attempting to introduce vulnerabilities into the Linux kernel via patches on the mailing list. [Research](https://lore.kernel.org/lkml/202105051005.49BFABCE@keescook/) | Two-person review caught most (but not all) vulnerabilities. |
| B Leaking the source code repository | [PHP](https://news-web.php.net/php.internals/113838): Attackers compromised PHP's self-hosted git server and injected two malicious commits. | A better-protected source code platform would make it more difficult for attackers to succeed. |
| C Building from modified source code | [Webmin](https://www.webmin.com/exploit.html): Attackers modified the build infrastructure to use source files that didn't match source control. | SLSA compliant build servers generate provenance to identify the actual sources used, enabling consumers to detect such tampering. |
| D Leaking the build process | [SolarWinds](https://www.crowdstrike.com/blog/sunspot-malware-technical-analysis/): Attackers compromised the build platform and installed implants that injected malicious behavior during each build. | Higher SLSA levels require stronger security controls on the build platform making compromise and gaining persistence more difficult. |
| E Using compromised dependencies | [event-stream](https://web.archive.org/web/20210909051737/https://schneider.dev/blog/event-stream-vulnerability-explained/): Attackers added a seemingly harmless dependency, then updated that dependency to add malicious behavior. The update didn't match the code submitted to GitHub (i.e., attack F). | Recursively applying SLSA to all dependencies blocks this specific vector because provenance would show it wasn't built by the proper builder or the source wasn't from GitHub. |
| F Uploading modified packages | [CodeCov](https://about.codecov.io/apr-2021-post-mortem/): Attackers used leaked credentials to upload malicious artifacts to Google Cloud Storage (GCS) from which users could download directly. | Provenance of artifacts in GCS showed the artifacts weren't built from the expected source code repository in the expected way. |
| G Leaking the package repository | [Attacks on package mirrors](https://theupdateframework.io/papers/attacks-on-package-managers-ccs2008.pdf): Researchers ran mirrors for several popular package repositories, which could be used to serve malicious packages. | Similar to (F) above, the provenance of malicious artifacts would show they weren't built as expected nor from the expected source code repository. |
| H Using compromised packages | [Browserify typosquatting](https://blog.sonatype.com/damaging-linux-mac-malware-bundled-within-browserify-npm-brandjack-attempt): Attackers uploaded a malicious package with a similar name to the original. | SLSA doesn't directly address this threat, but linking provenance back to source control enables and enhances other solutions. |

## SLSA Levels



| Level | Description | Example |
|-----|------|------|
|1 | Documentation of the build process | Unsigned provenance |
|2 | Tamper-resistant build service | Hosted source/build, signed provenance |
|3 | Additional resistance to specific threats | Security controls on the host, unforgeable provenance |
|4 | Highest level of confidence and trust | Two-person review + hermetic build |

### Detailed Explanation

| Level | Requirements |
|-----|------|
|0 | No guarantees. SLSA 0 indicates a lack of any SLSA level. |
|1 | **The build process must be fully scripted/automated and generate provenance.** <br>Provenance is metadata about how an artifact was built, including the build process, top-level source, and dependencies. <br>Understanding provenance allows software consumers to make risk-based security decisions. <br>SLSA 1 Provenance doesn't prevent tampering, but it provides a basic level of code origin identification and helps with vulnerability management. |
|2 | **Requires version control and a hosted build service that generates authenticated provenance.** <br>These additional requirements give software consumers more confidence in the software's origin. <br>At this level, provenance is tamper-resistant to the degree that the build service is trusted. <br>SLSA 2 also provides an easy path to upgrade to SLSA 3. |
|3 | **Source and build platforms meet specific standards to guarantee source auditability and provenance integrity, respectively.** <br>We envision a certification process where auditors can attest that platforms meet requirements, which consumers can then trust. <br>SLSA 3 provides stronger tamper resistance than earlier levels by preventing specific classes of threats (e.g., cross-build contamination). |
|4 | **Requires two-person review of all changes and a hermetic, reproducible build process.** <br>Two-person review is an industry best practice for finding errors and preventing malicious behavior. <br>Hermetic builds guarantee the dependency list of the provenance is complete. <br>Reproducible builds, while not strictly required, provide numerous auditability and reliability benefits. <br>Overall, SLSA 4 gives consumers high confidence that the software hasn't been tampered with. |

### Limitations

SLSA can help reduce supply chain threats in software artifacts, but it also has limitations.

* Many artifacts have a large number of dependencies in the supply chain, and the complete dependency graph can be very large.
* Teams actually doing security work need to identify and focus on important components in the supply chain. This can be done manually, but the workload can be significant.
* The SLSA level of an artifact is not transitive and dependencies have their own SLSA rating, meaning that an SLSA 4 artifact can be built from SLSA 0 dependencies. Therefore, while the main artifact has strong security, there may still be risks elsewhere. The sum of these risks will help software consumers understand how and where to use SLSA 4 artifacts.
* While automation of these tasks would help, a full review of the entire graph for every software artifact for every consumer isn't practical. To bridge this gap, auditors and certification bodies can verify and attest that something meets SLSA requirements. This might be particularly valuable for closed-source software.

As part of the SLSA roadmap, the SLSA team will also continue to explore how to identify important components, how to determine the overall risk of the entire supply chain, and the role of certification.

## SLSA Implementation

SLSA is a standard, but how do we implement it?

We can use the summary table of SLSA [Requirements](https://slsa.dev/spec/v0.1/requirements) to check one by one and see which security level our current CI/CD workflow is at.

Are there tools that can better help us check and guide us on how to improve the security level?

Currently, there are only a few tools that can achieve this, and the vast majority are limited to GitHub.

[OpenSSF Scorecard](https://github.com/ossf/scorecard) is an automated tool from the Open Source Security Foundation (OpenSSF) for checking security metrics of open-source software. It helps open-source maintainers improve their security best practices and helps open-source consumers judge whether their dependencies are secure.

It does this by assessing many important projects related to software security and assigning a score of 0-10 to each check. You can use these scores to understand specific areas that need improvement to strengthen the security posture of the project.  It can also assess risks introduced by dependencies and make informed decisions about accepting those risks, assessing alternative solutions, or collaborating with maintainers to make improvements.

## Other Tools

* [slsa-verifier](https://github.com/slsa-framework/slsa-verifier) - Verifies build provenance compliant with SLSA standards
* [Sigstore](https://github.com/sigstore) - A new standard for signing, verifying, and securing software

---

Please indicate the author and source when reprinting this article. Please do not use it for any commercial purposes. Welcome to follow the WeChat public account "DevOps攻城狮".