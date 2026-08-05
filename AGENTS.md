# AGENTS.md — Xianpeng Shen's Blog

Instructions for AI coding agents working on this repository. This is a personal technical blog built with Hugo + Blowfish theme, deployed to GitHub Pages. The blog covers AI, DevOps, CI/CD, and Open Source.

## Project Overview

- **Framework:** Hugo static site generator with Blowfish theme
- **Deployment:** GitHub Pages (`shenxianpeng.github.io`)
- **Languages:** Bilingual — Chinese (zh-cn, primary) + English (en)
- **Content:** technical articles, personal essays, annual summaries
- **Default language:** `zh-cn` (Chinese)
- **Main sections:** `posts/` (technical articles), `misc/` (personal essays, annual
  summaries), plus `about/`, `portfolio/`, `hireme/`, `archive/`, `tags/`, `authors/`
- **Deployment:** GitHub Pages via `.github/workflows/pages.yaml`. Netlify runs
  deploy previews on pull requests only — it is not the production host.

## Design System

**`DESIGN.md` is an unbuilt proposal, not a description of this site.** None of it
is implemented: there is no custom CSS in the repository, and `Instrument Serif`,
`#F8F4EF`, `#C84B2F` and `Fraunces` appear zero times outside that document. The
live site runs stock Blowfish with the `slate` colour scheme and the theme's
default fonts.

So:

- **Do not** treat a mismatch with `DESIGN.md` as a bug, and do not "fix" the site
  to match it. Everything would look like a violation, because none of it was
  ever built.
- **Do not** start implementing `DESIGN.md` as a side effect of another task.
  Adopting it is a large visual overhaul and needs the user to ask for it
  explicitly.
- Read it for intent — the editorial, restrained, typography-first direction is
  real and worth respecting in any new UI.
- If the user does adopt it, update this section; if they abandon it, delete
  `DESIGN.md` so it stops misleading agents.

For visual work today, the operative rule is simpler: **match the surrounding
Blowfish styling.** Prefer a theme config option in `config/_default/params.toml`
over new CSS, and prefer a `layouts/` override over touching
`themes/blowfish/`.

## Writing Style & Tone

