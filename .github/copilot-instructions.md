# GitHub Copilot Instructions

This is a personal blog repository, built with MkDocs NG and the Sumi theme, for Xianpeng Shen, covering topics on DevOps, CI/CD, and Open Source.

## Project Structure

- **Theme**: [Sumi](https://sumi.mkdocs-ng.org/) on [MkDocs NG](https://mkdocs-ng.org/)
- **Content**: Located in `content/` directory
  - `content/posts/` - Blog posts organized by year (e.g., `2024/`, `2025/`)
  - `content/about/` - About page
  - `content/portfolio/` - Projects (open source and products), one bundle per project
  - `content/resume/` - CV, linked only from About
  - `content/archive/` - Archive page
  - `content/misc/` - Essays and annual summaries
  - `content/index.en.md` / `content/index.md` - home page hero and product tiles
- **Configuration**: `mkdocs.yml` (site, theme, languages, menus)
  - `hooks/site.py` - drafts, Projects cards, series pages, old-address redirects
  - `overrides/` - templates: home page, Projects, post footer, footer, analytics
  - `assets/css/sumi-evergreen.css` - the Evergreen look on Sumi

## Languages

This blog supports bilingual content:
- **Chinese (zh-cn)**: written first, files named `index.md`, served under `/zh-cn/`
- **English (en)**: the site's default language, files named `index.en.md`, served from `/`

## Blog Post Structure

Each blog post is a folder containing:
- `index.md` - Chinese content (default)
- `index.en.md` - English content (optional)
- `featured.jpg` - Cover image, 1200 x 800 (see AGENTS.md)

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
# Install the site's dependencies
make install-site

# Start development server
make dev

# Build for production
make build

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

- `pages.yaml` - Builds the site with MkDocs NG and deploys it to GitHub Pages
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
