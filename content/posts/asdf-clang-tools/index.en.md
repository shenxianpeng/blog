---
title: asdf-clang-tools—A New Way to Install Clang Tools Using asdf
summary: |
  asdf-clang-tools is an asdf plugin for installing and managing Clang Tools, such as clang-format, clang-tidy, clang-query, and clang-apply-replacements.
tags:
  - clang-tools
  - asdf
author: shenxianpeng
date: 2025-05-29
---

Recently, I released a new repository under the cpp-linter organization called **[asdf-clang-tools](https://github.com/cpp-linter/asdf-clang-tools)**. This project is a fork of amrox/asdf-clang-tools.  Due to the original author's lack of maintenance for many years, I have repaired, upgraded, and expanded its functionality, giving it a new lease on life. In short, asdf-clang-tools is an **asdf plugin** for installing and managing Clang Tools, such as clang-format, clang-tidy, clang-query, and clang-apply-replacements.

## A New Installation Method: asdf in Addition to pip

Previously, I released the **clang-tools-pip** toolkit, allowing users to install a complete set of Clang executable tools (including clang-format, clang-tidy, clang-query, and clang-apply-replacements) using `pip install clang-tools`.

asdf-clang-tools provides another approach—using the [asdf](https://asdf-vm.com) version manager to install these tools.  In short, this gives developers who prefer using asdf to manage tool versions another option.

These two methods are not mutually exclusive: you can easily install and manage Clang tools using either pip or asdf. The choice depends on your workflow and personal preferences.

## What is the asdf Version Manager?

Many developers may not be familiar with asdf. **asdf** is a polyglot, multi-tool version manager.

It can manage versions of multiple runtime environments with a single command-line tool and supports a plugin mechanism.

For example, you can use asdf to manage versions of Python, Node.js, Ruby, and other languages, as well as Clang tools (like the asdf-clang-tools I introduced).

All tool version information is recorded in a shared `.tool-versions` file, allowing teams to easily synchronize configurations across different machines.

In short, the advantage of asdf is "one tool to manage all dependencies," unifying the versions of various tools required by a project and eliminating the hassle of using different version managers for each tool.

## Installation and Usage Example

Installing Clang tools using asdf-clang-tools is very simple. Assuming you have already installed asdf, simply follow the instructions in the official repository:

* First, **add the plugin**: Using `clang-format` as an example, run the following in your terminal:

  ```bash
  asdf plugin add clang-format https://github.com/cpp-linter/asdf-clang-tools.git
  ```

  Similarly, `clang-query`, `clang-tidy`, `clang-apply-replacements`, and other tools use the same repository address; just change the plugin name to the corresponding name.

* **View available versions**: After adding the plugin, you can run `asdf list all clang-format` to list all installable clang-format versions.

* **Install the tool**: Choose a version (e.g., the latest `latest`), and execute:

  ```bash
  asdf install clang-format latest
  ```

  This will download and install the specified version of the clang-format binary.

* **Set the global version**: After installation, you can execute:

  ```bash
  asdf set clang-format latest
  ```

  This will write the version to the `~/.tool-versions` file, making it globally available.  After this, you can directly use commands like `clang-format` on the command line.

After completing the above steps, clang-format, clang-tidy, and other tools will be integrated into asdf management.  Refer to the official asdf documentation for more details.

## Welcome to Try and Provide Feedback

In summary, asdf-clang-tools provides a new installation method for developers who need Clang Tools.

It complements other tools from the cpp-linter organization (such as clang-tools-pip).

I sincerely welcome everyone to try the entire C/C++ lint solution provided by cpp-linter and choose the tools that best suit their workflow.

Also, if you encounter any problems or have suggestions for improvement during use, please submit them through GitHub Issues, the discussion area, etc. Let's work together to improve the Cpp Linter toolchain and make C/C++ formatting and static analysis more convenient and efficient!

---

Please indicate the author and source when reprinting this article, and do not use it for any commercial purposes.  Welcome to follow the WeChat public account "DevOps攻城狮"