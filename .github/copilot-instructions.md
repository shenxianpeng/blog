# GitHub Copilot Instructions

This is a Hugo-based personal blog repository for Xianpeng Shen, covering topics on DevOps, CI/CD, and Open Source.

## Project Structure

- **Theme**: [Blowfish](https://blowfish.page/) Hugo theme
- **Content**: Located in `content/` directory
  - `content/posts/` - Blog posts organized by year (e.g., `2024/`, `2025/`)
  - `content/about/` - About page
  - `content/archive/` - Archive page
  - `content/misc/` - Miscellaneous content
- **Configuration**: Located in `config/_default/`
  - `hugo.toml` - Main Hugo configuration
  - `languages.*.toml` - Language-specific settings
  - `menus.*.toml` - Menu configurations
  - `params.toml` - Theme parameters

## Languages

This blog supports bilingual content:
- **Chinese (zh-cn)**: Default language, files named `index.md`
- **English (en)**: Secondary language, files named `index.en.md`

## Blog Post Structure

Each blog post is a folder containing:
- `index.md` - Chinese content (default)
- `index.en.md` - English content (optional)
- `featured.png` - Featured image (optional)

### Front Matter Format

```yaml
---
title: Post Title
summary: Brief description of the post
tags:
  - Tag1
  - Tag2
authors:
  - shenxianpeng
date: YYYY-MM-DD
translate: false  # Optional: set to false to skip auto-translation
---
```

## Development Commands

```bash
# Start development server
make dev
# or
hugo serve --buildFuture

# Build for production
make build
# or
hugo build

# Install translation dependencies
make install-deps

# Run auto-translation (requires GEMINI_API_KEY)
make translate
```

## Auto-Translation Feature

The repository includes an auto-translation script (`.github/auto_translate.py`) that:
- Finds blog posts missing Chinese or English versions
- Uses Google Gemini API to translate content
- Creates pull requests with translated content
- Respects `translate: false` front matter to skip specific posts

## GitHub Actions Workflows

- `pages.yaml` - Deploys the Hugo site to GitHub Pages
- `auto-translate.yml` - Runs auto-translation for missing language versions
- `trigger-profile-update.yml` - Triggers profile updates

## Code Style

- Follow EditorConfig settings (`.editorconfig`)
- Use LF line endings
- UTF-8 encoding
- Python: 4 spaces indentation
- YAML: 2 spaces indentation

## License

Content is licensed under CC BY-NC-SA 4.0 International License.
