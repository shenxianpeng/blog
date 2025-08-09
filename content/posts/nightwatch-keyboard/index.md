---
title: Nightwatch 模拟键盘操作
summary: 本文介绍了如何在 Nightwatch.js 中模拟键盘操作，包括输入文本和组合键操作的示例代码。
date: 2017-10-19
tags:
  - Nightwatch
author: shenxianpeng
---

在自动化测试中有这样一个场景，在一个输入框中输入一串字符，然后执行敲回车键，验证搜索结果，以 Google 搜索为例，代码如下：

```javascript
'search nightwatch and click ENTER key': function(client) {
 client
    .url('http://google.com')
    .expect.element('body').to.be.present.before(1000);
 client.setValue('input[type=text]', ['nightwatch', client.Keys.ENTER])
    .pause(1000)
    .assert.containsText('#main', 'Night Watch');
}
```



不能翻墙的可换成 baidu，相应的 element 需要改一下否则以上代码会报错。
上面的代码是执行一个按键操作，如果想做组合键操作怎么办呢？比如在 Google 搜索框中输入 nightwatch，然后按 ctrl+a 组合键来进行全选操作。还是以 Google 搜索为例，代码如下：

```javascript
 client.setValue('input[type=text]',['nightwatch', [client.Keys.CONTROL, 'a']])
```

其他的组合键操作以此类推。

其他按键 Keys 如下：
Keys:
{ NULL,
  CANCEL,
  HELP,
  BACK_SPACE,
  TAB,
  CLEAR,
  RETURN,
  ENTER,
  SHIFT,
  CONTROL,
  ALT,
  PAUSE,
  ESCAPE,
  SPACE,
  PAGEUP,
  PAGEDOWN,
  END,
  HOME,
  LEFT_ARROW,
  UP_ARROW,
  RIGHT_ARROW,
  DOWN_ARROW,
  ARROW_LEFT,
  ARROW_UP,
  ARROW_RIGHT,
  ARROW_DOWN,
  INSERT,
  DELETE,
  SEMICOLON,
  EQUALS,
  NUMPAD0,
  NUMPAD1,
  NUMPAD2,
  NUMPAD3,
  NUMPAD4,
  NUMPAD5,
  NUMPAD6,
  NUMPAD7,
  NUMPAD8,
  NUMPAD9,
  MULTIPLY,
  ADD,
  SEPARATOR,
  SUBTRACT,
  DECIMAL,
  DIVIDE,
  F1,
  F2,
  F3,
  F4,
  F5,
  F6,
  F7,
  F8,
  F9,
  F10,
  F11,
  F12,
  COMMAND,
  META
},
