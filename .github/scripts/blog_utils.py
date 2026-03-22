"""Shared utilities for blog sync scripts."""

import re

import yaml

BASE_URL = "https://shenxianpeng.github.io"


def parse_front_matter(content):
    """Parse YAML front matter from markdown content.

    Returns (front_matter_dict, body_str). If no front matter is found,
    returns ({}, original_content).
    """
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1)), content[match.end():]
    return {}, content


def build_canonical_url(post_path):
    """Build canonical URL from a post file path.

    Example:
      content/posts/2026/hadolint-pre-commit/index.en.md
      -> https://shenxianpeng.github.io/posts/2026/hadolint-pre-commit/
    """
    parts = post_path.replace("content/", "").replace("/index.en.md", "")
    return f"{BASE_URL}/{parts}/"
