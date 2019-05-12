---
title: Nightwatch判断元素是否存在
date: 2017-10-26 17:09:06
tags: nightwatch
categories: automation
---

用Nightwatch去判断一个element是否存在，如果存在执行如下操作，如果不存在做另外的操作。
这个在Java编写的自动化测试用例中可以用try catch可以解决，Nightwatch试过不行。
另外看到stackoverflow上有通过判断 (result.status != -1)，没有解决我的问题。最后这样解决的，请看下面tutorial.js：
```javascript
const tutorialCommands = {
  notShowTutorial: function() {
    const tutorialSection = this.section.tutorial;
    this.api.element('css selector', '.andes-dialog md-icon', function(result) {
      if (result.value && result.value.ELEMENT) {
        this.pause(2000);
        tutorialSection.click('@doNotShowBtn');
        this.pause(2000);
        tutorialSection.click('@closeBtn');
    } else {
      console.log('no tutorial exists');
    }
    });
  }
};

module.exports = {
  commands: [tutorialCommands],
  url: function() {
    return `https://shenxianpeng.github.io/`;
  },
  sections: {
    tutorial: {
      selector: '.andes-dialog',
      elements: {
        closeBtn: 'md-icon',
        doNotShowBtn: 'md-checkbox .md-container'
      }
    }
  }
};
```
注意：这里的元素不能通过section的方式引用，例如这样，怀疑这是Nightwatch的bug。
```javascript
tutorialSection.api.element('css selector', '@closeBtn', function(result) {

}
```