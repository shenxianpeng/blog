---
title: Nightwatch 异步操作
summary: 本文介绍了如何在 Nightwatch.js 中处理异步操作，包括获取 License 数量并进行比较的示例代码。
date: 2017-10-21
tags:
- Nightwatch
---

在自动化测试中常常需要通过一个 command（或 function ）中返回的值来进行下一步的操作，JavaScript 与 JAVA 在调用返回值时有所不同，JS 中需要特定的写法来进行这种异步操作。

以下面的 get License 数量为例，首先需要 get 一次 License 数量，然后进行一些列操作之后，再一次 get License 数量，比较这两次 License 数量值。


getLicenseNum 方法：

```javascript
getLicenseNum: function (cb) {
    const license = 'ul > li.license-id.ng-binding';
    this.waitForElementVisible(license, 5000);
    this.api.elements('css selector', license, function (result) {
        cb(result.value.length);
    return this;
    });
}
```

对两次得到的 License num 进行比较：

```javascript
'JavaScrpit asynchronous operation': function(client) {
    const license = client.page.license();
    let num1, num2;
    license.getLicenseNum(function(num) {
        num1 = num;
    });
    license.getLicenseNum(function(num) {
        num2 = num;
    });
    client.perform(function() {
        client.assert.equal(num2 - num1, 1, 'license number increase 1');
    });
}
```
