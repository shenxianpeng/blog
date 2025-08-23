---
title: Nightwatch Opening Multiple Windows
summary: |
  How to open multiple browser windows and switch control in Nightwatch.
date: 2018-01-02
tags:
- Nightwatch
author: shenxianpeng
---

What if you want to open two windows and control which window?

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