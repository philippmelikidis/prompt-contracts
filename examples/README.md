# Prompt-Contracts Examples

This directory contains complete example contracts demonstrating various use cases and execution modes.

## 📁 Available Examples

### 1. Support Ticket Classification
**Directory:** [`support_ticket/`](./support_ticket/)
**Use Case:** Support request classification
**Execution Mode:** `assist`
**Provider:** Ollama (Mistral)

Classifies support tickets into categories with priority and reasoning.

**Files:**
- `pd.json` - Prompt Definition
- `es.json` - Expectation Suite (6 Checks)
- `ep.json` - Evaluation Profile (2 Fixtures)

**Run:**
```bash
prompt-contracts run \
  --pd examples/support_ticket/pd.json \
  --es examples/support_ticket/es.json \
  --ep examples/support_ticket/ep.json \
  --report cli
```

---

### 2. Email Classification
**Directory:** [`email_classification/`](./email_classification/)
**Use Case:** Email categorization with sentiment analysis
**Execution Modes:** All four modes (observe, assist, enforce, auto)
**Provider:** Ollama / OpenAI

Analyzes emails and classifies them by category, urgency, and sentiment.

**Files:**
- `pd.json` - Prompt Definition
- `es.json` - Expectation Suite (8 Checks)
- `ep_observe.json` - Observe Mode (validation only)
- `ep_assist.json` - Assist Mode (prompt augmentation)
- `ep_enforce.json` - Enforce Mode (schema-guided JSON, OpenAI)
- `ep_auto.json` - Auto Mode (adaptive)

**Run:**
```bash
# Observe Mode - Validation only
prompt-contracts run \
  --pd examples/email_classification/pd.json \
  --es examples/email_classification/es.json \
  --ep examples/email_classification/ep_observe.json

# Assist Mode - With prompt augmentation
prompt-contracts run \
  --pd examples/email_classification/pd.json \
  --es examples/email_classification/es.json \
  --ep examples/email_classification/ep_assist.json

# Enforce Mode - Schema-guided (requires OpenAI)
export OPENAI_API_KEY="sk-..."
prompt-contracts run \
  --pd examples/email_classification/pd.json \
  --es examples/email_classification/es.json \
  --ep examples/email_classification/ep_enforce.json

# Auto Mode - Adaptive
prompt-contracts run \
  --pd examples/email_classification/pd.json \
  --es examples/email_classification/es.json \
  --ep examples/email_classification/ep_auto.json
```

---

### 3. Product Recommendation
**Directory:** [`product_recommendation/`](./product_recommendation/)
**Use Case:** Personalized product recommendations
**Execution Mode:** `assist`
**Provider:** Ollama (Mistral)

Generates product recommendations based on user preferences.

**Files:**
- `pd.json` - Prompt Definition
- `es.json` - Expectation Suite (7 Checks)
- `ep.json` - Evaluation Profile (3 Fixtures)

**Run:**
```bash
prompt-contracts run \
  --pd examples/product_recommendation/pd.json \
  --es examples/product_recommendation/es.json \
  --ep examples/product_recommendation/ep.json \
  --save-io artifacts/product_recs/
```

---

### 4. Simple YAML Example
**Directory:** [`simple_yaml/`](./simple_yaml/)
**Use Case:** Minimal example in YAML format
**Format:** YAML

Simple example showing how YAML contracts can be used.

**Run:**
```bash
# YAML is automatically converted to JSON
prompt-contracts validate pd examples/simple_yaml/contract.yaml
```

---

## 🚀 Quick Start

### 1. Installation
```bash
pip install prompt-contracts
```

### 2. Setup Ollama (for local models)
```bash
# Install Ollama
brew install ollama

# Start Server
ollama serve

# Pull Mistral
ollama pull mistral
```

### 3. Run your first example
```bash
prompt-contracts run \
  --pd examples/support_ticket/pd.json \
  --es examples/support_ticket/es.json \
  --ep examples/support_ticket/ep.json \
  --report cli
```

---

## 📊 Execution Modes Comparison

| Example | observe | assist | enforce | auto |
|---------|---------|--------|---------|------|
| support_ticket | - | ✅ | - | - |
| email_classification | ✅ | ✅ | ✅ | ✅ |
| product_recommendation | - | ✅ | - | - |
| simple_yaml | - | - | - | - |

### Mode Properties

| Mode | Prompt Changes | Auto-Repair | Retry | Schema Enforcement |
|------|----------------|-------------|-------|-------------------|
| **observe** | ❌ None | ❌ No | ❌ No | ❌ No |
| **assist** | ✅ Constraints | ✅ Yes | ✅ Yes | ❌ No |
| **enforce** | ✅ Schema | ✅ Yes | ✅ Yes | ✅ Yes (if supported) |
| **auto** | 🔄 Adaptive | ✅ Yes | ✅ Yes | 🔄 When available |

---

## 🔧 Artifact Saving

Save all input/output artifacts for detailed analysis:

```bash
prompt-contracts run \
  --pd examples/email_classification/pd.json \
  --es examples/email_classification/es.json \
  --ep examples/email_classification/ep_assist.json \
  --save-io artifacts/ \
  --report json \
  --out results.json
```

**Artifact Structure:**
```
artifacts/
  <target-id>/
    <fixture-id>/
      input_final.txt      # Final prompt (with constraints if assist)
      output_raw.txt       # Raw model response
      output_norm.txt      # Normalized output (after auto-repair)
      run.json            # Complete execution metadata
```

---

## 📝 Creating Your Own Contract

### 1. Prompt Definition (pd.json)
```json
{
  "pcsl": "0.1.0",
  "id": "my.contract.v1",
  "io": {
    "channel": "text",
    "expects": "structured/json"
  },
  "prompt": "Your prompt here..."
}
```

### 2. Expectation Suite (es.json)
```json
{
  "pcsl": "0.1.0",
  "checks": [
    { "type": "pc.check.json_valid" },
    { "type": "pc.check.json_required", "fields": ["field1", "field2"] },
    { "type": "pc.check.enum", "field": "$.field1", "allowed": ["val1", "val2"] }
  ]
}
```

### 3. Evaluation Profile (ep.json)
```json
{
  "pcsl": "0.1.0",
  "targets": [
    { "type": "ollama", "model": "mistral", "params": { "temperature": 0 } }
  ],
  "fixtures": [
    { "id": "test1", "input": "Test input 1" },
    { "id": "test2", "input": "Test input 2" }
  ],
  "execution": {
    "mode": "assist",
    "max_retries": 1,
    "auto_repair": {
      "lowercase_fields": ["$.field1"],
      "strip_markdown_fences": true
    }
  }
}
```

---

## 📚 Additional Resources

- **Complete Documentation:** [README.md](../README.md)
- **Getting Started Guide:** [QUICKSTART.md](../QUICKSTART.md)
- **PCSL Specification:** [pcsl-v0.1.md](../src/promptcontracts/spec/pcsl-v0.1.md)
- **GitHub Repository:** https://github.com/philippmelikidis/prompt-contracts

---

## 🤝 Contributing

Have an interesting example? We welcome pull requests!

1. Fork the repository
2. Create your example in `examples/your-example/`
3. Add a description to this README
4. Open a pull request

---

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details
