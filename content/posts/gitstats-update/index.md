---
title: 🚀 gitstats 升级来袭：支持 JSON 输出、多平台兼容、代码重构！
summary: |
  gitstats 经过两个月的持续改进，现已支持 JSON 输出、代码重构、argparse 替换 getopt，并全面兼容 Windows 和 macOS。欢迎使用和 Star 支持！
tags:
  - GitStats
  - Git
author: shenxianpeng
date: 2025-02-05
---

大家好！自从上次发文[宣布开始维护 **gitstats**](https://shenxianpeng.github.io/2024/11/gitstats/) 以来，我一直在不断地改进这个项目，下面是这两个月的主要更新内容：

## ✨ 新增功能与改进



1. **支持生成 JSON 文件**
   除了原有的 HTML 报告，现在 gitstats 还可以生成 JSON 文件！
   **用途**：方便开发者进行二次开发或编程使用，满足更多定制化需求。
   **来源**：根据用户反馈，迅速实现了这一功能。

2. **代码重构**
   对原本混杂在一起的代码进行了大量拆分和优化。
   **好处**：代码结构更清晰，易于维护，同时为编写单元测试奠定了基础。

3. **替换 getopt**
   使用更现代的 **argparse** 替换了已弃用的 getopt。
   **优势**：提升了代码的可读性和可维护性。

4. **多平台支持**
   除了 Linux，gitstats 现在已全面对 **Windows** 和 **macOS** 进行了测试。
   **测试**：我在这三个平台上进行了充分测试，确保实时可用。

## 📅 下一步计划

1. **支持主题切换**
   除了默认主题，计划增加 **黑暗模式（Dark Mode）**，满足不同用户的视觉偏好。

2. **单元测试与覆盖率**
   将增加单元测试，并将覆盖率提升至 **100%**（小目标），避免回归 Bug。

## 💡 你的需求很重要！

如果你有其他需求或功能建议，欢迎随时访问以下仓库地址，提 Issue 告诉我：👉 [https://github.com/shenxianpeng/gitstats](https://github.com/shenxianpeng/gitstats)

## 🌟 欢迎使用与支持

如果你觉得 gitstats 对你有帮助，欢迎 **Star🌟** 支持！你的认可是我持续改进的动力！

你希望 gitstats 增加哪些新功能？欢迎在评论区留言，或直接到 GitHub 提 Issue！

---

转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
