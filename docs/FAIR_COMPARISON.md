# Fair Comparison Protocol

**Version:** 1.0.0
**PCSL Version:** 0.3.2
**Last Updated:** 2025-01-10

## Overview

This document defines the protocol for **fair, statistically sound comparisons** between PCSL and baseline systems (CheckList, Guidance, OpenAI Structured Outputs, etc.).

Fair comparisons require:
1. **Identical fixtures** across all systems
2. **Identical configurations** (seed, temperature, stop sequences)
3. **Paired statistical tests** (McNemar for binary, bootstrap for continuous)
4. **Standardized setup time measurement**
5. **Reproducible evaluation** with fixed seeds

## 1. Fixture Standardization

### Requirements

All systems must evaluate on **exactly the same fixtures** in **the same order**.

```python
# Load fixtures once, use for all systems
fixtures = load_pcsl_fixtures("examples/classification_en/fixtures.jsonl")

# Use with PCSL
pcsl_results = run_pcsl(fixtures, config)

# Convert to baseline format
checklist_fixtures = standardize_fixtures(fixtures, format="checklist")
checklist_results = run_checklist(checklist_fixtures, config)
```

### Fixture Format

PCSL canonical format:
```json
{
  "id": "fixture_001",
  "input": "...",
  "gold": "...",
  "metadata": {"domain": "...", "difficulty": "..."}
}
```

## 2. Configuration Equivalence

### Required Parameters

All systems must use:
- **Same random seed** (default: 42)
- **Same temperature** (e.g., 0.0 for deterministic, 0.7 for sampling)
- **Same top_p** (if applicable)
- **Same stop sequences** (if applicable)
- **Same model** (e.g., gpt-4o-mini)

### Example Configuration

```json
{
  "seed": 42,
  "temperature": 0.0,
  "top_p": 1.0,
  "stop_sequences": null,
  "model": "gpt-4o-mini",
  "max_tokens": 1000
}
```

### Verification

```bash
# Verify configuration match
prompt-contracts compare \
  --config-check \
  --systems pcsl,checklist \
  --fixtures examples/classification_en/fixtures.jsonl
```

## 3. Statistical Significance Testing

### Binary Outcomes (Pass/Fail)

Use **McNemar's test** for paired binary outcomes:

```python
from promptcontracts.stats.significance import mcnemar_test

# Count disagreements
a01 = 15  # System A failed, System B passed
a10 = 5   # System A passed, System B failed

p_value = mcnemar_test(a01, a10)

if p_value < 0.05:
    print("Significant difference detected")
else:
    print("No significant difference")
```

**Interpretation:**
- **p < 0.05**: Systems differ significantly
- **p ≥ 0.05**: No significant difference detected

**Reporting:**
- Always report counts (a01, a10) along with p-value
- Use continuity correction for small samples (default: enabled)
- Require a01 + a10 ≥ 10 for reliable approximation

### Continuous Metrics (Latency, F1, etc.)

Use **bootstrap difference CI** for continuous metrics:

```python
from promptcontracts.stats.significance import bootstrap_diff_ci

latencies_a = [120, 135, 128, ...]  # ms
latencies_b = [110, 125, 118, ...]  # ms (same fixtures)

lower, upper = bootstrap_diff_ci(latencies_a, latencies_b, B=1000)

if upper < 0:
    print(f"System B significantly faster: {lower:.1f} to {upper:.1f} ms")
elif lower > 0:
    print(f"System B significantly slower: {lower:.1f} to {upper:.1f} ms")
else:
    print("No significant latency difference")
```

**Interpretation:**
- **CI excludes 0**: Significant difference
- **CI contains 0**: No significant difference

## 4. Setup Time Measurement

"Setup time" = time from template import to first successful run

### Protocol

1. **Start timer** when user first accesses system templates/docs
2. **Stop timer** when first run completes successfully (validation passes)
3. **Record steps**: number of iterations needed
4. **Exclude** time spent reading external documentation (e.g., API docs)

### Scripted Measurement

```bash
#!/bin/bash
# setup_time_measurement.sh

SYSTEM=$1
START_TIME=$(date +%s)

case $SYSTEM in
  pcsl)
    # Copy template
    cp examples/classification_en/ep.json my_ep.json
    # First run
    prompt-contracts run --pd pd.json --es es.json --ep my_ep.json
    ;;
  checklist)
    # Adapt CheckList template
    python adapt_checklist_template.py
    python run_checklist.py
    ;;
esac

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

echo "Setup time for $SYSTEM: ${ELAPSED}s"
```

### Reporting

Report setup time as:
```
System A: 5 minutes, 2 iterations
System B: 15 minutes, 5 iterations
```

## 5. Comparison Harness

### CLI Usage

