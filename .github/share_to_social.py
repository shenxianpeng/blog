import os
import requests
from pathlib import Path

# --- Config ---
DEVTO_API_KEY = os.getenv('DEVTO_API_KEY')
MEDIUM_TOKEN = os.getenv('MEDIUM_INTEGRATION_TOKEN')
X_BEARER_TOKEN = os.getenv('X_BEARER_TOKEN')

# --- Helper: Get latest post ---
def get_latest_post():
    posts = list(Path('content/posts').glob('*/index.md')) + list(Path('content/posts').glob('*/index.en.md'))
    posts += list(Path('content/misc').glob('*/index.md')) + list(Path('content/misc').glob('*/index.en.md'))
    posts = [p for p in posts if p.is_file()]
    if not posts:
        return None
    posts.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return posts[0]

# --- Dev.to ---
def share_to_devto(title, content):
    url = 'https://dev.to/api/articles'
    headers = {'api-key': DEVTO_API_KEY}
    data = {
        'article': {
            'title': title,
            'published': True,
            'body_markdown': content,
            'tags': ['blog', 'python'],
        }
    }
    if r.status_code >= 200 and r.status_code < 300:
        print(f'Dev.to: Success ({r.status_code})')
    else:
        print(f'Dev.to: Failed ({r.status_code}) - {r.reason}')

# --- Medium ---
def share_to_medium(title, content):
    url = 'https://api.medium.com/v1/users/me/posts'
    headers = {
        'Authorization': f'Bearer {MEDIUM_TOKEN}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    data = {
        'title': title,
        'contentFormat': 'markdown',
        'content': content,
        'publishStatus': 'public',
        'tags': ['blog', 'python'],
    }
    if r.status_code == 201:
        print('Medium: Success (201 Created)')
    else:
        print(f'Medium: Failed ({r.status_code})')
        # Optionally, print a sanitized error message
        error_msg = r.json().get('message') if r.headers.get('Content-Type', '').startswith('application/json') else None
        if error_msg:
            print(f'Medium: Error message: {error_msg}')

# --- X (Twitter) ---
def share_to_x(title, url):
    api_url = 'https://api.twitter.com/2/tweets'
    headers = {
        'Authorization': f'Bearer {X_BEARER_TOKEN}',
        'Content-Type': 'application/json',
    }
    data = {
        'text': f'New blog post: {title} {url}'
    }
    r = requests.post(api_url, json=data, headers=headers)
    if r.status_code == 201:
        logging.info(f'X: Tweet posted successfully (status code: {r.status_code})')
    else:
        logging.warning(f'X: Failed to post tweet (status code: {r.status_code})')
# --- Main ---
def main():
    post = get_latest_post()
    if not post:
        print('No post found.')
        return
    with open(post, 'r', encoding='utf-8') as f:
        content = f.read()
    # Robust title extraction: first markdown heading
    match = next((re.match(r'^\s*#+\s+(.*)', line) for line in content.splitlines() if line.strip()), None)
    title = match.group(1).strip() if match else 'Blog Post'
    # Share to Dev.to
    if DEVTO_API_KEY:
        share_to_devto(title, content)
    # Share to Medium
    if MEDIUM_TOKEN:
        share_to_medium(title, content)
    # Share to X (Twitter)
    if X_BEARER_TOKEN:
        # You may want to use your blog URL here
        blog_url = f'https://shenxianpeng.github.io/posts/{post.parent.name}/'
        share_to_x(title, blog_url)

if __name__ == '__main__':
    main()
