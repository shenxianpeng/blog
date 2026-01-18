# 验证链接可访问性

## 描述
验证一组 URL 是否可访问，确保周刊中的所有链接都是有效的。

## 输入
- `urls`: URL 列表
- `timeout`: 超时时间（秒，默认 10）

## 过程

### 1. 准备验证

对每个 URL 进行预处理：
- 移除 Google 重定向链接前缀
- 提取实际的目标 URL
- 标准化 URL 格式

常见重定向模式：
```
❌ https://vertexaisearch.cloud.google.com/grounding-api-redirect/...
✅ 提取其中的实际目标 URL
```

### 2. 执行验证

对每个 URL：
1. 发送 HTTP HEAD 请求（更快，不下载内容）
2. 检查响应状态码
3. 记录响应时间
4. 捕获任何错误

### 3. 分类结果

根据状态码分类：

**✅ 可访问（推荐使用）：**
- 200 OK：正常访问
- 301/302：重定向（记录最终 URL）

**⚠️ 需要注意：**
- 403 Forbidden：可能需要登录或有地区限制
- 429 Too Many Requests：速率限制
- 503 Service Unavailable：临时不可用

**❌ 不可访问（不要使用）：**
- 404 Not Found：页面不存在
- 500 Internal Server Error：服务器错误
- Timeout：请求超时
- Connection Error：连接失败

### 4. 处理重定向

如果遇到重定向：
- 跟踪重定向链（最多 5 次）
- 返回最终的目标 URL
- 建议使用最终 URL 而不是重定向 URL

## 输出

返回验证结果：

```json
{
  "total_checked": 10,
  "accessible": 8,
  "inaccessible": 2,
  "results": [
    {
      "original_url": "https://example.com/article",
      "final_url": "https://example.com/article",
      "status_code": 200,
      "status": "accessible",
      "redirected": false,
      "response_time_ms": 234,
      "error": null
    },
    {
      "original_url": "https://example.com/old-page",
      "final_url": "https://example.com/new-page",
      "status_code": 301,
      "status": "accessible",
      "redirected": true,
      "redirect_chain": [
        "https://example.com/old-page",
        "https://example.com/new-page"
      ],
      "response_time_ms": 456,
      "error": null,
      "recommendation": "使用最终 URL: https://example.com/new-page"
    },
    {
      "original_url": "https://example.com/not-found",
      "final_url": null,
      "status_code": 404,
      "status": "inaccessible",
      "redirected": false,
      "response_time_ms": 123,
      "error": "Not Found",
      "recommendation": "不要包含在周刊中"
    }
  ]
}
```

## 批量处理

为提高效率：
- 并发检查多个 URL（建议 5-10 个并发）
- 设置合理的超时时间
- 使用连接池复用连接
- 添加适当的延迟避免被封禁

## 特殊处理

某些网站可能需要特殊处理：

**需要 User-Agent：**
- 设置真实的浏览器 User-Agent
- 示例：`Mozilla/5.0 ...`

**GitHub：**
- GitHub 很稳定，通常不需要验证
- 但仍建议检查 404（仓库已删除）

**Medium / Dev.to：**
- 可能有速率限制
- 建议添加延迟

## 使用建议

在生成周刊时：
1. 收集所有待包含的 URL
2. 批量验证所有链接
3. 移除不可访问的链接
4. 使用重定向后的最终 URL
5. 记录验证结果供参考
