# 📜 prompt-contracts

**Test your LLM prompts like code.**  
Prompt-Contracts is a specification and toolkit that brings **contract testing** to LLM prompts.  
When models drift (provider updates, parameter changes, switch to local models), your integration can silently break:
- JSON becomes invalid or wrapped in Markdown
- Required fields go missing
- Enum values drift ("urgent" instead of `high`)
- Latency and token budgets regress

**Prompt-Contracts** lets you define a **Prompt Definition (PD)**, an **Expectation Suite (ES)** and an **Evaluation Profile (EP)**.  
A runner executes these contracts across targets (OpenAI, Ollama, etc.), validates structural & semantic properties, and reports regressions.

---

## ✨ What's inside (v0.1 MVP)

- **PCSL (Prompt Contract Specification Language)** — early spec + JSON Schemas
- **Conformance levels**
  - **L1 Structural**: JSON validity, required fields, budgets
  - **L2 Semantic**: enums, JSONPath assertions, regex absence
  - **L3 Differential** (scaffold): cross-target pass-rate & drift tolerance
- **Runner & Adapters**: OpenAI, Ollama
- **Reports**: CLI, JSON, JUnit (for CI)
- **Examples**: JSON-first contracts (YAML supported for convenience)

> Goal: become the **OpenAPI/JUnit** of LLM prompt stability.

---

## 🚀 Quickstart

### 1) Install

```bash
# from source
pip install -e .
# or with requirements
pip install -r requirements.txt
```

### 2) Pull a local model (optional but recommended)

Using Ollama on macOS:

```bash
brew install ollama
ollama serve
ollama pull mistral
```

### 3) Run the example

```bash
prompt-contracts run \
  --pd examples/support_ticket/pd.json \
  --es examples/support_ticket/es.json \
  --ep examples/support_ticket/ep.json \
  --report cli
```

Expected CLI output (illustrative):

```
TARGET ollama: mistral
  [PASS] json_valid
  [PASS] json_required (category, priority, reason)
  [PASS] enum ($.priority in [low, medium, high])
  [PASS] regex_absent (no ``` found)
  [PASS] token_budget (<= 200)
  [PASS] latency_budget (p95 <= 5000ms)
Summary: 6/6 checks passed (fixtures: 2) — status: GREEN
```

---

## 🧩 Concepts

### Prompt Definition (PD)

Describes the I/O channel and the canonical prompt content.

```json
{
  "pcsl": "0.1.0",
  "id": "support.ticket.classify.v1",
  "io": { "channel": "text", "expects": "structured/json" },
  "prompt": "You are a support classifier. Reply ONLY with strict JSON with fields {category, priority, reason}."
}
```

### Expectation Suite (ES)

Declares checks as **properties** you expect to hold for **every** run.

```json
{
  "pcsl": "0.1.0",
  "checks": [
    { "type": "pc.check.json_valid" },
    { "type": "pc.check.json_required", "fields": ["category", "priority", "reason"] },
    { "type": "pc.check.enum", "field": "$.priority", "allowed": ["low", "medium", "high"] },
    { "type": "pc.check.regex_absent", "pattern": "```" },
    { "type": "pc.check.token_budget", "max_out": 200 },
    { "type": "pc.check.latency_budget", "p95_ms": 5000 }
  ]
}
```

### Evaluation Profile (EP)

Defines **targets** (models/providers), **fixtures** (inputs), and **tolerances** (acceptable failure rates).

```json
{
  "pcsl": "0.1.0",
  "targets": [
    { "type": "ollama", "model": "mistral", "params": { "temperature": 0 } }
  ],
  "fixtures": [
    { "id": "pwd_reset", "input": "User: My password doesn't work." },
    { "id": "billing", "input": "User: I was double charged last month." }
  ],
  "tolerances": {
    "pc.check.json_valid": { "max_fail_rate": 0.0 },
    "pc.check.enum": { "max_fail_rate": 0.01 }
  }
}
```

---

## 🧪 CLI

```bash
# Validate artefacts against PCSL schemas
prompt-contracts validate pd examples/support_ticket/pd.json
prompt-contracts validate es examples/support_ticket/es.json
prompt-contracts validate ep examples/support_ticket/ep.json

# Run a full contract
prompt-contracts run \
  --pd <path> --es <path> --ep <path> \
  [--report cli|json|junit] [--out outpath]
```

---

## 🔌 Adapters

* **OpenAI**: uses `openai` SDK (`model`, `temperature`, etc.)
* **Ollama**: uses `POST /api/generate` (`model`, optional params)
* Implement your own by subclassing `adapters.base.AbstractAdapter`.

---

## ✅ Checks (built-in)

* `pc.check.json_valid`
* `pc.check.json_required` (`fields: [...]`)
* `pc.check.enum` (`field: "$.path"`, `allowed: [...]`)
* `pc.check.regex_absent` (`pattern: "```"`)
* `pc.check.token_budget` (`max_out: 200`) — MVP approximation by word count
* `pc.check.latency_budget` (`p95_ms: 5000`) — computed across runs

> Roadmap: JSON Schema-based field validation, numeric ranges, cross-field deps, differential drift gates.

---

## 🧱 Conformance Levels

* **L1 – Structural**: `json_valid`, `json_required`, budget checks
* **L2 – Semantic**: `enum`, regex absence, JSONPath assertions
* **L3 – Differential**: compare pass-rates/latency across models or versions, enforce tolerances

A runner or artefact can declare the highest level it satisfies; we plan **badges** (e.g., `PCSL L2 Conformant`).

---

## 🏗️ Project Layout

```
src/promptcontracts/
  cli.py            # CLI entrypoints
  core/
    loader.py       # JSON/YAML load + schema validate
    validator.py    # check registry + execution
    runner.py       # orchestration + aggregation
    reporters/      # cli/json/junit outputs
    adapters/       # openai/ollama
    checks/         # built-in check implementations
  spec/             # PCSL draft + JSON Schemas
examples/           # ready-to-run contracts
tests/              # minimal test coverage
```

---

## 📦 Install & Dev

`requirements.txt` (core deps):

```
pyyaml
jsonschema
jsonpath-ng
openai
httpx
rich
numpy
```

Dev:

```bash
pip install -e .
pytest -q
```

---

## 🗺️ Roadmap

* L3 Differential runner (multi-target drifts, pass-rate gates)
* HTML report with diffs & trend charts
* JSON Schema field-level checks
* L4 Security profile: jailbreak escape-rate as a first-class metric
* Registry for check types & metrics
* GitHub Action / GitLab CI templates

---

## 🤝 Contributing / Spec Governance

* Spec lives under `/src/promptcontracts/spec/`
* Use GitHub Issues as **RFCs** for changes to PCSL (fields, checks, levels)
* We target semantic versioning for the spec (`pcsl: "0.1.0"` → `0.2.0`, …)

---

## ⚖️ License

MIT (code), Documentation under CC-BY 4.0.

