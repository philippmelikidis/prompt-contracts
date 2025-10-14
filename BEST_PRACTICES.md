# Best Practices Guide

A comprehensive guide to building robust, maintainable, and production-ready prompt contracts.

---

## Table of Contents

- [Contract Design Principles](#contract-design-principles)
- [Execution Mode Selection](#execution-mode-selection)
- [Writing Effective Prompts](#writing-effective-prompts)
- [Designing Expectation Suites](#designing-expectation-suites)
- [Fixture Strategy](#fixture-strategy)
- [Auto-Repair Configuration](#auto-repair-configuration)
- [Tolerance Tuning](#tolerance-tuning)
- [Production Deployment](#production-deployment)
- [Testing & CI/CD](#testing--cicd)
- [Monitoring & Observability](#monitoring--observability)
- [Common Pitfalls](#common-pitfalls)
- [Real-World Examples](#real-world-examples)

---

## Contract Design Principles

### 1. Single Responsibility
Each contract should validate **one specific capability** of your LLM system.

**❌ Bad: Mixed responsibilities**
```json
{
  "id": "general.assistant.v1",
  "prompt": "You can classify text, translate languages, and answer questions..."
}
```

**✅ Good: Focused contract**
```json
{
  "id": "support.ticket.classifier.v1",
  "prompt": "You are a support ticket classifier. Categorize tickets by type and priority."
}
```

### 2. Version Your Contracts
Always include version in contract IDs for tracking changes.

```json
{
  "id": "email.classifier.v2",  // Changed from v1
  "prompt": "Enhanced email classifier with sentiment analysis..."
}
```

### 3. Explicit Over Implicit
Be explicit about expected structure and constraints in prompts.

**❌ Bad: Vague expectations**
```
Classify this email.
```

**✅ Good: Clear structure**
```
Classify this email into one of: spam, personal, business.
Reply with JSON containing: category, confidence, reason.
```

### 4. Fail Fast, Fail Clearly
Design checks that fail quickly with clear error messages.

```json
{
  "checks": [
    { "type": "pc.check.json_valid" },  // Fail fast if not JSON
    { "type": "pc.check.json_required", "fields": ["category"] },  // Then check structure
    { "type": "pc.check.enum", "field": "$.category", "allowed": ["spam", "personal", "business"] }
  ]
}
```

---

## Execution Mode Selection

### Decision Matrix

| Scenario | Mode | Why |
|----------|------|-----|
| **OpenAI Production** | `enforce` | Native schema support guarantees structure |
| **Ollama/Local Models** | `assist` | No schema enforcement, need prompt augmentation |
| **Multi-Provider** | `auto` | Adapts to each provider's capabilities |
| **A/B Testing** | `observe` | No modifications, pure measurement |
| **Development** | `assist` | Good debugging with visible constraints |
| **Critical Systems** | `enforce` with `strict_enforce: true` | Fail explicitly if enforcement unavailable |

### Mode-Specific Best Practices

#### observe Mode
```json
{
  "execution": {
    "mode": "observe",
    "max_retries": 0  // No retries in observe mode
  },
  "tolerances": {
    "pc.check.enum": { "max_fail_rate": 0.05 }  // Allow 5% drift for monitoring
  }
}
```

**Use for:**
- Baseline measurements before optimization
- Monitoring production behavior
- Comparing model versions

#### assist Mode
```json
{
  "execution": {
    "mode": "assist",
    "max_retries": 2,
    "auto_repair": {
      "lowercase_fields": ["$.status", "$.priority"],
      "strip_markdown_fences": true
    }
  }
}
```

**Best practices:**
- Set `max_retries` between 1-3 (higher = more latency)
- Lowercase fields that are case-insensitive enums
- Always enable `strip_markdown_fences` for JSON outputs

#### enforce Mode
```json
{
  "execution": {
    "mode": "enforce",
    "max_retries": 1,  // Less retries needed with schema enforcement
    "strict_enforce": false  // or true for critical systems
  }
}
```

**Best practices:**
- Use with OpenAI for guaranteed structure
- Set `strict_enforce: true` for mission-critical systems
- Lower `max_retries` since enforcement reduces failures

#### auto Mode
```json
{
  "execution": {
    "mode": "auto",
    "max_retries": 2,
    "auto_repair": {
      "lowercase_fields": ["$.priority"],
      "strip_markdown_fences": true
    }
  }
}
```

**Best practices:**
- Default choice for most applications
- Configure auto-repair for worst-case (non-enforcing) providers
- Test with multiple providers to verify fallback behavior

---

## Writing Effective Prompts

### 1. Structure Your Prompts

**Template Structure:**
```
[Role Definition]
You are a [specific role].

[Task Description]
Your task is to [specific task].

[Input Format]
You will receive [input description].

[Output Format]
Respond with [exact output format].

[Constraints]
- Constraint 1
- Constraint 2

[Examples - Optional]
Example:
Input: ...
Output: ...
```

**Example:**
```json
{
  "prompt": "You are a customer support ticket classifier.\n\nYour task is to categorize incoming support tickets and assign priority levels.\n\nYou will receive a customer message describing their issue.\n\nRespond with valid JSON containing exactly these fields:\n- category: one of [technical, billing, feature_request, other]\n- priority: one of [low, medium, high, urgent]\n- reasoning: brief explanation (max 100 chars)\n\nDo NOT use markdown formatting or code fences."
}
```

### 2. Avoid Ambiguity

**❌ Bad: Ambiguous**
```
Classify the urgency of this ticket.
```

**✅ Good: Specific**
```
Classify urgency as one of: low, medium, high, urgent
- low: can wait weeks
- medium: can wait days
- high: needs attention within 24h
- urgent: immediate attention required
```

### 3. Include Format Examples in Critical Cases

```
Respond with JSON in this EXACT format:
{
  "category": "technical",
  "priority": "high",
  "reasoning": "Database connection error affecting users"
}
```

### 4. Test Prompt Robustness

Create fixtures that test edge cases:
```json
{
  "fixtures": [
    { "id": "happy_path", "input": "Normal input..." },
    { "id": "empty_input", "input": "" },
    { "id": "very_long_input", "input": "..." },  // 1000+ chars
    { "id": "special_chars", "input": "Input with émojis 🎉 and symbols @#$" },
    { "id": "multilingual", "input": "Mixed English and 中文 text" }
  ]
}
```

---

## Designing Expectation Suites

### 1. Layer Your Checks

Order checks from **structural → semantic → performance**:

```json
{
  "checks": [
    // Layer 1: Structural (L1)
    { "type": "pc.check.json_valid" },
    { "type": "pc.check.json_required", "fields": ["category", "priority"] },

    // Layer 2: Semantic (L2)
    { "type": "pc.check.enum", "field": "$.category", "allowed": ["tech", "billing"] },
    { "type": "pc.check.regex_absent", "pattern": "```" },

    // Layer 3: Performance (L3)
    { "type": "pc.check.token_budget", "max_out": 200 },
    { "type": "pc.check.latency_budget", "p95_ms": 3000 }
  ]
}
```

### 2. Be Strict Where It Matters

**Critical fields:** Zero tolerance
```json
{
  "type": "pc.check.enum",
  "field": "$.payment_status",
  "allowed": ["pending", "completed", "failed"]
}
```

**Tolerances:**
```json
{
  "tolerances": {
    "pc.check.enum": { "max_fail_rate": 0.0 }  // 0% tolerance for critical enums
  }
}
```

**Non-critical fields:** Allow some flexibility
```json
{
  "type": "pc.check.token_budget",
  "max_out": 500
}
```

```json
{
  "tolerances": {
    "pc.check.token_budget": { "max_fail_rate": 0.1 }  // 10% tolerance acceptable
  }
}
```

### 3. Use JSONPath Effectively

**Array validation:**
```json
{
  "type": "pc.check.enum",
  "field": "$.items[*].status",
  "allowed": ["available", "sold", "reserved"]
}
```

**Nested field validation:**
```json
{
  "type": "pc.check.json_required",
  "fields": ["user.id", "user.email", "transaction.amount"]
}
```

### 4. Regex for Pattern Matching

**Prevent markdown:**
```json
{
  "type": "pc.check.regex_absent",
  "pattern": "```"
}
```

**Prevent explanatory text:**
```json
{
  "type": "pc.check.regex_absent",
  "pattern": "(?i)(here is|as requested|i've analyzed)"
}
```

**Ensure specific format:**
```json
{
  "type": "pc.check.regex_present",
  "pattern": "^[A-Z]{3}-[0-9]{6}$",  // e.g., TKT-123456
  "field": "$.ticket_id"
}
```

---

## Fixture Strategy

### 1. Coverage-Based Fixtures

Create fixtures that cover:
- **Happy path** (expected normal inputs)
- **Edge cases** (empty, very long, special chars)
- **Error conditions** (malformed, unexpected)
- **Business logic** (domain-specific scenarios)

```json
{
  "fixtures": [
    // Happy path
    { "id": "normal_ticket", "input": "My app crashed when uploading files." },

    // Edge cases
    { "id": "minimal_input", "input": "Help" },
    { "id": "long_input", "input": "..." },  // 2000 chars

    // Error conditions
    { "id": "empty_input", "input": "" },
    { "id": "gibberish", "input": "asdkjfh alksjdhf alksdjf" },

    // Business logic
    { "id": "urgent_outage", "input": "URGENT: Production down!" },
    { "id": "billing_complaint", "input": "Charged twice for subscription" }
  ]
}
```

### 2. Representative Data

Use **real** or **realistic** data from your domain:

**❌ Bad: Generic fixtures**
```json
{ "id": "test1", "input": "test message" }
```

**✅ Good: Domain-specific**
```json
{ "id": "db_connection_error", "input": "Getting 'Connection refused' error when connecting to PostgreSQL database. Error code: 53300" }
```

### 3. Fixture Naming

Use descriptive IDs that explain the test case:

```json
{ "id": "urgent_customer_churn_risk", "input": "..." }
{ "id": "billing_double_charge_complaint", "input": "..." }
{ "id": "technical_api_timeout_issue", "input": "..." }
```

### 4. Incremental Fixture Growth

Start small, grow based on failures:

**v1: Basic coverage**
```json
{ "fixtures": [
  { "id": "basic_tech", "input": "..." },
  { "id": "basic_billing", "input": "..." }
]}
```

**v2: Add edge cases discovered**
```json
{ "fixtures": [
  { "id": "basic_tech", "input": "..." },
  { "id": "basic_billing", "input": "..." },
  { "id": "edge_empty", "input": "" },  // Added after empty input failures
  { "id": "edge_multilingual", "input": "..." }  // Added after non-English failures
]}
```

---

## Auto-Repair Configuration

### 1. Lowercase Fields Strategy

**Rule:** Lowercase any field used in case-insensitive enum checks

```json
{
  "checks": [
    {
      "type": "pc.check.enum",
      "field": "$.priority",
      "allowed": ["low", "medium", "high"]  // lowercase values
    }
  ]
}
```

```json
{
  "execution": {
    "auto_repair": {
      "lowercase_fields": ["$.priority"]  // matches enum check
    }
  }
}
```

### 2. Markdown Fence Stripping

**Always enable** when expecting JSON:

```json
{
  "auto_repair": {
    "strip_markdown_fences": true  // Handles: ```json\n{...}\n```
  }
}
```

### 3. Field-Specific Repair

**Pattern:** Repair only what's likely to fail

```json
{
  "auto_repair": {
    "lowercase_fields": [
      "$.status",      // enum check on status
      "$.category",    // enum check on category
      "$.priority"     // enum check on priority
    ],
    // Don't lowercase user-generated content
    "strip_markdown_fences": true
  }
}
```

### 4. Monitoring Repair Rates

Track repair frequency to improve prompts:

```bash
# Save artifacts to analyze repair patterns
prompt-contracts run \
  --pd pd.json --es es.json --ep ep.json \
  --save-io artifacts/ \
  --report json --out results.json

# Analyze repair patterns
jq '.targets[].fixtures[] | select(.status == "REPAIRED") | .repaired_details' results.json
```

**If repair rate > 30%:** Improve prompt clarity
**If repair rate > 50%:** Consider different execution mode

---

## Tolerance Tuning

### 1. Start Strict, Relax Gradually

**Initial tolerances (strict):**
```json
{
  "tolerances": {
    "pc.check.json_valid": { "max_fail_rate": 0.0 },
    "pc.check.enum": { "max_fail_rate": 0.0 },
    "pc.check.token_budget": { "max_fail_rate": 0.0 }
  }
}
```

**After testing, relax non-critical:**
```json
{
  "tolerances": {
    "pc.check.json_valid": { "max_fail_rate": 0.0 },     // Keep strict
    "pc.check.enum": { "max_fail_rate": 0.02 },          // Allow 2% drift
    "pc.check.token_budget": { "max_fail_rate": 0.1 }    // Allow 10% variance
  }
}
```

### 2. Critical vs Non-Critical Checks

**Critical (zero tolerance):**
- JSON validity
- Required fields for downstream systems
- Security/compliance enums (e.g., `is_approved`)

**Non-Critical (some tolerance):**
- Token budgets (performance)
- Optional fields
- Formatting preferences

### 3. Environment-Specific Tolerances

**Development:**
```json
{ "tolerances": { "pc.check.latency_budget": { "max_fail_rate": 0.5 } }}
```

**Staging:**
```json
{ "tolerances": { "pc.check.latency_budget": { "max_fail_rate": 0.2 } }}
```

**Production:**
```json
{ "tolerances": { "pc.check.latency_budget": { "max_fail_rate": 0.05 } }}
```

---

## Production Deployment

### 1. Pre-Production Checklist

- [ ] All fixtures pass with target execution mode
- [ ] Tested with production-like data volume
- [ ] Latency budgets validated under load
- [ ] Fallback behavior tested (for `auto`/`enforce` modes)
- [ ] Artifact saving configured for debugging
- [ ] Monitoring/alerting set up

### 2. Deployment Strategy

**Phase 1: Shadow Mode (observe)**
```json
{
  "execution": { "mode": "observe" },
  "tolerances": {
    "pc.check.enum": { "max_fail_rate": 1.0 }  // Allow all, just measure
  }
}
```

**Phase 2: Assisted Production (assist)**
```json
{
  "execution": { "mode": "assist", "max_retries": 2 }
}
```

**Phase 3: Enforced Production (enforce/auto)**
```json
{
  "execution": { "mode": "auto", "max_retries": 1 }
}
```

### 3. Multi-Environment Configuration

**Use environment variables for targets:**

```json
{
  "targets": [
    {
      "type": "openai",
      "model": "${OPENAI_MODEL:-gpt-4o-mini}",
      "params": {
        "temperature": "${TEMPERATURE:-0}"
      }
    }
  ]
}
```

**Separate EP files per environment:**
- `ep.dev.json` - Development settings
- `ep.staging.json` - Staging settings
- `ep.prod.json` - Production settings

### 4. Graceful Degradation

**Configure fallbacks:**

```json
{
  "targets": [
    { "type": "openai", "model": "gpt-4o" },
    { "type": "openai", "model": "gpt-3.5-turbo" },  // Fallback
    { "type": "ollama", "model": "mistral" }  // Local fallback
  ],
  "execution": { "mode": "auto" }
}
```

---

## Testing & CI/CD

### 1. Contract Testing in CI Pipeline

```yaml
# .github/workflows/contract-tests.yml
name: Contract Tests

on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install prompt-contracts

      - name: Validate contracts
        run: |
          prompt-contracts validate pd contracts/classifier/pd.json
          prompt-contracts validate es contracts/classifier/es.json
          prompt-contracts validate ep contracts/classifier/ep.json

      - name: Run contract tests
        run: |
          prompt-contracts run \
            --pd contracts/classifier/pd.json \
            --es contracts/classifier/es.json \
            --ep contracts/classifier/ep.ci.json \
            --report junit --out test-results.xml

      - name: Publish test results
        uses: EnricoMi/publish-unit-test-result-action@v2
        if: always()
        with:
          files: test-results.xml
```

### 2. Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: validate-contracts
        name: Validate PCSL contracts
        entry: prompt-contracts validate
        language: system
        files: \.(json|yaml)$
        pass_filenames: true
```

### 3. Regression Testing

**Save baseline results:**
```bash
prompt-contracts run \
  --pd pd.json --es es.json --ep ep.json \
  --report json --out baseline.json
```

**Compare against baseline:**
```bash
# In CI, fail if significant degradation
prompt-contracts run \
  --pd pd.json --es es.json --ep ep.json \
  --report json --out current.json

# Custom script to compare
python compare_results.py baseline.json current.json
```

---

## Monitoring & Observability

### 1. Key Metrics to Track

**Per Contract:**
- Pass rate (%)
- Repair rate (%)
- Failure rate (%)
- p50/p95/p99 latency
- Token usage

**Per Check:**
- Individual check pass rates
- Failure patterns
- Tolerance threshold proximity

### 2. Alerting Thresholds

```python
# Example: Alert on degradation
if pass_rate < 0.95:  # Below 95%
    alert("Contract degradation detected")

if repair_rate > 0.30:  # Above 30% repairs
    alert("High repair rate - review prompt")

if p95_latency > budget * 1.2:  # 20% over budget
    alert("Latency budget exceeded")
```

### 3. Artifact Analysis

**Save artifacts for debugging:**
```bash
prompt-contracts run \
  --save-io artifacts/$(date +%Y%m%d-%H%M%S) \
  ...
```

**Analyze failure patterns:**
```bash
# Find all failures
find artifacts/ -name "run.json" -exec jq 'select(.status == "FAIL")' {} \;

# Extract failed fixture IDs
find artifacts/ -name "run.json" -exec jq -r 'select(.status == "FAIL") | .fixture_id' {} \;
```

### 4. Dashboard Metrics

**Track over time:**
- Contract health (GREEN/YELLOW/RED counts)
- Repair rate trends
- Latency percentiles
- Cost metrics (tokens * rate)

---

## Common Pitfalls

### 1. ❌ Over-Reliance on Auto-Repair

**Problem:** High repair rates mask prompt quality issues

**Solution:** If repair rate > 30%, improve the prompt instead of relying on repairs

```json
// Bad: 60% repair rate
{ "execution": { "mode": "assist", "max_retries": 5 }}

// Good: Fix prompt to reduce repairs
{ "prompt": "Reply with ONLY valid JSON. Do NOT use markdown." }
```

### 2. ❌ Ignoring Latency Budgets

**Problem:** No latency checks until production

**Solution:** Set realistic budgets early

```json
{
  "checks": [
    { "type": "pc.check.latency_budget", "p95_ms": 2000 }  // Based on requirements
  ]
}
```

### 3. ❌ Too Few Fixtures

**Problem:** Contracts pass tests but fail in production

**Solution:** Minimum 5-10 fixtures covering edge cases

```json
{
  "fixtures": [
    { "id": "happy", "input": "..." },
    { "id": "edge_empty", "input": "" },
    { "id": "edge_long", "input": "..." },  // 1000+ chars
    { "id": "edge_special", "input": "@#$%^&*()" },
    { "id": "error_gibberish", "input": "asdfkjh" }
  ]
}
```

### 4. ❌ Vague Enum Values

**Problem:** Model outputs variations not in enum

**Solution:** Be exhaustive and explicit

```json
// Bad: Incomplete
{ "allowed": ["yes", "no"] }

// Good: Exhaustive
{ "allowed": ["yes", "no", "unknown", "not_applicable"] }
```

### 5. ❌ Not Testing Provider Fallbacks

**Problem:** `auto` mode behaves unexpectedly

**Solution:** Test with each target provider

```bash
# Test with OpenAI (will use enforce)
prompt-contracts run --pd pd.json --es es.json --ep ep.openai.json

# Test with Ollama (will use assist)
prompt-contracts run --pd pd.json --es es.json --ep ep.ollama.json
```

---

## Real-World Examples

### Example 1: Content Moderation

**Use Case:** Moderate user-generated content for safety

**Prompt Definition:**
```json
{
  "id": "content.moderation.v1",
  "io": { "channel": "text", "expects": "structured/json" },
  "prompt": "You are a content moderator. Analyze the following text for policy violations.\n\nClassify into categories:\n- safe: No violations\n- spam: Promotional/spam content\n- toxic: Harassment, hate speech\n- explicit: Sexual/graphic content\n- harmful: Violence, self-harm\n\nRespond with JSON:\n{\n  \"category\": \"<category>\",\n  \"confidence\": <0.0-1.0>,\n  \"reason\": \"<brief explanation>\",\n  \"action\": \"approve|review|block\"\n}"
}
```

**Expectation Suite:**
```json
{
  "checks": [
    { "type": "pc.check.json_valid" },
    { "type": "pc.check.json_required", "fields": ["category", "confidence", "reason", "action"] },
    { "type": "pc.check.enum", "field": "$.category", "allowed": ["safe", "spam", "toxic", "explicit", "harmful"] },
    { "type": "pc.check.enum", "field": "$.action", "allowed": ["approve", "review", "block"] },
    { "type": "pc.check.latency_budget", "p95_ms": 1500 },
    { "type": "pc.check.token_budget", "max_out": 150 }
  ]
}
```

**Evaluation Profile:**
```json
{
  "targets": [{ "type": "openai", "model": "gpt-4o-mini", "params": { "temperature": 0.1 }}],
  "fixtures": [
    { "id": "safe_content", "input": "I love this product! Great quality." },
    { "id": "spam_content", "input": "CLICK HERE FOR FREE MONEY!!! 💰💰💰" },
    { "id": "toxic_content", "input": "You're an idiot and should..." },
    { "id": "edge_borderline", "input": "This is somewhat controversial but..." }
  ],
  "execution": {
    "mode": "enforce",
    "max_retries": 1,
    "strict_enforce": true
  },
  "tolerances": {
    "pc.check.enum": { "max_fail_rate": 0.0 }  // Zero tolerance for moderation
  }
}
```

### Example 2: Financial Transaction Classifier

**Use Case:** Categorize bank transactions for budgeting

**Prompt Definition:**
```json
{
  "id": "transaction.classifier.v2",
  "io": { "channel": "text", "expects": "structured/json" },
  "prompt": "You are a financial transaction classifier. Categorize the following transaction.\n\nCategories:\n- groceries, dining, transportation, utilities, entertainment, shopping, healthcare, income, transfer, other\n\nRespond with JSON:\n{\n  \"category\": \"<category>\",\n  \"subcategory\": \"<optional specific type>\",\n  \"merchant_type\": \"<type of business>\",\n  \"is_recurring\": <true|false>\n}\n\nDo NOT use markdown formatting."
}
```

**Expectation Suite:**
```json
{
  "checks": [
    { "type": "pc.check.json_valid" },
    { "type": "pc.check.json_required", "fields": ["category", "merchant_type", "is_recurring"] },
    { "type": "pc.check.enum", "field": "$.category", "allowed": ["groceries", "dining", "transportation", "utilities", "entertainment", "shopping", "healthcare", "income", "transfer", "other"] },
    { "type": "pc.check.regex_absent", "pattern": "```" },
    { "type": "pc.check.token_budget", "max_out": 200 },
    { "type": "pc.check.latency_budget", "p95_ms": 2000 }
  ]
}
```

**Evaluation Profile:**
```json
{
  "targets": [
    { "type": "openai", "model": "gpt-4o-mini" },
    { "type": "ollama", "model": "mistral" }
  ],
  "fixtures": [
    { "id": "grocery_store", "input": "WHOLE FOODS MARKET - $87.34" },
    { "id": "restaurant", "input": "CHIPOTLE #2847 - $15.67" },
    { "id": "gas_station", "input": "SHELL OIL 12345678 - $52.00" },
    { "id": "subscription", "input": "NETFLIX.COM - $15.99" },
    { "id": "unclear", "input": "SQ *UNKNOWN MERCHANT - $23.45" }
  ],
  "execution": {
    "mode": "auto",
    "max_retries": 2,
    "auto_repair": {
      "lowercase_fields": ["$.category"],
      "strip_markdown_fences": true
    }
  },
  "tolerances": {
    "pc.check.json_valid": { "max_fail_rate": 0.0 },
    "pc.check.enum": { "max_fail_rate": 0.05 },
    "pc.check.token_budget": { "max_fail_rate": 0.1 }
  }
}
```

### Example 3: Customer Sentiment Analyzer

**Use Case:** Analyze customer feedback sentiment with reasoning

**Prompt Definition:**
```json
{
  "id": "sentiment.analyzer.v1",
  "io": { "channel": "text", "expects": "structured/json" },
  "prompt": "You are a customer feedback sentiment analyzer.\n\nAnalyze the sentiment and extract key insights.\n\nRespond with JSON:\n{\n  \"sentiment\": \"positive|negative|neutral|mixed\",\n  \"score\": <-1.0 to 1.0>,\n  \"key_topics\": [\"topic1\", \"topic2\"],\n  \"actionable\": <true|false>,\n  \"summary\": \"<one sentence summary>\"\n}\n\nDo NOT use markdown code fences."
}
```

**Expectation Suite:**
```json
{
  "checks": [
    { "type": "pc.check.json_valid" },
    { "type": "pc.check.json_required", "fields": ["sentiment", "score", "key_topics", "actionable", "summary"] },
    { "type": "pc.check.enum", "field": "$.sentiment", "allowed": ["positive", "negative", "neutral", "mixed"] },
    { "type": "pc.check.regex_absent", "pattern": "```" },
    { "type": "pc.check.token_budget", "max_out": 300 }
  ]
}
```

---

## Quick Reference

### Execution Mode Cheat Sheet

```bash
# observe - Monitor without changes
prompt-contracts run --pd pd.json --es es.json --ep ep.observe.json

# assist - Augment prompts with constraints
prompt-contracts run --pd pd.json --es es.json --ep ep.assist.json

# enforce - Schema-guided (OpenAI)
prompt-contracts run --pd pd.json --es es.json --ep ep.enforce.json

# auto - Adaptive (recommended)
prompt-contracts run --pd pd.json --es es.json --ep ep.auto.json
```

### Common Check Patterns

```json
// Basic structure validation
{ "type": "pc.check.json_valid" }
{ "type": "pc.check.json_required", "fields": ["field1", "field2"] }

// Enum validation
{ "type": "pc.check.enum", "field": "$.status", "allowed": ["active", "inactive"] }

// Array validation
{ "type": "pc.check.enum", "field": "$.items[*].type", "allowed": ["A", "B"] }

// Pattern matching
{ "type": "pc.check.regex_absent", "pattern": "```" }

// Performance
{ "type": "pc.check.token_budget", "max_out": 200 }
{ "type": "pc.check.latency_budget", "p95_ms": 3000 }
```

### Auto-Repair Patterns

```json
{
  "auto_repair": {
    // Always enable for JSON
    "strip_markdown_fences": true,

    // Lowercase enum fields
    "lowercase_fields": ["$.status", "$.category", "$.priority"]
  }
}
```

---

## Additional Resources

- **Full Documentation:** [README.md](README.md)
- **Getting Started:** [QUICKSTART.md](QUICKSTART.md)
- **Examples:** [examples/](examples/)
- **PCSL Specification:** [promptcontracts/spec/pcsl-v0.1.md](promptcontracts/spec/pcsl-v0.1.md)
- **GitHub:** https://github.com/philippmelikidis/prompt-contracts

---

## Contributing

Have a best practice to share? We welcome contributions!

1. Fork the repository
2. Add your best practice to this guide
3. Include a real-world example if possible
4. Open a pull request

---

**Last Updated:** 2025-10-09
**Version:** 1.0
