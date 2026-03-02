"""Sync a blog post (Markdown) to WeChat as a draft article."""

import os
import re
import sys

import markdown
import requests
import yaml


def get_access_token(app_id, app_secret):
    resp = requests.get(
        "https://api.weixin.qq.com/cgi-bin/token",
        params={"grant_type": "client_credential", "appid": app_id, "secret": app_secret},
    )
    data = resp.json()
    token = data.get("access_token")
    if not token:
        print(f"Failed to get access_token: {data}")
        sys.exit(1)
    return token


def parse_front_matter(content):
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1)), content[match.end():]
    return {}, content


def sync_to_wechat(post_path, app_id, app_secret):
    with open(post_path, encoding="utf-8") as f:
        raw = f.read()

    front_matter, body = parse_front_matter(raw)

    title = front_matter.get("title", "Untitled")
    summary = front_matter.get("summary", "")
    digest = summary[:120] if summary else ""  # WeChat digest: max 120 chars
    author = (front_matter.get("authors") or ["shenxianpeng"])[0]

    html_content = markdown.markdown(body, extensions=["fenced_code", "tables"])

    access_token = get_access_token(app_id, app_secret)

    payload = {
        "articles": [
            {
                "title": title,
                "content": html_content,
                "author": author,
                "digest": digest,
                "need_open_comment": 1,
                "only_fans_can_comment": 0,
            }
        ]
    }

    resp = requests.post(
        f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}",
        json=payload,
    )
    data = resp.json()

    if data.get("errmsg") != "ok":
        print(f"Failed to sync to WeChat: {data}")
        sys.exit(1)

    print(f"Successfully synced '{title}' to WeChat as a draft.")
    print(f"Media ID: {data.get('media_id')}")


if __name__ == "__main__":
    post_path = os.environ.get("POST_PATH")
    app_id = os.environ.get("WECHAT_APP_ID")
    app_secret = os.environ.get("WECHAT_APP_SECRET")

    if not post_path:
        print("POST_PATH environment variable is required.")
        sys.exit(1)
    if not app_id or not app_secret:
        print("WECHAT_APP_ID and WECHAT_APP_SECRET are required.")
        sys.exit(1)

    sync_to_wechat(post_path, app_id, app_secret)
