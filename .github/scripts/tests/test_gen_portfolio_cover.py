"""Tests for the portfolio cover set.

The covers themselves are hand-designed, so there is nothing to assert about
their looks — what these guard is the contract around them: every portfolio
project has a design and every design has a project, the SVG is well-formed,
and the set obeys the same rules as post covers (target size, no baked-in
text, deterministic output).
"""

import os
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from gen_cover import H, W
from gen_portfolio_cover import COVERS, build_svg

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
PORTFOLIO = os.path.join(REPO_ROOT, "content", "portfolio")


def portfolio_bundles():
    return {
        d
        for d in os.listdir(PORTFOLIO)
        if os.path.isdir(os.path.join(PORTFOLIO, d))
        and os.path.exists(os.path.join(PORTFOLIO, d, "index.md"))
    }


class TestCoverRegistry:
    def test_every_project_has_a_design(self):
        # A new portfolio bundle without a cover design should fail loudly
        # here, not ship with a missing or stale featured.jpg.
        missing = portfolio_bundles() - set(COVERS)
        assert not missing, f"portfolio bundles without a cover design: {sorted(missing)}"

    def test_every_design_has_a_project(self):
        # The reverse: a design for a deleted project is dead code, and its
        # renders would land in a directory Hugo no longer reads.
        orphaned = set(COVERS) - portfolio_bundles()
        assert not orphaned, f"cover designs without a portfolio bundle: {sorted(orphaned)}"

    def test_unknown_slug_raises(self):
        try:
            build_svg("no-such-project")
        except KeyError:
            pass
        else:
            raise AssertionError("expected KeyError for unknown slug")


class TestSvgContract:
    def test_declares_target_dimensions(self):
        for slug in COVERS:
            svg = build_svg(slug)
            assert f'width="{W}"' in svg and f'height="{H}"' in svg, slug
            assert f'viewBox="0 0 {W} {H}"' in svg, slug

    def test_is_well_formed(self):
        for slug in COVERS:
            ET.fromstring(build_svg(slug))

    def test_carries_no_text(self):
        # Same rule as post covers: the card supplies the bilingual title, so
        # text baked into the artwork could not be translated.
        for slug in COVERS:
            svg = build_svg(slug)
            assert "<text" not in svg and "<tspan" not in svg, slug

    def test_is_deterministic(self):
        for slug in COVERS:
            assert build_svg(slug) == build_svg(slug), slug

    def test_designs_are_distinct(self):
        rendered = {slug: build_svg(slug) for slug in COVERS}
        assert len(set(rendered.values())) == len(rendered)
