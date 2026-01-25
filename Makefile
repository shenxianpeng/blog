default: dev

d: dev
dev:
	hugo serve --buildFuture

b: build
build:
	hugo build

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
	@git push
	@echo Checkpoint created and pushed to remote

# Update submodules
update-submodules:
	@git submodule update --init --recursive

# make help
help:
	@echo "Available targets:"
	@echo "  dev               Serve the site with Hugo (including future content)"
	@echo "  build             Build the site with Hugo"
	@echo "  install-deps      Install dependencies for translation"
	@echo "  translate         Auto translate Chinese posts to English (requires Gemini API key)"
	@echo "  checkpoint        Create a git checkpoint with a timestamp"
	@echo "  update-submodules Update git submodules"

.PHONY: dev build install-deps translate checkpoint update-submodules help
