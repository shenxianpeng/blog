---
title: Setting up Sphinx + ReadTheDocs from Scratch: Rapidly Deploying Automated Documentation
summary: |
  In open-source projects or team collaborations, Sphinx + ReadTheDocs provides an easy-to-maintain, automatically deployable documentation system. This article documents the configuration process and considerations.
tags:
  - Sphinx
  - ReadTheDocs
  - RST
author: shenxianpeng
date: 2025-04-12
---

In daily open-source projects or team collaborations, we often need an easy-to-maintain, automatically deployable documentation system.

Recently, while maintaining my own open-source project, I tried using [Sphinx](https://www.sphinx-doc.org/) to generate documentation and [ReadTheDocs](https://readthedocs.org/) to achieve automatic building and hosting. The overall experience was quite good.

I'm documenting the configuration process here, hoping it can help others with similar needs.

## Why Choose Sphinx and ReadTheDocs

- **Sphinx** is a documentation generator written in Python, initially designed for the official Python documentation. It supports reStructuredText and Markdown (via plugins).
- **ReadTheDocs** is a documentation hosting platform that can automatically pull code from your Git repository, build, and publish documentation, supporting webhook auto-triggering.

The combination of these two tools is ideal for continuously maintaining and updating documentation, and the community is mature with abundant resources.



## Basic Configuration Steps

Below is the complete process configured in a real project.

### 1. Install Sphinx and Related Dependencies

It's recommended to use a virtual environment, then install:

```bash
# docs/requirements.txt
sphinx==5.3.0
sphinx_rtd_theme==1.1.1

# If you need Markdown support, add:
myst_parser==0.18.1
```

Install dependencies:

```bash
pip install -r docs/requirements.txt
```

Notes:

- `sphinx-rtd-theme` is the default theme used by ReadTheDocs
- `myst-parser` is used to support Markdown

### 2. Initialize the Documentation Project Structure

In the project root directory, execute:

```bash
sphinx-quickstart docs
```

It is recommended to separate the `source` and `build` directories.

After execution, the `docs` directory will generate files such as `conf.py` and `index.rst`.

### 3. Modify the `conf.py` Configuration File

Several key settings are as follows:

```python
# Read the Docs configuration file
# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details
from datetime import datetime

project = "GitStats"
author = "Xianpeng Shen"
copyright = f"{datetime.now().year}, {author}"
html_theme = "sphinx_rtd_theme"
```

If you need Markdown support, you need to add the following to `conf.py`:

```python
extensions = [
    'myst_parser',  # Support Markdown
]
```

## Configuring ReadTheDocs for Automatic Building

As long as the project structure is clear, ReadTheDocs can basically run with one click.

### 1. Import the Project to ReadTheDocs

- Log in to [https://readthedocs.org/](https://readthedocs.org/)
- Click "Import a Project" and select your GitHub or GitLab repository
- Ensure the repository contains `docs/conf.py`; the system will automatically recognize it.

### 2. Add the `.readthedocs.yml` Configuration File

To better control the build process, it is recommended to add `.readthedocs.yml` to the project root directory:

```yaml
# Read the Docs configuration file
# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details
version: 2

build:
  os: ubuntu-24.04
  tools:
    python: "3.12"

sphinx:
   configuration: docs/source/conf.py

python:
   install:
   - requirements: docs/requirements.txt
```

After configuration, every time you submit a Pull Request, ReadTheDocs will automatically pull and build the latest documentation for preview, ensuring the documentation is as expected.

## Final Result

After building, ReadTheDocs will provide a documentation address similar to `https://your-project.readthedocs.io/`, facilitating team collaboration and user consultation.

My current open-source project also uses this scheme, for example: [GitStats documentation](https://gitstats.readthedocs.io/en/latest/)

![GitStats documentation](example.png)

## Summary

By following the above configuration, you can almost achieve "submit after writing documentation, and it goes live," greatly improving the efficiency of documentation maintenance.

If you are writing open-source project documentation, or want to add a documentation system to a team project (especially Python projects), you might want to try Sphinx + ReadTheDocs.

---

Please indicate the author and source when reprinting this article, and do not use it for any commercial purposes. Welcome to follow the official account "DevOps攻城狮" (DevOps Engineers).