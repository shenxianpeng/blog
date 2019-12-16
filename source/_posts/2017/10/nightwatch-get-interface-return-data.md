---
title: 如何获取接口返回数据
date: 2017-10-22 22:38:50
tags: 
- Nightwatch
- Automation
categories: 
- Automation
---

如何在 JavaScript 通过接口自动生成和返回接口数据呢？

在自动化测试中常常遇到接口测试，或是使用的数据需要从接口返回，那么如何来实现这种情况？
例如我想通过 generateLicense 方法生成一个 license，然后在之后的自动化测试用例中使用这个生成的 license 继续做下一步的操作，例如注册 license 等。

在 license.js 文件中创建一个 generateLicense 方法：

```javascript
generateLicense: function(success, day, capacity, code) {
    var request = require('request');
    var options = { method: 'POST',
    url: 'https://generate-license/api/licenses',
    headers:
        { 'postman-token': 'd849e636-58c9-2705',
        'cache-control': 'no-cache',
        authorization: 'Basic YWRtaW46U',
        'content-type': 'application/json' },

    body: { company: 'Google',
        email: '5012962@qq.com',
        expiration: day,
        capacity: capacity,
        phone: '89262518',
        address: 'Dalian',
        code: code },
    json: true
  };

  request(options, function (error, response) {
    if (error) {
        console.log(error);
            return;
        }
    success(response);
  });
},
```

对上面生成的 license 进行赋值，之后的测试用例中就可以使用 MVlicense 了。
使用中会涉及到异步操作，异步如何操作请看之前的文章。

```javascript
const license = client.page.license();
let MVlicense;
license.generateLicense(function(response) {
    MVlicense = response.body.data.license.license;
}, 365, 10, 'MV');
```
