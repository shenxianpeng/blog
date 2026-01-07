import os
import subprocess
from pathlib import Path
from github import Github
import google.generativeai as genai

# Config
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO = os.getenv('GITHUB_REPOSITORY', 'shenxianpeng/blog')
BRANCH_PREFIX = 'auto-translate/'
BASE_BRANCH = 'main'

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def find_missing_files():
    missing = []
    for folder in ['content/posts', 'content/misc']:
        # Use **/*/ to search recursively through year folders
        subs = [sub for sub in Path(folder).glob('**/*') if sub.is_dir() and (sub / 'index.md').exists() or (sub / 'index.en.md').exists()]
        for sub in subs:
            zh = sub / 'index.md'
            en = sub / 'index.en.md'
            # Helper to check if translate: false is present
            def should_translate(path):
                if not path.exists():
                    return True
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip().lower().startswith('translate:'):
                                if 'false' in line.lower():
                                    return False
                                else:
                                    return True
                except Exception:
                    return True
                return True
            if zh.exists() and not en.exists() and should_translate(zh):
                missing.append((sub, 'en'))
            elif en.exists() and not zh.exists() and should_translate(en):
                missing.append((sub, 'zh'))
    return missing

def translate_with_gemini(src_path, target_lang):
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    prompt = f"""
Translate the following blog post to {'Chinese' if target_lang == 'zh' else 'English'}.
Keep all formatting, code blocks, and technical terms.

- Do not change any format of the original (e.g., title, summary, tags).
- In the `title:` field, replace any colons (`:`) with an em dash (`—`) or remove them if present, so the result is always valid for Hugo.
- Preserve all code blocks and inline code exactly as is.
- The output MUST start with `---` (three hyphens) for the YAML front matter, NOT with ```yaml or any code fence marker.
- The output MUST NOT be wrapped in markdown code fences (```) - return only the raw translated markdown content.
- Return the translated content directly without any formatting markers like ```yaml or ``` at the beginning or end.

{content}
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        if hasattr(e, 'message') and 'quota' in str(e.message).lower():
            print('Gemini API quota exceeded. Skipping translation for this run.')
        elif 'quota' in str(e).lower():
            print('Gemini API quota exceeded. Skipping translation for this run.')
        else:
            print(f'Error during translation: {e}')
        return None

def create_branch(branch_name):
    subprocess.run(['git', 'checkout', BASE_BRANCH], check=True)
    subprocess.run(['git', 'checkout', '-b', branch_name], check=True)

def commit_and_push(branch_name, files):
    subprocess.run(['git', 'add'] + files, check=True)
    subprocess.run(['git', 'commit', '-m', f'Auto-translate missing blog post(s)'], check=True)
    subprocess.run(['git', 'push', 'origin', branch_name], check=True)

def check_existing_pr(repo, post_name, lang):
    """Check if there's already an open PR for this post translation"""
    try:
        # Get all open PRs with 'translate' label
        pulls = repo.get_pulls(state='open', base=BASE_BRANCH)
        for pr in pulls:
            # Check if PR title or branch name contains the post name
            if post_name in pr.head.ref and f'-{lang}-' in pr.head.ref:
                print(f'Found existing PR for {post_name} ({lang}): {pr.html_url}')
                return True
        return False
    except Exception as e:
        print(f'Error checking existing PRs: {e}')
        return False

def branch_exists_remotely(branch_name):
    """Check if branch already exists on remote"""
    try:
        result = subprocess.run(
            ['git', 'ls-remote', '--heads', 'origin', branch_name],
            capture_output=True,
            text=True,
            check=True
        )
        return bool(result.stdout.strip())
    except Exception as e:
        print(f'Error checking remote branch: {e}')
        return False

def create_pr(branch_name, files, post_name):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO)
    pr = repo.create_pull(
        title=f'Auto-translate: {post_name}',
        body=f'This PR was created automatically to add missing translation for **{post_name}**.\n\nTranslated files:\n' + '\n'.join(f'- `{f}`' for f in files),
        head=branch_name,
        base=BASE_BRANCH
    )
    pr.add_to_labels('translate')
    # Request review from repo owner and GitHub Copilot
    reviewers = [repo.owner.login]
    try:
        pr.create_review_request(reviewers=reviewers)
    except Exception as e:
        print(f'Failed to request reviewers: {e}')
    print(f'Created PR: {pr.html_url}')

def main():
    missing = find_missing_files()
    if not missing:
        print('No missing files detected.')
        return
    print(f'Found {len(missing)} missing translation(s)')
    
    # Initialize GitHub client if running in CI
    g = None
    repo = None
    if os.getenv('GITHUB_ACTIONS', 'false').lower() == 'true':
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO)
    
    # Only process one post per run, but check for existing PRs first
    for sub, lang in missing:
        post_name = sub.name
        
        # Check if PR already exists for this post
        if repo and check_existing_pr(repo, post_name, lang):
            print(f'Skipping {post_name} ({lang}) - PR already exists')
            continue
        
        # Create branch name without PID to avoid duplicates
        branch_name = BRANCH_PREFIX + f'add-missing-{post_name}-{lang}'
        
        # Check if branch already exists remotely
        if branch_exists_remotely(branch_name):
            print(f'Skipping {post_name} ({lang}) - branch {branch_name} already exists')
            continue
        
        # Found a post that needs translation and has no existing PR
        print(f'Processing: {post_name} ({lang})')
        create_branch(branch_name)
        src = sub / ('index.en.md' if lang == 'zh' else 'index.md')
        target = sub / ('index.md' if lang == 'zh' else 'index.en.md')
        print(f'Translating {src} -> {target}')
        translated = translate_with_gemini(src, lang)
        if not translated:
            print('Translation failed or quota exceeded. Exiting without commit or PR.')
            # Clean up branch
            subprocess.run(['git', 'checkout', BASE_BRANCH], check=False)
            subprocess.run(['git', 'branch', '-D', branch_name], check=False)
            return
        with open(target, 'w', encoding='utf-8') as f:
            f.write(translated)
        # Only commit and create PR if running in CI (GitHub Actions)
        if os.getenv('GITHUB_ACTIONS', 'false').lower() == 'true':
            commit_and_push(branch_name, [str(target)])
            create_pr(branch_name, [str(target)], post_name)
        else:
            print('Running locally: skipping commit and PR creation.')
        # Only process one post per run
        return
    
    print('All missing translations either have existing PRs or branches.')

if __name__ == '__main__':
    main()
