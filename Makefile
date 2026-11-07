default: dev

d: dev
dev:
	mkdocs serve

b: build
build:
	mkdocs build

# Install what the site needs to build
install-site:
	pip3 install -r site-requirements.txt

# Install dependencies for translation
install-deps:
	pip3 install -r requirements.txt

# Auto translate Chinese posts to English (requires Gemini API key)
translate:
	python3 .github/auto_translate.py

# Create a git checkpoint with a timestamp
checkpoint:
	@git add -A
	@git commit -m "checkpoint at $$(date '+%Y-%m-%dT%H:%M:%S%z')"
	@git pull --rebase
	@git push
	@echo Checkpoint created and pushed to remote

# make help
help:
	@echo "Available targets:"
	@echo "  install-site      Install MkDocs NG, Sumi and the Markdown extensions"
	@echo "  dev               Serve the site with live reload"
	@echo "  build             Build the site into site/"
	@echo "  install-deps      Install dependencies for translation"
	@echo "  translate         Auto translate Chinese posts to English (requires Gemini API key)"
	@echo "  checkpoint        Create a git checkpoint with a timestamp"

.PHONY: dev build install-site install-deps translate checkpoint help
