#!/usr/bin/env python3
"""Generate the portfolio project covers.

Unlike post covers (gen_cover.py, seeded and random), these are designed by
hand, one per project, because each portfolio card is a product: the artwork
depicts what the project actually does — lint findings for cpp-linter, a branch
diagram for conventional-branch, maturity steps for devops-maturity.

What they share is the design language, and that is what makes the page read as
one body of work: the same dark ground, the same faint grid, one accent palette,
the same stroke weight and rounded caps, and no text baked into the image (the
card supplies the bilingual title).

    python3 .github/scripts/gen_portfolio_cover.py           # all projects
    python3 .github/scripts/gen_portfolio_cover.py cpp-linter
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_cover import H, W, render  # noqa: E402  (shared Chromium pipeline)

# One palette for the whole set — unity is the point.
BG = "#0f172a"
BLUE = "#38bdf8"    # primary: structure, subjects
INDIGO = "#818cf8"  # secondary structure
OK = "#34d399"      # the "it passed" accent every project earns
ERR = "#f87171"     # the defect being caught
WARN = "#fbbf24"    # sparks, highlights
MUTE = "#64748b"    # neutral scaffolding

SW = 11  # base stroke width


def scaffold():
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<defs><radialGradient id="g" cx="50%" cy="45%" r="70%">'
        f'<stop offset="0%" stop-color="{BLUE}" stop-opacity="0.12"/>'
        f'<stop offset="100%" stop-color="{BLUE}" stop-opacity="0"/></radialGradient></defs>',
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        f'<rect width="{W}" height="{H}" fill="url(#g)"/>',
        f'<g stroke="{BLUE}" stroke-width="1" opacity="0.05">',
    ]
    for x in range(0, W, 60):
        p.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>')
    for y in range(0, H, 60):
        p.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>')
    p.append("</g>")
    p.append(f'<circle cx="600" cy="400" r="310" fill="none" stroke="{INDIGO}" stroke-width="2" opacity="0.14"/>')
    return p


def _check(p, cx, cy, size, color=OK, sw=16):
    s = size
    p.append(
        f'<path d="M{cx - s:.0f},{cy:.0f} L{cx - s * 0.15:.0f},{cy + s * 0.75:.0f} L{cx + s:.0f},{cy - s * 0.65:.0f}" '
        f'fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def _badge(p, cx, cy, r, color=OK):
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BG}" stroke="{color}" stroke-width="{SW + 2}"/>')
    _check(p, cx, cy, r * 0.42, color)


def _window(p, x, y, w, h, color=BLUE):
    """Editor-window frame: rounded rect, header rule, two window dots."""
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="24" fill="{BG}" stroke="{color}" stroke-width="{SW}"/>')
    p.append(f'<line x1="{x}" y1="{y + 64}" x2="{x + w}" y2="{y + 64}" stroke="{color}" stroke-width="6" opacity="0.55"/>')
    p.append(f'<circle cx="{x + 36}" cy="{y + 32}" r="9" fill="{color}" opacity="0.9"/>')
    p.append(f'<circle cx="{x + 68}" cy="{y + 32}" r="9" fill="{MUTE}"/>')


# --- one function per project -------------------------------------------------

def cpp_linter(p):
    """Code lines, one defect flagged, the run ends green."""
    _window(p, 300, 170, 520, 440)
    rows = [(360, 300, MUTE), (360, 380, MUTE), (360, 240, ERR), (360, 340, MUTE), (360, 200, MUTE)]
    y = 290
    for x, w, col in rows:
        op = "0.95" if col == ERR else "0.45"
        p.append(f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="15" fill="{col}" opacity="{op}"/>')
        if col == ERR:
            zig = " ".join(f"{x + i * 20},{y + 48 + (6 if i % 2 else 0)}" for i in range(13))
            p.append(f'<polyline points="{zig}" fill="none" stroke="{ERR}" stroke-width="6" stroke-linecap="round"/>')
        y += 66
    _badge(p, 850, 520, 105)


def commit_check(p):
    """A commit line whose next commit must pass through the shield."""
    p.append(f'<line x1="250" y1="400" x2="950" y2="400" stroke="{MUTE}" stroke-width="10" opacity="0.6"/>')
    for x in (330, 450, 570):
        p.append(f'<circle cx="{x}" cy="400" r="26" fill="{BLUE}"/>')
        p.append(f'<circle cx="{x}" cy="400" r="26" fill="none" stroke="{BG}" stroke-width="6"/>')
    p.append(f'<circle cx="900" cy="400" r="20" fill="{MUTE}"/>')
    p.append(
        f'<path d="M730,275 l105,42 v88 c0,88 -105,135 -105,135 s-105,-47 -105,-135 v-88 z" '
        f'fill="{BG}" stroke="{OK}" stroke-width="{SW + 2}" stroke-linejoin="round"/>'
    )
    _check(p, 730, 405, 46)


def conventional_branch(p):
    """The git graph itself: main line, a named branch that comes home."""
    p.append(f'<path d="M270,500 H930" fill="none" stroke="{MUTE}" stroke-width="{SW}" opacity="0.7"/>')
    p.append(
        f'<path d="M390,500 C460,500 460,300 540,300 H720 C800,300 800,500 870,500" '
        f'fill="none" stroke="{BLUE}" stroke-width="{SW}"/>'
    )
    p.append(
        f'<path d="M470,500 C520,500 520,620 585,620 H700" fill="none" stroke="{INDIGO}" '
        f'stroke-width="{SW - 2}" opacity="0.8" stroke-linecap="round"/>'
    )
    for x, y, col in ((320, 500, MUTE), (390, 500, BLUE), (470, 500, INDIGO), (870, 500, OK)):
        p.append(f'<circle cx="{x}" cy="{y}" r="24" fill="{col}"/>')
    p.append(f'<circle cx="870" cy="500" r="40" fill="none" stroke="{OK}" stroke-width="5" opacity="0.45"/>')
    for x in (540, 630, 720):
        p.append(f'<circle cx="{x}" cy="300" r="24" fill="{BLUE}"/>')
    p.append(f'<circle cx="700" cy="620" r="20" fill="{INDIGO}" opacity="0.9"/>')


def devops_maturity(p):
    """A staircase of maturity levels, the team partway up."""
    step_w, step_h = 128, 88
    x0, y0 = 300, 620
    for i in range(5):
        x = x0 + i * step_w
        y = y0 - (i + 1) * step_h
        col = BLUE if i == 2 else MUTE
        op = "0.9" if i == 2 else "0.35"
        p.append(
            f'<rect x="{x}" y="{y}" width="{step_w - 10}" height="{y0 - y}" rx="14" fill="{col}" opacity="{op}"/>'
        )
    # the climber: dots up the steps, current position ringed, summit flagged
    for i in range(3):
        cx = x0 + i * step_w + (step_w - 10) / 2
        cy = y0 - (i + 1) * step_h - 34
        if i == 2:
            p.append(f'<circle cx="{cx:.0f}" cy="{cy}" r="20" fill="{OK}"/>')
            p.append(f'<circle cx="{cx:.0f}" cy="{cy}" r="36" fill="none" stroke="{OK}" stroke-width="5" opacity="0.45"/>')
        else:
            p.append(f'<circle cx="{cx:.0f}" cy="{cy}" r="13" fill="{OK}" opacity="0.55"/>')
    top_cx = x0 + 4 * step_w + (step_w - 10) / 2
    top_cy = y0 - 5 * step_h
    p.append(f'<line x1="{top_cx:.0f}" y1="{top_cy - 24}" x2="{top_cx:.0f}" y2="{top_cy - 110}" stroke="{WARN}" stroke-width="8" stroke-linecap="round"/>')
    p.append(f'<path d="M{top_cx:.0f},{top_cy - 110} h64 l-20,24 20,24 h-64 z" fill="{WARN}" opacity="0.9"/>')


def explain_error(p):
    """A build error handed to the model, an explanation handed back."""
    p.append(f'<circle cx="360" cy="400" r="96" fill="{BG}" stroke="{ERR}" stroke-width="{SW + 2}"/>')
    for dx, dy in ((-1, -1), (1, -1)):
        p.append(
            f'<line x1="{360 - 38 * dx}" y1="{400 - 38 * dy}" x2="{360 + 38 * dx}" y2="{400 + 38 * dy}" '
            f'stroke="{ERR}" stroke-width="15" stroke-linecap="round"/>'
        )
    p.append(f'<line x1="490" y1="400" x2="620" y2="400" stroke="{MUTE}" stroke-width="10" stroke-linecap="round"/>')
    p.append(f'<path d="M600,372 L648,400 L600,428" fill="none" stroke="{MUTE}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    p.append(
        f'<path d="M690,290 h230 a28,28 0 0 1 28,28 v130 a28,28 0 0 1 -28,28 h-130 l-58,56 v-56 h-42 '
        f'a28,28 0 0 1 -28,-28 v-130 a28,28 0 0 1 28,-28 z" fill="{BG}" stroke="{OK}" stroke-width="{SW}"/>'
    )
    _check(p, 806, 372, 40)
    for cx, cy, r in ((950, 250, 5), (975, 225, 8), (1000, 260, 4)):
        p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{WARN}"/>')


def gitstats(p):
    """Repository history rendered as the report it becomes."""
    for i, h in enumerate((150, 260, 200, 330)):
        x = 320 + i * 104
        col = OK if i == 3 else BLUE
        op = "0.9" if i == 3 else str(0.45 + i * 0.12)
        p.append(f'<rect x="{x}" y="{620 - h}" width="66" height="{h}" rx="14" fill="{col}" opacity="{op}"/>')
    p.append(f'<circle cx="850" cy="290" r="96" fill="none" stroke="{MUTE}" stroke-width="26" opacity="0.35"/>')
    p.append(
        f'<circle cx="850" cy="290" r="96" fill="none" stroke="{BLUE}" stroke-width="26" '
        f'stroke-dasharray="241 362" stroke-linecap="round" transform="rotate(-90 850 290)"/>'
    )
    p.append(f'<line x1="300" y1="680" x2="900" y2="680" stroke="{MUTE}" stroke-width="8" opacity="0.5"/>')
    for x in (340, 420, 500, 580, 660, 740):
        p.append(f'<circle cx="{x}" cy="680" r="12" fill="{INDIGO}" opacity="0.85"/>')


def clang_tools_distributions(p):
    """One toolchain fanned out into three ways to ship it."""
    p.append(f'<rect x="270" y="330" width="150" height="140" rx="26" fill="{BG}" stroke="{BLUE}" stroke-width="{SW}"/>')
    p.append(f'<path d="M330,370 L305,400 L330,430" fill="none" stroke="{BLUE}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    p.append(f'<path d="M360,370 L385,400 L360,430" fill="none" stroke="{BLUE}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    for ty in (210, 400, 590):
        p.append(f'<path d="M430,400 C540,400 540,{ty} 660,{ty}" fill="none" stroke="{MUTE}" stroke-width="8" opacity="0.7"/>')
    # docker: container of blocks
    p.append(f'<rect x="680" y="150" width="180" height="120" rx="22" fill="{BG}" stroke="{INDIGO}" stroke-width="{SW}"/>')
    for i in range(3):
        p.append(f'<rect x="{706 + i * 44}" y="196" width="32" height="32" rx="7" fill="{INDIGO}" opacity="0.85"/>')
    # static binary: terminal chevron + cursor
    p.append(f'<rect x="680" y="340" width="180" height="120" rx="22" fill="{BG}" stroke="{BLUE}" stroke-width="{SW}"/>')
    p.append(f'<path d="M712,375 L744,400 L712,425" fill="none" stroke="{BLUE}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    p.append(f'<line x1="762" y1="425" x2="820" y2="425" stroke="{BLUE}" stroke-width="10" stroke-linecap="round"/>')
    # python wheel: ring with hub
    p.append(f'<rect x="680" y="530" width="180" height="120" rx="22" fill="{BG}" stroke="{OK}" stroke-width="{SW}"/>')
    p.append(f'<circle cx="770" cy="590" r="34" fill="none" stroke="{OK}" stroke-width="9"/>')
    p.append(f'<circle cx="770" cy="590" r="8" fill="{OK}"/>')


def open_delivery_spec(p):
    """A spec checklist standing behind a governance shield."""
    p.append(f'<rect x="380" y="180" width="300" height="420" rx="26" fill="{BG}" stroke="{BLUE}" stroke-width="{SW}"/>')
    for i in range(4):
        y = 260 + i * 82
        col = OK if i < 3 else MUTE
        p.append(f'<circle cx="440" cy="{y}" r="17" fill="none" stroke="{col}" stroke-width="7"/>')
        if i < 3:
            _check(p, 440, y, 9, col, 6)
        p.append(f'<rect x="482" y="{y - 12}" width="{150 - i * 18}" height="24" rx="12" fill="{MUTE}" opacity="0.45"/>')
    p.append(
        f'<path d="M760,360 l100,40 v84 c0,84 -100,128 -100,128 s-100,-44 -100,-128 v-84 z" '
        f'fill="{BG}" stroke="{OK}" stroke-width="{SW + 2}" stroke-linejoin="round"/>'
    )
    _check(p, 760, 482, 42)


def pypistats(p):
    """Published packages stacked, adoption climbing."""
    for i, (w, col, op) in enumerate(((330, BLUE, "0.95"), (390, INDIGO, "0.55"), (450, MUTE, "0.35"))):
        x = 600 - w / 2
        y = 200 + i * 122
        p.append(f'<rect x="{x:.0f}" y="{y}" width="{w}" height="94" rx="20" fill="{col}" opacity="{op}"/>')
        p.append(f'<circle cx="{x + 47:.0f}" cy="{y + 47}" r="13" fill="{BG}" opacity="0.7"/>')
    pts = "320,650 470,610 620,626 780,560 900,520"
    p.append(f'<polyline points="{pts}" fill="none" stroke="{OK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
    p.append(f'<circle cx="900" cy="520" r="18" fill="{OK}"/>')


COVERS = {
    "cpp-linter": cpp_linter,
    "commit-check": commit_check,
    "conventional-branch": conventional_branch,
    "devops-maturity": devops_maturity,
    "explain-error-plugin": explain_error,
    "gitstats": gitstats,
    "clang-tools-distributions": clang_tools_distributions,
    "atlassian-api-py": open_delivery_spec,  # bundle dir kept for URL stability; page is Open Delivery Spec
    "pypistats": pypistats,
}


def build_svg(slug):
    fn = COVERS.get(slug)
    if fn is None:
        raise KeyError(f"no cover design for {slug!r} — add one to COVERS")
    p = scaffold()
    fn(p)
    p.append("</svg>")
    return "\n".join(p)


def main():
    targets = sys.argv[1:] or sorted(COVERS)
    for slug in targets:
        try:
            svg = build_svg(slug)
        except KeyError as e:
            sys.exit(str(e))
        dest = os.path.join("content/portfolio", slug, "featured.jpg")
        render(svg, dest)
        print(f"  {dest}  ({os.path.getsize(dest) // 1024} KB)")


if __name__ == "__main__":
    main()
