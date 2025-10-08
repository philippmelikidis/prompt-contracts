# Tests

This directory contains the test suite for prompt-contracts.

## Running Tests

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=promptcontracts --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_loader.py -v
```

### Run tests by marker
```bash
# Run only integration tests (requires LLM)
pytest -m integration

# Skip integration tests
pytest -m "not integration"
```

## Test Organization

- `test_loader.py` - Artifact loading and schema validation
- `test_checks.py` - Built-in check implementations
- `test_enforcement.py` - Enforcement features (normalization, schema derivation)
- `test_normalization.py` - Output normalization utilities
- `test_runner_modes.py` - Execution mode negotiation and retry logic

## Test Markers

- `@pytest.mark.integration` - Tests that require an actual LLM (Ollama, OpenAI)
- `@pytest.mark.slow` - Tests that take significant time

## Coverage

Coverage reports are generated in `htmlcov/` directory. Open `htmlcov/index.html` in a browser to view.

Target: > 80% coverage for core modules.

