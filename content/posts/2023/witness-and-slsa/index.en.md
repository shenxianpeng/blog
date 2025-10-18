---
title: Witness and SLSA 💃
summary: This article introduces the concept and working mechanism of Witness, and how to use Witness to generate and verify the provenance of software artifacts, emphasizing its importance in improving software supply chain security.
tags:
  - SLSA
  - Witness
author: shenxianpeng
date: 2023-11-30
---

Due to the increasing frequency of attacks targeting software supply chains in recent years, Google proposed a solution in 2021: Supply chain Levels for Software Artifacts ("SLSA").

This article will describe how to generate and verify the provenance of software artifacts outside the **GitHub** ecosystem to improve your project's SLSA Level.

Witness is a pluggable software supply chain risk management framework that automates, standardizes, and verifies software artifact provenance. It is a CNCF project under [CNCF](https://www.cncf.io/projects/in-toto/), originally authored by Testifysec and later donated to [in-toto](https://in-toto.io/).

## What is Witness

Witness is a pluggable supply chain security framework that creates a provenance trace throughout the software development lifecycle (SDLC), ensuring the integrity of software from source code to target.  It supports most major CI and infrastructure providers, offering a versatile and flexible solution for securing software supply chains.

The use of a secure Public Key Infrastructure (PKI) system and the ability to verify Witness metadata further enhance the security of the process and help mitigate many software supply chain attack vectors.

Witness works by encapsulating commands executed within a continuous integration process, providing a provenance trace for each operation in the software development lifecycle (SDLC). This allows for a detailed and verifiable record of how the software was built, by whom, and what tools were used.

This evidence can be used to assess policy compliance, detect any potential tampering or malicious activity, and ensure that only authorized users or machines can complete a given step in the process.

Summary - What Witness can do

* Verify who built the software, how it was built, and what tools were used
* Detect any potential tampering or malicious activity
* Ensure that only authorized users or machines can complete each step in the process
* Distribute Attestations and Policies

## How to use Witness

It mainly consists of three steps:

1. `witness run` - Run the provided command and record an attestation about the execution.
2. `witness sign` - Sign the provided file using the provided key.
3. `witness verify` - Verify the witness policy.

### Quick Start

This is a [Witness Demo repository](https://github.com/shenxianpeng/witness-demo) I created to demonstrate the Witness workflow. You can follow these steps.



#### Prepare the environment

Install Witness and download the demo project

```bash
bash <(curl -s https://raw.githubusercontent.com/in-toto/witness/main/install-witness.sh)
Latest version of Witness is 0.1.14
Downloading for linux amd64 from https://github.com/in-toto/witness/releases/download/v0.1.14/witness_0.1.14_linux_amd64.tar.gz
expected checksum: f9b67ca04cb391cd854aec3397eb904392ff689dcd3c38305d38c444781a5a67
file checksum:     f9b67ca04cb391cd854aec3397eb904392ff689dcd3c38305d38c444781a5a67
witness v0.1.14-aa35c1f
Witness v0.1.14 has been installed at /usr/local/bin/witness

git clone https://github.com/shenxianpeng/witness-demo.git
```

#### Create key pair

```bash
openssl genpkey -algorithm ed25519 -outform PEM -out witness-demo-key.pem
openssl pkey -in witness-demo-key.pem -pubout > witness-demo-pub.pem
```

### Prepare the Witness configuration file `.witness.yaml`

```yaml
run:
    signer-file-key-path: witness-demo-key.pem
    trace: false
verify:
    attestations:
        - "witness-demo-att.json"
    policy: policy-signed.json
    publickey: witness-demo-pub.pem
```

### Integrate the build step into the Attestation

```
witness run --step build -o witness-demo-att.json -- python3 -m pip wheel --no-deps -w dist .
INFO    Using config file: .witness.yaml
INFO    Starting environment attestor...
INFO    Starting git attestor...
INFO    Starting material attestor...
INFO    Starting command-run attestor...
Processing /tmp/witness-demo
Building wheels for collected packages: witness-demo
  Running setup.py bdist_wheel for witness-demo: started
  Running setup.py bdist_wheel for witness-demo: finished with status 'done'
  Stored in directory: /tmp/witness-demo/dist
Successfully built witness-demo
INFO    Starting product attestor...
```

That is, add the `witness run` command to the previous build command.

#### View the verification data of the signed Attestation

Because the Attestation data is base64 encoded, it needs to be decoded before viewing.

```bash
cat witness-demo-att.json | jq -r .payload | base64 -d | jq

# Partial output below
 {
  "type": "https://witness.dev/attestations/command-run/v0.1",
  "attestation": {
    "cmd": [
      "python3",
      "-m",
      "pip",
      "wheel",
      "--no-deps",
      "-w",
      "dist",
      "."
    ],
    "stdout": "Processing /tmp/witness-demo\nBuilding wheels for collected packages: witness-demo\n  Running setup.py bdist_wheel for witness-demo: started\n  Running setup.py bdist_wheel for witness-demo: finished with status 'done'\n  Stored in directory: /tmp/witness-demo/dist\nSuccessfully built witness-demo\n",
    "exitcode": 0
  },
  "starttime": "2023-11-29T05:15:19.227943473-05:00",
  "endtime": "2023-11-29T05:15:20.078517025-05:00"
},
{
  "type": "https://witness.dev/attestations/product/v0.1",
  "attestation": {
    "dist/witness_demo-1.0.0-py3-none-any.whl": {
      "mime_type": "application/zip",
      "digest": {
        "gitoid:sha1": "gitoid:blob:sha1:b4b7210729998829c82208685837058f5ad614ab",
        "gitoid:sha256": "gitoid:blob:sha256:473a0f4c3be8a93681a267e3b1e9a7dcda1185436fe141f7749120a303721813",
        "sha256": "471985cd3b0d3e0101a1cbba8840819bfdc8d8f8cc19bd08add1e04be25b51ec"
      }
    }
  },
  "starttime": "2023-11-29T05:15:20.078579187-05:00",
  "endtime": "2023-11-29T05:15:20.081170078-05:00"
}
```

#### Create the Policy file

`policy.json` is used to define or require that a step has specific attributes or meets certain values, thereby requiring verification of the Attestation for successful verification. For example, if the `expires` field expires (is less than the current time), the execution of `witness verify` will fail.

```json
{
  "expires": "2033-12-17T23:57:40-05:00",
  "steps": {
    "build": {
      "name": "build",
      "attestations": [
        {
          "type": "https://witness.dev/attestations/material/v0.1",
          "regopolicies": []
        },
        {
          "type": "https://witness.dev/attestations/command-run/v0.1",
          "regopolicies": []
        },
        {
          "type": "https://witness.dev/attestations/product/v0.1",
          "regopolicies": []
        }
      ],
      "functionaries": [
        {
          "publickeyid": "{{PUBLIC_KEY_ID}}"
        }
      ]
    }
  },
  "publickeys": {
    "{{PUBLIC_KEY_ID}}": {
      "keyid": "{{PUBLIC_KEY_ID}}",
      "key": "{{B64_PUBLIC_KEY}}"
    }
  }
}
```

More information about policy attributes and settings can be found here: https://github.com/in-toto/witness/blob/main/docs/policy.md

### Sign the Policy file

Before signing, you need to replace the variables in the Policy file.

```bash
id=`sha256sum witness-demo-pub.pem | awk '{print $1}'` && sed -i "s/{{PUBLIC_KEY_ID}}/$id/g" policy.json

pubb64=`cat witness-demo-pub.pem | base64 -w 0` && sed -i "s/{{B64_PUBLIC_KEY}}/$pubb64/g" policy.json
```

Then use `witness sign` to sign.

```bash
witness sign -f policy.json --signer-file-key-path witness-demo-key.pem --outfile policy-signed.json
INFO    Using config file: .witness.yaml
```

#### Verify that the binary file meets policy requirements

```bash
witness verify -f dist/witness_demo-1.0.0-py3-none-any.whl -a witness-demo-att.json -p policy-signed.json -k witness-demo-pub.pem
INFO    Using config file: .witness.yaml
INFO    Verification succeeded
INFO    Evidence:
INFO    0: witness-demo-att.json
```

## Finally

This is a demonstration of using Witness for Non-GitHub projects.

If your project code is on GitHub, the easiest and most popular way is to use [slsa-github-generator](https://github.com/slsa-framework/slsa-github-generator), a tool provided by the [SLSA Framework](https://github.com/slsa-framework), and then use [slsa-verifier](https://github.com/slsa-framework/slsa-verifier) to verify the Provenance.  Refer to my previous article [Python and SLSA 💃](https://shenxianpeng.github.io/2023/11/python-and-slsa/) for details.

---

Please indicate the author and source when reprinting this article, and do not use it for any commercial purposes. Welcome to follow the WeChat official account "DevOps攻城狮".