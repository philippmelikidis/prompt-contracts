.PHONY: help install dev-install setup test lint format clean build publish eval-small eval-full docker-build docker-run

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup:  ## Set up development environment (v0.3.0)
	pip install -e .
	pip install -r requirements.txt
	pip install sentence-transformers numpy  # Optional v0.3.0 deps

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
	prompt-contracts validate pd examples/extraction/pd.json
	prompt-contracts validate es examples/extraction/es.json
	prompt-contracts validate ep examples/extraction/ep.json

run-example:  ## Run example contract
	prompt-contracts run \
		--pd examples/support_ticket/pd.json \
		--es examples/support_ticket/es.json \
		--ep examples/support_ticket/ep.json \
		--report cli

eval-small:  ## Run small evaluation suite (v0.3.0)
	@echo "Running small evaluation suite..."
	prompt-contracts run \
		--pd examples/extraction/pd.json \
		--es examples/extraction/es.json \
		--ep examples/extraction/ep.json \
		--n 2 --seed 42 \
		--save-io artifacts/eval-small \
		--report json --out results-small.json

eval-full:  ## Run full evaluation suite across all 5 tasks (v0.3.1)
	@echo "Running full evaluation suite with N=10 sampling, seed=42"
	@echo "=================================================="
	@echo "Task 1/5: Classification"
	@mkdir -p artifacts/eval-full/classification
	prompt-contracts run \
		--pd examples/email_classification/pd.json \
		--es examples/email_classification/es.json \
		--ep examples/email_classification/ep.json \
		--n 10 --seed 42 --temperature 0.0 \
		--save-io artifacts/eval-full/classification \
		--report json --out artifacts/eval-full/classification/results.json
	@echo ""
	@echo "Task 2/5: Extraction"
	@mkdir -p artifacts/eval-full/extraction
	prompt-contracts run \
		--pd examples/extraction/pd.json \
		--es examples/extraction/es.json \
		--ep examples/extraction/ep.json \
		--n 10 --seed 42 --temperature 0.0 \
		--save-io artifacts/eval-full/extraction \
		--report json --out artifacts/eval-full/extraction/results.json
	@echo ""
	@echo "Task 3/5: Summarization"
	@mkdir -p artifacts/eval-full/summarization
	prompt-contracts run \
		--pd examples/summarization/pd.json \
		--es examples/summarization/es.json \
		--ep examples/summarization/ep.json \
		--n 10 --seed 42 --temperature 0.3 \
		--save-io artifacts/eval-full/summarization \
		--report json --out artifacts/eval-full/summarization/results.json
	@echo ""
	@echo "Task 4/5: Product Recommendation"
	@mkdir -p artifacts/eval-full/product_recommendation
	prompt-contracts run \
		--pd examples/product_recommendation/pd.json \
		--es examples/product_recommendation/es.json \
		--ep examples/product_recommendation/ep.json \
		--n 10 --seed 42 --temperature 0.0 \
		--save-io artifacts/eval-full/product_recommendation \
		--report json --out artifacts/eval-full/product_recommendation/results.json
	@echo ""
	@echo "Task 5/5: Support Ticket"
	@mkdir -p artifacts/eval-full/support_ticket
	prompt-contracts run \
		--pd examples/support_ticket/pd.json \
		--es examples/support_ticket/es.json \
		--ep examples/support_ticket/ep.json \
		--n 10 --seed 42 --temperature 0.0 \
		--save-io artifacts/eval-full/support_ticket \
		--report json --out artifacts/eval-full/support_ticket/results.json
	@echo ""
	@echo "=================================================="
	@echo "✓ Full evaluation complete. Results in artifacts/eval-full/"

docker-build:  ## Build Docker image (v0.3.1)
	docker build -t prompt-contracts:0.3.1 -t prompt-contracts:latest .

docker-run:  ## Run Docker container interactively
	docker run -it --rm \
		-v $(PWD)/examples:/workspace/examples \
		-v $(PWD)/fixtures:/workspace/fixtures \
		-v $(PWD)/artifacts:/workspace/artifacts \
		-e OPENAI_API_KEY=${OPENAI_API_KEY} \
		prompt-contracts:0.3.1 /bin/bash

docker-eval-full:  ## Run full evaluation inside Docker (reproducible)
	docker run --rm \
		-v $(PWD)/artifacts:/workspace/artifacts \
		-e OPENAI_API_KEY=${OPENAI_API_KEY} \
		-e PYTHONHASHSEED=42 \
		prompt-contracts:0.3.1 make eval-full

pre-commit:  ## Run pre-commit hooks on all files
	pre-commit run --all-files

release-check:  ## Run all release checks (tests, lint, build, validate)
	@echo "Running release checks for v0.3.1..."
	@echo ""
	@echo "1️⃣  Running tests..."
	@pytest -v --tb=short
	@echo ""
	@echo "2️⃣  Validating examples..."
	@prompt-contracts validate pd examples/support_ticket/pd.json
	@prompt-contracts validate es examples/support_ticket/es.json
	@prompt-contracts validate ep examples/support_ticket/ep.json
	@prompt-contracts validate pd examples/extraction/pd.json
	@prompt-contracts validate es examples/extraction/es.json
	@prompt-contracts validate ep examples/extraction/ep.json
	@echo ""
	@echo "3️⃣  Building package..."
	@python -m build
	@echo ""
	@echo "4️⃣  Checking package..."
	@twine check dist/*
	@echo ""
	@echo "✅ All checks passed! Ready to release."
