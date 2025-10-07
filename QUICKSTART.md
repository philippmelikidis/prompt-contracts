# Quick Start Guide

Get up and running with prompt-contracts in 5 minutes.

## Prerequisites

- Python 3.10 or higher
- Ollama installed (for local models) OR OpenAI API key

## Installation

### 1. Install Dependencies

```bash
cd /Users/PhilipposMelikidis/Desktop/prompt-contracts
pip install -r requirements.txt
```

### 2. Install the Package

```bash
pip install -e .
```

This makes the `prompt-contracts` command available globally.

### 3. Setup Ollama (Optional but Recommended)

```bash
# Install Ollama (macOS)
brew install ollama

# Start Ollama server (in a separate terminal)
ollama serve

# Pull a model
ollama pull mistral
```

## Running Your First Contract

### Validate the Example Contracts

```bash
# Validate each artefact
prompt-contracts validate pd examples/support_ticket/pd.json
prompt-contracts validate es examples/support_ticket/es.json
prompt-contracts validate ep examples/support_ticket/ep.json
```

Expected output:
```
✓ Valid Prompt Definition: examples/support_ticket/pd.json
  PCSL version: 0.1.0
  ID: support.ticket.classify.v1
```

### Run the Contract

```bash
prompt-contracts run \
  --pd examples/support_ticket/pd.json \
  --es examples/support_ticket/es.json \
  --ep examples/support_ticket/ep.json \
  --report cli
```

This will:
1. Load the prompt definition
2. Run 2 test fixtures through Mistral
3. Validate each response against 6 checks
4. Display a pretty CLI report

## Using OpenAI Instead

Edit `examples/support_ticket/ep.json` and change the target:

```json
{
  "targets": [
    {
      "type": "openai",
      "model": "gpt-4o-mini",
      "params": {
        "temperature": 0
      }
    }
  ],
  ...
}
```

Set your API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Creating Your Own Contract

### 1. Create a Prompt Definition (pd.json)

```json
{
  "pcsl": "0.1.0",
  "id": "my.custom.prompt",
  "io": {
    "channel": "text",
    "expects": "structured/json"
  },
  "prompt": "Your prompt here..."
}
```

### 2. Create an Expectation Suite (es.json)

```json
{
  "pcsl": "0.1.0",
  "checks": [
    { "type": "pc.check.json_valid" },
    { "type": "pc.check.json_required", "fields": ["field1", "field2"] }
  ]
}
```

### 3. Create an Evaluation Profile (ep.json)

```json
{
  "pcsl": "0.1.0",
  "targets": [
    { "type": "ollama", "model": "mistral", "params": {} }
  ],
  "fixtures": [
    { "id": "test1", "input": "Test input 1" }
  ]
}
```

### 4. Run It

```bash
prompt-contracts run --pd pd.json --es es.json --ep ep.json --report cli
```

## Running Tests

```bash
# From the project root
pytest tests/ -v
```

## Troubleshooting

### "Module not found: promptcontracts"

Make sure you ran `pip install -e .` from the project root.

### "Connection refused" with Ollama

Make sure Ollama is running: `ollama serve`

### "Model not found"

Pull the model first: `ollama pull mistral`

## Next Steps

- Read the full spec: `src/promptcontracts/spec/pcsl-v0.1.md`
- Explore check types in `src/promptcontracts/core/checks/`
- Try different report formats: `--report json` or `--report junit`
- Add your own custom checks by extending the validator registry

## Getting Help

- Check the README for detailed documentation
- Review the example contracts in `examples/`
- Read the PCSL spec for advanced features

