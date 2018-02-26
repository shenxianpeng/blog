---
title: How to debug nightwatch in VS
date: 2018-02-01 14:40:05
tags: nightwatch
---

除了通过增加
```javascript
console.log('===========')
```
来调试Nightwatch代码，如何通过配置VS code来Debug Nightwatch代码？

Ctrl+Shift+D 打开Debug界面，配置如下：

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