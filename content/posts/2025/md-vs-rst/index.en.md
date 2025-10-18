---
title: Markdown — Not So Great Anymore? Why More and More Python Projects Use RST?
summary: |
  Markdown and reStructuredText (RST) are two commonly used markup languages. This article compares their advantages and disadvantages and shares usage suggestions in different scenarios.
tags:
  - Markdown
  - RST
authors:
  - shenxianpeng
date: 2025-04-11
---

In daily work, whether writing READMEs, blogs, or project documentation, we always need to choose a markup language to format the content.

Currently, there are two mainstream choices: **Markdown** and **reStructuredText (RST)**.

What are the differences between them? And which one should be chosen in what scenario?

Recently, I converted the documentation of the [gitstats](https://github.com/shenxianpeng/gitstats) project from Markdown to RST and published it on [ReadTheDocs](https://gitstats.readthedocs.io/). This article will discuss some of my practical experiences.



## What is Markdown?

Markdown is a lightweight markup language, originally designed by John Gruber and Aaron Swartz in 2004, aiming to make documents as "readable, writable, and convertible to well-formed HTML" as possible.

**Advantages:**

- Simple syntax, easy to learn
- Wide community support (GitHub, GitLab, Hexo, Jekyll, etc., all support it)
- Fast rendering speed, good format consistency

**Common Uses:**

- README.md
- Blog posts
- Simple project documentation

## What is RST?

RST is a markup language used more frequently in the Python community, maintained by the Docutils project. Compared to Markdown, its syntax is richer and stricter.

**Advantages:**

- Native support for footnotes, cross-references, automatic indexing, code documentation, and other advanced features
- The preferred format for Sphinx, suitable for large-scale project documentation
- More friendly to structured documents

**Common Uses:**

- Documentation for Python projects (such as official documentation)
- Technical manuals generated using Sphinx
- Multilingual documentation (in conjunction with gettext)

## Syntax Comparison Summary

| Feature             | Markdown                    | RST                            |
|------------------|-----------------------------|--------------------------------|
| Heading             | `#` at the beginning        | `=====` or `-----` underline       |
| Bold / Italic       | `**text**` / `*text*`        | `**text**` / `*text*`        |
| Hyperlink           | `[text](url)`               | `` `text <url>`_ ``            |
| Table             | Simple tables (extension supported)        | Requires strict indentation, complex writing           |
| Footnote / Citation | Unsupported / Highly limited           | Native support                         |
| Cross-reference     | Unsupported                      | Native support                         |

Markdown is easier, RST is more professional.

## When to Use Markdown?

- For smaller projects requiring only simple documentation
- When team members are unfamiliar with RST and want to write documentation quickly
- For blogs and daily notes, Markdown is more recommended
- When the platform used (such as GitHub Pages, Hexo) supports Markdown by default

In short: **Markdown is the preferred choice for lightweight documents.**

## When to Use RST?

- When using **Sphinx** to generate API documentation or technical manuals
- When the project structure is complex and requires advanced features such as automatic indexing, cross-referencing, and module documentation
- When integration with the Python toolchain (such as `autodoc`, `napoleon`, etc.) is required
- When publishing to ReadTheDocs (although it now supports Markdown, the RST experience is better)

In short: **RST is recommended for Python projects or structured technical documents.**

## My Personal Suggestion

If you are:

- A **development engineer**, using Markdown for daily documentation is sufficient
- A **Python developer**, it's recommended to learn RST, especially when using Sphinx to write documentation
- An **open-source project maintainer**, for small-scale projects, using Markdown for the README is fine; but for documentation sites, consider using RST + Sphinx for building

## Summary in One Sentence

> Markdown is more like a convenient notepad for writing, while RST is more like a typesetting system for writing books.

The choice depends on whether your goal is to write "notes" or "manuals".

If you have your own insights on Markdown, RST, or documentation building tools, please feel free to leave a comment and share.

Next time, I plan to share my experience with Sphinx configuration and automatic publication to ReadTheDocs～

---

Please indicate the author and source when reprinting this article, and do not use it for any commercial purposes. Welcome to follow the WeChat official account "DevOps攻城狮"