---
title: Witness 和 SLSA 💃
summary: 本文介绍了 Witness 的概念、工作原理以及如何使用 Witness 来生成和验证软件工件的来源，强调了其在提高软件供应链安全性方面的重要性。
tags:
  - SLSA
  - Witness
authors:
aliases:
  - /2023/11/witness-and-slsa/
  - shenxianpeng
date: 2023-11-30
---

由于近些年针对软件的供应链的攻击越来越频繁，因此 Google 在 2021 提出的解决方案是软件工件供应链级别（Supply chain Levels for Software Artifacts，"SLSA"）

本篇将介绍在**非 GitHub** 生态系统中，我们如何生成和验证软件工件的来源，从而提高你的项目的 SLSA Level。

Witness 是一个可插拔的软件供应链风险管理框架，它能自动、规范和验证软件工件出处。它是 in-toto 是 [CNCF](https://www.cncf.io/projects/in-toto/) 下的项目之一。它的最初作者是 Testifysec，后来捐赠给了 [in-toto](https://in-toto.io/)。

## 什么是 Witness

Witness 是一个可插拔的供应链安全框架，可创建整个软件开发生命周期（SDLC）的证据（Provenance）跟踪，确保软件从源代码到目标的完整性。它支持大多数主要的 CI 和基础架构提供商，是确保软件供应链安全的多功能、灵活的解决方案。

安全 PKI (Public Key Infrastructure - 公钥基础设施)分发系统的使用和验证 Witness 元数据的能力进一步增强了流程的安全性，并有助于减少许多软件供应链攻击向量。

Witness 的工作原理是封装在持续集成流程中执行的命令，为软件开发生命周期（SDLC）中的每个操作提供证据跟踪，这样就可以详细、可验证地记录软件是如何构建的、由谁构建以及使用了哪些工具。

这些证据可用于评估政策合规性，检测任何潜在的篡改或恶意活动，并确保只有授权用户或机器才能完成流程中的某一步骤。

总结 - Witness 可以做什么

* 验证软件由谁构建、如何构建以及使用了哪些工具
* 检测任何潜在的篡改或恶意活动
* 确保只有经授权的用户或机器才能完成流程的每一步
* 分发证词（Attestations）和策略（Policy）

## 如何使用 Witness

主要分三步：

1. `witness run` - 运行提供的命令并记录有关执行的证词。
2. `witness sign` - 使用提供的密钥签署提供的文件。
3. `witness verify` - 验证 witness 策略。

### 快速开始

这是我创建的 [Witness Demo 仓库](https://github.com/shenxianpeng/witness-demo)用于演示 witness 的工作流程，具体可以根据如下步骤进行。



#### 准备环境

安装 witnesss，下载 demo 项目

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

#### 创建钥匙对

```bash
openssl genpkey -algorithm ed25519 -outform PEM -out witness-demo-key.pem
openssl pkey -in witness-demo-key.pem -pubout > witness-demo-pub.pem
```

### 准备 Witness 配置文件 `.witness.yaml`

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

### 将构建步骤进入到证词（Attestation）中

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

即在之前的 build command 中加入 `witness run` 的相关命令。

#### 查看已签名的 Attestation 的验证数据

因为 Attestation 数据是进行的 base64 编码，因此需要解码进行查看

```bash
cat witness-demo-att.json | jq -r .payload | base64 -d | jq

# 以下是部分输出
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

#### 创建 Policy 文件

`policy.json` 用来定义或要求一个步骤由具有特定属性或满足一些特殊的值，从而要求验证 Attestation 才能成功。比如这里的 `expires` 字段过期了即小于当前的时间，那么在执行 `witness verify` 的时候就会失败。

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

更多关于 policy 的属性和设置可以参考这里：https://github.com/in-toto/witness/blob/main/docs/policy.md

### 给 Policy 文件做签名

在签名之前需要先替换到 Policy 文件的变量

```bash
id=`sha256sum witness-demo-pub.pem | awk '{print $1}'` && sed -i "s/{{PUBLIC_KEY_ID}}/$id/g" policy.json

pubb64=`cat witness-demo-pub.pem | base64 -w 0` && sed -i "s/{{B64_PUBLIC_KEY}}/$pubb64/g" policy.json
```

然后使用 `witness sign` 来做签名

```bash
witness sign -f policy.json --signer-file-key-path witness-demo-key.pem --outfile policy-signed.json
INFO    Using config file: .witness.yaml
```

#### 验证二进制文件是否符合政策要求

```bash
witness verify -f dist/witness_demo-1.0.0-py3-none-any.whl -a witness-demo-att.json -p policy-signed.json -k witness-demo-pub.pem
INFO    Using config file: .witness.yaml
INFO    Verification succeeded
INFO    Evidence:
INFO    0: witness-demo-att.json
```

## 最后

以上就是使用 witness 针对 Non-GitHub 项目的演示。

如果你的项目代码是放在 GitHub 上的，目前最容易、最流行的方式就是使用 [slsa-github-generator](https://github.com/slsa-framework/slsa-github-generator) 一个由 [SLSA Framework](https://github.com/slsa-framework) 官方提供的工具，然后使用 [slsa-verifier](https://github.com/slsa-framework/slsa-verifier) 来验证 Provenance。具体可以参考我的上一篇文章 [Python 和 SLSA 💃](https://shenxianpeng.github.io/2023/11/python-and-slsa/)

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
