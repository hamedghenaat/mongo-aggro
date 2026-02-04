.PHONY: help install install-dev install-test install-all lint format test test-cov clean build publish docs docs-serve

PYTHON := python
UV := uv

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	$(UV) sync --no-dev

install-dev:  ## Install development dependencies
	$(UV) sync --extra dev

install-test:  ## Install test dependencies
	$(UV) sync --extra test

install-all:  ## Install all dependencies (dev + test + docs)
	$(UV) sync --extra dev --extra test --extra docs

lint:  ## Run all linters
	$(UV) run ruff check .
	$(UV) run mypy mongo_aggro

format:  ## Format code with black and isort
	$(UV) run black .
	$(UV) run isort .
	$(UV) run ruff check --fix .

test:  ## Run tests
	$(UV) run pytest

test-cov:  ## Run tests with coverage
	$(UV) run pytest --cov=mongo_aggro --cov-report=term-missing --cov-report=html

test-fast:  ## Run tests without coverage (faster)
	$(UV) run pytest -x -q

pre-commit:  ## Run pre-commit hooks on all files
	$(UV) run pre-commit run --all-files

pre-commit-install:  ## Install pre-commit hooks
	$(UV) run pre-commit install

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	$(UV) build

publish:  ## Publish to PyPI (usage: make publish REPO=pypi)
	$(UV) run twine upload --repository $(REPO) dist/*

publish-test:  ## Publish to TestPyPI
	$(UV) run twine upload --repository testpypi dist/*

check:  ## Run all checks (lint + test)
	$(MAKE) lint
	$(MAKE) test

ci:  ## Run CI pipeline (format check + lint + test)
	$(UV) run black --check .
	$(UV) run isort --check-only .
	$(MAKE) lint
	$(MAKE) test-cov

docs:  ## Build documentation
	$(UV) run mkdocs build

docs-serve:  ## Serve documentation locally
	$(UV) run mkdocs serve

docs-deploy:  ## Deploy documentation to GitHub Pages
	$(UV) run mkdocs gh-deploy --force
