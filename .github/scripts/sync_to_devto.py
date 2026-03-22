"""Sync an English blog post (Markdown) to dev.to.

Supports upsert: if an article with the same canonical_url already exists,
it will be updated (PUT) rather than created again (POST).
"""

import os
import sys

import requests

from blog_utils import build_canonical_url, parse_front_matter

DEVTO_API = "https://dev.to/api"


def find_existing_article(api_key, canonical_url):
    """Return the dev.to article ID if an article with this canonical_url exists."""
    try:
        resp = requests.get(
            f"{DEVTO_API}/articles/me/all",
            headers={"api-key": api_key},
            params={"per_page": 1000},
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Warning: could not query existing articles: {e}")
        return None

    for article in resp.json():
        if article.get("canonical_url") == canonical_url:
            return article["id"]
    return None


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

    headers = {"api-key": api_key, "Content-Type": "application/json"}
    existing_id = find_existing_article(api_key, canonical_url)

    try:
        if existing_id:
            resp = requests.put(
                f"{DEVTO_API}/articles/{existing_id}",
                headers=headers,
                json=payload,
            )
            action = "updated"
        else:
            resp = requests.post(
                f"{DEVTO_API}/articles",
                headers=headers,
                json=payload,
            )
            action = "created"
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to sync to dev.to: {e}")
        sys.exit(1)

    data = resp.json()
    status = "published" if published else "draft"
    print(f"Successfully {action} '{title}' on dev.to as {status}.")
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
