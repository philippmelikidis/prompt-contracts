.PHONY: help install dev-install test lint format clean build publish

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install package
	pip install -e .

dev-install:  ## Install package with dev dependencies
	pip install -e ".[dev]"
	pre-commit install

test:  ## Run tests
	pytest -v

test-cov:  ## Run tests with coverage
	pytest --cov=promptcontracts --cov-report=html --cov-report=term

lint:  ## Run linters
	ruff check src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/

format:  ## Format code
	black src/ tests/
	isort src/ tests/
	ruff check --fix src/ tests/

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	python -m build

publish-test:  ## Publish to TestPyPI
	twine upload --repository testpypi dist/*

publish:  ## Publish to PyPI (use with caution!)
	twine upload dist/*

validate-examples:  ## Validate example artifacts
	prompt-contracts validate pd examples/support_ticket/pd.json
	prompt-contracts validate es examples/support_ticket/es.json
	prompt-contracts validate ep examples/support_ticket/ep.json

run-example:  ## Run example contract
	prompt-contracts run \
		--pd examples/support_ticket/pd.json \
		--es examples/support_ticket/es.json \
		--ep examples/support_ticket/ep.json \
		--report cli

pre-commit:  ## Run pre-commit hooks on all files
	pre-commit run --all-files

release-check:  ## Run all release checks (tests, lint, build, validate)
	@echo "🚀 Running release checks for v0.2.0..."
	@echo ""
	@echo "1️⃣  Running tests..."
	@pytest -v --tb=short
	@echo ""
	@echo "2️⃣  Validating examples..."
	@prompt-contracts validate pd examples/support_ticket/pd.json
	@prompt-contracts validate es examples/support_ticket/es.json
	@prompt-contracts validate ep examples/support_ticket/ep.json
	@echo ""
	@echo "3️⃣  Building package..."
	@python -m build
	@echo ""
	@echo "4️⃣  Checking package..."
	@twine check dist/*
	@echo ""
	@echo "✅ All checks passed! Ready to release."
