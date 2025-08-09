---
title: Nightwatch 元素判断
summary: 本文介绍了如何在 Nightwatch.js 中验证元素的存在性和状态，包括常用的验证方法和示例代码。
tags:
  - Nightwatch
date: 2017-12-14
author: shenxianpeng
---

### Nightwatch 元素常用验证方法

验证元素的值信息


```javascript
andesFormSection
    .assert.containsText('@errorMessage', 'The email address is invalid.')
```

验证元素是否可用

```javascript
andesFormSection
    .assert.attributeEquals('@continueBtn', 'disabled', 'true');
```

等待元素可用

```javascript
andesFormSection
    .expect.element('@signInBtn').to.be.visible.before(5000);

或者

andesFormSection
    waitForElementVisible('signInBtn', 5000);
```

等待元素呈现

```javascript
andesFormSection
    .expect.element('@signInBtn').to.be.present.before(5000);

或者

andesFormSection
    waitForElementPresent('signInBtn', 5000);
```
