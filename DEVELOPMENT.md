# Development Installation Guide

This guide ensures a reliable development setup for prompt-contracts.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/philippmelikidis/prompt-contracts.git
cd prompt-contracts

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .

# Verify installation
prompt-contracts --version
```

## Troubleshooting

If you encounter `ModuleNotFoundError: No module named 'promptcontracts'`:

### Method 1: Clean Reinstall
```bash
pip uninstall prompt-contracts -y
pip install -e . --force-reinstall
```

### Method 2: Use Requirements
```bash
pip install -r requirements.txt
pip install -e .
```

### Method 3: Manual PYTHONPATH (Last Resort)
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pip install -e .
```

## Project Structure

The project uses a standard Python package layout (not src-layout):

```
prompt-contracts/
├── promptcontracts/          # Main package
├── tests/                    # Test suite
├── examples/                 # Example contracts
├── pyproject.toml           # Package configuration
├── setup.py                 # Fallback setup
└── requirements.txt         # Dependencies
```

## Why This Layout?

We switched from `src/` layout to standard layout to ensure:
- ✅ Reliable editable installs across Python versions
- ✅ Consistent behavior across different environments
- ✅ Better compatibility with various tools and IDEs
- ✅ Simpler debugging and development workflow

## Testing

```bash
# Run all tests
make test

# Run specific test
pytest tests/test_checks.py -v
```

## CLI Usage

```bash
# Validate artifacts
prompt-contracts validate pd examples/support_ticket/pd.json

# Run contract
prompt-contracts run \
  --pd examples/support_ticket/pd.json \
  --es examples/support_ticket/es.json \
  --ep examples/support_ticket/ep.json \
  --report cli
```
