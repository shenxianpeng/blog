---
title: 已解决 - The Pip Inspector tree parse failed to produce output
summary: |
  本文介绍在 Black Duck Detect 中出现 "The Pip Inspector tree parse failed to produce output" 错误的原因分析及解决方法。
tags:
  - Troubleshooting
  - BlackDuck
authors:
  - shenxianpeng
date: 2022-03-02
---

## 问题详情

```bash
Failure: PIP - Pip Inspector
  The Pip Inspector tree parse failed to produce output.

Overall Status: FAILURE_DETECTOR - Detect had one or more detector failures while extracting dependencies.
```

<details>
<summary>点击展开完整输出</summary>

```bash
[main] --- ======== Detect Issues ========
[main] ---
[main] --- DETECTORS:
[main] --- 	Detector Issue
[main] --- 		/workdir/test
[main] --- 		Failure: PIP - Pip Inspector
[main] --- 			The Pip Inspector tree parse failed to produce output.
[main] ---
[main] --- ======== Detect Result ========
[main] ---
[main] --- Black Duck Project BOM: https://org.blackducksoftware.com/api/projects/246c8952-7cb8-40e9-9987-35f7d4602ae1/versions/e1cb4204-42d0-4445-8675-978df62b150d/components
[main] ---
[main] --- ======== Detect Status ========
[main] ---
[main] --- GIT: SUCCESS
[main] --- PIP: FAILURE
[main] ---
[main] --- Signature scan / Snippet scan on /workdir/test: SUCCESS
[main] --- Overall Status: FAILURE_DETECTOR - Detect had one or more detector failures while extracting dependencies. Check that all projects build and your environment is configured correctly.
[main] ---
[main] --- If you need help troubleshooting this problem, generate a diagnostic zip file by adding '-d' to the command line, and provide it to Synopsys Technical Support. See 'Diagnostic Mode' in the Detect documentation for more information.
[main] ---
[main] --- ===============================
[main] ---
[main] --- Detect duration: 00h 00m 54s 951ms
[main] --- Exiting with code 5 - FAILURE_DETECTOR
```

</details>

**运行环境**：

* Product: synopsys-detect-7.11.1.jar
* OpenJDK 11
* Python 3.6 和 Python 2.7.5

---

## 根本原因

在调试输出中可以看到，Detect 调用的是 `python`（指向 python2），而不是 `python3`，导致运行
[pip-inspector.py](https://github.com/blackducksoftware/synopsys-detect/blob/master/src/main/resources/pip-inspector.py) 失败：

```bash
DEBUG [main-Executable_Stream_Thread] --- Python 2.7.5
...
[main] --- Running executable >/usr/bin/python .../pip-inspector.py --projectname=test
```

---

## 解决方法

将 `python` 链接到 `python3` 即可。

```bash
# 备份原 python
sudo mv /usr/bin/python /usr/bin/python.old
# 建立指向 python3 的软链接
sudo ln -s /usr/bin/python3 /usr/bin/python
```

然后重新运行 Detect，例如：

```bash
bash <(curl -s -L https://detect.synopsys.com/detect7.sh) \
  --blackduck.url=https://org.blackducksoftware.com \
  --blackduck.api.token=MmMwMjdlOTctMT \
  --detect.project.name=HUB \
  --detect.project.version.name=TEST_v1.1.1 \
  --detect.source.path=/workdir/test \
  --logging.level.com.synopsys.integration=DEBUG \
  --blackduck.trust.cert=TRUE \
  --detect.tools.excluded=POLARIS \
  --detect.blackduck.signature.scanner.snippet.matching=SNIPPET_MATCHING
```

---

## Docker 方式

如果想用 Docker 来进行 Black Duck 扫描，可以构建镜像，例如：

```Dockerfile
FROM openjdk:11

# 可指定需要的 DETECT 版本，留空则下载最新
ENV DETECT_LATEST_RELEASE_VERSION=""

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
        git \
        python \
        pip \
    && apt-get autoremove \
    && apt-get clean

RUN curl -sSOL https://detect.synopsys.com/detect7.sh && bash detect7.sh --help \
    && rm -rf /usr/bin/python \
    && ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /src
```

---

希望能帮到你。

---

转载本文请注明作者与出处，禁止商业用途。欢迎关注公众号「DevOps攻城狮」。
