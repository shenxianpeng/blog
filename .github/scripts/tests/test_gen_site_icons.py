"""Tests for the site icon mark. Rendering needs Chromium, so these check the SVG only."""

import os
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from gen_site_icons import ACCENT, PAGE_DARK, mark_svg

NS = "{http://www.w3.org/2000/svg}"


def test_mark_is_valid_svg_on_a_64_grid():
    root = ET.fromstring(mark_svg())
    assert root.tag == f"{NS}svg"
    assert root.get("viewBox") == "0 0 64 64"


def test_rounded_by_default_square_for_apple_touch():
    assert ET.fromstring(mark_svg()).find(f"{NS}rect").get("rx") == "14"
    assert ET.fromstring(mark_svg(radius=0)).find(f"{NS}rect").get("rx") == "0"


def test_uses_evergreen_colours():
    svg = mark_svg()
    assert PAGE_DARK in svg and ACCENT in svg
