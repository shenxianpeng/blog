#!/usr/bin/env python3
"""Generate a post's cover image.

Covers are deterministic: the same post path and tag always produce the same image, so
re-running this never churns the repository. The palette comes from the post's
primary tag, which groups a topic into one colour family on list pages; the
composition comes from the post path, so two posts sharing a tag still look distinct.

Output matches the contract in AGENTS.md: 1200x800 JPEG, no text baked in.

    python3 .github/scripts/gen_cover.py content/posts/2026/some-post
    python3 .github/scripts/gen_cover.py --all          # every post missing a cover
    python3 .github/scripts/gen_cover.py --all --force  # regenerate everything
"""

import argparse
import hashlib
import math
import os
import random
import re
import subprocess
import sys
import tempfile

W, H = 1200, 800

# Background, primary, secondary. Deep and low-key — the cover sits behind a
# title on the card, so it must never fight the text.
PALETTES = [
    ("#0f172a", "#38bdf8", "#818cf8"),
    ("#1a1625", "#e879f9", "#c084fc"),
    ("#0c1a17", "#34d399", "#a7f3d0"),
    ("#1c1917", "#fbbf24", "#fb923c"),
    ("#0f1729", "#60a5fa", "#34d399"),
    ("#1e1b18", "#f87171", "#fbbf24"),
    ("#111827", "#a78bfa", "#38bdf8"),
    ("#0d1b1e", "#2dd4bf", "#facc15"),
    ("#141b2d", "#7dd3fc", "#f0abfc"),
    ("#18181b", "#4ade80", "#22d3ee"),
]


def _seed(text):
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], 16)


def cover_key(post_dir):
    """The string a post's composition is seeded from.

    Deliberately the path, not the bare slug: slugs repeat across years
    (posts/2025/jenkinsfilelint and posts/2026/jenkinsfilelint), and seeding on
    the slug alone hands both the same cover.
    """
    return os.path.relpath(post_dir, "content").replace(os.sep, "/")


def choose_motif(key):
    return MOTIFS[(_seed(key) >> 8) % len(MOTIFS)]


def _motif_pipeline(p, rnd, c1, c2, bg):
    """Nodes advancing through lanes, with branches — a build pipeline."""
    lanes = rnd.randint(3, 4)
    lane_y = [H * (i + 1) / (lanes + 1) for i in range(lanes)]
    nodes = []
    for y in lane_y:
        n = rnd.randint(4, 6)
        nodes.append(
            [(W * (j + 1) / (n + 1) + rnd.uniform(-30, 30), y + rnd.uniform(-26, 26)) for j in range(n)]
        )
    p.append(f'<g stroke="{c1}" stroke-width="4" fill="none" opacity="0.45" stroke-linecap="round">')
    for lane in nodes:
        for a, b in zip(lane, lane[1:]):
            mx = (a[0] + b[0]) / 2
            p.append(
                f'<path d="M{a[0]:.0f},{a[1]:.0f} C{mx:.0f},{a[1]:.0f} {mx:.0f},{b[1]:.0f} {b[0]:.0f},{b[1]:.0f}"/>'
            )
    for _ in range(3):
        la, lb = rnd.sample(range(lanes), 2)
        a, b = rnd.choice(nodes[la]), rnd.choice(nodes[lb])
        mx = (a[0] + b[0]) / 2
        p.append(
            f'<path d="M{a[0]:.0f},{a[1]:.0f} C{mx:.0f},{a[1]:.0f} {mx:.0f},{b[1]:.0f} {b[0]:.0f},{b[1]:.0f}" opacity="0.22"/>'
        )
    p.append("</g>")
    for lane in nodes:
        for x, y in lane:
            r = rnd.choice([14, 20, 28, 38])
            col = c2 if rnd.random() < 0.35 else c1
            if rnd.random() < 0.22:
                p.append(
                    f'<rect x="{x - r:.0f}" y="{y - r:.0f}" width="{r * 2}" height="{r * 2}" '
                    f'rx="{r * 0.3:.0f}" fill="{bg}" stroke="{col}" stroke-width="5"/>'
                )
            else:
                p.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{col}" opacity="{rnd.uniform(0.8, 1):.2f}"/>')


