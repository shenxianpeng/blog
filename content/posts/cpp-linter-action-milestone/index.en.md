---
title: Microsoft and NASA Use It? My 4-Year-Old Side Project Hit 100 Stars
summary: |
  cpp-linter-action is a GitHub Action that provides C/C++ code formatting and static analysis capabilities. It uses clang-format and clang-tidy, supporting various configurations and custom rules.  Since its creation in 2021, the project has been used by several well-known organizations and open-source projects.
tags:
  - clang-format
  - clang-tidy
  - clang
  - cpp-linter
author: shenxianpeng
date: 2025-04-15
---

Last week, the open-source project I created and maintain, [cpp-linter-action](https://github.com/cpp-linter/cpp-linter-action), reached a small milestone:

> 🌟 GitHub Star count surpassed 100!

While this number isn't huge, it's a small milestone for me—it's the first time one of my projects has received over 100 stars on GitHub.  It's a validation of the project and gives me the motivation to continue maintaining it.

My first commit to this project was on **April 26, 2021**, and almost 4 years have passed. Looking back, I'm glad I haven't been idle and have left behind something useful for others.

As the project has evolved, so has its user base.  I estimate that thousands of projects are currently using this Action.

These include several well-known organizations and open-source projects, such as:

* Microsoft
* Apache
* NASA
* CachyOS
* nextcloud
* Jupyter

Most importantly, this process has taught me many new skills and knowledge, and it's maintained a "side hustle" habit for me:

> My phone isn't just for WeChat and Douyin (TikTok), but also for GitHub.

This project also became a springboard for my subsequent work. I later created the [cpp-linter](https://github.com/cpp-linter) organization to maintain and release binary versions and Docker images of `clang-tools` with other developers. I also developed [cpp-linter-hooks](https://github.com/cpp-linter/cpp-linter-hooks), providing users with `clang-format` and `clang-tidy` pre-commit hooks for easier use.

Without being immodest:

> If your project is developed in C/C++, and you want to use `clang-format` and `clang-tidy`, then cpp-linter is an unavoidable option.

Finally, I welcome your feedback and suggestions, and you're welcome to contact me via [Issue](https://github.com/cpp-linter/cpp-linter-action/issues) or [Discussions](https://github.com/orgs/cpp-linter/discussions)!

If you find this project helpful, please leave a message on the WeChat official account "DevOps攻城狮" or give the project a star on GitHub to show your support!

—— Written on 2025-04-15 12:49 AM