### Voice
- **Conversational but disciplined.** Write like an experienced engineer explaining to a peer — direct, no fluff, but with genuine warmth.
- **First-person is encouraged.** Use "我" freely. This is a personal blog, not corporate documentation.
- **Opening style:** Open with a concrete hook — the problem, the surprising
  number, the thing that actually happened ("今天打开 Gmail，看到一封来自
  thanks.dev 的邮件"). Roughly 4% of posts open with "大家好，我是沈工"; it is an
  occasional flourish, **not** the house style, so do not reach for it by default.
- **Closing style:** A personal sign-off is welcome (e.g., "老司机们，我们下期见～").
  About a third of posts also carry this footer — follow the convention of
  neighbouring posts rather than adding it reflexively:
  ```
  转载本站文章请注明作者和出处，请勿用于任何商业用途。欢迎关注公众号「沈显鹏」
  ```

### Language Rules
- **Primary content is Chinese (zh-cn).** English is a translation, not the original.
- Use simplified Chinese characters, not traditional.
- Write in natural, conversational Chinese — avoid stiff/translated phrasing.
- Technical terms: keep common English acronyms (CI/CD, PR, API, AI, LLM) untranslated. Less common terms should have a Chinese explanation on first use.
- **No emojis** in article body text. Emojis are acceptable in social media promotion but not in the article itself.
- Keep paragraphs short — 3-5 sentences max. Mobile readers are a significant audience.

### Avoiding AI slop

The author maintains a Chinese-language skill for exactly this problem:
**https://github.com/shenxianpeng/no-ai-slop**. Install and run it over any draft
before proposing it. It has an edit mode (minimal fixes, preserves voice) and a
detect mode (names the patterns it found and quotes them, no fake percentage
scores).

If you cannot install it, these are the rules it enforces. A draft that trips
them is not ready:

**Banned vocabulary** — Chinese business/tech filler, worn out from overuse:

> 赋能、抓手、底层逻辑、顶层设计、闭环、打法、拉通、对齐、颗粒度、赛道、护城河、降维打击

**Banned patterns:**

| Pattern | Looks like |
|---|---|
| 废话开头 | "不得不说"、"有一说一"、"不可否认的是"、"说到底"、"毫无疑问" |
| 伪洞察 | "很多人不知道的是"、"真正的关键在于" — casts the author as sole holder of the truth |
| 二元对立 | "不是 X，而是 Y" as a reflex |
| 否定列举 | "不是 A。不是 B。而是 C。" |
| 冒号揭示 | "最关键的一点：它……" |
| 模板化结构 | "首先……其次……最后……"; every paragraph summarising itself before expanding |
| 表面分析 | "彰显了"、"体现了" standing in for actual analysis |
| 重要性吹捧 | "标志着一个里程碑式的时刻"、"具有深远的意义"、"扮演着至关重要的角色" |
| 模糊引用 | "专家表示"、"研究表明" with no named source |
| 同义词轮换 | Cycling synonyms for the same thing within a paragraph to seem varied |
| 伪深刻的结尾 | Forcing an aphorism at the end to elevate the piece |

The underlying failure these describe: prose where every sentence is correct and
nothing is memorable. Too smooth, too balanced, too complete. Concrete beats
polished — a real number, a real error message, a real thing that went wrong is
worth more than a paragraph of well-formed generalities.

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

## Writing a New Post — End to End

When asked to write a post, work in this order. Do not skip to drafting.

1. **Establish the facts first.** Verify every version number, star count, repo
   URL, and API detail against the actual source before writing a sentence about
   it. Do not describe a tool's behaviour from memory. If a claim cannot be
   checked, either cut it or attribute it explicitly.
2. **Agree the angle before drafting.** State in one sentence what the post
   argues and what the reader can do afterwards. A post that merely surveys a
   topic is not worth publishing here.
3. **Create the bundle:** `content/posts/YYYY/slug/index.md`, year matching the
   post date. See the naming rules below.
4. **Write the Chinese version.** This is the canonical text — never draft in
   English and translate inward.
5. **Run the draft through no-ai-slop** (see "Avoiding AI slop" above).
6. **Add `featured.jpg`** — 1200×800, under 200 KB, no text in the image. See
   "Images".
7. **Translate to `index.en.md`** via `make translate`, then read the result.
   Machine translation of technical Chinese needs a human-quality pass.
8. **Run `make build`.** It catches broken refs, bad shortcodes, and missing
   images. A post that does not build is not finished.
9. **Work through the checklist** in "Before Committing".

### What makes a post good here

- **It comes from something that actually happened.** The strongest posts on this
  blog start from a specific event — an email that arrived, a PR that got merged,
  a bug that took three days. Lead with that, not with background.
- **The numbers are real and specific.** "583 MB across 270 covers, median
  2.5 MB" persuades; "the images were large" does not.
- **It shows the work.** Commands, config, actual output, the failed attempt
  before the one that worked.
- **It admits limits.** What was not tried, what remains unsolved, where the
  author was wrong. This is the single biggest differentiator from AI-written
  technical content, which is relentlessly confident.
- **It ends when the point is made.** No summary of what was just read, no
  elevated closing aphorism.

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
- `tags`: 2-5 relevant tags, shared across languages. **Reuse an existing tag —
  do not invent one.** `content/tags/` holds only the section index, not the tag
  list; tags come from front matter, so list what is actually in use with:
  ```bash
  grep -rhA20 '^tags:' content --include=index.md | grep -E '^  - ' | sort | uniq -c | sort -rn
  ```
  There are already 158 distinct tags across 270 posts and 90 of them are used
  exactly once, which is tag sprawl, not taxonomy. A new tag needs to be one you
  expect to use again.
- `authors`: Always `shenxianpeng` for the main author.
- `date`: ISO format `YYYY-MM-DD`. This is the publication date.
- `translate`: optional. Set `translate: false` to opt the post out of the
  automatic English translation in `.github/auto_translate.py` — the script skips
  any post whose front matter carries it. Used by 81 posts so far: pieces aimed
  squarely at Chinese readers (公众号-oriented essays, Chinese-language tooling)
  where an English version adds nothing. If you leave it off, the post is
  expected to get an `index.en.md`.
- **Never** include `draft: true` in published posts. Drafts should remain local only.

### English Front Matter
The `index.en.md` version should have:
- `title`: Translated English title
- `summary`: Translated English summary
- Same `tags`, `authors`, `date` as the Chinese version

## Images

### Cover image (`featured.jpg`)

Every post has one, in the post's own directory. It is **not** decoration: Hugo
publishes it as the `og:image` and `twitter:image` for the post, and Blowfish
also derives the list-page card thumbnail from it. Get it wrong and both the
social preview and the article list suffer.

| | |
|---|---|
| **Filename** | `featured.jpg` — exactly this, in the post bundle next to `index.md` |
| **Dimensions** | **1200 × 800** (3:2), no exceptions |
| **Format** | JPEG, quality 85, progressive |
| **File size** | Target under 200 KB. Over 300 KB means something is wrong |

Why 3:2 specifically: Blowfish renders cards with `.Resize "600x"` — it sets the
width and lets the height follow the source aspect ratio. A square or portrait
cover makes that one card taller than its neighbours and the grid loses its
rhythm. Every cover being 3:2 is what keeps the list aligned.

Why the size cap: this file is the `og:image`. Social crawlers fetch it with
tight size and timeout limits, so a multi-megabyte cover risks the preview card
simply not rendering. It is also the single easiest way to bloat the repo — the
covers once totalled 583 MB at a 2.5 MB median.

Content rules for covers:

- **No text baked into the image.** It renders at 600px wide in a card and gets
  cropped again by social platforms. Any text is illegible in both places, and
  it cannot be translated for the English version.
- **One clear subject**, readable as a thumbnail. Detailed diagrams and
  screenshots do not survive the downscale — put those in the article body.
- The established look is **flat vector-style illustration**: a single subject,
  soft palette, clean outlines, no photorealism.
- If you must adapt a non-3:2 source, letterbox it onto a blurred, darkened copy
  of itself rather than cropping — cropping decapitates people and cuts off the
  subject.

### In-article images

- Put them in the post directory and reference them relatively:
  `![描述](screenshot.png)`
- **Screenshots:** PNG is fine when text must stay crisp, but resize to **at most
  1600px wide** and keep each file **under 500 KB**.
- **Photos and illustrations:** JPEG quality 85.
- Never commit an image straight from a phone, a screen-capture tool, or an image
  generator without resizing first. Those routinely run 3–5 MB each.
- Every image needs alt text.

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
