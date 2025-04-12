---
title: Markdown 不香了吗？为什么越来越多 Python 项目用 RST？
tags:
  - Markdown
  - RST
categories:
  - DevOps
author: shenxianpeng
date: 2025-04-11 01:00:00
---

在日常工作中，无论是写 README、写博客，还是写项目文档，我们总要选择一种标记语言来排版内容。

目前主流的有两种：**Markdown** 和 **reStructuredText（简称 RST）**。

那它们之间到底有什么区别？又该在什么场景下选哪个呢？

最近我将 [gitstats](https://github.com/shenxianpeng/gitstats) 项目的文档从 Markdown 转换为 RST，并发布到 [ReadTheDocs](https://gitstats.readthedocs.io/) 上，这篇文章就来聊聊我的一些实践体会。

<!-- more -->

## Markdown 是什么？

Markdown 是一种轻量级标记语言，最早由 John Gruber 和 Aaron Swartz 在 2004 年设计，目标是让文档尽可能「可读、可写、可转换为结构良好的 HTML」。

**优点：**

- 语法简单、容易上手
- 社区支持广泛（GitHub、GitLab、Hexo、Jekyll 等等都支持）
- 渲染速度快，格式一致性好

**常见用途：**

- README.md
- 博客文章
- 简单的项目文档

## RST 是什么？

RST 是 Python 社区使用较多的一种标记语言，由 Docutils 项目维护。相比 Markdown，语法更丰富，也更严格一些。

**优点：**

- 原生支持脚注、交叉引用、自动索引、代码文档化等高级功能
- 是 Sphinx 的首选格式，适合大型项目的文档编写
- 对结构化文档更友好

**常见用途：**

- Python 项目的文档（如官方文档）
- 使用 Sphinx 生成的技术手册
- 多语言文档（结合 gettext）

## 语法对比小结

| 功能             | Markdown                    | RST                            |
|------------------|-----------------------------|--------------------------------|
| 标题             | `#` 开头                    | `=====` 或 `-----` 下划线       |
| 粗体 / 斜体       | `**text**` / `*text*`        | `**text**` / `*text*`        |
| 超链接           | `[text](url)`               | `` `text <url>`_ ``            |
| 表格             | 简单表格（扩展支持）        | 需要严格缩进，写法复杂           |
| 脚注 / 引用       | 不支持 / 限制较多           | 原生支持                         |
| 交叉引用         | 不支持                      | 原生支持                         |

Markdown 更轻松，RST 更专业。

## 什么时候用 Markdown？

- 项目较小，只需写简单说明文档
- 团队成员不熟悉 RST，想快速写文档
- 写博客、日常笔记更推荐 Markdown
- 使用平台（如 GitHub Pages、Hexo）默认支持 Markdown

一句话：**轻量文档首选 Markdown**。

## 什么时候用 RST？

- 使用 **Sphinx** 生成 API 文档或技术手册
- 项目结构复杂，需要自动索引、交叉引用、模块文档等高级功能
- 需要与 Python 工具链（如 `autodoc`, `napoleon` 等）集成
- 要发布到 ReadTheDocs（虽然现在也支持 Markdown，但 RST 体验更好）

一句话：**Python 项目或结构化技术文档推荐 RST**。

## 我个人的建议

如果你是：

- **开发工程师**，日常文档写 Markdown 足够
- **Python 开发者**，建议学一下 RST，特别是用 Sphinx 写文档时
- **开源项目维护者**，项目规模不大，README 用 Markdown 就好；但文档站点可以考虑用 RST + Sphinx 构建

## 总结一句话

> Markdown 更像是写字的便利贴，RST 更像是写书的排版系统。

选哪个，其实就看你的目标是写“随笔”还是写“手册”。

如果你对 Markdown、RST 或文档构建工具有自己的心得，欢迎留言交流。

下期我打算分享下 Sphinx 配置和 ReadTheDocs 自动发布的经验～

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
