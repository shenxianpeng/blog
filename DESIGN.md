# Design System — Xianpeng Shen's Blog

This describes what the site runs. Implementation:

| What | Where |
|---|---|
| Colours (light and dark) | `assets/css/schemes/evergreen.css`, selected by `colorScheme` in `config/_default/params.toml` |
| Fonts | loaded in `layouts/partials/extend-head.html`, stacks in `assets/css/custom.css` |
| Home page | `layouts/partials/home/landing.html`, `layouts/index.html`, `layouts/partials/recent-articles/main.html`, `layouts/shortcodes/projects.html` + `project.html`, styles `.home-*` in `assets/css/custom.css` |

## Direction

Editorial and restrained: a technical journal, not a documentation site.
Typography carries the page; colour is one accent used sparingly. Ruled rows
instead of cards on the home page.

Deliberately avoided: the ivory-and-terracotta palette (`#F8F4EF` /
`#C84B2F`) this file used to propose. It is close to Anthropic's own brand
colours and has become the default look of AI-generated pages.

## Colour — "Evergreen"

Cool grey-green paper, green-black ink, one forest-green accent. Green is the
colour of a passing check, which is what the site's projects are about.

Blowfish reads the scheme as RGB triplets on a neutral / primary / secondary
scale. Light pages use `--color-neutral` as background and `neutral-900` as
text; dark pages use `neutral-800` and `--color-neutral`.

| Role | Light | Dark |
|---|---|---|
| Page | `#F2F3EF` (neutral) | `#111914` (neutral-800) |
| Surface (cards, code, bands) | `#E7E9E3` (neutral-100) | `#243029` (neutral-700) |
| Rule | `#D3D7CF` (neutral-200) | `#243029` (neutral-700) |
| Ink | `#0D120F` (neutral-900) | `#F2F3EF` (neutral) |
| Body text | `#36403A` (neutral-600) | `#B7C1B9` (neutral-300) |
| Muted text | `#5C665F` (neutral-500) | `#8A968E` (neutral-400) |
| Accent | `#1D6A4B` (primary-600) | `#4FB88A` (primary-400) |
| Accent hover | `#14513A` (primary-700) | `#7FD4A8` (primary-300) |

Secondary (inline code, some theme accents) is a teal of the same family.

## Type

| Use | Face | Notes |
|---|---|---|
| Headings, home hero, project and post titles | Fraunces | weight 600; italic 400 for the accent word in the hero |
| Article body, home lead and descriptions | Newsreader | article body at 19px, line-height 1.7 |
| UI, navigation, buttons, labels | Geist | |
| Code, dates, captions, tags | Geist Mono | |
| Chinese | Noto Serif SC | falls in behind the Latin faces; line-height 1.85, no italics, positive letter-spacing on headings |

All five come from Google Fonts. Noto Serif SC is served in unicode-range
slices, so English pages do not download it.

## Home page

Top to bottom: mono caption, large Fraunces title with the `heroHighlight`
phrase in the accent colour, Newsreader lead, two buttons (ink, outline),
a ruled row of `heroStats`, the intro paragraph, "What I build" as numbered
ruled rows (`projects` / `project` shortcodes), recent posts as ruled rows
(date, title, first tag), then a sponsor band from the `sponsor` front matter.
The Chinese home adds the WeChat QR section between projects and posts.

## Rules

- Change colours in `evergreen.css`, not in component CSS. Components use
  `rgb(var(--color-…))`.
- The theme's compiled Tailwind only contains the utilities the theme uses.
  New components need plain CSS in `custom.css`, not new Tailwind classes.
- One accent. No gradients, no emoji, no left-border callouts.
- Text contrast at least 4.5:1 (3:1 at 24px and up) in both appearances.
