SCRIPT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

SHELL = /bin/bash

# highlight the Makefile targets
# @grep -E '^[a-zA-Z0-9_\-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: help
.DEFAULT_GOAL=help
help:  ## help for this Makefile
	@grep -E '^[a-zA-Z0-9_\-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

PROJECT := semantic-kernel-sample
VENV := ~/.cache/venv/$(PROJECT)
UV_RUN := UV_PROJECT_ENVIRONMENT=$(VENV) uv run

EXECUTABLES = isort ruff black

.PHONY: check_tools
check_tools:= $(foreach exec,$(EXECUTABLES),\
        $(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

.PHONY: fix
fix:  ## run isort and ruff on python code
	isort --float-to-top .
	ruff check --fix .
	black -l 79 .

.PHONY: aider
aider:  ## run aider
	$(UV_RUN) aider --model deepseek

.PHONY: env-up
env-up:
	UV_PROJECT_ENVIRONMENT=$(VENV) uv sync

.PHONY: env-rm
env-rm:
	rm -rf $(VENV)

.PHONY: clean
clean: env-rm  ## remove temporary files
	rm -f poetry.lock
	find . -name '.pytest_cache' -type d -exec rm -rf '{}' +
	find . -name '.ruff_cache' -type d -exec rm -rf '{}' +
	find . -name '__pycache__' -type d -exec rm -rf '{}' +
	find . -name '__pycache__' -type d -exec rm -rf '{}' +

.PHONY: nvim
nvim:  ## nvim
	$(UV_RUN) nvim -S Session.vim

.PHONY: hello
hello: env-up  ## run hello example
	$(UV_RUN) python hello.py


