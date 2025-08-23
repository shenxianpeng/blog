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
BASE_BRANCH = os.getenv('GITHUB_REF_NAME', 'main')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def find_missing_files():
    missing = []
    for folder in ['content/posts', 'content/misc']:
        subs = [sub for sub in Path(folder).glob('*/') if sub.is_dir()]
        # Sort subfolders by modification time, latest first
        subs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        for sub in subs:
            zh = sub / 'index.md'
            en = sub / 'index.en.md'
            if zh.exists() and not en.exists():
                missing.append((sub, 'en'))
            elif en.exists() and not zh.exists():
                missing.append((sub, 'zh'))
    return missing

def translate_with_gemini(src_path, target_lang):
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    prompt = f"""
Translate the following markdown blog post to {'Chinese' if target_lang == 'zh' else 'English'}.
Keep all formatting, code blocks, and technical terms. Only return the translated markdown.

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

def create_pr(branch_name, files):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO)
    pr = repo.create_pull(
        title='Auto-translate missing blog post(s)',
        body='This PR was created automatically to add missing Chinese/English blog post versions.',
        head=branch_name,
        base=BASE_BRANCH
    )
    pr.add_to_assignees(repo.owner.login)
    pr.add_to_labels(['translate'])
    print(f'Created PR: {pr.html_url}')

def main():
    missing = find_missing_files()
    if not missing:
        print('No missing files detected.')
        return
    # Only process one post per run
    sub, lang = missing[0]
    branch_name = BRANCH_PREFIX + f'add-missing-{sub.name}-{lang}-{os.getpid()}'
    create_branch(branch_name)
    src = sub / ('index.en.md' if lang == 'zh' else 'index.md')
    target = sub / ('index.md' if lang == 'zh' else 'index.en.md')
    print(f'Translating {src} -> {target}')
    translated = translate_with_gemini(src, lang)
    if not translated:
        print('Translation failed or quota exceeded. Exiting without commit or PR.')
        return
    with open(target, 'w', encoding='utf-8') as f:
        f.write(translated)
    commit_and_push(branch_name, [str(target)])
    create_pr(branch_name, [str(target)])

if __name__ == '__main__':
    main()
