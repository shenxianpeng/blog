default: dev

d:dev
dev:
	hugo serve

b:build
build:
	hugo build

.PHONY: default d dev b build

# Install dependencies for translation
install-deps:
	pip3 install -r requirements.txt

# Auto translate Chinese posts to English (requires Gemini API key)
translate:
	.github/auto_translate.py

# Translate the latest post only (requires Gemini API key)
translate-latest:
	.github/auto_translate.py

# Translate specific post (usage: make translate-post POST=content/posts/my-post/)
translate-post:
	.github/auto_translate.py

.PHONY: default dev build install-deps translate translate-latest translate-post
