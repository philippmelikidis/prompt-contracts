# Migration Guide: v0.2.x → v0.3.0

## Overview

Version 0.3.0 introduces probabilistic contracts, semantic validation, and enhanced reproducibility. Most v0.2.x contracts will work without modification, but new features require schema updates.

## Breaking Changes

### None

v0.3.0 is backward compatible. All v0.2.x PD/ES/EP files work without changes.

## New Features

### 1. Probabilistic Sampling (EP)

**v0.2.x**: Single execution per fixture

**v0.3.0**: N-sampling with aggregation

```json
{
  "pcsl": "0.3.0",
  "sampling": {
    "n": 5,
    "seed": 42,
    "aggregation": "majority",
    "bootstrap_samples": 1000,
    "confidence_level": 0.95
  }
}
```

**Migration**:
- Add `sampling` section to EP
- Default: `{"n": 1}` (equivalent to v0.2.x)
- Set `seed` for reproducibility

### 2. Repair Policy (EP)

**v0.2.x**: `auto_repair` with boolean flags

**v0.3.0**: Structured `repair_policy`

```json
{
  "execution": {
    "repair_policy": {
      "enabled": true,
      "max_steps": 2,
      "allowed": ["strip_markdown_fences", "json_loose_parse"]
    }
  }
}
```

**Migration**:
- Old `auto_repair` still works
- New `repair_policy` provides finer control
- `json_loose_parse` replaces basic JSON repair

### 3. Semantic Checks (ES)

**New check types**:

```json
{
  "checks": [
    {
      "type": "pc.check.contains_all",
      "required": ["keyword1", "keyword2"],
      "case_sensitive": false
    },
    {
      "type": "pc.check.contains_any",
      "options": ["option1", "option2"]
    },
    {
      "type": "pc.check.regex_present",
      "pattern": "\\d{3}-\\d{3}-\\d{4}",
      "flags": "i"
    },
    {
      "type": "pc.check.similarity",
      "reference": "Expected semantic meaning",
      "threshold": 0.8
    }
  ]
}
```

**Migration**:
- Add semantic checks alongside existing structural checks
- `similarity` requires embedding adapter (optional dependency)

### 4. LLM-as-Judge (ES)

**New**:

```json
{
  "type": "pc.check.judge",
  "criteria": "Is the response professional and accurate?",
  "pass_when": "all",
  "budget": {
    "max_tokens": 500,
    "max_latency_ms": 3000
  }
}
```

**Migration**:
- Add judge checks for subjective quality
- Requires judge adapter initialization

### 5. Enhanced CLI Flags

**v0.2.x**: `--save-io`, `--report`, `--out`

**v0.3.0**: Additional flags

```bash
prompt-contracts run \
  --pd pd.json --es es.json --ep ep.json \
  --n 5 \                    # NEW: Override sampling.n
  --seed 42 \                # NEW: Set random seed
  --temperature 0.7 \        # NEW: Override temperature
  --top-p 0.9 \              # NEW: Override top-p
  --baseline structural-only # NEW: Baseline comparison
```

**Migration**:
- CLI flags override EP settings
- Useful for experiments without editing files

## Schema Updates

### PD: No changes required

- v0.2.x PD files work as-is
- Optional: Update `pcsl` field to `"0.3.0"`

### ES: Optional new checks

```json
{
  "pcsl": "0.3.0",
  "checks": [
    // Existing v0.2.x checks still work
    {"type": "pc.check.json_valid"},
    {"type": "pc.check.json_required", "fields": ["name"]},

    // NEW v0.3.0 checks (optional)
    {"type": "pc.check.contains_all", "required": ["key"]},
    {"type": "pc.check.similarity", "reference": "...", "threshold": 0.8}
  ]
}
```

### EP: Optional new sections

```json
{
  "pcsl": "0.3.0",
  "execution": {
    "mode": "auto",  // unchanged
    "max_retries": 1,  // DEPRECATED (use sampling.n instead)
    "repair_policy": {  // NEW
      "enabled": true,
      "max_steps": 2,
      "allowed": ["strip_markdown_fences", "json_loose_parse"]
    }
  },
  "sampling": {  // NEW
    "n": 1,
    "seed": null,
    "aggregation": "first"
  }
}
```

