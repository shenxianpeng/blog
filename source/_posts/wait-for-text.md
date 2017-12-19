---
title: Wait For Text
date: 2017-12-19 10:29:41
tags: nightwatch
---

在使用Nightwatch做自动化测试的时候，会遇到这样一种情况：
创建一个query, 等待这个query的状态从Wait变成Running最后到Available时再执行操作。
Nightwatch并没有提供这样的方法，可以通过下面的方式解决。

```javascript
'Wait for text': function waitForText(client) {
    let i = 0;
    const query = client.page.query();
    query.navigate();
    // if status != 'Available', wait until 10s
    client.getText(firestName, function (result) {
        while (result.value.indexOf('Available') != 0 && i <= 10) {
            client.pause(1000);
            i++;
        }
        // break, TODO
    });
}
```