---
title: Where Does Your Software Really Come From?
summary: This article introduces provenance for software artifacts, emphasizing the importance of securing the process of transforming code into artifacts throughout the software development lifecycle, and introduces the SLSA project and Sigstore's role.
tags:
  - SLSA
  - DevSecOps
author: shenxianpeng
date: 2024-06-13
---

Software is a fascinating and deeply mysterious thing. It’s composed of seemingly magical snippets of code that run on end-user machines, yet it’s not alive, but it has a lifecycle.

Software begins as source code, merely text files sitting in a repository somewhere.  Then, through a unique build process, this source code is transformed into something else.  For example, compressed JavaScript bundles delivered to a web server, container images containing framework code and business logic, or raw binary files compiled for a specific processor architecture.

This final transformed form—the thing that’s created from source code—is generally referred to as a “software artifact.” After creation, artifacts usually sit dormant, waiting to be used. They might reside in a package registry (like npm, RubyGems, PyPI, etc.) or a container registry (like GitHub Packages, Azure Container Registry, AWS ECR, etc.), attached as binaries to a GitHub release, or just sitting as a ZIP file in some blob storage service.

Eventually, someone decides to pick up that artifact and use it. They might unzip it, execute the code, start the container, install the driver, update the firmware—whatever the case, the completed software starts running.

This marks the culmination of a production lifecycle that may involve substantial human effort, significant financial investment, and, given the modern world’s reliance on software, critical importance.

However, in many cases, we can’t fully guarantee that the artifact we run is the artifact we built.  The details of the artifact’s journey are either lost or obscured, making it difficult to connect the artifact back to its source code and build instructions.

This lack of visibility into the artifact lifecycle is at the root of many of today’s most serious security challenges.  There are opportunities throughout the software development lifecycle (SDLC) to secure the process of transforming code into artifacts—eliminating the risk of threat actors compromising the final software and causing significant harm.  Some cybersecurity challenges might seem impossibly difficult to successfully address, but this is not one of them. Let’s dive into some background.


## Hashes and Signatures

Let’s say you have a file in your directory, and you want to make sure that it’s exactly the same tomorrow as it is today. How do you do that? A good way is to generate a hash of the file using a secure hashing algorithm.

Here’s how you do that using OpenSSL and the SHA-256 algorithm:

```bash
openssl dgst -sha256 ~/important-file.txt
```

Now you have a hash (also known as a digest), a 64-character string of letters and numbers that represents a unique fingerprint for that file.  Change anything in that file, then run the hash function again, and you’ll get a different string. You can write the hash down somewhere, and then come back tomorrow and try the same process. If you don't get the same hash string twice, something in the file has changed.

So far, we can determine if a file has been tampered with. What if we want to make a statement about an artifact? What if we want to say “I saw this artifact today, and I (system or person) vouch for this thing being the thing I saw”?  At this point, you need a software artifact signature; you need to process that hash string through a cryptographic algorithm to produce another string that represents the process of “signing” that fingerprint with a unique key.

If you subsequently want other people to be able to confirm your signature, you need to use asymmetric cryptography: sign the hash with your private key, and provide the corresponding public key so anyone who gets your file can verify.

As you probably know, asymmetric cryptography underpins nearly all trust on the internet. It helps you securely interact with your bank, and it helps GitHub securely deliver your repository contents. We use asymmetric cryptography to underpin technologies like TLS and SSH to create trusted communication channels, but we also use it to create the basis of trusting software through signatures.

Operating systems like Windows, macOS, iOS, Android, etc., all have mechanisms for ensuring the trustworthy provenance of executable software artifacts by mandating the presence of signatures. These systems are incredibly important components of the modern software world and are incredibly difficult to build.


## Beyond Signatures - To Attestation

Signatures are a good start when we think about how to show more trustworthy information about software artifacts. It says “some trusted system did see this thing.” But if you really want to make serious progress in securing the entire software development lifecycle (SDLC), you need to move beyond simple signatures and consider attestation.

An attestation is a factual assertion, a statement made about an artifact or something done to an artifact, created by an entity that can be authenticated. It can be authenticated because the statement has been signed, and the key used to sign it is trustworthy.

One of the most important and foundational types of attestation is asserting facts about the origin and creation of the artifact—the source code it came from and the build instructions that transformed the source code into the artifact—what we call provenance.

Our choice of provenance specification comes from the [SLSA project](https://slsa.dev/). SLSA is a great way to think about software supply chain security because it provides a common framework for both producers and consumers of software to reason about security guarantees and boundaries, independent of specific systems and technology stacks.

SLSA builds on the work of the [in-toto project](https://in-toto.io/), providing a standardized architecture for generating provenance for software artifacts. in-toto is a CNCF graduated project whose raison d'être is, in part, to provide a standardized metadata architecture for a range of relevant information about supply chains and build processes.


## What Does it Take to Build Something Like This?

GitHub, as the world’s largest software development platform hosting a massive amount of code and build pipelines, has thought a lot about this. Building an attestation service requires many moving parts.

Doing this means having a way to:

* Issue certificates (essentially public keys bound to some authenticated identity).
* Ensure those certificates aren’t abused.
* Enable the secure signing of artifacts in a well-known context.
* Verify those signatures in a way that end-users can trust.

This means setting up a [certificate authority (CA)](https://en.wikipedia.org/wiki/Certificate_authority) and having some client application that you can use to verify signatures associated with certificates issued by that authority.

To prevent certificates from being abused, you need to either (1) maintain a certificate revocation list or (2) ensure that signing certificates are short-lived, meaning some time-stamping authority counter-signature is needed (which can provide an authoritative stamp that a certificate was only used to generate signatures during its valid lifetime).

This is where [Sigstore](https://www.sigstore.dev/) comes in, an open-source project providing both an X.509 CA and an RFC 3161-based timestamping authority. It also allows you to authenticate using [OIDC tokens](https://www.microsoft.com/en-us/security/business/security-101/what-is-openid-connect-oidc), which many CI systems already generate and associate with their workloads.

Sigstore does for software signing what [Let's Encrypt](https://letsencrypt.org/) does for TLS certificates: make it simple, transparent, and easy to adopt.

GitHub, through a seat on the technical steering committee, helps oversee the governance of the Sigstore project, is a maintainer of the server application and multiple client libraries, and (along with folks from Chainguard, Google, RedHat, and Stacklok) makes up the operations team for the Sigstore public good instance, whose existence is to support public attestation for OSS projects.

Sigstore needs to conform to the standards set by the [The Update Framework (TUF) ](https://theupdateframework.org/) for a secure root of trust. This allows clients to keep up with rotations of the underlying keys of the CA without having to update their code. TUF exists to mitigate a massive attack surface that can exist when updating code in the field. Many projects use it to update long-running telemetry agents, provide secure firmware updates, and more.

With Sigstore, it’s possible to create tamper-evident paper trails connecting artifacts back to CI. This is incredibly important, because signing software in a way that can’t be forged, and capturing provenance details, means software consumers have a way to enforce their own rules about determining the origin of the code they are executing.

> Original: https://github.blog/2024-04-30-where-does-your-software-really-come-from/

---

Please indicate the author and source when reprinting this article, and please do not use it for any commercial purposes. Welcome to follow the WeChat public account "DevOps攻城狮".