---
title: Python 供应链“核弹”级攻击刚刚发生：一个 pip install 就偷走你的所有凭证！
summary: |
  Python 供应链攻击已经发生，一个 pip install 就能偷走你的所有凭证。介绍如何用 pipguard 在安装前拦截恶意包。

tags:
  - pipguard
  - python
  - pip
authors:
  - shenxianpeng
date: 2026-03-26
translate: false
series: ["我的开源项目"]
series_order: 3
---


大家好，我是沈工。

最近 AI 圈知名人物 Karpathy（前特斯拉 AI 总监、OpenAI 联合创始人）发了一条推文刷爆了 Python 社区——**LiteLLM 遭供应链攻击**。

简单一个 `pip install litellm`，你的 SSH 密钥、AWS/GCP/Azure 凭证、K8s 配置、Git 密钥、所有环境变量里的 API Key、Shell 历史、加密钱包、SSL 私钥、CI/CD 秘密、数据库密码，统统被偷偷发走。

更厉害的是：**你甚至都不用直接安装 litellm**。

只要你的项目依赖了它（比如 dspy 依赖 litellm>=1.64.0），就会中招。这个包一个月下载量高达 **97 million** 次。

---

### 这到底是怎么发生的？

2026 年 3 月 24 日，LiteLLM 官方版本 1.82.8 被恶意上传到 PyPI（维护者账号大概率被攻破）。攻击者往包里塞了一个 `litellm_init.pth` 文件。

`.pth` 文件会在 Python 解释器**启动时自动执行**，完全不需要你 `import litellm`。里面藏着 base64 编码的恶意代码，疯狂扫描并外传敏感文件，还会自我复制。

这个版本只上线了不到 3 小时，PyPI 很快隔离了。但那 3 小时里已经下载了多少？没人说得清。

值得一提的是：攻击者代码写得不够利落——有个用户用 Cursor 的 MCP 插件拉依赖时，恶意代码把内存耗尽直接崩溃，这才被及时发现。否则，可能要等几天甚至几周，大家才意识到凭证已经泄露。

Karpathy 说：现代开发把依赖当积木，但每一次 `pip install` 都在赌整个依赖树里有没有毒包。

---

### 传统安全工具为什么没用？

pip-audit、GuardDog 这类工具，原理是等漏洞暴露后，用已知签名或 CVE 数据库去扫描。逻辑上就是**先安装，后检查**。

遇到零日攻击——没有已知 CVE 的攻击——这些工具根本看不见。

---

看到 Karpathy 那条推文后，就这个问题本身是可以杜绝的——**在下载阶段就做检查，把危险识别出来，拦在安装之前**。

于是快速原型出了这个工具：**pipguard**。

**核心思路**：不等安装完再查，而是先 `pip download` 把包下载下来 → 解压（绝不执行任何代码）→ 用 Python **标准库 AST（抽象语法树）** 做静态分析，扫所有 `.py`、`.pth`、`setup.py` 文件。

**AST 到底是怎么识别危险的？**  
AST 就是把 Python 源码“解剖”成一棵树，只看结构，不运行代码。pipguard 遍历这棵树，专门找以下危险信号：

```python
import ast

code = "exec(base64.b64decode(b'ZGVmIG1hbGljaW91cygpOiBwcmludCgiaGFjayIp'))"
tree = ast.parse(code)                    # 解析成 AST
for node in ast.walk(tree):
    if isinstance(node, ast.Call):        # 发现函数调用
        if getattr(node.func, 'id', None) in ('eval', 'exec'):
            print("⚠️ 发现可疑的 eval/exec！")
        # 继续检查参数里有没有 base64、读取 ~/.ssh 等路径
```

只要检测到 `.pth` 自动执行 + `eval(base64...)` + 读取 `~/.ssh/id_rsa` 或 `~/.aws/credentials`，立刻打 **CRITICAL** 直接阻断。

**几个设计原则：**
- 零依赖、纯 stdlib（不联网、不依赖数据库，工具本身极干净）
- 行为风险评分（不查已知病毒，看“这个包敢不敢干坏事”）
- 无感切换（原来 `pip install`，现在 `pipguard install`）

如果 litellm 1.82.8 还在 PyPI 上，pipguard 的输出会是这样的：
```
✗ BLOCKED: litellm==1.82.8
.pth autorun · reads ~/.ssh/id_rsa
exfiltrates to 44.202.x.x:4444
Severity: CRITICAL · Exit code: 1
```

