# Design System — Xianpeng Shen's Blog

This describes what the site runs. Implementation:

| What | Where |
|---|---|
| Colours (light and dark) | `assets/css/schemes/evergreen.css`, selected by `colorScheme` in `config/_default/params.toml` |
| Fonts | loaded in `layouts/partials/extend-head.html`, stacks in `assets/css/custom.css` |
| Home page | `layouts/partials/home/landing.html`, `layouts/index.html`, `layouts/partials/recent-articles/main.html`, styles `.home-*` in `assets/css/custom.css`, content in the front matter of `content/_index.en.md` and `content/_index.md` |
| Home demos | `layouts/partials/home/demo-cpp-linter.html`, `demo-keelhaven.html`, `demo-accesslens.html`, `demo-agent8.html`; CSS under "Animated demos" in `custom.css` |

## Direction

A personal site with depth, not a page of text. The tools themselves carry
it: each one shown at work, real users, real numbers and real posts.
Structure comes from a full-bleed dark band, flat cards and jumps in type
size — short headlines, quiet sublines. The home
page is kept short: who is speaking, what he works on (the stages card) and
the proof are on the first screen.

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
| Flagship band | `#111914` (neutral-800) | `#0D120F` (neutral-900), with neutral-700 rules |
| Sponsor band, flat card | `#E7E9E3` (neutral-100) | neutral-700 (the band at 45%) |
| Rule | `#D3D7CF` (neutral-200) | `#243029` (neutral-700) |
| Ink | `#0D120F` (neutral-900) | `#F2F3EF` (neutral) |
| Body text | `#36403A` (neutral-600) | `#B7C1B9` (neutral-300) |
| Muted text | `#5C665F` (neutral-500) | `#8A968E` (neutral-400) |
| Accent | `#1D6A4B` (primary-600) | `#4FB88A` (primary-400) |
| Accent hover | `#14513A` (primary-700) | `#7FD4A8` (primary-300) |
| Mint tile | `#DDF3E6` (primary-100) | `#0A2A1E` (primary-900) |

Secondary (inline code, some theme accents) is a teal of the same family.

Which appearance a visitor sees follows their system setting. The sun/moon
switcher picks the other one and remembers it; switching back to what the
system shows forgets the choice, and the page follows the system again. The
logic is the `assets/js/appearance.js` override of the theme's script.

## Site icon

The favicon and app icons are a mark, not the author photo: on a
green-black (`#111914`) rounded square, a path from a commit (a paper-coloured
dot) to a release (an accent-green dot), drawn as a check mark in `#4FB88A`.
It says "from commit to release, checks passing" and still reads at 16px.
The mark is `mark_svg()` in `.github/scripts/gen_site_icons.py`, which writes
every icon size; the author photo (`params.author.image`) stays wherever the
author is shown and on the default social card.

## Type

| Use | Face | Notes |
|---|---|---|
| Headings, home headlines, UI, buttons | Geist | 700 for headings, tracking −0.025em (articles) to −0.045em (home headlines) |
| Article body | Newsreader | article body at 19px, line-height 1.7 |
| Code, dates | Geist Mono | |
| Chinese | Noto Serif SC in reading text; PingFang SC / Noto Sans SC in headings | line-height 1.85, no italics, no negative tracking; home headlines break only at spaces and punctuation (`word-break: keep-all`) |

All from Google Fonts. Noto Serif SC is served in unicode-range slices, so
English pages do not download it.

## Layout

From the `lg` breakpoint the body is padded 4rem a side (Blowfish uses 8rem),
giving 72rem of content. Full-bleed bands (`.home-band`) span the viewport and
pad their content back to the same 72rem, so everything lines up with the
header.

The header is Blowfish's `fixed-fill` layout: a solid bar in the page colour
with a 1px rule under it. The `fixed` layout's translucent, blurred bar let
bright content smear through.

Chinese article text keeps Blowfish's `max-w-prose` measure, about 35
characters a line. English is capped at 37rem (592px, roughly 70 characters),
and the series boxes with it: `max-w-prose` is 65ch, and Newsreader's "0",
which `ch` measures, is a third wider than its average letter, so the theme's
column ran 79–91. Article titles and headings use `text-wrap: balance`.

