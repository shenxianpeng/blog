SHELL := bash # we want bash behaviour in all shell invocations

# https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
BOLD := \033[1m
NORMAL := \033[0m
GREEN := \033[1;32m

HELP_TARGET_DEPTH ?= \#
.PHONY: help
help: # Help
	@printf "\nThis is a list of all the make targets that you can run, e.g. $(BOLD)make server$(NORMAL)\n\n"
	@awk -F':+ |$(HELP_TARGET_DEPTH)' '/^[0-9a-zA-Z._%-]+:+.+$(HELP_TARGET_DEPTH).+$$/ { printf "$(GREEN)%-20s\033[0m %s\n", $$1, $$3 }' $(MAKEFILE_LIST) | sort
	@echo

deps: # Install dependencies
	npm install
	npm install -g hexo-cli

clean: # Remove generated files and cache
	@hexo clean

generate: # Generate static files
	@hexo generate

server: # Start the deamon server with default port 4000
	@hexo server

test-server: generate # Start the server with new port 4001
	@hexo server --port 4001 > /dev/null 2>&1 &

test: # Test hexo server with port 4001
	@curl -Is http://localhost:4001/ | head -n 1

package: # Copy files for packaing
	@echo "== copy new README.md"
	@cp source/README.md public/
	@ls public/README.md

	@echo "== copy new LICENSE"
	@cp source/LICENSE public/
	@ls public/LICENSE

	@echo "== copy new workflow yml"
	@mkdir -p public/.github/workflows/
	@cp -r source/.github/workflows/*.yml public/.github/workflows/
	@ls public/.github/workflows/*.yml

deploy: # Deploy your website
	@hexo deploy

release: clean generate new-server test package deploy # Release blog manully
	@echo "== Release ✅ Succeeded."
