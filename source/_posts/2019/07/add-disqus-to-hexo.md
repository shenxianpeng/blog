---
title: Hexo添加Disqus留言功能
date: 2019-07-07 20:20:50
tags: 
- Hexo
categories: 
- Hexo
author: shenxianpeng
---

## 在你的 Hexo 网站添加 Disqus

去 Disqus 创建一个账号，在这个过程中有需要选择一个 shortname，完成后，你可以在设置页码找到你的 shortname

```url
https://YOURSHORTNAMEHERE.disqus.com/admin/settings/general
```

在你Hexo博客里打开 _config.yml, 然后输入 disqus_shortnameand: YOURSHORTNAMEHERE，像这样：

<!-- more -->

```bash
disqus_shortname: myshortnamegoeshere
comments: true
```

也需要更改_config.yml文件如下，例如我的：

```bash
# 修改默认 url: http://yoursite.com 为：
url: https://shenxianpeng.github.io
```

复制这段代码到blog\themes\landscape\layout\_partial\footer.ejs

```js
<% if (config.disqus_shortname){ %>
<script>
  var disqus_shortname = '<%= config.disqus_shortname %>';
  <% if (page.permalink){ %>
  var disqus_url = '<%= page.permalink %>';
  <% } %>
  (function(){
    var dsq = document.createElement('script');
    dsq.type = 'text/javascript';
    dsq.async = true;
    dsq.src = '//go.disqus.com/<% if (page.comments){ %>embed.js<% } else { %>count.js<% } %>';
    (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
  })();
</script>
<% } %>
```

也需要复制这些文件到 footer.ejs 到最底部：

```js
<div id="disqus_thread"></div>
```

最后最footer.ejs文件是这样的：

```js
<% if (theme.sidebar === 'bottom'){ %>
  <%- partial('_partial/sidebar') %>
<% } %>

<% if (config.disqus_shortname){ %>
  <script>
    var disqus_shortname = '<%= config.disqus_shortname %>';
    <% if (page.permalink){ %>
    var disqus_url = '<%= page.permalink %>';
    <% } %>
    (function(){
      var dsq = document.createElement('script');
      dsq.type = 'text/javascript';
      dsq.async = true;
      dsq.src = '//go.disqus.com/<% if (page.comments){ %>embed.js<% } else { %>count.js<% } %>';
      (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
    })();
  </script>
<% } %>

<footer id="footer">
  <div class="outer">
    <div id="footer-info" class="inner">
      &copy; <%= date(new Date(), 'YYYY') %> <%= config.author || config.title %><br>
      <%= __('powered_by') %> <a href="http://hexo.io/" target="_blank">Hexo</a>
    </div>
  </div>
</footer>

<div id="disqus_thread"></div>
```

最后清理和构建

```bash
hexo clean
hexo generate && hexo server
```

现在你可以看到我的博客已经可以添加评论了 : )
