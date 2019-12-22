---
title: Nightwatch 打开多个窗口
date: 2018-01-02 09:57:32
tags: 
- Nightwatch
- Automation
categories: 
- Automation
author: shenxianpeng
---

如果想打开两个窗口并控制那个窗口怎么办？

```javascript
var url = process.env.BASE_URL, newWindow;

client.execute(function (url, newWindow) {
    window.open(url, newWindow, 'height=768,width=1024');
}, [url, newWindow]);

client.window_handles(function(result) {
    this.verify.equal(result.value.length, 2, 'There should be 2 windows open');
    newWindow = result.value[1];
    this.switchWindow(newWindow);
})
```