Pages other than the home keep only the header bar's height (57px, 65px under
853px) of Blowfish's 148px header space, then 3rem (1.25rem on a phone) above
the content. On an article the table of contents sits 4rem right of the text,
not at the far edge of the body. On a phone an article title is 30px.

## Home page

Top to bottom:

The layout and its numbers come from the proposal the home page was rebuilt
to in 2026-11; treat them as the spec. The page is drawn on its own grid:
74rem (1184px) of content, where the rest of the site has 72rem, on a 16px
base with a 1.55 line-height.

0. **Header** — the site's own, the same as on every other page (the
   proposal drew a text-only menu; one header across the site won). On the
   home page its inner container takes the page's 3rem side padding so its
   ends line up with the content, and the 148px Blowfish reserves for it is
   cut to the bar's own height, so the hero's 64px of top padding is the
   whole distance between the two.

1. **Hero** — left-aligned, 64px under the header, two columns from 1024px
   (601 : 535, 48px gap), sized to fit the first screen of a laptop:
   - left: the author's photo (52px), name (16px, 600) and `heroRole` (14px,
     muted), linked to About; the headline (`title`, or `heroTitle` with a
     manual line break) at 62px, line-height 1.04, tracking −0.035em;
     `heroLead` at 19px in body-text colour; pill buttons 48px high, 15px,
     600;
   - right: **stages** (`heroAlso.stages`), the pipeline `commit` → `review`
     → `build` → `release` as a card (the About page's diagram has a fifth
     stage, `support`; the home card stops at release) (neutral-50, rule border,
     18px radius, 24px by 26px padding), one row per stage at 14px: its name
     in 12px Geist Mono in the accent colour, its projects as accent links
     (one may carry a small tag, such as "flagship") and a one-phrase `note`
     in muted text, with no full stop;
   - under both, **proof**, under a rule: five facts, each a 32px number or
     short phrase above a 14px label, in as many 180px-or-wider columns as
     fit, then the organisations whose projects use cpp-linter on one line
     at 18px, 700. On a phone each fact sits on a row with its label.
2. **Flagship** — dark full-bleed band for cpp-linter, 72px of padding.
   Stacked on a narrow screen; from 1024px the text is on the left and the
   demo on the right. Text: a 13px mono label in the accent colour, the
   headline at 42px, 17px text, a row of **chips** (12px mono pills; the one
   named by `chipActive` in the accent colour) and the links at 15px, 600.
   Demo: one static frame of a GitHub pull request, the format-review
   suggestion with its "Commit suggestion" button
   (`demo-cpp-linter-review.html`), in GitHub's own colours.
3. **Features** — an open-source project with a full-bleed section of its
   own, 64px of padding, closed by a rule; text beside its demo, and `flip:
   true` puts the demo on the left. Same label, headline, text, chips and
   links as the flagship, on the page colour. Now one: commit-check, with a
   terminal (`demo-commit-check.html`, static, dark in both appearances)
   showing the README's JSON example cut down to its first six fields.
4. **Products** — a 36px headline on the left and one 15px sentence on the
   right, then cards side by side (stacked under 960px): keelinfra (dark,
   neutral-800) and Keelhaven (the flat surface colour, neutral-100). Cards
   are flat: 18px radius, 24px padding, no shadow; a 12px mono label, the
   name at 24px, 14px text, a small static preview of the product
   (`layouts/partials/home/preview-<name>.html`, a few rows of its own
   screen; the two previews are the same height, so neither card has an
   empty band under its picture) and "Learn more" at 14px, 600. keelapps is one quiet 14px line
   under the cards (`products.also`): its buyers are on the Atlassian
   Marketplace, not on this blog.
5. **Writing** — a 36px headline with its subline on the same baseline and
   "All posts" at the far end, then the four most recent posts as ruled
   rows, 14px of padding each: date (13px mono), title (17px, 600), tag
   (12px mono).
6. **Page body** — only the Chinese home has one: the WeChat QR code.
7. **Sponsor** — a tinted full-bleed band (neutral-100 under a rule) that
   closes the page: one 15px sentence and a link on the left, the footer
   menu on the right, and 62px of page under it. The theme's footer (its
   menu and the copyright line) is not shown on the home page.

