default: dev

d:dev
dev:
	hugo serve --buildFuture

b:build
build:
	hugo build

.PHONY: default d dev b build

# Install dependencies for translation
install-deps:
	pip3 install -r requirements.txt

# Auto translate Chinese posts to English (requires Gemini API key)
translate:
	python3 .github/auto_translate.py


checkpoint:
	@git add -A
	@git commit -m "checkpoint at $$(date '+%Y-%m-%dT%H:%M:%S%z')"
	@git push
	@echo Checkpoint created and pushed to remote

.PHONY: default dev build install-deps translate checkpoint
