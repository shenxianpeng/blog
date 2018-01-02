---
title: Open multiple windows
date: 2018-01-02 09:57:32
tags: nightwatch
---

如果想打开两个窗口并控制那个窗口怎么办？
```javascript
var url, newWindow;

client
    .execute(function (url, newWindow) {
        window.open('https://www.google.com', newWindow, 'height=768,width=1024');
    }, [url, newWindow]);

client
    .windowHandles(function(result) {
        this.verify.equal(result.value.length, 2, 'There should be 2 windows   open');
        newWindow = result.value[1];
        this.switchWindow(newWindow);
})
```
