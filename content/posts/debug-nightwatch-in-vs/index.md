---
title: Nightwatch 使用 VS code 进行调试
summary: 本文介绍如何配置 VS Code 来调试 Nightwatch 测试代码，提供了详细的配置示例和步骤。
date: 2018-02-01
tags:
- Nightwatch
- Javascript
- Automation
author: shenxianpeng
---

除了通过增加

```javascript

console.log('===========')
```

来调试 Nightwatch 代码，如何通过配置 VS code 来 Debug Nightwatch 代码？

Ctrl+Shift+D 打开 Debug 界面，配置如下：

```javascript
{
    // Use IntelliSense to learn about possible Node.js debug attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [

        {
            "type": "node",
            "request": "launch",
            "name": "npm test",
            "program": "${workspaceRoot}/node_modules/nightwatch/bin/runner.js",
            "args": [
                "tests/DQA/DQA-221/login.js"
            ]
        }
    ]
}
```
