"""Tests for the cover generator.

These cover the two invariants that actually broke while building it: seeding
that collided across posts sharing a slug, and renders that came back the wrong
size. Both are cheap to assert and expensive to notice by eye across 259 files.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from gen_cover import MOTIFS, H, W, build_svg, choose_motif, cover_key, primary_tag


class TestCoverKey:
    def test_strips_content_prefix(self):
        assert cover_key("content/posts/2026/aiops") == "posts/2026/aiops"

    def test_same_slug_different_year_gets_different_key(self):
        # The real bug: main() seeded on os.path.basename(), so these two posts
        # were handed one cover. The key must keep them apart.
        a = cover_key("content/posts/2025/jenkinsfilelint")
        b = cover_key("content/posts/2026/jenkinsfilelint")
        assert a != b
        assert build_svg(a, "Jenkins") != build_svg(b, "Jenkins")

    def test_same_slug_different_section_gets_different_key(self):
        a = cover_key("content/posts/2026/pycon-lt-d1")
        b = cover_key("content/misc/pycon-lt-d1")
        assert a != b
        assert build_svg(a, "Work") != build_svg(b, "Work")

    def test_trailing_slash_is_stable(self):
        assert cover_key("content/posts/2026/a/") == cover_key("content/posts/2026/a")


class TestDeterminism:
    def test_same_input_same_output(self):
        # Re-running the generator must not churn the repo.
        assert build_svg("posts/2026/a", "Jenkins") == build_svg("posts/2026/a", "Jenkins")

    def test_different_paths_differ(self):
        assert build_svg("posts/2026/a", "Jenkins") != build_svg("posts/2026/b", "Jenkins")

    def test_same_slug_different_year_differs(self):
        # The bug this guards: seeding on the bare slug handed
        # posts/2025/jenkinsfilelint and posts/2026/jenkinsfilelint one cover.
        a = build_svg("posts/2025/jenkinsfilelint", "Jenkins")
        b = build_svg("posts/2026/jenkinsfilelint", "Jenkins")
        assert a != b

    def test_tag_drives_palette(self):
        # Same composition seed, different tag — the artwork must recolour.
        assert build_svg("posts/2026/a", "Jenkins") != build_svg("posts/2026/a", "Python")

    def test_missing_tag_is_tolerated(self):
        svg = build_svg("posts/2026/a", "")
        assert svg.startswith("<svg")


class TestSvgShape:
    def test_declares_target_dimensions(self):
        svg = build_svg("posts/2026/a", "AI")
        assert f'width="{W}"' in svg and f'height="{H}"' in svg
        assert f'viewBox="0 0 {W} {H}"' in svg

    def test_is_well_formed(self):
        import xml.etree.ElementTree as ET

        # Parses as XML, so a malformed motif cannot ship a broken render.
        for slug in ("posts/2026/a", "posts/2020/b", "misc/c", "posts/2019/d"):
            ET.fromstring(build_svg(slug, "DevOps"))

    def test_carries_no_text(self):
        # AGENTS.md forbids baked-in text: it is illegible in a 600px card and
        # cannot be translated for the English version of the post.
        for slug in ("posts/2026/a", "posts/2020/b", "misc/c"):
            svg = build_svg(slug, "Git")
            assert "<text" not in svg and "<tspan" not in svg

    def test_all_motifs_reachable(self):
        # A seeding change could silently collapse every post onto one shape,
        # which is invisible in review and obvious on the live list page.
        chosen = {choose_motif(f"posts/2026/post-{i}") for i in range(80)}
        assert chosen == set(MOTIFS)

    def test_motif_choice_is_stable(self):
        assert choose_motif("posts/2026/a") is choose_motif("posts/2026/a")


class TestPrimaryTag:
    def _post(self, tmp, front_matter):
        d = os.path.join(tmp, "post")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.md"), "w", encoding="utf-8") as f:
            f.write(front_matter)
        return d

    def test_reads_first_tag(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = self._post(tmp, "---\ntitle: T\ntags:\n  - Jenkins\n  - Git\n---\nBody")
            assert primary_tag(d) == "Jenkins"

    def test_no_tags_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = self._post(tmp, "---\ntitle: T\ndate: 2026-01-01\n---\nBody")
            assert primary_tag(d) == ""

    def test_missing_front_matter_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = self._post(tmp, "Just a body, no front matter.")
            assert primary_tag(d) == ""

    def test_field_after_tags_stops_collection(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = self._post(tmp, "---\ntags:\nauthors:\n  - shenxianpeng\n---\nBody")
            assert primary_tag(d) == ""

    def test_missing_directory_returns_empty(self):
        assert primary_tag("/nonexistent/post") == ""
