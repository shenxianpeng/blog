"""Tests for the home page demo CSS generator.

The generated block in assets/css/custom.css must match what the script
produces, otherwise someone edited the block by hand and the next run will
silently undo it. The helpers are checked for the one property the timelines
rely on: an element is visible exactly inside its windows.
"""

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from gen_demo_css import BEGIN, CSS_PATH, END, build, splice, vis

PARTIALS = os.path.join(os.path.dirname(CSS_PATH), "..", "..", "layouts", "partials", "home")


def read_css():
    with open(CSS_PATH, encoding="utf-8") as f:
        return f.read()


def test_custom_css_is_up_to_date():
    css = read_css()
    assert splice(css, build()) == css, "run .github/scripts/gen_demo_css.py"


def test_markers_appear_once():
    css = read_css()
    assert css.count(BEGIN) == 1
    assert css.count(END) == 1
    assert css.index(BEGIN) < css.index(END)


def opacity_at(keyframes, pct):
    stops = sorted(
        (float(k), int(v)) for k, v in re.findall(r"([\d.]+)% \{ opacity: (\d); \}", keyframes)
    )
    value = stops[0][1]
    for at, v in stops:
        if at <= pct:
            value = v
    return value


def test_vis_is_visible_inside_windows_only():
    frames = vis("x", [(10, 20), (60, 100)])
    assert opacity_at(frames, 5) == 0
    assert opacity_at(frames, 15) == 1
    assert opacity_at(frames, 40) == 0
    assert opacity_at(frames, 80) == 1
    assert opacity_at(frames, 100) == 1


def test_vis_window_from_zero_starts_visible():
    frames = vis("x", [(0, 44)])
    assert opacity_at(frames, 0) == 1
    assert opacity_at(frames, 50) == 0


def test_every_animated_class_in_the_partials_has_keyframes():
    block = build()
    defined = set(re.findall(r"@keyframes ([\w-]+)", block))
    used = set(re.findall(r"animation: ([\w-]+) ", block))
    assert used <= defined
    for name in ("demo-cpp-linter.html", "demo-accesslens.html", "demo-keelinfra.html"):
        with open(os.path.join(PARTIALS, name), encoding="utf-8") as f:
            html = f.read()
        for cls in set(re.findall(r"\b((?:cl|al|ki)-demo-[\w-]+)", html)):
            if cls in defined:
                assert cls in used, f"{cls} has keyframes but no animation rule"
