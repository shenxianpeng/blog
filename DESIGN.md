# Design System — Xianpeng Shen's Blog

This describes what the site runs. Implementation:

| What | Where |
|---|---|
| Colours (light and dark) | `assets/css/schemes/evergreen.css`, selected by `colorScheme` in `config/_default/params.toml` |
| Fonts | loaded in `layouts/partials/extend-head.html`, stacks in `assets/css/custom.css` |
| Home page | `layouts/partials/home/landing.html`, `layouts/index.html`, `layouts/partials/recent-articles/main.html`, styles `.home-*` in `assets/css/custom.css`, content in the front matter of `content/_index.en.md` and `content/_index.md` |
| Home demos | `layouts/partials/home/demo-cpp-linter.html`, `demo-keelhaven.html`, `demo-accesslens.html`; CSS under "Animated demos" in `custom.css` |

## Direction

A personal site with depth, not a page of text. The tools themselves carry
it: animated demos that show each one at work, real users and real posts.
Structure comes from full-bleed bands that change light and dark, large tiles
with soft shadows, and big jumps in type size — short headlines, quiet
sublines.

Deliberately avoided, because they read as AI-generated:

- the ivory-and-terracotta palette (`#F8F4EF` / `#C84B2F`), close to
  Anthropic's brand colours;
- a big serif headline over a small monospaced uppercase "eyebrow";
- a row of three stats, numbered list items, one italic accent word;
- abstract illustrations standing in for the product at work.

## Colour — "Evergreen"

Cool grey-green paper, green-black ink, one forest-green accent. Green is the
colour of a passing check, which is what the site's projects are about.

Blowfish reads the scheme as RGB triplets on a neutral / primary / secondary
scale. Light pages use `--color-neutral` as background and `neutral-900` as
text; dark pages use `neutral-800` and `--color-neutral`.

| Role | Light | Dark |
|---|---|---|
| Page | `#F2F3EF` (neutral) | `#111914` (neutral-800) |
| Card, tile | `#FFFFFF` | `#243029` (neutral-700) |
| Band (sponsor) | `#E7E9E3` (neutral-100) | neutral-700 at 45% |
| Flagship band | `#0D120F` (neutral-900), both appearances | same, with neutral-700 rules |
| Rule | `#D3D7CF` (neutral-200) | `#243029` (neutral-700) |
| Ink | `#0D120F` (neutral-900) | `#F2F3EF` (neutral) |
| Body text | `#36403A` (neutral-600) | `#B7C1B9` (neutral-300) |
| Muted text | `#5C665F` (neutral-500) | `#8A968E` (neutral-400) |
| Accent | `#1D6A4B` (primary-600) | `#4FB88A` (primary-400) |
| Accent hover | `#14513A` (primary-700) | `#7FD4A8` (primary-300) |
| Mint tile | `#DDF3E6` (primary-100) | `#0A2A1E` (primary-900) |

Secondary (inline code, some theme accents) is a teal of the same family.

## Type

| Use | Face | Notes |
|---|---|---|
| Headings, home headlines, UI, buttons | Geist | 700 for headings, tracking −0.025em (articles) to −0.045em (home headlines) |
| Article body | Newsreader | article body at 19px, line-height 1.7 |
| Code, dates | Geist Mono | |
| Chinese | Noto Serif SC in reading text; PingFang SC / Noto Sans SC in headings | line-height 1.85, no italics, no negative tracking |

All from Google Fonts. Noto Serif SC is served in unicode-range slices, so
English pages do not download it.

## Layout

From the `lg` breakpoint the body is padded 4rem a side (Blowfish uses 8rem),
giving 72rem of content. Full-bleed bands (`.home-band`) span the viewport and
pad their content back to the same 72rem, so everything lines up with the
header. Article text keeps Blowfish's `max-w-prose` measure.

## Home page

Top to bottom:

1. **Hero** — centred headline (`title`, or `heroTitle` for a manual line
   break), `heroLead` and pill buttons. No image.
2. **Flagship** — dark full-bleed band for cpp-linter: label, short headline,
   text, links, the animated demo, and the users row.
3. **Products** — centred headline, then wide tiles with animated demos
   (Keelhaven, demo right; keelapps in mint, demo left via `flip: true`),
   then keelinfra as a full-width dark tile.
4. **Writing** — recent posts as one list of ruled rows: date, title, tag.
5. **Page body** — only the Chinese home has one: the WeChat QR code.
6. **Sponsor** — full-bleed tinted band.

## Rules

- Change colours in `evergreen.css`, not in component CSS. Components use
  `rgb(var(--color-…))`.
- The theme's compiled Tailwind only contains the utilities the theme uses.
  New components need plain CSS in `custom.css`, not new Tailwind classes.
- One accent. No gradient washes on page surfaces (the Keelhaven demo's
  desktop backdrop is the one gradient), no emoji, no left-border callouts.
- Show a product by animating what it does (`demo: <name>` in front matter
  renders `layouts/partials/home/demo-<name>.html`), not with an
  illustration. Demos are pure CSS loops (12–20s), fixed-pixel layouts scaled
  with `zoom` on small screens, and fall back to one static frame under
  `prefers-reduced-motion`. The Keelhaven demo is ported from keelhaven.app;
  keep the two in step.
  - **cpp-linter** (20s): four scenes, one per action input, named in the
    chip row: `thread-comments`, `format-review`, `step-summary`,
    `auto-fix`. Report wording is cpp-linter's own; the auto-fix commit
    uses the action's default message and is made as the actor who
    triggered the run. It does not show the check turning green afterwards:
    a push made with `GITHUB_TOKEN` does not start a new run.
  - **AccessLens** (keelapps, 16s): reverse lookup by group, then an access
    review with Confirm / Remediate and sign-off. Labels, badges and
    colours follow `keelapps/accesslens-for-jira/static/explore`.
  - The cpp-linter and AccessLens CSS is generated: timings live as data in
    `.github/scripts/gen_demo_css.py`, which rewrites the marked block in
    `custom.css`. Edit the script and rerun it, never the block;
    `--check` (and `.github/scripts/tests/test_gen_demo_css.py`) fails when
    the block is stale. Each partial's header comment says what happens
    when.
- Text contrast at least 4.5:1 (3:1 at 24px and up) in both appearances.
