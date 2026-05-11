# AGENTS.md — Xianpeng Shen's Blog

Instructions for AI coding agents working on this repository. This is a personal technical blog built with Hugo + Blowfish theme, deployed to GitHub Pages. The blog covers AI, DevOps, CI/CD, and Open Source.

## Project Overview

- **Framework:** Hugo static site generator with Blowfish theme
- **Deployment:** GitHub Pages (`shenxianpeng.github.io`)
- **Languages:** Bilingual — Chinese (zh-cn, primary) + English (en)
- **Content:** technical articles, personal essays, annual summaries
- **Default language:** `zh-cn` (Chinese)
- **Main sections:** `posts/`, `misc/`, `about/`

## Design System

Always read `DESIGN.md` before making any visual or UI decisions.
All font choices, colors, spacing, and aesthetic direction are defined there.
Do not deviate without explicit user approval.
In QA mode, flag any code that doesn't match `DESIGN.md`.

Key design decisions to remember:
- Body font is **Instrument Serif** (not a sans-serif — this is intentional and the core differentiator)
- Background is **#F8F4EF** warm ivory in light mode (not pure white)
- Accent color is **#C84B2F** terracotta orange (not blue, not purple)
- Max content width is **680px** for article body

## Writing Style & Tone

### Voice
- **Conversational but disciplined.** Write like an experienced engineer explaining to a peer — direct, no fluff, but with genuine warmth.
- **First-person is encouraged.** Use "我" freely. This is a personal blog, not corporate documentation.
- **Opening style:** Posts typically open with "大家好，我是沈工" or a brief, engaging hook that draws the reader in.
- **Closing style:** End with a personal sign-off (e.g., "老司机们，我们下期见～") and the standard footer:
  ```
  转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「DevOps攻城狮」
  ```

### Language Rules
- **Primary content is Chinese (zh-cn).** English is a translation, not the original.
- Use simplified Chinese characters, not traditional.
- Write in natural, conversational Chinese — avoid stiff/translated phrasing.
- Technical terms: keep common English acronyms (CI/CD, PR, API, AI, LLM) untranslated. Less common terms should have a Chinese explanation on first use.
- **No emojis** in article body text. Emojis are acceptable in social media promotion but not in the article itself.
- Keep paragraphs short — 3-5 sentences max. Mobile readers are a significant audience.

### Units & Currency
- **Use RMB (¥) for all monetary amounts**, not USD. Chinese readers are the primary audience.
- Examples: "¥0.07" not "$0.01", "几毛钱" not "a few cents".
- For technical metrics: use metric units (KB/MB/GB, km, kg).
- For dates in article body: use Chinese format when natural ("2026年5月"), ISO format in front matter (`2026-05-10`).

### Content Principles
- **Show, don't just tell.** Include code snippets, configuration examples, comparison tables, and concrete numbers.
- **Be specific.** "提交了一百多次" is better than "提交了很多次".
- **Link generously.** Link to GitHub repos, documentation, reference articles — give readers paths to dive deeper.
- **Respect the reader's time.** If a concept can be explained in 200 words, don't use 500.
- **No clickbait.** Titles should accurately describe the content. The writing quality should sell itself.

## Content Organization

### Directory Structure
```
content/
├── posts/YYYY/slug/
│   ├── index.md        # Chinese version (REQUIRED)
│   └── index.en.md     # English version (optional but recommended)
├── misc/               # Personal essays, annual summaries
│   └── slug/
│       ├── index.md
│       └── index.en.md
└── about/
```

### Naming Conventions
- **Slug:** lowercase, English, hyphens for spaces. Keep it concise and descriptive.
  - Good: `agentic-devops`, `why-open-source`, `devops-trends-2025`
  - Bad: `post-about-devops`, `artical1`, `my_blog_post`
- **Directory:** `content/posts/YYYY/slug/` — year must match the post date.

### Slug Rules
- Use the same concept/meaning as the Chinese title, but in concise English
- No dates in slugs (the directory year handles that)
- No sequential numbering (slugs are permanent URLs)
- Max 4-5 words, hyphen-separated

## Front Matter

Every post MUST have front matter. Here's the template:

```yaml
---
title: 中文标题
summary: |
  中文摘要，2-3 句话，描述文章核心内容。用于列表页和 SEO description。
tags:
  - Tag1
  - Tag2
  - Tag3
authors:
  - shenxianpeng
date: YYYY-MM-DD
---
```