def _motif_orbit(p, rnd, c1, c2, bg):
    """Concentric rings with satellites — a system and its dependencies."""
    cx, cy = W * rnd.uniform(0.4, 0.6), H * rnd.uniform(0.44, 0.56)
    for i in range(rnd.randint(4, 6)):
        r = 95 + i * rnd.uniform(58, 82)
        p.append(
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="none" '
            f'stroke="{c1}" stroke-width="2" opacity="{max(0.08, 0.34 - i * 0.045):.2f}"/>'
        )
        for _ in range(rnd.randint(1, 3)):
            a = rnd.uniform(0, math.tau)
            p.append(
                f'<circle cx="{cx + r * math.cos(a):.0f}" cy="{cy + r * math.sin(a):.0f}" '
                f'r="{rnd.choice([12, 18, 26])}" fill="{c2 if rnd.random() < 0.4 else c1}" opacity="0.95"/>'
            )
    p.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rnd.choice([34, 44, 54])}" fill="{c2}"/>')


def _motif_bars(p, rnd, c1, c2, bg):
    """Stacked columns on a baseline — throughput, coverage, growth."""
    cols = rnd.randint(5, 7)
    base_y = H * 0.72
    for i in range(cols):
        x = W * (i + 0.5) / cols
        h = rnd.uniform(100, 340)
        w = W / cols * 0.5
        col = c2 if rnd.random() < 0.35 else c1
        p.append(
            f'<rect x="{x - w / 2:.0f}" y="{base_y - h:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'rx="10" fill="{col}" opacity="{rnd.uniform(0.5, 0.92):.2f}"/>'
        )
        for _ in range(rnd.randint(1, 3)):
            yy = base_y - h + rnd.uniform(20, max(25, h - 20))
            p.append(f'<rect x="{x - w / 2:.0f}" y="{yy:.0f}" width="{w:.0f}" height="5" fill="{bg}" opacity="0.55"/>')
    p.append(f'<line x1="0" y1="{base_y:.0f}" x2="{W}" y2="{base_y:.0f}" stroke="{c1}" stroke-width="3" opacity="0.45"/>')


def _motif_flow(p, rnd, c1, c2, bg):
    """Layered contours — streams, versions, history."""
    rows = rnd.randint(7, 10)
    for i in range(rows):
        y = H * (i + 0.5) / rows
        amp, ph = rnd.uniform(20, 58), rnd.uniform(0, math.tau)
        pts = " ".join(f"{W * j / 8:.0f},{y + amp * math.sin(ph + j * 0.8):.0f}" for j in range(9))
        col = c2 if i % 3 == 0 else c1
        p.append(
            f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{rnd.choice([3, 4, 6])}" '
            f'opacity="{rnd.uniform(0.32, 0.75):.2f}" stroke-linecap="round"/>'
        )
    for _ in range(rnd.randint(3, 6)):
        p.append(
            f'<circle cx="{rnd.uniform(100, W - 100):.0f}" cy="{rnd.uniform(80, H - 80):.0f}" '
            f'r="{rnd.choice([16, 24, 34])}" fill="{c2}" opacity="0.9"/>'
        )


MOTIFS = [_motif_pipeline, _motif_orbit, _motif_bars, _motif_flow]


