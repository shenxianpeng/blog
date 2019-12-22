---
title: Nightwatch 得到和验证 cookies
date: 2017-12-14 14:21:56
tags: 
- Nightwatch
- Javascript
categories: 
- Automation
author: shenxianpeng
---

## 测试用例

验证登录 cookies 和清除 access_token。测试用例设计如下

## 测试用例设计

登录系统时，不选择记住我按钮，验证 cookies

```javascript
client.getCookies(function cb(result) {
    this.assert.equal(result.value.length, 3);
    this.assert.equal(result.value[0].name, 'domain');
    this.assert.equal(result.value[1].name, 'user_id');
    this.assert.equal(result.value[2].name, 'access_token');
});
```

登录系统时，选择记住我按钮，验证 cookies

```javascript
client.getCookies(function cb(result) {
    this.assert.equal(result.value.length, 5);
    this.assert.equal(result.value[0].name, 'domain');
    this.assert.equal(result.value[1].name, 'user_id');
    this.assert.equal(result.value[2].name, 'identifier');
    this.assert.equal(result.value[3].name, 'access_token');
    this.assert.equal(result.value[4].name, 'persistent_token');
});
```

登录系统时，不选择记住我按钮，删除 cookies

```javascript
let accesstoken;
client.getCookies(function cb(result) {
    accesstoken = result.value[2].name;
    this.deleteCookie(accesstoken, function () {
        // refresh current page, logout
        this.refresh().waitForElementVisible('div.login-form', 5000);
    });
});
```

登录系统时，选择记住我按钮，删除 cookies

```javascript
let accesstoken;
client.getCookies(function cb(result) {
    accesstoken = result.value[3].name;
    this.deleteCookie(accesstoken, function() {
        // refresh current page, still login
        this.refresh().waitForElementVisible('.andes-header', 5000);
    });
});
```

## 如何知道登录都有哪些参数

事先在手动测试的时候打开 chrome 浏览器，然后按 F12，登录时查看 Network。

以成功百度登录时为例，可以看到 Headers 里的参数，我们可以通过验证这些参数来确定登录成功了。

这样我们就可以这些参数来实现对 cookie，token 等等参数进行自动化测试的验证。

