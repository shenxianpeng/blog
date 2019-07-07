---
title: Hexo 添加留言功能
date: 2019-07-07 20:20:50
tags: hexo
---

# 在你的Hexo网站添加Disqus

1. 去Disqus创建一个账号，在这个过程中有需要选择一个shortname，完成后，你可以在设置页码找到你的shortname。
```
https://YOURSHORTNAMEHERE.disqus.com/admin/settings/general
```
2. 在你Hexo博客里打开_config.yml, 然后输入disqus_shortnameand: YOURSHORTNAMEHERE，像这样：
```
disqus_shortname: myshortnamegoeshere
comments: true
```
也需要更改_config.yml文件如下，例如我的：
```
url: https://shenxianpeng.github.io
```
3. 复制这段代码到blog\themes\landscape\layout\_partial\footer.ejs
```
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
Also in footer.ejs, paste in the following markup where you want the comments to go.
也需要复制这些文件到footer.ejs到最底部:
```
<div id="disqus_thread"></div>
```
最后最footer.ejs文件是这样的：
```
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
4. 最后清理和构建
```
$ hexo clean
$ hexo generate && hexo server
```

现在你可以看到我的博客已经可以添加评论了 : )