Not on the home page any more, but kept in the repo: the animated demos of
cpp-linter (four scenes), Agent8, AccessLens and Keelhaven. `demo:
"cpp-linter"` on the flagship puts the first back; the other three render
for a product with `style: wide`.

## About page

Its own template (`layouts/about/single.html`), not the theme's article
page. It opens with the author, not the word "About": a 72px photo, the name
at 26px/600, the role in 12px mono, and four pill links on the right (GitHub
with the ink border, X, Email, Résumé; 13px, 34px tall), over a rule.
On a narrow screen the role breaks between its parts and the links wrap
under the name.

Under the rule, two columns from 1024px: the text in the article's measure,
and "At a glance", six facts as ruled rows of label and value (13px; label
muted, value 500) in the place an article gives its table of contents: 4rem
from the text, 18rem wide, sticky. The page is 59rem wide in English
(37 + 4 + 18) and 62.25rem in Chinese, so the header's rule ends where the
facts do. Below 1024px the facts sit between the header and the text. The
first paragraph, the positioning line, is set a size up (23px; 22px in
Chinese; 21px on a phone). There is no author card at the end; the comments
follow the text. Copy: `role`, `links` and `facts` in the front matter of
`content/about/index.en.md` and `index.md`; keep the facts in step with the
home page's `proof`. Styles `.about-*` in `custom.css`.

The text opens with the positioning line and one paragraph on why, then the pipeline
as a diagram (`{{< pipeline >}}`): the banner's line with one dot per stage,
the stage name as a small code chip under each dot, and the projects of
that stage as accent links below it. Five columns within the article's
measure; under 35rem the line turns vertical. The line into the last stage,
`support`, is dashed: it stands for years, where the others stand for minutes.
Styles `.pipeline-*` in `custom.css`.

## Résumé page

`content/resume/`, on the About page's template (`type: about`) without the
photo or the facts: the name, the role in 12px mono, the address and GitHub
profile written out as plain accent links (so they survive on paper), over a
rule. One column in the article's measure. The positioning line and a short
summary, then Highlights (the numbers), Experience (every job, the last two
as bullets), Open Source (one line a project), Skills, Languages and
education. Print styles set it at 9.5pt on one A4 page; a new line should
replace a weaker one. The numbers in Highlights are the ones in the home
page's `proof`, so check them together. Styles `.about-single` in
`custom.css`.

## Article header

Between an article's title (36px; 30px on a phone) and its text:

- **Meta**, one line of 13px mono in the muted colour
  (`layouts/partials/article-meta/basic.html`): date, the updated date when
  it differs, reading time ("5 min read"), then the tags as plain accent
  links, written as the post lists write them. Items are separated by a dot
  and the line breaks between items. No word count, no icons: zen mode is
  off, and "Edit this page" closes the share line at the end of the article.
- **Series**, when the post belongs to one (`layouts/partials/series/`): an
  outlined card in the page's colour (1px rule, 10px radius), a small
  uppercase mono "Series", the name at 14px, 600, and "All parts" with a
  chevron on the right. Open, the parts are a list (`Part n` in mono, the
  title); the current article is in ink, the others are accent links. The
  same card, closed, follows the article.
- **Table of contents on a phone**: the theme's own, restyled as the same
  kind of card ("Table of Contents" and a chevron), above the series card.
  From 1024px it is the theme's column beside the text.

Styles `.post-meta*`, `.post-series*`, `.toc-inside` in `custom.css`.

## Post footer

Posts and essays end with "From the author" (one or two project cards, the
home tiles' white surface and shadow at a smaller radius) and "Follow" (text
links; the WeChat QR code on Chinese pages), within the article's measure.
Styles `.post-footer-*` in `custom.css`.

Then, in the same measure (37rem in English, 40.25rem in Chinese): one line
of share links as text (`layouts/partials/sharing-links.html`), "Related" as
three ruled rows of date and title (`layouts/partials/related.html`: the six
best matches by tag, newest three), and the previous/next links. Styles
`.post-related`, `.post-share` in `custom.css`.

## Post lists

