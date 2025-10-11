VENV_DIR ?= .venv

.PHONY: uv-installed
uv-installed:
	@command -v uv &> /dev/null ||\
		(echo "UV doesn't seem to be installed, try the following instructions:" &&\
		echo "https://docs.astral.sh/uv/getting-started/installation/" && false)

.PHONY: clean-caches
clean-caches: 
	rm -rf .pytest_cache

.PHONY: venv 
venv: uv-installed
	uv sync

.PHONY: clean
clean: clean-caches
	rm -rf ${VENV_DIR}

.PHONY: pytest
pytest: uv-installed venv
	uv run pytest tests -W error -vv

.PHONY: filecheck
filecheck: uv-installed
	uv run ruff check

.PHONY: format
format: uv-installed filecheck
	uv run ruff format 
