# 生成攻城狮周刊

## 描述
自动生成《攻城狮周刊》，涵盖 DevOps、AI 工程化、CI/CD 和 Build 领域的最新技术动态。

## 输入
- `week_number`: 期数（如第 3 期）
- `start_date`: 开始日期（格式：YYYY-MM-DD）
- `end_date`: 结束日期（格式：YYYY-MM-DD）

## 文件路径规则

根据当前年份自动确定周刊存储路径：
- 路径格式：`content/posts/{YEAR}/weekly-{week_number}/index.md`
- 年份从 `start_date` 或 `end_date` 中提取
- 示例：2026 年第 3 期 → `content/posts/2026/weekly-3/index.md`
- 所有相关图片（封面图、章节图片等）保存在同一目录下

## 核心理念

- **致敬经典，但保持独特**：聚焦于 DevOps/AI/CI/CD/Build 领域
- **深度优于广度**：提供工程师视角的解读，不只是罗列新闻
- **高质量优先**：只推荐真正有价值的内容
- **真实性第一**：所有内容基于真实搜索，严禁编造

## 过程

### 步骤 1：收集各类内容

使用 **search_tech_content** skill 分别搜索：

1. **行业动态**（news）
   - 时间范围：最近 7 天
   - 关键词：DevOps news, AI engineering news, Kubernetes updates
   - 目标数量：5-8 条

2. **深度阅读**（blog）
   - 重点来源：Medium, Dev.to, AWS Blog, Google Cloud Blog, Netflix TechBlog 等
   - 时间范围：最近 2 周（如果 7 天内容不足）
   - 目标数量：3-5 篇高质量文章

3. **效率工具**（tool）
   - 搜索新发布或热门的 DevOps/AI 工具
   - GitHub Trending DevOps/AI 工具
   - 目标数量：3-5 个

4. **AI 相关**（project）
   - GitHub Trending AI 项目
   - 新兴的 AI 开发工具
   - 目标数量：2-3 个

5. **学习资源**（resource）
   - 教程、电子书、课程
   - 目标数量：1-2 个

### 步骤 2：验证 GitHub 项目

对所有涉及的 GitHub 项目，使用 **fetch_github_info** skill：
- 获取真实的 Star 数
- 验证项目是否活跃
- 获取项目描述和标签
- 确保项目可访问

### 步骤 3：验证所有链接

使用 **verify_links** skill：
- 收集所有内容中的链接
- 批量验证可访问性
- 移除 404 或不可访问的链接
- 使用重定向后的最终 URL

### 步骤 4：选择本周话题

从收集的内容中选择：
- 最热门、最具争议或影响深远的话题
- 能引发思考的技术趋势
- 撰写 200-300 字的卷首语
- 风格：像社论，有观点有洞察

### 步骤 5：选择封面图

- 从本周重要事件中选择有代表性的图片
- 或使用相关技术的官方图片
- 使用 **download_images** skill 下载图片到周刊目录，命名为 `featured.png`
- Hugo 会自动识别 `featured.png` 作为封面图
- 提供图片描述和来源链接

### 步骤 6：下载所有章节图片

使用 **download_images** skill：
- 为每个章节（除"行业观点"外）选择合适的图片
- 优先使用官方图片、GitHub Social Preview、Unsplash 等
- 图片保存路径：`content/posts/{YEAR}/weekly-{week_number}/`（与 markdown 文件相同目录）
- 使用相对路径引用图片（如 `![](cover.jpg)`）

### 步骤 7：创建周刊文件

创建文件：`content/posts/{YEAR}/weekly-{week_number}/index.md`

其中 `{YEAR}` 从 `start_date` 或 `end_date` 中提取，`{week_number}` 为输入的期数。

### 步骤 7：创建周刊文件

创建文件：`content/posts/{YEAR}/weekly-{week_number}/index.md`

其中 `{YEAR}` 从 `start_date` 或 `end_date` 中提取，`{week_number}` 为输入的期数。

按照以下结构组织周刊：

