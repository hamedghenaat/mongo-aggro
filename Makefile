.PHONY: help install install-dev install-test install-all lint format test test-cov clean build publish docs docs-serve

PYTHON := python
POETRY := poetry

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	$(POETRY) install --only main

install-dev:  ## Install development dependencies
	$(POETRY) install --with dev

install-test:  ## Install test dependencies
	$(POETRY) install --with test

install-all:  ## Install all dependencies (dev + test + docs)
	$(POETRY) install --with dev,test,docs

lint:  ## Run all linters
	$(POETRY) run ruff check .
	$(POETRY) run mypy mongo_aggro

format:  ## Format code with black and isort
	$(POETRY) run black .
	$(POETRY) run isort .
	$(POETRY) run ruff check --fix .

test:  ## Run tests
	$(POETRY) run pytest

test-cov:  ## Run tests with coverage
	$(POETRY) run pytest --cov=mongo_aggro --cov-report=term-missing --cov-report=html

test-fast:  ## Run tests without coverage (faster)
	$(POETRY) run pytest -x -q

pre-commit:  ## Run pre-commit hooks on all files
	$(POETRY) run pre-commit run --all-files

pre-commit-install:  ## Install pre-commit hooks
	$(POETRY) run pre-commit install

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
	$(POETRY) build

publish:  ## Publish to PyPI (requires authentication)
	$(POETRY) publish

publish-test:  ## Publish to TestPyPI
	$(POETRY) publish -r testpypi

check:  ## Run all checks (lint + test)
	$(MAKE) lint
	$(MAKE) test

ci:  ## Run CI pipeline (format check + lint + test)
	$(POETRY) run black --check .
	$(POETRY) run isort --check-only .
	$(MAKE) lint
	$(MAKE) test-cov

docs:  ## Build documentation
	$(POETRY) run mkdocs build

docs-serve:  ## Serve documentation locally
	$(POETRY) run mkdocs serve

docs-deploy:  ## Deploy documentation to GitHub Pages
	$(POETRY) run mkdocs gh-deploy --force
