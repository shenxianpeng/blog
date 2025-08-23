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
	python3 .github/auto_translate.py

.PHONY: default dev build install-deps translate
