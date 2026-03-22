"""Tests for blog_utils shared module."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from blog_utils import build_canonical_url, parse_front_matter


class TestParseFrontMatter:
    def test_valid_front_matter(self):
        content = "---\ntitle: Hello World\ntags:\n  - devops\n---\nBody text here."
        front_matter, body = parse_front_matter(content)
        assert front_matter["title"] == "Hello World"
        assert front_matter["tags"] == ["devops"]
        assert body == "Body text here."

    def test_missing_front_matter(self):
        content = "No front matter here."
        front_matter, body = parse_front_matter(content)
        assert front_matter == {}
        assert body == "No front matter here."

    def test_empty_tags_field(self):
        content = "---\ntitle: No Tags\ntags:\n---\nBody."
        front_matter, _ = parse_front_matter(content)
        # yaml.safe_load returns None for empty field — callers should use `or []`
        assert front_matter.get("tags") is None


class TestBuildCanonicalUrl:
    def test_standard_path(self):
        path = "content/posts/2026/hadolint-pre-commit/index.en.md"
        url = build_canonical_url(path)
        assert url == "https://shenxianpeng.github.io/posts/2026/hadolint-pre-commit/"

    def test_trailing_slash(self):
        path = "content/posts/2025/my-post/index.en.md"
        url = build_canonical_url(path)
        assert url.endswith("/")
