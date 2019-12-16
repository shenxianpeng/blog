---
title: Nightwatch handle cookies
date: 2017-12-14 14:21:56
tags: 
- Nightwatch
- Javascript
categories: 
- Automation
---

#### Test Case: 验证登录 cookies 和清除 access_token

Login system, don't chosse Remember Me, verify Cookies

```javascript
client.getCookies(function cb(result) {
    this.assert.equal(result.value.length, 3);
    this.assert.equal(result.value[0].name, 'domain');
    this.assert.equal(result.value[1].name, 'user_id');
    this.assert.equal(result.value[2].name, 'access_token');
});
```

Login system, choose Remember Me，verify Cookies

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

Login system，do not chosse Remember Me, delete Cookies

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

Login system，choose Remember Me, delete Cookies

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