def build_svg(slug, tag=""):
    palette_seed = _seed(tag) if tag else _seed(slug)
    bg, c1, c2 = PALETTES[palette_seed % len(PALETTES)]
    shape_seed = _seed(slug)
    rnd = random.Random(shape_seed)

    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<defs><radialGradient id="g" cx="50%" cy="45%" r="70%">'
        f'<stop offset="0%" stop-color="{c1}" stop-opacity="0.13"/>'
        f'<stop offset="100%" stop-color="{c1}" stop-opacity="0"/></radialGradient></defs>',
        f'<rect width="{W}" height="{H}" fill="{bg}"/>',
        f'<rect width="{W}" height="{H}" fill="url(#g)"/>',
        f'<g stroke="{c1}" stroke-width="1" opacity="0.05">',
    ]
    for x in range(0, W, 60):
        p.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>')
    for y in range(0, H, 60):
        p.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>')
    p.append("</g>")

    choose_motif(slug)(p, rnd, c1, c2, bg)
    p.append("</svg>")
    return "\n".join(p)


def primary_tag(post_dir):
    for name in ("index.md", "index.en.md"):
        path = os.path.join(post_dir, name)
        if not os.path.exists(path):
            continue
        m = re.search(r"^---\n(.*?)\n---", open(path, encoding="utf-8").read(), re.S)
        if not m:
            continue
        collecting = False
        for line in m.group(1).split("\n"):
            if re.match(r"^tags:", line):
                collecting = True
                continue
            if collecting:
                if re.match(r"^\s*-\s+", line):
                    return line.split("-", 1)[1].strip()
                if re.match(r"^[A-Za-z_]+:", line):
                    break
    return ""


def render(svg, dest):
    """Rasterise via headless Chromium — no native image toolchain required."""
    from PIL import Image

    with tempfile.TemporaryDirectory() as tmp:
        svg_path = os.path.join(tmp, "c.html")
        png_path = os.path.join(tmp, "c.png")
        # Wrap in HTML with the margin zeroed. Chromium renders a bare .svg inside
        # a generated document that keeps the default 8px body margin, which
        # offsets the artwork and leaves a black band down the right and bottom.
        open(svg_path, "w", encoding="utf-8").write(
            f"<!doctype html><style>html,body{{margin:0;padding:0;overflow:hidden}}"
            f"svg{{display:block}}</style>{svg}"
        )
        subprocess.run(
            [
                os.environ.get("CHROMIUM", "/opt/pw-browsers/chromium"),
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--hide-scrollbars",
                "--default-background-color=00000000",
                # Chromium's --window-size is not the viewport: the viewport comes
                # out ~90px shorter, which silently clips the bottom of the art.
                # Render with headroom and crop back to exact size.
                f"--window-size={W},{H + 240}",
                f"--screenshot={png_path}",
                f"file://{svg_path}",
            ],
            check=True,
            capture_output=True,
        )
        shot = Image.open(png_path).convert("RGB")
        if shot.size[0] < W or shot.size[1] < H:
            raise RuntimeError(f"render came back {shot.size}, need at least {W}x{H}")
        shot.crop((0, 0, W, H)).save(dest, "JPEG", quality=85, optimize=True, progressive=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("post_dir", nargs="?", help="path to a post bundle")
    ap.add_argument("--all", action="store_true", help="process every post")
    ap.add_argument("--force", action="store_true", help="overwrite existing covers")
    args = ap.parse_args()

    if args.all:
        targets = []
        for root in ("content/posts", "content/misc"):
            for d, _, fs in os.walk(root):
                if any(f.startswith("index") and f.endswith(".md") for f in fs):
                    targets.append(d)
    elif args.post_dir:
        targets = [args.post_dir.rstrip("/")]
    else:
        ap.error("pass a post directory or --all")

    made = 0
    for d in sorted(targets):
        dest = os.path.join(d, "featured.jpg")
        if os.path.exists(dest) and not args.force:
            continue
        render(build_svg(cover_key(d), primary_tag(d)), dest)
        made += 1
        print(f"  {dest}  ({os.path.getsize(dest) // 1024} KB)")
    print(f"\n{made} cover(s) written")


if __name__ == "__main__":
    main()