```markdown
---
title: "攻城狮周刊（第 {week_number} 期）：[本周话题标题]"
summary: "这里记录每周值得分享的 DevOps 与 AI 技术内容"
tags:
  - Weekly
  - DevOps
  - AI
  - CI/CD
authors:
  - shenxianpeng
date: {end_date}
---

本杂志[开源](https://github.com/shenxianpeng/blog)，欢迎[投稿](https://github.com/shenxianpeng/blog/issues)。合作请[邮件联系](mailto:xianpeng.shen@gmail.com)（xianpeng.shen@gmail.com）。

## 本周封面

![](featured.png)

[图片描述]。（[via](来源链接)）

## [本周话题标题]

[卷首语内容，200-300字...]

## 行业动态

1、[新闻标题](链接)

![](news-1.png)

[新闻简介，50-100字。]

[攻城狮视角的点评。]

2、[新闻标题](链接)

![](news-2.jpg)

...

## 深度阅读

1、[文章标题](链接)（英文/中文）

![](blog-1.jpg)

[文章简介：核心观点、为什么值得读。]

2、[文章标题](链接)（英文/中文）

![](blog-2.png)

...

## 效率工具

1、[工具名称](链接)

![](tool-1.png)

[工具介绍和用途。]

2、[工具名称](链接)

![](tool-2.jpg)

...

## AI 相关

1、[项目名称](链接)

![](ai-1.png)

[AI 项目功能和特点。]

⭐ Star 数：{真实的 star 数}

2、[项目名称](链接)

![](ai-2.jpg)

...

## 学习资源

1、[资源名称](链接)

![](resource-1.jpg)

[资源介绍。]

## 精彩摘要

1、[文章标题](链接)

> [摘录有深度的文字段落]

## 行业观点

（注意：此章节不需要添加图片）

1、

> [言论内容]

-- [作者/来源](链接)

2、
...

（完）
```

### 步骤 8：质量检查

最后检查：
- ✅ 所有链接都是最终 URL，非重定向链接
- ✅ 所有 GitHub 项目都有真实的 Star 数
- ✅ 没有使用 "N/A" 或占位文本
- ✅ 每个章节都有实质内容（至少 2-3 条）
- ✅ 每个章节（除"行业观点"）都有相关图片
- ✅ 所有图片都保存在周刊目录中
- ✅ 图片引用使用相对路径
- ✅ 图片来源标注清晰
- ✅ 语言风格专业但有极客感
- ✅ 没有编造的日期、数据或事件
- ✅ 移除了所有 [cite: ...] 引用标记

## 输出

1. 创建目录（如果不存在）：`content/posts/{YEAR}/weekly-{week_number}/`
2. 生成完整的 Markdown 周刊文件：`content/posts/{YEAR}/weekly-{week_number}/index.md`
3. 下载所有图片到同一目录
4. 使用 Hugo Front Matter 格式包含元数据（title, summary, tags, authors, date）

## 内容质量标准

### 博客文章
- ✅ 有实践案例、代码示例、架构图
- ✅ 来自可信来源（知名平台或大公司博客）
- ✅ 最近发布（7 天内，最多 2 周）
- ❌ 纯理论或浅层介绍
- ❌ 营销软文

### 新闻
- ✅ 有事实依据
- ✅ 对 DevOps/AI 工程师有实际影响
- ✅ 提供攻城狮视角的点评
- ❌ 无关的科技新闻

### 工具/项目
- ✅ 活跃维护（6 个月内有更新）
- ✅ 有实际使用价值
- ✅ Star 数 > 100（或新兴但有潜力）
- ❌ 已归档或废弃的项目
- ❌ 低质量或玩具项目

### 学习资源
- ✅ 权威性、系统性
- ✅ 适合工程师学习
- ✅ 免费或开放访问
- ❌ 收费课程（除非特别优质）
- ❌ 过时的教程

## 语气风格

- 专业、客观，但带有工程师的极客感
- 避免营销号语气（"震惊！"、"必看！"等）
- 用数据和事实说话
- 可以有观点，但要有依据
- 简洁明了，不啰嗦

## 典型工作流示例

```
输入：
- week_number: 3
- start_date: 2026-01-11
- end_date: 2026-01-17

确定文件路径：
→ 从 end_date 提取年份: 2026
→ 目标路径: content/posts/2026/weekly-3/index.md
→ 图片目录: content/posts/2026/weekly-3/

1. 搜索行业动态
   → search_tech_content(content_type="news", time_range="过去7天")
   
2. 搜索深度博客
   → search_tech_content(content_type="blog", time_range="过去2周")
   
3. 搜索工具和项目
   → search_tech_content(content_type="tool")
   → search_tech_content(content_type="project")
   
4. 验证所有 GitHub 项目
   → fetch_github_info(repo_url="...")
   
5. 验证所有链接
   → verify_links(urls=[...])
   
6. 下载所有图片
   → download_images(target_dir="content/posts/2026/weekly-3/")
   
7. 生成周刊文件
   → 创建 content/posts/2026/weekly-3/index.md
   
8. 最终质量检查
```

## 注意事项

- **绝对不要编造内容**：所有信息必须来自真实搜索
- **移除引用标记**：不要在正文中显示 [cite: ...] 标记
- **真实的数据**：Star 数、日期等必须准确
- **高质量链接**：确保所有链接可访问
- **完整性**：每个章节都要有实质内容
- **时效性**：优先最近 7 天的内容
- **领域聚焦**：严格限定在 DevOps/AI/CI/CD/Build 领域
