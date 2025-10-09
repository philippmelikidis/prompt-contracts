# Test Repair Example

This example is specifically designed to **trigger auto-repair** by intentionally getting the LLM to produce output that needs fixing.

## The Setup

The prompt **deliberately asks the LLM to**:
- Use capitalization (e.g., "Technical", "High") - which will fail enum checks expecting lowercase
- Wrap response in markdown code fences (```json ... ```) - which will fail the regex_absent check

The expectation suite requires:
- Lowercase enums: `["technical", "billing", "other"]` and `["low", "medium", "high"]`
- No markdown fences

## Testing Different Modes

### 1. Observe Mode (Will FAIL)

```bash
prompt-contracts run \
  --pd examples/test_repair/pd.json \
  --es examples/test_repair/es.json \
  --ep examples/test_repair/ep_observe.json \
  --save-io artifacts/test_observe \
  --verbose
```

**Expected outcome:**
- Status: FAIL
- Enum checks fail because "Technical" != "technical", "High" != "high"
- Regex check fails because of ```json fences
- No auto-repair applied (observe mode)

**Check the artifacts:**
```bash
cat artifacts/test_observe/ollama:mistral/password_issue/output_raw.txt
# Should show: ```json\n{"category": "Technical", "priority": "High", ...}\n```

cat artifacts/test_observe/ollama:mistral/password_issue/output_norm.txt
# Same as raw (no normalization in observe mode)

jq '.status' artifacts/test_observe/ollama:mistral/password_issue/run.json
# Should show: "FAIL"
```

### 2. Assist Mode (Should REPAIR)

```bash
prompt-contracts run \
  --pd examples/test_repair/pd.json \
  --es examples/test_repair/es.json \
  --ep examples/test_repair/ep_assist.json \
  --save-io artifacts/test_assist \
  --verbose
```

**Expected outcome:**
- Status: REPAIRED
- Auto-repair fixes:
  - Strips markdown fences: ```json ... ``` → {...}
  - Lowercases fields: "Technical" → "technical", "High" → "high"
- All checks pass after repair

**Check the artifacts:**
```bash
# Raw output (before repair)
cat artifacts/test_assist/ollama:mistral/password_issue/output_raw.txt
# Should show: ```json\n{"category": "Technical", "priority": "High", ...}\n```

# Normalized output (after repair)
cat artifacts/test_assist/ollama:mistral/password_issue/output_norm.txt
# Should show: {"category": "technical", "priority": "high", ...}

# Check repair details
jq '.repaired_details' artifacts/test_assist/ollama:mistral/password_issue/run.json
# Should show:
# {
#   "stripped_fences": true,
#   "lowercased_fields": ["$.category", "$.priority"]
# }

# Check status
jq '.status' artifacts/test_assist/ollama:mistral/password_issue/run.json
# Should show: "REPAIRED"
```

## What This Tests

1. **Markdown fence stripping**: The prompt tells LLM to use ```json fences, which auto-repair should remove
2. **Field lowercasing**: The prompt tells LLM to capitalize, which auto-repair should fix
3. **Observe vs Assist comparison**: Shows how same prompt fails in observe but succeeds in assist
4. **Artifact tracking**: All transformations are logged in run.json

## Verification Commands

```bash
# Compare raw vs normalized
diff \
  artifacts/test_assist/ollama:mistral/password_issue/output_raw.txt \
  artifacts/test_assist/ollama:mistral/password_issue/output_norm.txt

# See what was repaired
jq '{status, repaired_details, checks: [.checks[] | select(.result == "PASS" or .result == "FAIL")]}' \
  artifacts/test_assist/ollama:mistral/password_issue/run.json

# Check if fences were stripped
grep -c '```' artifacts/test_assist/ollama:mistral/password_issue/output_norm.txt || echo "Fences removed!"

# Check if fields were lowercased
jq '.category, .priority' artifacts/test_assist/ollama:mistral/password_issue/output_norm.txt
```

## Expected Flow

### Observe Mode:
```
1. LLM generates: ```json\n{"category": "Technical", ...}\n```
2. Validate raw output → FAIL (has fences, wrong case)
3. Status: FAIL
```

### Assist Mode:
```
1. LLM generates: ```json\n{"category": "Technical", ...}\n```
2. Validate raw output → FAIL
3. Apply auto-repair:
   - Strip fences: {"category": "Technical", ...}
   - Lowercase: {"category": "technical", "priority": "high", ...}
4. Re-validate normalized output → PASS
5. Status: REPAIRED
```

## Troubleshooting

If auto-repair doesn't trigger:
- Check that Ollama is running: `ollama serve`
- Verify the model gives capitalized output (it usually does)
- Try adjusting temperature in EP (higher = more variation)
- Check `output_raw.txt` to see what LLM actually produced
