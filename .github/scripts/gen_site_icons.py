#!/usr/bin/env python3
"""Generate the site's icons and default social card.

The icons are the site mark: on a green-black square, a path from a commit
(the paper-coloured dot) to a release (the green dot), drawn as a check mark,
because the site is about getting changes from commit to release with checks
that pass. It is drawn in MARK_SVG below and reads at 16 px.

The social card keeps the author photo, assets/img/sxp.jpg (the headshot also
used on GitHub, X and LinkedIn).

    python3 .github/scripts/gen_site_icons.py              # icons and card
    python3 .github/scripts/gen_site_icons.py --icons-only

Writes, overriding the Blowfish theme's defaults (a pufferfish):

  static/favicon.ico            16, 32 and 48 px, rounded square
  static/favicon-16x16.png      rounded square (tab size)
  static/favicon-32x32.png      rounded square (tab size)
  static/apple-touch-icon.png   180 px, square and opaque (iOS adds the corners)
  static/android-chrome-192x192.png, static/android-chrome-512x512.png
  static/site.webmanifest       name and colours for those icons
  assets/img/social-card.png    1200x630, the og:image of pages without a
                                cover (params.toml: defaultSocialImage)

Everything is rendered with Playwright's Chromium (pip install playwright;
set CHROMIUM to a Chrome binary if Playwright has no browser of its own), so
the Geist web font loads before the social card's screenshot.
"""

import base64
import io
import json
import os
import sys

from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
PHOTO = os.path.join(ROOT, "assets", "img", "sxp.jpg")
STATIC = os.path.join(ROOT, "static")
CARD = os.path.join(ROOT, "assets", "img", "social-card.png")

# Evergreen (assets/css/schemes/evergreen.css)
PAGE_DARK = "#111914"
INK = "#F2F3EF"
BODY = "#B7C1B9"
MUTED = "#8A968E"
RULE = "#243029"
ACCENT = "#4FB88A"

# The mark, on a 64-unit grid. `radius` rounds the square: 14 for the tab and
# Android icons, 0 for the Apple touch icon, which iOS masks itself.
def mark_svg(radius=14):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        f'<rect width="64" height="64" rx="{radius}" fill="{PAGE_DARK}"/>'
        f'<path d="M11 33 L28 44 L52 18" fill="none" stroke="{ACCENT}" stroke-width="7" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="11" cy="33" r="6.5" fill="{INK}"/>'
        f'<circle cx="52" cy="18" r="6.5" fill="{ACCENT}"/>'
        "</svg>"
    )


def launch(p):
    exe = os.environ.get("CHROMIUM")
    return p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()


