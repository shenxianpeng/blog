---
title: Resolved - The Pip Inspector tree parse failed to produce output
summary: |
  This article explains how to resolve the "The Pip Inspector tree parse failed to produce output" error in Black Duck Detect, including the root cause and solution.
tags:
  - Troubleshooting
  - BlackDuck
author: shenxianpeng
date: 2022-03-02
---

## Details

```bash
Failure: PIP - Pip Inspector
  The Pip Inspector tree parse failed to produce output.

Overall Status: FAILURE_DETECTOR - Detect had one or more detector failures while extracting dependencies.
```

For more output please click to expand.

<details>
<summary>👉 Click to see more output 👈</summary>

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

ENVIRONMENT:

* Product: synopsys-detect-7.11.1.jar
* Others: OpenJDK 11, Python 3.6 and Python 2.7.5

## Root cause



More output of this run, I see it used `python` (which is python2) not `python3`,
so run [pip-inspector.py](https://github.com/blackducksoftware/synopsys-detect/blob/master/src/main/resources/pip-inspector.py) failed.

```bash
DEBUG [main-Executable_Stream_Thread] --- Python 2.7.5

...

[main] --- Running executable >/usr/bin/python /home/****/blackduck/runs/2022-03-01-07-45-05-986/shared/pip/pip-inspector.py --projectname=test
```

## Solution

Link python to python3, it works in my case.

For example

```bash
# save python to other name
sudo mv /usr/bin/python /usr/bin/python.old
# link python3 to python
sudo ln -s /usr/bin/python3 /usr/bin/python
```

Then try to run `bash <(curl -s -L https://detect.synopsys.com/detect7.sh)` again, my test commands:

```bash
bash <(curl -s -L https://detect.synopsys.com/detect7.sh) --blackduck.url=https://org.blackducksoftware.com --blackduck.api.token=MmMwMjdlOTctMT --detect.project.name=HUB --detect.project.version.name=TEST_v1.1.1 --detect.source.path=/workdir/test --logging.level.com.synopsys.integration=DEBUG --blackduck.trust.cert=TRUE --detect.tools.excluded=POLARIS --detect.blackduck.signature.scanner.snippet.matching=SNIPPET_MATCHING
```

If you want to use Docker to do Blackduck scan, you can create a Docker image. like this



```Dockerfile
FROM openjdk:11

# Set DETECT version you need, if it's empty download the latest version.
# https://sig-repo.synopsys.com/artifactory/bds-integrations-release/com/synopsys/integration/synopsys-detect
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

Hope this help.

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
