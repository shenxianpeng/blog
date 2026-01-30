#!/bin/bash
# 下载周刊图片的 Shell 脚本（不依赖 Python requests）
# 用法: bash download_weekly_images.sh <weekly_dir>
# 示例: bash download_weekly_images.sh content/posts/2026/weekly-3

set -e

WEEKLY_DIR="$1"

if [ -z "$WEEKLY_DIR" ]; then
    echo "用法: bash download_weekly_images.sh <weekly_dir>"
    echo "示例: bash download_weekly_images.sh content/posts/2026/weekly-3"
    exit 1
fi

# 创建目录
mkdir -p "$WEEKLY_DIR"

echo "📁 处理周刊目录: $WEEKLY_DIR"
echo "📥 开始下载图片..."
echo ""

# 下载函数
download_image() {
    local filename="$1"
    local url="$2"
    local filepath="$WEEKLY_DIR/$filename"
    
    if [ -f "$filepath" ]; then
        echo "⏭️  已存在，跳过: $filename"
        return 0
    fi
    
    echo "📥 下载: $filename"
    if curl -L -s -o "$filepath" "$url" --max-time 15; then
        echo "✅ 成功: $filename"
        return 0
    else
        echo "❌ 失败: $filename"
        return 1
    fi
}

# 封面图
download_image "featured.png" "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1200&h=630&fit=crop&q=80"

# 行业动态
download_image "news-1.png" "https://github.githubassets.com/assets/hero-drone-82106eb07f6e.jpg"
download_image "news-2.png" "https://raw.githubusercontent.com/kubernetes/kubernetes/master/logo/logo.png"
download_image "news-3.png" "https://about.gitlab.com/images/press/logo/png/gitlab-icon-rgb.png"

# 深度阅读
download_image "blog-1.jpg" "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&h=450&fit=crop&q=80"
download_image "blog-2.png" "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=450&fit=crop&q=80"
download_image "blog-3.jpg" "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=450&fit=crop&q=80"

# 效率工具 - 使用 Unsplash 通用图
download_image "tool-1.png" "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&h=450&fit=crop&q=80"
download_image "tool-2.jpg" "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=800&h=450&fit=crop&q=80"
download_image "tool-3.png" "https://images.unsplash.com/photo-1518432031352-d6fc5c10da5a?w=800&h=450&fit=crop&q=80"

# AI 相关
download_image "ai-1.png" "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=800&h=450&fit=crop&q=80"
download_image "ai-2.jpg" "https://images.unsplash.com/photo-1676277791608-ac3b90836e6e?w=800&h=450&fit=crop&q=80"
download_image "ai-3.png" "https://images.unsplash.com/photo-1675557009997-ded49f9fc920?w=800&h=450&fit=crop&q=80"

# 学习资源
download_image "resource-1.jpg" "https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=800&h=450&fit=crop&q=80"
download_image "resource-2.png" "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800&h=450&fit=crop&q=80"

echo ""
echo "✅ 图片下载完成！"
echo "📁 保存位置: $WEEKLY_DIR"