def render_mark(page, size, radius=14):
    """The mark at exactly size x size pixels, transparent outside the square."""
    page.set_viewport_size({"width": size, "height": size})
    svg = mark_svg(radius).replace("<svg ", f'<svg width="{size}" height="{size}" ', 1)
    page.set_content(f"<!doctype html><style>html,body{{margin:0}}svg{{display:block}}</style>{svg}")
    png = page.screenshot(clip={"x": 0, "y": 0, "width": size, "height": size}, omit_background=True)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def icons():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = launch(p)
        page = browser.new_page()
        tab = {size: render_mark(page, size) for size in (16, 32, 48, 192, 512)}
        touch = render_mark(page, 180, radius=0).convert("RGB")
        browser.close()
    for size in (16, 32):
        tab[size].save(os.path.join(STATIC, f"favicon-{size}x{size}.png"), optimize=True)
    # Each ICO frame drawn at its own size, not downscaled from one big frame.
    tab[48].save(os.path.join(STATIC, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)],
                 append_images=[tab[16], tab[32]])
    touch.save(os.path.join(STATIC, "apple-touch-icon.png"), optimize=True)
    for size in (192, 512):
        tab[size].save(os.path.join(STATIC, f"android-chrome-{size}x{size}.png"), optimize=True)
    manifest = {
        "name": "Xianpeng Shen",
        "short_name": "Xianpeng Shen",
        "icons": [
            {"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"},
        ],
        "theme_color": PAGE_DARK,
        "background_color": PAGE_DARK,
        "display": "standalone",
    }
    with open(os.path.join(STATIC, "site.webmanifest"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")


STAGES = [("commit", "commit-check"), ("review", "cpp-linter"), ("build", "explain-error"), ("release", "release-ledger")]


def card_html(photo):
    buf = io.BytesIO()
    photo.resize((600, 600), Image.LANCZOS).save(buf, "JPEG", quality=92)
    src = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    x0, step, y = 522, 176, 470
    nodes = []
    for i, (stage, proj) in enumerate(STAGES):
        cx = x0 + i * step
        nodes.append(
            f'<text x="{cx}" y="{y - 30}" text-anchor="middle" class="stage">{stage}</text>'
            f'<circle cx="{cx}" cy="{y}" r="17" fill="{PAGE_DARK}"/><circle cx="{cx}" cy="{y}" r="13" fill="{ACCENT}"/>'
            f'<path d="M{cx - 5.5},{y + 0.5} L{cx - 1.5},{y + 4.5} L{cx + 6},{y - 4.5}" fill="none" stroke="{PAGE_DARK}" '
            f'stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<text x="{cx}" y="{y + 44}" text-anchor="middle" class="proj">{proj}</text>'
        )
    line = f'<line x1="{x0}" y1="{y}" x2="{x0 + 3 * step}" y2="{y}" stroke="{ACCENT}" stroke-width="3" stroke-linecap="round"/>'
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@500..700&family=Geist+Mono:wght@500&display=swap">
<style>
html,body{{margin:0}}
body{{width:1200px;height:630px;overflow:hidden;background:{PAGE_DARK};
  background-image:radial-gradient(rgba(242,243,239,.05) 1.4px,transparent 1.6px);background-size:32px 32px;background-position:16px 16px}}
svg{{display:block}}
.name{{font-family:Geist,sans-serif;font-weight:700;font-size:68px;letter-spacing:-0.035em;fill:{INK}}}
.line{{font-family:Geist,sans-serif;font-weight:500;font-size:31px;letter-spacing:-0.01em;fill:{BODY}}}
.stage,.url{{font-family:'Geist Mono',monospace;font-weight:500;fill:{MUTED}}}
.stage{{font-size:17px}}
.url{{font-size:20px}}
.proj{{font-family:Geist,sans-serif;font-weight:600;font-size:18px;fill:{INK}}}
</style></head><body>
<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
<defs><clipPath id="c"><circle cx="250" cy="300" r="150"/></clipPath></defs>
<circle cx="250" cy="300" r="156" fill="{RULE}"/>
<image href="{src}" x="100" y="150" width="300" height="300" clip-path="url(#c)"/>
<text x="460" y="236" class="name">Xianpeng Shen</text>
<text x="462" y="290" class="line">Open-source guardrails for software delivery,</text>
<text x="462" y="332" class="line">from commit to release.</text>
{line}{''.join(nodes)}
<text x="1100" y="590" text-anchor="end" class="url">shenxianpeng.dev</text>
</svg></body></html>"""


def social_card(photo):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = launch(p)
        page = browser.new_page(viewport={"width": 1200, "height": 630})
        page.set_content(card_html(photo), wait_until="networkidle")
        # SVG text does not trigger web-font loading by itself; ask for each face.
        page.evaluate("Promise.all(['700 68px Geist','500 31px Geist','600 18px Geist','500 17px \"Geist Mono\"']"
                      ".map(f => document.fonts.load(f))).then(() => document.fonts.ready)")
        page.wait_for_timeout(300)
        png = page.screenshot(clip={"x": 0, "y": 0, "width": 1200, "height": 630})
        browser.close()
    Image.open(io.BytesIO(png)).convert("RGB").save(CARD, optimize=True)


def main():
    icons()
    if "--icons-only" not in sys.argv[1:]:
        social_card(Image.open(PHOTO).convert("RGB"))
    for name in ("favicon.ico", "favicon-16x16.png", "favicon-32x32.png", "apple-touch-icon.png",
                 "android-chrome-192x192.png", "android-chrome-512x512.png", "site.webmanifest"):
        print(f"  static/{name}  ({os.path.getsize(os.path.join(STATIC, name)) // 1024} KB)")
    if "--icons-only" not in sys.argv[1:]:
        print(f"  assets/img/social-card.png  ({os.path.getsize(CARD) // 1024} KB)")


if __name__ == "__main__":
    main()
