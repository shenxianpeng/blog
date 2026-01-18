# 下载和管理周刊图片

## 描述
为周刊的各个章节下载和管理相关图片，增强内容的可读性和吸引力。

## 输入
- `weekly_path`: 周刊目录路径（如 `content/posts/2026/weekly-3/`）
- `content_sections`: 周刊内容的各个章节及其关键词

## 过程

### 步骤 1：确定图片需求

为以下章节准备图片（**不包括"行业观点"**）：

1. **本周封面** - 1张主题图片
2. **行业动态** - 每条新闻 1 张相关图片
3. **深度阅读** - 每篇文章 1 张相关图片
4. **效率工具** - 每个工具的 logo 或截图
5. **AI 相关** - 每个项目的 logo 或架构图
6. **学习资源** - 每个资源的封面图或相关图片
7. **精彩摘要** - 可选，视情况添加

### 步骤 2：图片来源策略

**优先顺序：**

1. **官方来源**（最优先）
   - 项目 GitHub README 中的图片
   - 官方网站的 logo 和截图
   - 官方博客文章中的配图

2. **开源图库**
   - Unsplash (https://unsplash.com/) - 免费高质量图片
   - Pexels (https://www.pexels.com/) - 免费商用图片
   - GitHub Social Preview - `https://opengraph.githubassets.com/{hash}/owner/repo`

3. **技术相关图片**
   - 技术 logo（如 Kubernetes、Docker、AWS 等）
   - 架构图、流程图
   - 代码截图

### 步骤 3：下载图片

对每张图片：

1. **访问图片源 URL**
2. **下载图片到周刊目录**
   - 路径格式：`content/posts/{YEAR}/weekly-{week_number}/`
   - 示例：`content/posts/2026/weekly-3/featured.png`
   - 命名规范：`{section}-{index}.{ext}`
     - 例如：`featured.png`, `news-1.png`, `tool-2.jpg`
3. **记录图片元数据**
   - 原始 URL
   - 来源说明
   - 版权信息（如需要）

### 步骤 4：更新 Markdown 引用

在 markdown 中使用**相对路径**引用图片：

```markdown
## 本周封面

![本周封面](featured.png)

简单的解决方案往往比复杂的架构更稳定。（[via Unsplash](原始URL)）

## 行业动态

1、[AWS 发布 DevOps Agent](链接)

![AWS DevOps Agent](news-1.png)

AWS 在 re:Invent 2025 上发布了 DevOps Agent...

## 深度阅读

1、[Why Service Mesh Never Took Off](链接)（英文）

![Service Mesh](blog-1.jpg)

这篇文章分析了为什么 Service Mesh 技术...

## 效率工具

1、[AionUi](https://github.com/iOfficeAI/AionUi)

![AionUi Logo](tool-1.png)

一个免费、本地、开源的 AI 编程助手 UI...

## AI 相关

1、[LEANN](https://github.com/yichuan-w/LEANN)

![LEANN Architecture](ai-1.png)

在个人设备上运行快速、准确且 100% 私密的 RAG 应用...
```

## 图片选择建议

### 行业动态
- 公司/产品 logo
- 产品截图
- 相关技术栈图标

### 深度阅读
- 文章原始配图（如果有）
- 相关技术概念图
- 架构图或流程图

### 效率工具
- 工具 logo（优先）
- 工具界面截图
- GitHub Social Preview 图

### AI 相关
- 项目 logo
- 架构图
- 示例效果图

### 学习资源
- 课程/教程封面
- 相关技术图标
- 示意图

## 图片规范

### 尺寸
- **封面图**：建议 1200x630px（适合社交分享）
- **章节图片**：建议 800x450px 或 16:9 比例
- **Logo/图标**：建议 400x400px 或原始尺寸

### 格式
- 优先使用 **JPG**（照片）或 **PNG**（logo、截图）
- WebP 格式可选（更小的文件大小）
- 避免使用 GIF（除非必要的动画）

### 文件命名
```
featured.png          # 封面图（固定名称，Hugo 自动识别）
news-{n}.{ext}        # 行业动态第 n 条
blog-{n}.{ext}        # 深度阅读第 n 篇
tool-{n}.{ext}        # 效率工具第 n 个
ai-{n}.{ext}          # AI 相关第 n 个
resource-{n}.{ext}    # 学习资源第 n 个
quote-{n}.{ext}       # 精彩摘要第 n 个（可选）
```

## 版权和归属

### 必须包含的信息
- Unsplash/Pexels 图片：在图片说明中添加 `(via Unsplash/Pexels)`
- 官方图片：在图片说明中标注来源
- GitHub 项目：可以使用项目中的图片（遵循项目许可证）

### 示例
```markdown
![](featured.png)
DevOps 工程师在工作。（[via Unsplash](https://unsplash.com/photos/xxx)）

![](tool-1.png)
AionUi 界面截图。（[via GitHub](https://github.com/iOfficeAI/AionUi)）
```

## 输出

图片文件保存在周刊目录中：
- 路径：`content/posts/{YEAR}/weekly-{week_number}/`
- 每个章节的内容都应该包含：
  1. 相关的图片文件（保存在周刊目录）
  2. Markdown 中的图片引用（使用相对路径，如 `![](featured.png)`）
  3. 图片来源说明

## 注意事项

- ❌ **不要为"行业观点"章节添加图片**
- ✅ 优先使用官方图片和开源图片
- ✅ 确保图片文件名简洁且有意义
- ✅ 保持图片质量，避免模糊或低分辨率
- ✅ 图片应与内容相关，不要随意配图
- ✅ 如果找不到合适的图片，可以不配图，不要强行配不相关的图片
