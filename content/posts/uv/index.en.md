---
title: Still using pip and venv? You're outdated! Try uv!
summary: |
  uv is a Python package management tool developed by the Astral team. It replaces the functionality of pip, venv, and pip-tools, offering faster dependency resolution and a more modern project management approach.
tags:
  - uv
  - pip
author: shenxianpeng
date: 2025-05-05
---

If you're used to `pip install`, manually creating virtual environments, and managing `requirements.txt` yourself, you might be surprised by [uv](https://docs.astral.sh/uv/).

This is a Python package management tool developed by the [Astral](https://astral.sh/) team and written in Rust.  It not only replaces the functionality of pip, venv, and pip-tools, but also provides faster dependency resolution and a more modern project management approach.

### Start with `uv init` to create a project skeleton with one command

We won't start with "how to install uv," but with "how to use uv to create a project."


```bash
uv init
```

After running this command, uv will help you:

* Create a `.venv` virtual environment;
* Initialize the `pyproject.toml` configuration file;
* (Optional) Add dependencies;
* Generate a `uv.lock` lock file;
* Set `.venv` as the default environment for the current directory (no manual activation needed);

The entire process only requires one command to complete what used to take multiple steps, making it a better starting point for building Python projects.

### Install dependencies using `uv add` (instead of pip install)

The traditional way is:

```bash
pip install requests
```

But in the uv world, adding dependencies looks like this:

```bash
uv add requests
```

The benefits are:

* Automatically writes to `pyproject.toml`'s `[project.dependencies]`;
* Automatically installs into `.venv`;
* Automatically updates the `uv.lock` lock file;
* No need to maintain `requirements.txt` anymore.

If you want to add development dependencies (such as testing or formatting tools), you can:

```bash
uv add --dev pytest ruff
```

Want to remove dependencies?

```bash
uv remove requests
```

### Running project scripts or tools: `uv venv` + `uvx`

uv's virtual environment is installed by default in `.venv`, but you **don't need to `source activate` every time**.  Just execute:

```bash
uv venv
```

This ensures that `.venv` exists and is automatically configured as the default Python environment for the current shell.  After that, you can run scripts or tools without worrying about path issues.

Even better, uv provides a `uvx` command, similar to `pipx` and Node.js's `npx`, which allows you to directly run CLI tools installed in the project.

For example, let's use `ruff` to check or format Python code:

```bash
uvx ruff check .
uvx ruff format .
```

Now with `uvx`, you don't need to install a bunch of global tools, nor do you need to use `pre-commit` to unify command calls—use it directly within the project, it's cross-platform and convenient.

### Example Project Structure

After `uv init` and some `uv add` commands, a clean Python project structure might look like this:

```
my-project/
├── .venv/               ← Virtual environment
├── pyproject.toml       ← Project configuration (dependencies, metadata, etc.)
├── uv.lock              ← Locked dependency versions
├── main.py              ← Project entry script
```

### User Experience?

I've recently adopted uv as the default tool for new projects:

* No more manually writing `requirements.txt`
* No more struggling with mixing `poetry.lock` and `pyproject.toml`
* Dependency installation is very fast, 3-5 times faster for large projects on the first installation.
* Combined with `ruff` as a Lint + Format tool, there's no need to install black and flake8 separately.

In CI, I'm also gradually replacing `pip install -r requirements.txt` with it, using the lock file to build the environment for stronger consistency.

### Summary

If you:

* Are dissatisfied with the slow speed of `pip install`;
* Don't want to write a bunch of requirements files;
* Want a more modern, faster, and more automated Python project structure;

Then you should try `uv`. It's a faster and more modern package manager toolset.

Starting with your next project, why not start with `uv init`?

Project address: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

---

Please indicate the author and source when reprinting this article. Please do not use it for any commercial purposes. Welcome to follow the WeChat official account "DevOps攻城狮"