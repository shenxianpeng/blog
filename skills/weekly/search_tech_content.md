# 搜索技术内容

## 描述
搜索 DevOps、AI 工程化、CI/CD 和 Build 领域的最新技术内容，包括博客文章、新闻、开源项目等。

## 输入
- `time_range`: 时间范围（如 "过去7天"、"2026年1月"）
- `content_type`: 内容类型（news/blog/tool/project/resource）
- `keywords`: 搜索关键词（可选）

## 过程

### 1. 确定搜索源和关键词

根据内容类型选择合适的搜索源：

**博客文章（blog）：**
- Medium: `site:medium.com DevOps [时间]`
- Medium AI: `site:medium.com AI engineering [时间]`
- Dev.to: `site:dev.to DevOps [时间]`
- Dev.to CI/CD: `site:dev.to CI/CD [时间]`
- AWS Blog: `site:aws.amazon.com/blogs DevOps`
- Google Cloud Blog: `site:cloud.google.com/blog AI`
- Azure Blog: `site:devblogs.microsoft.com Azure DevOps`
- Netflix: `Netflix TechBlog engineering`
- Uber: `Uber Engineering blog`
- Spotify: `site:engineering.atspotify.com`
- GitHub: `site:github.blog engineering`

**行业新闻（news）：**
- `DevOps news [时间]`
- `AI engineering news [时间]`
- `Kubernetes updates [时间]`
- `cloud native news [时间]`
- `site:techcrunch.com DevOps`
- `site:infoq.com DevOps`

**开源项目/工具（tool/project）：**
- `GitHub trending DevOps`
- `GitHub trending AI`
- `DevOps tools 2026`
- `AI developer tools`
- `CI/CD automation tools`
- `MLOps tools`
- `site:github.com awesome-devops`

**学习资源（resource）：**
- `DevOps tutorial [时间]`
- `AI engineering course`
- `Kubernetes best practices`
- `CI/CD guide`
- `site:freecodecamp.org DevOps`

**综合搜索：**
- Hacker News: `site:news.ycombinator.com DevOps`
- Reddit DevOps: `site:reddit.com/r/devops`
- Reddit ML: `site:reddit.com/r/MachineLearning`

### 2. 执行搜索

使用 Web Search 工具搜索每个来源，收集最近发布的高质量内容。

### 3. 筛选和验证

对搜索结果进行筛选：
- ✅ 检查发布日期是否在指定时间范围内
- ✅ 验证内容质量（是否有实践案例、代码示例、深度分析）
- ✅ 优先选择知名平台和公司官方博客
- ✅ 验证链接可访问性
- ❌ 排除营销软文和低质量内容
- ❌ 排除无法访问的链接

### 4. 提取关键信息

对每条内容提取：
- 标题
- 原始链接（非重定向链接）
- 发布日期
- 来源平台/作者
- 内容摘要（50-100字）
- 推荐理由（为什么值得关注）

## 输出

返回结构化的内容列表：

```json
{
  "content_type": "blog",
  "time_range": "2026-01-11 至 2026-01-18",
  "items": [
    {
      "title": "文章标题",
      "url": "https://...",
      "source": "Medium / AWS Blog / etc.",
      "published_date": "2026-01-15",
      "summary": "内容摘要，50-100字",
      "why_matters": "为什么值得关注的理由",
      "language": "英文/中文"
    }
  ],
  "search_queries_used": ["使用的搜索查询列表"],
  "total_found": 10
}
```

## 质量标准

- 博客文章必须包含实践案例、代码示例或架构图
- 新闻必须来自可信来源，有事实依据
- 工具/项目必须是活跃维护的，有实际使用价值
- 所有内容必须与 DevOps/AI/CI/CD/Build 领域相关
- 优先推荐大公司官方博客和知名技术平台的内容
