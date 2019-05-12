---
title: Nightwatch异步操作
date: 2017-10-21 21:26:43
tags: nightwatch
categories: automation
---

在自动化测试中常常需要通过一个command（或function）中返回的值来进行下一步的操作，JavaScript与JAVA在调用返回值时有所不同，JS中需要特定的写法来进行这种异步操作。

以下面的get License数量为例，首先需要get一次License数量，然后进行一些列操作之后，再一次get License数量，比较这两次License数量值。

getLicenseNum方法：
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

对两次得到的License num进行比较：

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