---
title: Nightwatch 持续集成问题
date: 2018-01-15 22:53:53
tags:
- Nightwatch
- Automation
categories:
- Automation
---

## 在持续集成执行自动化测试用例时候会遇到那些问题呢

1. 运行时间过长
2. 因为某些错误程序卡住
3. 异常处理

<!-- more -->
## 针对以上三种情况，通过下面的三种方式进行解决

### 运行时间过长, E2E 测试脚本中难免需要时间等待，例如

```javascript
this.pause(1000);
// 尽可能将说有的 pause 换成 wait，例如：
this.element('@columns').to.be.visible.before(2000);
// 或
this.waitForElementVisible('@columns', 5000);
```

### 因为某些错误程序卡住, 在 TestCase 中进行验证时，例如

```javascript
this.assert.equal(result.value.length, 1);
// 如果只想标注失败，继续执行后面的代码，则需将 assert 换成 verify
this.veriry.equal(result.value.length, 1);

// 在 waitForElementVisible 中加 abortOnFailure 参数，当设置为 false，在 wait 超时时，就会标志为 false 继续继续执行
this.waitForElementVisible('@columns', 5000, false);

//还可以通过在 nightwatch.conf.js 设置全局变量
abortOnAssertionFailure: false
```

### 异常处理

当程序执行运行一次时，程序运行正常，一旦遇到异常时，下次执行就回出错。
例如：比如邀请账号登录系统的操作。管理员添加一个新用户，然后用这个新用户登录，之后管理员删除这个账户。但如果删除这个账号失败时，下次执行这个程序再邀请这个账号时就会提示这个账号存在的，可能这个时候这个程序就执行不下去了。这个时候就需要考虑这些异常情况处理，保证程序能够良好的执行下去。
