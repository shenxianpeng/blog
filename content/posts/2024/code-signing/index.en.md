---
title: Code Signing
summary: This article introduces the concept and importance of code signing, along with a comparison of two common code signing tools, emphasizing its role in software supply chain security.
tags:
  - DevSecOps
  - SLSA
author: shenxianpeng
date: 2024-04-29
---

When it comes to software development and security, Code Signing is a crucial concept. In this article, we will explore what code signing is, why it's important, and compare two code signing tools.

## What is Code Signing?

Code signing is a digital signature technique used to verify the authenticity and integrity of software or code. It uses cryptography to attach a digital signature to a software file, proving that the file was created by a specific developer and has not been tampered with.

The code signing process typically involves the following steps:
1. **Generate a digital certificate**: Developers use a digital certificate to create a digital signature. Certificates are usually issued by a trusted third-party Certificate Authority (CA).
2. **Sign the software**: Developers use specialized tools, such as Microsoft's SignTool or Apple's codesign tool, to digitally sign the software.
3. **Distribute the signed software**: Digitally signed software can be distributed to user devices.


## Why is Code Signing Important?

The importance of code signing is reflected in several aspects:

1. **Integrity verification**: Code signing ensures that the software has not been tampered with during distribution. Users can verify the signature to confirm the software's integrity and ensure it comes from a trusted source.

2. **Authentication**: The digital certificate accompanying the signature can be used to verify the identity of the software publisher. Users can view the certificate to learn about the software manufacturer and assess its trustworthiness.

3. **Enhanced security**: Digital signatures prevent malicious software from being inserted into legitimate software packages, ensuring that the software downloaded by users is safe and reliable.

4. **Operating system trust**: Most operating systems and app stores require developers to code-sign software before publishing. Unsigned software may be considered insecure or untrusted.

## Code Signing Tools

In my work, I mainly use two code signing tools: Code Signing Certificates [Code Signing Certificates](https://www.thawte.com/code-signing/) and [GaraSign](https://garantir.io/use-cases/code-signing/), which are representative of two different types of tools.

Here's a brief comparison of Code Signing Certificates and GaraSign:

**Code Signing Certificates** and **GaraSign** are both solutions for verifying software integrity and origin, but they have some key differences in how they work and their functionality.

| Feature | Code Signing Certificates | GaraSign |
|---|---|---|
| **Issuer** | Trusted Certificate Authority (CA) | GaraSign |
| **Form** | Digital Certificate | Cloud Service |
| **Verification Method** | Cryptographic Hash | Cryptographic Hash |
| **Functionality** | Verify software integrity, ensure software hasn't been tampered with | Verify software integrity, ensure software hasn't been tampered with, provide centralized management, support audit and compliance |
| **Cost** | $100 to thousands of dollars per year | Pay-as-you-go |
| **Management** | Requires purchasing and managing certificates | No need to manage certificates |
| **Scalability** | Suitable for organizations that need to sign a large amount of software | Suitable for organizations of any size |

**In general, both Code Signing Certificates and GaraSign are effective solutions for verifying software integrity and origin.** The best choice for you will depend on your specific needs and budget. Here are some factors to consider:

* **Cost:** If you need to sign a large amount of software, GaraSign may be more cost-effective.
* **Scalability:** If you need to sign a large amount of software, GaraSign may be a better choice.
* **Audit and compliance:** If you need to meet stringent audit and compliance requirements, GaraSign may be a better choice.
* **Ease of use:** Based on my current experience, Code Signing Certificates are easier to set up and use. GaraSign requires setting up services and installing and configuring clients, which is very cumbersome[^1].

[^1]: I am still in the early stages of using GaraSign. If necessary, I will write separate articles about my user experience with it.

Other signing tools include Microsoft's [SignTool.exe](https://learn.microsoft.com/zh-cn/dotnet/framework/tools/signtool-exe), [Docker trust sign](https://docs.docker.com/reference/cli/docker/trust/sign/), etc., which will not be introduced here.

## Conclusion

Through code signing, developers can increase the security and trustworthiness of software, while helping users avoid malicious software and tampering risks.
In today's digital environment, code signing is an important part of ensuring software integrity and security, improving software supply chain security.

For more information on software supply chain security, see this [series of articles](../../tags/slsa/).

---

Please indicate the author and source when reprinting this article, and do not use it for any commercial purposes. Welcome to follow the official account "DevOps攻城狮"