---

### 怎么用？就两步！

**第一步**：**推荐用 pipx 安装（完全隔离，更安全）**，或者在项目虚拟环境**外面**用 pip 安装：
```bash
pipx install pipguard
# 或者
pip install pipguard
```

**第二步**：直接替换 pip install：
```bash
pipguard install litellm==1.82.8   # 当时的恶意版本，现已下架，会被直接阻断
pipguard install requests pandas   # 干净包正常通过
```

录了个小 demo，展示 pipguard 是怎么在安装前就识别出恶意行为的：

![](demo.gif)

如果是集成到 CI/CD。可以把 GitHub Actions / GitLab CI / Jenkins 里的 `pip install` 换成 `pipguard install`，整个流水线就会多一层防护。

---

### 局限性

老实说，目前 pipguard 仍有一些局限性——它基于静态 AST 分析，并非万能的银弹：

- 混淆绕过：恶意代码经过多层混淆后，AST 可能识别不出来
- 动态加载：运行时动态构造的恶意行为无法静态检测
- 误报可能：少数合法包也会用到高风险 API（比如测试框架），可能触发告警

后面会持续迭代检测规则，增加更多特征检测，逐步降低误报率，但永远不可能做到 100% 万无一失。

所以 pipguard 是额外的一道防线，而不是替代现有安全实践。但能把 **大多数的零日攻击挡在了门外**。

但基础的安全习惯仍然重要——锁定依赖版本（`pip freeze`）、定期审计、最小权限运行，这些基础还是要有。

---

### 供应链安全最佳实践

pipguard 只是工具链的一环，一些基本的供应链安全原则是需要了解并遵守的，比如：

**1. 锁定依赖版本**

生产环境一定要用 `mypackage==<version>` 或 `poetry.lock` / `uv.lock` 锁定完整依赖树。

版本浮动（`litellm>=1.64.0`）意味着你把选择权交给了别人。

**2. 使用隔离的虚拟环境**

避免将包安装到系统 Python，而要使用 Python Virtual Environment（虚拟环境）隔离，这样能把爆炸半径控制在最小范围：一个项目中招，不会污染整台机器。

**3. 最小权限运行**

CI/CD 流水线里，Runner 不要给 root 权限，SSH Key 和云凭证按需颁发、按需吊销。恶意包能偷走的，只有能拿到的。

**4. 审计间接依赖，不只看直接依赖**

这次攻击中，大多数受害者甚至没有直接安装 litellm——它藏在间接依赖里。定期跑 `pip-audit` 或 `safety check` 扫一遍已知 CVE，结合 pipguard 的零日拦截，双重覆盖。

**5. 在 CI/CD 里做依赖指纹校验**

用 `pip install --require-hashes` 配合 `requirements.txt` 里记录的 SHA256 哈希，确保安装的包字节级别完全一致，防止镜像源投毒。

```bash
# 生成带哈希的 requirements.txt
pip-compile --generate-hashes requirements.in

# 安装时强制校验哈希
pip install --require-hashes -r requirements.txt
```

**6. 监控 PyPI 变更告警**

关注 [PyPI Safety Advisories](https://pypi.org/security-advisories/)，订阅关键依赖的 GitHub Release 通知。攻击往往在几小时内发酵，信息差就是防御差。

**7. 沙箱/容器化运行不可信代码**

新包第一次跑，放进 Docker 容器或 macOS 沙箱里，观察有没有异常网络请求或文件操作，再决定是否引入正式项目。

> 安全没有银弹，但这七条加在一起，已经能挡住绝大多数供应链攻击。

---

### 最后说几句

这次 litellm 事件再次说明一件事：**安全必须前置，不能靠事后补救**。

传统扫描工具是事后验尸，pipguard 是门口的检查站——包还没落地，危险就被挡在外面了。

项目完全开源，MIT 协议：
- 文档：https://shenxianpeng.github.io/pipguard/
- GitHub：https://github.com/shenxianpeng/pipguard

有问题、有想法、想一起完善风险规则，GitHub Issues 见。

下一条供应链攻击不知道什么时候来，但我们可以提前做点准备。

`pipx install pipguard`（或 `pip install pipguard`），然后顺手去 GitHub 点个 Star，感谢支持。

老司机们，请安全驾驶，我们下期见～
