"""Structural checks on post tags.

Tags become URLs, so a few characters and spellings break the taxonomy in
ways that are invisible in the front matter and only show up as a wrong page
on the live site. These guard the two failures this repository has actually
hit.
"""

import os
import re
import sys
from collections import defaultdict

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
CONTENT = os.path.join(REPO_ROOT, "content")
SECTIONS = ("posts", "misc")


def tags_by_file():
    """Map each content file to the tag list in its front matter."""
    found = {}
    for section in SECTIONS:
        for d, _, files in os.walk(os.path.join(CONTENT, section)):
            for f in files:
                if not (f.startswith("index") and f.endswith(".md")):
                    continue
                path = os.path.join(d, f)
                with open(path, encoding="utf-8") as fh:
                    m = re.search(r"^---\n(.*?)\n---", fh.read(), re.S)
                if not m:
                    continue
                tags, collecting = [], False
                for line in m.group(1).split("\n"):
                    if re.match(r"^tags:\s*$", line):
                        collecting = True
                        continue
                    if collecting:
                        if re.match(r"^\s*-\s+", line):
                            tags.append(line.split("-", 1)[1].strip().strip("\"'"))
                        elif re.match(r"^\S", line):
                            break
                if tags:
                    found[os.path.relpath(path, REPO_ROOT)] = tags
    return found


ALL_TAGS = tags_by_file()


def test_content_was_found():
    # A silent zero here would make every other check vacuously pass.
    assert len(ALL_TAGS) > 100, f"only found {len(ALL_TAGS)} tagged files — walk is broken"


def test_no_slash_in_tag():
    """A slash turns one term into a nested URL that collides with its parent.

    'CI/CD' rendered at /tags/ci/cd/, which made the sibling tag 'CI' at
    /tags/ci/ swallow its posts and mislabel itself in the term list.
    """
    offenders = {f: [t for t in tags if "/" in t] for f, tags in ALL_TAGS.items()}
    offenders = {f: t for f, t in offenders.items() if t}
    assert not offenders, f"tags containing '/' break taxonomy URLs: {offenders}"


def test_no_case_only_duplicates():
    """Two spellings of one tag split its posts across two term pages."""
    by_lower = defaultdict(set)
    for tags in ALL_TAGS.values():
        for t in tags:
            by_lower[t.lower()].add(t)
    dupes = {k: sorted(v) for k, v in by_lower.items() if len(v) > 1}
    assert not dupes, f"tags differing only by case: {dupes}"


def test_no_leading_or_trailing_whitespace():
    offenders = {
        f: [t for t in tags if t != t.strip()] for f, tags in ALL_TAGS.items()
    }
    offenders = {f: t for f, t in offenders.items() if t}
    assert not offenders, f"tags with stray whitespace: {offenders}"


def test_no_empty_tags():
    offenders = {f: tags for f, tags in ALL_TAGS.items() if any(not t for t in tags)}
    assert not offenders, f"empty tag entries: {offenders}"


def test_no_duplicate_tag_within_a_post():
    offenders = {
        f: tags for f, tags in ALL_TAGS.items() if len(tags) != len(set(tags))
    }
    assert not offenders, f"the same tag listed twice in one post: {offenders}"


if __name__ == "__main__":
    sys.exit("run with pytest")
