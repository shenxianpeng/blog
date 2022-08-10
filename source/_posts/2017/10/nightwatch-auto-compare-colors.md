---
title: Nightwatch 自动化测试中比较颜色
date: 2017-10-25 15:28:49
tags:
- Nightwatch
- Automation
categories:
- Automation
---

在做 Nightwatch 自动化测试中，出现需要比较颜色的时候如何来做？
基本的思路是首先需要取到这个 element 的颜色值，然后跟预期的颜色进行对比。
比如我要取下面这个会话窗口的颜色，选中这个图标，按 F12，查看这个图标的属性。发现Angular中的颜色属性不是 Elements 下，是在 Styles 下面，如何取到这个颜色值？

![element](nightwatch-auto-compare-colors/color.png)

这里会用到 getCssProperty 这个方法，具体如何使用，请看如下代码：

```javascript
getChatColor: function(cb) {
    const chat = '[ng-click="show()"]'
    this.getCssProperty('@chat', 'background-color', function(result) {
      cb(result.value);
    });
    return this;
},
```

将上面的 getChatColor command 代码放到一个叫 chat.js 的 page 下面，然后在测试用例中这样调用这个 command

```javascript
'Test get color': function (client) {
    var chat = client.page.chat();
    let chatColor;
    chat.navigate();

    chat.getChatColor(function(color) {
        chatColor = color;
    });
    client.perform(function() {
        client.assert.equal(chatColor, 'rgba(50, 104, 152, 1)');
    });
}
```

截图中看到的 background color 是 rgb(50, 104, 152), 但是 getChatColor 返回指是rgba，rgb 和 rgba 之间需要转化一下，a 表示透明度，取值0~1之间。
