default: dev

d:dev
dev:
	hugo serve

b:build
build:
	hugo build

.PHONY: default d dev b build

# Install dependencies for translation
setup:
	pip3 install -r requirements.txt

# Auto translate Chinese posts to English (requires OpenAI API key)
translate:
	bin/auto-translate.py --all

# Translate the latest post only (requires OpenAI API key)
translate-latest:
	bin/auto-translate.py --latest

# Translate specific post (usage: make translate-post POST=content/posts/my-post/)
translate-post:
	bin/auto-translate.py $(POST)

.PHONY: default dev build setup translate translate-latest translate-post
