# Design System — Xianpeng Shen's Blog

## Product Context

- **What this is:** A personal technical blog covering AI, DevOps, CI/CD, and Open Source — written by an engineer who actually cares about prose, not just shipping code.
- **Who it's for:** Engineers, DevOps practitioners, and developers who value depth over clickbait.
- **Space/industry:** Technical blogging / personal brand / developer education
- **Project type:** Editorial blog (Hugo static site, GitHub Pages)

## Aesthetic Direction

- **Direction:** Precision Editorial
- **Decoration level:** Minimal — typography does all the work
- **Mood:** Technical rigor with the warmth of a writer who genuinely cares about the words. Like a well-typeset technical journal, not another tool documentation site. Quiet confidence — the design doesn't try hard, so readers focus on the writing.
- **Reference sites:** Josh Comeau (joshwcomeau.com), Lee Robinson (leerob.com), overreacted.io

### EUREKA Insight

Every DevOps/CI/CD blog defaults to "documentation aesthetics" — cold white backgrounds, monospace stacks, README-like layout. But this is a blog by a *writer who happens to work in DevOps*, not a documentation maintainer. The opportunity: bring editorial warmth and strong personal identity into a category where nobody has done it.

## Typography

- **Display/Hero:** [Fraunces](https://fonts.google.com/specimen/Fraunces) (variable optical-size serif, weight 800) — Has deliberate quirky character; feels engineered-yet-personal. Unusual in the DevOps space, which makes it memorable.
- **Body:** [Instrument Serif](https://fonts.google.com/specimen/Instrument+Serif) — **The key differentiator.** Every other DevOps blog uses a grotesque sans-serif. A serif signals: "I write essays, not Stack Overflow answers." Instrument Serif is crisp, editorial, not stuffy.
- **UI/Labels/Navigation:** [Geist](https://vercel.com/font) — Clean, purposeful, zero personality friction for interface text.
- **Data/Tables/Metadata:** [Geist Mono](https://vercel.com/font) — Dates, word counts, tags, reading time. Tabular numbers, tight and precise.
- **Code:** [Geist Mono](https://vercel.com/font) — Consistent with metadata, well-rendered at small sizes.
- **Loading:** Google Fonts CDN via `<link>` preconnect
- **Scale:**
  ```
  xs:   12px / 0.75rem   — metadata, captions
  sm:   14px / 0.875rem  — UI labels, navigation
  base: 17px / 1.0625rem — body text
  lg:   20px / 1.25rem   — lead paragraphs
  xl:   24px / 1.5rem    — subheadings (h3)
  2xl:  32px / 2rem      — section headings (h2)
  3xl:  48px / 3rem      — article titles (mobile)
  4xl:  64px / 4rem      — article titles (desktop)
  hero: 72px / 4.5rem    — homepage name
  ```

## Color

- **Approach:** Restrained — one accent color, used sparingly and with purpose.

### Light Mode

| Token | Value | Usage |
|---|---|---|
| `--bg` | `#F8F4EF` | Page background — warm ivory, signals "publication" not "tool" |
| `--surface` | `#F0EDE8` | Cards, code block backgrounds, slightly elevated surfaces |
| `--surface2` | `#E8E4DC` | Hover states, active elements |
| `--text` | `#18181A` | Primary text — near-black with warmth, never pure #000 |
| `--text-muted` | `#6B6460` | Secondary text, dates, descriptions |
| `--text-subtle` | `#9A918C` | Placeholder text, least-important metadata |
| `--accent` | `#C84B2F` | Terracotta orange — earthy, warm, tech-adjacent. Used for links, code highlights, left-border accents, tags |
| `--accent-hover` | `#A83A20` | Accent on hover |
| `--border` | `#D8D2CA` | Structural borders, dividers |
| `--code-bg` | `#F0EDE8` | Code block background |

### Dark Mode

| Token | Value | Usage |
|---|---|---|
| `--bg` | `#0F1117` | Deep blue-black — not pure black, not navy |
| `--surface` | `#161B22` | Elevated surfaces |
| `--surface2` | `#1E2530` | Further-elevated surfaces, hovers |
| `--text` | `#E8E4DC` | Primary text — warm white, zero eye fatigue |
| `--text-muted` | `#8A8680` | Secondary text |
| `--text-subtle` | `#5A5654` | Least-important metadata |
| `--accent` | `#E8400C` | Deep orange-red — same family as light mode, more vivid |
| `--accent-hover` | `#FF5520` | Accent on hover |
| `--border` | `#252B36` | Structural borders |
| `--code-bg` | `#161B22` | Code block background |

### Semantic Colors

| Purpose | Light | Dark |
|---|---|---|
| Success | `#2E7D4F` | `#3DCD6E` |
| Warning | `#A0620A` | `#F5A623` |
| Error | `#B83232` | `#FF5555` |
| Info | `#1A5E9E` | `#58A6FF` |

## Spacing

- **Base unit:** 8px
- **Density:** Comfortable
- **Max content width:** 680px (enforces good reading line length ~65-75 chars)
- **Max page width:** 1200px
- **Scale:**
  ```
  2xs:  2px   / 0.125rem
  xs:   4px   / 0.25rem
  sm:   8px   / 0.5rem
  md:   16px  / 1rem
  lg:   24px  / 1.5rem
  xl:   32px  / 2rem
  2xl:  48px  / 3rem
  3xl:  64px  / 4rem
  4xl:  80px  / 5rem
  ```
- **Border radius:** sm: 4px, md: 6px, lg: 10px, xl: 14px, full: 9999px

## Layout

- **Approach:** Grid-disciplined for article content, editorial-first on the homepage
- **Homepage:** Large typographic hero (name fills the viewport), then curated article list
- **Article pages:** Single centered column, max-width 680px, generous vertical spacing
- **Grid:** 12-column at desktop (≥1024px), 4-column at tablet (≥768px), 1-column at mobile
- **Article left-border accent:** Code blocks and blockquotes use a 3px left border in `--accent`

## Motion

- **Approach:** Intentional — only transitions that aid comprehension, no decorative animations
- **Easing:** enter: `ease-out` / exit: `ease-in` / move: `ease-in-out`
- **Duration:**
  ```
  micro:  80ms   — button state changes, focus rings
  short:  200ms  — hover effects, link color transitions
  medium: 300ms  — page transitions, dark mode toggle
  ```
- **Never:** scroll-triggered reveal animations, decorative entrance animations, bouncing anything

## Deliberate Design Risks

These are intentional departures from category norms. They're what give this blog its own identity.

1. **Serif body font** — Instrument Serif for all article body copy. Every other DevOps/CI/CD blog uses a grotesque sans-serif. This signals "essays worth reading" vs "documentation to skim."
2. **Warm ivory background** — #F8F4EF instead of pure white. Signals "publication" not "web app." Requires careful contrast calibration, but the payoff is a warmer, more inviting reading experience.

## Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-03-26 | Initial design system created | Created by /design-consultation based on visual research (Josh Comeau, overreacted.io, leerob.com, samwho.dev) + EUREKA insight about editorial differentiation in DevOps blogging space |
| 2026-03-26 | Instrument Serif for body | Key differentiator — no DevOps blog uses serif body; signals writing quality |
| 2026-03-26 | Warm ivory #F8F4EF background | "Publication" signal vs "documentation" — deliberate departure from sterile white/gray |
| 2026-03-26 | Fraunces for headings | Variable optical-size serif with character; warmer than geometric alternatives (Syne) |
| 2026-03-26 | Terracotta accent #C84B2F | Earthy, warm, unusual in the space — not the default blue/purple/teal |
| 2026-03-26 | Rejected: vertical reading progress axis | Interesting UX concept but requires non-trivial Hugo customization; not worth the complexity at this stage |