```bash
# Compare PCSL vs CheckList on validation success
prompt-contracts compare \
  --suite classification_en \
  --systems pcsl,checklist \
  --metric validation_success \
  --sig mcnemar \
  --out comparison_results.json

# Compare latencies
prompt-contracts compare \
  --suite classification_en \
  --systems pcsl,guidance \
  --metric latency_ms \
  --sig bootstrap \
  --out latency_comparison.json
```

### Python API

```python
from promptcontracts.eval import BaselineSystem, compare_systems

# Define systems
pcsl = BaselineSystem(
    name="pcsl",
    fixtures=fixtures,
    outcomes=[1, 1, 0, 1, 1, ...],  # Pass/fail
    metrics={"latency": [120, 135, ...]},
    config={"seed": 42, "temperature": 0.0}
)

checklist = BaselineSystem(
    name="checklist",
    fixtures=fixtures,
    outcomes=[1, 0, 0, 1, 1, ...],
    metrics={"latency": [150, 165, ...]},
    config={"seed": 42, "temperature": 0.0}
)

# Compare
result = compare_systems(pcsl, checklist, metric="validation_success")

print(f"P-value: {result['mcnemar_test']['p_value']}")
print(f"Significant: {result['mcnemar_test']['significant']}")
```

## 6. Reproducibility Requirements

### Environment

- **Python version**: 3.11.7 (fixed)
- **Package versions**: Pinned in `requirements.txt`
- **Random seeds**: Fixed throughout
- **Environment variables**:
  - `PYTHONHASHSEED=42`
  - `OMP_NUM_THREADS=1`
  - `TOKENIZERS_PARALLELISM=false`

### Docker

```bash
# Build reproducible image
docker build -t pcsl-comparison:0.3.2 .

# Run comparison
docker run --rm \
  -v $(pwd)/fixtures:/fixtures:ro \
  -v $(pwd)/results:/results \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  pcsl-comparison:0.3.2 \
  prompt-contracts compare \
    --suite /fixtures/classification_en \
    --systems pcsl,checklist \
    --out /results/comparison.json
```

## 7. Reporting Guidelines

### Minimum Required Information

1. **Systems compared**: Names and versions
2. **Fixtures**: Count, source, domain
3. **Configuration**: Seed, temperature, model
4. **Statistical test**: Method, p-value or CI
5. **Setup time**: For each system
6. **Reproducibility**: Docker image tag or commit hash

### Example Report

```markdown
## Comparison: PCSL vs CheckList

**Fixtures:** 100 email classification tasks (50 en, 50 de)
**Model:** gpt-4o-mini, temp=0.0, seed=42
**Setup Time:** PCSL 5min (2 iter), CheckList 18min (6 iter)

**Validation Success:**
- PCSL: 92/100 (92%)
- CheckList: 85/100 (85%)
- McNemar: a01=12, a10=5, p=0.076 (not significant at α=0.05)

**Latency (ms):**
- PCSL: mean=142 (95% CI: [135, 149])
- CheckList: mean=168 (95% CI: [159, 177])
- Bootstrap diff: -26ms (95% CI: [-35, -17]), **significant**

**Conclusion:** PCSL achieves similar validation success with significantly
lower latency. Setup time is 3.6× faster.
```

## 8. Limitations and Caveats

### Small Sample Sizes

- McNemar test requires a01 + a10 ≥ 10 for reliable approximation
- For smaller samples, use exact binomial test
- Bootstrap requires n ≥ 20 for stable CIs

### Multiple Comparisons

- When comparing > 2 systems, apply Bonferroni correction: α' = α / k
- For 3 systems (3 pairwise comparisons): use α' = 0.05 / 3 = 0.0167

### Setup Time Variability

- Setup time depends on user expertise
- Report range across multiple novice users if possible
- Exclude time for unrelated tasks (coffee breaks, etc.)

### Cross-Dataset Generalization

- Results on one dataset may not generalize
- Test on multiple domains for robustness
- Report domain-specific results separately

## 9. References

### Statistical Methods

- McNemar (1947). "Note on the sampling error of the difference between correlated proportions."
- Efron & Tibshirani (1993). "An Introduction to the Bootstrap."
- Brown, Cai & DasGupta (2001). "Interval Estimation for a Binomial Proportion."

### Baseline Systems

- **CheckList**: Ribeiro et al. (2020). "Beyond Accuracy: Behavioral Testing of NLP Models."
- **Guidance**: Microsoft Guidance library, https://github.com/guidance-ai/guidance
- **OpenAI Structured Outputs**: https://platform.openai.com/docs/guides/structured-outputs

## 10. Contact

For questions about the fair comparison protocol:
- Open an issue: https://github.com/your-org/prompt-contracts/issues
- Email: support@promptcontracts.org
