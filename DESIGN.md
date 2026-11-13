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

## Home page

Top to bottom:

The layout and its numbers come from the proposal the home page was rebuilt
to in 2026-11; treat them as the spec. The page is drawn on its own grid:
74rem (1184px) of content, where the rest of the site has 72rem, on a 16px
base with a 1.55 line-height.

0. **Header** — the home page has its own (`layouts/partials/header/home.html`,
   chosen in the `header/fixed-fill.html` override): a 64px full-bleed bar
   over a rule, not fixed, with the site name on the left (17px, 600) and a
   text menu on the right at 15px: Posts, Projects, About, GitHub, and the
   other language in 13px Geist Mono, muted. No icons, appearance switch or
   search; every other page keeps the theme's header with those.

1. **Hero** — left-aligned, 64px under the header, two columns from 1024px
   (628 : 508, 48px gap), sized to fit the first screen of a laptop:
   - left: the author's photo (52px), name (16px, 600) and `heroRole` (14px,
     muted), linked to About; the headline (`title`, or `heroTitle` with a
     manual line break) at 62px, line-height 1.04, tracking −0.035em;
     `heroLead` at 19px in body-text colour; pill buttons 46px high, 15px,
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
   screen) and "Learn more" at 14px, 600. keelapps is one quiet 14px line
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

Opens with the positioning line and one paragraph on why, then the pipeline
as a diagram (`{{< pipeline >}}`): the banner's line with one dot per stage,
the stage name as a small code chip under each dot, and the projects of
that stage as accent links below it. Five columns within the article's
measure; under 35rem the line turns vertical. The line into the last stage,
`support`, is dashed: it stands for years, where the others stand for minutes.
Styles `.pipeline-*` in `custom.css`.

## Post footer

Posts and essays end with "From the author" (one or two project cards, the
home tiles' white surface and shadow at a smaller radius) and "Follow" (text
links; the WeChat QR code on Chinese pages), within the article's measure.
Styles `.post-footer-*` in `custom.css`.

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
