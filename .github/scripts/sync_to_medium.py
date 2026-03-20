"""Sync an English blog post (Markdown) to Medium."""

import os
import re
import sys

import requests
import yaml

BASE_URL = "https://shenxianpeng.github.io"
MEDIUM_API = "https://api.medium.com/v1"


def parse_front_matter(content):
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1)), content[match.end():]
    return {}, content


def get_author_id(token):
    resp = requests.get(
        f"{MEDIUM_API}/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = resp.json()
    author_id = data.get("data", {}).get("id")
    if not author_id:
        print(f"Failed to get Medium user ID: {data}")
        sys.exit(1)
    return author_id


def build_canonical_url(post_path):
    # content/posts/2026/hadolint-pre-commit/index.en.md
    # -> https://shenxianpeng.github.io/posts/2026/hadolint-pre-commit/
    parts = post_path.replace("content/", "").replace("/index.en.md", "")
    return f"{BASE_URL}/{parts}/"


def sync_to_medium(post_path, token, publish_status):
    with open(post_path, encoding="utf-8") as f:
        raw = f.read()

    front_matter, body = parse_front_matter(raw)

    title = front_matter.get("title", "Untitled")
    tags = front_matter.get("tags") or []
    canonical_url = build_canonical_url(post_path)

    # Prepend canonical note and title so Medium article is self-contained
    content = f"# {title}\n\n> Originally published at [{canonical_url}]({canonical_url})\n\n{body}"

    author_id = get_author_id(token)

    payload = {
        "title": title,
        "contentFormat": "markdown",
        "content": content,
        "tags": [str(t) for t in tags[:5]],  # Medium allows up to 5 tags
        "canonicalUrl": canonical_url,
        "publishStatus": publish_status,
    }

    resp = requests.post(
        f"{MEDIUM_API}/users/{author_id}/posts",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    data = resp.json()

    post_data = data.get("data", {})
    if not post_data.get("id"):
        print(f"Failed to sync to Medium: {data}")
        sys.exit(1)

    print(f"Successfully synced '{title}' to Medium as {publish_status}.")
    print(f"Medium URL: {post_data.get('url')}")


if __name__ == "__main__":
    post_path = os.environ.get("POST_PATH")
    token = os.environ.get("MEDIUM_INTEGRATION_TOKEN")
    publish_status = os.environ.get("PUBLISH_STATUS", "draft")

    if not post_path:
        print("POST_PATH environment variable is required.")
        sys.exit(1)
    if not token:
        print("MEDIUM_INTEGRATION_TOKEN is required.")
        sys.exit(1)

    sync_to_medium(post_path, token, publish_status)
