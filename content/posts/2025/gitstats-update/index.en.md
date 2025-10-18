---
title: 🚀 gitstats Upgrade Arrives—JSON Output, Cross-Platform Compatibility, and Code Refactoring!
summary: |
  After two months of continuous improvement, gitstats now supports JSON output, code refactoring, argparse replacing getopt, and full compatibility with Windows and macOS. Welcome to use and Star support!
tags:
  - GitStats
  - Git
authors:
  - shenxianpeng
date: 2025-02-05
---

Hello everyone! Since my last post [announcing the start of maintaining **gitstats**](../gitstats/), I've been continuously improving this project. Here are the major updates over the past two months:

## ✨ New Features and Improvements



1. **Support for Generating JSON Files**
   In addition to the original HTML report, gitstats can now generate JSON files!
   **Use Case**: Facilitates secondary development or programmatic use for developers, meeting more customized needs.
   **Origin**: This feature was implemented quickly based on user feedback.

2. **Code Refactoring**
   A significant amount of refactoring and optimization has been performed on the previously mixed code.
   **Benefits**: The code structure is clearer and easier to maintain, laying the foundation for writing unit tests.

3. **Replacing getopt**
   The deprecated `getopt` has been replaced with the more modern **argparse**.
   **Advantages**: Improves code readability and maintainability.

4. **Cross-Platform Support**
   In addition to Linux, gitstats has now been fully tested on **Windows** and **macOS**.
   **Testing**: I've conducted thorough testing on all three platforms to ensure real-time availability.

## 📅 Next Steps

1. **Support for Theme Switching**
   In addition to the default theme, I plan to add a **Dark Mode**, catering to different user visual preferences.

2. **Unit Testing and Coverage**
   Unit tests will be added, and coverage will be increased to **100%** (a small goal) to prevent regression bugs.

## 💡 Your Needs Matter!

If you have any other needs or feature suggestions, feel free to visit the following repository address and submit an Issue: 👉 [https://github.com/shenxianpeng/gitstats](https://github.com/shenxianpeng/gitstats)

## 🌟 Welcome to Use and Support

If you find gitstats helpful, welcome to **Star🌟** it! Your recognition is the motivation for my continuous improvement!

What new features would you like to see added to gitstats?  Feel free to leave a comment or directly submit an Issue on GitHub!

---

Please indicate the author and source when reprinting this article, and do not use it for any commercial purposes. Welcome to follow the WeChat official account "DevOps攻城狮"