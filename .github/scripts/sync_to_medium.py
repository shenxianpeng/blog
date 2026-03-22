"""Sync an English blog post (Markdown) to Medium.

Tracks synced articles in .github/scripts/.synced_medium.json to prevent
duplicate posts (Medium API does not support querying by canonical URL).
"""

import json
import os
import sys
from pathlib import Path

import requests

from blog_utils import build_canonical_url, parse_front_matter

MEDIUM_API = "https://api.medium.com/v1"
SYNCED_RECORD = Path(__file__).parent / ".synced_medium.json"


def load_synced_record():
    """Return dict of {canonical_url: medium_post_id}."""
    if SYNCED_RECORD.exists():
        try:
            return json.loads(SYNCED_RECORD.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            print("Warning: could not read .synced_medium.json, treating as empty.")
    return {}


def save_synced_record(record):
    SYNCED_RECORD.write_text(json.dumps(record, indent=2), encoding="utf-8")


def get_author_id(token):
    try:
        resp = requests.get(
            f"{MEDIUM_API}/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to get Medium user ID: {e}")
        sys.exit(1)

    author_id = resp.json().get("data", {}).get("id")
    if not author_id:
        print(f"Unexpected response from Medium /me: {resp.text}")
        sys.exit(1)
    return author_id


def sync_to_medium(post_path, token, publish_status):
    with open(post_path, encoding="utf-8") as f:
        raw = f.read()

    front_matter, body = parse_front_matter(raw)

    title = front_matter.get("title", "Untitled")
    tags = front_matter.get("tags") or []
    canonical_url = build_canonical_url(post_path)

    synced = load_synced_record()

    if canonical_url in synced:
        print(
            f"'{title}' was already synced to Medium "
            f"(post ID: {synced[canonical_url]}). "
            "Medium does not support updating posts via API — edit it manually if needed."
        )
        return

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

    try:
        resp = requests.post(
            f"{MEDIUM_API}/users/{author_id}/posts",
            headers={"Authorization": f"Bearer {token}"},
            json=payload,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to sync to Medium: {e}")
        sys.exit(1)

    post_data = resp.json().get("data", {})
    if not post_data.get("id"):
        print(f"Unexpected response from Medium: {resp.text}")
        sys.exit(1)

    synced[canonical_url] = post_data["id"]
    save_synced_record(synced)

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
