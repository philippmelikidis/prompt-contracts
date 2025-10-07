# PCSL v0.1 – Prompt Contract Specification Language

**Version:** 0.1.0  
**Status:** Draft  
**Last Updated:** October 2025

---

## 1. Introduction

### 1.1 Goals

The **Prompt Contract Specification Language (PCSL)** aims to bring structured, repeatable testing to LLM prompt interactions. Similar to how OpenAPI defines REST API contracts or JSON Schema defines data contracts, PCSL defines:

- **What** a prompt expects as input
- **How** the LLM should respond (structure, semantics, performance)
- **Where** these expectations should hold (which models, providers, parameters)

### 1.2 Scope

PCSL v0.1 covers:
- Text-based prompts with structured (JSON) or unstructured responses
- Structural validation (JSON validity, required fields)
- Semantic validation (enum values, regex patterns, JSONPath assertions)
- Performance budgets (token limits, latency)
- Differential testing (comparing models/versions with tolerance thresholds)

Out of scope for v0.1:
- Multi-modal prompts (images, audio)
- Fine-tuning contract integration
- Production monitoring/alerting

---

## 2. Core Concepts

### 2.1 Artefacts

PCSL defines three primary artefact types:

#### 2.1.1 Prompt Definition (PD)
Describes the canonical prompt, I/O channel, and metadata.

**Required fields:**
- `pcsl` (string): Semantic version of PCSL (e.g., `"0.1.0"`)
- `id` (string): Unique identifier for this prompt
- `io` (object):
  - `channel` (enum): `"text"` (future: `"multimodal"`)
  - `expects` (enum): `"structured/json"`, `"unstructured/text"`
- `prompt` (string): The canonical prompt template

**Optional fields:**
- `metadata`: author, description, tags, etc.

#### 2.1.2 Expectation Suite (ES)
Declares checks (properties) that must hold for responses.

**Required fields:**
- `pcsl` (string): Version
- `checks` (array): List of check objects

Each check has:
- `type` (string): Qualified check name (e.g., `pc.check.json_valid`)
- Additional parameters specific to the check type

#### 2.1.3 Evaluation Profile (EP)
Defines execution context: which models to test, with what inputs, and acceptable tolerances.

**Required fields:**
- `pcsl` (string): Version
- `targets` (array): Model/provider configurations
- `fixtures` (array): Test inputs

Each target:
- `type` (string): `"openai"`, `"ollama"`, etc.
- `model` (string): Model identifier
- `params` (object): Provider-specific parameters (temperature, max_tokens, etc.)

Each fixture:
- `id` (string): Fixture identifier
- `input` (string): Input text to append/inject into prompt

**Optional fields:**
- `tolerances` (object): Map check types to `{ "max_fail_rate": number }` (0.0 = 0%, 1.0 = 100%)

---

## 3. Conformance Levels

PCSL defines progressive conformance levels:

### L1 – Structural Conformance
- JSON validity (`pc.check.json_valid`)
- Required field presence (`pc.check.json_required`)
- Token budget checks (`pc.check.token_budget`)

### L2 – Semantic Conformance
Includes L1 plus:
- Enum value validation (`pc.check.enum`)
- Regex pattern assertions (`pc.check.regex_absent`, `pc.check.regex_present`)
- JSONPath-based field checks

### L3 – Differential Conformance
Includes L2 plus:
- Multi-target execution with tolerance enforcement
- Pass-rate comparison across models/versions
- Latency budget validation (`pc.check.latency_budget`)

### L4 – Security Conformance (Planned)
Includes L3 plus:
- Jailbreak escape-rate metrics
- PII leakage detection
- Adversarial robustness checks

---

## 4. Built-in Check Types

### 4.1 `pc.check.json_valid`
Validates that the response is parseable JSON.

**Parameters:** None

**Example:**
```json
{ "type": "pc.check.json_valid" }
```

### 4.2 `pc.check.json_required`
Validates presence of required fields at the root level.

**Parameters:**
- `fields` (array of strings): Required field names

**Example:**
```json
{ "type": "pc.check.json_required", "fields": ["category", "priority"] }
```

### 4.3 `pc.check.enum`
Validates that a field (selected via JSONPath) has a value from an allowed set.

**Parameters:**
- `field` (string): JSONPath expression
- `allowed` (array): Allowed values

**Example:**
```json
{ "type": "pc.check.enum", "field": "$.priority", "allowed": ["low", "medium", "high"] }
```

### 4.4 `pc.check.regex_absent`
Fails if a regex pattern is found in the raw response.

**Parameters:**
- `pattern` (string): Regex pattern

**Example:**
```json
{ "type": "pc.check.regex_absent", "pattern": "```" }
```

### 4.5 `pc.check.token_budget`
Validates that the response does not exceed a token limit (approximated by word count in v0.1).

**Parameters:**
- `max_out` (integer): Maximum output tokens

**Example:**
```json
{ "type": "pc.check.token_budget", "max_out": 200 }
```

### 4.6 `pc.check.latency_budget`
Validates that the p95 latency across all fixtures stays within a threshold.

**Parameters:**
- `p95_ms` (integer): p95 latency in milliseconds

**Example:**
```json
{ "type": "pc.check.latency_budget", "p95_ms": 2000 }
```

---

## 5. Schema References

PCSL artefacts are validated using JSON Schema:

- **Prompt Definition:** `pcsl-pd.schema.json`
- **Expectation Suite:** `pcsl-es.schema.json`
- **Evaluation Profile:** `pcsl-ep.schema.json`

Each artefact SHOULD include a `$schema` field pointing to the canonical schema URL (or local file).

---

## 6. Versioning

PCSL follows Semantic Versioning (SemVer):
- **Patch** (0.1.x): Clarifications, non-breaking additions
- **Minor** (0.x.0): New check types, new fields (backward-compatible)
- **Major** (x.0.0): Breaking changes to artefact structure

The `pcsl` field in each artefact declares the spec version it targets.

---

## 7. Extensibility

Custom checks can be registered via the validator registry. Check types MUST use a namespaced identifier (e.g., `com.mycompany.check.custom_logic`).

---

## 8. Future Directions

- Multi-modal support (image, audio prompts)
- Advanced JSONPath/JSONLogic-based assertions
- Differential drift gates with statistical significance
- Integration with CI/CD (GitHub Actions, GitLab CI templates)
- Observability integration (OpenTelemetry export)

---

**End of PCSL v0.1 Specification**

