# Troubleshooting Guide

Common issues and solutions for Prompt-Contracts.

---

## Table of Contents

- [Installation Issues](#installation-issues)
- [Validation Errors](#validation-errors)
- [Runtime Errors](#runtime-errors)
- [Execution Modes](#execution-modes)
- [Artifact Issues](#artifact-issues)
- [Provider-Specific Issues](#provider-specific-issues)
- [CI/CD Issues](#cicd-issues)

---

## Installation Issues

### Command not found: prompt-contracts

**Problem:** After installation, `prompt-contracts` command is not available.

**Solutions:**

1. **Check installation method:**
```bash
# If installed from PyPI
pip install --upgrade prompt-contracts

# If installed from source
cd prompt-contracts
pip install -e .
```

2. **Check PATH:**
```bash
# Find where pip installs scripts
python -m site --user-base

# Add to PATH if needed (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"
```

3. **Use as module:**
```bash
python -m promptcontracts.cli --help
```

### ModuleNotFoundError

**Problem:** `ModuleNotFoundError: No module named 'promptcontracts'`

**Solutions:**

1. **Ensure installed in correct environment:**
```bash
# Check Python version
python --version  # Should be 3.10+

# Check if installed
pip list | grep prompt-contracts

# Reinstall
pip install --force-reinstall prompt-contracts
```

2. **Virtual environment activation:**
```bash
# If using venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

---

## Validation Errors

### Schema Validation Failed

**Problem:** `✗ Validation failed: 'field' is a required property`

**Solution:** Your artefact is missing required fields. Check the schema:

```bash
# PD must have: pcsl, id, io, prompt
# ES must have: pcsl, checks
# EP must have: pcsl, targets, fixtures
```

**Example fix for EP:**
```json
{
  "pcsl": "0.1.0",
  "targets": [
    { "type": "ollama", "model": "mistral", "params": {} }
  ],
  "fixtures": [
    { "id": "test1", "input": "Sample input" }
  ],
  "execution": {
    "mode": "auto",
    "max_retries": 1
  }
}
```

### Unknown Check Type

**Problem:** `Unknown check type: pc.check.custom`

**Solution:** Only these check types are supported in v0.2.x (v0.3.0 adds semantic checks):
- `pc.check.json_valid`
- `pc.check.json_required`
- `pc.check.enum`
- `pc.check.regex_absent`
- `pc.check.token_budget`
- `pc.check.latency_budget`

### Invalid Enum Values

**Problem:** Enum check fails with `Value 'High' not in allowed values ['low', 'medium', 'high']`

**Solutions:**

1. **Use auto-repair with lowercase_fields:**
```json
{
  "execution": {
    "mode": "assist",
    "auto_repair": {
      "lowercase_fields": ["$.priority", "$.status"]
    }
  }
}
```

2. **Use case_insensitive enum:**
```json
{
  "type": "pc.check.enum",
  "field": "$.priority",
  "allowed": ["low", "medium", "high"],
  "case_insensitive": true
}
```

---

## Runtime Errors

### Adapter Connection Error

**Problem:** `Connection refused` or `Adapter error` when using Ollama

**Solutions:**

1. **Ensure Ollama is running:**
```bash
# Start Ollama server
ollama serve

# In another terminal, verify it's running
curl http://localhost:11434/api/tags
```

2. **Pull the model:**
```bash
ollama pull mistral
ollama list  # Verify model is available
```

### OpenAI API Error

**Problem:** `OpenAI API key not found` or `Incorrect API key`

**Solutions:**

1. **Set environment variable:**
```bash
# Linux/Mac
export OPENAI_API_KEY="sk-..."

# Windows
set OPENAI_API_KEY=sk-...

# Verify
echo $OPENAI_API_KEY
```

2. **Check API key validity:**
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### JSON Parsing Error

**Problem:** `JSONDecodeError: Expecting value`

**Solutions:**

1. **Enable markdown fence stripping:**
```json
{
  "execution": {
    "auto_repair": {
      "strip_markdown_fences": true
    }
  }
}
```

2. **Check raw output:**
```bash
# Run with --save-io
prompt-contracts run ... --save-io artifacts/

# Inspect raw output
cat artifacts/ollama:mistral/fixture_id/output_raw.txt
```

3. **Improve prompt clarity:**
```json
{
  "prompt": "Reply with ONLY valid JSON. Do NOT use markdown code fences (```). Do NOT include explanations."
}
```

---

## Execution Modes

### NONENFORCEABLE Status

**Problem:** Fixtures marked as `NONENFORCEABLE` when using `enforce` mode.

**Explanation:** This happens when:
- You requested `enforce` mode
- The adapter doesn't support schema-guided JSON
- `strict_enforce` is set to `true`

**Solutions:**

1. **Use `auto` mode** (automatically selects best mode):
```json
{
  "execution": { "mode": "auto" }
}
```

2. **Use `assist` mode** for non-OpenAI providers:
```json
{
  "execution": { "mode": "assist" }
}
```

3. **Disable strict_enforce:**
```json
{
  "execution": {
    "mode": "enforce",
    "strict_enforce": false  // Falls back to assist
  }
}
```

### Mode Not Applied

**Problem:** Constraints not visible in prompt despite using `assist` mode.

**Solutions:**

1. **Check artifacts:**
```bash
cat artifacts/*/*/input_final.txt
# Should contain CONSTRAINTS block
```

2. **Verify execution block:**
```json
{
  "execution": {
    "mode": "assist"  // Not "observe"
  }
}
```

### High Repair Rate

**Problem:** Most fixtures showing `REPAIRED` status.

**Analysis:** This indicates prompt clarity issues.

**Solutions:**

1. **Improve prompt specificity:**
```json
{
  "prompt": "Respond with valid JSON containing:\n- priority: exactly one of ['low', 'medium', 'high'] (lowercase)\n- category: string\n\nDo NOT use markdown formatting."
}
```

2. **Add format example:**
```json
{
  "prompt": "Reply with JSON in this exact format:\n{\"priority\": \"low\", \"category\": \"support\"}"
}
```

3. **Review auto-repair settings:**
```bash
# Check run.json for repair details
jq '.repaired_details' artifacts/*/*/run.json
```

---

## Artifact Issues

### Artifacts Not Saved

**Problem:** No artifacts directory created.

**Solutions:**

1. **Ensure --save-io flag is used:**
```bash
prompt-contracts run \
  --pd pd.json --es es.json --ep ep.json \
  --save-io artifacts/  # <-- Required
```

2. **Check permissions:**
```bash
ls -ld artifacts/
# Should be writable
chmod 755 artifacts/
```

### Cannot Find Artifact Paths

**Problem:** Need to locate specific fixture artifacts.

**Solution:** Artifacts are organized by target and fixture:

```bash
artifacts/
  <target-type>:<model>/
    <fixture-id>/
      input_final.txt
      output_raw.txt
      output_norm.txt
      run.json

# Example
artifacts/ollama:mistral/pwd_reset/run.json
```

**View artifact paths from JSON report:**
```bash
prompt-contracts run ... --report json --out results.json
jq '.targets[].fixtures[].artifact_paths' results.json
```

### Artifact Paths Not Absolute

**Problem:** Artifact paths in run.json are relative.

**Solution:** This was fixed in v0.2.3. Upgrade to v0.3.0 for the latest fixes:
```bash
pip install --upgrade prompt-contracts
```

---

## Provider-Specific Issues

### Ollama: Schema Enforcement Not Supported

**Important:** Ollama and most local models currently **do not support** schema-guided JSON enforcement. This is **expected behavior**, not an error.

**What This Means:**
- Ollama automatically falls back to `assist` mode (even if `mode: enforce` is requested)
- Assist mode adds intelligent constraints to prompts and applies auto-repair
- This provides robust output validation without requiring native schema support
- **Recommended:** Use `mode: assist` or `mode: auto` for Ollama

**Example EP Configuration for Ollama:**
```json
{
  "targets": [
    { "type": "ollama", "model": "mistral", "params": {"temperature": 0.3} }
  ],
  "execution": {
    "mode": "assist",  // or "auto" for automatic fallback
    "max_retries": 2,
    "auto_repair": {
      "strip_markdown_fences": true,
      "lowercase_fields": ["$.category", "$.priority"]
    }
  }
}
```

**Why Assist Mode is Recommended:**
- ✅ Automatically adds constraint blocks to prompts
- ✅ Auto-repair fixes common issues (markdown fences, casing)
- ✅ Works reliably with local models
- ✅ No API costs, privacy-first

### Ollama: Model Not Found

**Problem:** `Model 'mistral' not found`

**Solutions:**

```bash
# Pull model
ollama pull mistral

# List available models
ollama list

# Use correct model name in EP
{
  "targets": [
    { "type": "ollama", "model": "mistral", "params": {} }
  ]
}
```

### OpenAI: Rate Limit

**Problem:** `Rate limit exceeded`

**Solutions:**

1. **Add retry delay** (handled automatically by SDK)
2. **Reduce concurrent fixtures** (run sequentially)
3. **Use lower tier model:**
```json
{
  "targets": [
    { "type": "openai", "model": "gpt-3.5-turbo", "params": {} }
  ]
}
```

### OpenAI: Token Limit Exceeded

**Problem:** `This model's maximum context length is...`

**Solutions:**

1. **Shorten prompt:**
```json
{
  "prompt": "Concise prompt here..."
}
```

2. **Set max_tokens:**
```json
{
  "targets": [
    {
      "type": "openai",
      "model": "gpt-4o-mini",
      "params": { "max_tokens": 500 }
    }
  ]
}
```

---

## CI/CD Issues

### Tests Fail in CI

**Problem:** Tests pass locally but fail in GitHub Actions/GitLab CI.

**Solutions:**

1. **Path issues** (relative vs absolute):
```bash
# Use absolute paths in CI
export ARTIFACTS_DIR="$PWD/artifacts"
prompt-contracts run ... --save-io "$ARTIFACTS_DIR"
```

2. **Missing dependencies:**
```yaml
# .github/workflows/ci.yml
- name: Install dependencies
  run: |
    pip install -e .
    pip install pytest
```

3. **Ollama not available in CI:**
```yaml
# Use OpenAI in CI, Ollama locally
# ep.ci.json
{
  "targets": [
    { "type": "openai", "model": "gpt-3.5-turbo", "params": {} }
  ]
}
```

### Environment Variables

**Problem:** `OPENAI_API_KEY` not set in CI.

**Solution:** Add to repository secrets:

```yaml
# GitHub Actions
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

```yaml
# GitLab CI
variables:
  OPENAI_API_KEY: $OPENAI_API_KEY  # From CI/CD variables
```

---

## Common Patterns

### Debug Mode

Enable verbose output to see what's happening:

```bash
prompt-contracts run \
  --pd pd.json --es es.json --ep ep.json \
  --verbose \
  --save-io artifacts/
```

### Inspect Artifacts

```bash
# View final prompt (with constraints)
cat artifacts/ollama:mistral/fixture_id/input_final.txt

# View raw model output
cat artifacts/ollama:mistral/fixture_id/output_raw.txt

# View normalized output (after auto-repair)
cat artifacts/ollama:mistral/fixture_id/output_norm.txt

# View full execution metadata
jq '.' artifacts/ollama:mistral/fixture_id/run.json
```

### Check Exit Codes

```bash
prompt-contracts run ... ; echo "Exit code: $?"

# 0 = success (all PASS or REPAIRED)
# 1 = failure (some FAIL or NONENFORCEABLE)
# 2 = validation error (PD/ES/EP schema issue)
# 3 = runtime error (adapter/connection issue)
```

### View Help

```bash
# Main help
prompt-contracts --help

# Command-specific help
prompt-contracts run --help
prompt-contracts validate --help
```

---

## Getting More Help

If your issue isn't covered here:

1. **Check run.json** for detailed execution info
2. **Enable --verbose** mode
3. **Review logs** in artifacts/
4. **Check GitHub Issues:** https://github.com/philippmelikidis/prompt-contracts/issues
5. **Read Documentation:**
   - [README.md](README.md)
   - [QUICKSTART.md](QUICKSTART.md)
   - [BEST_PRACTICES.md](BEST_PRACTICES.md)

---

**Last Updated:** 2025-01-09
**Version:** 0.3.0
