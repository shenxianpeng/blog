---
title: Nightwatch 测试用例失败继续执行
date: 2017-10-27 17:04:49
tags:
- Nightwatch
- Automation
categories:
- Automation
author: shenxianpeng
---

自动化测试中，有一个验证点，当测试通过时，后面的测试脚本继续执行；
当出现异常时，你希望标记出来这个错误，但不影响后面的测试脚本执行，在 Nightwatch 中如何做？

<!-- more -->
下面的一段代码验证 home 页面的 body 是否显示。这里如果显示则将验证点置为 false，如下：

```javascript
home.waitForElementVisible('@body', 3000, true, function(result) {
    if (result.value) {
        // 测试报告中会显示失败，但是会继续执行后面的测试脚本
        client.verify.equal(result.value, false);
    } else {
        // 验证点通过
        console.log('Pass');
    }
});
```

注意：这里如果用 assert，程序就会中断执行。

```javascript
// 中断执行
client.assert.equal(result.value, false);
```
