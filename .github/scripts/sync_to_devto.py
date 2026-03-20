"""Sync an English blog post (Markdown) to dev.to."""

import os
import re
import sys

import requests
import yaml

BASE_URL = "https://shenxianpeng.github.io"
DEVTO_API = "https://dev.to/api"


def parse_front_matter(content):
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1)), content[match.end():]
    return {}, content


def build_canonical_url(post_path):
    # content/posts/2026/hadolint-pre-commit/index.en.md
    # -> https://shenxianpeng.github.io/posts/2026/hadolint-pre-commit/
    parts = post_path.replace("content/", "").replace("/index.en.md", "")
    return f"{BASE_URL}/{parts}/"


def sync_to_devto(post_path, api_key, published):
    with open(post_path, encoding="utf-8") as f:
        raw = f.read()

    front_matter, body = parse_front_matter(raw)

    title = front_matter.get("title", "Untitled")
    tags = front_matter.get("tags") or []
    canonical_url = build_canonical_url(post_path)

    payload = {
        "article": {
            "title": title,
            "body_markdown": body,
            "published": published,
            "tags": [str(t) for t in tags[:4]],  # dev.to allows up to 4 tags
            "canonical_url": canonical_url,
        }
    }

    resp = requests.post(
        f"{DEVTO_API}/articles",
        headers={"api-key": api_key, "Content-Type": "application/json"},
        json=payload,
    )

    if resp.status_code not in (200, 201):
        print(f"Failed to sync to dev.to (HTTP {resp.status_code}): {resp.text}")
        sys.exit(1)

    data = resp.json()
    status = "published" if published else "draft"
    print(f"Successfully synced '{title}' to dev.to as {status}.")
    print(f"dev.to URL: {data.get('url')}")


if __name__ == "__main__":
    post_path = os.environ.get("POST_PATH")
    api_key = os.environ.get("DEVTO_API_KEY")
    published = os.environ.get("PUBLISHED", "false").lower() == "true"

    if not post_path:
        print("POST_PATH environment variable is required.")
        sys.exit(1)
    if not api_key:
        print("DEVTO_API_KEY is required.")
        sys.exit(1)

    sync_to_devto(post_path, api_key, published)