## Code Changes

### ContractRunner Initialization

**v0.2.x**:
```python
runner = ContractRunner(pd, es, ep, save_io_dir="artifacts")
results = runner.run()
```

**v0.3.0** (backward compatible):
```python
from promptcontracts.core.adapters.embeddings_local import LocalEmbeddingAdapter
from promptcontracts.core.adapters.judge_openai import OpenAIJudgeAdapter

# Optional: Add adapters for new checks
embedding_adapter = LocalEmbeddingAdapter()  # For similarity check
judge_adapter = OpenAIJudgeAdapter()  # For judge check

runner = ContractRunner(
    pd, es, ep,
    save_io_dir="artifacts",
    embedding_adapter=embedding_adapter,  # NEW
    judge_adapter=judge_adapter,  # NEW
)
results = runner.run()
```

### Results Structure

**v0.2.x**:
```python
{
  "targets": [
    {
      "fixtures": [
        {
          "status": "PASS" | "REPAIRED" | "FAIL",
          "latency_ms": 1234,
          "retries_used": 0
        }
      ]
    }
  ]
}
```

**v0.3.0** (enhanced):
```python
{
  "pcsl_version": "0.3.0",  # NEW
  "targets": [
    {
      "execution": {
        "negotiation_log": [...],  # NEW
        "repair_policy": {...},  # NEW
        "sampling": {...}  # NEW
      },
      "fixtures": [
        {
          "status": "PASS" | "FAIL",  # "REPAIRED" deprecated
          "latency_ms": 1234,
          "mean_latency_ms": 1200,  # NEW (if n > 1)
          "sampling_metadata": {  # NEW
            "n_samples": 5,
            "pass_rate": 0.8,
            "confidence_interval": [0.6, 0.95]
          },
          "repair_ledger": [...]  # NEW
        }
      ]
    }
  ]
}
```

## Deprecations

### `max_retries` (EP.execution)

**Status**: Deprecated (still works)

**Reason**: Replaced by `sampling.n` for clearer semantics

**Migration**:
```json
// OLD (v0.2.x)
{"execution": {"max_retries": 3}}

// NEW (v0.3.0)
{"sampling": {"n": 4}}  // n+1 attempts
```

### `REPAIRED` status

**Status**: Deprecated (not generated in v0.3.0)

**Reason**: Repairs tracked in `repair_ledger` instead

**Migration**:
- Check `repair_ledger` for repair details
- Status is now `PASS` or `FAIL` only

## Installation

### v0.2.x
```bash
pip install prompt-contracts==0.2.3
```

### v0.3.0
```bash
pip install prompt-contracts==0.3.0

# Optional: For semantic checks
pip install sentence-transformers numpy
```

## Testing Your Migration

1. **Validate schemas**:
```bash
prompt-contracts validate pd your_pd.json
prompt-contracts validate es your_es.json
prompt-contracts validate ep your_ep.json
```

2. **Run with v0.3.0**:
```bash
prompt-contracts run \
  --pd your_pd.json \
  --es your_es.json \
  --ep your_ep.json \
  --report json --out results.json
```

3. **Compare results**:
- Check `pcsl_version` field
- Verify all checks pass
- Inspect new `sampling_metadata` and `repair_ledger`

## Rollback

If issues occur, downgrade:
```bash
pip install prompt-contracts==0.2.3
```

All v0.2.x artifacts are forward compatible with v0.3.0, but not vice versa (v0.3.0 artifacts may not load in v0.2.x if they use new features).

## Support

- Issues: https://github.com/your-org/prompt-contracts/issues
- Docs: https://prompt-contracts.readthedocs.io
- Examples: `examples/` directory in repository

---

**Version**: 1.0.0
**Applies to**: prompt-contracts 0.2.x → 0.3.0
**Last Updated**: 2025-01-09