### Rules
- `title`: Full Chinese title. No English in Chinese titles unless it's a proper name/acronym (e.g., "CI/CD", "RepoKeeper").
- `summary`: 2-3 sentences in Chinese. Use `|` for multi-line summaries. The summary appears on list pages and as SEO description.
- `tags`: 2-5 relevant tags. Use existing tags when possible. Check `content/tags/` for the current tag list. Tags are shared across languages.
- `authors`: Always `shenxianpeng` for the main author.
- `date`: ISO format `YYYY-MM-DD`. This is the publication date.
- **Never** include `draft: true` in published posts. Drafts should remain local only.

### English Front Matter
The `index.en.md` version should have:
- `title`: Translated English title
- `summary`: Translated English summary
- Same `tags`, `authors`, `date` as the Chinese version

## Bilingual Content Management

### Translation Workflow
1. Write the Chinese version (`index.md`) first. This is the canonical content.
2. Translate to English (`index.en.md`). Use `make translate` for AI-assisted translation (Gemini).
3. Both files must coexist in the same directory.
4. Translations should be natural English, not literal word-for-word. Adjust idioms and cultural references.

### Translation Quality
- English version should read as if originally written in English
- Preserve all technical accuracy — code blocks, commands, configs are identical
- Formatting (bold, italic, code spans, links, images) must be preserved exactly
- The structure (headings, sections) should mirror the Chinese version
- Tone in English: same conversational but technically precise style

## Hugo & Build Rules

### Local Development
```bash
make dev     # hugo serve --buildFuture (includes future-dated posts)
make build   # hugo build (production build, excludes future dates)
```

### Content Rules for Hugo
- All content files go under `content/` with the required directory structure
- Static assets (images, downloads) go under `static/`
- Images in posts: use relative paths or absolute `/img/` paths
- Never modify theme files directly in `themes/blowfish/` — use `layouts/` overrides
- Do not create posts with future dates unless actively drafting for scheduled publishing

## Before Committing

### Content Checklist
- [ ] Chinese version (`index.md`) written and reviewed
- [ ] English version (`index.en.md`) exists (or explicitly decided not to translate)
- [ ] Front matter complete: title, summary, tags, authors, date
- [ ] Date is correct and matches directory year
- [ ] All links are valid (no broken GitHub links, no 404s)
- [ ] All internal links use relative paths or `{{</* ref */>}}` shortcodes
- [ ] Code blocks have language specifiers
- [ ] Images have alt text
- [ ] No emojis in body text
- [ ] No dollar amounts — all currency in RMB (¥)

### Technical Checks
```bash
# Build check (catches Hugo errors, shortcode issues, broken refs)
make build

# If build errors exist, fix them before committing
# Common issues: broken shortcodes, invalid refs, missing templates
```

### Git Rules

#### Committing
- **ONLY commit files YOU changed in THIS session**
- NEVER use `git add -A` or `git add .` — these sweep up changes from other agents
- ALWAYS use `git add <specific-file-paths>` listing only files you modified
- Before committing, run `git status` and verify you are only staging YOUR files
- Track which files you created/modified/deleted during the session

#### Forbidden Git Operations
These commands can destroy other agents' work:

- `git reset --hard` — destroys uncommitted changes
- `git checkout .` — destroys uncommitted changes
- `git clean -fd` — deletes untracked files
- `git stash` — stashes ALL changes including other agents' work
- `git add -A` / `git add .` — stages other agents' uncommitted work

#### Safe Workflow
```bash
# 1. Check status first
git status

# 2. Add ONLY your specific files
git add content/posts/2026/some-post/index.md content/posts/2026/some-post/index.en.md

# 3. Commit
git commit -m "description"

# 4. Push (pull --rebase if needed)
git pull --rebase && git push
```

### Commit Messages
- Use English for commit messages
- Format: `<type>: <brief description>`
- Types: `post:`, `fix:`, `chore:`, `design:`, `config:`
- Examples:
  - `post: add RepoKeeper v1.2.0 article`
  - `fix: correct typos in aiops article`
  - `chore: update copyright year to 2026`

## Content Quality Rules

- **Read the full file** before making any changes. Never edit based on grep/snippet context.
- **Always ask** before removing content that appears intentional (existing paragraphs, links, structures).
- **Check consistency:** If a post uses "RepoKeeper" (camel case), don't introduce "repo-keeper" or "Repo Keeper" elsewhere.
- **Cross-reference:** When mentioning a tool/technology, verify the project name, URL, and current status.
- **Preserve existing formatting:** Bold (`**text**`), inline code (`` `code` ``), and link syntax must remain consistent.

## External References

- RepoKeeper: https://github.com/shenxianpeng/repokeeper
- Blog repo: https://github.com/shenxianpeng/blog
- Live site: https://shenxianpeng.github.io
