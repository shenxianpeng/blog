# Copilot Skills 使用指南

这个目录包含了用于自动化生成博客内容的 GitHub Copilot Skills。

## 📁 目录结构

```
skills/
└── weekly/           # 攻城狮周刊生成相关 skills
    ├── generate_weekly.md        # 主流程：生成完整周刊
    ├── search_tech_content.md    # 搜索技术内容
    ├── fetch_github_info.md      # 获取 GitHub 项目信息
    ├── verify_links.md           # 验证链接有效性
    └── download_images.md        # 下载和管理图片
```

## 🚀 快速开始

### 生成攻城狮周刊

使用 `@workspace #file:generate_weekly.md` 来生成周刊。

#### 示例：生成第 3 期周刊（2026 年）

```
@workspace #file:generate_weekly.md 请生成第 3 期攻城狮周刊
- week_number: 3
- start_date: 2026-01-11
- end_date: 2026-01-17
```

这将自动：
1. 搜索本周的技术动态、博客文章、工具和项目
2. 验证所有 GitHub 项目的真实 Star 数
3. 验证所有链接的有效性
4. 下载相关图片到周刊目录
5. 生成完整的周刊文件：`content/posts/2026/weekly-3/index.md`

#### 输出结构

```
content/posts/2026/weekly-3/
├── index.md           # 周刊内容（带 Hugo Front Matter）
├── featured.png       # 封面图（Hugo 自动识别）
├── news-1.png         # 行业动态图片
├── blog-1.jpg         # 深度阅读图片
├── tool-1.png         # 效率工具图片
├── ai-1.png           # AI 项目图片
└── resource-1.jpg     # 学习资源图片
```

### 其他年份示例

生成 2027 年第 1 期：
```
@workspace #file:generate_weekly.md 请生成第 1 期攻城狮周刊
- week_number: 1
- start_date: 2027-01-02
- end_date: 2027-01-08
```

输出：`content/posts/2027/weekly-1/index.md`

## 📝 单独使用各个 Skill

### 搜索技术内容

```
@workspace #file:search_tech_content.md 搜索最近 7 天的 DevOps 博客文章
```

### 获取 GitHub 项目信息

```
@workspace #file:fetch_github_info.md 获取 kubernetes/kubernetes 的项目信息
```

### 验证链接

```
@workspace #file:verify_links.md 验证以下链接的有效性：
- https://example.com/article1
- https://github.com/user/repo
```

### 下载图片

```
@workspace #file:download_images.md 下载图片到 content/posts/2026/weekly-3/
```

## 🎯 工作流程

完整的周刊生成流程：

```mermaid
graph TD
    A[开始] --> B[输入期数和日期]
    B --> C[搜索技术内容]
    C --> D[验证 GitHub 项目]
    D --> E[验证所有链接]
    E --> F[选择本周话题]
    F --> G[下载所有图片]
    G --> H[生成周刊文件]
    H --> I[质量检查]
    I --> J[完成]
```

## 📋 前置要求

- GitHub Copilot 订阅
- VS Code with GitHub Copilot extension
- 能够访问互联网（用于搜索和下载）

## 💡 使用技巧

1. **灵活调整时间范围**：如果最近 7 天内容不足，可以扩展到 2 周
2. **手动筛选内容**：生成后可以手动调整内容顺序和筛选质量
3. **自定义话题**：可以根据当前热点自行修改本周话题
4. **图片优化**：如果自动下载的图片不合适，可以手动替换
5. **分步执行**：如果一次性生成有问题，可以分步使用各个 skill

## 🔍 常见问题

**Q: 生成的周刊放在哪里？**
A: 根据年份自动放置，格式为 `content/posts/{YEAR}/weekly-{NUMBER}/index.md`

**Q: 封面图为什么必须是 featured.png？**
A: Hugo 的 Blowfish 主题会自动识别 `featured.png` 作为文章封面图

**Q: 可以修改生成的内容吗？**
A: 当然可以！生成的内容是建议性的，你可以根据需要进行编辑和调整

**Q: 如果某个 GitHub 项目无法访问怎么办？**
A: Skill 会自动跳过无法访问的项目，并在生成时提示

**Q: 生成的周刊包含哪些章节？**
A: 包括：本周封面、本周话题、行业动态、深度阅读、效率工具、AI 相关、学习资源、精彩摘要、行业观点

## 📚 更多信息

- [Hugo 文档](https://gohugo.io/documentation/)
- [Blowfish 主题文档](https://blowfish.page/)
- [博客项目主页](https://github.com/shenxianpeng/blog)
