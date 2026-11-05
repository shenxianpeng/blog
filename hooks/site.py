"""Site-specific build steps for shenxianpeng.dev (MkDocs NG + Sumi).

- Leaves drafts out, as Hugo did.
- Builds the Projects page from the bundles in content/portfolio/.
- Generates the series pages (/series/<name>/) the Hugo site had.
- Keys Giscus threads by the pre-2026-09 path, so comments stay with their post.
- Writes redirect pages for the URLs the Hugo site used before English became
  the default language (/en/<path>/ and untranslated Chinese posts at
  /<path>/), and for Hugo's paginated and taxonomy pages that have no
  equivalent. Old Hexo URLs are front-matter `aliases`, which Sumi handles.
- Copies static/ and assets/img/ and assets/css/ into the site.
"""

from __future__ import annotations

import os
import posixpath
import re
import shutil
from urllib.parse import unquote

import yaml

from mkdocs.structure.files import File, Files, InclusionLevel
from mkdocs.utils.meta import get_data

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REDIRECT = ('<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><title>{to}</title>'
            '<meta name="generator" content="sumi-redirect">'
            '<link rel="canonical" href="{to}"><meta name="robots" content="noindex">'
            '<meta http-equiv="refresh" content="0; url={to}"></head></html>\n')
SITE = 'https://shenxianpeng.dev'

_state: dict = {}


def _lang(config) -> tuple[str, str]:
    """(code, path) of the language being built."""
    from mkdocs import languages

    lang = languages.current(config)
    return (lang.code, lang.path) if lang else ('en', '')


def _slug(name: str) -> str:
    """Hugo's urlize for taxonomy terms: `AI 工具实战` -> `ai-工具实战`."""
    slug = re.sub(r'[\s/\\]+', '-', name.strip().lower())
    return re.sub(r'[^\w.+#~-]', '', slug).strip('.')


def on_config(config):
    with open(os.path.join(ROOT, 'data', 'postfooter.yaml'), encoding='utf-8') as f:
        config.extra['postfooter'] = yaml.safe_load(f)
    code, _ = _lang(config)
    config.extra['lang'] = code
    return config


def on_files(files: Files, config):
    code, _ = _lang(config)
    portfolio = []
    series: dict[str, None] = {}
    for f in list(files):
        if not f.is_documentation_page():
            continue
        try:
            meta = get_data(f.content_string)[1]
        except (OSError, UnicodeDecodeError):
            continue
        if meta.get('draft'):
            files.remove(f)
            continue
        if f.src_uri.startswith(('authors/',)):
            files.remove(f)
            continue
        if f.src_uri.startswith('portfolio/') and f.src_uri != 'portfolio/index.md':
            folder = posixpath.dirname(f.src_uri)
            portfolio.append({
                'title': meta.get('title', ''),
                'summary': ' '.join(str(meta.get('summary', '')).split()),
                'url': meta.get('externalUrl') or f'{folder}/',
                'external': bool(meta.get('externalUrl')),
                'weight': meta.get('weight', 100),
                'image': f'{folder}/featured.jpg' if files.get_file_from_path(f'{folder}/featured.jpg') else None,
            })
            # A project without an outside address keeps its own page.
            if meta.get('externalUrl'):
                files.remove(f)
            continue
        if f.src_uri.startswith(('posts/', 'misc/')):
            s = meta.get('series')
            for name in [s] if isinstance(s, str) else (s or []):
                series.setdefault(str(name))
    config.extra['portfolio'] = sorted(portfolio, key=lambda p: (p['weight'], p['title'].lower()))
    # /series/<name>/: the posts of one series; /series/: all of them.
    names = sorted(series, key=str.lower)
    title = '系列' if code == 'zh-cn' else 'Series'
    lines = [f'# {title}\n']
    for name in names:
        uri = f'series/{_slug(name)}/index.md'
        lines.append(f'- [{name}]({_slug(name)}/index.md)')
        page = File.generated(config, uri, content=(
            f'---\ntemplate: blog.html\nblog_series: {yaml.safe_dump(name, allow_unicode=True).strip().removesuffix("...").strip()}\n'
            f'---\n\n# {name}\n'))
        page.inclusion = InclusionLevel.NOT_IN_NAV
        files.append(page)
    index = File.generated(config, 'series/index.md', content='\n'.join(lines) + '\n')
    index.inclusion = InclusionLevel.NOT_IN_NAV
    files.append(index)
    return files


def on_page_markdown(markdown, page, config, files):
    code, _ = _lang(config)
    # Giscus threads are keyed by the address the page had before 2026-09:
    # "posts/x/" for Chinese, "en/posts/x/" for English.
    page.meta.setdefault('comments_term', page.url if code == 'zh-cn' else f'en/{page.url}')
    # Hugo's `showTableOfContents: false` hides the table of contents.
    if page.meta.get('showTableOfContents') is False:
        page.meta['hide'] = [*page.meta.get('hide', []), 'toc']
    if page.file.src_uri.startswith(('posts/', 'misc/')) and page.file.src_uri.count('/') >= 2:
        page.meta.setdefault('authors', ['shenxianpeng'])
    else:
        page.meta.setdefault('comments', False)
    return markdown


def _write(path: str, html: str, overwrite: bool = False) -> None:
    if os.path.exists(path) and not overwrite:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)


def on_post_page(output, page, config):
    _state.setdefault(_lang(config)[0], set()).add(page.url)
    return output


def on_post_build(config):
    code, path = _lang(config)
    site = config.site_dir
    root = os.path.normpath(os.path.join(site, '..')) if path else site
    pages = _state.pop(code, set())
    if code == 'en':
        for src, dest in ((os.path.join(ROOT, 'static'), root),
                          (os.path.join(ROOT, 'assets', 'img'), os.path.join(root, 'img')),
                          (os.path.join(ROOT, 'assets', 'css'), os.path.join(root, 'assets', 'site')),
                          (os.path.join(ROOT, 'assets', 'js'), os.path.join(root, 'assets', 'site'))):
            shutil.copytree(src, dest, dirs_exist_ok=True)
        # The English feed's address before 2026-09.
        os.makedirs(os.path.join(root, 'en'), exist_ok=True)
        shutil.copyfile(os.path.join(root, 'index.xml'), os.path.join(root, 'en', 'index.xml'))
        # /en/<path>/ -> /<path>/, for every English page.
        for url in pages:
            if url:
                _write(os.path.join(root, 'en', *unquote(url).split('/'), 'index.html'),
                       REDIRECT.format(lang='en', to=f'{SITE}/{url}'))
        moved = {'categories/': 'tags/', 'categories/hexo/': 'tags/', 'authors/': 'about/',
                 'authors/shenxianpeng/': 'about/', 'posts/page/2/': 'posts/'}
    else:
        # /<path>/ -> /zh-cn/<path>/, for Chinese pages that have no English page there.
        for url in pages:
            if url:
                _write(os.path.join(root, *unquote(url).split('/'), 'index.html'),
                       REDIRECT.format(lang='zh-cn', to=f'{SITE}/{path}/{url}'))
        moved = {f'{path}/categories/': f'{path}/tags/', f'{path}/categories/hexo/': f'{path}/tags/',
                 f'{path}/authors/': f'{path}/about/', f'{path}/authors/shenxianpeng/': f'{path}/about/',
                 f'{path}/posts/page/2/': f'{path}/posts/', f'{path}/posts/page/3/': f'{path}/posts/'}
    for old, new in moved.items():
        _write(os.path.join(root, *old.split('/'), 'index.html'), REDIRECT.format(lang=code, to=f'{SITE}/{new}'))
