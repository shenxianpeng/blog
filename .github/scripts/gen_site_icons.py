#!/usr/bin/env python3
"""Generate the site's icons and default social card from the author photo.

Everything comes from one source, assets/img/sxp.jpg (the headshot also used on
GitHub, X and LinkedIn), so changing the photo means rerunning this script.

    python3 .github/scripts/gen_site_icons.py

Writes, overriding the Blowfish theme's defaults (a pufferfish):

  static/favicon.ico            16, 32 and 48 px, round, cropped to the face
  static/favicon-16x16.png      round, cropped to the face (tab size)
  static/favicon-32x32.png      round, cropped to the face (tab size)
  static/apple-touch-icon.png   180 px, square and opaque (iOS adds the corners)
  static/android-chrome-192x192.png, static/android-chrome-512x512.png
  static/site.webmanifest       name and colours for those icons
  assets/img/social-card.png    1200x630, the og:image of pages without a
                                cover (params.toml: defaultSocialImage)

The social card is rendered with Playwright's Chromium so the Geist web font
loads before the screenshot (pip install playwright). The icons need only Pillow.
"""

import base64
import io
import json
import os

from PIL import Image, ImageDraw

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

# At 16 and 32 px the whole headshot is a blur; crop to the face (cap brim to
# chin) for the tab-sized icons. Fractions of the square photo.
FACE = (0.20, 0.255, 0.825, 0.88)


def round_icon(img, size):
    """A circular icon with a transparent outside, antialiased by drawing at 4x."""
    big = img.resize((size * 4, size * 4), Image.LANCZOS)
    mask = Image.new("L", big.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, big.width - 1, big.height - 1), fill=255)
    out = Image.new("RGBA", big.size, (0, 0, 0, 0))
    out.paste(big, (0, 0), mask)
    return out.resize((size, size), Image.LANCZOS)


def icons(photo):
    w, h = photo.size
    face = photo.crop((int(FACE[0] * w), int(FACE[1] * h), int(FACE[2] * w), int(FACE[3] * h)))
    for size in (16, 32):
        round_icon(face, size).save(os.path.join(STATIC, f"favicon-{size}x{size}.png"), optimize=True)
    round_icon(face, 256).save(os.path.join(STATIC, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    photo.resize((180, 180), Image.LANCZOS).save(os.path.join(STATIC, "apple-touch-icon.png"), optimize=True)
    for size in (192, 512):
        photo.resize((size, size), Image.LANCZOS).save(os.path.join(STATIC, f"android-chrome-{size}x{size}.png"), optimize=True)
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
        browser = p.chromium.launch()
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
    photo = Image.open(PHOTO).convert("RGB")
    icons(photo)
    social_card(photo)
    for name in ("favicon.ico", "favicon-16x16.png", "favicon-32x32.png", "apple-touch-icon.png",
                 "android-chrome-192x192.png", "android-chrome-512x512.png", "site.webmanifest"):
        print(f"  static/{name}  ({os.path.getsize(os.path.join(STATIC, name)) // 1024} KB)")
    print(f"  assets/img/social-card.png  ({os.path.getsize(CARD) // 1024} KB)")


if __name__ == "__main__":
    main()
