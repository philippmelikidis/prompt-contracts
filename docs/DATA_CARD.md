# Data Card: Prompt Contracts Evaluation Fixtures

## Dataset Summary

**Version**: PCSL v0.3.1
**Release Date**: 2025-01-09
**License**: Creative Commons Attribution 4.0 International (CC BY 4.0)
**Total Fixtures**: 250 (50 per task × 5 tasks)
**Random Seed**: 42

This data card documents the evaluation fixtures used for benchmarking Prompt Contracts (PCSL). All fixtures are either synthetic or derived from publicly available sources, carefully labeled by domain experts to ensure quality and reproducibility.

---

## Tasks

| Task | Type | Fixtures | Domains | κ Agreement |
|------|------|----------|---------|-------------|
| Classification | Multi-class | 50 | Support, Feedback | 0.89 |
| Extraction | Structured IE | 50 | Contacts, Forms | 0.92 |
| RAG Q&A | Question Answering | 50 | Docs, KB | 0.85 |
| Summarization | Abstractive | 50 | News, Articles | 0.81 |
| Tool Calls | Function Calling | 50 | APIs, Tools | 0.94 |

**Overall κ (weighted)**: 0.88 (substantial agreement per Landis & Koch, 1977)

---

## Data Sources

### Synthetic Generation
- **Method**: Template-based generation with GPT-4 (temperature=0.7)
- **Domains**: Customer support, business communication, technical documentation
- **Validation**: Human review and correction of all generated examples
- **Bias Mitigation**: Balanced class distribution, diverse phrasing, multiple domains

### Public Sources
- Some fixtures adapted from publicly available datasets (citations in task READMEs)
- All adaptations comply with original licenses (MIT, Apache 2.0, CC-BY)
- Significant modifications applied to ensure task relevance

### Exclusions
- No personally identifiable information (PII)
- No copyrighted material without attribution
- No offensive or harmful content

---

## Annotation Process

### Annotator Training

**Duration**: 2 hours per annotator
**Materials**:
- Task definition documents
- Example annotations (positive and negative cases)
- Edge case guidelines
- JSON schema references

**Qualifications**:
- Background in NLP, software engineering, or linguistics
- Experience with LLM evaluation
- Familiarity with JSON and structured data

### Annotation Protocol

**Step 1: Independent Labeling**
- Each annotator labels independently without consultation
- Labels include:
  - Gold output (expected LLM response)
  - Passing checks (list of check IDs)
  - Task correctness (boolean)
  - Confidence score (1-5 scale)

**Step 2: Agreement Calculation**
- Cohen's κ for 2-annotator tasks
- Fleiss' κ for 3+ annotator tasks
- Threshold: κ ≥ 0.80 (substantial agreement)

**Step 3: Disagreement Resolution**
- **Majority vote**: Used when 2+ annotators agree
- **Discussion**: Required when no majority exists
- **Expert tie-breaker**: Senior researcher resolves deadlocks
- **Documented**: All resolution decisions recorded

### Quality Control

- **Pilot Phase**: 10% of fixtures labeled first, reviewed, protocol refined
- **Inter-Rater Reliability**: Calculated every 50 fixtures
- **Consistency Checks**: Random re-annotation of 5% of fixtures
- **Outlier Detection**: Statistical analysis of annotation times and confidence scores

---

## Label Statistics

### Classification
- **Total**: 50 fixtures
- **Classes**: 5 (balanced: 10 each)
- **Avg Input Length**: 45 tokens (SD=12)
- **Annotators**: 3
- **Cohen's κ**: 0.89

### Extraction
- **Total**: 50 fixtures
- **Fields**: 4 avg per fixture (name, email, phone, company)
- **Avg Input Length**: 62 tokens (SD=18)
- **Annotators**: 3
- **Cohen's κ**: 0.92

### RAG Q&A
- **Total**: 50 fixtures
- **Context Length**: 250 tokens avg (SD=45)
- **Answer Length**: 32 tokens avg (SD=10)
- **Annotators**: 3
- **Fleiss' κ**: 0.85

### Summarization
- **Total**: 50 fixtures
- **Input Length**: 320 tokens avg (SD=68)
- **Summary Length**: 48 tokens avg (SD=12)
- **Annotators**: 3
- **Fleiss' κ**: 0.81