Posts, Essays and each tag's page (`layouts/posts/list.html`,
`layouts/misc/list.html`, `layouts/_default/term.html`, all through
`layouts/partials/post-rows.html`) are the home page's Writing rows, not
cards: a 48px title, the post count in mono, then one section per year (a
24px year and its count) of ruled rows: month-day in 13px mono, the title at
17px, 600, the first tag in 12px mono. 50rem wide, every post on one page,
no covers. Styles `.post-list-*`.

The years to jump to are one `<nav>` drawn two ways. From 1024px it is a
rail in the space to the right of the list (4.5rem from it, 12.5rem wide,
sticky): "Jump to year", then a row per year in 12px mono with a 4px bar for
that year's share of the busiest year and the count, on a 2px line down the
left. The year being read is ink, 600, with the line and the bar in the
accent. Below 1024px it is one row of years stuck under the site header,
scrolled sideways, the current year in ink. A list with a single year (a
small tag) has no nav and keeps the plain 50rem column.

Posts and Essays name each other at the right end of the title's line
("Essays (21) →", 13px mono, accent). Between them they are everything the
Archive page used to list in a style of its own; that page is gone and its
addresses redirect to Posts.

## Tags page

`layouts/tags/terms.html`, with the post lists' header (48px title, the
number of tags in mono, the intro). The tags with five posts or more are
ruled rows in order of size, in two columns that read down (one on a phone):
the name at 15px, 600, a 4px accent bar for its share of the largest tag,
the count in 12px mono. The rest are folded into a `<details>` whose summary
is an outlined pill ("Show 92 tags with fewer than 5 posts") and open as
plain links with their counts. Styles `.tags-*`.

## 404 page

`layouts/404.html`, one file for both languages because GitHub Pages serves
only the root one: "404" in 13px mono, the title at the list pages' 48px,
one sentence in each language in the reading face (the page's own language
first), then the home page's buttons, filled for this language's home and
outlined for the other, and "Search the site" as a text button. No emoji.
Styles `.notfound-*`.

Page titles come in two sizes: 48px for the pages named by one or two words
(Posts, Essays, Projects, Tags, a tag, 404) and 36px for an article's title,
which runs to two or three lines. About opens with the author's name instead.

## Projects page

`layouts/portfolio/list.html`: the same header, then "Open source, by
delivery stage" — one block per stage (`commit`, `review`, `build`,
`release`, then `also`), the stage name in 13px mono in the accent colour on
the left and its projects as ruled rows on the right: name (17px, 600), the
site's host in 12px mono, and the `summary`. Then "Products": the same rows
with a 12px mono `label` (price and platform) above the name. Each bundle in
`content/portfolio/` sets `stage` and, for a product, `label`. Names are
written the way the projects write them (cpp-linter, commit-check,
explain-error). No pictures. Styles `.projects-*`.

## Rules

- Change colours in `evergreen.css`, not in component CSS. Components use
  `rgb(var(--color-…))`. The tokens are comma-separated triplets, so a
  translucent colour is `rgba(var(--color-…), 0.1)`; `rgb(var(--color-…) /
  0.1)` is invalid CSS and is silently dropped.
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
  - **Agent8** (keelinfra, 18s): on an AIX host, `sh install.sh --url
    https://jenkins.example.com/ --replace agent.jar` prints install.sh's own
    messages for Jenkins 2.580.1 (remoting `3386.v353e57a_1b_ea_0`, release
    `jenkins-2.580.1`), then the agent is restarted; then the controller's
    Nodes page shows the AIX, Solaris, HP-UX and CentOS 6 hosts, all on Java 8,
    coming online, and a build on the AIX host finishing. Update the version
    and the messages when a new LTS or a change to `install.sh` makes them
    stale. (The Keycloak demo it replaced is in git history.)
  - The cpp-linter, AccessLens and Agent8 CSS is generated: timings live as data in
    `.github/scripts/gen_demo_css.py`, which rewrites the marked block in
    `custom.css`. Edit the script and rerun it, never the block;
    `--check` (and `.github/scripts/tests/test_gen_demo_css.py`) fails when
    the block is stale. Each partial's header comment says what happens
    when.
- Text contrast at least 4.5:1 (3:1 at 24px and up) in both appearances.
