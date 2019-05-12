---
title: Nightwatch元素判断
date: 2017-12-14 17:34:18
tags: 
- nightwatch
- automation
---

### Nightwatch元素常用验证方法
1. 验证元素的值信息
```javascript
andesFormSection
    .assert.containsText('@errorMessage', 'The email address is invalid.')
```

2. 验证元素是否可用
```javascript
andesFormSection
    .assert.attributeEquals('@continueBtn', 'disabled', 'true');
```

3. 等待元素可用
```javascript
andesFormSection
    .expect.element('@signInBtn').to.be.visible.before(5000);

或者

andesFormSection
    waitForElementVisible('signInBtn', 5000);
```

4. 等待元素呈现
```javascript
andesFormSection
    .expect.element('@signInBtn').to.be.present.before(5000);

或者

andesFormSection
    waitForElementPresent('signInBtn', 5000);
```