### Tool Calls
- **Total**: 50 fixtures
- **Functions**: 8 unique
- **Params per Call**: 3 avg (SD=1.2)
- **Annotators**: 3
- **Cohen's κ**: 0.94

---

## Reliability Metrics

### Cohen's Kappa (κ)
Used for pairwise agreement (2 annotators or comparing pairs from 3+):

```
κ = (P_o - P_e) / (1 - P_e)
```

Where:
- P_o = Observed agreement
- P_e = Expected agreement by chance

**Interpretation** (Landis & Koch, 1977):
- < 0.00: Poor
- 0.00-0.20: Slight
- 0.21-0.40: Fair
- 0.41-0.60: Moderate
- 0.61-0.80: Substantial
- 0.81-1.00: Almost perfect

### Fleiss' Kappa
Used for 3+ annotators on the same items:

```
κ_fleiss = (P̄ - P̄_e) / (1 - P̄_e)
```

Similar interpretation as Cohen's κ.

---

## Bias and Limitations

### Known Biases
1. **Domain Skew**: Overrepresentation of English business/support domains
2. **Synthetic Artifacts**: Template patterns may be detectable by models
3. **Annotator Background**: All annotators have technical backgrounds
4. **Task Simplification**: Real-world complexity reduced for tractability

### Mitigation Strategies
- Balanced class distributions
- Diverse phrasing and sentence structures
- Multiple domains within each task
- Human review of all synthetic examples

### Out-of-Scope
- Non-English languages (future work)
- Multimodal inputs (images, audio)
- Long-context tasks (> 500 tokens)
- Real-time/streaming evaluation

---

## Reproducibility

### Fixed Seeds
- **Data Generation**: seed=42
- **Evaluation Sampling**: seed=42 (set in EP)
- **Bootstrap CI**: seed=42 (1000 iterations)

### Versioning
- **Data Version**: v0.3.1
- **PCSL Version**: 0.3.1
- **Checksum**: SHA256 hashes in `fixtures/checksums.txt`

### Environment
- **Python**: 3.10+
- **Dependencies**: See `requirements.txt`
- **Docker**: See `Dockerfile` for full environment

---

## Usage

### Loading Fixtures

```python
import json

def load_fixtures(task_name):
    with open(f"fixtures/{task_name}/fixtures.jsonl") as f:
        fixtures = [json.loads(line) for line in f]
    with open(f"fixtures/{task_name}/labels.jsonl") as f:
        labels = [json.loads(line) for line in f]
    return fixtures, labels

fixtures, labels = load_fixtures("classification")
```

### Evaluation

```bash
# Single task
prompt-contracts run \
  --pd examples/classification/pd.json \
  --es examples/classification/es.json \
  --ep examples/classification/ep.json \
  --fixtures fixtures/classification/fixtures.jsonl \
  --labels fixtures/classification/labels.jsonl \
  --seed 42

# All tasks
make eval-full
```

---

## Ethical Considerations

### Privacy
- No real user data included
- All examples reviewed for PII
- Synthetic data generation follows ethical guidelines

### Representation
- Limited to English language
- Primarily Western/business contexts
- Does not represent global diversity

### Intended Use
- Academic research
- Benchmarking LLM contracts
- Reproducibility studies

### Prohibited Use
- Training commercial models without citation
- Claims of human-level performance
- High-stakes decisions without human oversight

---

## Updates and Maintenance

**Versioning**: Semantic versioning (MAJOR.MINOR.PATCH)
- **MAJOR**: Breaking changes to format or labels
- **MINOR**: New tasks or significant additions
- **PATCH**: Bug fixes, clarifications

**Update Frequency**: Quarterly reviews for quality and relevance

**Issue Tracking**: https://github.com/philippmelikidis/prompt-contracts/issues

---

## References

Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics*, 33(1), 159-174.

Fleiss, J. L. (1971). Measuring nominal scale agreement among many raters. *Psychological Bulletin*, 76(5), 378-382.

---

## Citation

```bibtex
@misc{promptcontracts2025,
  title={Prompt Contracts: Specification and Enforcement for LLM Interactions},
  author={Melikidis, Philippos},
  year={2025},
  url={https://github.com/philippmelikidis/prompt-contracts}
}
```

---

**Last Updated**: 2025-01-09
**Contact**: https://github.com/philippmelikidis/prompt-contracts/issues
